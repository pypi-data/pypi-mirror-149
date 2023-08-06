# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2021 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

import asyncio

from libc.stdint cimport int64_t
from nautilus_trader.common.logging cimport LogColor
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.execution.reports cimport ExecutionMassStatus
from nautilus_trader.execution.reports cimport OrderStatusReport
from nautilus_trader.execution.reports cimport TradeReport
from nautilus_trader.live.execution_client cimport LiveExecutionClient as NautilusLiveExecutionClient
from nautilus_trader.model.identifiers cimport AccountId
from nautilus_trader.model.identifiers cimport InstrumentId


cdef class LiveExecutionClient(NautilusLiveExecutionClient):
    cpdef void _set_venue(self, Venue venue) except *:
        Condition.not_none(venue, "venue")
        self.venue = venue

    cpdef void _set_account_id(self, AccountId account_id) except *:
        Condition.not_none(account_id, "account_id")
        # Override check
        # Condition.equal(self.id.value, account_id.issuer, "id.value", "account_id.issuer")

        self.account_id = account_id

    async def generate_mass_status(self, lookback_mins: Optional[int]):
        full_mass_status = await super().generate_mass_status(lookback_mins)

        cdef ExecutionMassStatus mass_status = ExecutionMassStatus(
            client_id=self.id,
            account_id=self.account_id,
            venue=self.venue,
            report_id=self._uuid_factory.generate(),
            ts_init=self._clock.timestamp_ns(),
        )

        instrument_id_filters = self._instrument_provider._load_ids_on_start
        if instrument_id_filters is None:
            return full_mass_status

        instrument_ids = [InstrumentId.from_str_c(i) for i in instrument_id_filters]

        self._log.info(f"Filtering ExecutionMassStatus by instrument ids {instrument_id_filters}.")
        # Filter mass_status with instrument only specified on providers
        order_reports = []
        for order_report in full_mass_status.order_reports().values():
            if order_report.instrument_id in instrument_ids:
                order_reports.append(order_report)

        trade_reports = []
        for trade_reports_group in full_mass_status.trade_reports().values():
            if trade_reports_group[0].instrument_id in instrument_ids:
                trade_reports.extend(trade_reports_group)

        position_reports = []
        for instrument_id, position_reports_group in full_mass_status.position_reports().items():
            if instrument_id in instrument_ids:
                position_reports.extend(position_reports_group)

        mass_status.add_order_reports(reports=order_reports)
        mass_status.add_trade_reports(reports=trade_reports)
        mass_status.add_position_reports(reports=position_reports)

        return mass_status

    cpdef void _send_order_status_report(self, OrderStatusReport report) except *:
        # Filter report first
        instrument_id_filters = self._instrument_provider._load_ids_on_start
        if instrument_id_filters is not None:
            instrument_ids = [InstrumentId.from_str_c(i) for i in instrument_id_filters]
            if report.instrument_id not in instrument_ids:
                self._log.info(f"Ignoring {report}.", color=LogColor.BLUE)
                return

        self._msgbus.send(
            endpoint="ExecEngine.reconcile_report",
            msg=report,
        )

    cpdef void _send_trade_report(self, TradeReport report) except *:
        # Filter report first
        instrument_id_filters = self._instrument_provider._load_ids_on_start
        if instrument_id_filters is not None:
            instrument_ids = [InstrumentId.from_str_c(i) for i in instrument_id_filters]
            if report.instrument_id not in instrument_ids:
                self._log.info(f"Ignoring {report}.", color=LogColor.BLUE)
                return

        self._msgbus.send(
            endpoint="ExecEngine.reconcile_report",
            msg=report,
        )
