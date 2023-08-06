import asyncio
from datetime import timedelta
from typing import Awaitable, Callable, Dict, List  # noqa: TYP001

from aiohttp import ClientConnectorError
from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import Logger
from nautilus_trader.common.timer import TimeEvent
from nautilus_trader.common.uuid import UUIDFactory
from tenacity import retry
from tenacity.retry import retry_if_exception_type

from nacre.network.websocket import WebSocketClient


class ZbWebSocketClient(WebSocketClient):
    """
    Provides a `Zb` streaming WebSocket client.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        clock: LiveClock,
        logger: Logger,
        handler: Callable[[bytes], None],
        base_url: str,
    ):
        super().__init__(
            loop=loop,
            logger=logger,
            handler=handler,
            max_retry_connection=5,
        )

        self._base_url = base_url
        self._clock = clock
        self._subscriptions: Dict[str, Dict] = {}
        self._pager_name = None

        self._post_connect_callbacks: List[Awaitable] = []

    def add_post_connect_callbacks(self, *callbacks: Awaitable):
        self._post_connect_callbacks.extend(callbacks)

    async def post_connection(self):
        # Multiple writer should exist in other tasks
        # Ref: https://docs.aiohttp.org/en/stable/client_quickstart.html#websockets
        self._loop.create_task(self._post_connection())

    async def post_reconnection(self):
        self._loop.create_task(self._post_connection())

    async def _post_connection(self):
        if self._pager_name is None:
            self._set_up_pager()

        await self.on_post_connect()

    def _set_up_pager(self):
        self._pager_name = UUIDFactory().generate().value
        self._clock.set_timer(
            name=self._pager_name,
            interval=timedelta(seconds=3),  # Ping interval Hardcoded for now
            start_time=None,
            stop_time=None,
            callback=self._on_pager_inteval,
        )

    def _on_pager_inteval(self, event: TimeEvent):
        self._loop.create_task(self.ping())

    async def ping(self):
        if not self.retrying:
            try:
                await self.send_json({"action": "ping"})
            except ConnectionResetError:
                return

    async def on_post_connect(self):
        # Resubscribe when reconnect
        if self._subscriptions:
            await self._resubscribe()

        for callback_routine in self._post_connect_callbacks:
            await callback_routine

    async def post_disconnection(self):
        if self._pager_name:
            self._clock.cancel_timer(self._pager_name)
            self._pager_name = None

    async def _resubscribe(self):
        for subscription in self._subscriptions.values():
            self._log.debug(f"Resubscribe {subscription}")
            await self.send_json(subscription)

    @retry(retry=retry_if_exception_type(ClientConnectorError))
    async def connect(self, start: bool = True, **ws_kwargs) -> None:
        if "ws_url" in ws_kwargs:
            ws_kwargs.pop("ws_url")
        try:
            await super().connect(ws_url=self._base_url, start=start, **ws_kwargs)
        except ClientConnectorError as ex:
            self._log.warning(f"{ex}, Retrying...")
            raise ex

    # One time request
    async def _request_channel(self, channel: str, **kwargs):
        payload = {"channel": channel}
        if kwargs:
            payload.update(kwargs)
        await self._send_ws_request(payload)

    # Subscription continues to push when state change
    async def _subscribe_channel(self, channel: str, **kwargs):
        payload = {"channel": channel}
        if kwargs:
            payload.update(kwargs)

        # Resubscribe when reconnect
        hash_key = str(payload.values())
        self._subscriptions[hash_key] = payload
        await self._send_ws_request(payload)

    # Not tested
    async def _unsubscribe_channel(self, channel: str, **kwargs):
        payload = {"channel": channel}
        if kwargs:
            payload.update(kwargs)

        self._subscriptions.pop(channel, None)
        await self._send_ws_request(payload)

    async def _send_ws_request(self, payload: dict):
        while not self.is_connected:
            await self._sleep0()

        await self.send_json(payload)
