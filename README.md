# ERPNext Construction EPC & Running Account (RA) Billing 🏗️📐

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An enterprise infrastructure EPC contract billing, Joint Measurement Sheet (JMC) verification, Running Account (RA) bill certification, and retention money escrow engine for **ERPNext Projects & Real Estate Construction** (L&T, Tata Projects, Shapoorji Pallonji scale).

---

## 🚀 Key Features

- **Running Account (RA) Certification**: Computes work-in-progress (WIP) quantities against Bill of Quantities (BOQ) contracted rates.
- **Contractual Retention Escrow (5%)**: Automatically withholds defect liability retention money released only post-project commissioning.
- **Mobilization Advance Amortization**: Recovers upfront contractor advance payments progressively across certified RA bills.
- **Statutory Tax Deductions**: Handles Section 194C TDS withholding and GST TDS integration with ERPNext `Purchase Invoice`.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/erpnext-construction-epc-billing-ra-bill.git
cd erpnext-construction-epc-billing-ra-bill
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from epc.engine import ConstructionEPCBillingEngine, WorkItemMeasurement

engine = ConstructionEPCBillingEngine(retention_pct=5.0, advance_recovery_pct=10.0, tds_pct=2.0)

bill = engine.generate_ra_bill(
    bill_number="RA-04",
    project_code="HIGHWAY-PACKAGE-2",
    contractor="Dilip Buildcon Ltd",
    measurements=[
        WorkItemMeasurement(item_code="EARTHWORK-EXCAV", description="Excavation in Hard Rock", unit_of_measure="CUM", contracted_rate=450.0, previous_cumulative_quantity=2000.0, current_bill_quantity=500.0)
    ]
)
print(f"Gross: ₹{bill.current_gross_work_done} | Net Payable: ₹{bill.net_payable_amount} | Retention: ₹{bill.retention_money_withheld}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
