---
description: Carga contexto adicional de un área concreta sin sacar informe. Usable tras cualquier arranque para subir de nivel sin repetir síntesis.
---

El editor quiere cargar más contexto sobre un área concreta del proyecto, sin informe. El argumento tras el comando dice qué cargar.

Dos formas de uso:

- **Palabra clave corta:** `/ampliar diseño`, `/ampliar auditor`, `/ampliar tiers`. Mapea a los documentos de la tabla de abajo.
- **Descripción libre:** `/ampliar quiero tocar el tema de costes y las decisiones legales`. Interpreta la frase y elige qué leer.

## Palabras clave conocidas

| Palabra clave | Documentos que lee |
|---|---|
| `diseno` / `diseño` / `visual` | [`ESTUDIO-DISENO.md`](../../ESTUDIO-DISENO.md), [`DISENO-WEB.md`](../../DISENO-WEB.md) |
| `auditor` | [`ESTUDIO-COSTES-AUDITOR.md`](../../ESTUDIO-COSTES-AUDITOR.md) |
| `tiers` / `niveles` / `confianza` | [`ESTUDIO-TIERS.md`](../../ESTUDIO-TIERS.md) |
| `costes` / `coste` | [`ESTUDIO-COSTES-AUDITOR.md`](../../ESTUDIO-COSTES-AUDITOR.md), [`private/costs.md`](../../private/costs.md) |
| `pipeline` / `flujo` / `codigo` | [`ARQUITECTURA.md`](../../ARQUITECTURA.md) + archivos principales de `src/` (`report.py`, `classify.py`, `extract.py`, `verify.py`, `balance.py`) |
| `legal` / `titular` | sección legal de [`REVISION-FASE-0.5.md`](../../REVISION-FASE-0.5.md) + decisiones con tema `legal` en [`DECISIONES.md`](../../DECISIONES.md) |
| `contenido` / `editorial` / `retroactivo` | [`CONTENIDO-RETROACTIVO.md`](../../CONTENIDO-RETROACTIVO.md) |
| `seo` | [`SEO.md`](../../SEO.md) |
| `modelos` / `ia` | [`ESTUDIO-3-MODELOS.md`](../../ESTUDIO-3-MODELOS.md) |
| `docs` / `gestion` / `documental` | [`ESTUDIO-GESTION-CONOCIMIENTO.md`](../../ESTUDIO-GESTION-CONOCIMIENTO.md) |
| `auditoria` / `revision` / `fase 0.5` | [`REVISION-FASE-0.5.md`](../../REVISION-FASE-0.5.md) |
| `web` / `jekyll` / `prototipo` | `docs/_layouts/`, `docs/_includes/`, `docs/assets/css/main.css`, `docs/prototype/*.html` |

## Descripción libre

Si el argumento tras el comando no cuadra con una palabra clave, interpreta la frase y lanza Read de los documentos más pertinentes. Si hay ambigüedad real, **pregunta qué cargar antes de leer** — no improvises.

## Salida al editor

Una línea confirmando qué acabas de leer. Sin informe, sin síntesis, sin recomendaciones.

Ejemplo: *"Cargado: estudio de niveles de confianza + última entrada del diario sobre eso. Sigo."*

Después, responde al prompt del editor con el contexto ya ampliado.

## Regla dura

- **No sacar informe.** Este comando no genera síntesis, resumen ni recomendaciones. Solo confirma carga y sigue.
- **Ante ambigüedad, pregunta.** Si la palabra clave no cuadra y la descripción libre es vaga, pide aclaración antes de leer.
- **Al final, solo confirmas qué leíste y pasas a atender la tarea** del editor con el contexto nuevo ya dentro.
