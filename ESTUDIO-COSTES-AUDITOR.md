# Estudio de costes — Auditor IA del observatorio

**Fecha:** 2026-04-22
**Estado:** cerrado, listo para construir el módulo `src/audit.py` encima de estos números
**Origen:** tarea de ruta crítica de Fase 1 (revisión fundacional). Bloquea la construcción del auditor.
**Principio base:** el observatorio se audita a sí mismo con capas IA + heurísticas + log público. El editor no revisa contenido. El auditor es la respuesta técnica a *"¿quién revisa?"*.

---

## 1 · Resumen ejecutivo

El auditor de 5 capas añade **entre 0,08 € y 0,20 € al mes** sobre el pipeline ya existente en régimen normal. El backfill retroactivo de 12 semanas cuesta **~5,4 € una sola vez** (no los 3,5 € estimados en caliente el 21-abr; la diferencia se explica por generación retroactiva Opus y self-review, que no estaban en la cuenta original).

**Lectura corta:**

- **Mes típico con auditor encendido:** ~2 €/mes. Muy por debajo del tope blando (12 €).
- **Mes con backfill completo + auditoría trimestral + re-benchmark:** ~7,7 €/mes. Dentro de capa amarilla, nunca cerca del tope duro (50 €).
- **Delta neto del auditor sobre lo ya construido:** +0,2 €/mes. La mayor parte del pipeline ya existe (Haiku extrae, Sonnet valida, Opus fallback); lo que se añade es (a) re-extracción ciega con Sonnet en lugar de simple validación, (b) comparador determinista Python, (c) heurísticas sin IA, (d) log de auditoría por propuesta.
- **Sensibilidad:** si las disputas se disparan al 40 % (Haiku mal calibrado) o las propuestas/semana se triplican en temporada alta, el coste mensual sube a ~3 €/mes. No hay escenario realista que acerque el gasto al tope blando.

El cuello de botella del coste total del proyecto no es el auditor. Son `generate` con Opus (~85 % del gasto de una edición) y el backfill retroactivo one-shot. El auditor es **ruido contable** comparado con eso, y por tanto no debe limitarse por coste.

**Decisión recomendada:** construir el auditor con las 5 capas completas y las heurísticas sin IA desde el inicio, sin recortes por coste. El margen existe.

---

## 2 · Qué es el auditor y qué ya existe

### 2.1 Las 5 capas decididas el 21-abr

| Capa | Qué hace | Modelo | Estado actual |
|---|---|---|---|
| 1 | Extracción primaria de propuestas a partir de noticias clasificadas | Haiku 4.5 | ✅ Existe en [`src/extract.py`](src/extract.py) como `extract_with_haiku` |
| 2 | Auditoría ciega independiente (re-extrae sin ver capa 1) | Sonnet 4.6 | 🟡 Parcial — hoy hay un validador corto que devuelve `{valid, reason}` (~512 output tokens); el auditor pide re-extracción completa |
| 3 | Comparador determinista Python + 5 checks de `verify.py` + heurísticas sin IA (cross-source, verbatim, whitelist, viability sanity) | — | 🟡 Parcial — `verify.py` existe con checks HTTP/trazabilidad; faltan comparador y heurísticas |
| 4 | Arbitraje Opus solo cuando capa 1 y capa 2 discrepan | Opus 4.7 | ✅ Existe como `retry_with_opus` en `extract.py` (disparado por `valid=false` del validador) |
| 5 | Revisión humana: solo propuestas `flagged` y, opcional, muestreo aleatorio 10 % de auto-aprobadas | — humano | ⏳ Pendiente de decisión (ver §7) |

### 2.2 Gap analysis — qué hay que construir realmente

