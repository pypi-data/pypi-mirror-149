import asyncio

import orjson
import pydantic

from libc.stdint cimport int64_t

from json.decoder import JSONDecodeError
from typing import Dict, Optional, Union

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from prometheus_async import aio

from nautilus_trader.common.actor cimport Actor
from nautilus_trader.common.logging cimport LogColor
from nautilus_trader.common.logging cimport Logger
from nautilus_trader.common.logging cimport LoggerAdapter
from nautilus_trader.common.logging cimport LogLevel
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.model.data.base cimport DataType
from nautilus_trader.model.data.base cimport GenericData
from nautilus_trader.model.data.tick cimport QuoteTick
from nautilus_trader.model.data.tick cimport TradeTick
from nautilus_trader.model.objects cimport BaseDecimal

from nacre.config import ExposerConfig
from nacre.model.data.tick cimport MarkTick


def default(obj):
    if isinstance(obj, BaseDecimal):
        return str(obj.as_decimal())
    raise TypeError

cdef class AccessLoggerAdapter(LoggerAdapter):
    cpdef void info(
        self, str msg,
        LogColor color=LogColor.NORMAL,
        dict extra=None,
    ) except *:
        """
        Log the given information message with the logger.

        Parameters
        ----------
        msg : str
            The message to log.
        color : LogColor, optional
            The color for the log record.
        extra : dict[str, object], optional
            The annotations for the log record.

        """
        Condition.not_none(msg, "msg")

        if self.is_bypassed:
            return

        cdef dict record = self._logger.create_record(
            level=LogLevel.DEBUG,  # Hard code for now, metrics log might be too much for INFO level
            color=color,
            component=self.component,
            msg=msg,
            annotations=extra,
        )

        self._logger.log_c(record)



cdef class Exposer(Actor):
    """
    Expose nacre internal states via http endpoint

    Parameters
    ----------
    config : ExposerConfig
        The actor configuration.

    Raises
    ------
    TypeError
        If `config` is not of type `ExposerConfig`.
    """
    def __init__(self, config: ExposerConfig):
        super().__init__(config)

        self._run_http_server_task = None
        self._runner = None
        self._loop = asyncio.get_event_loop()

        self.trader = None  # Initialized when registered

    cpdef void register_trader(self, Trader trader) except *:
        Condition.not_none(trader, "trader")
        self.trader = trader

    cpdef void on_start(self) except *:
        self._run_http_server_task = self._loop.create_task(self._run_web_server())
        self._log.info(f"Scheduled {self._run_http_server_task}")

    cpdef void on_stop(self) except *:
        self._loop.create_task(self._stop_server())

    async def _run_web_server(self):
        self._log.info(f"HTTP server starting...")

        app = web.Application()
        app.add_routes([
            # General
            web.get('/health', self.expose_health),
            web.get('/metrics', aio.web.server_stats),
        ])

        access_log = AccessLoggerAdapter(
            component_name=self.type.__name__,
            logger=self._log.get_logger(),
        )

        self._runner = web.AppRunner(
            app,
            access_log=access_log,
        )

        await self._runner.setup()
        site = web.TCPSite(
            self._runner,
            self._config.get("host"),
            self._config.get("port"),
        )

        await site.start()
        self._log.info(f"HTTP server started")

    async def _stop_server(self):
        if self._runner:
            await self._runner.shutdown()
        self._log.info(f"HTTP server stopped")

    async def expose_health(self, request):
        return web.json_response({"status": "OK"})
