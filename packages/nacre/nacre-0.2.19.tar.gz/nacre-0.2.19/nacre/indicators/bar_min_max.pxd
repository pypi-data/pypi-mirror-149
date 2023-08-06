from cpython.datetime cimport datetime
from cpython.datetime cimport timedelta
from nautilus_trader.indicators.base.indicator cimport Indicator
from nautilus_trader.model.identifiers cimport InstrumentId
from nautilus_trader.model.objects cimport Price


cdef class BarMinMax(Indicator):
    cdef readonly timedelta lookback
    """The look back duration in time.\n\n:returns: `timedelta`"""
    cdef readonly WindowedMinMaxPrices prices
    """The windowed min max prices.\n\n:returns: `WindowedMinMaxPrices`"""
    cdef readonly WindowedMinMaxPrices volumes
    """The windowed min max prices.\n\n:returns: `WindowedMinMaxPrices`"""

cdef class WindowedMinMaxPrices:
    cdef object _min_prices
    cdef object _max_prices

    cdef readonly timedelta lookback
    """The look back duration in time.\n\n:returns: `timedelta`"""
    cdef readonly Price min_price
    """The minimum price in the window.\n\n:returns: `Price`"""
    cdef readonly Price max_price
    """The maximum price in the window.\n\n:returns: `Price`"""

    cpdef void add_price(self, datetime ts, Price price) except *
    cpdef void reset(self) except *

    cdef void _expire_stale_prices_by_cutoff(self, ts_prices, datetime cutoff) except *
    cdef void _add_min_price(self, datetime ts, Price price) except *
    cdef void _add_max_price(self, datetime ts, Price price) except *
