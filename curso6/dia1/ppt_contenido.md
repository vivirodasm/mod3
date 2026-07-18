# Certificación 6 — Día 1 · Contenido de diapositivas
## Madurez, Gobernanza y Estrategia de Calidad Organizacional

> 4 horas · Bloques de 45 min + descansos de 15 min
> Slides 1–44 · Proyecto: `proyectos/qa-governance-dashboard`

---

## DÍA 1 — Gobernanza, métricas y dashboards

### Slide 1 — Portada Día 1 (2 min)
**Título:** Madurez, Gobernanza y Estrategia de Calidad
- Certificación 6 · Día 1 autónomo · 4 horas
- Gobernanza · métricas · dashboards · Reto 1
- Formato: 45 min trabajo + 15 min descanso

### Slide 2 — Agenda del Día 1 (2 min)
- Bloque 1: Gobernanza de la automatización
- Bloque 2: Métricas de calidad y efectividad
- Bloque 3: Dashboards observables (Prometheus / Grafana / Kibana)
- Bloque 4: Reto 1 — dashboard de gobernanza QA en vivo

### Slide 3 — Objetivos de aprendizaje (3 min)
- Aplicar gobernanza y métricas avanzadas (flake rate, defect leakage, test effectiveness)
- Preparar automatización en IA, datos y RPA (MLflow, UiPath, Great Expectations)
- Diseñar madurez sostenible con TMMi y validación continua

### Slide 4 — ¿Cómo mediremos el éxito? (3 min)
- Políticas + métricas + dashboards observables
- Labs ejecutables (no solo teoría)
- Criterio final: decisiones de calidad defendibles ante negocio

### Slide 5 — Mapa del curso (2 min)
```
Día 1: Gobernar y medir
Día 2: IA/datos + RPA + madurez TMMi
```
- Reto 1 hoy · Reto 2 mañana
- Todo el contenido sale del temario oficial de Certificación 6

---

## BLOQUE 1 (45 min) — Gobernanza de la automatización

### Slide 6 — ¿Qué es gobernanza de pruebas? (4 min)
- No es “tener muchos tests”
- Es **políticas**, **criterios** y **trazabilidad** que todos entienden
- Pregunta guía: ¿quién decide qué se automatiza y por qué?

### Slide 7 — Políticas de automatización (5 min)
- Qué automatizar (regresión crítica, contratos, smoke)
- Qué NO automatizar (exploratorio puro, UI inestable sin valor)
- Criterios de cobertura ligados a **riesgo de negocio**

### Slide 8 — Criterios de cobertura con sentido (4 min)
- Cobertura ≠ porcentaje mágico
- Priorizar flujos de dinero, autenticación y datos sensibles
- Cada automatización debe tener dueño y criterio de éxito

### Slide 9 — Deuda técnica en pruebas (5 min)
- Tests frágiles, duplicados, sin datos controlados
- Suite lenta que nadie corre = deuda invisible
- Gobernanza = presupuesto para pagar esa deuda

### Slide 10 — Auditoría, cumplimiento y trazabilidad (5 min)
- ¿Qué se probó? ¿Cuándo? ¿Con qué evidencia?
- Requisito en industrias reguladas — y buena práctica en todas
- Trazabilidad: requisito → caso → automatización → resultado

### Slide 11 — Herramientas de gobernanza (5 min)
| Herramienta | Rol típico |
|---|---|
| TestRail | Gestión de casos y ciclos |
| Zephyr Scale | Trazabilidad en Jira |
| Allure TestOps | Resultados + analítica de suites |
- La herramienta no reemplaza la política

### Slide 12 — Mini-caso: sin política (4 min)
- Equipo A automatiza todo lo clickable
- Equipo B solo smoke manual
- Resultado: cobertura engañosa + fugas a producción
- **Debate:** ¿dónde falla la gobernanza?

### Slide 13 — Checklist de gobernanza (4 min)
- [ ] Política escrita de automatización
- [ ] Criterios de cobertura por riesgo
- [ ] Dueño de deuda de tests
- [ ] Evidencia auditable por release
- [ ] Herramienta alineada al proceso (no al revés)

