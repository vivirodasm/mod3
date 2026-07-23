# Sesión 6 — Contenido de diapositivas
## Performance con K6 · cierre del Reto 1

> ~20 slides · A: 1–7 · B: 8–14 · C: 15–20
> Regla: **1 idea + 1 demo** · menos tablas, más predicción

---

### Slide 1 — Portada (2 min)
**Título:** Performance con K6
- Sesión 6 · target local + Docker
- Frase: la performance también se verifica automáticamente

### Slide 2 — Al salir vas a poder (2 min)
- Smoke / load / thresholds
- Correr K6 en Docker (imagen **1.8**)
- Provocar un fallo (rojo) a propósito
- Cerrar Reto 1 (concepto): API + CI + umbrales

### Slide 3 — Funcional vs performance (4 min)
- Correcto ≠ usable bajo carga
- Complementa al test funcional; no lo reemplaza

### Slide 4 — Vocabulario corto (6 min)
- VU · p95 · error rate
- **Check** ≠ **threshold** (el pipeline escucha el threshold)
- Smoke / load
- Pausa 20 s: ¿son lo mismo check y threshold?

### Slide 5 — K6 como código 2026 (4 min)
- JS en Git · corre en CI
- `scenarios` + `ramping-vus`
- Imagen `grafana/k6:1.8.0`
- Escala (concepto): Grafana Cloud k6

### Slide 6 — Target local (3 min)
- nginx · `:8080` · `/api/health`
- Sin internet en el camino feliz

### Slide 7 — DEMO smoke (12 min)
```bash
docker compose up -d target
docker compose run --rm k6-smoke
```
- Predicción → Enter → exit 0
- Abre `smoke.js`: options + thresholds + checks
- Tras el café: load

---
**DESCANSO 15 MIN**
---

### Slide 8 — Arranque B (1 min)
**Título:** Load + el fallo (rojo)

### Slide 9 — Stages / ramping-vus (5 min)
- Subir → mantener → bajar
- Archivo: `load.js` · escenario `average_load`

### Slide 10 — DEMO load (10 min)
```bash
docker compose run --rm k6-load
```
- Señala los thresholds en el resumen

### Slide 11 — Cómo leer (sin miedo) (6 min)
- Solo 4 cosas: duration · failed · checks · ✓/✗ thresholds
- Si no sabes leerlo, no vas a saber por qué CI se puso rojo

### Slide 12 — DEMO del fallo (rojo) (8 min)
```bash
docker compose run --rm k6-fail
```
- p95 < 1ms → imposible → exit ≠ 0 (99)
- "Así se bloquea un merge"

### Slide 13 — K6 en el pipeline (4 min)
- Smoke/pytest en PR · load más pesado de noche / en main
- Mismo criterio: código de salida (S5)

### Slide 14 — Logro del bloque (2 min)
- Ya viste verde y rojo de performance
- Tras el café: endureces el umbral

---
**DESCANSO 15 MIN**
---

### Slide 15 — Arranque C (1 min)
**Título:** Mini-reto y cierre Reto 1

### Slide 16 — Mini-reto (12 min)
- `p(95)<800` → `<5` · correr · ver rojo · **revertir**

### Slide 17 — JMeter / Gatling (3 min)
- Herramientas del mercado · patrón igual
- K6 = nuestra ruta, integrada con CI

### Slide 18 — Reto 1 cerrado (6 min)
- API automatizada + CI + K6 thresholds
- Piezas S3–S6

### Slide 19 — Checklist + frase de cierre (6 min)
- Checklist del SESION_06
- Completa: "Un threshold sirve para ___."

### Slide 20 — Gracias
- `proyecto-integrador/performance/`
- Próxima: Seguridad (S7)
