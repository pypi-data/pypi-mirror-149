from typing import Dict

from nautilus_trader.model.enums import ContingencyType
from nautilus_trader.model.enums import LiquiditySide
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import OrderStatus
from nautilus_trader.model.enums import OrderType
from nautilus_trader.model.enums import PositionSide
from nautilus_trader.model.enums import TimeInForce
from nautilus_trader.model.events.account import AccountState
from nautilus_trader.model.events.order import OrderAccepted
from nautilus_trader.model.events.order import OrderCanceled
from nautilus_trader.model.events.order import OrderCancelRejected
from nautilus_trader.model.events.order import OrderDenied
from nautilus_trader.model.events.order import OrderEvent
from nautilus_trader.model.events.order import OrderExpired
from nautilus_trader.model.events.order import OrderFilled
from nautilus_trader.model.events.order import OrderInitialized
from nautilus_trader.model.events.order import OrderModifyRejected
from nautilus_trader.model.events.order import OrderPendingCancel
from nautilus_trader.model.events.order import OrderPendingUpdate
from nautilus_trader.model.events.order import OrderRejected
from nautilus_trader.model.events.order import OrderSubmitted
from nautilus_trader.model.events.order import OrderTriggered
from nautilus_trader.model.events.order import OrderUpdated
from nautilus_trader.model.events.position import PositionChanged
from nautilus_trader.model.events.position import PositionClosed
from nautilus_trader.model.events.position import PositionEvent
from nautilus_trader.model.events.position import PositionOpened
from nautilus_trader.model.orders.base import Order
from nautilus_trader.model.orders.limit import LimitOrder
from nautilus_trader.model.orders.market import MarketOrder
from nautilus_trader.model.orders.stop_limit import StopLimitOrder
from nautilus_trader.model.orders.stop_market import StopMarketOrder
from nautilus_trader.model.orders.trailing_stop_limit import TrailingStopLimitOrder
from nautilus_trader.model.orders.trailing_stop_market import TrailingStopMarketOrder
from nautilus_trader.model.position import Position
from schema_registry.client import schema


def enums_to_avro_type(cls) -> Dict:
    return {
        "type": "enum",
        "name": cls.__name__,
        "symbols": [e.name for e in cls],
    }


OrderEventSchema = schema.AvroSchema(
    {
        "type": "record",
        "name": OrderEvent.__name__,
        "namespace": "nautilus_trader.model.events.order",
        "fields": [
            {
                "name": "type",
                "type": {
                    "type": "enum",
                    "name": "OrderEventType",
                    "symbols": [cls.__name__ for cls in OrderEvent.__subclasses__()],
                },
            },
            {"name": "trader_id", "type": "string"},
            {"name": "strategy_id", "type": "string"},
            {"name": "instrument_id", "type": "string"},
            {"name": "client_order_id", "type": "string"},
            {"name": "venue_order_id", "type": ["string", "null"], "default": None},
            {"name": "trade_id", "type": ["string", "null"], "default": None},
            {"name": "position_id", "type": ["string", "null"], "default": None},
            {"name": "account_id", "type": ["string", "null"], "default": None},
            {
                "name": "order_side",
                "type": [enums_to_avro_type(OrderSide), "null"],
                "default": None,
            },
            {
                "name": "order_type",
                "type": [enums_to_avro_type(OrderType), "null"],
                "default": None,
            },
            {"name": "quantity", "type": ["float", "null"], "default": None},
            {
                "name": "time_in_force",
                "type": [enums_to_avro_type(TimeInForce), "null"],
                "default": None,
            },
            {"name": "post_only", "type": ["boolean", "null"], "default": None},
            {"name": "reduce_only", "type": ["boolean", "null"], "default": None},
            {"name": "options", "type": ["string", "null"], "default": None},
            {"name": "order_list_id", "type": ["string", "null"], "default": None},
            {
                "name": "contingency_type",
                "type": [enums_to_avro_type(ContingencyType), "null"],
                "default": None,
            },
            {"name": "linked_order_ids", "type": ["string", "null"], "default": None},
            {"name": "parent_order_id", "type": ["string", "null"], "default": None},
            {"name": "tags", "type": ["string", "null"], "default": None},
            {"name": "event_id", "type": "string"},
            {"name": "ts_event", "type": ["long", "null"], "default": None},
            {"name": "ts_init", "type": "long"},
            {"name": "reason", "type": ["string", "null"], "default": None},
            {"name": "reconciliation", "type": ["boolean", "null"], "default": None},
            {"name": "price", "type": ["float", "null"], "default": None},
            {"name": "trigger_price", "type": ["float", "null"], "default": None},
            {"name": "last_qty", "type": ["float", "null"], "default": None},
            {"name": "last_px", "type": ["float", "null"], "default": None},
            {"name": "currency", "type": ["string", "null"], "default": None},
            {"name": "commission", "type": ["string", "null"], "default": None},
            {"name": "liquidity_side", "type": ["string", "null"], "default": None},
            {"name": "info", "type": ["string", "null"], "default": None},
        ],
    }
)