1. **Módulo nuevo `src/audit.py`** que orquesta las 5 capas. Sustituye la función `run()` actual de `extract.py`, que se queda como biblioteca de llamadas individuales.
2. **Capa 2 re-extracción ciega**: llamada Sonnet con el mismo prompt `EXTRACT_SYSTEM` de extract.py, sobre el mismo payload que Haiku, sin ver el output de Haiku. Batch único.
3. **Comparador determinista**: función Python que compara dos extracciones campo a campo y devuelve `{identical: bool, diffs: [...], severity: critical|minor|none}`.
4. **Heurísticas sin IA**: módulo `src/audit_heuristics.py` con cross-source, single-source penalty, verbatim substring (difflib), whitelist dominio↔actor, viability sanity.
5. **Cálculo de tier**: función que combina salidas de capa 3 + capa 4 → 🟢 / 🟡 / 🟠 / 🔴.
6. **Log de auditoría** en `data/audit/YYYY-wWW/{proposal_id}.json` con trazabilidad completa. Abierto y público.
7. **Integración con `report.py`**: pipeline pasa de `ingest → classify → extract → generate → verify` a `ingest → classify → extract → audit → generate → verify`.
8. **Integración con `self_review.py`**: añadir un check específico de salud del auditor (ratio de disputas semanales).

Lo que **no** hay que reconstruir: `extract_with_haiku`, `retry_with_opus`, el sistema de registro de costes, el prompt de extracción. Están bien.

---

## 3 · Datos de calibración (reales, no hipótesis)

Todo lo que sigue sale de `data/costs.csv`, ejecución W17 del 2026-04-20 (última real del pipeline documental).

| Fase | Modelo | Input tok | Output tok | Coste USD |
|---|---|---|---|---|
| `classify` | Haiku 4.5 | 3 922 | 3 210 | $0,020 |
| `extract_base` | Haiku 4.5 | 1 880 | 1 020 | $0,007 |
| `extract_validate` × 3 | Sonnet 4.6 | ~820 cada | ~18 cada | $0,008 total |
| `generate` | Opus 4.7 (cache read 2 944) | 5 777 | 3 803 | $0,376 |
| `self_review` | Sonnet 4.6 | 5 943 | 756 | $0,029 |
| **Total edición** | | | | **~$0,44** |

En euros (USD→EUR 0,92): **~0,40 €/edición semanal**.

**Parámetros editoriales observados:**

- 3 propuestas extraídas en W17 (rango razonable por lectura de ediciones previas: 2-6 propuestas/semana).
- ~20 noticias clasificadas como `is_housing=True` por semana, de las que 3-6 llevan propuesta formal/en_movimiento.
- El `system` prompt de extracción pesa ~400 tokens; el payload por noticia (title+summary+url) ~200 tokens; la ficha JSON de salida por propuesta ~350-500 tokens.

**Precios por millón de tokens (abril 2026, desde [`src/costs.py`](src/costs.py)):**

| Modelo | Input | Output | Cache read | Cache write |
|---|---|---|---|---|
| Haiku 4.5 | $1,00 | $5,00 | $0,10 | $1,25 |
| Sonnet 4.6 | $3,00 | $15,00 | $0,30 | $3,75 |
| Opus 4.7 | $15,00 | $75,00 | $1,50 | $18,75 |

**Topes del proyecto** ([`src/costs.py`](src/costs.py) v3): blando 12 €/mes (solo avisa), duro 50 €/mes (corta pipeline).

---

## 4 · Coste por capa — números finos

Asumimos 3 propuestas/semana (media razonable calibrada con W17). La sección 8 cubre la sensibilidad si este supuesto falla.

### Capa 1 — Extracción primaria Haiku

- **Qué hace:** lee `classified.json`, devuelve lista de propuestas estructuradas por noticia.
- **Forma:** una sola llamada batch por ejecución (ya es así hoy).
- **Coste semanal:** $0,007 (datos reales W17).
- **Coste mensual (4,33 semanas):** $0,030 = **0,028 €/mes**.
- **Estado:** ya implementada, no se toca.

### Capa 2 — Auditoría ciega Sonnet

