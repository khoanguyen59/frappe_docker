import frappe


@frappe.whitelist()
def get_dashboard_data():
    if frappe.session.user == "Guest":
        frappe.throw("Login required")

    company = (
        frappe.defaults.get_user_default("company")
        or frappe.defaults.get_user_default("Company")
        or frappe.db.get_single_value("Global Defaults", "default_company")
    )

    job_filters = {}
    if company and frappe.db.exists("DocType", "Logistics Job"):
        job_filters["company"] = company

    jobs_total = frappe.db.count("Logistics Job", filters=job_filters) if frappe.db.exists("DocType", "Logistics Job") else 0
    jobs_payment = (
        frappe.db.count("Logistics Job", filters={**job_filters, "order_status": "payment"})
        if frappe.db.exists("DocType", "Logistics Job")
        else 0
    )
    jobs_pending_delivery = (
        frappe.db.count("Logistics Job", filters={**job_filters, "delivery_status": "pending"})
        if frappe.db.exists("DocType", "Logistics Job")
        else 0
    )

    recent_jobs = []
    if frappe.db.exists("DocType", "Logistics Job"):
        recent_jobs = frappe.get_all(
            "Logistics Job",
            filters=job_filters,
            fields=[
                "name",
                "cargo_reference",
                "customer",
                "supplier",
                "order_status",
                "payment_status",
                "delivery_status",
                "total_sell_amount",
                "total_buy_amount",
                "total_margin",
                "modified",
            ],
            order_by="modified desc",
            limit=8,
        )

    return {
        "company": company or "",
        "kpis": {
            "jobs_total": jobs_total,
            "jobs_payment": jobs_payment,
            "jobs_pending_delivery": jobs_pending_delivery,
        },
        "recent_jobs": recent_jobs,
    }
