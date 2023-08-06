import asyncio
import base64
import hashlib
import hmac
from typing import Any, Callable, Dict, Optional
from urllib.parse import urlparse

from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import Logger

from nacre.adapters.zb.common import format_symbol
from nacre.adapters.zb.websocket.client import ZbWebSocketClient


class ZbFuturesWebSocket:
    BASE_URL = "wss://fapi.zb.com/ws/public/v1"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        handler: Callable[[bytes], None],
        base_url: Optional[str] = None,
    ):

        usdt_m = ZbFuturesWebsocketClient(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=base_url or self.BASE_URL,
        )

        # force path replace
        qc_ws_url = urlparse(base_url or self.BASE_URL)._replace(path="/qc/ws/public/v1").geturl()
        qc_m = ZbFuturesWebsocketClient(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=qc_ws_url,
        )

        self.clients = {"usdt": usdt_m, "qc": qc_m}

    @property
    def is_connected(self) -> bool:
        return all(map(lambda c: c.is_connected, self.clients.values()))

    def get_client(self, symbol: str):
        if "/" in symbol:
            quote = symbol.partition("/")[2]
        elif "_" in symbol:
            quote = symbol.partition("_")[2]
        else:
            raise ValueError(f"Symbol {symbol} not supported")
        if quote == "ZUSD":
            quote = "usdt"
        return self.clients[quote.lower()]

    async def connect(self, **kwargs):
        await asyncio.gather(*[client.connect(**kwargs) for client in self.clients.values()])

    async def disconnect(self):
        # very weird bug here, can't await both otherwise it will stuck at return
        await self.clients["usdt"].disconnect()
        # await self.clients["qc"].disconnect()

    async def subscribe_mark_price(self, symbol: Optional[str] = None):
        if symbol:
            client = self.get_client(symbol)
            await client.subscribe_mark_price(symbol)
        else:
            await asyncio.gather(
                *[client.subscribe_mark_price(symbol) for client in self.clients.values()]
            )

    async def subscribe_index_price(self, symbol: Optional[str] = None):
        if symbol:
            client = self.get_client(symbol)
            await client.subscribe_index_price(symbol)
        else:
            await asyncio.gather(
                *[client.subscribe_index_price(symbol) for client in self.clients.values()]
            )

    async def subscribe_mark_bars(self, symbol: str, interval: str, size: int = 1):
        client = self.get_client(symbol)
        await client.subscribe_mark_bars(symbol, interval, size)

    async def subscribe_index_bars(self, symbol: str, interval: str, size: int = 1):
        client = self.get_client(symbol)
        await client.subscribe_index_bars(symbol, interval, size)

    async def subscribe_trades(self, symbol: str, size: int = 50):
        client = self.get_client(symbol)
        await client.subscribe_trades(symbol, size)

    async def subscribe_bars(self, symbol: str, interval: str, size: int = 1):
        client = self.get_client(symbol)
        await client.subscribe_bars(symbol, interval, size)

    async def subscribe_ticker(self, symbol: Optional[str] = None):
        if symbol:
            client = self.get_client(symbol)
            await client.subscribe_ticker(symbol)
        else:
            await asyncio.gather(
                *[client.subscribe_ticker(symbol) for client in self.clients.values()]
            )

    async def subscribe_book_deltas(
        self, symbol: str, depth: int = 50, precision: Optional[float] = None
    ):
        client = self.get_client(symbol)
        await client.subscribe_book_deltas(symbol, depth, precision)

    async def subscribe_book_snapshot(
        self, symbol: str, depth: int = 5, precision: Optional[float] = None
    ):
        client = self.get_client(symbol)
        await client.subscribe_book_snapshot(symbol, depth, precision)