### Slide 14 — Cierre Bloque 1 (3 min)
- Gobernanza = reglas + evidencia + dueños
- Mañana hablamos de RPA e IA; hoy medimos lo que importa
- Siguiente: las métricas que hacen visible la calidad

---
**DESCANSO 15 MIN**
---

### Slide 15 — Volvemos · Bloque 2 (1 min)
**Título:** Métricas de calidad y efectividad
- Flake rate · test debt · test effectiveness · defect leakage
- Calculamos juntos · sin fórmulas mágicas

---

## BLOQUE 2 (45 min) — Métricas de calidad

### Slide 16 — Por qué medir (3 min)
- Lo que no se mide se discute con opiniones
- Métricas buenas cambian comportamiento
- Métricas malas incentivan “maquillaje” de cobertura

### Slide 17 — Flake rate (5 min)
```
flake rate = tests flaky / tests ejecutados
```
- Flaky = a veces pasa, a veces falla, sin cambio de código
- Umbral típico de alerta en el lab: **> 10%**
- Flake alto destruye confianza en CI

### Slide 18 — Defect leakage (5 min)
```
defect leakage = defectos en prod / defectos totales
```
- Mide lo que “se escapó” del muro de calidad
- Umbral crítico lab: **> 12%**
- Pregunta: ¿fuga por falta de pruebas o por mal alcance?

### Slide 19 — Test effectiveness ratio (5 min)
```
effectiveness ≈ defectos hallados en test / defectos totales
```
- Complemento del leakage
- Umbral lab: **< 0.85** = warning
- Objetivo: que el test encuentre antes que el usuario

### Slide 20 — Test debt (4 min)
- Deuda = esfuerzo pendiente para volver la suite sana
- Señales: skips eternos, waits fijos, asserts débiles
- Se gestiona como backlog con prioridad de riesgo

### Slide 21 — Cobertura y priorización por riesgo (5 min)
- Cobertura por microservicio (auth, payments, catalog…)
- Más riesgo → más profundidad de prueba
- Menos riesgo → smoke + monitoreo

### Slide 22 — Ejercicio en vivo: calcular (8 min)
Datos de ejemplo (payments):
- 100 tests · 9 flaky → flake = **0.09**
- 20 bugs totales · 3 en prod → leakage = **0.15**
- Effectiveness ≈ **0.85**
- ¿Qué harían primero: bajar flake o bajar leakage?

### Slide 23 — Dashboard mental (4 min)
```
Flake ↓   Leakage ↓   Effectiveness ↑   Cobertura (riesgo) ↑
```
- Cuatro números · una conversación con liderazgo
- Siguiente bloque: llevarlos a Prometheus + Grafana

### Slide 24 — Cierre Bloque 2 (2 min)
- Métricas con umbral > métricas “bonitas”
- Ya tienen el lenguaje del Reto 1
- Café y volvemos a dashboards

---
**DESCANSO 15 MIN**
---

### Slide 25 — Volvemos · Bloque 3 (1 min)
**Título:** Dashboards observables
- Prometheus · Grafana · Kibana / Loki
- Diseño del Reto 1

---

## BLOQUE 3 (45 min) — Dashboards observables

### Slide 26 — Observabilidad para QA (4 min)
- No solo logs de app: **salud de la calidad**
- Métricas scrapeables + paneles + alertas
- Si nadie mira el dashboard, no existe gobernanza

### Slide 27 — Stack del lab (5 min)
```
Exporter (métricas QA)
    ↓ scrape
Prometheus (+ alertas)
    ↓ query
Grafana (dashboard)
```
- Kibana/Loki: logs y correlación (concepto)
- Puertos lab: **8000 / 9090 / 3000**

### Slide 28 — Prometheus en una frase (4 min)
- Guarda series de tiempo y evalúa reglas
- Scrape cada 10s al exporter
- Alertas: HighFlakeRate, HighDefectLeakage, LowEffectiveness, LowCoverage

### Slide 29 — Grafana en una frase (4 min)
- Convierte queries en paneles legibles
- Dashboard provisionado: *QA Governance Dashboard*
- Login demo: admin / admin (solo lab)

### Slide 30 — Kibana y Loki (3 min)
- Kibana: exploración de logs/eventos
- Loki: logs ligeros alineados a Grafana
- Uso típico: correlacionar flake con deploy o cambio de datos

