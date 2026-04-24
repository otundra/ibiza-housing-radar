---
description: Arranque completo — escaneo profundo para auditoría, refactor grande o desbloqueo (Tier 3, uso escaso)
---

Estás arrancando sesión en `ibiza-housing-radar` con escaneo completo. Usa este comando solo cuando:

- Auditoría estructural del proyecto (tipo la Revisión Fase 0.5 abierta el 21 de abril).
- Refactor grande del pipeline o de la web.
- El editor está bloqueado por falta de mapa mental global.
- Decisión de pivote o replanteo del producto.

Este comando consume mucho contexto (aprox. 15-20 mil tokens de lectura). No lo uses si `/arranque-fase` basta. Si no estás seguro, pregunta al editor antes de lanzarlo.

## 1. Capa base + fase (igual que `/arranque-fase`)

Ejecuta los pasos 1 y 2 de `/arranque-fase`: STATUS, DECISIONES, DIARIO, PLAN, ARQUITECTURA.

## 2. Capa fundacional

En paralelo:

- [`PIVOTE.md`](../../PIVOTE.md) — cinco reglas duras + decisión fundacional del modelo documental.
- [`DISENO-WEB.md`](../../DISENO-WEB.md) — UX dual (primer visitante + profesional recurrente).
- [`SEO.md`](../../SEO.md) — plan SEO.
- [`CONTENIDO-RETROACTIVO.md`](../../CONTENIDO-RETROACTIVO.md) — ediciones retroactivas bajo modelo documental.
- [`REVISION-FASE-0.5.md`](../../REVISION-FASE-0.5.md) — auditoría fundacional abierta.

## 3. Todos los estudios activos

En paralelo:

- [`ESTUDIO-DISENO.md`](../../ESTUDIO-DISENO.md) — sistema visual y 13 decisiones cerradas de diseño.
- [`ESTUDIO-TIERS.md`](../../ESTUDIO-TIERS.md) — re-estudio del sistema de tiers de confianza.
- [`ESTUDIO-COSTES-AUDITOR.md`](../../ESTUDIO-COSTES-AUDITOR.md) — costes del auditor IA de 5 capas.
- [`ESTUDIO-3-MODELOS.md`](../../ESTUDIO-3-MODELOS.md) — reparto Haiku / Sonnet / Opus por fase.
- [`ESTUDIO-GESTION-CONOCIMIENTO.md`](../../ESTUDIO-GESTION-CONOCIMIENTO.md) — gestión documental del proyecto.

## 4. Código del pipeline (si la auditoría lo toca)

Solo si la tarea entra en el pipeline Python, lee en paralelo los módulos principales:

- `src/report.py` — orquestador end-to-end.
- `src/classify.py` — clasificación de noticias.
- `src/extract.py` — ficha estructurada por propuesta.
- `src/verify.py` — verificación de URLs y trazabilidad de actores.
- `src/balance.py` — reparto de actores y bloques temporales.
- `src/costs.py` — tracking y topes de coste.

Si la tarea entra en la web, abre en su lugar `docs/_layouts/`, `docs/_includes/`, `docs/assets/css/main.css`.

Si la tarea es de auditoría documental sin tocar código, sáltate este paso.

## 5. Síntesis al editor

Formato más ampliado. Estructura:

- **Resumen ejecutivo** (5 líneas): qué es el proyecto hoy, dónde está en el ciclo editorial, qué bloquea qué.
- **Mapa de estudios:** tabla con columnas `Estudio · Estado · Decisiones cerradas · Preguntas abiertas`. En cada celda, nombre de la cosa primero; los códigos internos solo al final entre paréntesis y solo si aportan.
- **Decisiones vivas y tensiones:** decisiones del registro que podrían chocar entre sí o con la auditoría que vamos a hacer. Citar por nombre, no por código suelto.
- **Riesgos y deudas:** lo que el editor ha señalado como frágil, pospuesto o sin dueño.
- **Qué NO tocar:** reglas duras del proyecto + pausas + decisiones cerradas que acotan el trabajo.

Longitud objetivo: 600-900 palabras. Es una sesión pesada; el editor espera un mapa real.

## 6. Recomendaciones (1-3, según haya)

Con el mapa completo delante, ofrece **1 a 3 recomendaciones** de alcance o enfoque para la auditoría antes de la pregunta de cierre. A este nivel las recomendaciones pueden ser de tipo más estratégico (*"arrancar por la capa fundacional", "revisar primero las tensiones entre decisiones cerradas", "priorizar el módulo X por ser el más frágil"*).

Mismas reglas de redacción: una línea por recomendación, nombre de la cosa primero, verbo de acción + por qué corto.

## 7. Cierre

Pregunta al editor el alcance exacto de la auditoría. Con todo el contexto y las recomendaciones delante, afina antes de proponer cambios y antes de tocar nada.

## Regla dura

No edites nada durante este comando. Bajo ningún concepto. La auditoría se diseña después de la síntesis, no durante la lectura.
