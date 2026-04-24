# DISENO-AUDITOR.md — Diseño sobre papel del auditor mínimo viable

> Diseño concreto antes de tocar código. Deriva de [ESTUDIO-COSTES-AUDITOR.md §10](ESTUDIO-COSTES-AUDITOR.md) y de las decisiones [D1](DECISIONES.md), [D2](DECISIONES.md), [D3](DECISIONES.md) y [D5](DECISIONES.md).
>
> Vivo. Se va cerrando por turnos:
> - **Turno 1** (este) — piezas 1 y 2: contrato de módulos y estructura del registro.
> - **Turno 2** — piezas 3 y 4: árbol de decisión y encaje en el flujo.
> - **Turno 3** — piezas 5 y 6: ejemplo trazado y preguntas pendientes.

---

## 1 · Contrato de los tres módulos

Si estos contratos están claros, el código después es mecánico.

### 1.1 · `src/audit.py` — auditoría ciega con Sonnet

- **Recibe** el mismo lote de noticias que recibió Haiku en la extracción primaria. Sin pistas del resultado de Haiku. De ahí "ciega".
- **Devuelve** una ficha por noticia con la misma estructura que Haiku (actor, palanca, tipo, viabilidad, cita textual, URL de la cita).
- **Efecto lateral** — apunta el coste de la llamada en `data/costs.csv`.
- **Falla suave** — si la API no responde tras un reintento, marca la ficha como `skipped_by_timeout` y deja al resto del flujo seguir.

### 1.2 · `src/audit_compare.py` — comparador determinista

- **Recibe** dos fichas con la misma estructura (Haiku y Sonnet).
- **Devuelve** la lista de campos donde difieren y un veredicto global: `match` / `minor` / `major` / `mismatch`.
- **Efecto lateral** — ninguno. Función pura.
- **Falla dura** — si las estructuras no encajan, error del programador.

### 1.3 · `src/audit_heuristics.py` — tres comprobaciones sin IA

- **Recibe** la propuesta final (la que va a publicarse), el lote completo de noticias de la semana y el archivo de dominios oficiales por actor.
- **Devuelve** cuatro señales independientes:
  - **Cruce de fuentes** — cuántas fuentes distintas hablan de la propuesta.
  - **Coincidencia literal** — qué parte de la cita aparece literal en el texto original.
  - **Dominio del actor** — si la URL de la cita coincide con un dominio oficial conocido del actor.
  - **Plausibilidad de la viabilidad** — si la viabilidad declarada encaja con el tipo de propuesta (p. ej. "ley estatal" marcada como "viable en 3 meses" → señal en rojo).
- **Efecto lateral** — ninguno.
- **Falla suave** — cada señal tiene salida "no calculable" que el flujo entiende.

---

## 2 · Estructura del registro de auditoría

Cada propuesta publicada deja un expediente. Un archivo por propuesta en `data/audit/YYYY-wWW/{proposal_id}.json`. Append-only: se crea al publicar y solo se le añaden correcciones; el contenido original nunca se edita.

### 2.1 · Ejemplo

```json
{
  "proposal_id": "2026-w17-consell-pph-01",
  "edition": "2026-w17",
  "created_at": "2026-04-20T05:14:22Z",

  "tier": {
    "value": null,
    "reason": "pendiente implementación del módulo de tiers",
    "signals": {
      "consensus_ia": "minor",
      "cross_source": {"hit": false, "n_sources": 1},
      "verbatim_match": {"ratio": 0.82},
      "whitelist_hit": {"matches": true},
      "viability_sanity": {"plausible": true},
      "arbitraje_opus": {"invoked": false, "outcome": null}
    }
  },

  "layers": {
    "haiku":        {"extraction": "...", "cost_eur": 0.0012},
    "sonnet_blind": {"extraction": "...", "cost_eur": 0.0087},
    "compare":      {"diffs": [], "severity": "minor"},
    "heuristics":   "..."
  },

  "verify": {"url_ok": true, "actor_traceable": true, "forbidden_verbs": []},

  "corrections": [],

  "timestamps": {
    "haiku_at": "...", "sonnet_at": "...", "compare_at": "...",
    "heuristics_at": "...", "verify_at": "..."
  }
}
```

### 2.2 · Por qué cada bloque

