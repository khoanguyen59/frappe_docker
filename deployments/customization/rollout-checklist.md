# Rollout Checklist

- Define per-company UI policy (modules, workspaces, doctypes, homepage).
- Configure Role and User Permission first.
- Implement custom app boot hook + desk JS.
- Add app to image build (`development/apps-org-ui-example.json`).
- Deploy to staging, verify each company user account.
- Ensure hidden UI elements are still blocked by permission rules.
- Promote to production with backup and rollback plan.
