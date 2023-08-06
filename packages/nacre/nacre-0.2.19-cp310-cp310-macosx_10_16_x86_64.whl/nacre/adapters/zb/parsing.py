import time
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from nautilus_trader.common.providers import InstrumentProvider
from nautilus_trader.core.datetime import millis_to_nanos
from nautilus_trader.core.datetime import secs_to_nanos
from nautilus_trader.core.uuid import UUID4
from nautilus_trader.execution.reports import OrderStatusReport
from nautilus_trader.execution.reports import PositionStatusReport
from nautilus_trader.execution.reports import TradeReport
from nautilus_trader.model.currency import Currency
from nautilus_trader.model.data.bar import BarSpecification
from nautilus_trader.model.data.bar import BarType
from nautilus_trader.model.data.base import DataType
from nautilus_trader.model.data.base import GenericData
from nautilus_trader.model.data.tick import TradeTick
from nautilus_trader.model.enums import AggregationSource
from nautilus_trader.model.enums import AggressorSide
from nautilus_trader.model.enums import BarAggregation
from nautilus_trader.model.enums import BookAction
from nautilus_trader.model.enums import BookType
from nautilus_trader.model.enums import CurrencyType
from nautilus_trader.model.enums import LiquiditySide
from nautilus_trader.model.enums import OMSType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import OrderStatus
from nautilus_trader.model.enums import OrderType
from nautilus_trader.model.enums import PositionSide
from nautilus_trader.model.enums import PriceType
from nautilus_trader.model.enums import TimeInForce
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import ClientOrderId
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import PositionId
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.identifiers import TradeId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.identifiers import VenueOrderId
from nautilus_trader.model.instruments.base import Instrument
from nautilus_trader.model.instruments.crypto_perpetual import CryptoPerpetual
from nautilus_trader.model.instruments.currency_pair import CurrencyPair
from nautilus_trader.model.objects import AccountBalance
from nautilus_trader.model.objects import MarginBalance
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity
from nautilus_trader.model.orderbook.data import Order
from nautilus_trader.model.orderbook.data import OrderBookDelta
from nautilus_trader.model.orderbook.data import OrderBookDeltas
from nautilus_trader.model.orderbook.data import OrderBookSnapshot
from nautilus_trader.model.orders.limit import LimitOrder
from nautilus_trader.model.orders.market import MarketOrder
from nautilus_trader.model.position import Position

from nacre.adapters.zb.data_types import ZbBar
from nacre.adapters.zb.data_types import ZbTicker
from nacre.model.data.tick import MarkTick


def parse_mark_price(instrument_id: InstrumentId, price: str, ts_init: int) -> MarkTick:
    tick = MarkTick(
        instrument_id=instrument_id,
        price=Price.from_str(price),
        ts_event=ts_init,
        ts_init=ts_init,
    )
    return GenericData(
        data_type=DataType(MarkTick, metadata={"instrument_id": instrument_id}),
        data=tick,
    )


def parse_book_snapshot_ws(
    instrument_id: InstrumentId, msg: Dict, ts_init: int
) -> OrderBookSnapshot:
    ts_event: int = ts_init

    return OrderBookSnapshot(
        instrument_id=instrument_id,
        book_type=BookType.L2_MBP,
        bids=[[float(o[0]), float(o[1])] for o in msg.get("bids", [])],
        asks=[[float(o[0]), float(o[1])] for o in msg.get("asks", [])],
        ts_event=ts_event,
        ts_init=ts_init,
        update_id=int(msg.get("time")),
    )


def parse_diff_depth_stream_ws(
    instrument_id: InstrumentId, msg: Dict, ts_init: int
) -> OrderBookDeltas:
    ts_event: int = ts_init
    update_id: int = int(msg["time"])

    bid_deltas = [
        parse_book_delta_ws(instrument_id, OrderSide.BUY, d, ts_event, ts_init, update_id)
        for d in msg.get("bids", [])
    ]
    ask_deltas = [
        parse_book_delta_ws(instrument_id, OrderSide.SELL, d, ts_event, ts_init, update_id)
        for d in msg.get("asks", [])
    ]

    return OrderBookDeltas(
        instrument_id=instrument_id,
        book_type=BookType.L2_MBP,
        deltas=bid_deltas + ask_deltas,
        ts_event=ts_event,
        ts_init=ts_init,
        update_id=update_id,
    )


