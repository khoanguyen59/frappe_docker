import frappe


@frappe.whitelist()
def set_default_company(company):
    if frappe.session.user == "Guest":
        frappe.throw("Login required")

    allowed = {
        row.get("doc")
        for row in (frappe.defaults.get_user_permissions().get("Company") or [])
        if row.get("doc")
    }

    if allowed and company not in allowed:
        frappe.throw("Company is not allowed for this user")

    frappe.defaults.set_user_default("company", company, frappe.session.user)
    frappe.defaults.set_user_default("Company", company, frappe.session.user)
    frappe.db.commit()
    return {"ok": True, "company": company}


@frappe.whitelist()
def get_allowed_companies():
    if frappe.session.user == "Guest":
        return {"companies": [], "default_company": ""}

    perms = frappe.defaults.get_user_permissions().get("Company") or []
    companies = [row.get("doc") for row in perms if row.get("doc")]

    if not companies:
        companies = [d.name for d in frappe.get_all("Company", fields=["name"], limit=50)]

    default_company = (
        frappe.defaults.get_user_default("company")
        or frappe.defaults.get_user_default("Company")
        or (companies[0] if companies else "")
    )

    return {"companies": companies, "default_company": default_company}
