# Certificación 6 — Día 2 · Contenido de diapositivas
## Madurez, Gobernanza y Estrategia de Calidad Organizacional

> 4 horas · Bloques de 45 min + descansos de 15 min
> Slides 1–41 · Proyecto: `proyectos/ml-data-quality-lab`

---

## Día 2 — IA, datos, RPA y madurez

### Slide 1 — Portada Día 2 (2 min)
**Título:** Validación continua · IA · datos · madurez TMMi
- Certificación 6 · Día 2 autónomo · 4 horas
- Reto 2 + estrategia organizacional (no requiere Docker del Día 1)

### Slide 2 — Agenda del Día 2 (2 min)
- Bloque 1: Testing IA/ML + pipelines de datos
- Bloque 2: Reto 2 práctico
- Bloque 3: RPA · simulación de usuarios · gamificación
- Bloque 4: TMMi + cierre y Q&A

---

## BLOQUE 1 (45 min) — Testing IA/ML y datos

### Slide 3 — Por qué testing de IA es distinto (4 min)
- No hay “assert igual a 200” suficiente
- Modelos: precisión, sesgo, fairness, drift
- Datos malos → modelo “correcto” que decide mal

### Slide 4 — Validación de modelos (5 min)
- **Precisión:** ¿acertamos lo que importa?
- **Sesgo / fairness:** ¿el error castiga a un grupo?
- **Drift:** ¿los datos de hoy ya no se parecen a los de entrenamiento?
- Herramientas: DeepChecks · SageMaker Model Monitor

### Slide 5 — Pipelines de datos y modelos (5 min)
- MLflow: tracking de experimentos y métricas
- DVC: versionado de datos/modelos
- Idea clave: reproducibilidad = calidad

### Slide 6 — Testing de pipelines ETL/ELT (5 min)
- Integridad, nulos, duplicados, formatos
- Si el ETL ensucia, el modelo hereda el bug
- Herramientas: Great Expectations · Deequ · Soda Core · DBT

### Slide 7 — Great Expectations en una frase (4 min)
- “Expectativas” sobre columnas y tablas
- Suite = contrato de calidad de datos
- En el lab: nulos, uniques, sets, rangos, regex de email

### Slide 8 — DeepChecks y monitoreo (3 min)
- DeepChecks: suites de validación de ML
- SageMaker Model Monitor: drift en producción (concepto cloud)
- Elegir herramienta según stack del equipo

### Slide 9 — Plan de testing para un modelo (5 min)
1. Validar datos de entrada (ETL)
2. Entrenar / cargar modelo
3. Medir precisión
4. Medir fairness proxy
5. Medir drift vs referencia
6. Publicar resultado en CI + MLflow

### Slide 10 — Integración CI/CD (4 min)
- El plan no vive en una laptop: vive en el pipeline
- Rojo en CI = no merge / no deploy del artefacto de datos
- Workflow ejemplo en el Reto 2

### Slide 11 — Preview del Reto 2 (5 min)
Carpeta: `proyectos/ml-data-quality-lab`
```bash
uv sync
uv run pytest -v
uv run python -m src.run_pipeline
```
- 5 tests en verde · reporte JSON · MLflow local

### Slide 12 — Cierre Bloque 1 (2 min)
- Datos + modelo + CI = trinomio del Reto 2
- Descanso y manos a la obra

---
**DESCANSO 15 MIN**
---

### Slide 13 — Volvemos · Bloque 2 Reto 2 (1 min)
**Título:** Reto 2 — Plan de testing ML + datos

---

## BLOQUE 2 (45 min) — Reto 2 práctico

### Slide 14 — Enunciado del Reto 2 (3 min)
Diseñar y ejecutar un plan que valide:
- precisión
- sesgo
- drift de datos
- integridad del pipeline ETL  
Integrar resultados en pipeline CI/CD (workflow de ejemplo incluido)

### Slide 15 — Paso 1: entorno (7 min)
```bash
cd proyectos/ml-data-quality-lab
uv sync
```
- macOS: `brew install uv` o instalador Astral
- Windows: instalador PowerShell de uv
- Python 3.11+

### Slide 16 — Paso 2: suite ETL (8 min)
```bash
uv run pytest tests/test_data_quality.py -v
```
- Limpio pasa · sucio falla (nulos/duplicados)
- Nombrar expectativas al estilo Great Expectations

### Slide 17 — Paso 3: Great Expectations (7 min)
```bash
uv run pytest tests/test_gx_integration.py -v
```
- Suite ephemeral sobre dataset limpio
- Contrato de datos ejecutable

### Slide 18 — Paso 4: modelo + MLflow (8 min)
```bash
uv run pytest tests/test_model_checks.py -v
uv run python -m src.run_pipeline
```
- Precisión · gap por región · PSI de income
- Tracking en SQLite local (`mlruns/mlflow.db`)

### Slide 19 — Paso 5: CI (5 min)
- Abrir `.github/workflows/quality.yml`
- Mismos comandos que en local
- Mensaje: “si no corre en CI, no es gobernanza”

### Slide 20 — Debrief Reto 2 (5 min)
- ¿Qué fallaría primero en su empresa: datos o modelo?
- ¿Quién es dueño del umbral de drift?
- Puente al Bloque 3: procesos de negocio y RPA

---
**DESCANSO 15 MIN**
---

### Slide 21 — Volvemos · Bloque 3 (1 min)
**Título:** RPA · simulación de usuarios · gamificación

