#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-frappe}"
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD:-}"
FRAPPE_ADMIN_PASSWORD="${FRAPPE_ADMIN_PASSWORD:-}"

if [[ -z "$MYSQL_ROOT_PASSWORD" || -z "$FRAPPE_ADMIN_PASSWORD" ]]; then
  echo "Set MYSQL_ROOT_PASSWORD and FRAPPE_ADMIN_PASSWORD first."
  exit 1
fi

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
kubectl -n "$NAMESPACE" create secret generic frappe-secrets \
  --from-literal=mysql-root-password="$MYSQL_ROOT_PASSWORD" \
  --from-literal=admin-password="$FRAPPE_ADMIN_PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -k overlays/prod
kubectl -n "$NAMESPACE" get pods
