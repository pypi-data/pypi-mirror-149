import asyncio
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import orjson
import pandas as pd
from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import LogColor
from nautilus_trader.common.logging import Logger
from nautilus_trader.core.datetime import millis_to_nanos

# from nautilus_trader.model.commands.trading import CancelAllOrders
from nautilus_trader.execution.messages import CancelOrder
from nautilus_trader.execution.messages import SubmitOrder
from nautilus_trader.execution.reports import OrderStatusReport
from nautilus_trader.execution.reports import PositionStatusReport
from nautilus_trader.execution.reports import TradeReport
from nautilus_trader.model.enums import AccountType
from nautilus_trader.model.enums import OMSType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import OrderType
from nautilus_trader.model.enums import TimeInForce
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import ClientId
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import TradeId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.identifiers import VenueOrderId
from nautilus_trader.model.instruments.base import Instrument
from nautilus_trader.model.objects import AccountBalance
from nautilus_trader.model.objects import MarginBalance
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity
from nautilus_trader.model.orders.base import Order
from nautilus_trader.model.orders.limit import LimitOrder
from nautilus_trader.msgbus.bus import MessageBus

from nacre.adapters.zb.common import format_websocket_user_market
from nacre.adapters.zb.http.api.spot_account import ZbSpotAccountHttpAPI
from nacre.adapters.zb.http.api.spot_market import ZbSpotMarketHttpAPI
from nacre.adapters.zb.http.client import ZbHttpClient
from nacre.adapters.zb.http.error import ZbError
from nacre.adapters.zb.parsing import parse_spot_account_balances_raw
from nacre.adapters.zb.parsing import parse_spot_order_status
from nacre.adapters.zb.parsing import parse_zb_spot_liquidity_side
from nacre.adapters.zb.parsing import parse_zb_spot_order_side
from nacre.adapters.zb.providers import ZbInstrumentProvider
from nacre.adapters.zb.websocket.spot import ZbSpotUserDataWebSocket
from nacre.live.execution_client import LiveExecutionClient


