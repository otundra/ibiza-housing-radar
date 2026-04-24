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
