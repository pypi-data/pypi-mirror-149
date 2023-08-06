from typing import Any, Dict, List, Optional

from nautilus_trader.common.logging import Logger
from nautilus_trader.common.providers import InstrumentProvider
from nautilus_trader.config import InstrumentProviderConfig
from nautilus_trader.core.correctness import PyCondition
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import Venue

from nacre.adapters.zb.common import format_websocket_market
from nacre.adapters.zb.common.enums import ZbAccountType
from nacre.adapters.zb.http.api.future_market import ZbFutureMarketHttpAPI
from nacre.adapters.zb.http.api.spot_market import ZbSpotMarketHttpAPI
from nacre.adapters.zb.http.client import ZbHttpClient
from nacre.adapters.zb.parsing import parse_future_instrument_http
from nacre.adapters.zb.parsing import parse_spot_instrument_http


class ZbInstrumentProvider(InstrumentProvider):
    """
    An example template of an ``InstrumentProvider`` showing the minimal methods
    which must be implemented for an integration to be complete.
    """

    def __init__(
        self,
        logger: Logger,
        venue: Venue,
        client: ZbHttpClient,
        account_type: ZbAccountType,
        config: Optional[InstrumentProviderConfig] = None,
    ):
        super().__init__(
            venue=venue,
            logger=logger,
            config=config,
        )

        self._client = client
        self._account_type = account_type

        if account_type.is_spot:
            self._market = ZbSpotMarketHttpAPI(self._client)
        elif account_type.is_futures:
            self._market = ZbFutureMarketHttpAPI(self._client)
        else:
            raise ValueError(f"{account_type} not support by zb for now")

        self._local_symbols_to_instrument_id: Dict[str, InstrumentId] = {}
        self._local_market_id_to_instrument_id: Dict[str, InstrumentId] = {}

    async def load_all_async(self, filters: Optional[Dict] = None) -> None:
        """
        Load the latest ZB instruments into the provider asynchronously.
        """
        if self._account_type.is_futures:
            await self.load_future_markets()
        elif self._account_type.is_spot:
            await self.load_spot_markets()

    async def load_ids_async(
        self,
        instrument_ids: List[InstrumentId],
        filters: Optional[Dict] = None,
    ) -> None:
        if not instrument_ids:
            self._log.info("No instrument IDs given for loading.")
            return

        # Check all instrument IDs
        for instrument_id in instrument_ids:
            PyCondition.equal(instrument_id.venue, self.venue, "instrument_id.venue", "self.venue")

        filters_str = "..." if not filters else f" with filters {filters}..."
        self._log.info(f"Loading instruments {instrument_ids}{filters_str}.")

        if self._account_type.is_futures:
            await self.load_future_markets(instrument_ids)
        elif self._account_type.is_spot:
            await self.load_spot_markets(instrument_ids)

    async def load_future_markets(self, instrument_ids: Optional[List[InstrumentId]] = None):
        markets: List[Dict] = await self._market.market_list()
        for market in markets:
            instrument = parse_future_instrument_http(market, self.venue)
            if instrument_ids is not None and instrument.id not in instrument_ids:
                continue

            self.add_currency(currency=instrument.base_currency)
            self.add_currency(currency=instrument.quote_currency)
            self.add(instrument=instrument)

            self._local_symbols_to_instrument_id[market["symbol"]] = instrument.id
            self._local_market_id_to_instrument_id[market["id"]] = instrument.id

    async def load_spot_markets(self, instrument_ids: Optional[List[InstrumentId]] = None):
        markets: Dict[str, Any] = await self._market.markets()
        for market, entry in markets.items():
            instrument = parse_spot_instrument_http(market, entry, self.venue)
            if instrument_ids is not None and instrument.id not in instrument_ids:
                continue

            self.add_currency(currency=instrument.base_currency)
            self.add_currency(currency=instrument.quote_currency)
            self.add(instrument=instrument)

            self._local_symbols_to_instrument_id[market] = instrument.id
            # Spot websocket return symbol like "BTC/USDT" in "btcusdt", map it here
            ws_symbol = format_websocket_market(market)
            self._local_market_id_to_instrument_id[ws_symbol] = instrument.id

    def find_instrument_id_by_local_symbol(self, local_symbol: str) -> InstrumentId:
        return self._local_symbols_to_instrument_id[local_symbol]

    def find_instrument_id_by_local_market_id(self, market_id: str) -> InstrumentId:
        return self._local_market_id_to_instrument_id[market_id]

    def list_local_market_ids(self) -> List[str]:
        return list(self._local_market_id_to_instrument_id.keys())
