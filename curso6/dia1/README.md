# Día 1 — Gobernanza, métricas y dashboards (4 h)

Paquete autónomo: no depende del Día 2.

## Para estudiantes (seguir en clase)

**→ Empezá por [`SESION_01.md`](SESION_01.md)**  
Instalación, bloques, comandos, Reto 1 clic a clic, errores comunes.

## Para el instructor

| Archivo | Uso |
|---------|-----|
| [instructor_guide.md](instructor_guide.md) | Guion oral (virtual) |
| [ppt_contenido.md](ppt_contenido.md) | Contenido de diapositivas |
| [dia1.pptx](dia1.pptx) | Presentación PowerPoint |
| [proyectos/qa-governance-dashboard/](proyectos/qa-governance-dashboard/) | Lab Reto 1 |

## Arranque rápido del lab

```bash
cd proyectos/qa-governance-dashboard
python scripts/generate_history.py
docker compose up -d --build
```

- Grafana: http://localhost:3000 (admin / admin)  
- Alertas: http://localhost:9090/alerts  
- Graph: http://localhost:9090/graph?g0.expr=qa_flake_rate&g0.range_input=3d&g0.tab=0  
