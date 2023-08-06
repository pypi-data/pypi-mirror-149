import asyncio
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

import orjson
import pandas as pd
from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import LogColor
from nautilus_trader.common.logging import Logger
from nautilus_trader.core.datetime import millis_to_nanos
from nautilus_trader.execution.messages import CancelAllOrders
from nautilus_trader.execution.messages import CancelOrder
from nautilus_trader.execution.messages import ModifyOrder
from nautilus_trader.execution.messages import SubmitOrder
from nautilus_trader.execution.messages import SubmitOrderList
from nautilus_trader.execution.reports import OrderStatusReport
from nautilus_trader.execution.reports import PositionStatusReport
from nautilus_trader.execution.reports import TradeReport
from nautilus_trader.model.enums import AccountType
from nautilus_trader.model.enums import LiquiditySide
from nautilus_trader.model.enums import OMSType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import OrderStatus
from nautilus_trader.model.enums import OrderType
from nautilus_trader.model.enums import PositionSide
from nautilus_trader.model.enums import TimeInForce
from nautilus_trader.model.enums import TimeInForceParser
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import ClientId
from nautilus_trader.model.identifiers import ClientOrderId
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
from nautilus_trader.model.orders.list import OrderList
from nautilus_trader.msgbus.bus import MessageBus

from nacre.adapters.zb.http.api.future_account import ZbFutureAccountHttpAPI
from nacre.adapters.zb.http.api.future_market import ZbFutureMarketHttpAPI
from nacre.adapters.zb.http.client import ZbHttpClient
from nacre.adapters.zb.http.error import ZbError
from nacre.adapters.zb.parsing import parse_account_balances_raw
from nacre.adapters.zb.parsing import parse_account_margins_raw
from nacre.adapters.zb.parsing import parse_future_order_status
from nacre.adapters.zb.parsing import parse_order_fill
from nacre.adapters.zb.parsing import parse_position
from nacre.adapters.zb.parsing import parse_zb_order_side
from nacre.adapters.zb.parsing import parse_zb_order_type
from nacre.adapters.zb.parsing import zb_order_params
from nacre.adapters.zb.providers import ZbInstrumentProvider
from nacre.adapters.zb.websocket.futures import ZbFuturesUserDataWebSocketClient
from nacre.live.execution_client import LiveExecutionClient


VALID_TIF = (TimeInForce.GTC, TimeInForce.FOK, TimeInForce.IOC)