---

## BLOQUE 3 (45 min) — RPA, simulación y formación

### Slide 22 — RPA para validación de procesos (5 min)
- Bots que ejercitan procesos de negocio repetitivos
- Ideal: backoffice, altas, conciliaciones, flujos “click + form”
- No reemplaza API/UI testing: **complementa** donde el proceso es el SUT

### Slide 23 — Ecosistema RPA (5 min)
| Plataforma | Nota |
|---|---|
| UiPath | Ampliamente usado en empresa |
| Power Automate | Fuerte en ecosistema Microsoft |
| Automation Anywhere | Automatización de procesos a escala |
- Criterio de selección: stack IT + licenciamiento + observabilidad

### Slide 24 — Casos de uso de validación (5 min)
- Regresión de proceso de altas de cliente
- Verificación de reportes batch nocturnos
- Smoke de backoffice post-deploy
- Evidencia: capturas + logs + ID de transacción

### Slide 25 — Simulación de usuarios reales con IA (6 min)
- Modelar comportamiento (no solo scripts lineales)
- Escenarios realistas con reinforcement learning (concepto)
- Pruebas basadas en patrones de uso reales
- Objetivo: encontrar bugs que el camino feliz no ve

### Slide 26 — De script a comportamiento (4 min)
```
Script fijo → caminos probables → política aprendida
```
- Más cobertura de “cómo la gente usa el producto”
- Requiere telemetría ética y datos de uso

### Slide 27 — Formación, simulación y gamificación (5 min)
- Simuladores de entornos de testing
- Retos prácticos con scoring automático
- Plataformas: Test Automation University · Codecademy
- Aprender haciendo > solo slides

### Slide 28 — Diseño de un reto gamificado (5 min)
- Objetivo claro (ej. bajar flake bajo umbral)
- Score automático (tests verdes + métricas)
- Feedback inmediato
- Lo hicieron ayer (Reto 1) y hoy (Reto 2)

### Slide 29 — Mini-caso integrado (5 min)
Proceso de crédito:
- RPA valida carga en backoffice
- GE valida dataset ETL
- Modelo ML decide aprobación
- Dashboard QA alerta leakage
- **Pregunta:** ¿dónde pondrían el primer control?

### Slide 30 — Cierre Bloque 3 (2 min)
- Personas + procesos + datos + modelos
- Falta el marco que ordena la evolución: **TMMi**

---
**DESCANSO 15 MIN**
---

### Slide 31 — Volvemos · Bloque 4 (1 min)
**Título:** TMMi · madurez · cierre

---

## BLOQUE 4 (45 min) — TMMi y estrategia

### Slide 32 — ¿Qué es TMMi? (5 min)
- Test Management Maturity Model Integration
- Niveles de evolución de la organización de testing
- Prácticas recomendadas por nivel
- No es una herramienta: es un **mapa de madurez**

### Slide 33 — Niveles (visión práctica) (6 min)
```
Inicial → Gestionado → Definido → Medido → Optimizado
```
- Día 1 (métricas + dashboards) empuja hacia “Medido”
- Retos y CI empujan hacia “Optimizado”
- Pregunta: ¿en qué nivel está su equipo hoy?

### Slide 34 — Dashboards centralizados de calidad (5 min)
- Cobertura · defectos · flakiness en un solo lugar
- Prometheus + Grafana (+ Kibana/Loki para logs)
- Gestión centralizada = misma verdad para QA, Dev y liderazgo

### Slide 35 — Estrategia sostenible de validación continua (6 min)
- Políticas (Bloque 1)
- Métricas con umbral (Bloque 2)
- Observabilidad (Bloques 3–4)
- Datos + ML (Bloques 5–6)
- Procesos RPA + aprendizaje (Bloque 7)
- Madurez TMMi (Bloque 8)

### Slide 36 — Tablero de decisión (5 min)
Si duele… | Empieza por…
---|---
CI rojo por flake | bajar flake rate
Bugs en prod | leakage + alcance por riesgo
Modelo injusto | fairness + datos
Proceso manual frágil | RPA de validación
Nadie sabe el estado | dashboard de gobernanza

### Slide 37 — Consolidación Reto 1 + Reto 2 (5 min)
- Reto 1: calidad del sistema de pruebas (observable)
- Reto 2: calidad de datos y modelo (validada en CI)
- Juntos: gobernanza de punta a punta

### Slide 38 — Casos y dudas (8 min)
- Discutir situaciones reales del grupo
- Resolver dudas de conceptos
- Regla: toda respuesta anclada a métrica, política o evidencia

### Slide 39 — Checklist final del curso (3 min)
- [ ] Sé explicar flake, leakage y effectiveness
- [ ] Levanté el dashboard QA
- [ ] Corrí el lab de datos/ML
- [ ] Ubico RPA, simulación y gamificación en la estrategia
- [ ] Relaciono todo con un nivel TMMi

### Slide 40 — Cierre y siguientes pasos (3 min)
- Lleven un umbral y un dueño a su trabajo el lunes
- Publiquen al menos una métrica donde todo el equipo la vea
- Madurez no es un certificado: es un hábito medible

### Slide 41 — Gracias
**Título:** Certificación 6 — cierre
- Materiales en `curso6/dia2/`
- Proyecto en `proyectos/ml-data-quality-lab`
- ¡A gobernar con evidencia!

