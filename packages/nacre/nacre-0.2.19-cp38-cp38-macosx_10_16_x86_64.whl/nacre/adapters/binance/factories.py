# flake8: noqa
# mypy: ignore-errors
from functools import lru_cache
from typing import Dict, List, Optional

from nautilus_trader.adapters.binance.common.enums import BinanceAccountType
from nautilus_trader.adapters.binance.config import (
    BinanceExecClientConfig as NautilusBinanceExecClientConfig,
)
from nautilus_trader.adapters.binance.factories import _get_http_base_url
from nautilus_trader.adapters.binance.factories import _get_ws_base_url
from nautilus_trader.adapters.binance.factories import get_cached_binance_http_client
from nautilus_trader.adapters.binance.futures import data as futures_data
from nautilus_trader.adapters.binance.futures import execution as futures_execution
from nautilus_trader.adapters.binance.futures import providers as futures_providers
from nautilus_trader.adapters.binance.futures.http.account import BinanceFuturesAccountHttpAPI
from nautilus_trader.adapters.binance.futures.http.market import BinanceFuturesMarketHttpAPI
from nautilus_trader.adapters.binance.futures.http.user import BinanceFuturesUserDataHttpAPI
from nautilus_trader.adapters.binance.futures.http.wallet import BinanceFuturesWalletHttpAPI
from nautilus_trader.adapters.binance.http.error import BinanceClientError
from nautilus_trader.adapters.binance.spot import data as spot_data
from nautilus_trader.adapters.binance.spot import execution as spot_execution
from nautilus_trader.adapters.binance.spot import providers as spot_providers
from nautilus_trader.adapters.binance.spot.http.account import BinanceSpotAccountHttpAPI
from nautilus_trader.adapters.binance.spot.http.market import BinanceSpotMarketHttpAPI
from nautilus_trader.adapters.binance.spot.http.user import BinanceSpotUserDataHttpAPI
from nautilus_trader.adapters.binance.spot.http.wallet import BinanceSpotWalletHttpAPI
from nautilus_trader.adapters.binance.websocket.client import BinanceWebSocketClient
from nautilus_trader.common.logging import LogColor
from nautilus_trader.core.correctness import PyCondition
from nautilus_trader.core.datetime import millis_to_nanos
from nautilus_trader.live.factories import LiveDataClientFactory
from nautilus_trader.live.factories import LiveExecClientFactory
from nautilus_trader.model.enums import AccountType
from nautilus_trader.model.enums import OMSType
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import ClientId
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import Venue

from nacre.live.execution_client import LiveExecutionClient


# All the shitty code below patch custom venue/account_id/oms_type into clients
# Original nautilus clients locked venue to BINANCE_VENUE
# which not work in situations like some spot-futures arbitrage strategies that require both account type

# Temporary solution. Consider create PR to nautilus_trader


class BinanceExecClientConfig(NautilusBinanceExecClientConfig):
    oms_type: OMSType = OMSType.NETTING


@lru_cache(1)
def get_cached_binance_spot_instrument_provider(
    client,
    logger,
    venue,
    account_type,
    config,
):
    return spot_providers.BinanceSpotInstrumentProvider(
        client=client,
        logger=logger,
        venue=venue,
        account_type=account_type,
        config=config,
    )


@lru_cache(1)
def get_cached_binance_futures_instrument_provider(
    client,
    logger,
    venue,
    account_type,
    config,
):
    return futures_providers.BinanceFuturesInstrumentProvider(
        client=client,
        logger=logger,
        venue=venue,
        account_type=account_type,
        config=config,
    )