PositionEventSchema = schema.AvroSchema(
    {
        "type": "record",
        "name": PositionEvent.__name__,
        "namespace": "nautilus_trader.model.events.position",
        "fields": [
            {
                "name": "type",
                "type": {
                    "type": "enum",
                    "name": "OrderEventType",
                    "symbols": [cls.__name__ for cls in PositionEvent.__subclasses__()],
                },
            },
            {"name": "trader_id", "type": "string"},
            {"name": "strategy_id", "type": "string"},
            {"name": "instrument_id", "type": "string"},
            {"name": "position_id", "type": "string"},
            {"name": "account_id", "type": "string"},
            {"name": "from_order", "type": "string"},
            {"name": "entry", "type": enums_to_avro_type(OrderSide)},
            {"name": "side", "type": enums_to_avro_type(PositionSide)},
            {"name": "net_qty", "type": "float"},
            {"name": "quantity", "type": "float"},
            {"name": "peak_qty", "type": "float"},
            {"name": "last_qty", "type": "float"},
            {"name": "last_px", "type": "float"},
            {"name": "currency", "type": "string"},
            {"name": "event_id", "type": "string"},
            {"name": "ts_init", "type": "long"},
            {"name": "ts_event", "type": ["long", "null"], "default": None},
            {"name": "ts_opened", "type": ["long", "null"], "default": None},
            {"name": "ts_closed", "type": ["long", "null"], "default": None},
            {"name": "duration_ns", "type": ["long", "null"], "default": None},
            {"name": "avg_px_open", "type": ["float", "null"], "default": None},
            {"name": "avg_px_close", "type": ["float", "null"], "default": None},
            {"name": "realized_points", "type": ["float", "null"], "default": None},
            {"name": "realized_return", "type": ["string", "null"], "default": None},
            {"name": "realized_pnl", "type": "string"},
        ],
    }
)

OrderSchema = schema.AvroSchema(
    {
        "type": "record",
        "name": Order.__name__,
        "namespace": "nautilus_trader.model.orders",
        "fields": [
            {"name": "trader_id", "type": "string"},
            {"name": "strategy_id", "type": "string"},
            {"name": "instrument_id", "type": "string"},
            {"name": "client_order_id", "type": "string"},
            {"name": "order_list_id", "type": ["string", "null"], "default": None},
            {"name": "position_id", "type": ["string", "null"], "default": None},
            {"name": "account_id", "type": ["string", "null"], "default": None},
            {"name": "last_trade_id", "type": ["string", "null"], "default": None},
            {"name": "type", "type": enums_to_avro_type(OrderType)},
            {"name": "side", "type": enums_to_avro_type(OrderSide)},
            {"name": "quantity", "type": "float"},
            {"name": "price", "type": ["float", "null"], "default": None},
            {"name": "time_in_force", "type": enums_to_avro_type(TimeInForce)},
            {"name": "is_reduce_only", "type": "boolean"},
            {"name": "filled_qty", "type": "float"},
            {"name": "avg_px", "type": ["float", "null"], "default": None},
            {"name": "slippage", "type": "float"},
            {"name": "status", "type": enums_to_avro_type(OrderStatus)},
            {"name": "contingency_type", "type": enums_to_avro_type(ContingencyType)},
            {"name": "linked_order_ids", "type": ["string", "null"], "default": None},
            {"name": "parent_order_id", "type": ["string", "null"], "default": None},
            {"name": "tags", "type": ["string", "null"], "default": None},
            {"name": "ts_last", "type": "long"},
            {"name": "ts_init", "type": "long"},
            {"name": "expire_time_ns", "type": ["long", "null"], "default": None},
            {"name": "liquidity_side", "type": enums_to_avro_type(LiquiditySide)},
            {"name": "is_post_only", "type": "boolean"},
            {"name": "display_qty", "type": ["float", "null"], "default": None},
            {"name": "trigger_price", "type": ["float", "null"], "default": None},
            {"name": "trigger_type", "type": ["string", "null"], "default": None},
            {"name": "limit_offset", "type": ["string", "null"], "default": None},
            {"name": "trailing_offset", "type": ["string", "null"], "default": None},
            {"name": "offset_type", "type": ["string", "null"], "default": None},
        ],
    }
)


