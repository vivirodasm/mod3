# Sesión 6 — Performance con K6 (cierre del Reto 1)

> **Objetivo:** al terminar esta sesión vas a poder correr pruebas de **smoke** y **load** con K6 dentro de Docker, leer los **thresholds** de un reporte, provocar a propósito que una verificación de performance falle (rojo) y explicar cómo ese mismo criterio entra en CI.

**SUT (*System Under Test*):** un servidor local (nginx) que expone `/api/health` y `/api/product` en el puerto `8080`. Corre en Docker, así que **no dependes de internet** en el camino feliz.

**Frase del día:** la performance también se verifica automáticamente: no basta con que "funcione", tiene que responder **lo bastante rápido y estable** bajo carga.

**Cierre del Reto 1 (concepto):** hoy juntas las tres piezas de un criterio de release — API automatizada (S3/S4) + CI (S5) + umbrales de performance (K6, hoy).

---

## Antes de empezar

```bash
# 1. Verifica que Docker Desktop está corriendo
docker version

# 2. Entra al laboratorio de performance
cd proyecto-integrador/performance

# 3. Levanta el servidor local (target)
docker compose up -d target

# 4. Comprueba que responde (Windows: curl.exe · Mac/Linux: curl)
curl.exe http://127.0.0.1:8080/api/health
```

**Resultado esperado:** un JSON con `"status": "ok"`. El puerto **8080** debe estar libre.

> **Atajos** desde la raíz de `curso/`: `task test:perf:smoke` y `task test:perf:load`.

---

## Agenda (3 horas)

| Bloque | Duración | Contenido |
|---|---|---|
| **A** | 45 min | Funcional vs performance · vocabulario (VU, p95, check ≠ threshold) · tipos de prueba · primer **smoke** en verde |
| Descanso | 15 min | ☕ |
| **B** | 45 min | **Load** con `ramping-vus` · leer el reporte · provocar un fallo (rojo) · encaje con CI |
| Descanso | 15 min | ☕ |
| **C** | 45 min | Mini-reto: endurecer un threshold · p95 vs promedio · mapa de herramientas · **cierre del Reto 1** |

---

## Bloque A — Fundamentos de performance (45 min)

### 1. Funcional vs performance: dos preguntas distintas

| Tipo de prueba | Pregunta que responde | Cómo falla |
|---|---|---|
| **Funcional** | ¿Devuelve el resultado **correcto**? | `assert` / check en rojo |
| **Performance** | ¿Lo hace lo bastante **rápido y estable** bajo carga? | **threshold** roto (exit ≠ 0) |

Las dos pueden estar en verde y el sistema seguir siendo inusable: un JSON correcto que tarda 3 segundos bajo carga no sirve. La prueba de performance **complementa** a la funcional; no la reemplaza.

Ejemplo mental: `GET /checkout` devuelve el carrito bien… en 3.4 s con 200 usuarios concurrentes → nadie compra. La velocidad es parte del contrato.

### 2. Vocabulario que vas a usar hoy

| Término | Significado |
|---|---|
| **VU** (*Virtual User*) | Usuario virtual: una "persona" simulada haciendo requests |
| **p95** | El 95% de los requests fue más rápido que este valor (el 5% más lento queda por encima) |
| **Error rate** | Porcentaje de requests que fallaron (`http_req_failed`) |
| **Threshold** | Regla de aprobación: si se rompe, K6 termina en **rojo** (código de salida ≠ 0; en la práctica **99**) |
| **Check** | Validación por request (como un `assert`). **No** cambia el código de salida por sí solo |
| **Smoke** | Poca carga: ¿responde lo básico? |
| **Load** | Carga con etapas: subir → mantener → bajar |
| **Think time** | Pausa entre requests (`sleep`) — un humano no dispara en bucle sin respirar |

**La distinción clave del día:** un **check** verifica un request; un **threshold** es el criterio que decide si el proceso pasa o falla. **El pipeline de CI escucha el threshold, no el check.**

### 3. Mapa de tipos de prueba (para ubicar lo que harás)

