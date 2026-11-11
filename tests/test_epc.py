import unittest
from epc.engine import ConstructionEPCBillingEngine, WorkItemMeasurement


class TestConstructionEPCBilling(unittest.TestCase):
    def setUp(self):
        self.engine = ConstructionEPCBillingEngine(retention_pct=5.0, advance_recovery_pct=10.0, tds_pct=2.0)

    def test_ra_bill_generation(self):
        items = [
            WorkItemMeasurement(
                item_code="CIVIL-RCC-M25",
                description="RCC M25 Grade Casting",
                unit_of_measure="CUM",
                contracted_rate=6500.0,
                previous_cumulative_quantity=100.0,
                current_bill_quantity=50.0  # 50 * 6500 = 325,000
            ),
            WorkItemMeasurement(
                item_code="STEEL-REBAR-TMT",
                description="TMT Rebar Fe550D Binding",
                unit_of_measure="MT",
                contracted_rate=62000.0,
                previous_cumulative_quantity=20.0,
                current_bill_quantity=10.0  # 10 * 62000 = 620,000
            )
        ]
        # Current Gross = 325,000 + 620,000 = 945,000
        # Retention (5%) = 47,250
        # Advance Recovery (10%) = 94,500
        # TDS (2%) = 18,900
        # Total Deductions = 160,650 -> Net = 784,350
        bill = self.engine.generate_ra_bill(
            bill_number="RA-BILL-03",
            project_code="METRO-VIADUCT-P4",
            contractor="L&T Heavy Civil Infra",
            measurements=items,
            cumulative_previous_billed_value=1500000.0
        )
        self.assertEqual(bill.current_gross_work_done, 945000.0)
        self.assertEqual(bill.retention_money_withheld, 47250.0)
        self.assertEqual(bill.mobilization_advance_recovery, 94500.0)
        self.assertEqual(bill.tds_withheld_2pct, 18900.0)
        self.assertEqual(bill.net_payable_amount, 784350.0)
        self.assertEqual(bill.cumulative_work_done_total, 2445000.0)


if __name__ == "__main__":
    unittest.main()
