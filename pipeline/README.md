# Pipeline Templates

This folder contains CI/CD pipeline templates you can adapt for your environment.

- `github-actions/deploy-linux.yml`: deploys Docker Compose stack to a Linux host over SSH.
- `github-actions/deploy-windows.yml`: deploys Docker Compose stack to a Windows host over SSH.
- `github-actions/deploy-k8s.yml`: deploys Kubernetes manifests to any cloud/on-prem cluster.

## How to use

1. Copy a template into `.github/workflows/`.
2. Add repository secrets required by the template.
3. Trigger the workflow from GitHub Actions (`workflow_dispatch`) or add branch triggers.

## Common prerequisites

- Remote server has Docker + Docker Compose plugin installed.
- Kubernetes target has `kubectl` access and a working ingress controller.
- Update paths, host names, and secret names to match your infra.