| Tipo | Pregunta | Hoy |
|---|---|---|
| **Smoke** | ¿Enciende con poca carga? | Hands-on (`k6-smoke`) |
| **Load** | ¿Aguanta la carga esperada? | Hands-on (`k6-load`) |
| **Stress** | ¿Dónde se rompe si empujamos de más? | Concepto |
| **Spike** | ¿Qué pasa con un pico brusco? | Concepto |

No necesitas las cuatro el primer día. Necesitas **saber cuál estás corriendo** y por qué el umbral del smoke es más estricto que el del load.

### 4. K6: performance como código

- El script es **JavaScript** y vive en Git → se revisa en un PR como cualquier código.
- Corre desde una imagen de Docker (`grafana/k6:1.8.0`): **no instalas K6** en tu máquina.
- Estilo actual (2026): `scenarios` con el executor `ramping-vus` (además de los `stages` clásicos).
- Escala opcional (solo concepto): Grafana Cloud k6 — el mismo script, con muchos más VUs.

### 5. El servidor local (target)

El `docker-compose.yml` levanta un nginx que sirve dos endpoints:

- `GET /api/health` → `{"status": "ok", ...}`
- `GET /api/product` → un producto de ejemplo con `title`

K6 le pega a `http://target:8080` (ese es el nombre del servicio dentro de la red de Docker; por eso las pruebas corren con `docker compose run`, no contra `localhost`).

### 6. Tu primer smoke — lee el script completo

Abre `k6/smoke.js`. Tiene dos partes, igual que un test de pytest: **criterio** (`options`) y **acción** (`default function`).

**Criterio (el gate):**

```javascript
export const options = {
  vus: 2,
  duration: "15s",
  thresholds: {
    http_req_failed: ["rate<0.01"],     // menos del 1% de errores
    http_req_duration: ["p(95)<500"],   // p95 por debajo de 500 ms
    checks: ["rate>0.99"],              // más del 99% de checks OK
  },
};
```

**Acción (lo que hace cada VU):**

```javascript
export default function () {
  const health = http.get(`${BASE_URL}/api/health`);
  check(health, {
    "health status 200": (r) => r.status === 200,
    "health body ok": (r) => String(r.body).includes('"status": "ok"'),
  });

  const product = http.get(`${BASE_URL}/api/product`);
  check(product, {
    "product status 200": (r) => r.status === 200,
    "product has title": (r) => String(r.body).includes("title"),
  });

  sleep(0.5); // think time: simula que el usuario "piensa" medio segundo
}
```

Compara con la S4: `http.get` ≈ `httpx.get`, `check` ≈ `assert`, `thresholds` ≈ el criterio que CI usa para poner el job en rojo.

Córrelo (el target ya está arriba):

```bash
docker compose run --rm k6-smoke
```

**Antes de dar Enter, predice:** ¿exit 0 (verde) o ≠ 0 (rojo)?

**Resultado esperado (datos reales de una corrida):**

```
✓ 'p(95)<500' p(95)=49.42ms      ✓ 'rate<0.01' rate=0.00%
checks_succeeded: 100.00% (232/232)   http_reqs: 116   exit 0
```

Con 2 VUs durante 15 s se lanzaron 116 requests y el p95 quedó en ~49 ms, muy por debajo de los 500 ms → los tres thresholds pasan y el proceso termina en **exit 0**.

---

## ☕ Descanso (15 min)

**Tarea opcional:** abre `k6/load.js` y cuenta cuántas etapas (`stages`) tiene el escenario `average_load`. (Respuesta: 3.)

---

## Bloque B — Load, thresholds y el fallo a propósito (45 min)

### 1. Load con etapas (stages) + ramping-vus

Un load realista sube la carga, la mantiene y la baja. Abre `k6/load.js`:

```javascript
export const options = {
  scenarios: {
    average_load: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "10s", target: 5 },   // sube a 5 VUs
        { duration: "20s", target: 10 },  // mantiene alrededor de 10
        { duration: "10s", target: 0 },   // baja a 0
      ],
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<800"],   // más holgado que el smoke: hay más carga
    checks: ["rate>0.99"],
  },
};
```

