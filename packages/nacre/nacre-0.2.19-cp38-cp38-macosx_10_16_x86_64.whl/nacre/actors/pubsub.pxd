
from nautilus_trader.common.actor cimport Actor
from nautilus_trader.common.logging cimport LoggerAdapter
from nautilus_trader.common.queue cimport Queue
from nautilus_trader.model.identifiers cimport TraderId


cdef class PubSub(Actor):
    cdef list topic_filters
    cdef object _loop
    cdef object _run_queues_task
    cdef Queue _queue

    cdef readonly bint is_running

    cpdef int qsize(self) except *

    cpdef void kill(self) except *
    cdef void _enqueue_sentinels(self) except *

    cpdef object wrap_message(self, object obj)
    cpdef void relay(self, object obj) except *
