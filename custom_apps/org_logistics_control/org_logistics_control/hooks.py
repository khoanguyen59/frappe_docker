app_name = "org_logistics_control"
app_title = "Venucopy"
app_publisher = "Your Team"
app_description = "Venucopy logistics operations with selling, buying, and accounting flow"
app_email = "admin@example.com"
app_license = "MIT"

boot_session = "org_logistics_control.boot.load_org_ui_profile"
app_include_js = ["/assets/org_logistics_control/js/desk_ui.js"]

website_redirects = [
    {"source": "/Selling", "target": "/app"},
    {"source": "/selling", "target": "/app"},
    {"source": "/desk", "target": "/app"},
]