def parse_book_delta_ws(
    instrument_id: InstrumentId,
    side: OrderSide,
    delta: Tuple[str, str],
    ts_event: int,
    ts_init: int,
    update_id: int,
) -> OrderBookDelta:
    price = float(delta[0])
    size = float(delta[1])

    order = Order(
        price=price,
        size=size,
        side=side,
    )

    return OrderBookDelta(
        instrument_id=instrument_id,
        book_type=BookType.L2_MBP,
        action=BookAction.UPDATE if size > 0.0 else BookAction.DELETE,
        order=order,
        ts_event=ts_event,
        ts_init=ts_init,
        update_id=update_id,
    )


def parse_spot_ticker_ws(
    instrument_id: InstrumentId, msg: Dict[str, str], ts_init: int
) -> ZbTicker:
    return ZbTicker(
        instrument_id=instrument_id,
        price_change=Decimal(msg["riseRate"]),
        last_price=Decimal(msg["last"]),
        open_price=Decimal(msg["open"]),
        high_price=Decimal(msg["high"]),
        low_price=Decimal(msg["low"]),
        volume=Decimal(msg["vol"]),
        last_id=0,  # not return in spot
        # ts_event=secs_to_nanos(float(msg[6])-1),  # zb time not accurate
        ts_event=ts_init,
        ts_init=ts_init,
    )


def parse_ticker_ws(instrument_id: InstrumentId, msg: List, ts_init: int) -> ZbTicker:
    return ZbTicker(
        instrument_id=instrument_id,
        price_change=Decimal(msg[5]),
        last_price=Decimal(msg[3]),
        open_price=Decimal(msg[0]),
        high_price=Decimal(msg[1]),
        low_price=Decimal(msg[2]),
        volume=Decimal(msg[4]),
        last_id=msg[6],
        # ts_event=secs_to_nanos(float(msg[6])-1),  # zb time not accurate
        ts_event=ts_init,
        ts_init=ts_init,
    )


def parse_trade_tick(instrument_id: InstrumentId, msg: List, ts_init: int) -> TradeTick:
    return TradeTick(
        instrument_id=instrument_id,
        price=Price.from_str(str(msg[0])),
        size=Quantity.from_str(str(msg[1])),
        aggressor_side=AggressorSide.SELL if msg[2] == -1 else AggressorSide.BUY,
        trade_id=TradeId(str(msg[3])),  # zb future does not provide match id
        ts_event=secs_to_nanos(float(msg[3])),
        ts_init=ts_init,
    )


def parse_spot_book_snapshot_ws(
    instrument_id: InstrumentId, msg: Dict, ts_init: int
) -> OrderBookSnapshot:
    return OrderBookSnapshot(
        instrument_id=instrument_id,
        book_type=BookType.L2_MBP,
        bids=[[float(o[0]), float(o[1])] for o in msg.get("bids", [])],
        asks=[[float(o[0]), float(o[1])] for o in msg.get("asks", [])],
        # ts_event=ts_event,
        ts_event=secs_to_nanos(float(msg["timestamp"])),  # zb time precision too low
        ts_init=ts_init,
        update_id=msg["timestamp"],
    )


def parse_spot_trade_tick_ws(
    instrument_id: InstrumentId, msg: Dict[str, str], ts_init: int
) -> TradeTick:
    return TradeTick(
        instrument_id=instrument_id,
        price=Price.from_str(msg["price"]),
        size=Quantity.from_str(msg["amount"]),
        aggressor_side=AggressorSide.SELL if msg["type"] == "sell" else AggressorSide.BUY,
        trade_id=TradeId(str(msg["tid"])),
        # ts_event=secs_to_nanos(float(msg[3])),  # zb time precision too low
        ts_event=ts_init,
        ts_init=ts_init,
    )


def parse_trade_tick_ws(instrument_id: InstrumentId, msg: List, ts_init: int) -> TradeTick:
    return TradeTick(
        instrument_id=instrument_id,
        price=Price.from_str(str(msg[0])),
        size=Quantity.from_str(str(msg[1])),
        aggressor_side=AggressorSide.SELL if msg[2] == -1 else AggressorSide.BUY,
        trade_id=TradeId(str(msg[3])),
        # ts_event=secs_to_nanos(float(msg[3])),  # zb time not accurate
        ts_event=ts_init,
        ts_init=ts_init,
    )


