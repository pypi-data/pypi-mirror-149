
from libc.stdint cimport int64_t
from nautilus_trader.core.uuid cimport UUID4
from nautilus_trader.execution.reports cimport PositionStatusReport as NautilusPositionStatusReport
from nautilus_trader.model.c_enums.position_side cimport PositionSide
from nautilus_trader.model.identifiers cimport AccountId
from nautilus_trader.model.identifiers cimport ClientOrderId
from nautilus_trader.model.identifiers cimport InstrumentId
from nautilus_trader.model.identifiers cimport PositionId
from nautilus_trader.model.identifiers cimport TradeId
from nautilus_trader.model.identifiers cimport Venue
from nautilus_trader.model.identifiers cimport VenueOrderId
from nautilus_trader.model.objects cimport Price
from nautilus_trader.model.objects cimport Quantity


cdef class PositionStatusReport(NautilusPositionStatusReport):
    def __init__(
        self,
        AccountId account_id not None,
        InstrumentId instrument_id not None,
        PositionSide position_side,
        Quantity quantity not None,
        UUID4 report_id not None,
        int64_t ts_last,
        int64_t ts_init,
        PositionId venue_position_id = None,  # Can be None
        Price entry_px = None,
        Price last_px = None,
    ):
        super().__init__(
            account_id,
            instrument_id,
            position_side,
            quantity,
            report_id,
            ts_last,
            ts_init,
            venue_position_id,
        )

        self.entry_px = entry_px
        self.last_px = last_px
