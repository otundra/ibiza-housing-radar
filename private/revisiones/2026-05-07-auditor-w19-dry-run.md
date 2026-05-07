# Revisión 2026-05-07 — Auditor W19, dry-run de los criterios de cierre del Hito 1

- **Fecha:** 2026-05-07
- **Disparador:** Lectura proactiva durante `/arranque-auditoria`. La rec 1 del informe (cerrar Hito 1 antes de mover otra cosa) bajó a auditar lo que ya hay acumulado de W19, en vez de esperar 3 lunes a que llegue toda la muestra W19-W22.
- **Edición revisada:** [/ediciones/2026-w19/](../../docs/_editions/2026-w19.md) — solo el bloque del auditor (`data/audit/2026-w19/`).
- **Modelo activo durante la sesión:** opus + xhigh

## Resumen ejecutivo

Auditoría en frío de la única propuesta auditada en W19 (Govern Balear, 25M€). Cuatro hallazgos: dos son **comportamiento de diseño del MVP mal observable** (no son bugs, pero el lector del log no los distingue de fallos), uno es **bug real del comparador determinista** que mete falsos positivos en la métrica clave de la calibración, y el cuarto es **apunte para PI10** (la propuesta saldría de la edición cuando el cálculo de niveles real esté conectado). De los cuatro, solo se aplica el cosmético hoy: marcar explícitamente en el log de auditoría qué campos están diferidos al MVP. Los otros dos quedan apuntados con propuesta concreta para sesiones específicas. La medición formal de los seis criterios del cierre del Hito 1 (§10 del plano) sigue pendiente — la haremos sobre la muestra acumulada tras W22, no ahora con n=1.

## Diagnóstico de la edición

Aplicación en frío de los seis criterios de cierre del Hito 1 ([DISENO-AUDITOR-MVP.md §10](../../DISENO-AUDITOR-MVP.md)) sobre el archivo `data/audit/2026-w19/2026-w19-001.json`:

| Criterio | Estado | Comentario |
|---|---|---|
| 1. Log JSON escrito sin errores bloqueantes | ✅ | Archivo bien formado, todos los bloques presentes. |
| 2. Las 11 señales pobladas | ⚠️ 9/11 con valor real, 2 (`fecha_coherente`, `wayback_snapshot`) en `null` por diseño del MVP. La docstring del módulo lo declara, pero el log no lo distingue de un fallo de heurística. |
| 3. Ratio de disputas dentro del rango saludable (5-30%) | n/a | Con n=1 propuesta auditada en toda la edición, el ratio no es interpretable. La propuesta está marcada `severity: critical` por una sola diferencia entre Haiku y Sonnet — pero la diferencia es sinonimia (`Municipios` vs `Ayuntamientos`). |
| 4. Coste por edición auditada bajo 0,50 € | ✅ | Bloque "auditor puro" (Sonnet ciega + heurísticas) suma ~0,01 €. La edición completa cuesta 0,60 €, dominado por `generate` Opus y por un `extract_fallback` Opus que se disparó esta semana. |
| 5. Heurísticas no fallan silenciosamente | ⚠️ | Las heurísticas IA (verbatim, whitelist) reportan `error: null` explícitamente. El bloque `verify` del log devuelve tres campos en `null` sin marca de causa, lo que confunde "diferido al MVP" con "fallo de la heurística". |
| 6. Edición pública legible | ✅ | W19 publicada y servida sin problemas. |

Cuatro hallazgos identificados al cruzar el log con el código:

### Hallazgo 1 · `verify` por propuesta diferido al MVP, sin distinguir de fallo

`verify.py` corre cada lunes a nivel **edición markdown completa**, no por propuesta. La docstring de `_build_audit_record` en `src/audit.py` lo declara explícitamente (*"verify.py corre sobre la edición markdown completa, no por propuesta"*) y el plano §8 lo difiere a iteración posterior. Comportamiento correcto del MVP.

Lo que falla es la **observabilidad**: tres campos del bloque `verify` (`http_status`, `wayback_snapshot`, `fecha_coherente`) quedan en `null` sin marca de causa. Un lector futuro del log no puede decidir si está leyendo un MVP con verify diferido o un fallo silencioso de la heurística. Eso choca con el criterio 5 del §10.

### Hallazgo 2 · Comparador sin matching flexible — falso positivo crítico

El caso real de W19: Haiku extrajo `target_actor: "Municipios de Eivissa"`, Sonnet extrajo `"Ayuntamientos de Eivissa"`. El comparador hace `lower().strip()` y compara igualdad estricta (`src/audit_compare.py` función `_norm`). Las dos cadenas son distintas literal pero sinónimos exactos en este contexto. Resultado: `severity: critical`.

Impacto en la calibración del Hito 1: si W20-W22 trae 2-3 propuestas con sinónimos institucionales típicos del dominio (Govern / Govern Balear / GOIB; Consell / Consell d'Eivissa / Consell Insular; IBAVI / Institut Balear de l'Habitatge; Ajuntament / Ayuntamiento), cada caso infla el ratio de disputas. La métrica del criterio 3 saldría artificialmente alta y dispararía falsa alarma de "Haiku mal calibrado" cuando lo único que pasa es que dos modelos eligen sinónimos distintos.

