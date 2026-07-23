# Replica el job de CI en local con Docker (Windows PowerShell).
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "==> Build imagen CI (api-lab)"
docker compose build test
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Run pytest dentro de Docker"
docker compose run --rm --no-deps test
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "OK — mismo criterio que el workflow de GitHub Actions"
