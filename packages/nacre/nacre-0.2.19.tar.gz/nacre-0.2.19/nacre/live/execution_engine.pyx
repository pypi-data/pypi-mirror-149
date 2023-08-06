
import asyncio
from decimal import Decimal

from nautilus_trader.cache.cache cimport Cache
from nautilus_trader.common.clock cimport LiveClock
from nautilus_trader.common.logging cimport Logger
from nautilus_trader.model.position cimport Position
from nautilus_trader.msgbus.bus cimport MessageBus

from typing import Optional

from nacre.config.live import LiveExecEngineConfig

from nautilus_trader.execution.reports cimport OrderStatusReport
from nautilus_trader.execution.reports cimport PositionStatusReport
from nautilus_trader.execution.reports cimport TradeReport
from nautilus_trader.live.execution_engine cimport LiveExecutionEngine as NautilusLiveExecutionEngine
from nautilus_trader.model.c_enums.liquidity_side cimport LiquiditySide
from nautilus_trader.model.c_enums.order_side cimport OrderSide
from nautilus_trader.model.c_enums.order_status cimport OrderStatus
from nautilus_trader.model.c_enums.order_type cimport OrderType
from nautilus_trader.model.c_enums.position_side cimport PositionSide
from nautilus_trader.model.c_enums.time_in_force cimport TimeInForce
from nautilus_trader.model.currency cimport Currency
from nautilus_trader.model.identifiers cimport TradeId
from nautilus_trader.model.identifiers cimport VenueOrderId
from nautilus_trader.model.objects cimport Money
from nautilus_trader.model.objects cimport Price


# from nacre.execution.reports cimport PositionStatusReport

cdef class LiveExecutionEngine(NautilusLiveExecutionEngine):
    def __init__(
        self,
        loop not None: asyncio.AbstractEventLoop,
        MessageBus msgbus not None,
        Cache cache not None,
        LiveClock clock not None,
        Logger logger not None,
        config: Optional[LiveExecEngineConfig]=None,
    ):
        super().__init__(loop, msgbus, cache, clock, logger, config)
        self.reconcile_by_fake_fills = config.reconcile_by_fake_fills if config else False

    cdef bint _reconcile_position_report_hedging(self, PositionStatusReport report) except *:
        if self.reconcile_by_fake_fills:
            self._generate_fake_fills(report)

        cdef Position position = self._cache.position(report.venue_position_id)
        if position is None:
            self._log.error(
                f"Cannot reconcile position: "
                f"position ID {report.venue_position_id} not found.",
            )
            return False  # Failed
        if position.net_qty != report.net_qty:
            self._log.error(
                f"Cannot reconcile position: "
                f"position ID {report.venue_position_id} "
                f"net qty {position.net_qty} != reported {report.net_qty}. "
                f"{report}.",
            )
            return False  # Failed

        return True  # Reconciled

    cdef bint _reconcile_position_report_netting(self, PositionStatusReport report) except *:
        if self.reconcile_by_fake_fills:
            self._generate_fake_fills(report)

        cdef list positions_open = self._cache.positions_open(
            venue=None,  # Faster query filtering
            instrument_id=report.instrument_id,
        )
        net_qty = Decimal(0)
        for position in positions_open:
            net_qty += position.net_qty
        if net_qty != report.net_qty:
            self._log.error(
                f"Cannot reconcile position: "
                f"{report.instrument_id} "
                f"net qty {net_qty} != reported {report.net_qty}.",
            )
            return False  # Failed

        return True  # Reconciled

    cpdef void _generate_fake_fills(self, PositionStatusReport report) except *:
        self._log.warning(f"Generating fake fills to pass reconcile check.")

        ts = self._clock.timestamp_ns()
        fake_venue_order_id = VenueOrderId(f"FAKE_ORDER-{ts}")
        # Require exec client generate
        #   nacre.execution.reports.PositionStatusReport
        #   instead of
        #   nautilus_trader.execution.reports.PositionStatusReport
        entry_price = report.entry_px

        order_report = OrderStatusReport(
            account_id=report.account_id,
            instrument_id=report.instrument_id,
            client_order_id=None,
            venue_order_id=fake_venue_order_id,
            order_side=OrderSide.BUY if report.position_side == PositionSide.LONG else OrderSide.SELL,
            order_type=OrderType.LIMIT,
            time_in_force=TimeInForce.GTC,
            order_status=OrderStatus.FILLED,
            price=entry_price,
            quantity=report.quantity,
            filled_qty=report.quantity,
            avg_px=entry_price,
            post_only=False,
            reduce_only=False,
            report_id=self._uuid_factory.generate(),
            ts_accepted=ts,
            ts_last=ts,
            ts_init=ts,
            trigger_price=None,
        )

        trade = TradeReport(
            account_id=order_report.account_id,
            instrument_id=order_report.instrument_id,
            venue_order_id=order_report.venue_order_id,
            venue_position_id=report.venue_position_id,
            trade_id=TradeId(self._uuid_factory.generate().value),
            order_side=order_report.order_side,
            last_qty=order_report.quantity,
            last_px=entry_price,
            commission=Money(0, Currency.from_str("USDT")),  # HARDCODE for now
            liquidity_side=LiquiditySide.TAKER,
            report_id=self._uuid_factory.generate(),
            ts_event=ts,
            ts_init=ts,
        )

        success = self._reconcile_order_report(order_report, [trade])
        self._log.info(f"Generated fake fills {success}")
