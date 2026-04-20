# Arquitectura técnica — Pipeline del pivote

**Fecha:** 2026-04-20
**Origen:** [PIVOTE.md](PIVOTE.md).
**Alcance:** diseño del pipeline Python nuevo, schema de datos, módulos, flujos de control, tests. No entra en diseño web (ver [DISENO-WEB.md](DISENO-WEB.md)).

---

## Flujo actual vs. flujo nuevo

### Flujo actual (modelo "editor jefe")

```
ingest.py → classify.py → generate.py → write edition
                                ↓
                             costs.py (contabilidad)
                                ↓
                             notify.py (Telegram)
```

`generate.py` escribe propuestas propias basándose en la clasificación de Haiku.

### Flujo nuevo (modelo documental)

```
ingest.py → classify.py → extract.py → rescue.py → generate.py → verify.py → write edition
  (ampliado)  (ampliado)   (nuevo)     (nuevo)    (reescrito)    (nuevo, bloq)
                                                                          ↓
                                                                     balance.py
                                                                      (nuevo)
                                                                          ↓
                                                                       costs.py
                                                                     notify.py
```

El LLM interviene en tres puntos:

1. **Haiku clasifica** (como antes) + **extrae propuestas** con nombre, URL y datos estructurados.
2. **Opus compone** la edición uniendo lo clasificado, lo extraído y el rescate. **No genera propuestas.**
3. **Haiku verifica** precedentes externos y hace fact-check básico.

---

## Schema de datos

### 1. Salida de `ingest.py` (sin cambios estructurales)

```json
[
  {
    "title": "El Ayuntamiento de Ibiza desalojará...",
    "summary": "...",
    "url": "https://www.diariodeibiza.es/...",
    "source": "Diario de Ibiza",
    "published": "2026-04-17T09:30:00Z"
  },
  ...
]
```

### 2. Salida de `classify.py` (ampliada)

Para cada item se añaden los campos nuevos sobre los existentes (`is_housing`, `actor`, `lever`, `headline_es`).

```json
{
  "title": "...",
  "summary": "...",
  "url": "...",
  "source": "...",
  "published": "...",
  "is_housing": true,
  "actor": "consell",
  "lever": "normativa",
  "headline_es": "El Consell retira 700 anuncios de alquiler turístico ilegal",
  "has_explicit_proposal": true,
  "proposal_actor_hint": "Consell d'Eivissa",
  "proposal_actor_type_hint": "institucional_publico"
}
```

El clasificador Haiku solo marca si **parece haber propuesta** (`has_explicit_proposal`) y da pistas mínimas. La extracción detallada la hace `extract.py`.

### 3. Salida de `extract.py` (nueva)

Para cada item con `has_explicit_proposal=true`, extrae una o varias propuestas estructuradas:

```json
{
  "source_item_url": "...",
  "proposals": [
    {
      "id": "2026-w15-consell-ahr-01",
      "actor": "Consell d'Eivissa",
      "actor_type": "institucional_publico",
      "statement_verbatim": "texto literal citado",
      "statement_summary": "resumen de 1-2 frases",
      "url_source": "https://www.diariodeibiza.es/...",
      "palanca": "enforcement",
      "target_actor": "propietarios de alquiler turístico",
      "horizon": "corto_plazo",
      "state": "en_ejecucion",
      "viability_legal": "alta",
      "viability_legal_reason": "competencia ya ejercida bajo Llei 6/2017",
      "viability_economic": "sin_cifra_publica_disponible",
      "viability_economic_reason": "",
      "supporters_cited": [],
      "opponents_cited": [],
      "precedents": []
    }
  ]
}
```

**Dominios (enums):**

