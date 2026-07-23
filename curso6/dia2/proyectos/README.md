# Proyectos — Día 2

## ml-data-quality-lab (Reto 2)

Testing de datos ETL + modelo ML (Great Expectations, precisión/sesgo/drift, MLflow, CI).

### Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

**macOS**

```bash
brew install uv
```

**Windows (PowerShell)**

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### Arranque

```bash
cd ml-data-quality-lab
uv sync
uv run pytest -v
uv run python -m src.run_pipeline
```

Esperado: **5 passed**.

Más detalle: [ml-data-quality-lab/README.md](ml-data-quality-lab/README.md)