def spot_init(
    self,
    loop,
    client,
    msgbus,
    cache,
    clock,
    logger,
    instrument_provider,
    name,
    account_id,
    venue,
    account_type: BinanceAccountType = BinanceAccountType.SPOT,
    base_url_ws=None,
):
    super(spot_execution.BinanceSpotExecutionClient, self).__init__(
        loop=loop,
        client_id=ClientId(name),
        venue=venue,
        oms_type=OMSType.NETTING,
        instrument_provider=instrument_provider,
        account_type=AccountType.CASH,
        base_currency=None,
        msgbus=msgbus,
        cache=cache,
        clock=clock,
        logger=logger,
    )

    self._binance_account_type = account_type
    self._log.info(f"Account type: {self._binance_account_type.value}.", LogColor.BLUE)

    self._set_account_id(account_id)

    # HTTP API
    self._http_client = client
    self._http_account = BinanceSpotAccountHttpAPI(client=client)
    self._http_market = BinanceSpotMarketHttpAPI(client=client)
    self._http_user = BinanceSpotUserDataHttpAPI(client=client, account_type=account_type)

    # Listen keys
    self._ping_listen_keys_interval = 60 * 5  # Once every 5 mins (hardcode)
    self._ping_listen_keys_task = None
    self._listen_key = None

    # WebSocket API
    self._ws_client = BinanceWebSocketClient(
        loop=loop,
        clock=clock,
        logger=logger,
        handler=self._handle_user_ws_message,
        base_url=base_url_ws,
    )

    # Hot caches
    self._instrument_ids = {}

    self._log.info(f"Base URL HTTP {self._http_client.base_url}.", LogColor.BLUE)
    self._log.info(f"Base URL WebSocket {base_url_ws}.", LogColor.BLUE)


def futures_init(
    self,
    loop,
    client,
    msgbus,
    cache,
    clock,
    logger,
    instrument_provider,
    name,
    account_id,
    venue,
    oms_type,
    account_type: BinanceAccountType = BinanceAccountType.FUTURES_USDT,
    base_url_ws=None,
):
    super(futures_execution.BinanceFuturesExecutionClient, self).__init__(
        loop=loop,
        client_id=ClientId(name),
        venue=venue,
        oms_type=oms_type,
        instrument_provider=instrument_provider,
        account_type=AccountType.MARGIN,
        base_currency=None,
        msgbus=msgbus,
        cache=cache,
        clock=clock,
        logger=logger,
    )

    self._binance_account_type = account_type
    self._log.info(f"Account type: {self._binance_account_type.value}.", LogColor.BLUE)

    self._set_account_id(account_id)
    self._set_venue(venue)

    # HTTP API
    self._http_client = client
    self._http_account = BinanceFuturesAccountHttpAPI(client=client, account_type=account_type)
    self._http_market = BinanceFuturesMarketHttpAPI(client=client, account_type=account_type)
    self._http_user = BinanceFuturesUserDataHttpAPI(client=client, account_type=account_type)

    # Listen keys
    self._ping_listen_keys_interval = 60 * 5  # Once every 5 mins (hardcode)
    self._ping_listen_keys_task = None
    self._listen_key = None

    # WebSocket API
    self._ws_client = BinanceWebSocketClient(
        loop=loop,
        clock=clock,
        logger=logger,
        handler=self._handle_user_ws_message,
        base_url=base_url_ws,
    )

    # Hot caches
    self._instrument_ids = {}

    self._log.info(f"Base URL HTTP {self._http_client.base_url}.", LogColor.BLUE)
    self._log.info(f"Base URL WebSocket {base_url_ws}.", LogColor.BLUE)


spot_execution.BinanceSpotExecutionClient = type(
    "BinanceSpotExecutionClient",
    (LiveExecutionClient,),
    dict(spot_execution.BinanceSpotExecutionClient.__dict__),
)
futures_execution.BinanceFuturesExecutionClient = type(
    "BinanceFuturesExecutionClient",
    (LiveExecutionClient,),
    dict(futures_execution.BinanceFuturesExecutionClient.__dict__),
)
spot_execution.BinanceSpotExecutionClient.__init__ = spot_init
futures_execution.BinanceFuturesExecutionClient.__init__ = futures_init


