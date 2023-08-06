import asyncio
import socket
import urllib.parse
from ssl import SSLContext
from typing import Dict, List, Optional, Union

import aiohttp
import cython
from aiohttp import ClientResponse
from aiohttp import ClientResponseError
from aiohttp import ClientSession
from aiohttp import Fingerprint

from nacre.metrics.metrics import HTTP_ERROR_COUNTER
from nacre.metrics.metrics import REQ_TIME

from nautilus_trader.common.logging cimport Logger
from nautilus_trader.common.logging cimport LoggerAdapter
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.network.http cimport HttpClient as NautilusHttpClient


cdef int ONE_DAY = 86_400


cdef class HttpClient(NautilusHttpClient):
    def raise_for_status(self, resp: ClientResponse):
        if not resp.ok:
            # reason should always be not None for a started response
            assert resp.reason is not None
            resp.release()

            message = resp.reason
            if resp.data is not None:
                message = resp.data.decode(resp.get_encoding())
            raise ClientResponseError(
                resp.request_info,
                resp.history,
                status=resp.status,
                message=message,
                headers=resp.headers,
            )

    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]]=None,
        json: Optional[Dict[str, str]]=None,
        **kwargs,
    ) -> ClientResponse:
        session: ClientSession = self._get_session()
        if session.closed:
            self._log.warning("Session closed: reconnecting.")
            await self.connect()


        with REQ_TIME.labels(method=method, endpoint=url).time():
            with HTTP_ERROR_COUNTER.labels(
                method=method, endpoint=url
            ).count_exceptions():
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json,
                    **kwargs
                ) as resp:
                    # Get data first
                    resp.data = await resp.read()
                    self.raise_for_status(resp)
                    return resp
