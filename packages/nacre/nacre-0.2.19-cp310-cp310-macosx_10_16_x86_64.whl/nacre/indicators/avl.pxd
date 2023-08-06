from cpython.datetime cimport datetime
from nautilus_trader.indicators.base.indicator cimport Indicator


cdef class Avl(Indicator):
    cdef object _value_inputs
    cdef object _volume_inputs

    cdef readonly int period
    """The moving average period.\n\n:returns: `PriceType`"""
    cdef readonly int count
    """The count of inputs received by the indicator.\n\n:returns: `int`"""
    cdef readonly double value
    """The current value.\n\n:returns: `double`"""

    cpdef void update_raw(self, double value, double volume) except *

    cpdef void _increment_count(self) except *
