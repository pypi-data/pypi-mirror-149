# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2021 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

import asyncio
import types
from asyncio import Task
from typing import Callable, List, Optional

import aiohttp
from aiohttp import WSMessage

from nautilus_trader.common.logging cimport LogColor
from nautilus_trader.common.logging cimport Logger
from nautilus_trader.common.logging cimport LoggerAdapter
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.network.websocket cimport WebSocketClient as NautilusWebSocketClient

from nautilus_trader.network.error import MaxRetriesExceeded

from nacre.metrics.metrics import WEBSOCKET_DISCONNECT_COUNTER
from nacre.metrics.metrics import WEBSOCKET_RECONNECT_BACKOFF
from nacre.metrics.metrics import WEBSOCKET_RECV_ERROR_COUNTER


# from nautilus_trader.network.websocket cimport WSMsgType



cpdef enum WSMsgType:
    # websocket spec types
    CONTINUATION = 0x0
    TEXT = 0x1
    BINARY = 0x2
    PING = 0x9
    PONG = 0xA
    CLOSE = 0x8
    # aiohttp specific types
    CLOSING = 0x100
    CLOSED = 0x101
    ERROR = 0x102


cdef class WebSocketClient(NautilusWebSocketClient):
    def __init__(
        self,
        loop not None: asyncio.AbstractEventLoop,
        Logger logger not None: Logger,
        handler not None: Callable[[bytes], None],
        int max_retry_connection=0,
        bytes pong_msg=None,
        bint log_send=False,
        bint log_recv=False,
    ):
        super().__init__(
            loop=loop,
            logger=logger,
            handler=handler,
            max_retry_connection=max_retry_connection,
            pong_msg=pong_msg,
            log_send=log_send,
            log_recv=log_recv,
        )
        self.retrying = False

    async def receive(self) -> Optional[bytes]:
        cdef WSMsgType msg_type
        try:
            msg: WSMessage = await self._ws.receive()
            msg_type = msg.type
            if msg_type == TEXT:
                return msg.data.encode()  # Current workaround to always return bytes
            elif msg_type == BINARY:
                return msg.data
            elif msg_type == ERROR:  # aiohttp specific
                if self._stopping is True:
                    return
                self._log.warning(f"[RECV] {msg}.")
                raise ConnectionAbortedError("websocket aiohttp error")
            elif msg_type == CLOSE:  # Received CLOSE from server
                if self._stopping is True:
                    return
                self._log.warning(f"[RECV] {msg}.")
                raise ConnectionAbortedError("websocket closed by server")
            elif msg_type == CLOSING or msg_type == CLOSED:  # aiohttp specific
                if self._stopping is True:
                    return
                self._log.warning(f"[RECV] {msg}.")
                raise ConnectionAbortedError("websocket aiohttp closing or closed")
            else:
                self._log.warning(
                    f"[RECV] unknown data type: {msg.type}, data: {msg.data}.",
                )
                self.unknown_message_count += 1
                if self.unknown_message_count > 20:
                    self.unknown_message_count = 0  # Reset counter
                    # This shouldn't be happening, trigger a reconnection
                    raise ConnectionAbortedError("Too many unknown messages")
                return b""
        except (asyncio.IncompleteReadError, ConnectionAbortedError, RuntimeError) as ex:
            try:
                self.retrying = True
                WEBSOCKET_DISCONNECT_COUNTER.labels(endpoint=self._ws_url).inc()
                self._log.warning(
                    f"{ex.__class__.__name__}: Reconnecting {self.connection_retry_count=}, "
                    f"{self.max_retry_connection=}",
                )
                if self.max_retry_connection == 0:
                    raise
                if self.connection_retry_count > self.max_retry_connection:
                    raise MaxRetriesExceeded(f"Max retries of {self.max_retry_connection} exceeded.")
                await self._reconnect_backoff()
                self.connection_retry_count += 1
                self._log.debug(
                    f"Attempting reconnect (attempt: {self.connection_retry_count}).",
                )
                await self.reconnect()
            finally:
                self.retrying = False

    async def _reconnect_backoff(self) -> None:
        if self.connection_retry_count == 0:
            return  # Immediately attempt first reconnect
        cdef double backoff = 1.5 ** self.connection_retry_count
        WEBSOCKET_RECONNECT_BACKOFF.labels(endpoint=self._ws_url).set(backoff)
        self._log.debug(
            f"Exponential backoff attempt "
            f"{self.connection_retry_count}, sleeping for {backoff}",
        )
        await asyncio.sleep(backoff)

    async def start(self) -> None:
        self._log.debug("Starting recv loop...")
        cdef bytes raw
        while not self._stopping:
            try:
                raw = await self.receive()
                if self._log_recv:
                    self._log.info(f"[RECV] {raw}.", LogColor.BLUE)
                if raw is None:
                    continue
                if self._pong_msg is not None and raw == self._pong_msg:
                    continue  # Filter pong message
                self._handler(raw)
                self.connection_retry_count = 0
            except MaxRetriesExceeded as ex:
                self._log.exception("Error on max retry", ex)
                await self._reset_retry_count()  # Always retry don't stop!
                self._log.debug("Start new round.")
            except Exception as ex:
                WEBSOCKET_RECV_ERROR_COUNTER.labels(endpoint=self._ws_url).inc()
                self._log.exception(f"Error on receive", ex)
                # Always retry!!
                # break
        self._log.debug("Stopped.")
        self._stopped = True

    async def _reset_retry_count(self):
        nap = 2
        self.connection_retry_count = 0
        self._log.warning(f"Reset count and sleep for {nap} seconds")
        await asyncio.sleep(nap)
