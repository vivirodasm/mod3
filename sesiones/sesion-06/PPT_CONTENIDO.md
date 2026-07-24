# Sesión 6 — Contenido de diapositivas
## Performance con K6 (cierre del Reto 1)

> 20 slides · Bloque A: 1–7 (45 min) · Bloque B: 8–14 (45 min) · Bloque C: 15–20 (45 min)  
> Cada slide: **1 idea + demo o ejemplo**. Datos de demos verificados contra el target local.

---

### Slide 1 — Portada (2 min)
**Título:** Performance con K6 — ¿el sistema aguanta?
- Sesión 6 de 10 · Curso QA Automation
- De "¿devuelve lo correcto?" a "¿lo hace rápido y estable bajo carga?"
- SUT: target local (nginx) en Docker — sin depender de internet
- **Cierre Reto 1:** API (S3/S4) + CI (S5) + performance (hoy)

### Slide 2 — ¿Dónde estamos? (4 min)
- S3/S4 ✅ La API **responde lo correcto**
- S5 ✅ CI corre esos tests **solo**, en cada push
- S6 → La pregunta que falta: **¿aguanta bajo carga?**
- Una API correcta que tarda 3 s con 100 usuarios está, en la práctica, caída

### Slide 3 — Funcional vs performance (5 min)
**Título:** Dos preguntas distintas sobre el mismo endpoint

| Tipo | Pregunta | Cómo falla |
|---|---|---|
| **Funcional** | ¿Resultado **correcto**? | `assert` / check |
| **Performance** | ¿Rápido y estable bajo carga? | **threshold** roto |

- Ejemplo: `GET /checkout` OK… en 3.4 s con 200 usuarios → nadie compra
- Performance **complementa**; no reemplaza

### Slide 4 — Vocabulario del día (6 min)
**Título:** Los términos que vas a leer en cada reporte

| Término | Significado |
|---|---|
| **VU** | Usuario virtual |
| **p95** | Cola lenta (no el promedio) |
| **Check** | Assert por request — **no** cambia el exit code solo |
| **Threshold** | Criterio global → si se rompe, exit **99** |
| **Think time** | `sleep` entre requests (humano real) |

- **Distinción del día:** CI escucha el **threshold**, no el check
- Mapa rápido: smoke / load (hoy) · stress / spike (concepto)

### Slide 5 — K6: performance como código (7 min)
**Título:** El script vive en Git y corre en Docker

```javascript
export const options = {
  vus: 2, duration: "15s",
  thresholds: { http_req_duration: ["p(95)<500"] },  // gate
};
export default function () {
  const r = http.get(`${BASE_URL}/api/health`);
  check(r, { "status 200": (res) => res.status === 200 }); // assert
  sleep(0.5); // think time
}
```

- JS en PR · imagen `grafana/k6:1.8.0` · **no instalas K6**
- Mercado: **K6** (nuestra ruta) · JMeter · Gatling · Locust — mismo patrón
- Escala (concepto): Grafana Cloud k6 = mismo script, miles de VUs

### Slide 6 — El target local (6 min)
**Título:** Qué vamos a golpear hoy

- `GET /api/health` → `{"status":"ok"}` · `GET /api/product` → producto con `title`
- K6 pega a `http://target:8080` (red Docker), **no** `localhost`
- Compose espera `healthy` antes de lanzar K6
- Camino feliz reproducible sin internet

### Slide 7 — DEMO: smoke en verde (10 min)
**Título:** Primera corrida — ¿enciende?

```bash
docker compose up -d target
docker compose run --rm k6-smoke
```

- **Predicción antes de Enter:** ¿exit 0 o ≠ 0?
- **Resultado real:** `✓ p(95)<500` (~49 ms) · checks 100% · **exit 0**
- Abre `smoke.js`: `options` + `default function` + `sleep`
- Café → load con etapas

---
**☕ DESCANSO 15 MIN**
---

### Slide 8 — Arranque B (1 min)
**Título:** De "enciende" a "aguanta"
- Smoke = ¿responde? · Load = ¿aguanta con etapas?

### Slide 9 — Load con ramping-vus (6 min)
**Título:** Sube, mantiene, baja

