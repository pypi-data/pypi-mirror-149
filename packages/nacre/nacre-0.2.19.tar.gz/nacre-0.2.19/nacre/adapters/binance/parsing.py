from decimal import Decimal

from nautilus_trader.adapters.binance.futures.parsing import execution
from nautilus_trader.adapters.binance.futures.schemas.account import BinanceFuturesPositionRisk
from nautilus_trader.core.uuid import UUID4
from nautilus_trader.model.enums import PositionSide
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity

from nacre.execution.reports import PositionStatusReport


# Patch default binance futures execution position reports, added entry price and last price


def parse_position_report_http(
    account_id: AccountId,
    instrument_id: InstrumentId,
    data: BinanceFuturesPositionRisk,
    report_id: UUID4,
    ts_init: int,
) -> PositionStatusReport:
    net_size = Decimal(data.positionAmt)

    if net_size > 0:
        position_side = PositionSide.LONG
    elif net_size < 0:
        position_side = PositionSide.SHORT
    else:
        position_side = PositionSide.FLAT

    return PositionStatusReport(
        account_id=account_id,
        instrument_id=instrument_id,
        position_side=position_side,
        quantity=Quantity.from_str(str(abs(net_size))),
        report_id=report_id,
        entry_px=Price.from_str(data.entryPrice),
        last_px=Price.from_str(data.markPrice),
        ts_last=ts_init,
        ts_init=ts_init,
    )


execution.parse_position_report_http = parse_position_report_http
