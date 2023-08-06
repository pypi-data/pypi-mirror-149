from cpython.datetime cimport datetime

from collections import deque

import numpy as np

from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.core.stats cimport fast_mean
from nautilus_trader.indicators.base.indicator cimport Indicator
from nautilus_trader.model.data.bar cimport Bar


cdef class Avl(Indicator):
    """
    An indicator which calculates the volume weighted average price for the day.
    """

    def __init__(self, int period):
        """
        Initialize a new instance of the ``Avl`` class.
        """
        Condition.positive_int(period, "period")
        super().__init__(params=[period])

        self._value_inputs = deque(maxlen=period)
        self._volume_inputs = deque(maxlen=period)
        self.value = 0
        self.count = 0
        self.period = period

    cpdef void handle_bar(self, Bar bar) except *:
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        Condition.not_none(bar, "bar")

        prices = np.asarray(
            [
                bar.open.as_double(),
                bar.high.as_double(),
                bar.low.as_double(),
                bar.close.as_double(),
            ], dtype=np.float64)

        cdef double value = fast_mean(prices) * bar.volume.as_double()

        self.update_raw(
            value,
            bar.volume.as_double(),
        )

    cpdef void update_raw(
        self,
        double value,
        double volume,
    ) except *:
        """
        Update the indicator with the given raw values.

        Parameters
        ----------
        price : double
            The update price.
        volume : double
            The update volume.
        timestamp : datetime
            The current timestamp.

        """

        self._increment_count()
        self._value_inputs.append(value)
        self._volume_inputs.append(volume)

        self.value = sum(self._value_inputs) / sum(self._volume_inputs) if sum(self._volume_inputs) else 0

    cpdef void _reset(self) except *:
        self._inputs.clear()
        self.value = 0
        self.count = 0

    cpdef void _increment_count(self) except *:
        self.count += 1

        # Initialization logic
        if not self.initialized:
            self._set_has_inputs(True)
            if self.count >= self.period:
                self._set_initialized(True)
