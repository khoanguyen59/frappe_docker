# Organization UI Customization for Frappe

This guide helps you safely show/hide Desk UI elements per organization/company.

## Best practice (recommended order)

1. **Permissions first**
   - Use Role + User Permission + Role Profile to control true access.
   - UI hiding should never be the only security layer.

2. **Workspace and Dashboard customization**
   - Create separate Workspaces and Role-bound items for each business context.
   - This reduces the need for fragile DOM-based hide/show scripts.

3. **Custom app for per-company UI profile**
   - Add a custom app with a boot hook.
   - Resolve current user's company and load a UI profile.
   - Apply profile in Desk JS (hide modules/workspaces/actions).

4. **Separate site for hard isolation**
   - If companies are operationally independent, use one site per company.
   - This gives cleaner branding, workflow, and permission boundaries.

## Files in this folder

- `org_ui_profile.example.json`: example UI profile schema per company.
- `org_ui_control/hooks.py.example`: app hook to inject profile into boot info.
- `org_ui_control/boot.py.example`: server-side profile resolver.
- `org_ui_control/public/js/desk_ui.js.example`: client-side UI toggle example.
- `rollout-checklist.md`: practical rollout steps.
- `build-custom-image.md`: image build example using apps JSON.

## Docker repo integration

Use `development/apps-org-ui-example.json` as your app list template when building a custom image.

High-level flow:

1. Create your custom app repository.
2. Put app git URL in `development/apps-org-ui-example.json`.
3. Build custom image with `images/custom/Containerfile` using `apps.json` secret.
4. Use that image in your deployment Compose/K8s manifests.

## Included app blueprint in this repo

You now have a complete starter app at:

- `custom_apps/org_logistics_control`

It includes:

- `Org UI Profile` for per-company UI visibility
- `Logistics Item` for transported goods
- `Logistics Item Document` for goods paperwork
- `Vessel` and `Shipment Tracking` for ship tracking workflow
