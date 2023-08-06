from typing import Optional

from nautilus_trader.config import TradingNodeConfig as NautilusTradingNodeConfig

from nacre.config.actors import ExposerConfig
from nacre.config.actors import PubSubConfig
from nacre.config.live import LiveExecEngineConfig


class TradingNodeConfig(NautilusTradingNodeConfig):
    """
    Configuration for ``TradingNode`` instances.

    pubsub: PubSubConfig, optional
        The config for external msgbus pubsub
    exposer: ExposerConfig, optional
        The config for exposer
    """

    exec_engine: LiveExecEngineConfig = (
        LiveExecEngineConfig()
    )  # Override default execute engine config
    pubsub: Optional[PubSubConfig] = None
    exposer: Optional[ExposerConfig] = None
