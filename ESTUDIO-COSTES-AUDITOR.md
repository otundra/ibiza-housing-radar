# Estudio de costes — Auditor IA del observatorio

**Fecha:** 2026-04-22
**Estado:** cerrado, listo para construir el módulo `src/audit.py` encima de estos números
**Origen:** tarea de ruta crítica de Fase 1 (revisión fundacional). Bloquea la construcción del auditor.
**Principio base:** el observatorio se audita a sí mismo con capas IA + heurísticas + log público. El editor no revisa contenido. El auditor es la respuesta técnica a *"¿quién revisa?"*.

---

## 1 · Resumen ejecutivo

El auditor de 5 capas añade **entre 0,08 € y 0,20 € al mes** sobre el pipeline ya existente en régimen normal. El backfill retroactivo de 12 semanas cuesta **~5,4 € una sola vez** (no los 3,5 € estimados en caliente el 21-abr; la diferencia se explica por generación retroactiva Opus y self-review, que no estaban en la cuenta original).

**Lectura corta:**

- **Mes típico con auditor encendido (régimen estable desde mes 4):** ~2,4 €/mes. Muy por debajo del tope blando (12 €).
- **Meses 1-3 post-lanzamiento con auditoría Opus mensual de calibración:** ~5,7 €/mes. En verde cómoda.
- **Mes pico realista** (mayo 2026 con backfill + auditoría mensual + re-bench): ~10 €/mes. Capa naranja (9-12 €), nunca cerca del tope duro (50 €). Justificado: calibrar rápido el auditor antes de acumular errores.
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

- **Qué hace (cerrado 2026-04-23):**
  - Editor lee el correo Telegram del lunes con resumen del auditor. Si aparece alguna propuesta flagged 🟠 o 🔴, el editor decide: publicar en cuarentena, corregir, descartar.
  - **No hay muestreo aleatorio del 10 % de auto-aprobadas** (decisión del editor 2026-04-23). Contradice la regla fundacional del proyecto. La red la hacen capas 2-4 + heurísticas + log público + cuarentena pública + formulario externo.
- **Coste API:** **0 €**.
- **Tiempo editor:** estimado 5-10 min/semana en régimen normal (solo correo Telegram + decisión sobre 0-2 flagged/mes).

### Capa 5bis — Repaso IA mensual de cuarentena (cerrada 2026-04-23)

- **Qué hace:** una vez al mes, Opus 4.7 lee todas las propuestas que quedaron en cuarentena ese mes + sus logs de auditoría completos + la whitelist `data/actor_domains.yml` + los umbrales vigentes en `src/audit_heuristics.py`. Devuelve dos salidas:
  - **Diagnóstico narrativo corto** (~300 palabras) describiendo patrones detectados. Ejemplo: *"en 4 de 8 casos el verbatim match falló porque el texto estaba en catalán y la heurística solo pesa castellano; en 2 casos la whitelist no tenía el subdominio `.cat` del Consell"*.
  - **Bloque YAML de ajustes propuestos** ejecutables sin edición manual. Ejemplo: añadir entradas a la whitelist, mover umbrales, proponer refinado de prompt.
- **Aplicación de los ajustes:** nunca automática. El editor recibe por Telegram el diagnóstico y el bloque YAML, y responde OK/rechazo. Solo tras OK explícito se aplican los ajustes al repo (commit `config(audit): ajustes mensuales aprobados por editor`). Esto mantiene a la IA como proponente y al editor como custodio del método.
- **Coste API:** ~0,3-0,5 €/mes (Opus leyendo 10-30 propuestas + contexto).
- **Tiempo editor:** ~5 min/mes (leer diagnóstico + decisión). Reducción de 30 min a 5 min respecto a hacerlo manual.
- **Por qué IA y no editor humano:** coherencia con la regla fundacional del proyecto — el editor cuida la vía, no lee cada vagón. El repaso de patrones en cuarentena es trabajo analítico delegable; la decisión de aplicar ajustes no lo es.
- **Riesgo a vigilar:** IA afinando su propio sistema = ciclo cerrado. Mitigación: (a) los ajustes nunca se aplican sin OK humano, (b) la auditoría mensual/trimestral con Opus sobre el corpus general (§5) es independiente del repaso de cuarentena y puede detectar si los umbrales auto-ajustados están rebajando calidad. Si la auditoría general empieza a encontrar errores sistemáticos en propuestas auto-aprobadas, hay que congelar los ajustes del repaso mensual y revisar.

