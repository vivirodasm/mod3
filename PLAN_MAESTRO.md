# Plan Maestro — Certificación 3: Ingeniería de Automatización: APIs, Performance y Seguridad

> **Duración total:** 29 horas — 9 sesiones de 3h + 1 sesión final de 2h.
> **Ritmo:** 80% práctica, 20% teoría. Todo el código del curso es claro, mantenible y revisable: nombres explícitos, datos separados de la lógica, versionado en Git y revisión mediante Pull Request.
> **Para quién es:** es un curso que se explica solo — parte desde cero y no depende de ningún proyecto externo.

---

## 1. Qué vas a aprender

1. Diseñar tests robustos y mantenibles usando patrones como **Page Object Model** y técnicas de diseño basadas en requisitos y cobertura real.
2. Automatizar **interfaces de programación de aplicaciones** (*Application Programming Interface*, API), pruebas no funcionales y flujos de **integración y entrega continuas** (*Continuous Integration/Continuous Delivery*, CI/CD) con herramientas como Postman, K6, REST-assured, Jenkins y Docker.
3. Mantener y escalar suites de pruebas: gestión de datos, versionado y eliminación de tests frágiles que se rompen solos.

---

## 2. Stack del curso

| Dominio | Herramientas | Uso en el curso |
|---|---|---|
| Diseño de pruebas | Partición de equivalencias (*Equivalence Partitioning*, EP), análisis de valores límite (*Boundary Value Analysis*, BVA), tablas de decisión y pruebas combinatorias | Matriz de trazabilidad + laboratorios ejecutables |
| Scripts / Patrones | Page Object Model (POM), Screenplay, Don't Repeat Yourself (DRY) · Lenguajes: Java, Python, JavaScript, C# | Laboratorios con Python como lenguaje base; ejemplos comparados en los 4 lenguajes |
| Datos externos | JSON (*JavaScript Object Notation*), YAML (*YAML Ain't Markup Language*), CSV (*Comma-Separated Values*), bases de datos y mocks | Capa de datos desacoplada de la lógica de pruebas |
| APIs | Postman (colecciones) + Newman/Postman CLI · Python: httpx + pytest · Referencia para ecosistema Java: REST-assured, Karate DSL · Contratos: JSON Schema (con mención de Pact) | APIs públicas de práctica |
| CI/CD | GitHub Actions, Jenkins, GitLab CI, Azure Pipelines · Docker (Selenium Grid, Playwright, Cypress) | Flujo automatizado del proyecto integrador con disparadores por push, Pull Request y ejecución nocturna |
| Performance | K6, JMeter (+ Gatling vía Karate) | Scripts de carga como infraestructura como código |
| Seguridad | OWASP ZAP (*Open Worldwide Application Security Project Zed Attack Proxy*), Burp Suite | Escaneo automatizado de seguridad base |
| Accesibilidad | Axe, Lighthouse, WCAG (*Web Content Accessibility Guidelines*) | Auditorías automatizadas de accesibilidad |
| Compatibilidad | BrowserStack, SauceLabs, LambdaTest | Matriz de compatibilidad entre navegadores (cuentas gratuitas o demos) |
| Móvil / Escritorio | Appium, Maestro, Espresso, XCUITest, FlaUI, Pywinauto | Labs en emulador + estrategia emulador vs dispositivo real |
| Regresión visual | Applitools, Percy, Chromatic · comparación visual nativa de Playwright (`toHaveScreenshot`) | Línea base visual + comparación asistida por IA, diseño responsivo y modo oscuro |
| Mantenimiento | Healenium (autorreparación o *auto-healing*) + reparación de selectores asistida por IA generativa · Stryker JavaScript/TypeScript, PIT (Java), mutmut (Python) — pruebas de mutación (*Mutation Testing*) | Reducción de pruebas inestables + calidad del conjunto de pruebas más allá de la cobertura |
| Tooling base | — | `uv` (Python), `pnpm` (JS), `Taskfile`, `Git`, `Docker` como herramientas de ejecución y estandarización |

**Sobre qué practicamos:** aplicaciones públicas de práctica — **SauceDemo** (https://www.saucedemo.com) para todo lo relacionado con interfaz de usuario, y APIs públicas de entrenamiento para los ejercicios de servicios.

> **Herramientas del temario original actualizadas a 2026:**
> - **CrossBrowserTesting** → discontinuado por SmartBear en julio 2023; lo sustituye **LambdaTest** (mismo rol, adopción vigente).
> - **Recheck** → sin mantenimiento activo; lo sustituye la **comparación visual nativa de Playwright**, que ya usamos en el stack.
> - **Testim** → hoy es Tricentis Testim (comercial); se menciona como referencia y el lab usa **Healenium** (open source) + un demo de reparación de selectores con IA generativa.
> - **Newman** → sigue vigente y es el que usamos (no requiere cuenta); se menciona **Postman CLI** como su sucesor oficial.
> - **REST-assured y Karate DSL** → vigentes y mantenidos, pero atados a la JVM (Java + Maven/Gradle); el curso es Python-first y cubre los mismos conceptos (validaciones, contratos, data-driven, paralelo) con **pytest + httpx**. Se presentan como referencia para quien trabaje en ecosistema Java.
> - **Pact** → el *contract testing* se enseña como concepto con JSON Schema (S3) y contratos en código (S4); Pact se menciona como la herramienta profesional consumidor/proveedor.
> - Se agregan **Maestro** (móvil, estándar emergente) y **mutmut** (mutación en Python, coherente con los labs del curso).

---

## 3. El proyecto integrador — "Puerta de Calidad de Release" (*QA Release Gate*)

Sesión a sesión construimos un **flujo automatizado de control de calidad** sobre aplicaciones públicas. Al terminar el curso, ese flujo corre completo con un solo disparo:

```
                         ┌────────────────────────────────────────────────┐
                         │       PUERTA DE CALIDAD DE RELEASE (CI/CD)     │
  Pull Request ──────►   │                                                │
  Push         ──────►   │  Etapa 1: Lint + diseño y trazabilidad         │
  Nocturno     ──────►   │  Etapa 2: Pruebas de API (Postman + Karate)    │
                         │  Etapa 3: Pruebas de contrato (Pact)           │
                         │  Etapa 4: Pruebas básicas de UI (POM + Docker) │
                         │  Etapa 5: Performance (umbrales con K6)        │
                         │  Etapa 6: Seguridad (escaneo base con ZAP)      │
                         │  Etapa 7: Accesibilidad + visual               │
                         │  Etapa 8: Criterios de calidad del conjunto    │
                         └───────────────┬────────────────────────────────┘
                                         │
                                         ▼
                      Reportes HTML + matriz de trazabilidad
```

Cada sesión agrega una etapa al flujo. Al terminar la Sesión 10, todo corre en Jenkins **y** en GitHub Actions.
Los **retos del curso** se integran directamente al proyecto: Reto 1 (Jenkins + Postman + K6) en las Sesiones 5-6; Reto 2 (OWASP ZAP) en la Sesión 7.

---

## 4. Cronograma — las 10 sesiones

| # | Duración | Tema | Entregable del Proyecto Integrador |
|---|---|---|---|
| **S1** ✅ | 3h | **Diseño técnico de pruebas:** partición de equivalencias, valores límite, tablas de decisión, combinatorias · Mantenibilidad (reusabilidad, desacoplamiento, modulación) · Matriz de trazabilidad | Laboratorio de diseño ejecutable + matriz de trazabilidad inicial Requerimientos↔Casos↔Defectos |
| **S2** ✅ | 3h | **Desarrollo de scripts:** Page Object Model (POM), Screenplay, Don't Repeat Yourself (DRY) · datos/estados de prueba compartidos (*fixtures*), aserciones (*assertions*), manejo de errores, validaciones dinámicas · Datos externos: JSON/YAML/CSV/bases de datos/mocks · Lenguajes: Java, Python, JavaScript, C# | Conjunto base de pruebas de interfaz de usuario con POM + capa de datos externa desacoplada |
| **S3** | 3h | **APIs y servicios web I:** REST (*Representational State Transfer*) vs SOAP (*Simple Object Access Protocol*) vs GraphQL · Postman (colecciones) + Newman (con mención de Postman CLI, su sucesor oficial) · Validaciones: status, headers, payloads, esquemas JSON/XML (*Extensible Markup Language*) | Colección Postman versionada + Newman en Taskfile (Etapa 2a) |
| **S4** | 3h | **APIs II — automatización con Python:** cliente httpx con KISS · pytest + fixtures (DRY) · Data-Driven con JSON/YAML · contratos de API en código · Referencia: REST-assured y Karate DSL (*Domain-Specific Language*) para ecosistema Java · concepto de contratos consumidor/proveedor (Pact) | Suite pytest de APIs con cliente propio, fixtures y data-driven (Etapas 2b y 3) |
| **S5** | 3h | **CI/CD:** GitHub Actions, Jenkins, GitLab CI, Azure Pipelines · disparadores por push, Pull Request y ejecución nocturna · Docker: Selenium Grid, Playwright, Cypress · **Inicio Reto 1** | Jenkinsfile + flujo de GitHub Actions con etapas 1-4 en contenedores |
| **S6** | 3h | **Performance:** K6 como infraestructura como código (*Infrastructure as Code*, IaC) y JMeter · umbrales (*thresholds*), escenarios de carga · Karate+Gatling · **Cierre Reto 1** (Jenkins + Postman + K6) | Etapa 5 con umbrales de performance como criterio de aprobación — **Reto 1 entregado** |
| **S7** | 3h | **Seguridad y otras no funcionales:** OWASP ZAP (escaneo base automatizado), Burp Suite · Axe/Lighthouse (WCAG) · Compatibilidad (BrowserStack/SauceLabs/LambdaTest) · **Reto 2** | Etapas 6-7: ZAP + Axe en flujo automatizado — **Reto 2 entregado** |
| **S8** | 3h | **Mantenimiento:** reducción de pruebas inestables, refactorización, anotaciones condicionales, separación lógica/datos, versionado y trazabilidad · **Autorreparación** (*auto-healing*) con Healenium + reparación de selectores con IA generativa · **Pruebas de mutación** (*Mutation Testing*) con Stryker JavaScript/TypeScript, PIT (Java) y mutmut (Python) | Etapa 8: criterio de puntaje de mutación (*mutation score*) + demo de autorreparación |
| **S9** | 3h | **Móviles y escritorio:** Appium, Maestro, Espresso, XCUITest, FlaUI, Pywinauto · híbrido vs nativo · emuladores vs dispositivos reales · **Regresión visual:** línea base visual + IA (Applitools/Percy + Playwright nativo), diseño responsivo, media queries y modo oscuro | Pruebas móviles básicas (*smoke*) con Appium + validación visual en el flujo automatizado |
| **S10** | 2h | **Cierre:** integración final del flujo automatizado, demo end-to-end, revisión de retos, resolución de dudas y evaluación de conocimientos | **Puerta de Calidad de Release** completa funcionando + retrospectiva |

**Total: 9×3h + 1×2h = 29 horas.**

---

## 5. Cómo está organizada cada sesión de 3h

```
Bloque A (45 min) → Problema real + conceptos mínimos + demo paso a paso
   ── descanso 15 min ──
Bloque B (45 min) → Laboratorio guiado con práctica directa en código
   ── descanso 15 min ──
Bloque C (45 min) → Ejercicio individual + Mini reto + errores comunes / código limpio → salida
```

## 6. Estructura de carpetas del repo

```
curso-automatizacion-apis-performance-seguridad/
├── PLAN_MAESTRO.md            ← este documento
├── SETUP_ESTUDIANTES.md       ← guía de instalación para estudiantes
├── proyecto-integrador/       ← Puerta de Calidad de Release (crece cada sesión)
│   ├── trazabilidad/          ← matriz de trazabilidad (S1)
│   ├── api-tests/             ← Postman/Newman, Karate, Pact (S3-S4)
│   ├── performance/           ← scripts K6 (S6)
│   ├── security/              ← config OWASP ZAP (S7)
│   └── flujos-ci/             ← Jenkinsfile + flujos automatizados (S5+)
└── retos/                     ← Reto 1 y Reto 2 (enunciado + solución)
```

## 7. Evaluación y metodología

- Discusión de casos reales en cada sesión — no hay teoría suelta sin contexto.
- Entrega de los **Retos 1 y 2** como hitos obligatorios del programa.
- Espacio al final de cada sesión para resolver dudas sobre lo visto.