- `actor_type`: `partido`, `sindicato`, `patronal`, `tercer_sector`, `academico`, `judicial`, `institucional_publico`, `colectivo_ciudadano`, `otro`
- `palanca`: `normativa`, `fiscal`, `oferta_vivienda`, `intermediacion`, `enforcement`, `laboral`, `judicial`, `denuncia_social`, `otro`
- `horizon`: `inmediato`, `corto_plazo`, `temporada_2026`, `estructural`
- `state`: `propuesta`, `en_debate`, `aprobada`, `en_ejecucion`, `implementada`, `descartada`, `pendiente_resolucion_judicial`
- `viability_legal`: `alta`, `media`, `baja`, `no_evaluada`
- `viability_economic`: `alta`, `media`, `baja`, `sin_cifra_publica_disponible`, `no_evaluada`

**ID de propuesta:** formato `YYYY-wWW-{slug_actor}-{nn}`. Ejemplo: `2026-w15-consell-ahr-01`. Permite deduplicación entre ediciones y enlaces estables desde el tracker.

**Regla dura de `extract.py`:**

- Si `url_source` falta o no es accesible, la propuesta **no se incluye**.
- Si `statement_verbatim` no es atribuible a un actor con nombre, la propuesta **no se incluye**.
- Si un campo de viabilidad no puede evaluarse con la información disponible, se marca `no_evaluada` con razón vacía. **No se inventa.**

### 4. Salida de `rescue.py` (nueva)

Lee `docs/_editions/*.md` de las últimas ~16 semanas y los `extract` históricos (almacenados en `data/proposals_history.json` append-only). Selecciona 3-5 candidatas a rescate y pasa 1-2 al generador.

```json
[
  {
    "id": "2026-w13-caeb-residencias-01",
    "edition_origin": "2026-w13",
    "age_weeks": 2,
    "rescue_reason": "propuesta en estado 'propuesta' hace 3 semanas sin seguimiento público desde entonces",
    "still_relevant_check": "verificado manualmente o con Haiku según regla"
  }
]
```

Criterios duros para candidata a rescate:

1. Estado `propuesta`, `en_debate` o `aprobada` (no `implementada` ni `descartada`).
2. No mencionada en ninguna de las últimas 4 ediciones.
3. Sigue vigente (no caducada por cambio regulatorio posterior, verificable con Haiku + búsqueda rápida).
4. Edad entre 2 y 16 semanas.

### 5. Entrada a `generate.py` (nueva)

El generador recibe un paquete estructurado:

```json
{
  "edition": "2026-W17",
  "edition_title": "Semana 4 - Abril 2026",
  "signals": [...items clasificados con is_housing=true],
  "proposals_this_week": [...proposals extraídas de esta semana],
  "proposals_rescued": [...1-2 rescates],
  "map_of_positions": [...generado de los proposals_this_week agrupado por palanca],
  "omissions": [...signals sin proposals asociadas]
}
```

### 6. Salida de `generate.py` (nueva edición)

Markdown con frontmatter Jekyll expandido. Estructura:

```markdown
---
layout: edition
title: "Semana 4 - Abril 2026"
week: "2026-W17"
date: 2026-04-27
permalink: /ediciones/2026-w17/
excerpt: "…"
model: "pivote-documental-v1"
proposals_count: 4
actors_cited: ["Consell d'Eivissa", "CCOO", "Cáritas", "PSOE Ibiza", "Ayuntamiento de Ibiza"]
blocks_cited: ["institucional_publico", "sindicato", "tercer_sector", "partido"]
omissions_count: 1
rescued_count: 1
---

## 📡 Señales detectadas

- bullets con URL obligatoria

## 🗓 Cronología

3 líneas ordenando temporalmente los hechos. Sin valoración.

## 🗺 Mapa de posiciones

| Propuesta | Actor que la propone | Apoyos públicos | Rechazos públicos | Fuente |
|---|---|---|---|---|
| … | … | … | … | [↗]( url ) |

## 📋 Propuestas en circulación

### 1. [Título corto de la propuesta]

**Actor que la propone:** {actor} ({actor_type}) — [fuente]({url_source})

**Qué:** {statement_summary}

- **Actor que tendría que ejecutarla:** {target_actor}
- **Estado:** {state}
- **Horizonte:** {horizon}
- **Viabilidad jurídica:** {viability_legal} — {viability_legal_reason}
- **Viabilidad económica:** {viability_economic} — {viability_economic_reason}
- **Apoyos públicos citados:** {supporters_cited}
- **Rechazos públicos citados:** {opponents_cited}
- **Precedentes citados:** {precedents con URL cada uno}

## 🗄 Rescate: propuestas previas aún vigentes

### [Título propuesta rescatada] (origen: edición YYYY-wWW)

Misma ficha completa. Campo extra: **Por qué la rescatamos** — una frase.

## 🕳 Omisiones

- {Hecho documentado en señales sin propuesta asociada}: ningún actor ha propuesto nada al respecto esta semana.

## 👀 A vigilar la semana que viene

- bullets con fecha concreta
```