La función `default` hace la misma "historia" que el smoke (`/api/health` + `/api/product`), con `tags` por endpoint y un `sleep(0.3)` de think time. El umbral de load (`<800`) es más flexible que el de smoke (`<500`) porque hay más VUs.

Córrelo:

```bash
docker compose run --rm k6-load
```

**Resultado esperado (datos reales de una corrida previa; los ms varían un poco):**

```
✓ 'p(95)<800' p(95)=18.49ms      ✓ 'rate<0.01' rate=0.00%
checks_succeeded: 100.00%   vus_max: 10   exit 0
```

El target local aguanta con holgura → **exit 0**. Contra un backend real estos números suben; por eso el número del umbral (`<800`) es una **decisión de negocio**, no un valor mágico.

### 2. Cómo leer el reporte (mira solo 4 cosas)

El resumen de K6 es largo. No lo leas entero; busca solo esto:

1. `http_req_duration` → ¿dónde está el **p95**?
2. `http_req_failed` → ¿qué porcentaje falló?
3. `checks` → ¿qué porcentaje de validaciones pasó?
4. El `✓` o `✗` junto a cada **threshold** → eso es lo que decide verde o rojo

Si no sabes leer estas cuatro líneas, cuando CI se ponga rojo no vas a saber por qué.

### 3. Provoca un fallo a propósito (rojo)

Abre `k6/fail_demo.js`: pide un umbral **imposible** contra la latencia real.

```javascript
export const options = {
  vus: 2,
  duration: "10s",
  thresholds: {
    http_req_duration: ["p(95)<1"],   // p95 < 1 ms: imposible aquí
  },
};
```

Córrelo:

```bash
docker compose run --rm k6-fail
```

**Resultado esperado (datos reales de una corrida):**

```
checks_succeeded: 100.00% (98/98)        ← TODOS los checks pasan
✗ 'p(95)<1' p(95)=14.28ms                ← el threshold se rompe
level=error msg="thresholds on metrics 'http_req_duration' have been crossed"   exit 99
```

**El momento clave del día:** los checks quedaron **100% en verde** y aun así el proceso terminó con **código 99**. Esto lo demuestra en vivo: el `check` no mueve el gate; el `threshold` sí. En un pipeline, `exit 99` es un **"no" al merge**.

> ¿Por qué 99 y no un genérico 1? K6 usa el código **99** específicamente para "threshold roto", así lo distingues de otros fallos.

### 4. Cómo encaja con CI (lo de la Sesión 5)

El patrón de un equipo moderno:

1. Smoke (y pytest) en **cada PR** — rápido, barato.
2. Load más pesado en `main` o de noche (`schedule`) — no bloquea cada push chico.
3. Si K6 termina con código ≠ 0, el job **falla igual** que si fallara pytest.

Abre la plantilla didáctica: `proyecto-integrador/performance/workflows/qa-perf.yml`.

```yaml
- name: Start target + run smoke
  run: |
    docker compose up -d --wait target
    docker compose run --rm k6-smoke
    # threshold roto → exit 99 → job ROJO → no merge
```

Hoy no hace falta que ese workflow esté activo en GitHub: el criterio es el **código de salida**, exactamente como en la S5. La plantilla es para que veas el YAML real, no solo la idea.

### 5. Cómo se elige el número del threshold (regla práctica)

1. Corre 2–3 veces contra un entorno "bueno conocido" (baseline).
2. Mira el p95 real.
3. Suma un **buffer del 20–30%** (el CI es ruidoso: runners compartidos, red).
4. Ese valor pasa a ser tu umbral de gate.

Por eso el smoke usa `<500` y el load `<800` en este lab: holgados a propósito para el target local. En un producto real los mides; no los inventas.

---

## ☕ Descanso (15 min)

Sin tarea — llega fresco al mini-reto.

---

## Bloque C — Mini-reto y cierre del Reto 1 (45 min)

### Mini-reto: endurece un threshold

1. Abre `k6/load.js`.
2. Cambia `p(95)<800` por `p(95)<5`.
3. Corre `docker compose run --rm k6-load`.
4. Observa el **rojo**: el p95 real (decenas de ms) supera el nuevo límite de 5 ms.