- **`proposal_id`** — identificador estable que vive en URL, registros y correcciones. Formato: `YYYY-wWW-{actor-corto}-{palanca}-{nn}`.
- **`tier`** — hueco preparado desde el día uno. `value` nace vacío; las seis señales se acumulan igual. Cuando se implemente el módulo de tiers, solo se enchufa la función que lee `signals` y escribe `value`. Cero migración.
- **`layers`** — resultado crudo de cada capa. Si algo sale raro en producción, el expediente tiene todo para reproducir.
- **`verify`** — las tres verificaciones clásicas del proyecto. Ya existen; el auditor solo las recoge aquí.
- **`corrections`** — vacío al nacer. Cada petición externa añade un objeto con fecha, origen, cuerpo y resolución. El JSON original nunca se toca.
- **`timestamps`** — cuándo ocurrió cada paso. Sirve para medir tiempos reales y detectar cuellos de botella.

---

## 3 · Árbol de decisión: qué publica, qué escala, qué se cuarentena

Tres preguntas en orden. La primera que responde "sí" corta el árbol.

### 3.1 · ¿Hay bloqueante?

Cuatro motivos bloquean la publicación y mandan la propuesta a cuarentena:

1. **Estructuras incompatibles** — el comparador devuelve `mismatch` (actor o palanca distintos entre Haiku y Sonnet). No es un desacuerdo fino: es que una de las dos no entendió la noticia.
2. **URL muerta** — `verify.url_ok == false`.
3. **Actor no identificable** — `verify.actor_traceable == false`.
4. **Verbos prohibidos en la cita** — `verify.forbidden_verbs` no vacío.

Una propuesta bloqueada se escribe igual en `data/audit/YYYY-wWW/{id}.json` con `status: "quarantined"` y motivo explícito. No aparece en la edición publicada. Queda disponible para el protocolo de correcciones y para el repaso mensual futuro.

### 3.2 · ¿Hay disputa entre las dos extracciones?

Si el comparador devuelve `major` (diferencias en viabilidad, tipo o cita, sin llegar a ser incompatibles), se escala al fallback de Opus que **ya existe** en `extract.py` hoy. En mínimo viable no hay capa 4 separada; se reutiliza.

Opus recibe las dos fichas y la noticia original. Tres salidas posibles:

- **Resuelve a favor de Haiku** → ficha canónica = Haiku. Publica.
- **Resuelve a favor de Sonnet** → ficha canónica = Sonnet. Publica.
- **Resuelve que ninguna es correcta** → cuarentena con motivo `opus_rejected_both`.

La salida de Opus se guarda en `signals.arbitraje_opus` del registro para alimentar el futuro nivel de confianza.

### 3.3 · Resto de casos → publica

Si el comparador devuelve `match` o `minor`, la ficha canónica es la de Haiku (por coste). Las diferencias menores quedan registradas en `layers.compare.diffs` pero no bloquean.

### 3.4 · Las cuatro heurísticas corren siempre

Independientemente de si hay bloqueante, disputa o publicación directa. Sus señales se guardan en `tier.signals` aunque la propuesta vaya a cuarentena. El módulo futuro de tiers las necesitará tanto para colorear las publicadas como para proponer rescates desde cuarentena.

---

## 4 · Encaje en el flujo general

El pipeline actual, de izquierda a derecha:

```
ingest → classify → extract → verify → balance → generate → archive
```

Con auditor mínimo viable:

```
ingest → classify → extract ─┬─► audit (Sonnet ciego)
                             │
                             ├─► compare (Haiku vs Sonnet)
                             │
                             ├─► heuristics (4 señales sin IA)
                             │
                             └─► [si major] opus_fallback (ya existe)
                                        │
                                   verify → write_audit_log → balance → generate → archive
```

### 4.1 · Módulos nuevos

- **`src/audit.py`** — llama a Sonnet ciego y escribe el expediente final (`write_audit_log`).
- **`src/audit_compare.py`** — compara fichas.
- **`src/audit_heuristics.py`** — calcula las cuatro señales.
- **`data/actor_domains.yml`** — whitelist inicial de 15-20 actores con sus dominios oficiales ([D3](DECISIONES.md)).
- **`data/audit/YYYY-wWW/`** — carpeta nueva donde se escriben los expedientes.

### 4.2 · Módulos existentes que hay que tocar

- **`src/report.py`** (orquestador) — añade las llamadas al auditor entre `extract` y `verify`, y la escritura del expediente al final de cada propuesta. Es el cambio más largo, pero es pegado de llamadas, no lógica nueva.
- **`src/self_review.py`** — añade dos chequeos de salud semanales: ratio de disputas (sano entre 8 % y 25 %, según [§12](ESTUDIO-COSTES-AUDITOR.md)) y ratio de cuarentena. Si alguno se dispara, alerta por Telegram.

### 4.3 · Qué NO se toca en mínimo viable