class ZbSpotExecutionClient(LiveExecutionClient):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        client: ZbHttpClient,
        market_client: ZbHttpClient,
        name: str,
        account_id: AccountId,
        venue: Venue,
        msgbus: MessageBus,
        cache: Cache,
        clock: LiveClock,
        logger: Logger,
        instrument_provider: ZbInstrumentProvider,
        base_url_ws: Optional[str] = None,
    ):
        # HTTP API
        self._account_api = ZbSpotAccountHttpAPI(client=client)
        self._market_api = ZbSpotMarketHttpAPI(client=market_client)

        # WebSocket API
        self._ws_user_api = ZbSpotUserDataWebSocket(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=self._handle_user_ws_message,
            key=client.api_key,
            hashed_secret=client.hashed_secret,
            base_url=base_url_ws,
        )

        self._client = client
        self._proxy = client._proxy
        # Hot caches
        self._instrument_ids: Dict[str, InstrumentId] = {}
        self._order_types: Dict[VenueOrderId, OrderType] = {}

        super().__init__(
            loop=loop,
            client_id=ClientId(name),
            venue=venue,
            oms_type=OMSType.NETTING,
            instrument_provider=instrument_provider,
            account_type=AccountType.CASH,
            base_currency=None,
            msgbus=msgbus,
            cache=cache,
            clock=clock,
            logger=logger,
            config={"name": f"ZbExecClient-{name}"},
        )

        self._set_account_id(account_id)
        self._set_venue(Venue(account_id.issuer))

    def connect(self) -> None:
        self._log.info("Connecting...")
        self._loop.create_task(self._connect())

    def disconnect(self) -> None:
        self._log.info("Disconnecting...")
        self._loop.create_task(self._disconnect())

    async def _connect(self) -> None:
        if not self._client.connected:
            await self._client.connect()
        try:
            await self._instrument_provider.initialize()
            response = await self._account_api.get_account()
        except Exception as ex:
            self._log.exception("Error on connect", ex)
            return

        self._authenticate_api_key(response)
        balances = self.parse_account_balances(response)
        self._update_account_state(balances)

        # Connect WebSocket clients
        await self._connect_websockets()

        self._set_connected(True)
        assert self.is_connected
        self._log.info("Connected.")

    async def _connect_websockets(self) -> None:
        kwargs = {"proxy": self._proxy} if self._proxy else {}
        await self._ws_user_api.connect(**kwargs)

        await self._ws_user_api.subscribe_asset_snapshot()
        await self._subscribe_order_update_on_selected_markets()
        # await self._ws_user_api.logged_in()

    async def _disconnect(self) -> None:
        # Disconnect WebSocket clients
        if self._ws_user_api.is_connected:
            await self._ws_user_api.disconnect()

        if self._client.connected:
            await self._client.disconnect()

        self._set_connected(False)
        self._log.info("Disconnected.")

    def _update_account_state(
        self, balances: List[AccountBalance], margins: Optional[List[MarginBalance]] = None
    ) -> None:
        if not balances:
            return

        self.generate_account_state(
            balances=balances,
            margins=[] if margins is None else margins,
            reported=True,
            ts_event=self._clock.timestamp_ns(),  # zb account doesn't provide updateTime
        )

    async def _verify_order_status(self, order: Order):
        try:
            response = await self._account_api.get_order(
                symbol=order.instrument_id.symbol.value,
                client_order_id=order.client_order_id,
            )
            self._log.debug(f"Fetched order status: {response}")

            venue_order_id = VenueOrderId(response["id"])
            self.generate_order_accepted(
                strategy_id=order.strategy_id,
                instrument_id=order.instrument_id,
                client_order_id=order.client_order_id,
                venue_order_id=venue_order_id,
                ts_event=self._clock.timestamp_ns(),
            )
        except ZbError as ex:
            self.generate_order_rejected(
                strategy_id=order.strategy_id,
                instrument_id=order.instrument_id,
                client_order_id=order.client_order_id,
                reason=ex.message,
                ts_event=self._clock.timestamp_ns(),
            )

    # -- EXECUTION REPORTS -------------------------------------------------------------------------

    async def generate_order_status_report(
        self,
        venue_order_id: VenueOrderId = None,
    ) -> Optional[OrderStatusReport]:
        if venue_order_id is None:
            return None
        return None

        # ZB spot get order require symbol

        # try:
        #     response = await self._account_api.get_order(order_id=venue_order_id.value)
        # except ZbError as ex:
        #     self._log.error(ex.message)  # type: ignore  # TODO(cs): Improve errors
        #     return None
        #
        # # Get instrument
        # instrument_id: InstrumentId = self._get_cached_instrument_id(response)
        # instrument = self._instrument_provider.find(instrument_id)
        # if instrument is None:
        #     self._log.error(
        #         f"Cannot generate order status report: "
        #         f"no instrument found for {instrument_id}.",
        #     )
        #     return None
        #
        # return self.parse_order_status(
        #     account_id=self.account_id,
        #     instrument=instrument,
        #     data=response,
        #     report_id=self._uuid_factory.generate(),
        #     ts_init=self._clock.timestamp_ns(),
        # )

    async def generate_order_status_reports(
        self,
        instrument_id: InstrumentId = None,
        start: datetime = None,
        end: datetime = None,
        open_only: bool = False,
    ) -> List[OrderStatusReport]:
        self._log.info(f"Generating OrderStatusReports for {self.id}...")

        reports: List[OrderStatusReport] = []
        reports += await self._get_order_status_reports(
            instrument_id=instrument_id,
            start=start,
            end=end,
            open_only=open_only,
        )

        len_reports = len(reports)
        plural = "" if len_reports == 1 else "s"
        self._log.info(f"Generated {len(reports)} OrderStatusReport{plural}.")

        return reports

    async def generate_trade_reports(
        self,
        instrument_id: InstrumentId = None,
        venue_order_id: VenueOrderId = None,
        start: datetime = None,
        end: datetime = None,
    ) -> List[TradeReport]:
        self._log.info(f"Generating TradeReports for {self.id}...")

        # reports: List[TradeReport] = []

        reports = await self._get_trade_reports(
            instrument_id=instrument_id,
            venue_order_id=venue_order_id,
            start=start,
            end=end,
        )

        reports = sorted(reports, key=lambda x: x.trade_id)

        len_reports = len(reports)
        plural = "" if len_reports == 1 else "s"
        self._log.info(f"Generated {len(reports)} TradeReport{plural}.")

        return reports

    async def generate_position_status_reports(
        self,
        instrument_id: InstrumentId = None,
        start: datetime = None,
        end: datetime = None,
    ) -> List[PositionStatusReport]:

        self._log.info(f"Generating PositionStatusReports for {self.id}...")
        return []

    async def _subscribe_order_update_on_selected_markets(self):
        # ZB spot require subscribe each market specifically
        # TODO: better way to escape zb ws subscribe rate limit 60 sub/sec
        for market in self._instrument_provider.list_local_market_ids():
            if self._instrument_provider._filters:
                if not re.match(self._instrument_provider._filters["subscribe"], market):
                    self._log.debug(f"Ignored order update on {market}")
                    continue
            await asyncio.sleep(1 / 60)
            await self._ws_user_api.subscribe_order_update(f"{market}default")

    def parse_account_balances(self, response: Dict) -> List[AccountBalance]:
        return parse_spot_account_balances_raw(
            self._instrument_provider, response["result"]["coins"]
        )

    def _get_cached_instrument_id(self, response: Dict) -> InstrumentId:
        return self._instrument_provider.find_instrument_id_by_local_market_id(response["currency"])

    def _authenticate_api_key(self, response: Dict[str, Any]) -> None:
        if response["entrustPerm"]:
            self._log.info("Zb API key authenticated.", LogColor.GREEN)
            self._log.info(f"API key {self._client.api_key} has trading permissions.")
        else:
            self._log.error("Zb API key does not have trading permissions.")

    def _handle_user_ws_message(self, raw: bytes):
        try:
            msg: Dict[str, Any] = orjson.loads(raw)
        except orjson.JSONDecodeError:
            plain_text = raw.decode()
            if plain_text == "pong":
                return
            else:
                self._log.error(f"Unknown ws message received: {plain_text}")
                return

        chan: Optional[str] = msg.get("channel")
        code = msg.get("code")
        if code is not None and code != 1000:
            self._log.error(f"Error subscribe: {msg}")
            return

        if chan == "push_user_incr_record":
            self._handle_order_update(msg)
        elif chan == "push_user_asset":
            self._handle_asset_update(msg)
        else:
            self._log.warning(f"Unrecognized websocket message type, msg {msg}")
            return

    def _handle_order_update(self, data: Dict[str, Any]):
        self._log.debug(f"Received order update {data}")
        record: List = data["record"]

        # Parse client order ID
        venue_order_id = VenueOrderId(record[0])
        client_order_id = self._cache.client_order_id(venue_order_id)
        if client_order_id is None:
            self._log.warning(f"Cannot fill un-cached order with {repr(venue_order_id)}")
            return

        # Fetch strategy ID
        strategy_id = self._cache.strategy_id_for_order(client_order_id)
        if strategy_id is None:
            self._log.error(
                f"Cannot handle order update: " f"strategy ID for {client_order_id} not found",
            )
            return

        ts_event: int = millis_to_nanos(record[16])

        # Parse instrument ID
        zb_symbol = format_websocket_user_market(data["market"])
        instrument_id = self._instrument_provider.find_instrument_id_by_local_market_id(zb_symbol)

        order_status = record[7]
        if order_status == 1:  # 1 for cancel
            self.generate_order_canceled(
                strategy_id=strategy_id,
                instrument_id=instrument_id,
                client_order_id=client_order_id,
                venue_order_id=venue_order_id,
                ts_event=ts_event,
            )
        elif order_status == 2 or (
            order_status == 3 and record[3] > 0
        ):  # 2 for filled/partial filled complete
            instrument: Instrument = self._instrument_provider.find(instrument_id)

            self.generate_order_filled(
                strategy_id=strategy_id,
                instrument_id=instrument_id,
                client_order_id=client_order_id,
                venue_order_id=venue_order_id,
                venue_position_id=None,
                trade_id=TradeId(str(record[13])),
                order_side=parse_zb_spot_order_side(record[5]),
                order_type=OrderType.LIMIT,
                last_qty=Quantity.from_str(str(record[15])),
                last_px=Price.from_str(str(record[14])),
                quote_currency=instrument.quote_currency,
                commission=Money(record[8], instrument.quote_currency),
                liquidity_side=parse_zb_spot_liquidity_side(record[5]),
                ts_event=ts_event,
            )
        elif order_status == 0 or order_status == 3:  # 0 for pending, 3 for partial fill
            self.generate_order_accepted(
                strategy_id=strategy_id,
                instrument_id=instrument_id,
                client_order_id=client_order_id,
                venue_order_id=venue_order_id,
                ts_event=ts_event,
            )

    def _handle_asset_update(self, data: Dict):
        balances = parse_spot_account_balances_raw(self._instrument_provider, data["coins"])
        self._update_account_state(balances)

    def submit_order(self, command: SubmitOrder) -> None:
        order: Order = command.order
        self._loop.create_task(self._submit_order(order))

    def cancel_order(self, command: CancelOrder) -> None:
        self._loop.create_task(self._cancel_order(command))

    # def cancel_all_orders(self, command: CancelAllOrders) -> None:
    #     self._loop.create_task(self._cancel_all_order(command))

    async def _submit_order(self, order: Order) -> None:
        self._log.debug(f"Submitting {order}.")

        if order.type != OrderType.LIMIT:
            self._log.error(
                "Cannot submit order: "
                f"{order.type} orders not supported by the exchange for SPOT markets. "
                "Only LIMIT supported."
            )
            return

        # Generate event here to ensure correct ordering of events
        self.generate_order_submitted(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=order.client_order_id,
            ts_event=self._clock.timestamp_ns(),
        )

        try:
            response = await self._submit_limit_order(order)
            self._log.debug(f"Submit order response {response}")
            venue_order_id = VenueOrderId(response["id"])
            self.generate_order_accepted(
                strategy_id=order.strategy_id,
                instrument_id=order.instrument_id,
                client_order_id=order.client_order_id,
                venue_order_id=venue_order_id,
                ts_event=self._clock.timestamp_ns(),
            )
        except ZbError as ex:
            self.generate_order_rejected(
                strategy_id=order.strategy_id,
                instrument_id=order.instrument_id,
                client_order_id=order.client_order_id,
                reason=ex.message,
                ts_event=self._clock.timestamp_ns(),
            )
        except Exception as ex:
            self._log.error(f"Error occurs in submit order: {ex}, verifying order ...")
            await self._verify_order_status(order)

    async def _submit_limit_order(self, order: LimitOrder) -> Dict:
        order_type = None
        if order.is_post_only:
            order_type = 1
        elif order.time_in_force == TimeInForce.IOC:
            order_type = 2

        return await self._account_api.order(
            amount=order.quantity.as_double(),
            currency=order.instrument_id.symbol.value,
            customer_order_id=order.client_order_id.value,
            price=order.price.as_double(),
            trade_type=1 if order.side == OrderSide.BUY else 0,
            order_type=order_type,
        )

    async def _cancel_order(self, order: CancelOrder) -> None:
        self._log.debug(f"Canceling order {order.client_order_id.value}.")

        self.generate_order_pending_cancel(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=order.client_order_id,
            venue_order_id=order.venue_order_id,
            ts_event=self._clock.timestamp_ns(),
        )

        try:
            response = await self._account_api.cancel_order(
                currency=order.instrument_id.symbol.value,
                id=order.venue_order_id.value,
            )
            self._log.debug(f"Cancel order response {response}")
        except Exception as ex:
            if isinstance(ex, ZbError):
                message = ex.message
            else:
                message = repr(ex)
                self._log.exception("Error on cancel order", ex)
            self.generate_order_cancel_rejected(
                strategy_id=order.strategy_id,
                instrument_id=order.instrument_id,
                client_order_id=order.client_order_id,
                venue_order_id=order.venue_order_id,
                reason=message,
                ts_event=self._clock.timestamp_ns(),  # TODO(cs): Parse from response
            )

    async def _get_order_status_reports(
        self,
        instrument_id: InstrumentId = None,
        start: datetime = None,
        end: datetime = None,
        open_only: bool = False,
    ) -> List[OrderStatusReport]:
        reports: List[OrderStatusReport] = []

        if instrument_id is None:
            self._log.warning("InstrumentId not specified, zb does not support all orders query")
            return reports

        try:
            if open_only:
                response: List[
                    Dict[str, Any]
                ] = await self._account_api.get_unfinished_orders_ignore_trade_type(
                    currency=instrument_id.symbol.value,
                )
            else:
                response = await self._account_api.get_orders_ignore_trade_type(
                    currency=instrument_id.symbol.value,
                )
        except ZbError as ex:
            self._log.error(ex.message)  # type: ignore  # TODO(cs): Improve errors
            return []

        if response:
            for data in response:
                created_at = pd.to_datetime(data["trade_date"], unit="ms")
                if start is not None and created_at < start:
                    continue
                if end is not None and created_at > end:
                    continue

                # Get instrument
                instrument_id = instrument_id or self._get_cached_instrument_id(data)
                instrument = self._instrument_provider.find(instrument_id)
                if instrument is None:
                    self._log.error(
                        f"Cannot generate order status report: "
                        f"no instrument found for {instrument_id}.",
                    )
                    continue

                report: OrderStatusReport = parse_spot_order_status(
                    account_id=self.account_id,
                    instrument=instrument,
                    data=data,
                    report_id=self._uuid_factory.generate(),
                    ts_init=self._clock.timestamp_ns(),
                )

                self._log.debug(f"Received {report}.")
                reports.append(report)

        return reports

    async def _get_trade_reports(
        self,
        instrument_id: InstrumentId = None,
        venue_order_id: VenueOrderId = None,
        start: datetime = None,
        end: datetime = None,
    ) -> List[TradeReport]:
        return []  # Zb spot does not provide trade detail

    async def _get_position_status_report(
        self,
        instrument_id: InstrumentId = None,
        start: datetime = None,
        end: datetime = None,
    ) -> List[PositionStatusReport]:
        return []
