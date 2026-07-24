# Smoke K6 contra target local (Windows PowerShell)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
docker compose up -d target
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
docker compose run --rm k6-smoke
exit $LASTEXITCODE