def parse_bar(bar_type: BarType, values: List, ts_init: int) -> ZbBar:
    return ZbBar(
        bar_type=bar_type,
        open=Price.from_str(str(values[0])),
        high=Price.from_str(str(values[1])),
        low=Price.from_str(str(values[2])),
        close=Price.from_str(str(values[3])),
        volume=Quantity.from_str(str(values[4])),
        ts_event=secs_to_nanos(float(values[5])),
        ts_init=ts_init,
    )


def parse_spot_bar(bar_type: BarType, values: List, ts_init: int) -> ZbBar:
    return ZbBar(
        bar_type=bar_type,
        open=Price.from_str(str(values[1])),
        high=Price.from_str(str(values[2])),
        low=Price.from_str(str(values[3])),
        close=Price.from_str(str(values[4])),
        volume=Quantity.from_str(str(values[5])),
        ts_event=secs_to_nanos(float(values[0])),
        ts_init=ts_init,
    )


def parse_bar_ws(
    instrument_id: InstrumentId,
    kline: List,
    chan_type: str,
    ts_init: int,
) -> ZbBar:

    _, _, interval = chan_type.partition("_")
    resolution = interval[-1]
    if resolution == "M":
        aggregation = BarAggregation.MINUTE
    elif resolution == "H":
        aggregation = BarAggregation.HOUR
    elif resolution == "D":
        aggregation = BarAggregation.DAY
    else:  # pragma: no cover (design-time error)
        raise RuntimeError(f"unsupported time aggregation resolution, was {resolution}")

    bar_spec = BarSpecification(
        step=int(interval[:-1]),
        aggregation=aggregation,
        price_type=PriceType.LAST,
    )

    bar_type = BarType(
        instrument_id=instrument_id,
        bar_spec=bar_spec,
        aggregation_source=AggregationSource.EXTERNAL,
    )

    return ZbBar(
        bar_type=bar_type,
        open=Price.from_str(str(kline[0])),
        high=Price.from_str(str(kline[1])),
        low=Price.from_str(str(kline[2])),
        close=Price.from_str(str(kline[3])),
        volume=Quantity.from_str(str(kline[4])),
        ts_event=secs_to_nanos(float(kline[5])),
        ts_init=ts_init,
    )


# Order Parsing


def parse_spot_order_status(
    account_id: AccountId,
    instrument: Instrument,
    data: Dict[str, Any],
    report_id: UUID4,
    ts_init: int,
) -> OrderStatusReport:
    client_id_str = data.get("clientId")  # Not returned by zb spot
    price = data.get("price")

    created_at = millis_to_nanos(data["trade_date"])

    order_status = OrderStatus.ACCEPTED
    if data["status"] == 1:
        order_status = OrderStatus.CANCELED
    elif data["status"] == 2:
        order_status = (
            OrderStatus.CANCELED
            if data["trade_amount"] < data["total_amount"]
            else OrderStatus.FILLED
        )
    elif data["status"] == 3:
        order_status = OrderStatus.PARTIALLY_FILLED

    time_in_force = TimeInForce.GTC
    if data["type"] >= 4:
        time_in_force = TimeInForce.IOC

    return OrderStatusReport(
        account_id=account_id,
        instrument_id=instrument.id,
        client_order_id=ClientOrderId(client_id_str) if client_id_str is not None else None,
        venue_order_id=VenueOrderId(str(data["id"])),
        order_side=OrderSide.BUY if data["type"] % 2 == 1 else OrderSide.SELL,
        order_type=OrderType.LIMIT,  # ZB Spot only have limit order
        time_in_force=time_in_force,
        order_status=order_status,
        price=instrument.make_price(price) if price is not None else None,
        quantity=instrument.make_qty(data["total_amount"]),
        filled_qty=instrument.make_qty(data["trade_amount"]),
        avg_px=None,
        post_only=True if data["type"] == 2 or data["type"] == 3 else False,
        reduce_only=False,
        report_id=report_id,
        ts_accepted=created_at,
        ts_last=created_at,
        ts_init=ts_init,
    )