- **Qué hace:** Sonnet 4.6 recibe el mismo payload que Haiku (noticias con `proposal_type != ninguna`) y el mismo `EXTRACT_SYSTEM` prompt. Devuelve su propia lista de propuestas, sin haber visto la de Haiku.
- **Forma:** una sola llamada batch por ejecución.
- **Tokens esperados:** ~1 880 in + ~1 020 out (mismo orden que Haiku; Sonnet tiende a output similar o marginalmente mayor).
- **Coste semanal:** 1 880 × $3/M + 1 020 × $15/M = $0,0056 + $0,0153 = **$0,021**.
- **Coste mensual:** $0,091 = **0,084 €/mes**.
- **Delta neto vs validador actual:** el validador actual gastaba ~$0,008/semana en 3 llamadas Sonnet cortas. El cambio es +$0,013/semana = **+0,05 €/mes**. Marginal.
- **Por qué Sonnet y no otra cosa:** Haiku como auditor ciego daría demasiada correlación (mismo modelo, mismos sesgos). Opus sería excesivo (costaría 5× más, sin aportar calidad de auditoría proporcional). Sonnet es el punto óptimo calidad/coste del benchmark del 20-abr.

### Capa 3 — Comparador determinista + verify.py + heurísticas

- **Qué hace:**
  - Compara campo a campo la salida de capa 1 vs capa 2 y emite `{diffs, severity}`. Campos críticos: `actor`, `target_actor`, `palanca`, `state`, `url_source`, `statement_verbatim`. Campos menores: `viability_*`, `horizon`.
  - Aplica los 5 checks de `verify.py` por propuesta: URL 200, trazabilidad dominio↔actor, verbatim match en HTML, fecha coherente, Wayback snapshot.
  - Aplica las heurísticas sin IA (ver más abajo).
  - Emite tier preliminar 🟢 / 🟡 / 🟠 / 🔴.
- **Heurísticas sin IA a implementar:**
  1. **Cross-source confirmation.** Si la misma propuesta (mismo actor + misma palanca + misma target_actor) aparece en ≥2 URLs de dominios distintos, tier sube un nivel o refuerza 🟢.
  2. **Single-source penalty.** Si solo hay 1 URL, el tier máximo permitido es 🟡. Nunca 🟢 con fuente única (regla dura).
  3. **Verbatim substring match.** Con `difflib.SequenceMatcher` sobre el HTML limpio de la URL. Umbrales diferenciados:
     - Si `statement_type == "quote"`: ratio ≥0,95 (cita textual obligatoria).
     - Si `statement_type == "reported"`: ratio ≥0,60 del summary + presencia literal del nombre del actor + ≥2 términos clave de la propuesta. Aceptado según decisión 2026-04-21.
  4. **Domain-actor whitelist.** Diccionario `data/actor_domains.yml` mapea actores conocidos a dominios oficiales (p. ej. `Consell d'Eivissa → conselldeivissa.es`). Match refuerza; mismatch debilita pero no descarta (la URL puede ser una cobertura de tercera parte legítima).
  5. **Viability sanity.** Si `viability_economic == "alta"` pero no hay cifra numérica en el `statement_verbatim` ni en la noticia, downgrade automático a `"no_evaluada"`.
- **Coste API:** **0 €**. Código Python puro. HTTP hits de `verify.py` son marginales; Wayback snapshot una vez por URL.
- **Coste de implementación:** ~6-8 h de desarrollo inicial, amortizado una vez.

### Capa 4 — Arbitraje Opus solo en disputas