### Slide 31 — Métricas del exporter (5 min)
- `qa_flake_rate{service=...}`
- `qa_defect_leakage{service=...}`
- `qa_test_effectiveness_ratio{service=...}`
- `qa_coverage{service=...}`
- Servicios demo: auth · payments · catalog · notifications

### Slide 32 — Umbrales críticos del Reto 1 (4 min)
| Métrica | Alerta si… |
|---|---|
| Flake rate | > 0.10 |
| Defect leakage | > 0.12 |
| Effectiveness | < 0.85 |
| Cobertura | < 70% |

### Slide 33 — Preparación del Reto 1 (8 min)
Requisitos:
- Docker Desktop (Win/Mac)
- Carpeta: `proyectos/qa-governance-dashboard`
Comandos (en orden):
```bash
python scripts/generate_history.py
docker compose up -d --build
```
- `generate_history` = siembra ~3 días de datos
Validar:
```bash
curl http://127.0.0.1:8000/metrics
```

### Slide 34 — Plan B si Docker falla (3 min)
- Revisar que Docker Desktop esté “Running”
- Liberar puertos 8000/9090/3000
- En Mac: no usar puerto 5000 (AirPlay)
- Instructor comparte pantalla con stack ya levantado

### Slide 35 — Cierre Bloque 3 (2 min)
- Ya saben qué van a construir
- Siguiente bloque: manos en el teclado · Reto 1

---
**DESCANSO 15 MIN**
---

### Slide 36 — Volvemos · Bloque 4 Reto 1 (1 min)
**Título:** Reto 1 — Dashboard de gobernanza QA
- Construir · visualizar · interpretar alertas

---

## BLOQUE 4 (45 min) — Reto 1 práctico

### Slide 37 — Enunciado del Reto 1 (3 min)
Construir un dashboard con Grafana + Prometheus que muestre en tiempo real:
- flake rate
- defect leakage
- test effectiveness ratio
- cobertura por microservicio
…con alertas por umbrales críticos

### Slide 38 — Paso 1: levantar el stack (8 min)
```bash
cd proyectos/qa-governance-dashboard
python scripts/generate_history.py
docker compose up -d --build
```
Esperado:
- exporter healthy
- Prometheus con histórico ~3 días
- Grafana en :3000

### Slide 39 — Paso 2: validar métricas (7 min)
```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/metrics
curl http://127.0.0.1:9090/-/ready
```
- Buscar líneas `qa_flake_rate` y `qa_defect_leakage`

### Slide 40 — Paso 3: abrir Grafana (clic a clic) (8 min)
1. Abrir http://localhost:3000
2. Login: **admin** / **admin**
3. Menú ☰ → **Dashboards** → carpeta **QA Governance**
4. Abrir **QA Governance Dashboard**
5. Arriba a la derecha: rango **Last 3 days**
- Mirar panel de alertas + paneles por servicio
- Identificar el servicio “más rojo” (payments / notifications)

### Slide 41 — Paso 4: alertas en Prometheus (7 min)
- Alertas: http://localhost:9090/alerts → estado **firing**
- Graph (opcional): http://localhost:9090/graph?g0.expr=qa_flake_rate&g0.range_input=3d&g0.tab=0
- Si el Graph está vacío: falta la query `qa_flake_rate` (no abrir solo :9090)
- Relacionar alertas con umbrales del slide 32
- Discusión: ¿qué acción de gobernanza tomarían?

### Slide 42 — Debrief del Reto 1 (7 min)
- ¿Qué servicio priorizarían para reducir deuda?
- ¿La alerta es ruido o señal?
- Gobernanza = métrica + umbral + dueño + acción
- Cierre Día 1

### Slide 43 — Cierre Día 1 (3 min)
- Hoy: gobernar, medir y visualizar
- Mañana: IA/ML, datos ETL, RPA, gamificación y TMMi
- Tarea opcional: anotar 3 métricas de su trabajo actual

### Slide 44 — Fin Día 1
**Título:** Gracias — nos vemos en el Día 2
- Material: `proyectos/qa-governance-dashboard`
- Dudas al chat / foro del curso

---