### Hallazgo 3 · Capa 4 desacoplada — el evento Opus existe pero el log lo ignora

El registro de costes muestra que en W19 se disparó un `extract_fallback` con Opus (~0,067 USD), señal de que el validador corto Sonnet en `src/extract.py` rechazó la primera extracción Haiku. Pero el log del auditor sigue marcando `arbitraje: "no_hubo"`. El campo está hardcoded a esa cadena en `audit.py`.

Esto es **mezcla de diseño y bug**: la capa 4 formal está diferida al plano §8 (no es bug). Pero el evento Opus ya ocurre dentro de `src/extract.py::retry_with_opus` y hoy es invisible para `audit.py`. Sin esa señal, cuando el cálculo real de niveles se conecte (PI10), las decisiones automáticas se tomarán con información incompleta.

Cerrar bien el desacople requiere **propagar el `news_id` al `record_call` de `extract.py::retry_with_opus`** porque el CSV de costes hoy granulariza por edición, no por propuesta. Si una semana hubiera 3 propuestas y solo 1 disparara fallback, no podríamos saber cuál fue. Cambio en `extract.py`, no en `audit.py`.

### Hallazgo 4 · Esta propuesta saldría de la W19 cuando se conecte el cálculo de niveles

Apunte para PI10, no acción ahora. Las señales reales de la propuesta `2026-w19-001`:

- `n_fuentes_independientes: 1` → techo 🟡 según el árbol del estudio de niveles.
- `whitelist_match: "debilita"` (dominio msn.com, agregador) → otro techo 🟡.
- `verbatim_match_ratio: 0.026` → muy por debajo del mínimo bloqueante 0.60 para `reported`.

Hoy la propuesta entra a la edición porque el cálculo de niveles devuelve siempre `value: null` (stub). El día que PI10 conecte el cálculo real, esta clase de propuestas (cifras agregadas vía MSN sin fuente primaria localizada) van a cuarentena 🔴. La página `/propuestas/` perderá una entrada.

## Debate y alternativas

### ¿Aplicar fix de código del comparador antes del cron del lunes 11?

Primera idea: añadir matching difuso con `SequenceMatcher` ratio para el campo `target_actor`, threshold 0.85 para distinguir disputas reales de sinónimos. Recalibración tras hacer la cuenta:

> `SequenceMatcher("Municipios de Eivissa", "Ayuntamientos de Eivissa")` ≈ 0.49.

El threshold 0.85 deja el caso real fuera y sigue marcando `critical`. Bajar el threshold a 0.5 para que el caso entre traería falsos negativos en disputas reales (un actor confundido con otro tendría ratio 0.4-0.5 también).