- **Qué hace:** Opus 4.7 re-extrae una propuesta concreta, vista la noticia + ambas extracciones previas. Se invoca solo si capa 3 marca disputa crítica (diff en actor, target_actor, palanca, state, o verbatim match <0,60).
- **Frecuencia esperada:** ~15 % de propuestas disputan. Calibrado con literatura de ensemble-disagreement en extraction tasks y con el comportamiento observado de Haiku vs Sonnet en el benchmark del 20-abr (disagree en 2/10 casos en `bench_extract`).
- **Forma:** una llamada individual por propuesta disputada.
- **Tokens por disputa:** ~2 000 in (prompt + noticia + ambas extracciones) + 500 out (ficha nueva).
- **Coste por disputa:** 2 000 × $15/M + 500 × $75/M = $0,030 + $0,0375 = **$0,068**.
- **Volumen mensual:** 3 props/semana × 4,33 × 0,15 = ~2 disputas/mes.
- **Coste mensual:** 2 × $0,068 = $0,135 = **0,124 €/mes**.
- **Qué pasa con la propuesta tras Opus:**
  - Si Opus coincide con capa 1 → se publica como 🟡 (hubo disputa, resolución clara).
  - Si Opus coincide con capa 2 → se publica como 🟡.
  - Si Opus difiere de ambas → tier 🟠 con nota pública *"arbitrada por Opus, revisión recomendada"*, propuesta va a `/revision-pendiente/` (cuarentena).

### Capa 5 — Revisión humana

- **Qué hace (diseño propuesto, ver §7 para la decisión abierta):**
  - Editor lee el correo Telegram del lunes con resumen del auditor. Si aparece alguna propuesta flagged 🟠 o 🔴, el editor decide: publicar en cuarentena, corregir, descartar.
  - **No hay muestreo aleatorio del 10 % de auto-aprobadas.** Esa práctica entra en contradicción directa con la regla fundacional del proyecto (editor opera, no audita). Ver §7.
- **Coste API:** **0 €**.
- **Tiempo editor:** estimado 5-10 min/semana en régimen normal (solo correo Telegram + decisión sobre 0-2 flagged/mes).

---

## 5 · Régimen normal mensual — total

| Concepto | €/mes | Nota |
|---|---|---|
| Pipeline base (ingest + classify + extract Haiku + verify + generate + self-review) | 1,75 | Datos reales W17 × 4,33 semanas |
| Capa 2 auditor — Sonnet ciego | +0,08 | Delta neto sobre validator actual |
| Capa 3 auditor — Python + verify.py + heurísticas | 0,00 | Sin API |
| Capa 4 auditor — Opus disputas (~2/mes) | 0,12 | Ya existía como `extract_fallback`; ahora formalizado como capa 4 |
| Capa 5 — editor | 0,00 | Sin muestreo humano (recomendación §7) |
| **Subtotal pipeline + auditor operativo** | **~1,95** | 🟢 Zona verde holgada |
| Re-benchmark mensual (10 noticias × 3 modelos) | +0,30 | Una vez al mes |
| Auditoría trimestral Opus (prorrateada 1/3) | +1,00 | Una edición de cada ~13 |
| **Subtotal con todos los añadidos periódicos** | **~3,25** | 🟢 Zona verde cómoda |

**Comparación con topes:**

- 🟢 Capa verde (< 6 €/mes): el proyecto funciona aquí ~11 meses al año.
- 🟡 Capa amarilla (6-9 €/mes): trimestre con backfill + bench + trimestral + temporada alta simultáneos. Puntual.
- 🟠 Capa naranja (9-12 €/mes): mes con backfill retroactivo activo + trilingüe activo. Puntual.
- 🔴 Roja blanda (12-50 €/mes): no se alcanza en operación normal; solo ante bug o decisión editorial excepcional.
- 🚨 Roja dura (>50 €/mes): solo ante runaway (bucle descontrolado). El auditor no aporta esa clase de riesgo.

---

## 6 · Backfill 12 semanas — coste one-shot

El backfill retroactivo de 12 semanas (semanas de febrero a abril de 2026) cubre: ingesta retroactiva, clasificación, extracción, auditor completo, generación editorial retroactiva Opus, self-review, archivo.