### 7. Salida de `verify.py` (nueva)

Reporta un `verification_report.json` y un código de salida. Si hay **cualquier** fallo bloqueante, no publica y avisa por Telegram.

```json
{
  "edition": "2026-W17",
  "checks": {
    "urls_http_200": {"total": 17, "ok": 17, "failed": []},
    "actor_traceability": {"total": 12, "ok": 12, "failed": []},
    "precedent_verification": {
      "total": 3,
      "by_confidence": {
        "exacto": 2,
        "aproximado": 1,
        "dudoso": 0,
        "no_encontrado": 0
      },
      "flagged": []
    },
    "verbs_blacklist": {"matches": []},
    "proposal_without_author": {"count": 0}
  },
  "blocking_failures": [],
  "soft_warnings": []
}
```

**Fallos bloqueantes:**

- Cualquier URL que no devuelva 200.
- Cualquier actor citado que no aparezca en el `classified.json` original.
- Cualquier precedente con confianza `dudoso` o `no_encontrado`.
- Cualquier verbo de la lista negra detectado (`debería`, `convendría`, `sería oportuno`, `hace falta`, `urge`, `proponemos`, `habría que`).
- Cualquier propuesta sin actor identificado.

**Fallos suaves (publican pero avisan):**

- Precedente `aproximado` (Telegram FYI).
- Balance de la edición con concentración excesiva en un solo bloque (Telegram atención).

### 8. Salida de `balance.py` (nueva)

Lee las ediciones publicadas y calcula reparto:

```json
{
  "window": "last_90_days",
  "total_proposals": 42,
  "by_actor_type": {
    "institucional_publico": 14,
    "partido": 10,
    "patronal": 6,
    "sindicato": 5,
    "tercer_sector": 4,
    "academico": 2,
    "judicial": 1
  },
  "by_political_bloc": {
    "gobierno_actual_consell": 12,
    "oposicion_izquierda": 11,
    "oposicion_centro_derecha": 5,
    "sin_adscripcion_partidista": 14
  },
  "by_palanca": {...},
  "alerts": []
}
```

Se escribe a `private/balance.md` (consulta del editor) y se sirve en `/balance` (público).

---

## Módulos — detalle

### `src/ingest.py`

Cambios mínimos:

- Añadir parámetro opcional `--window-start YYYY-MM-DD --window-end YYYY-MM-DD` para ejecución de ventanas temporales retroactivas (necesario para Fase 0 contenido retroactivo W14-W15).
- Conservar dedup por URL y título.

### `src/classify.py`

Cambios:

- Schema ampliado con `has_explicit_proposal`, `proposal_actor_hint`, `proposal_actor_type_hint`.
- Prompt de Haiku actualizado para detectar propuestas explícitas (patrones: "X propone", "X reclama", "X solicita", "X presenta moción", "X rechaza", "X pide").
- Resiliencia ante respuesta corta (si devuelve menos items que input, loguea y sigue con los válidos).

### `src/extract.py` (nuevo)

Responsabilidad única: para cada item con `has_explicit_proposal=true`, invocar a Haiku con prompt que extraiga la ficha estructurada completa.

