from nautilus_trader.config.live import LiveExecEngineConfig as NautilusLiveExecEngineConfig


class LiveExecEngineConfig(NautilusLiveExecEngineConfig):
    reconcile_by_fake_fills: bool = False