class ZbFuturesWebsocketClient(ZbWebSocketClient):
    """
    Provides access to the `Zb FUTURES` streaming WebSocket API.
    """

    BASE_URL = "wss://fapi.zb.com/ws/public/v1"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        handler: Callable[[bytes], None],
        base_url: Optional[str] = None,
    ):
        super().__init__(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=base_url or self.BASE_URL,
        )

    async def _subscribe_channel(self, channel: str, **kwargs):
        kwargs["action"] = "subscribe"

        await super()._subscribe_channel(channel, **kwargs)

    async def _unsubscribe_channel(self, channel: str, **kwargs):
        kwargs["action"] = "unsubscribe"
        await super()._unsubscribe_channel(channel, **kwargs)

    async def subscribe_mark_price(self, symbol: Optional[str] = None):
        chan = "All"
        if symbol:
            chan = format_symbol(symbol)
        await self._subscribe_channel(channel=f"{chan}.mark")

    async def subscribe_index_price(self, symbol: Optional[str] = None):
        chan = "All"
        if symbol:
            chan = format_symbol(symbol)
        await self._subscribe_channel(channel=f"{chan}.index")

    async def subscribe_mark_bars(self, symbol: str, interval: str, size: int = 1):
        channel = f"{format_symbol(symbol)}.mark_{interval}"
        await self._subscribe_channel(channel=channel, size=size)

    async def subscribe_index_bars(self, symbol: str, interval: str, size: int = 1):
        channel = f"{format_symbol(symbol)}.index_{interval}"
        await self._subscribe_channel(channel=channel, size=size)

    async def subscribe_trades(self, symbol: str, size: int = 50):
        """
        Trade Streams.

        The Trade Streams push raw trade information; each trade has a unique buyer and seller.
        Update Speed: Real-time

        """
        await self._subscribe_channel(channel=f"{format_symbol(symbol)}.Trade", size=size)

    async def subscribe_bars(self, symbol: str, interval: str, size: int = 1):
        """
        Subscribe to bar (kline/candlestick) stream.

        The Kline/Candlestick Stream push updates to the current klines/candlestick every second.
        interval:
        1M,5M,15M, 30M, 1H, 6H, 1D, 5D
        Update Speed: 2000ms

        """
        channel = f"{format_symbol(symbol)}.KLine_{interval}"
        await self._subscribe_channel(channel=channel, size=size)

    async def subscribe_ticker(self, symbol: Optional[str] = None):
        """
        Individual symbol or all symbols ticker.

        24hr rolling window ticker statistics for a single symbol.
        These are NOT the statistics of the UTC day, but a 24hr rolling window for the previous 24hrs.
        Stream Name: <symbol>@ticker or
        Stream Name: !ticker@arr
        Update Speed: 1000ms

        """
        if symbol is None:
            await self._subscribe_channel(channel="All.Ticker")
        else:
            await self._subscribe_channel(channel=f"{format_symbol(symbol)}.Ticker")

    async def subscribe_book_deltas(
        self, symbol: str, depth: int = 50, precision: Optional[float] = None
    ):
        """
        Partial Book Depth Streams.

        Top bids and asks, Valid are min - 5000, default 50
        Update Speed: real time

        """
        channel = f"{format_symbol(symbol)}.Depth"
        if precision:
            channel = f"{format_symbol(symbol)}.Depth@{precision}"
        await self._subscribe_channel(channel=channel, size=depth)

    async def subscribe_book_snapshot(
        self, symbol: str, depth: int = 5, precision: Optional[float] = None
    ):
        """
        Diff book depth stream.

        Top bids and asks, Valid are 5 - 10
        Update Speed: 200ms
        Order book price and quantity depth updates used to locally manage an order book.

        """
        channel = f"{format_symbol(symbol)}.DepthWhole"
        if precision:
            channel = f"{format_symbol(symbol)}.DepthWhole@{precision}"
        await self._subscribe_channel(channel=channel, size=depth)


