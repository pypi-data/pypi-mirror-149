from nautilus_trader.execution.reports cimport OrderStatusReport
from nautilus_trader.execution.reports cimport PositionStatusReport
from nautilus_trader.execution.reports cimport TradeReport
from nautilus_trader.live.execution_engine cimport LiveExecutionEngine as NautilusLiveExecutionEngine


# from nacre.execution.reports cimport PositionStatusReport

cdef class LiveExecutionEngine(NautilusLiveExecutionEngine):
    cdef readonly bint reconcile_by_fake_fills

    cpdef void _generate_fake_fills(self, PositionStatusReport report) except *
