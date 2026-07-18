"""One-shot helper: split mixed curso6 materials into dia1/ and dia2/."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def split_ppt() -> None:
    ppt = (ROOT / "ppt_contenido.md").read_text(encoding="utf-8")
    marker = "## DÍA 2 — IA, datos, RPA y madurez"
    idx = ppt.index(marker)
    d1_start = ppt.index("## DÍA 1 — Gobernanza, métricas y dashboards")
    d1_content = ppt[d1_start:idx].rstrip() + "\n"
    d2_body = ppt[idx + len(marker) :].lstrip()

    def renumber(match: re.Match[str]) -> str:
        n = int(match.group(1))
        return f"### Slide {n - 44} —"

    d2_body = re.sub(r"### Slide (\d+) —", renumber, d2_body)
    d2_body = d2_body.replace(
        "curso6/proyectos/ml-data-quality-lab", "proyectos/ml-data-quality-lab"
    )
    d2_body = d2_body.replace(
        "Carpeta: `curso6/proyectos/ml-data-quality-lab`",
        "Carpeta: `proyectos/ml-data-quality-lab`",
    )

    ppt_d1 = f"""# Certificación 6 — Día 1 · Contenido de diapositivas
## Madurez, Gobernanza y Estrategia de Calidad Organizacional

> 4 horas · Bloques de 45 min + descansos de 15 min
> Slides 1–44 · Proyecto: `proyectos/qa-governance-dashboard`

---

{d1_content}
"""
    ppt_d1 = ppt_d1.replace(
        "curso6/proyectos/qa-governance-dashboard", "proyectos/qa-governance-dashboard"
    )
    ppt_d1 = ppt_d1.replace(
        "cd curso6/proyectos/qa-governance-dashboard",
        "cd proyectos/qa-governance-dashboard",
    )

    ppt_d2 = f"""# Certificación 6 — Día 2 · Contenido de diapositivas
## Madurez, Gobernanza y Estrategia de Calidad Organizacional

> 4 horas · Bloques de 45 min + descansos de 15 min
> Slides 1–41 · Proyecto: `proyectos/ml-data-quality-lab`

---

## Día 2 — IA, datos, RPA y madurez

{d2_body}
"""
    # Day 2 block labels: Bloque 5-8 -> Bloque 1-4 for standalone day
    replacements = [
        ("Bloque 5:", "Bloque 1:"),
        ("Bloque 6:", "Bloque 2:"),
        ("Bloque 7:", "Bloque 3:"),
        ("Bloque 8:", "Bloque 4:"),
        ("Cierre Bloque 5", "Cierre Bloque 1"),
        ("Cierre Bloque 7", "Cierre Bloque 3"),
        ("Volvemos · Bloque 6", "Volvemos · Bloque 2"),
        ("Volvemos · Bloque 7", "Volvemos · Bloque 3"),
        ("Volvemos · Bloque 8", "Volvemos · Bloque 4"),
    ]
    for old, new in replacements:
        ppt_d2 = ppt_d2.replace(old, new)

    (ROOT / "dia1" / "ppt_contenido.md").write_text(ppt_d1, encoding="utf-8")
    (ROOT / "dia2" / "ppt_contenido.md").write_text(ppt_d2, encoding="utf-8")
    print(
        "PPT:",
        len(re.findall(r"^### Slide ", ppt_d1, re.M)),
        "+",
        len(re.findall(r"^### Slide ", ppt_d2, re.M)),
    )


def split_guide() -> None:
    guide = (ROOT / "instructor_guide.md").read_text(encoding="utf-8")
    d1_start = guide.index("# DÍA 1")
    d2_start = guide.index("# DÍA 2")
    shared_header = guide[:d1_start]
    d1_body = guide[d1_start:d2_start].rstrip() + "\n"
    d2_body = guide[d2_start:].rstrip() + "\n"

    # Extract imprevistos from end of day2 if present
    imprevistos = ""
    if "## Imprevistos frecuentes" in d2_body:
        split_at = d2_body.index("## Imprevistos frecuentes")
        imprevistos = d2_body[split_at:]
        d2_body = d2_body[:split_at].rstrip() + "\n"

    guide_d1 = f"""# Guía del Instructor — Certificación 6 · Día 1
## Madurez, Gobernanza y Estrategia de Calidad Organizacional

> Guion para impartición **virtual (online)**. Texto pensado para leerse en voz alta.
> Marcas: `[SLIDE N]` · `[PAUSA]` · `[PREGUNTA]` · `[DEMO]` · `[COMPARTIR PANTALLA]` · `[CHAT]`

**Duración:** 4 horas · bloques de 45 min + descansos de 15 min
**Materiales:** `ppt_contenido.md` / `dia1.pptx` · `proyectos/qa-governance-dashboard`

---

## Checklist de preparación (30 min antes)

1. Abrir `dia1.pptx` en modo presentación.
2. Tener Docker Desktop **Running** y el Reto 1 levantado:
   ```bash
   cd proyectos/qa-governance-dashboard
   docker compose up -d --build
   ```
   Validar: `http://localhost:8000/metrics` · `http://localhost:9090` · `http://localhost:3000`
