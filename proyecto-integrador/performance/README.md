# Performance Lab — Sesión 6 (K6)

Pruebas de performance con **K6 en Docker** (`grafana/k6:1.8.0`) contra un **target local** (nginx). No hace falta instalar K6 ni depender de internet en el happy path.

## Requisitos

- Docker Desktop **Running**
- Puerto **8080** libre

## Arranque rápido

```bash
cd proyecto-integrador/performance
docker compose up -d target
curl http://127.0.0.1:8080/api/health   # Windows: curl.exe

docker compose run --rm k6-smoke   # exit 0
docker compose run --rm k6-load    # exit 0
docker compose run --rm k6-fail    # demo ROJO (exit 99)
docker compose down
```

Atajos desde `curso/`: `task test:perf:smoke` · `task test:perf:load`.  
Scripts opcionales: `scripts/run_smoke.ps1` / `.sh` y `run_load.ps1` / `.sh`.

## Archivos K6

| Script | Uso |
|--------|-----|
| `k6/smoke.js` | Pocos VUs — “¿enciende?” (health + product + think time) |
| `k6/load.js` | `scenarios` + `ramping-vus` + thresholds de gate |
| `k6/fail_demo.js` | Threshold imposible (p95 &lt; 1ms) → exit 99 |

**Idea clave:** `check` ≠ `threshold`. El gate de CI escucha el exit code del threshold.

## Plantilla CI (lectura en clase)

[`workflows/qa-perf.yml`](workflows/qa-perf.yml) — cómo meter smoke K6 en GitHub Actions (no está activo en `.github/` a propósito; el lab corre en local).

## Puerto

Target: **http://localhost:8080**.