def parse_future_order_status(
    account_id: AccountId,
    instrument: Instrument,
    data: Dict[str, Any],
    report_id: UUID4,
    ts_init: int,
) -> OrderStatusReport:
    client_id_str = data.get("orderCode")
    price = data.get("price")
    avg_px = data["avgPrice"]
    created_at = millis_to_nanos(data["createTime"])

    order_status = OrderStatus.ACCEPTED
    if data["showStatus"] == 2:
        order_status = OrderStatus.PARTIALLY_FILLED
    elif data["showStatus"] == 3:
        order_status = OrderStatus.FILLED
    elif data["showStatus"] == 4:
        order_status = OrderStatus.PENDING_CANCEL
    elif data["showStatus"] in (5, 7):
        order_status = OrderStatus.CANCELED

    time_in_force = TimeInForce.GTC
    if data["action"] in (3, 31, 32, 33, 34, 39):
        time_in_force = TimeInForce.IOC

    return OrderStatusReport(
        account_id=account_id,
        instrument_id=instrument.id,
        client_order_id=ClientOrderId(client_id_str) if client_id_str is not None else None,
        venue_order_id=VenueOrderId(data["id"]),
        order_side=OrderSide.BUY if data["type"] == 1 else OrderSide.SELL,
        order_type=OrderType.LIMIT,  # ZB future only support limit order for now
        time_in_force=time_in_force,
        order_status=order_status,
        price=instrument.make_price(price) if price is not None else None,
        quantity=instrument.make_qty(data["amount"]),
        filled_qty=instrument.make_qty(data["tradeAmount"]),
        avg_px=Decimal(avg_px) if avg_px != "0" else None,
        post_only=True if data["action"] == 4 else False,
        reduce_only=False,  # Zb future not support reduce only
        report_id=report_id,
        ts_accepted=created_at,
        ts_last=created_at,
        ts_init=ts_init,
    )


def parse_order_fill(
    account_id: AccountId,
    instrument: Instrument,
    data: Dict[str, Any],
    report_id: UUID4,
    ts_init: int,
) -> TradeReport:
    return TradeReport(
        account_id=account_id,
        instrument_id=instrument.id,
        venue_order_id=VenueOrderId(str(data["orderId"])),
        trade_id=TradeId(str(data["createTime"])),
        order_side=OrderSide.BUY if data["side"] in (1, 4) else OrderSide.SELL,
        last_qty=instrument.make_qty(data["amount"]),
        last_px=instrument.make_price(data["price"]),
        commission=Money(data["feeAmount"], Currency.from_str(data["feeCurrency"])),
        liquidity_side=LiquiditySide.MAKER if data["maker"] else LiquiditySide.TAKER,
        report_id=report_id,
        ts_event=millis_to_nanos(data["createTime"]),
        ts_init=ts_init,
    )


def parse_position(
    account_id: AccountId,
    instrument: Instrument,
    data: Dict[str, Any],
    report_id: UUID4,
    ts_init: int,
) -> PositionStatusReport:
    if data["side"] == 2:
        position_side = PositionSide.LONG if data["nominalValue"] > 0 else PositionSide.SHORT
    elif data["side"] == 1:
        position_side = PositionSide.LONG
    else:  # data["side"] == 0:
        position_side = PositionSide.SHORT

    return PositionStatusReport(
        account_id=account_id,
        instrument_id=instrument.id,
        position_side=position_side,
        venue_position_id=PositionId(data["id"]),  # FIX: not same with self-generated position_id
        quantity=instrument.make_qty(data["amount"]),
        report_id=report_id,
        ts_last=ts_init,
        ts_init=ts_init,
    )


# Account parsing


def parse_zb_spot_liquidity_side(side: int) -> OrderSide:
    if side >= 4:  # IOC
        return LiquiditySide.TAKER
    elif side >= 2:  # Post only
        return LiquiditySide.MAKER
    else:  # NOTE: Limit Order might be taker sometime
        return LiquiditySide.MAKER


def parse_zb_spot_order_side(side: int) -> OrderSide:
    if side == 1 or side == 3 or side == 5:
        return OrderSide.BUY
    elif side == 0 or side == 2 or side == 4:
        return OrderSide.SELL
    else:
        raise ValueError(f"Unknown order side: {side}")


def parse_account_balances_raw(provider, raw_balances: List) -> List[AccountBalance]:
    return _parse_balances(provider, raw_balances, "currencyName", "amount", "freezeAmount")


def parse_spot_account_balances_raw(provider, raw_balances: List) -> List[AccountBalance]:
    return _parse_balances(provider, raw_balances, "enName", "available", "freez")


