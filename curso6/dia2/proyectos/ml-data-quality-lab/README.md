# Reto 2 — Testing de datos ETL y modelo ML

Valida integridad del pipeline ETL (nulos, duplicados, formatos) con patrón **Great Expectations**, evalúa **precisión / sesgo (proxy) / drift** del modelo y registra métricas en **MLflow**. Incluye workflow de CI de ejemplo.

## Requisitos

- Python 3.11+ 
- [uv](https://docs.astral.sh/uv/) (recomendado) o `pip`

### macOS

```bash
brew install uv   # o el instalador oficial de Astral
```

### Windows (PowerShell)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

## Ejecutar

Desde esta carpeta:

```bash
uv sync
uv run pytest -v
uv run python -m src.run_pipeline
```

Script (macOS/Linux/Git Bash):

```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

## Qué valida

| Capa | Chequeos |
|------|----------|
| ETL | nulos, duplicados `customer_id`, regiones permitidas, rangos age/income, formato email |
| ML | precisión ≥ 0.70, gap de fairness por región ≤ 0.25, PSI de drift en income ≤ 0.25 |
| Tracking | MLflow con SQLite en `./mlruns/mlflow.db` |

Dataset sucio de demo: `uv run python -c "from src.generate_data import build_current_with_issues; print(build_current_with_issues().head())"`

## CI

Ver `.github/workflows/quality.yml` — ejecuta `pytest` + pipeline completo.

## Notas multiplataforma

- Rutas relativas / `Path`; variable opcional `DATA_DIR` para redirigir datos.
- Sin paths absolutos de Windows.
- `mlruns/` se crea localmente (añádelo a `.gitignore` si versionas el lab).
