# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "epc"
app_title = "Erpnext Construction Epc Billing Ra Bill"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Construction Epc Billing Ra Bill for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/epc/css/epc.bundle.css"
app_include_js = "/assets/epc/js/epc.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "epc.engine.on_document_submit",
        "on_cancel": "epc.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "epc.engine.daily_scheduled_sync"
    ]
}