| Concepto | Cálculo | Coste USD | Coste EUR |
|---|---|---|---|
| `classify` Haiku × 12 | 12 × $0,020 | $0,24 | 0,22 € |
| `extract_base` Haiku × 12 | 12 × $0,007 | $0,08 | 0,08 € |
| Capa 2 Sonnet ciego × 12 | 12 × $0,021 | $0,25 | 0,23 € |
| Capa 4 Opus disputas (~15 % × 36 props = 5-6) | 6 × $0,068 | $0,41 | 0,38 € |
| `verify.py` + heurísticas | Python, HTTP | $0 | 0 € |
| `generate` Opus retro × 12 | 12 × $0,38 | $4,56 | 4,20 € |
| `self_review` Sonnet × 12 | 12 × $0,029 | $0,35 | 0,32 € |
| **Total backfill** | | **$5,89** | **~5,43 €** |

**Corrección importante:** la estimación en caliente del 21-abr ("~3,50 €") no incluía `generate` retroactivo ni `self_review`. El número real está en **~5,4 €**. Sigue siendo perfectamente absorbible: ejecutar el backfill en un mes con bajo consumo coloca el total mensual en 🟡 amarilla, lejos del tope blando.

**Mes pico realista (mayo 2026, con backfill):**

| Componente | €/mes |
|---|---|
| Régimen normal con auditor + self-review semanal | 1,95 |
| Backfill completo (one-shot) | 5,43 |
| Re-benchmark mensual | 0,30 |
| **Total mayo 2026 proyectado** | **~7,7 €** |

Capa 🟡 amarilla. Sin cruce del tope blando.

---

## 7 · Decisión abierta — capa 5 y muestreo humano

El plan del 21-abr describía capa 5 como *"editor revisa solo los flagged + muestreo aleatorio del 10 % de auto-aprobadas"*. Ese diseño entra en contradicción directa con dos cosas:

1. **Regla fundacional del PIVOTE (21-abr noche):** *"el editor opera el proyecto como infraestructura automatizada; no audita contenido manualmente"*.
2. **Rol editor = operador (DIARIO 21-abr):** *"en principio yo no voy a revisar nada"*.

Muestrear el 10 % son ~20 min/semana. No son muchos, pero son **reales y recurrentes**, y contaminan el rol que el proyecto ha cerrado públicamente.

### Opciones sobre la mesa

| Opción | Descripción | Coste € | Tiempo editor | Coherencia con regla fundacional |
|---|---|---|---|---|
| **A** | Editor revisa el 10 % muestreado + los flagged | 0 € | 20-30 min/semana | ❌ Rompe la regla |
| **B** (recomendada) | Sin muestreo humano. Solo flagged. Confianza en capas 2-4 + heurísticas + log público + formulario "¿falta algo?" | 0 € | 5-10 min/semana (solo flagged) | ✅ Alineada |
| **C** | Contratar revisor externo (periodista local) para el 10 % | 20-50 €/mes | 0 min editor | ✅ Compatible pero dispara el coste mensual ×10 |

**Recomendación: opción B.** El auditor está diseñado precisamente para que la revisión humana no sea necesaria como red de seguridad recurrente. Las capas 2-4 + heurísticas son la red. El log de auditoría pública es la transparencia que sustituye la revisión interna. La cuarentena pública `/revision-pendiente/` absorbe los casos dudosos. El formulario "¿falta algo?" absorbe el escrutinio externo.

La opción C entra en consideración solo si tras 3-6 meses de operación el auditor muestra tasas de error silencioso > 5 % (medido en auditoría trimestral Opus). No hay que adelantarla.

**Coste de la decisión:** opción B es la de menor coste (€ y tiempo). Las otras no suponen ahorro sino gasto añadido.

---

## 8 · Sensibilidad — qué pasa si los supuestos fallan

| Supuesto base | Valor calibrado | Escenario peor | Impacto €/mes | Crítico |
|---|---|---|---|---|
| Propuestas/semana | 3 | 10 (temporada alta mayo-oct, pico de debate público) | +0,4 €/mes | No |
| Ratio de disputas | 15 % | 40 % (Haiku mal calibrado o noticias ambiguas) | +0,3 €/mes | No, pero señal de alerta |
| Tamaño del payload por noticia | 200 tok | 400 tok (noticias largas del BOIB) | +0,1 €/mes | No |
| Precio Sonnet | $3/$15 | ×2 (cambio de precios Anthropic) | +0,1 €/mes | No |
| Frecuencia ejecución | 1/semana | 2/semana (si se cierra el ciclo con edición intersemanal urgente) | ×2 de lo anterior = +0,3 €/mes | No |
| Trilingüe activado desde backfill | No afecta al auditor | Re-auditar ES/CA/EN (innecesario: se audita original) | 0 | — |