3. Enlaces listos en un bloc de notas para pegar en el chat.
4. Plan B: si Docker falla en la sala, vos compartís el stack ya levantado; los alumnos observan y anotan interpretaciones.

**Tono general:** conversacional, cercano, con energía. Evitá leer tablas enteras: apuntá y contá la historia.

---

{d1_body}
"""
    # Day1 path fixes
    guide_d1 = guide_d1.replace(
        "cd curso6/proyectos/qa-governance-dashboard",
        "cd proyectos/qa-governance-dashboard",
    )
    guide_d1 = guide_d1.replace("# DÍA 1\n\n", "")

    # Append day1-relevant imprevistos
    guide_d1 += """
---

## Imprevistos frecuentes (Día 1)

| Síntoma | Acción |
|---|---|
| Docker Desktop no corre | Plan B: demo del instructor + interpretación de paneles |
| Puerto ocupado | Cambiar mapeo izquierdo en `docker-compose.yml` |
| Grafana vacío al inicio | Esperar ~30 s a que provisione el datasource |

## Recordatorios de facilitación online

- Pegá comandos en el chat **antes** de pedir que los corran.
- Cada 10–12 minutos: una pregunta corta para recuperar atención.
- Los silencios de 3 segundos después de una pregunta son productivos.
"""

    # Renumber day 2 slides in guide: 45->1 ... and rewrite block numbers
    def renumber_slide_refs(text: str) -> str:
        def repl_range(m: re.Match[str]) -> str:
            a, b = int(m.group(1)), int(m.group(2))
            return f"[SLIDE {a - 44}–{b - 44}]"

        def repl_one(m: re.Match[str]) -> str:
            n = int(m.group(1))
            return f"[SLIDE {n - 44}]"

        text = re.sub(r"\[SLIDE (\d+)–(\d+)\]", repl_range, text)
        text = re.sub(r"\[SLIDE (\d+)\]", repl_one, text)
        text = re.sub(r"Slides (\d+)–(\d+)", lambda m: f"Slides {int(m.group(1))-44}–{int(m.group(2))-44}", text)
        return text

    d2_body = renumber_slide_refs(d2_body)
    d2_body = d2_body.replace("# DÍA 2\n\n", "")
    d2_body = d2_body.replace("BLOQUE 5", "BLOQUE 1")
    d2_body = d2_body.replace("BLOQUE 6", "BLOQUE 2")
    d2_body = d2_body.replace("BLOQUE 7", "BLOQUE 3")
    d2_body = d2_body.replace("BLOQUE 8", "BLOQUE 4")
    d2_body = d2_body.replace("DESCANSO 4", "DESCANSO 1")
    d2_body = d2_body.replace("DESCANSO 5", "DESCANSO 2")
    d2_body = d2_body.replace("DESCANSO 6", "DESCANSO 3")
    d2_body = d2_body.replace(
        "cd curso6/proyectos/ml-data-quality-lab",
        "cd proyectos/ml-data-quality-lab",
    )
    d2_body = d2_body.replace(
        "curso6/proyectos/ml-data-quality-lab",
        "proyectos/ml-data-quality-lab",
    )

    guide_d2 = f"""# Guía del Instructor — Certificación 6 · Día 2
## Madurez, Gobernanza y Estrategia de Calidad Organizacional

> Guion para impartición **virtual (online)**. Texto pensado para leerse en voz alta.
> Marcas: `[SLIDE N]` · `[PAUSA]` · `[PREGUNTA]` · `[DEMO]` · `[COMPARTIR PANTALLA]` · `[CHAT]`

**Duración:** 4 horas · bloques de 45 min + descansos de 15 min
**Materiales:** `ppt_contenido.md` / `dia2.pptx` · `proyectos/ml-data-quality-lab`

---

## Checklist de preparación (30 min antes)

1. Abrir `dia2.pptx` en modo presentación.
2. Tener el Reto 2 sincronizado y en verde:
   ```bash
   cd proyectos/ml-data-quality-lab
   uv sync
   uv run pytest -v
   ```
   Esperado: `5 passed`.
3. Enlaces y comandos listos para pegar en el chat.
4. Este día es autónomo: no requiere tener el stack Docker del Día 1 levantado.

**Tono general:** conversacional, cercano, con energía. Evitá leer tablas enteras: apuntá y contá la historia.

---

{d2_body}
"""
    if imprevistos:
        # keep only ML-relevant rows + facilitation
        guide_d2 += "\n---\n\n" + imprevistos.replace(
            "| Docker Desktop no corre | Plan B: demo del instructor + interpretación de paneles |\n",
            "",
        ).replace(
            "| Puerto ocupado | Cambiar mapeo izquierdo en `docker-compose.yml` |\n",
            "",
        ).replace(
            "| Grafana vacío al inicio | Esperar ~30 s a que provisione el datasource |\n",
            "",
        )

    (ROOT / "dia1" / "instructor_guide.md").write_text(guide_d1, encoding="utf-8")
    (ROOT / "dia2" / "instructor_guide.md").write_text(guide_d2, encoding="utf-8")
    print("Guides written")


if __name__ == "__main__":
    split_ppt()
    split_guide()
