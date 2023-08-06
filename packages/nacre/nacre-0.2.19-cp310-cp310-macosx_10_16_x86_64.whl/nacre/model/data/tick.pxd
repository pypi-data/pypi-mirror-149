
from nautilus_trader.model.data.tick cimport Tick
from nautilus_trader.model.identifiers cimport InstrumentId
from nautilus_trader.model.objects cimport Price


cdef class MarkTick(Tick):
    cdef readonly Price price
    """The events close price.\n\n:returns: `Price`"""

    @staticmethod
    cdef MarkTick from_dict_c(dict values)

    @staticmethod
    cdef dict to_dict_c(MarkTick obj)