class ZbFuturesExecutionClient(LiveExecutionClient):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        client: ZbHttpClient,
        name: str,
        account_id: AccountId,
        venue: Venue,
        oms_type: OMSType,
        msgbus: MessageBus,
        cache: Cache,
        clock: LiveClock,
        logger: Logger,
        instrument_provider: ZbInstrumentProvider,
        base_url_ws: Optional[str] = None,
    ):
        # HTTP API
        self._account_api = ZbFutureAccountHttpAPI(client=client)
        self._market_api = ZbFutureMarketHttpAPI(client=client)

        # Websocket API
        self._ws_user_api = ZbFuturesUserDataWebSocketClient(
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
        self._last_filled: Dict[VenueOrderId, Quantity] = {}

        # cache for position update
        self._position_side_by_client_order_id: Dict[ClientOrderId, PositionSide] = {}

        super().__init__(
            loop=loop,
            client_id=ClientId(name),
            venue=venue,
            oms_type=oms_type,
            instrument_provider=instrument_provider,
            account_type=AccountType.MARGIN,
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
            response = await self._account_api.get_account(future_account_type=1)  # Ignore QC
        except Exception as ex:
            self._log.exception("Error on connect", ex)
            return

        balances = self.parse_account_balances(response)
        margins = self.parse_account_margins(response)
        self._update_account_state(balances, margins)

        # Connect WebSocket clients
        await self._connect_websockets()

        self._set_connected(True)
        assert self.is_connected
        self._log.info("Connected.")

    async def _connect_websockets(self) -> None:
        kwargs = {"proxy": self._proxy} if self._proxy else {}
        await self._ws_user_api.connect(**kwargs)
        await asyncio.sleep(2)  # Wait for login, since login method in separate write coroutine
        await asyncio.gather(
            self._ws_user_api.subscribe_asset_update(),
            self._ws_user_api.subscribe_order_update(),
            self._ws_user_api.subscribe_position_update(),
        )
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
                client_order_id=order.client_order_id.value,
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
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
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
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
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

    def _handle_user_ws_message(self, raw: bytes):  # noqa: C901
        msg: Dict[str, Any] = orjson.loads(raw)
        data = msg.get("data")

        chan: Optional[str] = msg.get("channel")
        err: Optional[str] = msg.get("errorCode")

        if err:
            self._log.error(f"Subscribe failed for channel: {chan}, error: {err}")
            return
        if not chan:
            if msg.get("action") == "login" and data == "success":
                pass
            elif msg.get("action") == "pong":
                pass
            return

        if chan == "Fund.assetChange":
            self._handle_asset_update(data)
        elif chan == "Fund.balance":
            self._handle_asset_snapshot(data)
        elif chan == "Positions.change":
            self._handle_position_update(data)
        elif chan == "Trade.orderChange":
            self._handle_order_update(data)
        elif chan == "Trade.order":
            self._handle_order_submit(data)
        elif chan == "Trade.cancelOrder":
            self._handle_order_cancel(data)
        elif chan == "Trade.cancelAllOrders":
            self._handle_order_cancel_all(data)
        else:
            self._log.warning(f"Unrecognized websocket message type, msg {msg}")
            return

    def _handle_order_submit(self, data: Dict):
        venue_order_id = VenueOrderId(data["orderId"])
        client_order_id = ClientOrderId(data["orderCode"])

        order = self._cache.order(client_order_id)
        if order is None:
            self._log.error(
                f"Cannot handle order update: " f"order for {client_order_id} not found",
            )
            return

        self.generate_order_accepted(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=client_order_id,
            venue_order_id=venue_order_id,
            ts_event=self._clock.timestamp_ns(),
        )

    def _handle_order_cancel(self, data: str):
        venue_order_id = VenueOrderId(data)
        client_order_id = self._cache.client_order_id(venue_order_id)
        if client_order_id is None:
            return
        order = self._cache.order(client_order_id)
        self.generate_order_canceled(
            strategy_id=order.strategy_id,
            instrument_id=order.instrument_id,
            client_order_id=client_order_id,
            venue_order_id=venue_order_id,
            ts_event=self._clock.timestamp_ns(),
        )

    def _handle_order_cancel_all(self, data: List):
        pass

    def _handle_asset_snapshot(self, data: List[Dict]):
        balances = parse_account_balances_raw(self._instrument_provider, data)
        self._update_account_state(balances)

    def _handle_asset_update(self, data: Dict[str, Any]):
        pass

    def _handle_position_update(self, data: Dict[str, Any]):
        pass

    def _handle_order_update(self, data: Dict[str, Any]):  # noqa: C901
        self._log.debug(f"Received order update {data}")

        venue_order_id = VenueOrderId(data["id"])
        client_order_id_str = data.get("orderCode")
        if client_order_id_str is None:
            self._log.warning(f"Cannot fill un-cached order with {repr(venue_order_id)}")
            return
        client_order_id = ClientOrderId(client_order_id_str)

        strategy_id = self._cache.strategy_id_for_order(client_order_id)
        if strategy_id is None:
            self._log.error(
                f"Cannot handle order update: " f"strategy ID for {client_order_id} not found",
            )
            return
        ts_event: int = millis_to_nanos(int(data["modifyTime"]))

        instrument_id = self._instrument_provider.find_instrument_id_by_local_market_id(
            data["marketId"]
        )

        order_status = data["showStatus"]
        if order_status == 1:  # 1 for accepted
            self.generate_order_accepted(
                strategy_id=strategy_id,
                instrument_id=instrument_id,
                client_order_id=client_order_id,
                venue_order_id=venue_order_id,
                ts_event=ts_event,
            )
        elif order_status == 2 or order_status == 3:  # 2 for partial filled, 3 for filled
            instrument: Instrument = self._instrument_provider.find(instrument_id)
            order_type = parse_zb_order_type(data["action"])

            # calculate last qty
            current_filled = Quantity.from_str(data["tradeAmount"])
            if venue_order_id not in self._last_filled:
                self._last_filled[venue_order_id] = current_filled
                last_qty = current_filled
            else:
                last_qty = Quantity(
                    current_filled - self._last_filled[venue_order_id], instrument.size_precision
                )
                self._last_filled[venue_order_id] = current_filled

            # Zb future might push same event more than once
            if last_qty == 0:
                self._log.warning(f"ZbFuture pushed same {client_order_id} fill event again")
                return

            # FIX: get commission and liquidity_side, hard code for now
            if order_type == OrderType.MARKET:
                commission_fee = (
                    Decimal(data["avgPrice"]) * last_qty.as_decimal()
                ) * instrument.taker_fee
                liquidity_side = LiquiditySide.TAKER
            else:
                commission_fee = (
                    Decimal(data["avgPrice"]) * last_qty.as_decimal()
                ) * instrument.maker_fee
                liquidity_side = LiquiditySide.MAKER
            commission = Money(commission_fee, instrument.quote_currency)

            venue_position_id = None
            # TODO: Avoid same side order generate 2 different position_id
            if (
                self.oms_type == OMSType.HEDGING
                and client_order_id in self._position_side_by_client_order_id
            ):

                side = self._position_side_by_client_order_id[client_order_id]
                open_positions = self._cache.positions_open(
                    instrument_id=instrument_id, strategy_id=strategy_id
                )
                position = next(
                    filter(lambda position: position.side == side, open_positions), None
                )
                if position is not None:
                    venue_position_id = position.id

            self.generate_order_filled(
                strategy_id=strategy_id,
                instrument_id=instrument_id,
                client_order_id=client_order_id,
                venue_order_id=venue_order_id,
                venue_position_id=venue_position_id,
                trade_id=TradeId(
                    self._uuid_factory.generate().value,
                ),  # no trade id returned, use uuid instead
                order_side=parse_zb_order_side(data["type"]),
                order_type=order_type,
                last_qty=last_qty,
                last_px=Price.from_str(data["avgPrice"]),
                quote_currency=instrument.quote_currency,
                commission=commission,  # see above fix
                liquidity_side=liquidity_side,  # see above fix
                ts_event=ts_event,
            )
        elif order_status == 4:  # 4 for canceling
            self.generate_order_pending_cancel(
                strategy_id=strategy_id,
                instrument_id=instrument_id,
                client_order_id=client_order_id,
                venue_order_id=venue_order_id,
                ts_event=ts_event,
            )
        elif (
            order_status == 5 or order_status == 7
        ):  # 5 for canceled, 7 for partial filled partial cancel
            # Some order canceled immediately without "showStatus" = 1 pushed
            if (
                order_status == 5
                and self._cache.order(client_order_id).status == OrderStatus.SUBMITTED
            ):
                self.generate_order_accepted(
                    strategy_id=strategy_id,
                    instrument_id=instrument_id,
                    client_order_id=client_order_id,
                    venue_order_id=venue_order_id,
                    ts_event=ts_event,
                )
            self.generate_order_canceled(
                strategy_id=strategy_id,
                instrument_id=instrument_id,
                client_order_id=client_order_id,
                venue_order_id=venue_order_id,
                ts_event=ts_event,
            )
        elif order_status == 6:  # 6 for cancel failed
            self.generate_order_cancel_rejected(
                strategy_id=strategy_id,
                instrument_id=instrument_id,
                client_order_id=client_order_id,
                venue_order_id=venue_order_id,
                reason="",  # type: ignore  # TODO(cs): Improve errors
                ts_event=ts_event,
            )

    # -- COMMAND HANDLERS --------------------------------------------------------------------------

    def submit_order(self, command: SubmitOrder) -> None:
        order: Order = command.order
        if order.type == OrderType.STOP_MARKET:
            self._log.error(
                "Cannot submit order: "
                "STOP_MARKET orders not supported by the exchange for zb FUTURE markets. "
                "Use any of MARKET, LIMIT, STOP_LIMIT."
            )
            return
        elif order.type == OrderType.STOP_LIMIT:
            self._log.error(
                "Cannot submit order: "
                "STOP_LIMIT orders not supported by the exchange for zb FUTURE markets. "
                "Use any of MARKET, LIMIT, STOP_LIMIT."
            )
            return
        if order.time_in_force not in VALID_TIF:
            self._log.error(
                f"Cannot submit order: "
                f"{TimeInForceParser.to_str_py(order.time_in_force)} "
                f"not supported by the exchange. Use any of {VALID_TIF}.",
            )
            return
        self._loop.create_task(self._submit_order(command))

    def submit_order_list(self, command: SubmitOrderList) -> None:
        order_list: OrderList = command.list
        self._loop.create_task(self._submit_order_list(order_list))

    def modify_order(self, command: ModifyOrder) -> None:
        self._log.error(  # pragma: no cover
            "Cannot modify order: Not supported by the exchange.",
        )

    def cancel_order(self, command: CancelOrder) -> None:
        self._loop.create_task(self._cancel_order(command))

    def cancel_all_orders(self, command: CancelAllOrders) -> None:
        self._loop.create_task(self._cancel_all_order(command))

    async def _submit_order(self, command: SubmitOrder) -> None:
        order: Order = command.order
        self._log.debug(f"Submitting {order}.")

        position = None
        position_id = command.position_id
        if position_id is not None:
            position = self._cache.position(position_id)
            if position is None:
                self._log.error(f"Position {position_id} not found")
                return
        elif (
            self.oms_type == OMSType.HEDGING
        ):  # When not specify position_id, open position with same side
            if order.side == OrderSide.BUY:
                side = PositionSide.LONG
            else:
                side = PositionSide.SHORT
            self._position_side_by_client_order_id[order.client_order_id] = side

        # Generate event here to ensure correct ordering of events
        self.generate_order_submitted(
            strategy_id=command.strategy_id,
            instrument_id=command.instrument_id,
            client_order_id=order.client_order_id,
            ts_event=self._clock.timestamp_ns(),
        )

        try:
            kwargs = zb_order_params(order, self.oms_type, position)
            response = await self._account_api.new_order(**kwargs)
            self._log.debug(f"Submit order response {response}")
            # Submit order through REST & Websocket same time
            await self._ws_user_api.new_order(**kwargs)
        except ZbError as ex:
            self.generate_order_rejected(
                strategy_id=command.strategy_id,
                instrument_id=command.instrument_id,
                client_order_id=order.client_order_id,
                reason=ex.message,
                ts_event=self._clock.timestamp_ns(),  # TODO(cs): Parse from response
            )
        except Exception as ex:
            self._log.error(f"Error occurs in submit order: {ex}, verifying order ...")
            await self._verify_order_status(order)

    async def _submit_order_list(self, order_list: OrderList) -> None:
        batch_params = []
        for order in order_list.orders:
            if order.contingency_ids:  # TODO(cs): Implement
                self._log.warning(f"Cannot yet handle contingency orders, {order}.")
            params = zb_order_params(order, self.oms_type)
            params["orderCode"] = params.pop("client_order_id")
            batch_params.append(params)

        response = await self._account_api.new_batch_order(orders=batch_params)
        self._log.debug(f"Submit batch order response {response}", LogColor.YELLOW)

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
            if order.venue_order_id is not None:
                response = await self._account_api.cancel_order(
                    symbol=order.instrument_id.symbol.value,
                    order_id=order.venue_order_id.value,
                )
            else:
                response = await self._account_api.cancel_order(
                    symbol=order.instrument_id.symbol.value,
                    client_order_id=order.client_order_id.value,
                )
            # Cancel order through REST & Websocket same time
            await self._ws_user_api.cancel_order(
                symbol=order.instrument_id.symbol.value,
                client_order_id=order.client_order_id.value,
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
                reason=message,  # type: ignore  # TODO(cs): Improve errors
                ts_event=self._clock.timestamp_ns(),  # TODO(cs): Parse from response
            )

    async def _cancel_all_order(self, command: CancelAllOrders) -> None:
        self._log.debug(f"Canceling all orders for {command.instrument_id.value}.")

        # Cancel all in-flight orders
        inflight_orders = self._cache.orders_inflight(
            instrument_id=command.instrument_id,
            strategy_id=command.strategy_id,
        )
        for order in inflight_orders:
            self.generate_order_pending_cancel(
                strategy_id=order.strategy_id,
                instrument_id=order.instrument_id,
                client_order_id=order.client_order_id,
                venue_order_id=order.venue_order_id,
                ts_event=self._clock.timestamp_ns(),
            )

        # Cancel all working orders
        open_orders = self._cache.orders_open(
            instrument_id=command.instrument_id,
            strategy_id=command.strategy_id,
        )

        for order in open_orders:
            self.generate_order_pending_cancel(
                strategy_id=order.strategy_id,
                instrument_id=order.instrument_id,
                client_order_id=order.client_order_id,
                venue_order_id=order.venue_order_id,
                ts_event=self._clock.timestamp_ns(),
            )
        try:
            response = await self._account_api.cancel_open_orders(
                command.instrument_id.symbol.value
            )
            # # Cancel order through REST & Websocket same time
            # await self._ws_user_api.cancel_open_orders(command.instrument_id.symbol.value)
            self._log.debug(f"Cancel all order response {response}")
        except ZbError as ex:
            self._log.error(ex)  # type: ignore  # TODO(cs): Improve errors
        except Exception as ex:
            self._log.exception("Error on cancel all orders", ex)

    async def _get_order_status_reports(
        self,
        instrument_id: InstrumentId = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        open_only: bool = False,
    ) -> List[OrderStatusReport]:
        reports: List[OrderStatusReport] = []

        if instrument_id is None:
            self._log.warning("InstrumentId not specified, zb does not support all orders query")
            return reports

        try:
            if open_only:
                response: Dict[str, Any] = await self._account_api.get_open_orders(
                    symbol=instrument_id.symbol.value,
                )
            else:
                response = await self._account_api.get_all_orders(
                    symbol=instrument_id.symbol.value,
                )
        except ZbError as ex:
            self._log.error(ex.message)  # type: ignore  # TODO(cs): Improve errors
            return []

        if response:
            for data in response["data"]["list"]:
                created_at = pd.to_datetime(data["createTime"], unit="ms")
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

                report: OrderStatusReport = self.parse_order_status(
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
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[TradeReport]:
        reports: List[TradeReport] = []
        if instrument_id is None:
            return reports

        try:
            response: Dict[str, Any] = await self._account_api.get_history_trades(
                symbol=instrument_id.symbol.value,
                start_time=int(start.timestamp() * 1000) if start is not None else None,
                end_time=int(end.timestamp() * 1000) if end is not None else None,
            )
        except ZbError as ex:
            self._log.error(ex.message)  # type: ignore  # TODO(cs): Improve errors
            return []

        if response:
            for data in response["data"]["list"]:
                # Apply filter (FTX filters not working)
                created_at = pd.to_datetime(data["createTime"], unit="ms")
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

                report: TradeReport = parse_order_fill(
                    account_id=self.account_id,
                    instrument=instrument,
                    data=data,
                    report_id=self._uuid_factory.generate(),
                    ts_init=self._clock.timestamp_ns(),
                )

                self._log.debug(f"Received {report}.")
                reports.append(report)

        return reports

    async def _get_position_status_report(
        self,
        instrument_id: InstrumentId = None,
        start: datetime = None,
        end: datetime = None,
    ) -> List[PositionStatusReport]:
        try:
            response: Dict[str, Any] = await self._account_api.get_positions()
        except ZbError as ex:
            self._log.error(ex.message)  # type: ignore  # TODO(cs): Improve errors
            return []

        reports = []
        if response:
            for data in response["data"]:
                # Get instrument
                instrument_id = instrument_id or self._get_cached_instrument_id(data)
                instrument = self._instrument_provider.find(instrument_id)
                if instrument is None:
                    self._log.error(
                        f"Cannot generate order status report: "
                        f"no instrument found for {instrument_id}.",
                    )
                    continue

                report: PositionStatusReport = parse_position(
                    account_id=self.account_id,
                    instrument=instrument,
                    data=data,
                    report_id=self._uuid_factory.generate(),
                    ts_init=self._clock.timestamp_ns(),
                )

                if report.quantity == 0:
                    continue  # Flat position
                self._log.debug(f"Received {report}.")
                reports.append(report)
        return reports

    # -- Others -------------------------------------------------------------------------

    def parse_account_balances(self, response: Dict) -> List[AccountBalance]:
        return parse_account_balances_raw(self._instrument_provider, response["data"]["assets"])

    def parse_account_margins(self, response: Dict) -> List[MarginBalance]:
        return parse_account_margins_raw(self._instrument_provider, response["data"]["accounts"])

    def parse_order_status(self, account_id, instrument, data, report_id, ts_init):
        return parse_future_order_status(account_id, instrument, data["data"], report_id, ts_init)

    def _get_cached_instrument_id(self, response: Dict) -> InstrumentId:
        return self._instrument_provider.find_instrument_id_by_local_market_id(response["marketId"])
