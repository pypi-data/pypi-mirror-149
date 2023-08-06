import asyncio
import re

from aiokafka import AIOKafkaProducer

from nacre.actors.pubsub cimport PubSub

from nacre.config import KafkaConfig

from nautilus_trader.common.logging cimport Logger
from nautilus_trader.core.correctness cimport Condition

# from nautilus_trader.model.events.order cimport OrderModifyRejected
# from nautilus_trader.model.events.order cimport OrderPendingCancel
# from nautilus_trader.model.events.order cimport OrderPendingUpdate
# from nautilus_trader.model.events.order cimport OrderRejected
# from nautilus_trader.model.events.order cimport OrderAccepted
# from nautilus_trader.model.events.order cimport OrderCanceled
# from nautilus_trader.model.events.order cimport OrderCancelRejected
# from nautilus_trader.model.events.order cimport OrderDenied
# from nautilus_trader.model.events.order cimport OrderExpired
# from nautilus_trader.model.events.order cimport OrderFilled
from nautilus_trader.model.events.order cimport OrderEvent
from nautilus_trader.model.events.order cimport OrderInitialized
from nautilus_trader.model.events.order cimport OrderSubmitted
from nautilus_trader.model.events.position cimport PositionEvent
from nautilus_trader.model.identifiers cimport TraderId
from nautilus_trader.model.orders.base cimport Order
from nautilus_trader.model.position cimport Position
from nautilus_trader.serialization.msgpack.serializer cimport MsgPackSerializer

from nacre.serialization.avro.serializer cimport AvroSerializer


# from nautilus_trader.model.events.order cimport OrderTriggered
# from nautilus_trader.model.events.order cimport OrderUpdated
# from nautilus_trader.model.events.position cimport PositionChanged
# from nautilus_trader.model.events.position cimport PositionClosed
# from nautilus_trader.model.events.position cimport PositionOpened

cdef class KafkaPubSub(PubSub):

    def __init__(self, config: KafkaConfig):
        Condition.type(config, KafkaConfig, "config")
        super().__init__(config)

        self._key = b""
        self.config = config

        # init kafka producer
        self._producer = None
        self._consumer = None

        self._serializer = AvroSerializer(config.schema_registry)

        self._start_producer_task = None
        self._stop_producer_task = None


    cpdef object wrap_message(self, object obj):
        if isinstance(obj, OrderEvent):
            if isinstance(obj, (OrderInitialized, OrderSubmitted)):
                return obj

            order = self.cache.order(obj.client_order_id)
            if order is not None:
                return (obj, order)
            else:
                return obj
        elif isinstance(obj, PositionEvent):
            position = self.cache.position(obj.position_id)
            if position is not None:
                return (obj, position)
            else:
                return obj
        else:
            return obj

    cpdef void relay(self, object obj) except *:
        self._loop.create_task(self._relay(obj))

    cpdef str detect_topic(self, object obj):
        if isinstance(obj, OrderEvent):
            return "events.order"
        elif isinstance(obj, PositionEvent):
            return "events.position"
        elif isinstance(obj, Order):
            return "states.order"
        elif isinstance(obj, Position):
            return "states.position"
        else:
            return "general"

    async def _relay(self, object obj):
        if isinstance(obj, tuple):
            for o in obj:
                await self._send(o)
        else:
            await self._send(obj)

    async def _send(self, object obj):
        topic = self.detect_topic(obj)
        cdef bytes obj_value = b""
        try:
            obj_value = await self._serializer.serialize(obj)
        except Exception as ex:
            self._log.exception("Error on sending object", ex)
            return

        await self._producer.send_and_wait(topic, value=obj_value, key=self._key)

    def connect(self):
        self._start_producer_task = self._loop.create_task(self._run_producer())
        self._key = self.trader_id.value.encode()

    def disconnect(self):
        self._stop_producer_task = self._loop.create_task(self._stop_producer())

    async def _run_producer(self):
        self._producer = AIOKafkaProducer(
            acks=1,
            loop=self._loop,
            bootstrap_servers=self.config.bootstrap_servers,
            security_protocol=self.config.security_protocol,
            client_id=self.trader_id.value,
        )

        await self._producer.start()
        self._log.info("Kafka pubsub started")

    async def _stop_producer(self):
        await self._producer.stop()
        await self._serializer.stop()
        self._log.info("Kafka pubsub stopped")
