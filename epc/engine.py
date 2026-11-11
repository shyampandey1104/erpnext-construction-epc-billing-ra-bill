"""Construction EPC Contract Billing, Running Account (RA) Certification & Retention Escrow Engine."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class WorkItemMeasurement(BaseModel):
    item_code: str
    description: str     # e.g., RCC M25 Concrete, Structural Steel Fabrication
    unit_of_measure: str # CUM, SQM, MT
    contracted_rate: float
    previous_cumulative_quantity: float
    current_bill_quantity: float


class RABillCertificate(BaseModel):
    bill_number: str       # e.g., "RA-BILL-04"
    project_code: str
    contractor_name: str
    current_gross_work_done: float
    cumulative_work_done_total: float
    retention_money_withheld: float      # 5% withheld until defect liability period
    mobilization_advance_recovery: float # 10% amortized recovery
    tds_withheld_2pct: float             # Section 194C TDS
    net_payable_amount: float
    status: str = "APPROVED_BY_PROJECT_HEAD"


class ConstructionEPCBillingEngine:
    """Manages infrastructure Running Account (RA) bills, retention escrow, and advances."""

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
    ) -> RABillCertificate:
        current_gross = 0.0

        for m in measurements:
            item_val = m.current_bill_quantity * m.contracted_rate
            current_gross += item_val

        cumulative_total = cumulative_previous_billed_value + current_gross

        # Deductions
        retention = current_gross * (self.retention_pct / 100.0)
        advance_recovery = current_gross * (self.advance_recovery_pct / 100.0)
        tds = current_gross * (self.tds_pct / 100.0)

        total_deductions = retention + advance_recovery + tds
        net_payable = max(0.0, current_gross - total_deductions)

        return RABillCertificate(
            bill_number=bill_number,
            project_code=project_code,
            contractor_name=contractor,
            current_gross_work_done=round(current_gross, 2),
            cumulative_work_done_total=round(cumulative_total, 2),
            retention_money_withheld=round(retention, 2),
            mobilization_advance_recovery=round(advance_recovery, 2),
            tds_withheld_2pct=round(tds, 2),
            net_payable_amount=round(net_payable, 2),
            status="APPROVED_BY_PROJECT_HEAD"
        )
