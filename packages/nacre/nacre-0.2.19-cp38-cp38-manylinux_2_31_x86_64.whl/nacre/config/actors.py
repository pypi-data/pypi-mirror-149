from typing import List

from nautilus_trader.config import ActorConfig


class ExposerConfig(ActorConfig):
    """
    Configuration for ``PubSub`` instances.

    host : str
        listen interface
    port : int
        listen port
    """

    host: str = "127.0.0.1"
    port: int = 8080


class PubSubConfig(ActorConfig):
    """
    Configuration for ``PubSub`` instances.

    topic_filters : list
        List of topic filters separated by comma.
    """

    topic_filters: List[str] = []


class KafkaConfig(PubSubConfig):
    """
    Configuration for ``KafkaPubSub`` instances.

    bootstrap_servers : str
        Kafka bootstrap_servers
    security_protocol : str
        Security protocol
    schema_registry : bool
        Confluentinc schema registry url.
    """

    bootstrap_servers: str = "localhost:9092"
    security_protocol: str = "PLAINTEXT"
    schema_registry: str = "http://localhost:8081"