def spot_data_init(
    self,
    loop,
    client,
    msgbus,
    cache,
    clock,
    logger,
    instrument_provider,
    venue,
    account_type: BinanceAccountType = BinanceAccountType.SPOT,
    base_url_ws=None,
):
    super(spot_data.BinanceSpotDataClient, self).__init__(
        loop=loop,
        client_id=ClientId(venue.value),
        venue=venue,
        instrument_provider=instrument_provider,
        msgbus=msgbus,
        cache=cache,
        clock=clock,
        logger=logger,
    )

    assert account_type.is_spot or account_type.is_margin, "account type is not for spot/margin"
    self._binance_account_type = account_type
    self._log.info(f"Account type: {self._binance_account_type.value}.", LogColor.BLUE)

    self._update_instrument_interval = 60 * 60  # Once per hour (hardcode)
    self._update_instruments_task = None

    # HTTP API
    self._http_client = client
    self._http_market = BinanceSpotMarketHttpAPI(client=self._http_client)  # type: ignore

    # WebSocket API
    self._ws_client = BinanceWebSocketClient(
        loop=loop,
        clock=clock,
        logger=logger,
        handler=self._handle_ws_message,
        base_url=base_url_ws,
    )

    # Hot caches
    self._instrument_ids = {}
    self._book_buffer = {}

    self._log.info(f"Base URL HTTP {self._http_client.base_url}.", LogColor.BLUE)
    self._log.info(f"Base URL WebSocket {base_url_ws}.", LogColor.BLUE)


def futures_data_init(
    self,
    loop,
    client,
    msgbus,
    cache,
    clock,
    logger,
    instrument_provider,
    venue,
    account_type: BinanceAccountType = BinanceAccountType.FUTURES_USDT,
    base_url_ws=None,
):
    super(futures_data.BinanceFuturesDataClient, self).__init__(
        loop=loop,
        client_id=ClientId(venue.value),
        venue=venue,
        instrument_provider=instrument_provider,
        msgbus=msgbus,
        cache=cache,
        clock=clock,
        logger=logger,
    )

    assert account_type.is_futures, "account type is not for futures"
    self._binance_account_type = account_type
    self._log.info(f"Account type: {self._binance_account_type.value}.", LogColor.BLUE)

    self._update_instrument_interval = 60 * 60  # Once per hour (hardcode)
    self._update_instruments_task = None

    # HTTP API
    self._http_client = client
    self._http_market = BinanceFuturesMarketHttpAPI(client=client, account_type=account_type)
    self._http_user = BinanceFuturesUserDataHttpAPI(client=client, account_type=account_type)

    # Listen keys
    self._ping_listen_keys_interval = 60 * 5  # Once every 5 mins (hardcode)
    self._ping_listen_keys_task = None
    self._listen_key = None

    # WebSocket API
    self._ws_client = BinanceWebSocketClient(
        loop=loop,
        clock=clock,
        logger=logger,
        handler=self._handle_ws_message,
        base_url=base_url_ws,
    )

    # Hot caches
    self._instrument_ids = {}
    self._book_buffer = {}

    self._log.info(f"Base URL HTTP {self._http_client.base_url}.", LogColor.BLUE)
    self._log.info(f"Base URL WebSocket {base_url_ws}.", LogColor.BLUE)


spot_data.BinanceSpotDataClient.__init__ = spot_data_init
futures_data.BinanceFuturesDataClient.__init__ = futures_data_init

# Patch custom venue
class BinanceLiveDataClientFactory(LiveDataClientFactory):
    @staticmethod
    def create(
        loop,
        name,
        config,
        msgbus,
        cache,
        clock,
        logger,
    ):
        base_url_http_default: str = _get_http_base_url(
            config.account_type, config.testnet, config.us
        )
        base_url_ws_default: str = _get_ws_base_url(config.account_type, config.testnet, config.us)

        client = get_cached_binance_http_client(
            loop=loop,
            clock=clock,
            logger=logger,
            key=config.api_key,
            secret=config.api_secret,
            account_type=config.account_type,
            base_url=config.base_url_http or base_url_http_default,
            is_testnet=config.testnet,
            is_us=config.us,
        )

        venue = Venue(name.upper())

        if config.account_type.is_spot or config.account_type.is_margin:
            # Get instrument provider singleton
            provider = get_cached_binance_spot_instrument_provider(
                client=client,
                logger=logger,
                venue=venue,
                account_type=config.account_type,
                config=config.instrument_provider,
            )

            # Create client
            return spot_data.BinanceSpotDataClient(
                loop=loop,
                client=client,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                instrument_provider=provider,
                venue=venue,
                account_type=config.account_type,
                base_url_ws=config.base_url_ws or base_url_ws_default,
            )
        else:
            # Get instrument provider singleton
            provider = get_cached_binance_futures_instrument_provider(
                client=client,
                logger=logger,
                venue=venue,
                account_type=config.account_type,
                config=config.instrument_provider,
            )

            # Create client
            return futures_data.BinanceFuturesDataClient(
                loop=loop,
                client=client,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                instrument_provider=provider,
                venue=venue,
                account_type=config.account_type,
                base_url_ws=config.base_url_ws or base_url_ws_default,
            )


