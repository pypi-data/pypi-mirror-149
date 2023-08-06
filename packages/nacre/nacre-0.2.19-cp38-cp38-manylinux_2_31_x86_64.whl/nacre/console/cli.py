import importlib
import os
import sys
from typing import Dict, Optional

import fire
import yaml  # type: ignore
from nautilus_trader.common.actor import Actor
from nautilus_trader.config import ActorFactory
from nautilus_trader.config import ImportableActorConfig
from nautilus_trader.config import ImportableStrategyConfig
from nautilus_trader.config import StrategyFactory
from nautilus_trader.live.node import TradingNode
from nautilus_trader.trading.strategy import TradingStrategy

from nacre.config import TradingNodeConfig


def run():
    fire.Fire(run_live_node)


def run_live_node(config: str, log_path: Optional[str] = None, credential_path: str = "~/.nsrc"):
    with open(config, "r") as stream:
        node_cfg = yaml.safe_load(stream)

    # redirect log
    if log_path is None and "log_path" in node_cfg:
        log_path = node_cfg.pop("log_path")
    if log_path is not None:
        sys.stdout = open(log_path, "w")
        sys.stderr = sys.stdout

    # insert path
    paths = node_cfg.pop("paths", None)
    if paths and isinstance(paths, list):
        for path in paths:
            sys.path.insert(0, path)

    # load api key/sec from default credential path
    _load_credentials(node_cfg, credential_path)

    factories_cfg = node_cfg.pop("factories")

    # initialize actors
    actors = [_build_actor(actor_config) for actor_config in node_cfg.pop("actors", [])]
    # initialize strategies
    strategies = [_build_strategy(strategy) for strategy in node_cfg.pop("strategies", [])]

    node = TradingNode(config=TradingNodeConfig.parse_obj(node_cfg))
    if actors:
        node.trader.add_actors(actors)
    if strategies:
        node.trader.add_strategies(strategies)

    # apply factories
    _add_client_factories(node, factories_cfg)

    node.build()
    try:
        node.start()
    finally:
        node.dispose()


def _import_cls(path: str):
    assert path
    assert ":" in path

    module, cls = path.rsplit(":")
    mod = importlib.import_module(module)
    return getattr(mod, cls)


def _add_client_factories(node: TradingNode, config: Dict):
    if "data_clients" in config:
        for venue, path in config["data_clients"].items():
            node.add_data_client_factory(venue, _import_cls(path))
    if "exec_clients" in config:
        for venue, path in config["exec_clients"].items():
            node.add_exec_client_factory(venue, _import_cls(path))


def _build_actor(actor: Dict) -> Actor:
    config = ImportableActorConfig(**actor)
    return ActorFactory.create(config)


def _build_strategy(strategy: Dict) -> TradingStrategy:
    config = ImportableStrategyConfig(**strategy)
    return StrategyFactory.create(config)


def _load_credentials(node_cfg: Dict, credential_path: str) -> None:
    """
    Fulfill exec_clients with exec_client_ids

    """
    exec_clients = node_cfg.get("exec_clients", {})
    exec_client_ids = node_cfg.pop("exec_client_ids", None)
    if not exec_client_ids:
        return

    with open(os.path.expanduser(credential_path)) as yamlfile:
        account_credentials = yaml.safe_load(yamlfile)["account_credentials"]
        for id, settings in exec_client_ids.items():
            main_venue, _, account_id = id.partition("-")
            creds = account_credentials.get(id, {})

            # For each exec_client_id generate SPOT and FUTURE exec_client separately
            for account_type in ("SPOT", "FUTURE"):
                client_id = f"{main_venue}_{account_type}-{account_id}"
                override_settings = {"defaultType": account_type.lower(), **creds, **settings}
                if client_id in exec_clients:
                    for key, val in override_settings.items():
                        if key not in exec_clients[client_id]:
                            exec_clients[client_id][key] = val
                else:
                    exec_clients[client_id] = override_settings

    node_cfg["exec_clients"] = exec_clients
