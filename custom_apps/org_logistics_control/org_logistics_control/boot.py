import frappe
from org_logistics_control.themes import DEFAULT_THEME, get_theme_for_company


def load_org_ui_profile(bootinfo):
    if frappe.session.user == "Guest":
        bootinfo.org_ui_profile = {}
        return

    companies = _resolve_companies()
    org_policy = _resolve_org_policy(companies)
    _enforce_org_access_policy(org_policy)

    if not companies:
        bootinfo.org_ui_profile = {}
        return

    ui_profile_name = org_policy.get("ui_profile") if org_policy else None
    theme_profile_name = org_policy.get("theme_profile") if org_policy else None

    row = None
    if ui_profile_name:
        row = frappe.db.get_value(
            "Org UI Profile",
            ui_profile_name,
            ["company", "hide_modules", "hide_workspaces", "hide_doctypes", "homepage"],
            as_dict=True,
        )
    else:
        for company in companies:
            row = frappe.db.get_value(
                "Org UI Profile",
                {"company": company, "enabled": 1},
                ["company", "hide_modules", "hide_workspaces", "hide_doctypes", "homepage"],
                as_dict=True,
            )
            if row:
                break

    if not row:
        bootinfo.org_ui_profile = {}
        return

    bootinfo.org_ui_profile = {
        "company": row.company,
        "hide_modules": _to_list(row.hide_modules),
        "hide_workspaces": _to_list(row.hide_workspaces),
        "hide_doctypes": _to_list(row.hide_doctypes),
        "homepage": row.homepage or "",
    }
    bootinfo.org_context = {
        "organization_profile": org_policy.get("name") if org_policy else "",
        "company": org_policy.get("company") if org_policy else row.company,
        "role_profile": org_policy.get("role_profile") if org_policy else "",
        "module_profile": org_policy.get("module_profile") if org_policy else "",
    }

    bootinfo.org_ui_theme = get_theme_for_company(row.company)
    db_theme = _get_theme_from_db(row.company, theme_profile_name)
    if db_theme:
        bootinfo.org_ui_theme = db_theme


def _to_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return value
    return [item.strip() for item in str(value).split(",") if item.strip()]


def _resolve_companies():
    user_company = frappe.defaults.get_user_default("Company")
    user_company_lower = frappe.defaults.get_user_default("company")
    global_company = frappe.db.get_single_value("Global Defaults", "default_company")
    permitted_companies = _get_permitted_companies()

    candidates = []
    for company in [user_company, user_company_lower, global_company, *permitted_companies]:
        if not company:
            continue
        candidates.append(company)
        base = company.split("(")[0].strip()
        if base and base != company:
            candidates.append(base)

    seen = set()
    ordered = []
    for company in candidates:
        if company not in seen:
            ordered.append(company)
            seen.add(company)
    return ordered


def _get_permitted_companies():
    if frappe.session.user == "Guest":
        return []

    rows = frappe.get_all(
        "User Permission",
        filters={"user": frappe.session.user, "allow": "Company"},
        fields=["for_value", "is_default"],
        order_by="is_default desc, creation asc",
    )
    return [row.for_value for row in rows if row.for_value]


def _resolve_org_policy(companies):
    if not frappe.db.exists("DocType", "Organization Profile"):
        return {}

    assignment = _get_user_assignment(companies)
    if assignment:
        return assignment

    if not companies:
        return {}

    rows = frappe.get_all(
        "Organization Profile",
        filters={"enabled": 1, "company": ["in", companies]},
        fields=[
            "name",
            "company",
            "role_profile",
            "module_profile",
            "ui_profile",
            "theme_profile",
            "force_policy",
            "priority",
        ],
        order_by="priority asc, creation asc",
    )
    return rows[0] if rows else {}


