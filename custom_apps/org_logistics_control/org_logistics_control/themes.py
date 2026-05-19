DEFAULT_THEME = {
    "name": "venulog-base",
    "font_family": "'Satoshi', 'Manrope', 'Segoe UI', sans-serif",
    "color_bg": "#f8f9ff",
    "color_surface": "#ffffff",
    "color_text": "#111827",
    "color_muted": "#6b7280",
    "color_primary": "#5055a5",
    "color_primary_contrast": "#ffffff",
    "color_accent": "#6c63ff",
    "radius": "12px",
}


ORG_THEME_MAP = {
    "NetKhoa": {
        "name": "netkhoa",
        "font_family": "'Manrope', 'Segoe UI', sans-serif",
        "color_bg": "#f4f7fb",
        "color_surface": "#ffffff",
        "color_text": "#102a43",
        "color_muted": "#627d98",
        "color_primary": "#0ea5a5",
        "color_primary_contrast": "#ffffff",
        "color_accent": "#f97316",
        "radius": "12px",
    }
}


def get_theme_for_company(company):
    company_key = (company or "").split("(")[0].strip()
    theme = ORG_THEME_MAP.get(company_key) or ORG_THEME_MAP.get(company)
    if not theme:
        return DEFAULT_THEME
    merged = dict(DEFAULT_THEME)
    merged.update(theme)
    return merged