**Conclusión de sensibilidad:** incluso acumulando cuatro de los cinco peores escenarios a la vez, el coste mensual del auditor se mantiene por debajo de **1 €/mes**. No hay ruta realista al tope blando a través del auditor.

**El riesgo real no es coste.** Es calidad: si capa 2 resulta poco informativa (porque Sonnet converge con Haiku en casi todo y el comparador nunca dispara), el auditor pierde valor y pasa a ser puro ritual. Eso se mide con la auditoría trimestral Opus: si el Opus de auditoría trimestral encuentra errores que las capas 1-4 no detectaron, hay que subir el nivel de capa 2 (prompt más estricto, o cambio a Opus en capa 2 en detrimento del coste).

---

## 9 · Optimizaciones aplicables sin perder calidad

### 9.1 Prompt caching — evaluar caso a caso, no siempre activar

- `EXTRACT_SYSTEM` pesa ~400 tokens. El break-even de creación de caché (×1,25 en input) se paga con 2+ lecturas (×0,10) dentro de los 5 min de TTL.
- **Capa 1 batch único por semana:** una sola llamada → no hay reutilización → no cachear. Hoy el código activa `cache_control` "por si acaso"; se puede dejar porque tampoco penaliza significativamente con batch único.
- **Capa 2 batch único por semana:** igual que capa 1, una sola llamada Sonnet → no cachear.
- **Capa 4 arbitraje Opus:** 1-2 llamadas por semana con prompts distintos → no cachear.
- **Verdadero ahorro de cache ya está:** `generate` Opus. En W17 la segunda ejecución leyó 2 944 tokens de caché (reducción de input cost × 10). Bien calibrado ya.

**Conclusión:** no hay ahorro adicional por caché en el auditor. Los números del §4 no dependen de caché nueva.

### 9.2 Batch único vs llamada por propuesta — confirmar batch

- Llamada por propuesta multiplica ×N los *fixed overhead* por llamada (router, init).
- Llamada batch mete N noticias en un solo request.
- Capa 1 ya es batch. Capa 2 se diseña batch desde el principio.
- **Capa 4 Opus es por propuesta por definición** (solo disputadas), pero el volumen es 1-2/semana, no hay economía de escala que aprovechar.

### 9.3 Rebajar capa 2 a validator si llegara a hacer falta

- Si en 3 meses de operación las disputas son < 5 % y el valor agregado de capa 2 es bajo, se puede rebajar capa 2 a validador corto (el actual). Ahorro: -0,05 €/mes. No merece la pena perseguirlo ahora.
- La decisión inversa (subir capa 2 a Opus) sería: -0,1 €/mes adicionales. Solo si la auditoría trimestral detecta fallos sistemáticos.

### 9.4 Verify.py — caché HTTP local

- Implementar caché local de 30 días para URLs ya verificadas. Reduce HTTP hits repetidos en backfill (~30 % de URLs se repiten en 12 semanas).
- Ahorro en coste €: 0. Ahorro en tiempo: minutos. Merece la pena por resiliencia (si una URL cae puntualmente, la caché mantiene verify OK en la siguiente ejecución).

### 9.5 Log de auditoría — almacenamiento

- JSON por propuesta en `data/audit/YYYY-wWW/{proposal_id}.json`.
- Coste 0 € (repo git).
- Peso estimado: ~5 KB/propuesta × 150 propuestas/año = 750 KB/año. Negligible.
- Append-only. Parte de la transparencia radical del proyecto.

### 9.6 Reducción de frecuencia en semanas flacas

