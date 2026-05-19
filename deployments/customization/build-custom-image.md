# Build Custom Image with Org UI App

Example build command (from repository root):

```bash
docker build \
  --file images/custom/Containerfile \
  --target backend \
  --build-arg FRAPPE_BRANCH=version-16 \
  --secret id=apps_json,src=development/apps-org-ui-example.json \
  --tag your-registry/frappe-erpnext-org-ui:v16 \
  .
```

Then set your deployment image:

- Linux/Windows Compose: `FRAPPE_IMAGE=your-registry/frappe-erpnext-org-ui:v16`
- Kubernetes: update image in `deployments/k8s/base/*.yaml`