Prompt resumido (ver implementación detallada):

```
Eres un analista que extrae propuestas explícitas de noticias de vivienda en Ibiza.
Para cada noticia te paso, identifica las propuestas concretas que un actor con
nombre ha hecho. Devuelve JSON con la estructura exacta del schema descrito.

Si la noticia menciona algo general tipo "se habla de residencias para temporeros"
sin un actor concreto que lo proponga, devuelve lista vacía. No inventes actores.

Regla dura: statement_verbatim debe ser texto literal de la noticia o resumen
fiel sin añadir interpretación. url_source obligatorio.
```

Input: lista de items con `has_explicit_proposal=true`. Output: lista de propuestas estructuradas, puede ser 0-N por item.

Dedup entre items: si dos noticias reportan la misma propuesta del mismo actor, se consolidan (una sola entrada con múltiples `url_source`).

Append a `data/proposals_history.json` (lista completa histórica para tracker y rescate).

### `src/rescue.py` (nuevo)

Responsabilidad única: seleccionar candidatas a rescate de ediciones previas.

1. Lee `data/proposals_history.json`.
2. Filtra por criterios duros (listados arriba).
3. Ranking por: recencia inversa + frescura del actor (si el actor lleva ≥4 semanas sin aparecer en ninguna edición) + impacto potencial (heurística simple: más supporters_cited + menos opponents_cited).
4. Devuelve top 3-5 al generator, que elige 1-2.

### `src/generate.py` (reescrito)

Responsabilidad: componer la edición markdown a partir de input estructurado.

Prompt SYSTEM documental nuevo (borrador):

```
Eres el documentalista de Ibiza Housing Radar. Recibes propuestas ya extraídas
y verificadas. Tu trabajo es ORDENAR, CRUZAR Y PRESENTAR ese contenido en formato
edición semanal. No generas propuestas propias. No valoras. No opinas.

Estructura obligatoria: señales, cronología, mapa de posiciones, propuestas en
circulación, rescate, omisiones, a vigilar.

Verbos permitidos: propone, reclama, rechaza, presenta, solicita, exige, pide,
plantea, anuncia, dice, señala, denuncia, reitera, confirma, prevé.

Verbos prohibidos: debería, convendría, sería oportuno, hace falta, urge,
proponemos, habría que, toca, corresponde, es necesario.

Cada enlace markdown debe llevar a una URL REAL del input. Nunca inventes.
Cada cifra debe estar en el input. Nunca redondees al alza ni a la baja sin
declararlo.

Si en una semana no hay propuestas explícitas en el input, escribe honestamente
"esta semana no se han registrado propuestas formales en circulación" y amplía
la sección de rescate y omisiones. No rellenes.

Output: markdown con frontmatter Jekyll. Sin saludos. Sin despedidas. Sin firma.
```

Temperature baja (0.2-0.3). Max tokens 8192. Model `claude-opus-4-7`.

### `src/verify.py` (nuevo)

Corre tras `generate.py` y antes del commit/publish.

Checks:

1. `requests.head(url, timeout=10)` por cada URL del markdown. Si no 200, fallo bloqueante.
2. Cada actor citado en la edición debe aparecer como `proposal_actor` o `supporters_cited` o `opponents_cited` en el `extract.py` output.
3. Cada precedente externo de la edición (si existe; los documentales NO los generan, pero si el rescate los arrastra, los incluye) pasa a fact-check Haiku: *"¿existe este programa con este nombre y esta cifra con alta confianza? Devuelve exacto / aproximado / dudoso / no encontrado."*
4. Grep de lista negra de verbos.
5. Check "toda propuesta tiene actor identificado".

Output: `verification_report.json` + exit code. Si blocking, notifica Telegram con detalles y no publica.

### `src/balance.py` (nuevo)

Corre tras publicar (en report.py), o independiente para auditoría.

