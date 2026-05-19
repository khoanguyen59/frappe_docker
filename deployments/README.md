# Deployments

This folder provides deployment assets for:

- Linux servers with Docker Compose
- Windows servers with Docker Compose
- Kubernetes clusters (cloud or on-prem)

## Structure

- `linux/`: Compose + script for Linux hosts
- `windows/`: Compose + PowerShell deployment script for Windows hosts
- `k8s/`: Kubernetes manifests with Kustomize overlay

## Important

- These are starter templates. Set strong passwords and hostnames before production use.
- For Kubernetes, your storage class should support `ReadWriteMany` for shared `sites` and `logs` PVCs.