NAUTILUS_OBJECT_AVRO_SCHEMA = {
    AccountState.__name__: schema.AvroSchema(
        {
            "type": "record",
            "name": AccountState.__name__,
            "namespace": "nautilus_trader.model.events",
            "fields": [
                {"name": "account_id", "type": "string"},
                {"name": "account_type", "type": "string"},
                {"name": "base_currency", "type": ["string", "null"], "default": None},
                {"name": "balances", "type": "string"},
                {"name": "positions", "type": "string"},
                {"name": "reported", "type": "boolean"},
                {"name": "event_id", "type": "string"},
                {"name": "ts_event", "type": "long"},
                {"name": "ts_init", "type": "long"},
                {"name": "equity", "type": "float"},
                {"name": "equities", "type": "string", "default": "[]"},
            ],
        }
    ),
    # OrderEvent
    OrderAccepted.__name__: OrderEventSchema,
    OrderCancelRejected.__name__: OrderEventSchema,
    OrderCanceled.__name__: OrderEventSchema,
    OrderDenied.__name__: OrderEventSchema,
    OrderExpired.__name__: OrderEventSchema,
    OrderFilled.__name__: OrderEventSchema,
    OrderInitialized.__name__: OrderEventSchema,
    OrderPendingCancel.__name__: OrderEventSchema,
    OrderPendingUpdate.__name__: OrderEventSchema,
    OrderRejected.__name__: OrderEventSchema,
    OrderSubmitted.__name__: OrderEventSchema,
    OrderTriggered.__name__: OrderEventSchema,
    OrderModifyRejected.__name__: OrderEventSchema,
    OrderUpdated.__name__: OrderEventSchema,
    # PositionEvent
    PositionOpened.__name__: PositionEventSchema,
    PositionChanged.__name__: PositionEventSchema,
    PositionClosed.__name__: PositionEventSchema,
    # Orders
    LimitOrder.__name__: OrderSchema,
    MarketOrder.__name__: OrderSchema,
    StopLimitOrder.__name__: OrderSchema,
    StopMarketOrder.__name__: OrderSchema,
    TrailingStopLimitOrder.__name__: OrderSchema,
    TrailingStopMarketOrder.__name__: OrderSchema,
    # Position
    Position.__name__: schema.AvroSchema(
        {
            "type": "record",
            "name": Position.__name__,
            "namespace": "nautilus_trader.model.position",
            "fields": [
                {"name": "position_id", "type": "string"},
                {"name": "account_id", "type": "string"},
                {"name": "from_order", "type": "string"},
                {"name": "strategy_id", "type": "string"},
                {"name": "instrument_id", "type": "string"},
                {"name": "entry", "type": enums_to_avro_type(OrderSide)},
                {"name": "side", "type": enums_to_avro_type(PositionSide)},
                {"name": "net_qty", "type": "float"},
                {"name": "quantity", "type": "float"},
                {"name": "peak_qty", "type": "float"},
                {"name": "ts_opened", "type": "long"},
                {"name": "ts_closed", "type": "long"},
                {"name": "duration_ns", "type": "long"},
                {"name": "avg_px_open", "type": "float"},
                {"name": "avg_px_close", "type": ["float", "null"], "default": None},
                {"name": "quote_currency", "type": "string"},
                {"name": "base_currency", "type": "string"},
                {"name": "cost_currency", "type": "string"},
                {"name": "realized_points", "type": "float"},
                {"name": "realized_return", "type": "string"},
                {"name": "realized_pnl", "type": "string"},
                {"name": "commissions", "type": "string"},
            ],
        }
    ),
}