---

## 5 · Régimen normal mensual — total

| Concepto | €/mes | Nota |
|---|---|---|
| Pipeline base (ingest + classify + extract Haiku + verify + generate + self-review) | 1,75 | Datos reales W17 × 4,33 semanas |
| Capa 2 auditor — Sonnet ciego | +0,08 | Delta neto sobre validator actual |
| Capa 3 auditor — Python + verify.py + heurísticas | 0,00 | Sin API |
| Capa 4 auditor — Opus disputas (~2/mes) | 0,12 | Ya existía como `extract_fallback`; ahora formalizado como capa 4 |
| Capa 5 — editor | 0,00 | Sin muestreo humano (decisión editor 2026-04-23) |
| Capa 5bis — repaso IA mensual cuarentena (Opus) | +0,40 | Opus lee cuarentena mensual, propone ajustes, editor firma |
| **Subtotal pipeline + auditor operativo** | **~2,35** | 🟢 Zona verde holgada |
| Re-benchmark mensual (10 noticias × 3 modelos) | +0,30 | Una vez al mes |
| Auditoría Opus — **mensual los 3 primeros meses** (calibración rápida) | +3,00 | Solo may-jul 2026 |
| Auditoría Opus trimestral (desde mes 4, prorrateada 1/3) | +1,00 | Una edición de cada ~13 desde agosto |
| **Subtotal con añadidos — meses 1-3 post-lanzamiento** | **~5,65** | 🟢 Zona verde cómoda |
| **Subtotal con añadidos — mes 4 en adelante** | **~3,65** | 🟢 Zona verde holgada |

**Nota sobre la auditoría Opus mensual los 3 primeros meses (decisión 2026-04-23):** los 3 meses iniciales se audita cada edición del primer lunes de mes con Opus sobre una muestra de 10-15 propuestas recientes. Objetivo: calibrar umbrales del auditor con datos reales rápido, antes de que los problemas se acumulen. A partir del mes 4 vuelve a cadencia trimestral estándar. Coste extra del bloque de 3 meses: ~6 € totales (~2 €/mes × 3). Trazable en `costs.csv` como fase `monthly_audit`.

**Revisión de cadencias al mes 4 y al mes 7 (apuntado 2026-04-23):**
- **Mes 4 (agosto 2026):** revisar si la auditoría mensual del arranque se cierra como estaba previsto, se extiende unos meses más, o se fija como cadencia permanente. Criterio: ¿los ajustes mensuales siguen aportando señal nueva o ya saturan?
- **Mes 7 (noviembre 2026):** revisar si los reportes trimestrales conviene mantenerlos, sustituirlos por semestrales, o combinarlos. Criterio: valor informativo real, no costumbre. Evitar duplicación entre canales.

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

**Mes pico realista (mayo 2026, con backfill + auditoría mensual de arranque):**

| Componente | €/mes |
|---|---|
| Régimen normal con auditor + self-review + capa 5bis IA | 2,35 |
| Backfill completo (one-shot) | 5,43 |
| Re-benchmark mensual | 0,30 |
| Auditoría Opus mensual de calibración (solo meses 1-3) | 2,00 |
| **Total mayo 2026 proyectado** | **~10,1 €** |

Capa 🟠 naranja. Sin cruce del tope blando (12 €), lejísimos del duro (50 €). Es un mes excepcional por acumulación de arranque, no un régimen. Desde agosto 2026 el mes típico vuelve a ~2,4 €.

---

## 7 · Decisión abierta — capa 5 y muestreo humano

El plan del 21-abr describía capa 5 como *"editor revisa solo los flagged + muestreo aleatorio del 10 % de auto-aprobadas"*. Ese diseño entra en contradicción directa con dos cosas:

1. **Regla fundacional (21-abr noche, ver [CLAUDE.md](CLAUDE.md#reglas-fundacionales)):** *"el editor opera el proyecto como infraestructura automatizada; no audita contenido manualmente"*.
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

### 10.0 · Partición en mínimo viable + iteración (decisión 2026-04-23)

El plan semanal siguiente sigue siendo la referencia completa, pero su ejecución se parte en dos bloques — ver [D1](DECISIONES.md). Motivo: reducir la carga cognitiva del editor mientras aprende el sistema y llegar antes al punto *"funciona y lo entiendo"*. El mínimo viable entrega el 80 % de la transparencia (doble-ojo automático + log público + protocolo de corrección); la iteración posterior es confort y optimización.

**Mínimo viable — 2 semanas (Hito 1 del frame de tres hitos grandes, [D6](DECISIONES.md)):**

- **Semana 1** completa tal cual: capa 2 ciega Sonnet + `src/audit_compare.py` determinista. Sin cambios.
- **Semana 2** con alcance ajustado: heurísticas sin IA (cruce de fuentes, verbatim match, whitelist `actor_domains.yml` V1) + `compute_tier()` **como hueco reservado** que escribe `tier: { value: null, reason: "pendiente estudio", signals: {...} }` ([D5](DECISIONES.md)). Las señales se calculan y guardan desde el día uno; el badge de color no se combina hasta que RT15 cierre y defina el árbol de decisión.
- **Semana 3 reducida:** log de auditoría en `data/audit/YYYY-wWW/{proposal_id}.json` con el campo **`corrections`** append-only ([D2](DECISIONES.md)) + integración con `report.py` + activación de la página `/correcciones/` como stub mínimo. **Se omiten en esta fase:** página `/revision-pendiente/` (cuarentena navegable), dashboard `/auditor/`, formalización de capa 4 Opus como paso separado.
- **Semana 4** tal cual: prueba empírica sobre la semana W10 (2-8 marzo 2026).

**Iteración posterior — 2-3 semanas (Hito 1 cerrado, hitos 2-3 pueden empezar):**

- Formalización explícita de la capa 4 Opus (hoy fallback implícito en `extract.py`).
- Página `/revision-pendiente/` con la cuarentena navegable.
- Dashboard público `/auditor/` con las métricas del canal 1 (§12.1).
- Capa 5bis: repaso IA mensual de cuarentena con Opus + bloque YAML de ajustes firmado por el editor vía Telegram.
- Conexión de `compute_tier()` real cuando RT15 cierre, leyendo del bloque `signals` ya acumulado sin migrar logs antiguos.

**Schema del log en el mínimo viable:**

```json
{
  "proposal_id": "...",
  "tier": { "value": null, "reason": "pendiente estudio", "signals": {...} },
  "corrections": [],
  "layers": { "haiku": {...}, "sonnet_blind": {...}, "compare": {...}, "heuristics": {...} },
  "verify": {...},
  "timestamps": {...}
}
```

El campo `corrections` es append-only: cada petición de enmienda añade una nota fechada con origen (email/formulario), cuerpo y resolución. El JSON original de la propuesta nunca se modifica. Canal de correcciones: email al buzón del proyecto (**diferido hasta cierre del nombre**) **+** formulario en `/contacto/` con backend webhook → issue GitHub → notificación Telegram.

**Tests diferidos ([D4](DECISIONES.md)):** RT5 *"tests básicos del pipeline"* absorbe la cobertura de `audit.py` junto con `extract.py`, `verify.py`, `balance.py` y `rescue.py` en un solo bloque, con fixtures reales del backfill. La validación durante construcción es empírica (Semana 4 sobre W10).

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
- **No concatenar gastos grandes sin aviso previo, pero no evitarlos por sistema.** Si mayo 2026 acumula backfill + trilingüe + auditoría mensual + re-bench, el total puede llegar a 🟠 naranja (9-12 €). Está dentro de los topes y del presupuesto de arranque del proyecto. La regla sana es: hacer la estimación antes de apretar el botón, registrar la previsión, y proceder si beneficia al lanzamiento. Solo se separa en ventanas distintas si la suma proyectada roza el tope blando sin aportar valor al progreso.
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

### 12.1 · Dónde se ven los indicadores — tres canales complementarios

Los 6 indicadores anteriores se materializan en tres canales con funciones distintas; ninguno sustituye a los otros. Los tres se alimentan del mismo log en `data/audit/`, sin duplicación de cálculo.

**Canal 1 · Página pública `/auditor/`** (eje principal, coherente con la filosofía del log público).

- URL permanente, regenerada automáticamente tras cada edición del lunes.
- Contenido: distribución de tiers últimas 4 semanas, ratio de disputas, flagged/mes, cuarentena actual con links a cada caso, coste del auditor/mes, fecha y resultado de la última auditoría Opus.
- Es la respuesta visible a *"¿quién revisa?"*. No una página de "nuestras métricas"; una página donde cualquier visitante comprueba que el sistema funciona en abierto.
- Encaja con el resto de páginas de transparencia del proyecto: `/costes/`, `/estado/`, `/balance/`, `/correcciones/`.
- Implementación: script `src/audit_dashboard.py` que regenera `docs/auditor.md` desde `data/audit/*.json`. Parte del plan de la semana 3.

**Canal 2 · Alertas Telegram — parte único del lunes** (consolidado, sin sobrealertar).

- **Un solo mensaje por semana**, los lunes tras generar la edición. Agrupa todas las señales fuera de rango verde de los últimos 7 días. Si todo está verde, silencio: sin parte.
- Triggers que entran en el parte si ocurren (afinar con datos reales de los 3 primeros meses):
  - Ratio de disputas semanal > 25 %.
  - Flagged en la edición > 3.
  - Auditoría Opus mensual encuentra > 2 errores no detectados por capas 1-4.
  - Cuarentena supera 10 propuestas abiertas.
  - Coste mensual del auditor > 1 €.
- **Excepción — alertas críticas sueltas:** tope duro cruzado, pipeline roto, API key caducada. Esos sí disparan mensaje inmediato independiente del parte del lunes. No se mezclan con el parte rutinario.
- Infra: `src/notify.py` ya existe, se reutiliza. Lógica nueva en `src/audit_weekly_brief.py`: recoge señales, genera un mensaje si hay algo, silencio si no.

**Canal 3 · Reportes periódicos + página `/reportes/`** (narrativa, contexto, tendencias).

- **Cadencias:**
  - **Mensual** durante los 3 primeros meses post-lanzamiento (may-jul 2026). Calibración rápida con Opus.
  - **Trimestral** a partir del mes 4 (desde agosto 2026).
  - **Semestral** a partir del mes 7 (desde noviembre 2026) en adición a los trimestrales — mayor horizonte narrativo, comparación año a año una vez haya datos.
- **Revisión de cadencias** (apuntado 2026-04-23):
  - **Al cumplirse el mes 4** (agosto 2026), revisar si la auditoría mensual del arranque se extiende, se fija como cadencia permanente, o se cierra según lo previsto. Decisión basada en si los ajustes mensuales de los 3 primeros meses siguen aportando señal o ya saturan.
  - **Al cumplirse el mes 7** (noviembre 2026), revisar si los reportes trimestrales siguen siendo útiles con horizonte semestral encima o conviene sustituirlos por los semestrales. Evitar duplicación innecesaria; elegir cadencia por valor informativo real, no por costumbre.
- **Página `/reportes/`:** índice permanente con todos los reportes bajo URLs propias (`/reportes/2026-05/`, `/reportes/2026-q3/`, `/reportes/2026-h2/`...). Formato markdown, estilo editorial, comparables entre sí.
- **Envío por Telegram:** headline de una línea + link al reporte publicado. No el texto entero.
- **Qué contienen los reportes que la página `/auditor/` no tiene:** comparación con el periodo anterior, narrativa de ajustes hechos (umbrales, heurísticas, whitelist), lecturas de patrones detectados por el repaso IA mensual de cuarentena.

Los tres canales se construyen en orden de prioridad: canal 1 en semana 3 del plan, canal 2 en semana 3 también reutilizando `notify.py`, canal 3 al cierre del primer mes post-lanzamiento (junio 2026 si el relanzamiento es mayo).

---

## 13 · Ficha resumen de decisiones

| Decisión | Cerrada aquí |
|---|---|
| Capa 2 modelo | Sonnet 4.6 (no Haiku por correlación, no Opus por coste) |
| Capa 2 forma | Re-extracción ciega batch único, usando `EXTRACT_SYSTEM` existente |
| Capa 4 modelo y disparo | Opus 4.7 solo en disputas críticas (diff en `actor`, `target_actor`, `palanca`, `state`, `verbatim<0,60`) |
| Capa 5 muestreo humano | **Eliminado** (editor 2026-04-23). Solo flagged. Coherente con regla fundacional |
| Capa 5bis repaso mensual de cuarentena | **Delegada a IA** (editor 2026-04-23). Opus mensual lee cuarentena + logs y propone ajustes YAML; editor firma con OK en 5 min. ~0,4 €/mes |
| Prompt caching en capas auditor | Desactivado (batch único semanal, no hay reuso) |
| Heurísticas sin IA | 5 implementadas: cross-source, single-source penalty, verbatim match, whitelist dominio-actor, viability sanity |
| Log de auditoría | `data/audit/YYYY-wWW/{proposal_id}.json` por propuesta, append-only, público |
| Cuarentena | Página pública `/revision-pendiente/` para tier 🔴 y flagged |
| Auditoría Opus | **Mensual** los 3 primeros meses post-lanzamiento (editor 2026-04-23), luego trimestral. Revisión de cadencia al mes 4 |
| Reportes periódicos | Mensual (meses 1-3), trimestral (desde mes 4), semestral (desde mes 7). Revisión de cadencia al mes 7 |
| Panel de éxito del auditor | 3 canales: página pública `/auditor/` (eje), parte Telegram del lunes consolidado (un solo mensaje/semana, silencio si todo verde), página `/reportes/` con narrativa (mensual → trimestral → semestral) |
| Coste mensual auditor régimen normal | ~0,20 € (delta sobre pipeline existente) |
| Coste total mensual pipeline + auditor | ~5,65 €/mes en meses 1-3 (con auditoría Opus mensual); ~3,65 €/mes desde mes 4 |
| Coste backfill 12 semanas | ~5,4 € (one-shot), corregido desde la estimación inicial de 3,5 € |
| Política de concurrencia de gastos | Estimar antes, proceder si beneficia al progreso. Topes absolutos: blando 12 €, duro 50 €. |
| Plan | 4 semanas, ~35 h desarrollo |
| **Partición del plan (2026-04-23)** | **Mínimo viable 2 sem + iteración 2-3 sem — ver [D1](DECISIONES.md) y §10.0** |
| **Log público + protocolo de correcciones 72 h (2026-04-23)** | **Campo `corrections` append-only + `/correcciones/` + email (diferido) + formulario (webhook→issue GH) — ver [D2](DECISIONES.md)** |
| **Whitelist V1 antes del backfill (2026-04-23)** | **15-20 actores conocidos curados en `data/actor_domains.yml`, refinamiento post-backfill — ver [D3](DECISIONES.md)** |
| **Tests del auditor diferidos a RT5 (2026-04-23)** | **Cobertura en un solo bloque con fixtures reales; validación durante construcción = prueba empírica W10 — ver [D4](DECISIONES.md)** |
| **Re-estudio de tiers en paralelo (2026-04-23)** | **Auditor se construye con hueco `tier: { value: null, signals: {...} }`; RT15 deja de bloquear — ver [D5](DECISIONES.md)** |

---

## 14 · Enlaces

- [CLAUDE.md](CLAUDE.md#reglas-fundacionales) — regla fundacional automatización + veracidad.
- [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md) — decisión del 21-abr sobre auditor de 5 capas.
- [ROADMAP.md](ROADMAP.md) — fase 1, ruta crítica.
- [ARQUITECTURA.md](ARQUITECTURA.md) — pipeline completo.
- [`src/extract.py`](src/extract.py) — capas 1 y 4 ya implementadas.
- [`src/verify.py`](src/verify.py) — checks que alimentan capa 3.
- [`src/costs.py`](src/costs.py) — sistema de topes y registro.
- [`src/self_review.py`](src/self_review.py) — autoevaluación que incorporará check de salud del auditor.
- [`data/costs.csv`](data/costs.csv) — histórico de llamadas, base empírica de este estudio.