La solución correcta no es ratio de caracteres: es **diccionario de sinónimos institucionales del dominio** (Municipios=Ayuntamientos, Govern=GOIB, Consell=Consell Insular, IBAVI=Institut Balear de l'Habitatge…). Eso pide diseño firme — qué entradas, cuándo se actualiza, cómo se versiona — que no cabe en un parche de 15 minutos antes del cron.

Decisión: **no aplicar fix incompleto**. Apuntar el bug con propuesta concreta para sesión específica. La medición del §10 tras W22 puede contar fácilmente cuántas disputas son sinonimia y cuántas son disputa real — la distinción es manual a la vista del log y tarda 5 minutos por propuesta.

### ¿Aplicar fix del desacople de capa 4 ahora?

Toca `src/extract.py` (módulo distinto del auditor) para propagar `news_id` al `record_call`. Cambio razonable pero amplía superficie a un módulo del pipeline crítico justo antes del cron del lunes. Riesgo de introducir regresión > beneficio del fix.

Decisión: **no tocar antes del lunes 11**. Apuntar para sesión específica que abra el plano §8 entero (capa 4 formal + cuarentena pública + dashboard `/auditor/` + capa 5bis IA, todo es iteración posterior coordinada).

### ¿Aplicar el fix cosmético del bloque verify?

Sí. Añadir un campo `_note` al bloque `verify` del log que explique en una frase que el verify por propuesta está diferido al MVP. Cambio retrocompatible (los consumidores futuros pueden ignorar `_note`), no toca tipos, no toca otros módulos. ~5 minutos. Aplicado hoy.

### ¿Documentar los cuatro hallazgos como narrativa o como tabla en APRENDIZAJES?

Los cuatro son hallazgos sobre **el sistema del auditor**, no sugerencias del revisor automático sobre la edición. APRENDIZAJES está pensado para sugerencias del self-review semanal con su ciclo de vida (pendiente → aplicada / descartada / en seguimiento). Mezclar aquí desbordaría la tabla.

Decisión: documentar los cuatro como narrativa en este archivo de revisión. Apuntar los dos que requieren código futuro (hallazgos 2 y 3) en sus tareas naturales del roadmap.

## Decisiones tomadas

| # | Decisión | Dónde queda registrada |
|---|---|---|
| 1 | Marcar explícitamente con campo `_note` los campos del bloque `verify` que están diferidos al MVP. Distinguir "diferido por diseño" de "fallo de heurística" en el log. | Cambio cosmético en `src/audit.py::_build_audit_record`. Sin D propia. Cubierto por D1 (auditor MVP). Commit de esta sesión. |
| 2 | Comparador determinista con falso positivo en sinónimos institucionales (`Municipios`/`Ayuntamientos`, `Govern`/`GOIB`, etc.) — apuntado como tarea separada con propuesta concreta: diccionario de sinónimos versus matching difuso. | Apunte en este archivo + sección de seguimiento del Hito 1. No se aplica fix antes del cron del lunes 11. |
| 3 | Capa 4 desacoplada del log del auditor (Opus fallback de `extract.py` invisible para `audit.py`) — apuntado como tarea de la iteración posterior del plano §8. Requiere propagar `news_id` al `record_call` de `extract.py::retry_with_opus`. | Apunte en este archivo + plano §8. |
| 4 | Esta clase de propuesta (msn.com agregador + verbatim ratio 0.026 + n=1) saldría a cuarentena cuando PI10 conecte el cálculo real de niveles. | Apunte para PI10 — al activarlo, contar cuántas propuestas históricas se mueven a `/revision-pendiente/` y comunicarlo en `/correcciones/` si corresponde. |
| 5 | Medición formal de los seis criterios de cierre del Hito 1 sigue diferida a tras W22. n=1 no es muestra. | Sin cambio respecto a [D20](../../DECISIONES.md). Acumular hasta el lunes 1 de junio. |

## Cambios aplicados

Un commit:

- (pendiente) — `chore(audit): marcar explícitamente campos del bloque verify diferidos al MVP`

Archivos tocados: `src/audit.py` (función `_build_audit_record`), `private/revisiones/2026-05-07-auditor-w19-dry-run.md` (este archivo), `REVISIONES.md` (entrada nueva en el índice).

## Seguimiento

Cosas a vigilar en próximas ediciones, además de lo que ya está vigilado en la revisión W19:

- **W20 (lunes 11 de mayo)**: cuántas propuestas se auditan. Si vuelve a ser n=1, la medición del §10 tras W22 tendrá muestra demasiado pequeña incluso acumulada (4 lunes × 1 propuesta = 4). Si la edición trae 3-5 propuestas como las semanas históricas más densas, la muestra acumulada (n=12-20) sí permite calibrar.
- **Sinónimos institucionales en `target_actor`**: contar manualmente cuántos casos en W20-W22 son sinonimia (Municipios/Ayuntamientos, Govern/GOIB…) y cuántos son disputa real. Si la sinonimia supera el 30% del total de "críticas", el caso está claro y entra como sesión específica para el comparador. Si está por debajo del 10%, no merece pelea: apuntar como ruido conocido y usar el log con criterio.
- **Eventos Opus fallback en `costs.csv`**: comprobar después de cada edición si hubo `extract_fallback` y si el log del auditor lo ignora. Si pasan 3 ediciones seguidas con fallback ignorado, se prioriza el fix del desacople sobre otras tareas del plano §8.
- **Conteo de propuestas de la página `/propuestas/`** antes y después del día que PI10 active. Apuntar cuántas se mueven a cuarentena para que la nota en `/correcciones/` (si procede bajo la regla 5 fundacional) sea precisa.
- **Cierre del Hito 1**: la decisión [D20](../../DECISIONES.md) sigue siendo *"primera corrida limpia W19 + revisión tras 3-4 ediciones consecutivas (W19-W22)"*. La medición formal del §10 se hace el lunes 1 de junio sobre la muestra acumulada — ese día se decide cierre o reapertura.

## Revisar si

Señales que romperían las decisiones de esta sesión y obligarían a reabrirla:

- (a) Si W20 trae 3-5 propuestas y los hallazgos 2 y 3 se confirman en cadena (sinónimos institucionales en mayoría de "críticas" + Opus fallback ignorado en cada lunes): elevar prioridad y abrir sesión específica antes de W22, no esperar.
- (b) Si el `_note` del bloque `verify` resulta ser ruido en el log JSON (consumidor lo lee como campo del schema y rompe): retirar y volver a `null` puro, gestionando la observabilidad por documentación externa.
- (c) Si tras W22 la medición formal del §10 da ratio de disputas dentro de rango y los cuatro hallazgos se quedan sin reproducir: cerrar el Hito 1 sin tocar el comparador ni el desacople, dejándolos como deuda explícita para la iteración posterior del plano §8.
- (d) Si tras W22 la medición da ratio fuera de rango y se demuestra que la sinonimia es la causa: el fix del comparador entra en la iteración posterior con prioridad alta y bloquea PI10 hasta resolverse.