```javascript
scenarios: {
  average_load: {
    executor: "ramping-vus",
    stages: [
      { duration: "10s", target: 5 },
      { duration: "20s", target: 10 },
      { duration: "10s", target: 0 },
    ],
  },
},
thresholds: { http_req_duration: ["p(95)<800"] }, // más holgado que smoke
```

- Misma historia que smoke: health + product + think time
- Estilo moderno k6 1.x: `scenarios` + `ramping-vus`

### Slide 10 — DEMO: load en verde (10 min)
**Título:** ~10 VUs, ~40 s, ¿sigue rápido?

```bash
docker compose run --rm k6-load
```

- **Resultado real:** `✓ p(95)<800` · checks 100% · vus_max 10 · **exit 0**
- Contra un backend real los ms suben → el número del umbral es decisión de negocio

### Slide 11 — Cómo leer el reporte (6 min)
**Título:** El resumen es largo — mira solo 4 líneas

1. `http_req_duration` → **p95**
2. `http_req_failed` → % de error
3. `checks` → % de validaciones
4. `✓` / `✗` del **threshold** → **el veredicto**

- Si no sabes leer estas 4, el rojo de CI es superstición

### Slide 12 — DEMO: fallo a propósito (8 min)
**Título:** El aha — checks verdes, gate rojo

```javascript
thresholds: { http_req_duration: ["p(95)<1"] }  // imposible
```

```
checks_succeeded: 100% (98/98)     ← todos verdes
✗ 'p(95)<1' p(95)≈14ms             ← threshold roto → exit 99
```

- **El check no mueve el gate; el threshold sí**
- En un pipeline: exit 99 = **"no" al merge**

### Slide 13 — K6 en CI + cómo elegir el número (5 min)
**Título:** Mismo criterio que la S5 + baseline

- Smoke en PR (rápido) · load en `main` / noche (concepto)
- Plantilla: `performance/workflows/qa-perf.yml`
- Regla: baseline real + **buffer 20–30%** = umbral de gate
- Hoy el criterio es el **exit code**, igual que pytest

### Slide 14 — Logro del bloque (2 min)
- Corriste smoke y load en verde · provocaste exit 99
- Entendiste **check ≠ threshold**
- Tras el café: **tú** endureces el umbral

---
**☕ DESCANSO 15 MIN**
---

### Slide 15 — Arranque C (1 min)
**Título:** Mini-reto y cierre del Reto 1

### Slide 16 — Mini-reto: endurece un threshold (12 min)
1. En `load.js`: `p(95)<800` → `p(95)<5`
2. `docker compose run --rm k6-load` → **rojo** (exit 99)
3. **Revierte** a `<800`

- Subir/bajar ese número = decisión de negocio, no magia

### Slide 17 — p95 vs promedio (4 min)
| Métrica | Qué esconde |
|---|---|
| **Promedio** | Un pico de 5 s se diluye → engaña |
| **p95 / p99** | Cola lenta = usuario desafortunado |

- SLO/SLA se escriben con percentiles: "p95 < 300 ms"
- Mide la cola, no el centro

### Slide 18 — Herramientas del mercado (4 min)
| Herramienta | Nota |
|---|---|
| **K6** | JS + CI — **nuestra ruta** |
| JMeter | GUI · legados |
| Gatling | JVM · reportes ricos |
| Locust | Python |

- Grafana Cloud k6: mismo script, miles de VUs

### Slide 19 — Reto 1 cerrado + checklist (6 min)
- API (S3/S4) + CI (S5) + **umbrales K6** (hoy)
- Checklist:
  - [ ] Funcional ≠ performance
  - [ ] Check ≠ threshold
  - [ ] Smoke + load en verde
  - [ ] Vi exit 99 a propósito
  - [ ] Sé elegir umbral (baseline + buffer)

### Slide 20 — Errores + frase de cierre (3 min)
- 8080 ocupado · `target` vs `localhost` · pull lento de k6 · no revertir el mini-reto
- Completa: *"Un threshold sirve para ___."*
- **S7:** Seguridad — el mismo criterio automático, ahora contra vulnerabilidades
