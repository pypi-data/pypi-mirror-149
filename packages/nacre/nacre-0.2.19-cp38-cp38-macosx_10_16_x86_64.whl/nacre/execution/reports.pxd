
from nautilus_trader.execution.reports cimport PositionStatusReport as NautilusPositionStatusReport
from nautilus_trader.model.objects cimport Price


cdef class PositionStatusReport(NautilusPositionStatusReport):
    cdef readonly Price entry_px
    cdef readonly Price last_px
