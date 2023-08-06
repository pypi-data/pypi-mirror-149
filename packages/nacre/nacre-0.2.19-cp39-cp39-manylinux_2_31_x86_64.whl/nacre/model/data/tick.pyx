from libc.stdint cimport int64_t
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.model.data.tick cimport Tick
from nautilus_trader.model.identifiers cimport InstrumentId
from nautilus_trader.model.objects cimport Price


cdef class MarkTick(Tick):
    """
    Represents an instrument mark price at a venue.
    """

    def __init__(
        self,
        InstrumentId instrument_id not None,
        Price price not None,
        int64_t ts_event,
        int64_t ts_init,
    ):
        """
        Initialize a new instance of the ``MarkTick`` class.

        Parameters
        ----------
        price : Price
            The mark price for the instrument.
        ts_event : int64
            The UNIX timestamp (nanoseconds) when the close price event occurred.
        ts_init : int64
            The UNIX timestamp (nanoseconds) when the object was initialized.

        """
        super().__init__(instrument_id, ts_event, ts_init)
        self.price = price

    def __eq__(self, MarkTick other) -> bool:
        return MarkTick.to_dict_c(self) == MarkTick.to_dict_c(other)

    def __hash__(self) -> int:
        return hash(frozenset(MarkTick.to_dict_c(self)))

    def __str__(self) -> str:
        return (f"{self.instrument_id},"
                f"{self.price},"
                f"{self.ts_event}")

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self})"

    @staticmethod
    cdef MarkTick from_dict_c(dict values):
        Condition.not_none(values, "values")
        return MarkTick(
            instrument_id=InstrumentId.from_str_c(values["instrument_id"]),
            price=Price.from_str_c(values["price"]),
            ts_event=values["ts_event"],
            ts_init=values["ts_init"],
        )

    @staticmethod
    cdef dict to_dict_c(MarkTick obj):
        Condition.not_none(obj, "obj")
        return {
            "type": "MarkTick",
            "instrument_id": obj.instrument_id.value,
            "price": str(obj.price),
            "ts_event": obj.ts_event,
            "ts_init": obj.ts_init,
        }

    @staticmethod
    def from_dict(dict values) -> MarkTick:
        """
        Return an instrument close price event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        MarkTick

        """
        return MarkTick.from_dict_c(values)

    @staticmethod
    def to_dict(MarkTick obj):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """
        return MarkTick.to_dict_c(obj)
