import frappe


def get_context(context):
    context.no_cache = 1
    context.title = "Venucopy"

    if frappe.session.user == "Guest":
        context.is_guest = True
        return context

    context.is_guest = False
    context.user = frappe.session.user
    context.company = (
        frappe.defaults.get_user_default("company")
        or frappe.defaults.get_user_default("Company")
        or frappe.db.get_single_value("Global Defaults", "default_company")
    )
    return context
