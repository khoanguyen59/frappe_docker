# Kubernetes Deployment

This deployment uses Kustomize with a base + `prod` overlay.

## Quick start

1. Create namespace and secret:
   - `kubectl create namespace frappe`
   - `kubectl -n frappe create secret generic frappe-secrets --from-literal=mysql-root-password='...' --from-literal=admin-password='...'`
2. Apply manifests:
   - `kubectl apply -k deployments/k8s/overlays/prod`
3. Check rollout:
   - `kubectl -n frappe get pods`

## Notes

- Set ingress host in `overlays/prod/ingress-patch.yaml`.
- `sites` and `logs` PVCs request `ReadWriteMany`. Use a storage class that supports RWX.
