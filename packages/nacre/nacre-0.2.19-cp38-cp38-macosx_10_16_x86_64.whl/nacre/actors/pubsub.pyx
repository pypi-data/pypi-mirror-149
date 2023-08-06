import asyncio
from typing import Any, Callable

from nautilus_trader.common.actor cimport Actor
from nautilus_trader.common.logging cimport Logger
from nautilus_trader.common.logging cimport LoggerAdapter
from nautilus_trader.common.queue cimport Queue
from nautilus_trader.model.identifiers cimport TraderId

from nacre.config import PubSubConfig


cdef class PubSub(Actor):
    _sentinel = None

    def __init__(self, config: PubSubConfig):
        super().__init__(config)

        self._loop = None
        self.topic_filters = config.topic_filters
        self._queue = Queue(maxsize=10000)  # hardcoded for now

        self._run_queues_task = None
        self.is_running = False

    def get_run_queue_task(self) -> asyncio.Task:
        return self._run_queues_task

    cpdef int qsize(self) except *:
        return self._queue.qsize()

    cpdef void on_start(self) except *:
        self._loop = asyncio.get_running_loop()

        self.is_running = True  # Queues will continue to process

        for topic_filter in self.topic_filters:
            self._msgbus.subscribe(topic=topic_filter, handler=self._handle_data, priority=1)

        # Run queue
        self._run_queues_task = self._loop.create_task(self._run())
        self._log.debug(f"Scheduled {self._run_queues_task}")
        self.connect()

    cpdef void on_stop(self) except *:
        if self.is_running:
            self.is_running = False
            self._enqueue_sentinels()

        self.disconnect()

    def connect(self):
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    def disconnect(self):
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    cpdef void kill(self) except *:
        self._log.warning("Killing pusub...")
        if self._run_queues_task:
            self._log.debug("Canceling run_queues_task...")
            self._run_queues_task.cancel()
        if self.is_running:
            self.is_running = False  # Avoids sentinel messages for queues
            self.stop()

    cpdef object wrap_message(self, object obj):
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    def _handle_data(self, obj):
        message = self.wrap_message(obj)
        try:
            self._queue.put_nowait(message)
        except asyncio.QueueFull:
            self._log.warning(
                f"Blocking on `_queue.put` as message_queue full at "
                f"{self._queue.qsize()} items.",
            )
            self._loop.create_task(self._queue.put(message))  # Blocking until qsize reduces

    async def _run(self):
        self._log.debug(
            f"Message queue processing starting (qsize={self.qsize()})...",
        )
        cdef object message
        cdef str topic
        try:
            while self.is_running:
                message = await self._queue.get()
                if message is None:  # Sentinel message (fast C-level check)
                    continue         # Returns to the top to check `self.is_running`
                else:
                    self.relay(message)

        except asyncio.CancelledError:
            if not self._queue.empty():
                self._log.warning(
                    f"Running canceled with {self.qsize()} message(s) on queue.",
                )
            else:
                self._log.debug(
                    f"Message queue processing stopped (qsize={self.qsize()}).",
                )

        self._log.debug(
            f"Message queue exit (qsize={self.qsize()})...",
        )

    cdef void _enqueue_sentinels(self) except *:
        self._queue.put_nowait(self._sentinel)
        self._log.debug(f"Sentinel message placed on message queue.")

    cpdef void relay(self, object obj) except *:
        """Abstract method (implement in subclass)."""
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover
