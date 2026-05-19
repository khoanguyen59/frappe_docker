# Venucopy

Custom Frappe app for:

- per-company Desk UI visibility control
- logistics items (`Logistics Item`)
- item documents (`Logistics Item Document`)
- vessels (`Vessel`)
- shipment/vessel tracking (`Shipment Tracking`)
- Venulog-inspired logistics lifecycle (`Logistics Job`)

## Business mapping

- `cac mat hang logistics van chuyen` -> `Logistics Item`
- `giay to cho cac mat hang` -> `Logistics Item Document`
- `tau thuyen va tracking` -> `Vessel` + `Shipment Tracking`
- selling + buying + accounting flow -> `Logistics Job`

## Logistics Job flow

`Logistics Job` follows a Venulog-style lifecycle:

- order statuses: `draft -> packaging -> summary -> payment -> completed`
- delivery status and payment status fields compatible with the Venulog naming style
- line-level buy/sell rates with automatic margin computation
- on submit: auto-create `Sales Order` and `Purchase Order`
- action button: create linked `Sales Invoice` and `Purchase Invoice`

## Install (inside bench)

```bash
bench get-app org_logistics_control <your-git-url>
bench --site <site-name> install-app org_logistics_control
bench --site <site-name> migrate
```

## Permissions

- Default access is for `System Manager`.
- Add role permissions for operational users after validating your process.

## Organization-specific theming

- Preferred: manage theme tokens in DocType `Org Theme Profile` (one row per company).
- Fallback defaults still exist in `org_logistics_control/themes.py`.
- Best practice:
  - Keep a small token set (colors, radius, font), not raw CSS per company.
  - Use one shared component style, only swap tokens.
  - Store brand assets (logo/favicons) via Website Settings/Branding, not JS.
  - Keep role permissions separate from theme logic.

## Organization policy layer

Use these DocTypes to assign policy by company:

- `Organization Profile`: binds `Company` to `Role Profile`, `Module Profile`, `Org UI Profile`, and `Org Theme Profile`.
- `Organization User Assignment`: binds a `User` to an `Organization Profile` and controls policy enforcement.

When a user opens Desk, the app resolves active organization policy and can enforce role/module profile automatically.
