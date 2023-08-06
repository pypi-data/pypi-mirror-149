from nautilus_trader.model.data.base import DataType
from nautilus_trader.model.identifiers import ClientId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.trading.strategy import Strategy
from nautilus_trader.trading.strategy import StrategyConfig

from nacre.model.data.tick import MarkTick


class MonConfig(StrategyConfig):
    venues: str  # separate by comma


class Mon(Strategy):
    def __init__(self, config: MonConfig):
        super().__init__(config)
        self.venues = [Venue(v) for v in config.venues.split(",")]

    def on_start(self):
        for venue in self.venues:
            self.subscribe_data(
                client_id=ClientId(venue.value),
                data_type=DataType(MarkTick),
            )
            for id in self.cache.instrument_ids(venue=venue):
                self.subscribe_quote_ticks(id)
