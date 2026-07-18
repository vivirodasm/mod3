# Proyectos — Día 1

## qa-governance-dashboard (Reto 1)

Dashboard de gobernanza QA con Prometheus + Grafana.

### Requisitos

- Docker Desktop (Windows o macOS), estado **Running**
- Puertos libres: **8000**, **9090**, **3000** (evita el 5000 en Mac/AirPlay)

### Arranque

```bash
cd qa-governance-dashboard
python scripts/generate_history.py   # histórico ~3 días (primera vez / tras down -v)
docker compose up -d --build
```

### Validación

```bash
# macOS / Linux / Git Bash
curl -sf http://127.0.0.1:8000/
curl -sf http://127.0.0.1:8000/metrics | head
curl -sf http://127.0.0.1:9090/-/ready

# Windows PowerShell
curl.exe -sf http://127.0.0.1:8000/
curl.exe -sf http://127.0.0.1:9090/-/ready
```

UI: http://localhost:3000 → **QA Governance Dashboard** (admin / admin)

Detener: `docker compose down`

Más detalle: [qa-governance-dashboard/README.md](qa-governance-dashboard/README.md)
