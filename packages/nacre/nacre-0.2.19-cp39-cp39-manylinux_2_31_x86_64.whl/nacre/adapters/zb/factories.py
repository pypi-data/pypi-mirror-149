import asyncio
import os
from functools import lru_cache
from typing import Dict, Optional, Union

from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import LiveLogger
from nautilus_trader.common.logging import Logger
from nautilus_trader.config import InstrumentProviderConfig
from nautilus_trader.live.factories import LiveDataClientFactory
from nautilus_trader.live.factories import LiveExecClientFactory
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.msgbus.bus import MessageBus

from nacre.adapters.zb.common.enums import ZbAccountType
from nacre.adapters.zb.config import ZbDataClientConfig
from nacre.adapters.zb.config import ZbExecClientConfig
from nacre.adapters.zb.data import ZbFutureDataClient
from nacre.adapters.zb.data import ZbSpotDataClient
from nacre.adapters.zb.futures.execution import ZbFuturesExecutionClient
from nacre.adapters.zb.http.client import ZbHttpClient
from nacre.adapters.zb.http.spot import ZbSpotHttpClient
from nacre.adapters.zb.providers import ZbInstrumentProvider
from nacre.adapters.zb.spot.execution import ZbSpotExecutionClient


HTTP_CLIENTS: Dict[str, ZbHttpClient] = {}


def get_cached_zb_http_client(
    loop: asyncio.AbstractEventLoop,
    clock: LiveClock,
    logger: Logger,
    base_url: str,
    key: Optional[str] = None,
    sec: Optional[str] = None,
    account_type: ZbAccountType = ZbAccountType.SPOT,
    proxy: Optional[str] = None,
) -> ZbHttpClient:

    global HTTP_CLIENTS
    key = key or os.environ.get("ZB_API_KEY", "")
    sec = sec or os.environ.get("ZB_API_SECRET", "")

    client_key: str = "|".join((key, sec, account_type.value, str(proxy or "")))
    if client_key not in HTTP_CLIENTS:
        if account_type.is_futures:
            client = ZbHttpClient(
                loop=loop,
                clock=clock,
                logger=logger,
                key=key,
                secret=sec,
                base_url=base_url,
                timeout=10,
                proxy=proxy,
            )
        elif account_type.is_spot:
            client = ZbSpotHttpClient(
                loop=loop,
                clock=clock,
                logger=logger,
                key=key,
                secret=sec,
                base_url=base_url,
                timeout=10,
                proxy=proxy,
            )
        else:
            raise ValueError(f"{account_type} not support by zb for now")

        HTTP_CLIENTS[client_key] = client
    return HTTP_CLIENTS[client_key]


@lru_cache(1)
def get_cached_zb_instrument_provider(
    logger: Logger,
    venue: Venue,
    client: ZbHttpClient,
    account_type: ZbAccountType,
    config: InstrumentProviderConfig,
) -> ZbInstrumentProvider:
    return ZbInstrumentProvider(
        logger=logger,
        venue=venue,
        client=client,
        account_type=account_type,
        config=config,
    )


class ZbLiveDataClientFactory(LiveDataClientFactory):
    @staticmethod
    def create(
        loop: asyncio.AbstractEventLoop,
        name: str,
        config: ZbDataClientConfig,
        msgbus: MessageBus,
        cache: Cache,
        clock: LiveClock,
        logger: LiveLogger,
    ) -> Union[ZbSpotDataClient, ZbFutureDataClient]:

        base_url_http_default: str = _get_default_http_base_url(config)
        base_url_ws_default: str = _get_default_ws_base_url(config)

        client = get_cached_zb_http_client(
            loop=loop,
            clock=clock,
            logger=logger,
            base_url=config.base_url_http or base_url_http_default,
            key=config.api_key,
            sec=config.api_secret,
            account_type=config.account_type,
            proxy=config.http_proxy,
        )

        venue = Venue(name.upper())

        # Get instrument provider singleton
        provider = get_cached_zb_instrument_provider(
            venue=venue,
            client=client,
            logger=logger,
            account_type=config.account_type,
            config=config.instrument_provider,
        )

        # Create client
        if config.account_type.is_spot:
            return ZbSpotDataClient(
                loop=loop,
                client=client,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                venue=venue,
                instrument_provider=provider,
                base_url_ws=config.base_url_ws or base_url_ws_default,
            )
        elif config.account_type.is_futures:
            return ZbFutureDataClient(
                loop=loop,
                client=client,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                venue=venue,
                instrument_provider=provider,
                base_url_ws=config.base_url_ws or base_url_ws_default,
            )
        else:
            raise ValueError(f"Account type not implemented: {config.account_type}")


