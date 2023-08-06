from enum import Enum
from enum import unique


@unique
class ZbAccountType(Enum):
    """Represents a `Zb` account type"""

    SPOT = "SPOT"
    MARGIN = "MARGIN"
    FUTURES_USDT = "FUTURES_USDT"
    FUTURES_COIN = "FUTURES_COIN"

    @property
    def is_spot(self):
        return self == ZbAccountType.SPOT

    @property
    def is_margin(self):
        return self == ZbAccountType.MARGIN

    @property
    def is_futures(self) -> bool:
        return self in (ZbAccountType.FUTURES_USDT, ZbAccountType.FUTURES_COIN)
