"""Construction EPC Project Ledger & Running Account (RA) Billing Engine."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class WorkItemMeasurement:
    item_code: str
    description: str
    unit_of_measure: str  # CUM, MT, SQM
    contracted_rate: float
    previous_cumulative_quantity: float
    current_bill_quantity: float


@dataclass
class RABillStatement:
    bill_number: str
    project_code: str
    contractor: str
    current_gross_work_done: float
    retention_money_withheld: float
    mobilization_advance_recovery: float
    tds_withheld_2pct: float
    net_payable_amount: float
    cumulative_work_done_total: float


class ConstructionEPCBillingEngine:
    """Manages EPC Contract milestone billing, RA bills, retention escrows, and mobilization recovery."""

    def __init__(self, retention_pct: float = 5.0, advance_recovery_pct: float = 10.0, tds_pct: float = 2.0):
        self.retention_pct = retention_pct
        self.advance_recovery_pct = advance_recovery_pct
        self.tds_pct = tds_pct

    def generate_ra_bill(
        self,
        bill_number: str,
        project_code: str,
        contractor: str,
        measurements: List[WorkItemMeasurement],
        cumulative_previous_billed_value: float = 0.0
    ) -> RABillStatement:
        current_gross = 0.0
        for item in measurements:
            item_gross = item.current_bill_quantity * item.contracted_rate
            current_gross += item_gross

        current_gross = round(current_gross, 2)
        retention = round((current_gross * self.retention_pct) / 100.0, 2)
        advance_recovery = round((current_gross * self.advance_recovery_pct) / 100.0, 2)
        tds = round((current_gross * self.tds_pct) / 100.0, 2)

        total_deductions = retention + advance_recovery + tds
        net_payable = round(current_gross - total_deductions, 2)
        cumulative_total = round(cumulative_previous_billed_value + current_gross, 2)

        return RABillStatement(
            bill_number=bill_number,
            project_code=project_code,
            contractor=contractor,
            current_gross_work_done=current_gross,
            retention_money_withheld=retention,
            mobilization_advance_recovery=advance_recovery,
            tds_withheld_2pct=tds,
            net_payable_amount=net_payable,
            cumulative_work_done_total=cumulative_total
        )