class ZbLiveExecClientFactory(LiveExecClientFactory):
    @staticmethod
    def create(
        loop: asyncio.AbstractEventLoop,
        name: str,
        config: ZbExecClientConfig,
        msgbus: MessageBus,
        cache: Cache,
        clock: LiveClock,
        logger: LiveLogger,
    ) -> Union[ZbSpotExecutionClient, ZbFuturesExecutionClient]:

        base_url_http_default: str = _get_default_http_base_url(config)
        base_url_ws_default: str = _get_default_ws_base_url(config)

        client = get_cached_zb_http_client(
            loop=loop,
            clock=clock,
            logger=logger,
            base_url=config.base_url_http or base_url_http_default,
            key=config.api_key,
            sec=config.api_secret,
            account_type=config.account_type,
            proxy=config.http_proxy,
        )

        res = name.partition("-")
        if res[1]:
            account_id = AccountId.from_str(name)
        else:
            account_id = AccountId(name, "DEFAULT")
        venue = Venue(account_id.issuer)

        market_client = client
        # ZbSpot separate market and trade api to "api.zb.com" and "trade.zb.com"
        if config.account_type.is_spot:
            market_client = get_cached_zb_http_client(
                loop=loop,
                clock=clock,
                logger=logger,
                base_url="https://api.zb.com",  # Hardcode for now
                account_type=config.account_type,
            )

        provider = get_cached_zb_instrument_provider(
            venue=venue,
            client=market_client,
            logger=logger,
            account_type=config.account_type,
            config=config.instrument_provider,
        )

        if config.account_type.is_spot:
            return ZbSpotExecutionClient(
                loop=loop,
                client=client,
                market_client=market_client,
                name=name,
                account_id=account_id,
                venue=venue,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                instrument_provider=provider,
                base_url_ws=config.base_url_ws or base_url_ws_default,
            )
        elif config.account_type.is_futures:
            return ZbFuturesExecutionClient(
                loop=loop,
                client=client,
                oms_type=config.oms_type,
                name=name,
                account_id=account_id,
                venue=venue,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                instrument_provider=provider,
                base_url_ws=config.base_url_ws or base_url_ws_default,
            )
        else:
            raise ValueError(f"Account type not implemented: {config.account_type}")


def _get_default_http_base_url(config: Union[ZbDataClientConfig, ZbExecClientConfig]) -> str:
    if config.account_type == ZbAccountType.SPOT:
        if isinstance(config, ZbDataClientConfig):
            return "https://api.zb.com"
        elif isinstance(config, ZbExecClientConfig):
            return "https://trade.zb.com"
    elif config.account_type == ZbAccountType.FUTURES_USDT:
        return "https://fapi.zb.com"

    raise RuntimeError(f"invalid Zb account type, was {config.account_type}")


def _get_default_ws_base_url(config: Union[ZbDataClientConfig, ZbExecClientConfig]) -> str:
    if config.account_type in (ZbAccountType.SPOT, ZbAccountType.MARGIN):
        return "wss://api.zb.com/websocket"
    elif config.account_type == ZbAccountType.FUTURES_USDT:
        if isinstance(config, ZbDataClientConfig):
            return "wss://fapi.zb.com/ws/public/v1"
        elif isinstance(config, ZbExecClientConfig):
            return "wss://fapi.zb.com/ws/private/api/v2"

    raise RuntimeError(f"invalid Zb account type, was {config.account_type}")