def _get_user_assignment(companies):
    if not frappe.db.exists("DocType", "Organization User Assignment"):
        return {}

    assignment_rows = frappe.get_all(
        "Organization User Assignment",
        filters={"user": frappe.session.user, "enabled": 1},
        fields=["organization_profile", "as_default", "enforce_policy"],
        order_by="as_default desc, creation asc",
    )
    if not assignment_rows:
        return {}

    org_names = [row.organization_profile for row in assignment_rows if row.organization_profile]
    if not org_names:
        return {}

    org_rows = frappe.get_all(
        "Organization Profile",
        filters={"name": ["in", org_names], "enabled": 1},
        fields=[
            "name",
            "company",
            "role_profile",
            "module_profile",
            "ui_profile",
            "theme_profile",
            "force_policy",
            "priority",
        ],
    )
    by_name = {row.name: row for row in org_rows}

    for assignment in assignment_rows:
        org = by_name.get(assignment.organization_profile)
        if not org:
            continue
        if companies and org.company not in companies:
            continue
        org.enforce_policy = assignment.enforce_policy if assignment.enforce_policy is not None else org.force_policy
        return org

    return {}


def _enforce_org_access_policy(org_policy):
    if not org_policy:
        return

    if not org_policy.get("enforce_policy") and not org_policy.get("force_policy"):
        return

    user = frappe.session.user
    updates = {}

    role_profile = org_policy.get("role_profile")
    module_profile = org_policy.get("module_profile")

    if role_profile and frappe.db.get_value("User", user, "role_profile_name") != role_profile:
        updates["role_profile_name"] = role_profile
    if module_profile and frappe.db.get_value("User", user, "module_profile") != module_profile:
        updates["module_profile"] = module_profile

    if updates:
        frappe.db.set_value("User", user, updates, update_modified=False)


def _get_theme_from_db(company, theme_profile_name=None):
    if theme_profile_name:
        row = frappe.db.get_value(
            "Org Theme Profile",
            theme_profile_name,
            [
                "theme_name",
                "font_family",
                "color_bg",
                "color_surface",
                "color_text",
                "color_muted",
                "color_primary",
                "color_primary_contrast",
                "color_accent",
                "radius",
            ],
            as_dict=True,
        )
        if row:
            return _merge_theme_row(row)

    candidates = []
    if company:
        candidates.append(company)
        base = company.split("(")[0].strip()
        if base and base != company:
            candidates.append(base)

    fields = [
        "theme_name",
        "font_family",
        "color_bg",
        "color_surface",
        "color_text",
        "color_muted",
        "color_primary",
        "color_primary_contrast",
        "color_accent",
        "radius",
    ]

    row = None
    for c in candidates:
        row = frappe.db.get_value(
            "Org Theme Profile", {"company": c, "enabled": 1}, fields, as_dict=True
        )
        if row:
            break

    if not row:
        fallback = get_theme_for_company(company)
        return dict(fallback) if fallback else dict(DEFAULT_THEME)

    return _merge_theme_row(row)


def _merge_theme_row(row):
    if not row:
        return dict(DEFAULT_THEME)

    theme = dict(DEFAULT_THEME)
    theme.update(
        {
            "name": row.get("theme_name") or "db-theme",
            "font_family": row.get("font_family") or DEFAULT_THEME["font_family"],
            "color_bg": row.get("color_bg") or DEFAULT_THEME["color_bg"],
            "color_surface": row.get("color_surface") or DEFAULT_THEME["color_surface"],
            "color_text": row.get("color_text") or DEFAULT_THEME["color_text"],
            "color_muted": row.get("color_muted") or DEFAULT_THEME["color_muted"],
            "color_primary": row.get("color_primary") or DEFAULT_THEME["color_primary"],
            "color_primary_contrast": row.get("color_primary_contrast")
            or DEFAULT_THEME["color_primary_contrast"],
            "color_accent": row.get("color_accent") or DEFAULT_THEME["color_accent"],
            "radius": row.get("radius") or DEFAULT_THEME["radius"],
        }
    )
    return theme