1. Lee `docs/_editions/*.md` y extrae frontmatter (`actors_cited`, `blocks_cited`, `proposals_count`).
2. Agrupa por ventanas: 30, 90, 180, 365 días.
3. Calcula reparto absoluto y relativo.
4. Genera alertas si algún bloque > 50% en ventana 90d durante 2+ meses.
5. Escribe `private/balance.md` (privado) y `docs/balance.md` (público).

### `src/self_review.py` (nuevo — autoevaluación semanal)

Corre inmediatamente después de publicar la edición. Responsabilidad: verificar que la edición recién publicada cumple los estándares del pivote y alertar si no.

Input: edición recién escrita + 3 ediciones anteriores + las 5 reglas duras literales.

Modelo: **Sonnet 4.6** (no Opus — suficiente aquí y 5× más barato).

Prompt (resumido):

```
Eres un revisor interno del observatorio. Analiza la edición recién
publicada contra las 5 reglas duras y devuelve JSON con:

- score_reglas (1-10): cumplimiento de las reglas duras.
- score_rigor (1-10): calidad factual (cifras trazables, actores con nombre).
- score_balance (1-10): diversidad de actores en la edición.
- score_cobertura (1-10): ¿cubre los hechos importantes de la semana?
- score_claridad (1-10): legibilidad sin perder densidad.
- warnings: lista de problemas concretos detectados.
- suggestions: 0-3 ajustes al prompt si detectas patrón degradado.
```

Output: `private/self-review/YYYY-wWW.md`.

Si cualquier score < 7 → **Telegram urgente con link** al archivo. Editor revisa.

Si todos ≥ 7 → silencio.

Coste estimado: ~0,15 €/edición ≈ 0,60 €/mes.

### `src/quarterly_audit.py` (nuevo — auditoría trimestral)

Corre cada 13 semanas (programado en GitHub Action separado).

Input: 13 ediciones publicadas + 13 self-reviews + balance acumulado + `proposals_history.json`.

Modelo: **Opus 4.7** (única fase donde se justifica razonamiento profundo sobre corpus extenso).

Prompt (resumido):

```
Eres un auditor externo del observatorio. Revisa las 13 ediciones del
trimestre. Evalúa:

1. Cumplimiento sostenido de las 5 reglas duras (regresión vs trimestre
   anterior).
2. Patrones emergentes (temas recurrentes, actores nuevos, propuestas
   zombies).
3. Calidad editorial evolutiva (comparativa con trimestre anterior si
   existe).
4. Recomendaciones concretas: ajustar prompt, añadir/retirar fuentes RSS,
   modificar criterios de admisión.
5. Señales sistemáticamente perdidas (hechos importantes que el pipeline
   no detectó pero deberían haberlo sido).

Devuelve un informe en markdown de 800-1500 palabras, tono directo,
publicable tal cual.
```

Output: **público** en `docs/_auditorias/YYYY-qN.md`, accesible en `/auditoria/YYYY-qN/`. Transparencia radical: el proyecto se audita a sí mismo en abierto.

Coste estimado: ~3-5 €/trimestre ≈ 1,50 €/mes promediado.

### `src/model_rebench.py` (nuevo — re-benchmark mensual de modelos)

Corre cada 4 semanas (programado).

Dataset: 10 noticias nuevas del mes recién cerrado.

Ejecuta las 6 tareas del pipeline con los 3 modelos contra gold standard generado con Opus + razonamiento extendido.

Output: `private/bench/YYYY-MM.csv` + alerta Telegram si:

- Ratio calidad/coste de algún modelo cambia >20% vs línea base.
- Aparece un modelo nuevo de Anthropic (detectar manualmente cada 4 semanas).
- Precios cambian (leer desde API si exponen endpoint, o chequeo manual).

Coste estimado: ~1 €/mes.

### `src/report.py` (adaptado)

Orquestador:

```python
def main():
    items = ingest(window=args.window)
    classified = classify(items)
    extracted = extract(classified)
    rescue_candidates = rescue()
    generated_md = generate(classified, extracted, rescue_candidates)
    verification = verify(generated_md, extracted)
    if verification.blocking_failures:
        notify_critical(verification)
        sys.exit(1)
    write_edition(generated_md)
    balance()
    notify_ok()
```

---

## Tests propuestos

Fase 0 no requiere cobertura exhaustiva pero sí un mínimo que garantice que el pipeline no se rompe al cambiar algo.

1. **Smoke test** con dataset fake (`tests/fixtures/`): 3 noticias, 1 con propuesta explícita. Mock de Anthropic que devuelve respuestas predecibles. Verifica que el pipeline completo produce una edición markdown válida.
2. **Test de `extract.py`** con 5 noticias reales curadas: verifica que no alucina URLs.
3. **Test de `verify.py`**: dataset con una URL rota → debe bloquear; dataset con verbo prohibido → debe bloquear; dataset limpio → pasa.
4. **Test de `rescue.py`**: con `proposals_history.json` de 16 semanas fake, verifica que selecciona solo candidatos que cumplan los 4 criterios duros.
5. **Test de `balance.py`**: con 13 ediciones fake, verifica que el reparto se calcula correctamente y que la alerta dispara si un bloque > 50%.

Ubicación: `tests/` en raíz del repo. Framework: `pytest`.

---

## Migración desde el código actual

No se mantiene backwards compatibility. El modelo antiguo queda en el histórico git de `main` y se puede consultar ahí si hace falta.

Pasos:

1. Crear módulos nuevos en `src/` sin tocar los existentes.
2. Reescribir `generate.py` como `generate.py.new` al principio y probar en paralelo.
3. Una vez probado, swap: `generate.py.new → generate.py`.
4. Ejecutar pipeline completo contra W16 con el nuevo modelo en un directorio temporal, comparar output con la edición actual, validar diferencias.
5. Si OK, ejecutar sobre W14-W17 en sucesión para contenido retroactivo.
6. Merge del branch a main.

---

## Coste API estimado bajo el nuevo pipeline (con los 3 niveles de autoevaluación)

| Fase | Modelo | Coste/edición (€) |
|---|---|---|
| Clasificación | Haiku | 0,015 |
| Detección de propuestas | Haiku | 0,010 |
| Extracción estructurada | Sonnet | 0,18 |
| Rescate (verificación de vigencia) | Haiku | 0,005 |
| Fact-check de precedentes | Sonnet | 0,08 |
| Generación | Opus 4.7 (con prompt caching) | 1,40 |
| Verificación técnica (URLs, verbos) | — (no LLM) | 0 |
| Self-review semanal | Sonnet | 0,15 |
| **Total/edición** | | **~1,84 €** |
| **Total/mes (4 ediciones de operación)** | | **~7,36 €** |
| Auditoría trimestral (promedio/mes) | Opus | 1,50 |
| Re-benchmark de modelos (mes) | Mixto | 1,00 |
| **Total mensual proyectado** | | **~9,86 €** |

**Cruce de tope blando:** el nuevo coste proyectado (~9,86 €/mes) cruza el tope blando actual de 8 €. Decisión derivada (pendiente de confirmar): **subir tope blando a 12 €** manteniendo la misma filosofía ("avisa pero publica"). Nuevo sistema de capas propuesto:

| Capa | Umbral | Acción |
|---|---|---|
| 🟢 Verde | < 6 € | Silencio |
| 🟡 Amarilla | 6-9 € | Telegram FYI |
| 🟠 Naranja | 9-12 € | Telegram atención |
| 🔴 Roja blanda | 12-20 € | Telegram urgente, pipeline sigue publicando |
| 🚨 Roja dura | > 20 € | Corte, alerta crítica (protección runaway) |

Cuando se active trilingüe (Fase 4 diferida), subirá a ~13-14 €/mes cruzando la capa naranja. Revisar tope duro en ese momento.
