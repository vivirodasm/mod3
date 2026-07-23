# CI Lab — Sesión 5

Replica en **Docker** (y en GitHub Actions) la misma suite de [api-lab](../api-lab/) de la Sesión 4.

## Requisitos

- Docker Desktop **Running**
- (Opcional) `uv` para comparar local vs Docker

## Arranque rápido (ruta única)

```bash
cd proyecto-integrador/ci-lab
docker compose build test
docker compose run --rm --no-deps test
```

**Esperado:** `17 passed` (misma suite que api-lab).

Scripts opcionales: `scripts/run_local.ps1` / `run_local.sh`.

## Comparar local vs CI (opcional)

```bash
cd ../api-lab
uv sync --group dev
uv run pytest -v
```

**Regla de oro:** el comando de CI debe ser el mismo que confías en local.

## Workflow de GitHub Actions (patrones 2026)

- Real: [`.github/workflows/qa-api.yml`](../../.github/workflows/qa-api.yml)
- Copia didáctica: [`workflows/qa-api.yml`](workflows/qa-api.yml)

Mirar en clase: `on` · `permissions` · `concurrency` · `jobs` / `steps` · caché `uv` · filtro `-k smoke`.

## Plan B si JSONPlaceholder no responde

Seguí con Docker (si ya tenés una imagen/cache) y con la lectura del YAML. El punto de la sesión es el **juez neutral**, no la API pública.