# Patch custom account id and venue
class BinanceLiveExecClientFactory(LiveExecClientFactory):
    @staticmethod
    def create(
        loop,
        name,
        config,
        msgbus,
        cache,
        clock,
        logger,
    ):
        base_url_http_default: str = _get_http_base_url(
            config.account_type, config.testnet, config.us
        )
        base_url_ws_default: str = _get_ws_base_url(config.account_type, config.testnet, config.us)

        client = get_cached_binance_http_client(
            loop=loop,
            clock=clock,
            logger=logger,
            key=config.api_key,
            secret=config.api_secret,
            account_type=config.account_type,
            base_url=config.base_url_http or base_url_http_default,
            is_testnet=config.testnet,
        )

        res = name.partition("-")
        if res[1]:
            account_id = AccountId.from_str(name)
        else:
            account_id = AccountId(name, "DEFAULT")
        venue = Venue(account_id.issuer)

        if config.account_type.is_spot or config.account_type.is_margin:
            # Get instrument provider singleton
            provider = get_cached_binance_spot_instrument_provider(
                client=client,
                logger=logger,
                venue=venue,
                account_type=config.account_type,
                config=config.instrument_provider,
            )

            # Create client
            return spot_execution.BinanceSpotExecutionClient(
                loop=loop,
                client=client,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                instrument_provider=provider,
                name=name,
                account_id=account_id,
                venue=venue,
                account_type=config.account_type,
                base_url_ws=config.base_url_ws or base_url_ws_default,
            )
        else:
            # Get instrument provider singleton
            provider = get_cached_binance_futures_instrument_provider(
                client=client,
                logger=logger,
                venue=venue,
                account_type=config.account_type,
                config=config.instrument_provider,
            )

            # Create client
            return futures_execution.BinanceFuturesExecutionClient(
                loop=loop,
                client=client,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                instrument_provider=provider,
                name=name,
                account_id=account_id,
                venue=venue,
                oms_type=config.oms_type,
                account_type=config.account_type,
                base_url_ws=config.base_url_ws or base_url_ws_default,
            )


def spot_provider_init(
    self,
    client,
    logger,
    venue,
    account_type: BinanceAccountType = BinanceAccountType.SPOT,
    config=None,
):
    super(spot_providers.BinanceSpotInstrumentProvider, self).__init__(
        venue=venue,
        logger=logger,
        config=config,
    )

    self._client = client
    self._account_type = account_type

    self._http_wallet = BinanceSpotWalletHttpAPI(self._client)
    self._http_market = BinanceSpotMarketHttpAPI(self._client)


async def load_all_async(self, filters: Optional[Dict] = None) -> None:
    """
    Load the latest instruments into the provider asynchronously, optionally
    applying the given filters.

    Parameters
    ----------
    filters : Dict, optional
        The venue specific instrument loading filters to apply.

    """
    filters_str = "..." if not filters else f" with filters {filters}..."
    self._log.info(f"Loading all instruments{filters_str}")

    # Get current commission rates
    try:
        fee_res = await self._http_wallet.trade_fees()
        fees = {s.symbol: s for s in fee_res}
    except BinanceClientError:
        self._log.error(
            "Cannot load instruments: API key authentication failed "
            "(this is needed to fetch the applicable account fee tier).",
        )
        fees = {}

    # Get exchange info for all assets
    exchange_info = await self._http_market.exchange_info()
    for symbol_info in exchange_info.symbols:
        self._parse_instrument(
            symbol_info=symbol_info,
            fees=fees.get(symbol_info.symbol),
            ts_event=millis_to_nanos(exchange_info.serverTime),
        )


