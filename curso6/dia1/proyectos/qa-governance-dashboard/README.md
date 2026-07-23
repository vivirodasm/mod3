# Reto 1 — Dashboard de gobernanza QA (Prometheus + Grafana)

Visualiza **flake rate**, **defect leakage**, **test effectiveness ratio** y **cobertura por microservicio** con histórico de ~**3 días** y alertas reales por umbrales críticos.

## Requisitos

- Docker Desktop (Windows o macOS) o Docker Engine + Compose v2
- Puertos libres: **8000**, **9090**, **3000** (evitar el 5000 en Mac/AirPlay)
- Python 3 (solo para regenerar el seed histórico, opcional)

## Arranque rápido

Desde esta carpeta:

```bash
# 1) Generar histórico OpenMetrics (~3 días) — obligatorio la primera vez / al recrear volumen
python scripts/generate_history.py

# 2) Levantar stack (seed TSDB + Prometheus + Grafana + exporter)
docker compose up -d --build
```

Si ya tenías un volumen viejo sin histórico:

```bash
docker compose down -v
python scripts/generate_history.py
docker compose up -d --build
```

PowerShell (Windows):

```powershell
python scripts/generate_history.py
docker compose up -d --build
curl.exe http://127.0.0.1:8000/metrics
curl.exe http://127.0.0.1:9090/-/ready
```

## URLs (qué abrir en clase)

| Servicio | URL | Qué ven |
|----------|-----|---------|
| Exporter | http://localhost:8000/metrics | Texto plano con métricas `qa_*` |
| Prometheus Graph | http://localhost:9090/graph?g0.expr=qa_flake_rate&g0.range_input=3d&g0.tab=0 | Serie de 3 días (hay que poner query; sin `expr` queda vacío) |
| Prometheus Alerts | http://localhost:9090/alerts | Alertas **firing** (payments / notifications) |
| Grafana | http://localhost:3000 | Dashboard **QA Governance Dashboard** (rango `now-3d`, panel de alertas) · admin/admin |

## Alertas configuradas

| Alerta | Condición |
|--------|-----------|
| HighFlakeRate | `qa_flake_rate > 0.10` |
| HighDefectLeakage | `qa_defect_leakage > 0.12` |
| LowTestEffectiveness | `qa_test_effectiveness_ratio < 0.85` |
| LowCoverage | `qa_coverage < 70` |

En el lab, **payments** y **notifications** suelen estar en rojo a propósito.

## Detener

```bash
docker compose down        # conserva histórico del volumen
docker compose down -v     # borra histórico (hay que volver a generar seed)
```

## Notas multiplataforma

- Rutas relativas; scripts `#!/usr/bin/env sh` / bash compatibles con macOS.
- Retention Prometheus: **5 días** (`--storage.tsdb.retention.time=5d`).
- El seed solo corre una vez por volumen (marker `.curso6_seeded`).
