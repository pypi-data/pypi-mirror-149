import asyncio
from typing import Any, Dict, List, Optional

from nautilus_trader.core.correctness import PyCondition

from nacre.adapters.zb.common import format_endpoint
from nacre.adapters.zb.common import format_symbol
from nacre.adapters.zb.http.client import ZbHttpClient


class ZbFutureMarketHttpAPI:
    """
    Provides access to the `ZB FUTURE Market` HTTP REST API.
    """

    BASE_ENDPOINT = "/{quote}/api/public/v1/"

    def __init__(self, client: ZbHttpClient):
        """
        Initialize a new instance of the ``ZbFutureMarketHttpAPI`` class.

        Parameters
        ----------
        client : ZbHttpClient
            The Binance REST API client.

        """
        PyCondition.not_none(client, "client")

        self.client = client

    async def market_list(self) -> List[Dict]:
        results = await asyncio.gather(
            self.client.query(url_path="/Server/api/v2/" + "config/marketList"),
            self.client.query(url_path="/qc/Server/api/v2/" + "config/marketList"),
        )
        markets = []
        for res in results:
            markets.extend(res.get("data", []))
        return markets

    async def depth(
        self, symbol: str, size: Optional[int] = None, scale: Optional[int] = None
    ) -> Dict[str, Any]:
        payload: Dict[str, str] = {"symbol": format_symbol(symbol)}
        if size is not None:
            payload["size"] = str(size)
        if scale is not None:
            payload["scale"] = str(scale)

        return await self.client.query(
            url_path=format_endpoint(self.BASE_ENDPOINT, symbol=symbol) + "depth",
            payload=payload,
        )

    async def trades(self, symbol: str, size: Optional[int] = None) -> Dict[str, Any]:
        payload: Dict[str, str] = {"symbol": format_symbol(symbol)}
        if size is not None:
            payload["size"] = str(size)

        return await self.client.query(
            url_path=format_endpoint(self.BASE_ENDPOINT, symbol=symbol) + "trade",
            payload=payload,
        )

    async def klines(
        self,
        symbol: str,
        period: str,
        size: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, str] = {
            "symbol": format_symbol(symbol),
            "period": period,
        }
        if size is not None:
            payload["size"] = str(size)

        return await self.client.query(
            url_path=format_endpoint(self.BASE_ENDPOINT, symbol=symbol) + "kline",
            payload=payload,
        )

    async def mark_klines(
        self,
        symbol: str,
        period: str,
        size: Optional[int] = None,
    ) -> List[List[Any]]:
        payload: Dict[str, str] = {
            "symbol": format_symbol(symbol),
            "period": period,
        }
        if size is not None:
            payload["size"] = str(size)

        return await self.client.query(
            url_path=format_endpoint(self.BASE_ENDPOINT, symbol=symbol) + "markKline",
            payload=payload,
        )

    async def index_klines(
        self,
        symbol: str,
        period: str,
        size: Optional[int] = None,
    ) -> List[List[Any]]:
        payload: Dict[str, str] = {
            "symbol": format_symbol(symbol),
            "period": period,
        }
        if size is not None:
            payload["size"] = str(size)

        return await self.client.query(
            url_path=format_endpoint(self.BASE_ENDPOINT, symbol=symbol) + "indexKline",
            payload=payload,
        )

    async def ticker_price(self, symbol: str = None) -> Dict[str, Any]:
        payload: Dict[str, str] = {}
        if symbol is not None:
            payload["symbol"] = format_symbol(symbol)

        return await self.client.query(
            url_path=format_endpoint(self.BASE_ENDPOINT, symbol=symbol) + "ticker",
            payload=payload,
        )

    async def mark_price(self, symbol: str = None) -> Dict[str, Any]:
        payload: Dict[str, str] = {}
        if symbol is not None:
            payload["symbol"] = format_symbol(symbol)

        return await self.client.query(
            url_path=format_endpoint(self.BASE_ENDPOINT, symbol=symbol) + "markPrice",
            payload=payload,
        )

    async def index_price(self, symbol: str = None) -> Dict[str, Any]:
        payload: Dict[str, str] = {}
        if symbol is not None:
            payload["symbol"] = format_symbol(symbol)

        return await self.client.query(
            url_path=format_endpoint(self.BASE_ENDPOINT, symbol=symbol) + "indexPrice",
            payload=payload,
        )

    async def premium_index(self, symbol: str = None) -> Dict[str, Any]:
        payload: Dict[str, str] = {}
        if symbol is not None:
            payload["symbol"] = format_symbol(symbol)

        return await self.client.query(
            url_path=format_endpoint("/{quote}/Server/api/v2/", symbol=symbol) + "premiumIndex",
            payload=payload,
        )

    async def historical_funding_rate(
        self,
        symbol: str = None,
        start_time_ms: Optional[int] = None,
        end_time_ms: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, str] = {}
        if symbol is not None:
            payload["symbol"] = format_symbol(symbol)
        if start_time_ms is not None:
            payload["startTime"] = str(start_time_ms)
        if end_time_ms is not None:
            payload["endTime"] = str(end_time_ms)
        if limit is not None:
            payload["limit"] = str(limit)

        return await self.client.query(
            url_path=format_endpoint("/{quote}/Server/api/v2/", symbol=symbol) + "fundingRate",
            payload=payload,
        )

    async def historical_liquidated_orders(
        self,
        symbol: str = None,
        start_time_ms: Optional[int] = None,
        end_time_ms: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, str] = {}
        if symbol is not None:
            payload["symbol"] = format_symbol(symbol)
        if start_time_ms is not None:
            payload["startTime"] = str(start_time_ms)
        if end_time_ms is not None:
            payload["endTime"] = str(end_time_ms)
        if limit is not None:
            payload["limit"] = str(limit)

        return await self.client.query(
            url_path=format_endpoint("/{quote}/Server/api/v2/", symbol=symbol) + "allForceOrders",
            payload=payload,
        )

    async def funding_rate(self, symbol: str) -> Dict[str, Any]:
        payload: Dict[str, str] = {"symbol": format_symbol(symbol)}

        return await self.client.query(
            url_path=format_endpoint(self.BASE_ENDPOINT, symbol=symbol) + "fundingRate",
            payload=payload,
        )
