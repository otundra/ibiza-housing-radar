---
description: Arranque ligero de sesión — panorámica de dónde estamos y qué no tocar (Tier 1, default)
---

Estás arrancando sesión en `ibiza-housing-radar`. Objetivo: sintetizar el estado del proyecto lo suficiente para trabajar con criterio, sin escanear nada más. Si al terminar la síntesis detectas que la tarea del editor pide más contexto, dilo y sugiere `/arranque-fase` o `/arranque-auditoria` antes de ejecutar.

## 1. Lectura en paralelo

En un solo mensaje, lanza Read a:

- [`STATUS.md`](../../STATUS.md) — completo (siempre ≤ 100 líneas por regla dura D0).
- [`DECISIONES.md`](../../DECISIONES.md) — completo.
- [`DIARIO.md`](../../DIARIO.md) — primeras 120 líneas (las más recientes; el diario va con lo nuevo arriba).

No leas nada más en este comando.

## 2. Síntesis al editor

Formato viñetas, sin adornos, máximo 200 palabras. Estructura:

- **Dónde estamos:** 1-2 frases (hito activo + fase).
- **Activo / en curso / pausado:** bullets con lo que refleja STATUS.
- **Últimos 3-5 cambios del diario:** una línea por entrada, con fecha y tema.
- **Decisiones que acotan trabajo inminente:** ID + título corto, solo si tocan.
- **Qué NO tocar:** pausas explícitas + reglas duras vigentes que limitan la sesión.
- **Señales ambiguas:** si STATUS, DIARIO y DECISIONES se contradicen, o hay algo abierto sin dueño claro, dilo en una línea.

## 3. Cierre

Pregunta al editor: *"¿Qué vamos a hacer en esta sesión?"* — no propongas tú la agenda. Con esa respuesta ya tienes criterio para decidir si la tarea cabe en Tier 1 o si conviene escalar.

## Cuándo escalar

Si el editor contesta con algo que toca:

- **Cambio de fase, arquitectura, estudio grande, o refactor del pipeline** → sugiere `/arranque-fase` antes de ejecutar.
- **Auditoría estructural, decisión de pivote, o bloqueo por falta de mapa mental global** → sugiere `/arranque-auditoria`.
- **Resto** → sigue con lo que hay, ya es suficiente.

## Regla dura

No edites nada durante este comando. Es un arranque de contexto, no una sesión de trabajo. Las ediciones empiezan después de que el editor diga qué quiere hacer.