def _parse_balances(
    provider: InstrumentProvider,
    raw_balances: List[Dict[str, str]],
    asset_key: str,
    free_key: str,
    locked_key: str,
) -> List[AccountBalance]:
    parsed_balances: Dict[Currency, Tuple[Decimal, Decimal, Decimal]] = {}
    for b in raw_balances:
        currency = provider.currency(b[asset_key].upper())
        if not currency:
            continue

        free = Decimal(b[free_key])
        locked = Decimal(b[locked_key])
        total: Decimal = free + locked

        # Ignore empty balances
        if total == 0:
            continue

        parsed_balances[currency] = (total, locked, free)

    balances: List[AccountBalance] = [
        AccountBalance(
            total=Money(values[0], currency),
            locked=Money(values[1], currency),
            free=Money(values[2], currency),
        )
        for currency, values in parsed_balances.items()
    ]

    return balances


def parse_account_margins_raw(provider, raw_margins: List[Dict]) -> List[MarginBalance]:
    balances = []
    for margin in raw_margins:
        currency = provider.currency(margin["unit"].upper())
        balances.append(
            MarginBalance(
                initial=Money(margin["allMargin"], currency),
                maintenance=Money(margin["freeze"], currency),
            )
        )
    return balances


# ZB future use USDT as default


def parse_zb_position_side(side: int) -> PositionSide:
    if side == 3 or side == 1:
        return "LONG"
    else:
        return "SHORT"


def parse_zb_order_side(type: int) -> OrderSide:
    if type == 1:
        return OrderSide.BUY
    elif type == -1:
        return OrderSide.SELL
    else:
        raise ValueError(f"Unknown order side: {type}")


def parse_zb_order_type(action: int) -> OrderType:
    if action == 11 or action == 31 or action == 51:
        return OrderType.MARKET
    else:  # TODO: parse other STOP LIMIT
        return OrderType.LIMIT


def zb_order_side(  # noqa: C901
    order: Order, oms_type: OMSType, position: Optional[Position] = None
) -> int:
    if order.side == OrderSide.BUY:
        if oms_type == OMSType.NETTING:
            if order.is_reduce_only:
                return 0
            else:
                return 5
        elif oms_type == OMSType.HEDGING:
            # Closing short position
            if position is not None and position.side == PositionSide.SHORT:
                return 4
            else:
                return 1
    elif order.side == OrderSide.SELL:
        if oms_type == OMSType.NETTING:
            if order.is_reduce_only:
                return 0
            else:
                return 6
        elif oms_type == OMSType.HEDGING:
            # Closing long position
            if position is not None and position.side == PositionSide.LONG:
                return 3
            else:
                return 2
    raise ValueError(f"Unsupported oms type {oms_type}")


def zb_order_params(
    order: Order, oms_type: OMSType, position: Optional[Position] = None
) -> Dict[str, Any]:
    if order.type == OrderType.MARKET:
        return dict(
            symbol=order.instrument_id.symbol.value,
            side=zb_order_side(order, oms_type, position),
            amount=order.quantity.as_double(),
            action=zb_order_action_market(order),
            client_order_id=order.client_order_id.value,
        )
    elif order.type == OrderType.LIMIT:
        return dict(
            symbol=order.instrument_id.symbol.value,
            side=zb_order_side(order, oms_type, position),
            amount=order.quantity.as_double(),
            action=zb_order_action_limit(order),
            price=order.price.as_double(),
            client_order_id=order.client_order_id.value,
        )
    else:
        raise ValueError(f"Unsupported order type for zb: {order.type}")


def zb_order_action_market(order: MarketOrder) -> int:
    # Zb future using limit order to simulate market order
    if order.time_in_force == TimeInForce.GTC:
        return 19
    elif order.time_in_force == TimeInForce.IOC:
        return 39
    elif order.time_in_force == TimeInForce.FOK:
        return 59
    else:
        raise ValueError(f"Unsupported time_in_force market for zb: {order.time_in_force}")


def zb_order_action_limit(order: LimitOrder) -> int:
    if order.is_post_only:
        return 4
    elif order.time_in_force == TimeInForce.GTC:
        return 1
    elif order.time_in_force == TimeInForce.IOC:
        return 3
    elif order.time_in_force == TimeInForce.FOK:
        return 5
    else:
        raise ValueError(f"Unsupported time_in_force limit for zb: {order.time_in_force}")


def _quote_precision(quote_asset: str) -> int:
    #  common quotes are ("ZUSD", "USDT", "QC", "BTC", "USDC"):
    return 8  # hardcode for now


