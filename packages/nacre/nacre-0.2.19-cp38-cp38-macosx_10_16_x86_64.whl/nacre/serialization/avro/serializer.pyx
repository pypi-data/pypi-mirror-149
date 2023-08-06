from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.core.datetime cimport nanos_to_millis
from nautilus_trader.model.events.order cimport OrderAccepted
from nautilus_trader.model.events.order cimport OrderCanceled
from nautilus_trader.model.events.order cimport OrderCancelRejected
from nautilus_trader.model.events.order cimport OrderDenied
from nautilus_trader.model.events.order cimport OrderEvent
from nautilus_trader.model.events.order cimport OrderExpired
from nautilus_trader.model.events.order cimport OrderFilled
from nautilus_trader.model.events.order cimport OrderInitialized
from nautilus_trader.model.events.order cimport OrderModifyRejected
from nautilus_trader.model.events.order cimport OrderPendingCancel
from nautilus_trader.model.events.order cimport OrderPendingUpdate
from nautilus_trader.model.events.order cimport OrderRejected
from nautilus_trader.model.events.order cimport OrderSubmitted
from nautilus_trader.model.events.order cimport OrderTriggered
from nautilus_trader.model.events.order cimport OrderUpdated
from nautilus_trader.model.events.position cimport PositionChanged
from nautilus_trader.model.events.position cimport PositionClosed
from nautilus_trader.model.events.position cimport PositionEvent
from nautilus_trader.model.events.position cimport PositionOpened
from nautilus_trader.model.orders.base cimport Order
from nautilus_trader.model.orders.limit cimport LimitOrder
from nautilus_trader.model.orders.market cimport MarketOrder
from nautilus_trader.model.orders.stop_limit cimport StopLimitOrder
from nautilus_trader.model.orders.stop_market cimport StopMarketOrder
from nautilus_trader.model.orders.trailing_stop_limit cimport TrailingStopLimitOrder
from nautilus_trader.model.orders.trailing_stop_market cimport TrailingStopMarketOrder
from nautilus_trader.model.position cimport Position
from nautilus_trader.serialization.base cimport _OBJECT_TO_DICT_MAP

from schema_registry.client import AsyncSchemaRegistryClient
from schema_registry.serializers import AsyncAvroMessageSerializer

from nacre.serialization.base cimport AsyncSerializer

from nacre.serialization.avro.schema import NAUTILUS_OBJECT_AVRO_SCHEMA


_AVRO_TO_DICT_MAP = {
    # Orders
    LimitOrder.__name__: lambda obj: obj.to_dict(),
    MarketOrder.__name__: lambda obj: obj.to_dict(),
    StopLimitOrder.__name__: lambda obj: obj.to_dict(),
    StopMarketOrder.__name__: lambda obj: obj.to_dict(),
    TrailingStopLimitOrder.__name__: lambda obj: obj.to_dict(),
    TrailingStopMarketOrder.__name__: lambda obj: obj.to_dict(),

    # Position
    Position.__name__: lambda obj: obj.to_dict(),
}


# Kafka postgresql connector require "-value", "-key" suffix on topic
_AVRO_TO_SUBJECT_MAP = {

    # Orders
    LimitOrder.__name__: "states.order-value",
    MarketOrder.__name__: "states.order-value",
    StopLimitOrder.__name__: "states.order-value",
    StopMarketOrder.__name__: "states.order-value",
    TrailingStopLimitOrder.__name__: "states.order-value",
    TrailingStopMarketOrder.__name__: "states.order-value",

    OrderAccepted.__name__: "events.order-value",
    OrderCancelRejected.__name__: "events.order-value",
    OrderCanceled.__name__: "events.order-value",
    OrderDenied.__name__: "events.order-value",
    OrderExpired.__name__: "events.order-value",
    OrderFilled.__name__: "events.order-value",
    OrderInitialized.__name__: "events.order-value",
    OrderPendingCancel.__name__: "events.order-value",
    OrderPendingUpdate.__name__: "events.order-value",
    OrderRejected.__name__: "events.order-value",
    OrderSubmitted.__name__: "events.order-value",
    OrderTriggered.__name__: "events.order-value",
    OrderModifyRejected.__name__: "events.order-value",
    OrderUpdated.__name__: "events.order-value",

    # PositionEvent
    PositionOpened.__name__: "events.position-value",
    PositionChanged.__name__: "events.position-value",
    PositionClosed.__name__: "events.position-value",

    # Position
    Position.__name__: "states.position-value",
}


cdef class AvroSerializer(AsyncSerializer):
    def __init__(self, schema_registry: str):
        self._client = AsyncSchemaRegistryClient(schema_registry)
        self._async_serializer = AsyncAvroMessageSerializer(self._client)

    async def serialize(self, object obj) -> bytes:
        Condition.not_none(obj, "obj")

        cls_name = type(obj).__name__

        delegate = _AVRO_TO_DICT_MAP.get(cls_name)
        if delegate is None:
            delegate = _OBJECT_TO_DICT_MAP.get(cls_name)
        if delegate is None:
            raise TypeError(f"Cannot serialize object `{cls_name}`.")

        obj_dict = delegate(obj)
        schema = NAUTILUS_OBJECT_AVRO_SCHEMA.get(cls_name)
        if schema is None:
            raise TypeError(f"Cannot get schema for class `{cls_name}`")

        subject = _AVRO_TO_SUBJECT_MAP.get(cls_name)
        if subject is None:
            raise TypeError(f"Cannot get subject for class `{cls_name}`")

        obj_dict = self.type_convert(obj, obj_dict)
        return await self._async_serializer.encode_record_with_schema(subject, schema, obj_dict)

    async def deserialize(self, obj_bytes: bytes) -> object:
        pass

    async def stop(self):
        await self._client.session.aclose()

    cpdef dict type_convert(self, object obj, dict obj_dict):
        # Convert timestamp fields to millisecond
        cdef str field_name
        for field_name in ("ts_event", "ts_init", "ts_last", "ts_opened", "ts_closed"):
            field = obj_dict.get(field_name)
            if field is not None:
                obj_dict[field_name] = nanos_to_millis(field)

        if isinstance(obj, (Order, OrderEvent)):
            return self.order_type_convert(obj, obj_dict)
        elif isinstance(obj, (Position, PositionEvent)):
            return self.position_type_convert(obj, obj_dict)
        return obj_dict

    cpdef dict order_type_convert(self, object obj, dict obj_dict):
        # Convert str typed value back to float
        cdef str field_name
        for field_name in ("quantity", "price", "filled_qty", "avg_px", "slippage", "display_qty", "trigger_price", "last_qty", "last_px"):
            field = obj_dict.get(field_name)
            if field is not None:
                obj_dict[field_name] = float(field)

        # Fix MarketOrder reduce_only name inconsistence
        reduce_flag = obj_dict.get("reduce_only")
        if reduce_flag is not None:
            obj_dict["is_reduce_only"] = reduce_flag

        return obj_dict

    cpdef dict position_type_convert(self, object obj, dict obj_dict):
        # Convert str typed value back to float
        cdef str field_name
        for field_name in ("net_qty", "quantity", "peak_qty", "avg_px_open", "realized_points", "last_qty", "last_px"):
            field = obj_dict.get(field_name)
            if field is not None:
                obj_dict[field_name] = float(field)
        # Bug here
        avg_px_close = obj_dict.get("avg_px_close")
        if avg_px_close is not None:
            if avg_px_close == "None":
                obj_dict["avg_px_close"] = None
            else:
                obj_dict["avg_px_close"] = float(avg_px_close)
        return obj_dict
