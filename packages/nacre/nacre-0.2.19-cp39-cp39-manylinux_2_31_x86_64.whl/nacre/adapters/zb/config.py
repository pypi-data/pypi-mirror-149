from typing import Optional

from nautilus_trader.config.live import LiveDataClientConfig
from nautilus_trader.config.live import LiveExecClientConfig
from nautilus_trader.model.enums import OMSType

from nacre.adapters.zb.common.enums import ZbAccountType


class ZbDataClientConfig(LiveDataClientConfig):
    """
    Configuration for ``ZbDataClient`` instances.
    Parameters
    ----------
    api_key : str, optional
        The Zb API public key.
    api_secret : str, optional
        The Zb API private key.
    account_type : ZbAccountType, default ZbAccountType.SPOT
        The account type for the client.
    base_url_http : str, optional
        The HTTP client custom endpoint override.
    base_url_ws : str, optional
        The WebSocket client custom endpoint override.
    http_proxy : str, optional
        The HTTP proxy url.
    """

    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    account_type: ZbAccountType = ZbAccountType.SPOT
    base_url_http: Optional[str] = None
    base_url_ws: Optional[str] = None
    http_proxy: Optional[str] = None


class ZbExecClientConfig(LiveExecClientConfig):
    """
    Configuration for ``ZbExecutionClient`` instances.
    Parameters
    ----------
    api_key : str, optional
        The Zb API public key.
    api_secret : str, optional
        The Zb API private key.
    oms_type: OMSType, default OMSType.NETTING
        OMSType for ZB, NETTING on spot, NETTING/HEDGING on futures
    account_type : ZbAccountType, default ZbAccountType.SPOT
        The account type for the client.
    base_url_http : str, optional
        The HTTP client custom endpoint override.
    base_url_ws : str, optional
        The WebSocket client custom endpoint override.
    http_proxy : str, optional
        The HTTP proxy url.
    """

    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    oms_type: OMSType = OMSType.NETTING
    account_type: ZbAccountType = ZbAccountType.SPOT
    base_url_http: Optional[str] = None
    base_url_ws: Optional[str] = None
    http_proxy: Optional[str] = None