async def load_ids_async(
    self,
    instrument_ids: List[InstrumentId],
    filters: Optional[Dict] = None,
) -> None:
    """
    Load the instruments for the given IDs into the provider, optionally
    applying the given filters.

    Parameters
    ----------
    instrument_ids: List[InstrumentId]
        The instrument IDs to load.
    filters : Dict, optional
        The venue specific instrument loading filters to apply.

    Raises
    ------
    ValueError
        If any `instrument_id.venue` is not equal to `self.venue`.

    """
    if not instrument_ids:
        self._log.info("No instrument IDs given for loading.")
        return

    # Check all instrument IDs
    for instrument_id in instrument_ids:
        PyCondition.equal(instrument_id.venue, self.venue, "instrument_id.venue", "self.venue")

    filters_str = "..." if not filters else f" with filters {filters}..."
    self._log.info(f"Loading instruments {instrument_ids}{filters_str}.")

    # Get current commission rates
    try:
        fee_res = await self._http_wallet.trade_fees()
        fees = {s.symbol: s for s in fee_res}
    except BinanceClientError:
        self._log.error(
            "Cannot load instruments: API key authentication failed "
            "(this is needed to fetch the applicable account fee tier).",
        )
        fees = {}

    # Extract all symbol strings
    symbols: List[str] = [instrument_id.symbol.value for instrument_id in instrument_ids]

    # Get exchange info for all assets
    exchange_info = await self._http_market.exchange_info(symbols=symbols)
    for symbol_info in exchange_info.symbols:
        self._parse_instrument(
            symbol_info=symbol_info,
            fees=fees.get(symbol_info.symbol),
            ts_event=millis_to_nanos(exchange_info.serverTime),
        )


async def load_async(self, instrument_id: InstrumentId, filters: Optional[Dict] = None):
    """
    Load the instrument for the given ID into the provider asynchronously, optionally
    applying the given filters.

    Parameters
    ----------
    instrument_id: InstrumentId
        The instrument ID to load.
    filters : Dict, optional
        The venue specific instrument loading filters to apply.

    Raises
    ------
    ValueError
        If `instrument_id.venue` is not equal to `self.venue`.

    """
    PyCondition.not_none(instrument_id, "instrument_id")
    PyCondition.equal(instrument_id.venue, self.venue, "instrument_id.venue", "self.venue")

    filters_str = "..." if not filters else f" with filters {filters}..."
    self._log.debug(f"Loading instrument {instrument_id}{filters_str}.")

    symbol = instrument_id.symbol.value

    # Get current commission rates
    try:
        fees = await self._http_wallet.trade_fee(symbol=instrument_id.symbol.value)
    except BinanceClientError:
        self._log.error(
            "Cannot load instruments: API key authentication failed "
            "(this is needed to fetch the applicable account fee tier).",
        )
        fees = {}

    # Get exchange info for asset
    exchange_info = await self._http_market.exchange_info(symbol=symbol)
    for symbol_info in exchange_info.symbols:
        self._parse_instrument(
            symbol_info=symbol_info,
            fees=fees,
            ts_event=millis_to_nanos(exchange_info.serverTime),
        )


spot_providers.BinanceSpotInstrumentProvider.__init__ = spot_provider_init
spot_providers.BinanceSpotInstrumentProvider.load_all_async = load_all_async
spot_providers.BinanceSpotInstrumentProvider.load_ids_async = load_ids_async
spot_providers.BinanceSpotInstrumentProvider.load_async = load_async


def futures_provider_init(
    self,
    client,
    logger,
    venue,
    account_type: BinanceAccountType = BinanceAccountType.FUTURES_USDT,
    config=None,
):
    super(futures_providers.BinanceFuturesInstrumentProvider, self).__init__(
        venue=venue,
        logger=logger,
        config=config,
    )

    self._client = client
    self._account_type = account_type

    self._http_wallet = BinanceFuturesWalletHttpAPI(self._client)
    self._http_market = BinanceFuturesMarketHttpAPI(self._client, account_type=account_type)


futures_providers.BinanceFuturesInstrumentProvider.__init__ = futures_provider_init