- `extract.py` — el fallback Opus que ya tiene se reutiliza tal cual; no se extrae a capa propia todavía.
- `verify.py` — se llama en otro orden, pero la lógica interna no cambia.
- `balance.py`, `generate.py`, `archive.py` — invariantes.

Esto limita la superficie de cambio a código nuevo + dos archivos existentes tocados. Cabe en las dos semanas calendario del hito.

---

## 5 · Ejemplo trazado

Ejemplo inventado pero plausible para validar que el diseño cubre todos los campos.

**Noticia de partida.** "CCOO Ibiza y PIMEEF exigen al Consell una bolsa de alquiler público para trabajadores de temporada" — Diario de Ibiza, 19 abr 2026.

### Paso a paso

1. **`ingest`** — la noticia entra en `ingested.json`.
2. **`classify` (Haiku)** — `is_housing=true`, `actor_guess="sindicato"`, `has_explicit_proposal=true`.
3. **`extract` primaria (Haiku)** — ficha: actor *CCOO*, palanca *bolsa de alquiler público*, tipo *exigencia*, viabilidad *requiere activación IBAVI*, cita literal, URL del Diario.
4. **`audit` ciega (Sonnet)** — ficha con matiz: co-firmante PIMEEF que Haiku se saltó. Resto idéntico.
5. **`compare`** — `severity="minor"`. Diff registrado en `actor` (Haiku: *CCOO* / Sonnet: *CCOO + PIMEEF*). Cita y palanca idénticas.
6. **`heuristics`** — cuatro señales:
   - *cross_source* → `{hit: true, n_sources: 2}` (Periódico de Ibiza también lo cubre).
   - *verbatim_match* → `{ratio: 0.91}` (cita casi literal).
   - *whitelist_hit* → `{matches: false, expected: ["ccoo.cat", "pimeef.org"], actual: "diariodeibiza.es"}`. La noticia viene de medio, no del actor. Ausencia normal, cross_source compensa.
   - *viability_sanity* → `{plausible: true}`.
7. **Árbol de decisión** — sin bloqueantes; `minor` no escala. Publica. Ficha canónica = Haiku; el diff del co-firmante queda registrado pero no corrige (ver [Q3](#q3)).
8. **`verify`** — url viva, actor trazable, sin verbos prohibidos.
9. **`write_audit_log`** — expediente a `data/audit/2026-w17/2026-w17-ccoo-alquiler-01.json`.
10. **`balance` + `generate` + `archive`** — sin cambios.

### Cómo cambia si...

- **URL muerta** → `status: "quarantined", reason: "url_ok=false"`. Expediente se guarda igual.
- **`compare="major"`** → llamada al Opus fallback existente; salida en `signals.arbitraje_opus`.
- **`compare="mismatch"`** → cuarentena directa sin pasar por Opus.

---

## 6 · Preguntas pendientes antes de tocar código

Cuatro decisiones para cerrar con el editor.

### Q1 — Umbrales iniciales: ¿código o YAML?

Las heurísticas necesitan números: ratio de coincidencia literal que cuenta como *match* vs *minor*, cuántas fuentes cuentan como cruce, etc.

- **A · Hard-coded en el módulo.** Simple. Para cambiar hay que tocar código.
- **B · En `data/audit_thresholds.yml` desde el día uno.** El editor afina tras la prueba empírica sobre W10 sin tocar Python.

**Recomiendo B.** La semana 4 del hito es precisamente para calibrar.

### Q2 — Si Sonnet no responde (timeout/error)

- **A · Cuarentena automática.** Sin dos extracciones no hay auditoría.
- **B · Publica solo con Haiku, marca señal `sonnet_missing`.** El módulo futuro de tiers decidirá si eso baja el color.

**Recomiendo B.** Si los fallos son sistemáticos, `self_review` alerta por Telegram.

### Q3 — En `minor`, ¿ficha canónica Haiku o Sonnet?

En el ejemplo: Sonnet detectó un co-firmante que Haiku se saltó. ¿Qué se publica?

- **A · Siempre Haiku.** El diff se registra, no corrige. Sonnet es vigía, no editor.
- **B · Siempre Sonnet.** Más fino, más caro.
- **C · Lo decide el comparador.** Complicado.

**Recomiendo A.** Si queremos corrección fina, subimos a Opus (ya arbitra en `major`).

### Q4 — ¿Los expedientes son públicos en el repo?

- **A · Públicos en GitHub** (cualquiera los ve).
- **B · Privados en el repo, solo `/correcciones/` expone lo necesario.**

**Recomiendo A.** Coherente con [D2](DECISIONES.md) (registro público desde el día uno).
