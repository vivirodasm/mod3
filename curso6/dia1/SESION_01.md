# Día 1 — Gobernanza, métricas y dashboards observables

> **Duración:** 4 horas · **Ritmo:** Bloque A (45) → descanso 15 → B (45) → descanso 15 → C (45) → descanso 15 → D (45)
> **Lo que vas a construir:** un dashboard de gobernanza QA con Prometheus + Grafana que muestra flake rate, defect leakage, test effectiveness y cobertura por microservicio, con alertas reales e histórico de ~3 días.
> **Este día es autónomo:** no necesitás el material del Día 2.

---

## Antes de empezar

### Requisitos

| Herramienta | Windows | macOS |
|-------------|---------|-------|
| Docker Desktop | [Instalar](https://docs.docker.com/desktop/setup/install/windows-install/) y dejarlo **Running** | [Instalar](https://docs.docker.com/desktop/setup/install/mac-install/) y dejarlo **Running** |
| Python 3.11+ | Ya instalado o desde python.org | `brew install python` (o el que uses) |
| Navegador | Chrome / Edge / Firefox | Safari / Chrome / Firefox |
| Terminal | PowerShell o Git Bash | Terminal (zsh/bash) |

### Puertos que deben estar libres

- **8000** — exporter de métricas  
- **9090** — Prometheus  
- **3000** — Grafana  

> En Mac **no uses el puerto 5000** para este lab (conflicto frecuente con AirPlay).

### Arranque del laboratorio (hazlo antes o al inicio del Bloque C/D)

```bash
# Desde la carpeta del Día 1
cd curso6/dia1/proyectos/qa-governance-dashboard

# 1) Genera ~3 días de histórico (obligatorio la primera vez o tras `docker compose down -v`)
python scripts/generate_history.py

# 2) Levanta exporter + Prometheus + Grafana
docker compose up -d --build
```

**En Windows PowerShell**, si `python` no funciona, prueba `py scripts/generate_history.py`.

Espera 30–60 segundos y valida:

```bash
# macOS / Linux / Git Bash
curl -sf http://127.0.0.1:8000/
curl -sf http://127.0.0.1:9090/-/ready

# Windows PowerShell
curl.exe -sf http://127.0.0.1:8000/
curl.exe -sf http://127.0.0.1:9090/-/ready
```

Deberías ver JSON `{"status":"ok"...}` y el texto `Prometheus Server is Ready.`

Si algo falla aquí, **paré** y mirá la tabla de [Errores comunes](#errores-comunes) al final.

---

## Agenda

| Bloque | Duración | Contenido |
|--------|----------|-----------|
| **A** | 45 min | Gobernanza de la automatización de pruebas |
| Descanso | 15 min | ☕ |
| **B** | 45 min | Métricas: flake, leakage, effectiveness, test debt |
| Descanso | 15 min | ☕ |
| **C** | 45 min | Dashboards observables (Prometheus / Grafana / Kibana) |
| Descanso | 15 min | ☕ |
| **D** | 45 min | **Reto 1:** dashboard de gobernanza QA en vivo |

Material de apoyo (no es la guía del estudiante):
- Diapositivas: `ppt_contenido.md` / `dia1.pptx`
- Guion del instructor: `instructor_guide.md`

---

## Bloque A — Gobernanza de la automatización (45 min)

### 1. ¿Qué es gobernanza de pruebas?

No es “tener muchos tests”. Es tener:

- **Políticas** de qué se automatiza y qué no  
- **Criterios de cobertura** ligados a riesgo de negocio  
- **Dueños** de la deuda técnica de las pruebas  
- **Trazabilidad** auditable: requisito → caso → automatización → resultado  

Pregunta para anotar: *en tu equipo, ¿quién decide hoy qué se automatiza?*

### 2. Políticas y cobertura con sentido

Automatizá prioritariamente:

- Regresión crítica  
- Contratos / APIs de dinero, auth y datos sensibles  
- Smoke de release  

No automatices por deporte: exploratorio puro o UI que cambia cada martes sin valor de negocio suelen ser mala inversión.

**Cobertura ≠ porcentaje mágico.** Más riesgo → más profundidad. Menos riesgo → smoke + monitoreo.

### 3. Deuda técnica en pruebas

Señales típicas:

- Tests flaky (a veces pasan, a veces fallan)  
- Duplicación de locators / URLs / datos  
- `sleep` / waits fijos  
- Suite tan lenta que nadie la corre  

Gobernanza = presupuesto y tiempo para **pagar** esa deuda.

### 4. Auditoría y herramientas

| Herramienta | Rol típico |
|-------------|------------|
| TestRail | Gestión de casos y ciclos |
| Zephyr Scale | Trazabilidad en Jira |
| Allure TestOps | Resultados + analítica de suites |

La herramienta **no reemplaza** la política. Sin reglas, solo tenés un cementerio más ordenado.

### Checklist rápido del Bloque A

- [ ] Sé explicar gobernanza en una frase  
- [ ] Distingo cobertura por riesgo vs % cosmético  
- [ ] Sé nombrar al menos una señal de deuda de tests  

---

## Bloque B — Métricas de calidad y efectividad (45 min)

### 1. Por qué medir

Lo que no se mide se discute con opiniones.  
Métricas buenas cambian comportamiento.  
Métricas malas incentivan maquillaje (subir cobertura sin bajar riesgo).

### 2. Las cuatro métricas del día

| Métrica | Fórmula / idea | Umbral del lab |
|---------|----------------|----------------|
| **Flake rate** | tests flaky / tests ejecutados | alerta si **> 0.10** |
| **Defect leakage** | defectos en prod / defectos totales | alerta si **> 0.12** |
| **Test effectiveness** | defectos hallados en test / totales | warning si **< 0.85** |
| **Test debt** | esfuerzo pendiente para sanar la suite | se gestiona como backlog |
| **Cobertura** | % automatizado por servicio (con criterio de riesgo) | warning si **< 70%** |

### 3. Ejercicio rápido (calculá a mano)

Datos de ejemplo (*payments*):

- 100 tests, 9 flaky → flake = **0.09**  
- 20 bugs totales, 3 en prod → leakage = **0.15**  
- Effectiveness ≈ **0.85**  

¿Qué atacarías primero: flake o leakage? Anotá tu respuesta; no hay una sola correcta — depende del dolor dominante (CI que nadie cree vs prod que arde).

### 4. Dashboard mental

```
Flake ↓   Leakage ↓   Effectiveness ↑   Cobertura (por riesgo) ↑
```

Con esos números podés hablar con liderazgo sin improvisar.

---

## Bloque C — Dashboards observables (45 min)

### 1. El stack del laboratorio

```
Exporter (:8000/metrics)  →  Prometheus (:9090)  →  Grafana (:3000)
     datos crudos              guarda + alertas         lo que se mira
```

- **Kibana / Loki** (concepto): correlacionar métricas con logs (ej. flake subió después de un deploy).

### 2. Métricas que publica el exporter

- `qa_flake_rate{service=...}`  
- `qa_defect_leakage{service=...}`  
- `qa_test_effectiveness_ratio{service=...}`  
- `qa_coverage{service=...}`  

Servicios demo: **auth · payments · catalog · notifications**

### 3. Prepará el Reto 1

Si aún no levantaste el stack, volvé a la sección [Antes de empezar](#antes-de-empezar) y ejecutá los comandos.

Confirmá métricas:

```bash
# macOS / Linux / Git Bash
curl -sf http://127.0.0.1:8000/metrics | grep qa_flake_rate

# Windows PowerShell
curl.exe -sf http://127.0.0.1:8000/metrics | Select-String qa_flake_rate
```

---

## Bloque D — Reto 1: dashboard de gobernanza QA (45 min)

### Enunciado

Construir (y **usar**) un dashboard con Grafana + Prometheus que visualice en tiempo real:

- flake rate  
- defect leakage  
- test effectiveness ratio  
- cobertura por microservicio  

…con alertas por umbrales críticos e histórico de ~3 días.

> En este curso el stack ya viene armado en `proyectos/qa-governance-dashboard`. Tu trabajo es **levantarlo, validarlo, leerlo e interpretar** las señales como lo harías en un equipo real.

### Paso 1 — Levantar (si no lo hiciste)

```bash
cd curso6/dia1/proyectos/qa-governance-dashboard
python scripts/generate_history.py
docker compose up -d --build
```

Esperado: contenedores `qa-exporter`, `qa-prometheus`, `qa-grafana` arriba.

### Paso 2 — Validar exporter y Prometheus

```bash
curl.exe -sf http://127.0.0.1:8000/          # o curl -sf en Mac
curl.exe -sf http://127.0.0.1:8000/metrics
curl.exe -sf http://127.0.0.1:9090/-/ready
```

### Paso 3 — Grafana (clic a clic — empezá por acá)

1. Abrí **http://localhost:3000**  
2. Login: usuario **`admin`** · contraseña **`admin`**  
3. Menú ☰ (izquierda) → **Dashboards**  
4. Carpeta **QA Governance** → **QA Governance Dashboard**  
5. Arriba a la derecha (reloj de tiempo) → elegí **Last 3 days**  

**Qué deberías ver:**

- Panel de **alertas** arriba (firing / pending)  
- Flake, leakage, effectiveness y cobertura por servicio  
- Gráficos con histórico de ~3 días  

En el lab, **payments** y **notifications** suelen verse “en rojo” a propósito (umbrales rotos).

### Paso 4 — Alertas en Prometheus

1. Abrí **http://localhost:9090/alerts**  
2. Buscá alertas en estado **firing** (HighFlakeRate, HighDefectLeakage, etc.)  
3. Relacionalas con los umbrales del Bloque B  

### Paso 5 — Graph de Prometheus (opcional)

Si querés ver la serie cruda, usá **este link** (ya trae la query):

http://localhost:9090/graph?g0.expr=qa_flake_rate&g0.range_input=3d&g0.tab=0

Tocá **Execute** / pestaña **Graph**.

> Si abrís solo `http://localhost:9090` y el recuadro de Expression está vacío → **no vas a ver nada**. Siempre hace falta una query (ej. `qa_flake_rate`).

### Entregable / checklist del Reto 1

- [ ] Stack levantado y respondiendo  
- [ ] Grafana abierto con rango Last 3 days  
- [ ] Identificaste el servicio más crítico y por qué  
- [ ] Viste al menos una alerta **firing** en `/alerts`  
- [ ] Podés explicar: métrica + umbral + dueño + acción  

### Preguntas de cierre (anotá tus respuestas)

1. ¿Qué servicio priorizarías para pagar deuda de tests?  
2. ¿Esa alerta es ruido o señal?  
3. ¿Quién sería el dueño de bajar el flake en tu empresa?  

---

## Errores comunes

| Error / síntoma | Causa probable | Solución |
|-----------------|----------------|----------|
| `dockerDesktopLinuxEngine` / cannot connect | Docker Desktop apagado | Abrí Docker Desktop y esperá a que diga **Running** |
| Puerto en uso (`bind: address already in use`) | Otro proceso usa 8000/9090/3000 | Cerrá el proceso o cambiá el lado izquierdo del mapeo en `docker-compose.yml` (ej. `"8001:8000"`) |
| Grafana sin dashboard | Aún no provisionó | Esperá ~30 s y refrescá; carpeta **QA Governance** |
| Prometheus Graph vacío | Query vacía | Usá el link con `g0.expr=qa_flake_rate` o escribí la query y Execute |
| Sin histórico de 3 días | No corriste el seed o borraste el volumen | `python scripts/generate_history.py` y `docker compose down -v && docker compose up -d --build` |
| `python: command not found` | Python no en PATH | Windows: `py scripts/generate_history.py` · Mac: instalá Python / usá `python3` |
| Login Grafana no funciona | Credenciales distintas | Lab: **admin / admin** |

---

## Comandos útiles

```bash
# Ver contenedores
docker compose ps

# Logs si algo falla
docker compose logs -f exporter
docker compose logs -f prometheus

# Detener (conserva histórico)
docker compose down

# Detener y borrar histórico (hay que volver a generar seed)
docker compose down -v
```

---

## Para llevar

Después del Día 1 tenés:

- Vocabulario de gobernanza (políticas, deuda, trazabilidad)  
- Métricas con umbral: flake, leakage, effectiveness, cobertura  
- Un lab runnable: Prometheus + Grafana con alertas reales  
- La cuádruple cadena: **métrica + umbral + dueño + acción**  

En el **Día 2** (`curso6/dia2/SESION_02.md`) vas a testing de datos/ML, RPA, gamificación y madurez TMMi.
