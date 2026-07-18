# Certificación 6 — Madurez, Gobernanza y Estrategia de Calidad

Curso de **8 horas** en **2 días independientes**. Cada día tiene su propia guía, PPT y proyectos.

```
curso6/
  dia1/          ← 4 h autónomas (gobernanza, métricas, dashboards, Reto 1)
  dia2/          ← 4 h autónomas (IA/datos, RPA, TMMi, Reto 2)
  scripts/       ← utilidades (generar PPTX)
```

| Día | Carpeta | Guía del estudiante | Lab |
|-----|---------|---------------------|-----|
| 1 | [dia1/](dia1/) | **[SESION_01.md](dia1/SESION_01.md)** | `proyectos/qa-governance-dashboard` |
| 2 | [dia2/](dia2/) | **[SESION_02.md](dia2/SESION_02.md)** | `proyectos/ml-data-quality-lab` |

Los archivos `SESION_0X.md` son lo que siguen los estudiantes (instalación, pasos, retos, errores comunes), al estilo de `sesiones/sesion-02/SESION_02.md`.

## Regenerar presentaciones

```bash
pip install python-pptx
python curso6/scripts/build_pptx.py          # ambas
python curso6/scripts/build_pptx.py dia1     # solo día 1
python curso6/scripts/build_pptx.py dia2     # solo día 2
```