class ZbFutureUserDataWebSocket:
    BASE_URL = "wss://fapi.zb.com/ws/private/api/v2"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        handler: Callable[[bytes], None],
        key: str,
        hashed_secret: str,
        base_url: Optional[str] = None,
    ):
        usdt_m = ZbFuturesUserDataWebSocketClient(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            key=key,
            hashed_secret=hashed_secret,
            futures_account_type=1,
            base_url=base_url or self.BASE_URL,
        )

        # force path replace
        qc_ws_url = (
            urlparse(base_url or self.BASE_URL)._replace(path="/qc/ws/private/api/v2").geturl()
        )

        qc_m = ZbFuturesUserDataWebSocketClient(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            key=key,
            hashed_secret=hashed_secret,
            futures_account_type=2,
            base_url=qc_ws_url,
        )

        self.clients = {"usdt": usdt_m, "qc": qc_m}

    @property
    def is_connected(self) -> bool:
        return all(map(lambda c: c.is_connected, self.clients.values()))

    async def connect(self, **kwargs):
        await asyncio.gather(*[client.connect(**kwargs) for client in self.clients.values()])

    async def disconnect(self):
        # very weird bug here, can't await both otherwise it will stuck at return
        await self.clients["usdt"].disconnect()
        # await self.clients["qc"].disconnect()
        # for client in self.clients.values():
        #     await client.disconnect()

    # async def logged_in(self):
    #     for client in self.clients.values():
    #         await client.logged_in()

    # def add_post_connect_callbacks(self, *callbacks: Awaitable):
    #     for client in self.clients.values():
    #         client.add_post_connect_callbacks(*callbacks)

    def get_client(self, symbol: str):
        quote = symbol.partition("/")[2]
        if quote == "ZUSD":
            quote = "usdt"
        return self.clients[quote.lower()]

    async def subscribe_funding_update(self, currency: str):
        await asyncio.gather(
            *[client.subscribe_funding_update(currency) for client in self.clients.values()]
        )

    async def subscribe_asset_update(self):
        await asyncio.gather(*[client.subscribe_asset_update() for client in self.clients.values()])

    async def get_asset_snapshot(self, currency: str):
        await asyncio.gather(
            *[client.get_asset_snapshot(currency) for client in self.clients.values()]
        )

    async def subscribe_position_update(self, symbol: Optional[str] = None):
        if symbol is not None:
            client = self.get_client(symbol)
            await client.subscribe_position_update(symbol)
        else:
            await asyncio.gather(
                *[client.subscribe_position_update() for client in self.clients.values()]
            )

    async def subscribe_order_update(self, symbol: Optional[str] = None):
        if symbol is not None:
            client = self.get_client(symbol)
            await client.subscribe_order_update(symbol)
        else:
            await asyncio.gather(
                *[client.subscribe_order_update() for client in self.clients.values()]
            )

    async def new_order(
        self,
        symbol: str,
        side: int,
        amount: float,
        price: Optional[float] = None,
        action: Optional[int] = None,
        client_order_id: Optional[str] = None,
    ):
        client = self.get_client(symbol)
        await client.new_order(symbol, side, amount, price, action, client_order_id)

    async def cancel_order(
        self,
        symbol: str,
        order_id: Optional[str] = None,
        client_order_id: Optional[str] = None,
    ):
        client = self.get_client(symbol)
        await client.cancel_order(symbol, order_id, client_order_id)

    async def cancel_open_orders(self, symbol: str):
        client = self.get_client(symbol)
        await client.cancel_open_orders(symbol)

    async def get_trade_list(self, symbol: str, order_id: str):
        client = self.get_client(symbol)
        await client.get_trade_list(symbol, order_id)


