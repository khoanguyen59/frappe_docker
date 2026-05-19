#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example. Update credentials before production use."
fi

docker compose -f docker-compose.host.yml --env-file .env up -d --remove-orphans
docker compose -f docker-compose.host.yml --env-file .env ps