- Si una semana no hay propuestas nuevas (solo rescate), capa 2 y capa 4 se saltan. Capa 1 devuelve lista vacía ya.
- Coste de semana flaca: clasificación Haiku + verify + generate Opus reducido. ~0,35 €/semana en lugar de 0,40 €.
- No requiere código nuevo: el pipeline actual ya hace nada cuando no hay candidatos.

---

## 10 · Plan de implementación — 4 semanas

Ruta ajustada al ritmo sostenible del editor (~15 h/semana, según roadmap).

### Semana 1 — Capa 2 y comparador

- **`src/audit.py`**: función `run_blind_audit()` que llama Sonnet con `EXTRACT_SYSTEM` sobre el mismo payload de capa 1. 3-4 h.
- **`src/audit_compare.py`**: función `compare_extractions(a, b)` que devuelve `{diffs, severity}` campo a campo. 2-3 h.
- **Tests unitarios mínimos**: dataset fake con 3 noticias, 2 escenarios (match completo, match con diff en `viability`). 2 h.
- **Entregable:** capa 2 + capa 3a (comparador determinista) operativas. Capa 4 (Opus) ya existe, no se toca aún.

### Semana 2 — Heurísticas sin IA

- **`src/audit_heuristics.py`**: cross-source, single-source penalty, verbatim substring con difflib, viability sanity. 4-5 h.
- **`data/actor_domains.yml`**: whitelist inicial con 15-20 actores más frecuentes (instituciones públicas, partidos, sindicatos, patronales, tercer sector). 1-2 h de curación manual.
- **Función `compute_tier()`**: combina salidas de capa 3 (comparador + verify + heurísticas) en 🟢/🟡/🟠/🔴 según árbol de decisión explícito. 2-3 h.
- **Entregable:** tier calculado correctamente sobre las 3 propuestas de W17 como validación empírica.

### Semana 3 — Log de auditoría + cuarentena + integración

- **`src/audit.py::write_audit_log()`**: serializa cada propuesta auditada a `data/audit/YYYY-wWW/{proposal_id}.json` con las 5 capas. 2-3 h.
- **Página `/revision-pendiente/`** (plantilla Jekyll + include): lista propuestas con tier 🔴 o flagged. 3-4 h.
- **Integración con `report.py`**: nuevo orden de fases, audit corre tras extract. 2 h.
- **Integración con `self_review.py`**: añadir check de salud del auditor (ratio de disputas + propuestas flagged). 1-2 h.
- **Entregable:** pipeline end-to-end corre con auditor en una edición piloto.

### Semana 4 — Prueba empírica con una edición real del backfill

- Ejecutar backfill solo de la semana **W10** (2-8 marzo 2026). Una semana sola, no las 12.
- Medir: coste real vs proyección, tasa de disputas real, tiempo de ejecución, tamaño del log.
- Ajustar umbrales de las heurísticas si los tiers quedan mal calibrados.
- Decidir si se procede con las 11 semanas restantes del backfill o si hay iteraciones pendientes.
- **Entregable:** decisión go / no-go para el backfill completo.

**Coste total de implementación:** ~30-40 h de desarrollo + 1 edición piloto. Cabe en 4 semanas a ritmo sostenible.

---

## 11 · Qué NO hacer

- **No revisar manualmente el 10 % de auto-aprobadas.** Rompe la regla fundacional. Si falta confianza, se sube el rigor de capa 2 o se añade una auditoría trimestral más exigente, no se mete al editor.
- **No activar prompt caching en capa 2.** Con batch único por semana no hay reuso dentro del TTL. Solo complica la lectura del código.
- **No usar Opus en capa 2 por defecto.** Sonnet está calibrado para este trabajo. Opus solo arbitra disputas.
- **No ejecutar el backfill en un mes con otros gastos acumulados** (trimestral + trilingüe activado a la vez): puede llevar el total a 🟠 naranja. Separar en ventanas temporales distintas cuando sea posible.
- **No auditar cada idioma por separado si se activa trilingüe.** La auditoría corre sobre el original (ES). Las traducciones son paso de salida, no de verificación.
- **No reducir capa 4 (Opus arbitraje) para ahorrar.** Es el último filtro antes de publicar. El ahorro máximo son ~0,1 €/mes. Ridículo comparado con el coste reputacional de una propuesta mal extraída publicada como 🟢.

