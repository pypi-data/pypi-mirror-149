# flake8: noqa
# mypy: ignore-errors
import os

import nautilus_trader
from nautilus_trader.adapters.binance.http import client as http_client
from nautilus_trader.adapters.binance.http import error
from nautilus_trader.adapters.binance.websocket import client as ws_client

from nacre.adapters.binance.parsing import execution
from nacre.network.http import HttpClient
from nacre.network.websocket import WebSocketClient


def __repr__(self) -> str:
    return f"{type(self).__name__}(" f"status={self.status}, " f"message={self.message})"


error.BinanceError.__repr__ = __repr__

http_client.BinanceHttpClient = type(
    "BinanceHttpClient", (HttpClient,), dict(http_client.BinanceHttpClient.__dict__)
)
NAUTILUS_VERSION = nautilus_trader.__version__


# Patch BinanceHttpClient using nacre.network.http.HttpClient
def http_init(
    self,
    loop,
    clock,
    logger,
    key=None,
    secret=None,
    base_url=None,
    timeout=None,
    show_limit_usage=False,
    proxy=None,
):
    super(http_client.BinanceHttpClient, self).__init__(
        loop=loop,
        logger=logger,
    )
    self._clock = clock
    self._key = key
    self._secret = secret
    self._base_url = base_url or self.BASE_URL
    self._show_limit_usage = show_limit_usage
    self._proxies = None
    self._headers = {
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "nautilus-trader/" + NAUTILUS_VERSION,
        "X-MBX-APIKEY": key,
    }
    self._proxy = proxy if proxy else os.environ.get("PROXY")

    if timeout is not None:
        self._headers["timeout"] = timeout


async def request(self, *args, **kwargs):
    if "proxy" not in kwargs and self._proxy:
        kwargs["proxy"] = self._proxy
    return await super(http_client.BinanceHttpClient, self).request(*args, **kwargs)


http_client.BinanceHttpClient.__init__ = http_init
http_client.BinanceHttpClient.request = request

# Patch BinanceWebSocketClient using nacre.network.websocket.WebSocketClient


ws_client.BinanceWebSocketClient = type(
    "BinanceWebSocketClient", (WebSocketClient,), dict(ws_client.BinanceWebSocketClient.__dict__)
)


def ws_init(
    self,
    loop,
    clock,
    logger,
    handler,
    base_url=None,
):
    super(ws_client.BinanceWebSocketClient, self).__init__(
        loop=loop,
        logger=logger,
        handler=handler,
        max_retry_connection=6,
    )

    self._base_url = base_url

    self._clock = clock
    self._streams = []


async def ws_connect(
    self,
    key=None,
    start=True,
    **ws_kwargs,
) -> None:
    if not self._streams:
        raise RuntimeError("No subscriptions for connection.")

    # Always connecting combined streams for consistency
    ws_url = self._base_url + "/stream?streams=" + "/".join(self._streams)
    if key is not None:
        ws_url += f"&listenKey={key}"

    self._log.info(f"Connecting to {ws_url}")
    await super(ws_client.BinanceWebSocketClient, self).connect(
        ws_url=ws_url, start=start, **ws_kwargs
    )


ws_client.BinanceWebSocketClient.__init__ = ws_init
ws_client.BinanceWebSocketClient.connect = ws_connect
