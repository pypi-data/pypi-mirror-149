#!/usr/bin/env python3
from nautilus_trader.config import InstrumentProviderConfig

# from nautilus_trader.config import CacheDatabaseConfig
from nautilus_trader.live.node import TradingNode
from nautilus_trader.model.enums import OMSType

# from nacre.config.actors import KafkaConfig
from nacre.adapters.zb.common.enums import ZbAccountType
from nacre.adapters.zb.config import ZbDataClientConfig
from nacre.adapters.zb.config import ZbExecClientConfig
from nacre.adapters.zb.factories import ZbLiveDataClientFactory
from nacre.adapters.zb.factories import ZbLiveExecClientFactory

# from nacre.infrastructure.kafka import KafkaPubSub
from nacre.config import TradingNodeConfig
from nacre.examples.strategies.mon import Mon
from nacre.examples.strategies.mon import MonConfig


# os.environ["PYTHONASYNCIODEBUG"] = "1"
# import logging
# logging.basicConfig(level=logging.DEBUG)

# sys.stdout = open("/var/log/nacre/watcher.log", 'w')
# sys.stderr = sys.stdout


# Configure the trading node
config_node = TradingNodeConfig(
    trader_id="MM-001",
    log_level="DEBUG",
    data_clients={
        "ZB": ZbDataClientConfig(
            account_type=ZbAccountType.FUTURES_USDT,
            # instrument_provider=InstrumentProviderConfig(load_ids=["ZETH/ZUSD.ZB"]),
            instrument_provider=InstrumentProviderConfig(load_all=True),
            base_url_http="https://futures.zb.zone",
            base_url_ws="wss://futures.zb.zone/ws/public/v1",
        ),
        # "ZB": ZbDataClientConfig(
        #     account_type=ZbAccountType.SPOT,
        #     # instrument_provider=InstrumentProviderConfig(load_ids=["ZETH/ZUSD.ZB"]),
        #     instrument_provider=InstrumentProviderConfig(load_all=True),
        # ),
    },
    exec_clients={
        "ZB": ZbExecClientConfig(  # noqa: S106
            api_key="",
            api_secret="",
            oms_type=OMSType.NETTING,
            account_type=ZbAccountType.FUTURES_USDT,
            instrument_provider=InstrumentProviderConfig(load_all=True),
            # base_url_http="https://futures.zb.zone",
            # base_url_ws="wss://futures.zb.zone/ws/private/api/v2",
        ),
    },
    # cache_database=CacheDatabaseConfig(),
    # timeout_disconnection=30,
    # timeout_connection=30,
)
# Instantiate the node with a configuration
node = TradingNode(config=config_node)


# actor = KafkaPubSub(
#     config=KafkaConfig(
#         bootstrap_servers="192.168.18.4:19092,192.168.18.4:29092,192.168.18.4:39092",
#         schema_registry="http://192.168.18.4:8081",
#         topic_filters=["events.order*", "events.position*"],
#     )
# )
# node.trader.add_actor(actor)

stra = Mon(
    config=MonConfig(
        venues="ZB",
        oms_type="NETTING",
    )
)
node.trader.add_strategy(stra)

node.add_data_client_factory("ZB", ZbLiveDataClientFactory)
node.add_exec_client_factory("ZB", ZbLiveExecClientFactory)
node.build()

# Stop and dispose of the node with SIGINT/CTRL+C
if __name__ == "__main__":
    try:
        node.start()
    finally:
        node.dispose()