---

## 12 · Definición de éxito del auditor

El auditor funciona si, a los 6 meses de operación:

1. **Ratio de disputas estable entre 8 % y 25 %.** Por debajo de 8 %, Sonnet capa 2 es redundante. Por encima de 25 %, Haiku capa 1 está mal calibrado.
2. **Auditoría trimestral Opus encuentra < 2 errores/trimestre** no detectados por capas 1-4 en una muestra de 30 propuestas. Si > 5, hay que rediseñar (no "el auditor falla", sino "hay que subir rigor").
3. **Tier 🟢 / 🟡 / 🟠 / 🔴 se distribuyen ~70 / 20 / 8 / 2.** Si > 30 % queda fuera de 🟢, las heurísticas son demasiado estrictas.
4. **Coste mensual del auditor se mantiene < 0,5 €/mes.** Si sube, revisar sensibilidad.
5. **Flagged 🟠 promedio = 0-2/mes.** Si > 5, el editor empieza a ser revisor de facto — señal para rediseñar heurísticas.
6. **Cero incidentes reputacionales** por propuesta 🟢 retirada por error de hecho.

Los 6 indicadores se publican en el dashboard interno de auditor (simple página markdown regenerada mensualmente; no es prioritario construirlo ahora, pero sí registrar las métricas desde el inicio).

---

## 13 · Ficha resumen de decisiones

| Decisión | Cerrada aquí |
|---|---|
| Capa 2 modelo | Sonnet 4.6 (no Haiku por correlación, no Opus por coste) |
| Capa 2 forma | Re-extracción ciega batch único, usando `EXTRACT_SYSTEM` existente |
| Capa 4 modelo y disparo | Opus 4.7 solo en disputas críticas (diff en `actor`, `target_actor`, `palanca`, `state`, `verbatim<0,60`) |
| Capa 5 muestreo humano | **Eliminado.** Editor solo mira flagged. Coherente con regla fundacional |
| Prompt caching en capas auditor | Desactivado (batch único semanal, no hay reuso) |
| Heurísticas sin IA | 5 implementadas: cross-source, single-source penalty, verbatim match, whitelist dominio-actor, viability sanity |
| Log de auditoría | `data/audit/YYYY-wWW/{proposal_id}.json` por propuesta, append-only, público |
| Cuarentena | Página pública `/revision-pendiente/` para tier 🔴 y flagged |
| Coste mensual auditor régimen normal | ~0,20 € (delta sobre pipeline existente) |
| Coste total mensual pipeline + auditor | ~2,0 €/mes típico, ~3,3 €/mes con añadidos periódicos |
| Coste backfill 12 semanas | ~5,4 € (one-shot), corregido desde la estimación inicial de 3,5 € |
| Plan | 4 semanas, ~35 h desarrollo |

---

## 14 · Enlaces

- [PIVOTE.md](PIVOTE.md) — regla fundacional automatización + veracidad.
- [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md) — decisión del 21-abr sobre auditor de 5 capas.
- [ROADMAP.md](ROADMAP.md) — fase 1, ruta crítica.
- [ARQUITECTURA.md](ARQUITECTURA.md) — pipeline completo.
- [`src/extract.py`](src/extract.py) — capas 1 y 4 ya implementadas.
- [`src/verify.py`](src/verify.py) — checks que alimentan capa 3.
- [`src/costs.py`](src/costs.py) — sistema de topes y registro.
- [`src/self_review.py`](src/self_review.py) — autoevaluación que incorporará check de salud del auditor.
- [`data/costs.csv`](data/costs.csv) — histórico de llamadas, base empírica de este estudio.
