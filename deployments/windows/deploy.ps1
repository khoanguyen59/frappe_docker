$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example. Update credentials before production use."
}

docker compose -f docker-compose.host.yml --env-file .env up -d --remove-orphans
docker compose -f docker-compose.host.yml --env-file .env ps
