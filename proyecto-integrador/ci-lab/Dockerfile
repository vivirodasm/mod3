# Sesión 5 — imagen CI que corre la suite de api-lab (S4)
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /usr/local/bin/uv

WORKDIR /app

COPY api-lab/pyproject.toml api-lab/uv.lock ./
COPY api-lab/client ./client
COPY api-lab/conftest.py ./
COPY api-lab/data ./data
COPY api-lab/tests ./tests

RUN uv sync --group dev --frozen

CMD ["uv", "run", "pytest", "-v"]