class ZbFuturesUserDataWebSocketClient(ZbWebSocketClient):
    BASE_URL = "wss://fapi.zb.com/ws/private/api/v2"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        handler: Callable[[bytes], None],
        key: str,
        hashed_secret: str,
        futures_account_type: int = 1,
        base_url: Optional[str] = None,
    ):
        super().__init__(
            loop=loop,
            clock=clock,
            logger=logger,
            handler=handler,
            base_url=base_url or self.BASE_URL,
        )

        self._key = key
        self._hashed_secret = hashed_secret
        # self.is_logged_in = False
        self.futures_account_type = futures_account_type

    async def _request_channel(self, channel: str, **kwargs):
        kwargs["action"] = "subscribe"

        await super()._request_channel(channel, **kwargs)

    async def _subscribe_channel(self, channel: str, **kwargs):
        kwargs["action"] = "subscribe"

        await super()._subscribe_channel(channel, **kwargs)

    def _get_sign(self, timestamp, http_method, url_path) -> str:
        whole_data = timestamp + http_method + url_path
        m = hmac.new(self._hashed_secret.encode(), whole_data.encode(), hashlib.sha256)
        return str(base64.b64encode(m.digest()), "utf-8")

    async def _login(self):
        """
        Login to the user data stream.

        """
        timestamp = self._clock.utc_now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        signature = self._get_sign(timestamp, "GET", "login")
        payload = {
            "action": "login",
            "ZB-APIKEY": self._key,
            "ZB-TIMESTAMP": timestamp,
            "ZB-SIGN": signature,
        }

        await self.send_json(payload)

    # async def logged_in(self):
    #     while not self.is_logged_in:
    #         await self._sleep0()
    #     self._log.debug("Websocket logged in")

    async def on_post_connect(self):
        await self._login()
        await super().on_post_connect()
        # self.is_logged_in = True

    async def subscribe_funding_update(self, currency: str):
        await self._subscribe_channel(
            channel="Fund.change", futuresAccountType=self.futures_account_type, currency=currency
        )

    async def subscribe_asset_update(self):
        await self._subscribe_channel(
            channel="Fund.assetChange", futuresAccountType=self.futures_account_type
        )

    async def get_asset_snapshot(self, currency: str):
        await self._request_channel(
            channel="Fund.balance", futuresAccountType=self.futures_account_type, currency=currency
        )

    async def subscribe_position_update(self, symbol: Optional[str] = None):
        payload: Dict[str, Any] = {"futuresAccountType": self.futures_account_type}
        if symbol:
            payload["symbol"] = format_symbol(symbol)

        await self._subscribe_channel(channel="Positions.change", **payload)

    async def subscribe_order_update(self, symbol: Optional[str] = None):
        payload = {}
        if symbol:
            payload["symbol"] = format_symbol(symbol)

        await self._subscribe_channel(channel="Trade.orderChange", **payload)

    async def new_order(
        self,
        symbol: str,
        side: int,
        amount: float,
        price: Optional[float] = None,
        action: Optional[int] = None,
        client_order_id: Optional[str] = None,
    ):
        payload: Dict[str, Any] = {"symbol": format_symbol(symbol), "side": side, "amount": amount}
        if price is not None:
            payload["price"] = price
        if action is not None:
            payload["actionType"] = action
        if client_order_id is not None:
            payload["clientOrderId"] = client_order_id

        await self._request_channel(channel="Trade.order", **payload)

    async def cancel_order(
        self,
        symbol: str,
        order_id: Optional[str] = None,
        client_order_id: Optional[str] = None,
    ):
        payload: Dict[str, Any] = {"symbol": format_symbol(symbol)}
        if order_id is not None:
            payload["orderId"] = order_id
        elif client_order_id is not None:
            payload["clientOrderId"] = client_order_id

        await self._request_channel(channel="Trade.cancelOrder", **payload)

    async def cancel_open_orders(self, symbol: str):
        payload: Dict[str, Any] = {"symbol": format_symbol(symbol)}
        await self._request_channel(channel="Trade.cancelAllOrders", **payload)

    async def get_trade_list(self, symbol: str, order_id: str):
        payload = {}
        payload["symbol"] = format_symbol(symbol)
        payload["orderId"] = order_id
        await self._request_channel(channel="Trade.getTradeList", **payload)