```
✗ 'p(95)<5' p(95)=…ms   →   exit 99
```

5. **Revierte** el cambio (deja `<800`) para que el lab quede utilizable.

**Lo que demuestra:** el número del threshold es una **decisión de negocio**. Bajarlo o subirlo cambia qué se considera "aceptable"; no hay un valor mágico universal.

### Por qué p95 y no el promedio

| Métrica | Qué esconde |
|---|---|
| **Promedio** | Un pico de 5 s se "diluye" entre muchos requests rápidos → engaña |
| **p95 / p99** | Muestran la **cola lenta**: la experiencia del usuario desafortunado |

Los umbrales de negocio se escriben como **SLO/SLA** (por ejemplo, "p95 < 300 ms"). Regla práctica: mide la cola, no el centro — los usuarios recuerdan el request lento.

### Herramientas del mercado (30 s por fila)

| Herramienta | Lenguaje | Nota |
|---|---|---|
| **K6** | JavaScript | Script + integración con CI — **la ruta de este curso** |
| JMeter | GUI/XML | Clásico con interfaz gráfica; mucha empresa con sistemas heredados lo usa |
| Gatling | Scala/JVM | Reportes ricos; ecosistema Java |
| Locust | Python | Familiar si el equipo ya trabaja en Python |

El patrón es el mismo en las cuatro; la herramienta cambia según el equipo. **A escala:** Grafana Cloud k6 corre el mismo script con miles de VUs desde varias regiones.

### Reto 1 cerrado (concepto)

Ya tienes las tres piezas de un criterio de release automatizado:

- **Automatización de API** (Postman y/o pytest — S3/S4)
- **CI** (GitHub Actions — S5)
- **Performance con umbrales** (K6 — hoy)

Hoy cerraste la pieza de **umbrales de performance**.

### Checklist

- [ ] Distingo una prueba funcional de una de performance
- [ ] Sé qué es un threshold y por qué **no** es lo mismo que un check
- [ ] Ubico smoke vs load (y sé que stress/spike existen)
- [ ] Corrí smoke y load en verde (exit 0)
- [ ] Provoqué un fallo a propósito y vi checks 100% en verde pero **exit 99**
- [ ] Relaciono el resultado de K6 con el criterio de CI de la S5
- [ ] Sé la regla práctica para elegir un umbral (baseline + buffer)

### Frase de cierre (30 s)

Completa: *"Un threshold sirve para ___."*

### Para llevar

La performance también se verifica de forma automática. Con un threshold roto, el pipeline bloquea el cambio igual que con un test funcional en rojo.

---

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| El puerto 8080 está ocupado | Otro proceso lo usa | Cambia el mapeo a `"8081:8080"` en `docker-compose.yml` |
| `target` aparece *unhealthy* | El servidor no arrancó bien | Revisa `docker compose logs target` |
| K6 no encuentra `target` | Corriste K6 contra `localhost` | Usa `docker compose run` (misma red Docker; el host es `target`) |
| El pull de la imagen k6 es lento | Primera vez que se descarga | Pre-descárgala: `docker pull grafana/k6:1.8.0` |
| El smoke sale rojo | El target no estaba arriba | `docker compose up -d target` primero |
| `load.js` quedó roto tras el mini-reto | No revertiste el cambio | Vuelve a poner `p(95)<800` |

---

## Resumen de comandos

```bash
cd proyecto-integrador/performance
docker compose up -d target                   # levanta el servidor local
curl.exe http://127.0.0.1:8080/api/health      # comprueba: "status": "ok"

docker compose run --rm k6-smoke               # smoke → exit 0
docker compose run --rm k6-load                # load  → exit 0
docker compose run --rm k6-fail                # demo de fallo → exit 99

docker compose down                            # apaga y limpia el lab

# Atajos desde curso/
task test:perf:smoke
task test:perf:load
```

**Plantilla CI para leer:** `proyecto-integrador/performance/workflows/qa-perf.yml`

**Próxima sesión (S7):** Seguridad — cómo llevar el mismo criterio automático al terreno de las vulnerabilidades.