def parse_future_instrument_http(market: Dict, venue: Venue) -> Instrument:
    # Create base asset
    base_asset = market["sellerCurrencyName"].upper()
    base_currency = Currency(
        code=base_asset,
        precision=int(market["priceDecimal"]),
        iso4217=0,  # Currently undetermined for crypto assets
        name=base_asset,
        currency_type=CurrencyType.CRYPTO,
    )

    # Create quote asset
    quote_asset = market["buyerCurrencyName"].upper()
    quote_currency = Currency(
        code=quote_asset,
        precision=_quote_precision(quote_asset),
        iso4217=0,  # Currently undetermined for crypto assets
        name=quote_asset,
        currency_type=CurrencyType.CRYPTO,
    )

    symbol = Symbol(base_currency.code + "/" + quote_currency.code)
    # symbol = Symbol(market["symbol"])
    instrument_id = InstrumentId(symbol=symbol, venue=venue)

    # NOTE: ZB api doesn't provide info about tick size, simulate using price_precision
    price_increment = Price(
        value=1 / (10 ** int(market["priceDecimal"])), precision=int(market["priceDecimal"])
    )
    size_increment = Quantity(
        value=1 / (10 ** int(market["amountDecimal"])),
        precision=int(market["amountDecimal"]),
    )

    # TODO: query vip status programmatically
    # default fee rate is 0.075% for taker, 0.025% for vip taker
    # default fee rate is 0 for maker, -0.025% for vip maker
    maker_fee: Decimal = Decimal("-0.00025")  # vip
    taker_fee: Decimal = Decimal("0.00025")  # vip
    # maker_fee: Decimal = Decimal(0)
    # taker_fee: Decimal = Decimal("0.00075")

    return CryptoPerpetual(
        instrument_id=instrument_id,
        native_symbol=Symbol(market["symbol"]),
        base_currency=base_currency,
        quote_currency=quote_currency,
        settlement_currency=quote_currency,  # for USDT-based markets, settlement == quote
        is_inverse=False,
        price_precision=int(market["priceDecimal"]),
        size_precision=int(market["amountDecimal"]),
        price_increment=price_increment,
        size_increment=size_increment,
        max_quantity=Quantity(market["maxAmount"], int(market["amountDecimal"])),
        min_quantity=Quantity(market["minAmount"], int(market["amountDecimal"])),
        max_notional=None,
        min_notional=Money(market["minTradeMoney"], currency=quote_currency),
        max_price=None,
        min_price=None,
        margin_init=Decimal(0),
        margin_maint=Decimal(0),
        maker_fee=maker_fee,
        taker_fee=taker_fee,
        ts_event=time.time_ns(),
        ts_init=time.time_ns(),
        info=market,
    )


def parse_spot_instrument_http(market: str, entry: Dict, venue: Venue):
    base, _, quote = market.partition("_")

    # Create base asset
    base_asset = base.upper()
    base_currency = Currency(
        code=base_asset,
        precision=4,  # Hardcoded for zb spot
        iso4217=0,  # Currently undetermined for crypto assets
        name=base_asset,
        currency_type=CurrencyType.CRYPTO,
    )

    # Create quote asset
    quote_asset = quote.upper()
    quote_currency = Currency(
        code=quote_asset,
        precision=_quote_precision(quote_asset),
        iso4217=0,  # Currently undetermined for crypto assets
        name=quote_asset,
        currency_type=CurrencyType.CRYPTO,
    )

    symbol = Symbol(base_currency.code + "/" + quote_currency.code)
    instrument_id = InstrumentId(symbol=symbol, venue=venue)

    price_increment = Price(
        value=1 / (10 ** int(entry["priceScale"])),
        precision=int(entry["priceScale"]),
    )
    size_increment = Quantity(
        value=1 / (10 ** int(entry["amountScale"])),
        precision=int(entry["amountScale"]),
    )

    return CurrencyPair(
        instrument_id=instrument_id,
        native_symbol=Symbol(market),
        base_currency=base_currency,
        quote_currency=quote_currency,
        price_precision=int(entry["priceScale"]),
        size_precision=int(entry["amountScale"]),
        price_increment=price_increment,
        size_increment=size_increment,
        lot_size=None,
        max_quantity=None,
        min_quantity=Quantity(entry["minAmount"], int(entry["minAmount"])),
        max_notional=None,
        min_notional=None,
        max_price=None,
        min_price=None,
        margin_init=Decimal(0),
        margin_maint=Decimal(0),
        maker_fee=Decimal("0.002"),
        taker_fee=Decimal("0.002"),
        ts_event=time.time_ns(),
        ts_init=time.time_ns(),
        info=entry,
    )
