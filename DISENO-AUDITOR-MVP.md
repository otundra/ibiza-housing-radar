# Diseño del auditor — Mínimo viable

**Fecha:** 2026-04-24
**Estado:** ACTIVO (plano de obra durante las 4 semanas de construcción)
**Horizonte:** 4 semanas calendario / ~30-40 h editor
**Referencia cerrada:** [ESTUDIO-COSTES-AUDITOR.md](ESTUDIO-COSTES-AUDITOR.md) (qué y cuánto)
**Decisiones que lo enmarcan:** [D1](DECISIONES.md) (partición MVP + iteración), [D2](DECISIONES.md) (log público + correcciones), [D3](DECISIONES.md) (whitelist V1), [D4](DECISIONES.md) (tests diferidos), [D5](DECISIONES.md) (tiers en paralelo), [D6](DECISIONES.md) (marco de hitos), [D9](DECISIONES.md) (tiers cerrado).

Este documento es el **plano de obra** del auditor mínimo viable. El estudio de costes del 22-abr cerró el *por qué* y el *cuánto*; aquí va el *cómo* concreto: contratos de módulos, estructura exacta del registro de auditoría, árbol de heurísticas, whitelist V1 cerrada, integración con el pipeline y criterios de cierre.

> **Uso del documento.** Referencia viva durante la construcción. Entregables con `[ ]` se marcan `[x]` al cerrar. No es decisional: las decisiones siguen en [DECISIONES.md](DECISIONES.md). Se archiva como histórico cuando el Hito 1 cierre.

---

## 1 · Resumen operativo

**Qué construimos en el MVP** (2 semanas de alcance según D1, ampliado a 4 con integración + prueba empírica):

- Capa 2 auditoría ciega con Sonnet 4.6 sobre el mismo prompt que Haiku.
- Comparador determinista campo a campo (Python puro).
- 3 heurísticas sin IA: cruce de fuentes, coincidencia textual verbatim, encaje dominio-actor.
- Registro público por propuesta en `data/audit/YYYY-wWW/{id}.json` con campo `corrections` append-only.
- Whitelist V1 cerrada en `data/actor_domains.yml` (20 actores).
- Integración con el pipeline existente (nuevo paso entre extracción y generación).
- Página `/correcciones/` como plantilla Jekyll mínima, enlazada desde el footer.

**Coste neto proyectado:** +0,20 €/mes sobre el pipeline actual. Régimen estable ~2,35 €/mes (verde holgada). Detalle y sensibilidad en [ESTUDIO-COSTES-AUDITOR.md §4-§8](ESTUDIO-COSTES-AUDITOR.md).

**Qué queda fuera del MVP** (iteración posterior, 2-3 sem adicionales, ver §8):

- Capa 4 Opus formalizada como paso separado (hoy es fallback implícito en `src/extract.py`).
- Página navegable `/revision-pendiente/` (cuarentena pública).
- Tablero público `/auditor/` con métricas.
- Repaso mensual por IA de la cuarentena (capa 5bis).
- Formulario funcional con webhook en la página de correcciones.
- Función `compute_tier(signals) -> color` real. El MVP escribe `tier.value = null` siempre y deja el bloque `signals` poblado para que PI10 lo conecte cuando llegue.

**Dependencias externas del MVP:**

- **Prototipo HTML del Bloque B** está pausado desde 2026-04-21. La página `/correcciones/` se crea como plantilla Jekyll aparte, sin tocar el prototipo. Integración visual cuando el editor reabra ese bloque.
- **Buzón de email del proyecto** queda diferido hasta el cierre del nombre del observatorio (D2). En `/correcciones/` se anuncia *"próximamente"* con ruta alternativa (issue en GitHub).
- **Estudio legal del titular** es Hito 3 (D6). La exposición del protocolo se revisa al cerrar ese hito. Apuntado también en STATUS.md.

**Cierre del Hito 1:** prueba empírica sobre la semana W10 (2-8 marzo 2026) con el auditor activo y log visible, sin fallos bloqueantes. D1 revisa el MVP tras esa prueba. Sin fecha de calendario ([D15](DECISIONES.md)).

---

## 2 · Módulos nuevos y sus funciones

### 2.1 · `src/audit.py` — Orquestador

**Propósito.** Coordinar las 5 capas del auditor (capas 1 y 4 ya existen; 2, 3a, 3b y el log se añaden aquí) sobre las propuestas extraídas. Devolver flujo enriquecido al `generate()` actual.

**Funciones públicas.**

```python
def audit_proposals(
    proposals: list[Proposal],
    news: dict[str, NewsItem],
    actor_domains: dict,
) -> AuditedProposals:
    """Ejecuta el auditor completo sobre las propuestas extraídas.

    Orquesta: capa 2 Sonnet ciega → capa 3 comparador + verify + heurísticas →
    escribe log JSON por propuesta → devuelve flujo enriquecido.
    En el MVP, tier.value queda null siempre; las señales se pueblan.
    """

def run_blind_audit(
    proposals: list[Proposal],
    news: dict,
) -> list[BlindExtraction]:
    """Capa 2. Una única llamada batch Sonnet con EXTRACT_SYSTEM sobre el
    mismo payload que Haiku, sin ver el output de capa 1."""

def write_audit_log(
    result: AuditedProposals,
    week: str,  # formato "2026-w17"
) -> None:
    """Escribe un JSON por propuesta en data/audit/{week}/{proposal_id}.json.
    Append-only: si el archivo existe, aborta con error (no sobreescribe)."""

def compute_tier(signals: dict) -> dict:
    """Hueco reservado en el MVP. Devuelve siempre:
    {value: null, reason: 'pendiente_estudio', signals: signals}.
    En la iteración posterior (PI10) lee signals y devuelve color real."""
```

**Importa.**

- `src.extract` — reutiliza `EXTRACT_SYSTEM` prompt.
- `src.costs` — registro de llamadas API.
- `src.audit_compare.compare_extractions`.
- `src.audit_heuristics.run_heuristics`.
- `src.verify` — los 5 checks existentes se incorporan al log sin duplicar lógica.

### 2.2 · `src/audit_compare.py` — Comparador determinista

**Propósito.** Comparar capa 1 (Haiku) vs capa 2 (Sonnet) campo a campo y clasificar los diffs por severidad.

**Funciones públicas.**

```python
def compare_extractions(a: Proposal, b: Proposal) -> CompareResult:
    """Devuelve:
    {
      'identical': bool,
      'severity': 'critical' | 'minor' | 'none',
      'diffs': [{'field': str, 'a': any, 'b': any, 'reason': str}],
    }
    """
```

**Árbol de severidad.**

- **Campos críticos** (cualquier diff → `critical`):
  - `actor`, `target_actor`, `palanca`, `state`, `url_source`.
- **Campo con umbral textual** (diff según ratio):
  - `statement_verbatim`: si `SequenceMatcher` ratio < 0.85 → `critical`; entre 0.85 y 0.95 → `minor`; ≥ 0.95 → no diff.
- **Campos menores** (diffs → `minor`):
  - `viability_economic`, `viability_political`, `viability_tecnica`, `horizon`, `statement_type`.
- **Sin diffs en ningún campo crítico ni menor** → `severity: none`, `identical: true`.

**Qué importa.** Solo stdlib (`difflib` para ratio textual).

### 2.3 · `src/audit_heuristics.py` — Heurísticas sin IA

**Propósito.** Aplicar las 3 heurísticas del MVP sobre cada propuesta. Sin llamadas a modelos IA. Alimenta el bloque `signals` del registro.

**Funciones públicas.**

```python
def run_heuristics(
    proposal: Proposal,
    news: dict,
    actor_domains: dict,
) -> HeuristicResult:
    """Agrega las 3 señales del MVP. Devuelve:
    {
      'cross_source': {...},
      'verbatim_match': {...},
      'whitelist': {...},
    }
    """

def check_cross_source(proposal: Proposal, news: dict) -> dict:
    """Cuenta URLs de dominios distintos que cubren la misma propuesta
    (mismo actor + misma palanca + mismo target_actor)."""

def check_verbatim_match(proposal: Proposal) -> dict:
    """Descarga HTML de url_source (caché local 30 días), extrae texto
    plano, aplica SequenceMatcher sobre statement_verbatim.
    Umbrales: quote ≥0.95, reported ≥0.60 (mínimo) / ≥0.80 (🟢)."""

def check_whitelist(proposal: Proposal, actor_domains: dict) -> dict:
    """Clasifica el dominio de url_source respecto al actor:
    refuerza (dominio oficial del actor) / neutro (medio aceptado) /
    debilita (dominio no verificado)."""
```

**Heurísticas descritas en el estudio pero no implementadas aparte en el MVP:**

- **Single-source penalty.** Queda codificada como señal: `n_fuentes_independientes == 1` implica techo 🟡. La regla se aplicará cuando `compute_tier()` real exista (PI10). En el MVP solo se registra el valor.
- **Viability sanity.** Codificada como señal `viability_con_cifra`. Si `viability_economic ∈ {alta, media}` y no hay cifra numérica en `statement_verbatim` ni en la noticia, `viability_con_cifra = false`. En el MVP se registra; el ajuste automático a `no_evaluada` se aplica en PI10.

**Qué importa.**

- `requests` + caché local simple (archivos en `.cache/http/` con TTL 30 días, clave = hash de URL).
- `lxml` o `beautifulsoup4` (elegir en semana 2; preferencia `lxml` por rendimiento).
- `difflib` (stdlib).
- `pyyaml` para `data/actor_domains.yml`.

### 2.4 · `data/actor_domains.yml` — Whitelist V1

**Propósito.** Mapear cada actor conocido a sus dominios oficiales + lista curada de medios de cobertura aceptada. Leído por `check_whitelist`. Curado manualmente en V1 ([D3](DECISIONES.md)); refinamiento post-backfill.

**Esquema.**

```yaml
meta:
  version: 1
  last_updated: 2026-04-24
  criterio: 15-20 actores principales del dominio público vivienda Ibiza

medios_cobertura_aceptada:
  - <dominio>
  ...

actors:
  <nombre_actor>:
    oficial:
      - <dominio_oficial>
    # opcional: medios de cobertura que suelen cubrir a este actor
    cobertura_aceptada:
      - <dominio>
```

Lista completa V1 en §5.

---

## 3 · Estructura del registro de auditoría

Un archivo JSON por propuesta en `data/audit/YYYY-wWW/{proposal_id}.json`. Append-only: no se edita una vez escrito. Las correcciones se añaden al bloque `corrections`, nunca se sobreescribe el original. Público: expuesto en `/auditor/` (iteración posterior) y enlazado desde cada propuesta publicada cuando el bloque del auditor se integre en las ediciones.

### 3.1 · Esquema completo

```json
{
  "proposal_id": "2026-w17-001",
  "week": "2026-w17",
  "created_at": "2026-04-20T10:15:00Z",

  "tier": {
    "value": null,
    "reason": "pendiente_estudio",
    "signals": {
      "ia_consenso": "completo",
      "arbitraje": "no_hubo",
      "url_ok": true,
      "traza_dominio_actor": true,
      "fecha_coherente": true,
      "verbatim_match_ratio": 0.87,
      "wayback_snapshot": true,
      "n_fuentes_independientes": 2,
      "whitelist_match": "refuerza",
      "viability_con_cifra": true,
      "statement_type": "reported"
    }
  },

  "corrections": [],

  "layers": {
    "haiku": {
      "model": "claude-haiku-4-5",
      "extracted_at": "2026-04-20T10:12:00Z",
      "proposal": { "...ficha completa..." }
    },
    "sonnet_blind": {
      "model": "claude-sonnet-4-6",
      "extracted_at": "2026-04-20T10:13:00Z",
      "proposal": { "...ficha completa..." }
    },
    "compare": {
      "identical": false,
      "severity": "minor",
      "diffs": [
        {"field": "viability_economic", "a": "alta", "b": "media", "reason": "diff_enum"}
      ]
    },
    "heuristics": {
      "cross_source": {
        "n_fuentes_independientes": 2,
        "urls": ["diariodeibiza.es/...", "periodicodeibiza.es/..."]
      },
      "verbatim_match": {
        "ratio": 0.87,
        "statement_type": "reported",
        "threshold_blocking": 0.60,
        "threshold_green": 0.80,
        "passed_blocking": true,
        "passed_green": true
      },
      "whitelist": {
        "match": "refuerza",
        "domain": "conselldeivissa.cat",
        "known_actor": true
      }
    }
  },

  "verify": {
    "url_ok": true,
    "http_status": 200,
    "checked_at": "2026-04-20T10:14:00Z",
    "wayback_snapshot": "https://web.archive.org/web/20260420/...",
    "traza_dominio_actor": true,
    "fecha_coherente": true,
    "verbos_prohibidos_detectados": []
  },

  "timestamps": {
    "haiku_ms": 1820,
    "sonnet_blind_ms": 2310,
    "heuristics_ms": 45,
    "verify_ms": 890,
    "total_ms": 5065
  }
}
```

### 3.2 · Estado de cada señal en el MVP

| Señal | Tipo | Fuente | Estado MVP |
|---|---|---|---|
| `ia_consenso` | enum {completo, parcial, disputa} | `compare.severity` | ✅ Se calcula |
| `arbitraje` | enum {no_hubo, opus_confirma_*, opus_discrepa_ambas} | Capa 4 Opus | ⏳ Siempre `no_hubo` en MVP (capa 4 formal = iteración) |
| `url_ok` | bool | `verify.py` existente | ✅ Ya se calcula |
| `traza_dominio_actor` | bool | `check_whitelist` + `verify.py` | ✅ Se calcula |
| `fecha_coherente` | bool | `verify.py` | ✅ Ya se calcula |
| `verbatim_match_ratio` | float [0,1] | `check_verbatim_match` | ✅ Se calcula |
| `wayback_snapshot` | bool | `verify.py` | ✅ Ya se calcula |
| `n_fuentes_independientes` | int ≥1 | `check_cross_source` | ✅ Se calcula |
| `whitelist_match` | enum {refuerza, neutro, debilita} | `check_whitelist` | ✅ Se calcula |
| `viability_con_cifra` | bool | Regla Python sobre ficha | ✅ Se calcula |
| `statement_type` | enum {quote, reported} | Ficha extraída por Haiku | ✅ Ya viene de capa 1 |

**En el MVP `tier.value` siempre es `null`**. Las 11 señales se pueblan desde el día uno para que `compute_tier()` real (PI10) solo tenga que leer el bloque `signals` cuando se conecte. No se migran logs antiguos.

### 3.3 · Bloque `corrections`

Vacío al crear el archivo. Cada aviso externo añade una entrada:

```json
{
  "received_at": "YYYY-MM-DDTHH:MM:SSZ",
  "origin": "email" | "form" | "issue_github" | "otro",
  "reporter_public": "Asociación X (nombre público) | anónimo",
  "body": "descripción breve de la alegación",
  "resolution": null,
  "resolved_at": null,
  "resolution_body": null
}
```

Al resolver:

- `resolution`: `corregido` | `sin_cambio_justificado` | `pendiente_informacion`.
- `resolved_at`: fecha ISO.
- `resolution_body`: nota breve de la decisión, que se publica en `/correcciones/` con enlace a la propuesta afectada.

**Regla dura.** El resto del JSON no se edita nunca. La decisión editorial se guarda como nueva entrada en `corrections`; la ficha original, el log de capas y el bloque tier quedan congelados. Esto sostiene la transparencia del archivo histórico frente a ataques o presiones posteriores.

---

## 4 · Las 3 heurísticas del mínimo viable

### 4.1 · Cruce de fuentes (`check_cross_source`)

**Input.**

- Propuesta con `{actor, palanca, target_actor, url_source}`.
- Diccionario de noticias de la misma semana (`classified.json` o equivalente).

**Algoritmo.**

1. Filtrar las noticias de la semana clasificadas como `is_housing=True`.
2. De ellas, quedarse con las que tengan mismo `actor` principal + misma `palanca` (match literal; si en el MVP el match literal falla en casos obvios, anotarlo y afinar en semana 4).
3. Opcional: si hay `target_actor` declarado, exigir que coincida también.
4. Agrupar las URLs supervivientes por dominio raíz (quitar `www.`, quedarse con `a.b.tld` en dominios de segundo nivel).
5. Contar dominios distintos — incluye siempre el dominio de `url_source`.

**Output.**

```json
{
  "n_fuentes_independientes": 2,
  "urls": ["diariodeibiza.es/noticia-1", "periodicodeibiza.es/noticia-2"],
  "dominios": ["diariodeibiza.es", "periodicodeibiza.es"]
}
```

**Umbrales que aplicará `compute_tier()` (PI10, no el MVP):**

- `n_fuentes_independientes == 1` → techo 🟡 (single-source penalty, regla dura).
- `n_fuentes_independientes ≥ 2` → habilita camino a 🟢.

### 4.2 · Coincidencia textual verbatim (`check_verbatim_match`)

**Input.**

- Propuesta con `{url_source, statement_verbatim, statement_type}`.

**Algoritmo.**

1. Comprobar caché HTTP local. Si existe y < 30 días, usar; si no, descargar `url_source`.
2. Si la descarga devuelve 4xx o 5xx persistente (tras 2 reintentos), abortar con `ratio=null` y marcar `url_ok=false`.
3. Parsear HTML con `lxml`. Eliminar `<script>`, `<style>`, `<nav>`, `<footer>`, `<header>` y bloques de navegación.
4. Extraer el cuerpo del artículo (heurística: el nodo con más texto entre los hijos directos de `<main>` o `<article>`, fallback `<body>`).
5. Aplicar `difflib.SequenceMatcher(None, body_text.lower(), statement_verbatim.lower()).ratio()`.

**Output.**

```json
{
  "ratio": 0.87,
  "statement_type": "reported",
  "threshold_blocking": 0.60,
  "threshold_green": 0.80,
  "passed_blocking": true,
  "passed_green": true,
  "html_cache_hit": true
}
```

**Umbrales.**

- `statement_type == "quote"` → ratio ≥ 0.95 obligatorio. Si < 0.95, bloqueante (🔴 en `compute_tier()` real).
- `statement_type == "reported"` → ratio ≥ 0.60 mínimo bloqueante. Entre 0.60 y 0.80: techo 🟡. ≥ 0.80: habilita camino a 🟢.

### 4.3 · Encaje dominio-actor (`check_whitelist`)

**Input.**

- Propuesta con `{actor, url_source}`.
- `data/actor_domains.yml` cargado en memoria.

**Algoritmo.**

1. Extraer dominio raíz de `url_source` (mismo criterio que cross-source).
2. Buscar `actor` en `actor_domains.actors`.
3. Clasificar:
   - Dominio en `actors[actor].oficial` → `refuerza`.
   - Dominio en `actors[actor].cobertura_aceptada` → `neutro`.
   - Dominio en `medios_cobertura_aceptada` (lista global) → `neutro`.
   - Actor existe pero dominio no coincide con nada → `debilita` + `whitelist_miss: false`.
   - Actor NO existe en el YAML → `debilita` + `whitelist_miss: true` (actor nuevo, parte del lunes).

**Output.**

```json
{
  "match": "refuerza",
  "domain": "conselldeivissa.cat",
  "known_actor": true,
  "whitelist_miss": false
}
```

**Regla operativa.** Si `whitelist_miss: true` (actor nuevo no listado), no se descarta la propuesta: el sistema registra la señal y entra al parte del lunes. El repaso mensual IA (iteración) propone ampliaciones que el editor firma con OK antes de tocar el YAML (D3).

---

## 5 · Whitelist V1 cerrada

Los 20 actores principales del dominio público de la vivienda en Ibiza, con sus dominios oficiales conocidos. Base: taxonomía cerrada de 8 categorías (memoria `taxonomia_actores.md`, 2026-04-20) + actores frecuentes en las noticias W06-W17.

```yaml
# data/actor_domains.yml
# V1 — 2026-04-24. Refinamiento con datos reales del backfill (próxima revisión D3: post-backfill).

meta:
  version: 1
  last_updated: 2026-04-24
  criterio: 20 actores principales del dominio público vivienda Ibiza
  nota: refinamiento de subdominios (.cat, caib.es vs goib.es) con datos empíricos del backfill

# Medios de cobertura general aceptada (cualquier actor sobre cualquier tema vivienda).
# Un dominio aquí NO confirma autoría del actor, solo traza legítima de la cobertura.
medios_cobertura_aceptada:
  - diariodeibiza.es
  - periodicodeibiza.es
  - ultimahora.es
  - ibizaactualidad.com
  - noudiari.es
  - ib3tv.com
  - ib3.org
  - europapress.es
  - efe.com
  - rtve.es
  - elpais.com
  - elmundo.es

actors:
  # Categoría 1 — Instituciones públicas (8 actores)
  Consell d'Eivissa:
    oficial: [conselldeivissa.es, conselldeivissa.cat]
  Govern Balear:
    oficial: [caib.es, goib.es, caib.cat]
  IBAVI:
    oficial: [ibavi.es, ibavi.caib.es]
  Ajuntament d'Eivissa:
    oficial: [eivissa.es, eivissa.cat]
  Ajuntament de Santa Eulària:
    oficial: [santaeulalia.net, santaeularia.eu]
  Ajuntament de Sant Antoni:
    oficial: [santantoni.net]
  Ajuntament de Sant Josep:
    oficial: [santjosep.org]
  Ajuntament de Sant Joan:
    oficial: [santjoandelabritja.com]

  # Categoría 2 — Partidos políticos (4 actores)
  # UI: gris neutro, regla dura de imparcialidad visual (ver ESTUDIO-DISENO §5.1)
  PP Balears:
    oficial: [ppbalears.es]
  PSOE Balears:
    oficial: [psib-psoe.com, psoe-ibiza.es]
  Vox Balears:
    oficial: [voxbalears.es, voxespana.es]
  Més per Mallorca:
    oficial: [mesperillesbalears.cat]

  # Categoría 3 — Sindicatos (2 actores)
  CCOO Illes Balears:
    oficial: [ccoo-illesbalears.cat, ccoo.es]
  UGT Illes Balears:
    oficial: [ugt-ib.org, ugt.es]

  # Categoría 4 — Patronales (2 actores)
  CAEB:
    oficial: [caeb.es]
  PIMEEF:
    oficial: [pimeef.com]

  # Categoría 5 — Tercer sector (2 actores)
  Cáritas Ibiza:
    oficial: [caritas-ibiza.org, caritas.es]
  Creu Roja Illes Balears:
    oficial: [creurojaib.org, cruzroja.es]

  # Categoría 6 — Colectivos ciudadanos (2 actores)
  Sindicat de Llogaters Eivissa:
    oficial: [sindicatdellogaters.org]
  PAH Eivissa:
    oficial: [afectadosporlahipoteca.com]
```

**Total: 20 actores, 8 categorías cubiertas de las 8 de la taxonomía.** Las categorías 7 y 8 (colectivos ad-hoc, asambleas, expertos individuales) no tienen actores fijos y se tratarán caso a caso con la regla `whitelist_miss: true`.

**Dominios que quedan por confirmar durante el backfill:** `ibavi.caib.es` (algunos informes usan `ibavi.es` directo), `goib.es` vs `caib.es` (duplicación oficial conocida), `.cat` vs `.es` para algunos consells. El refinamiento va a la revisión de [D3](DECISIONES.md) tras el backfill.

---

## 6 · Integración con el pipeline actual

### 6.1 · Estado actual del pipeline

El orquestador `src/report.py` ejecuta hoy:

```
ingest → classify → extract → generate → verify → archive → self_review → build_index → costs
```

Ver detalle en [ARQUITECTURA.md](ARQUITECTURA.md).

### 6.2 · Estado tras el MVP

```
ingest → classify → extract → audit → generate → verify → archive → self_review → build_index → costs
                                 ↑
                            NUEVO PASO
```

El resultado de `audit` es la entrada de `generate`. La ficha de cada propuesta que `generate` recibe es **la de Haiku** (capa 1) enriquecida con metadatos del log — no la extracción ciega de Sonnet (capa 2). La capa 2 es auditoría, no sustitución. Caso excepcional: si `compare.severity == 'critical'` y el fallback Opus (capa 4 implícita en `src/extract.py`) devuelve una ficha distinta a ambas, esa ficha reemplaza. Eso ya pasa hoy; no cambia en el MVP.

### 6.3 · Cambios en `src/report.py`

- Tras la llamada a `extract(...)`, insertar:

```python
from src import audit, audit_heuristics
import yaml

actor_domains = yaml.safe_load(open("data/actor_domains.yml"))
audit_result = audit.audit_proposals(proposals, news, actor_domains)
# audit_result contiene proposals enriquecidas + log escrito.
```

- Pasar `audit_result.proposals` (no `proposals` crudo) a `generate()`.
- `audit.write_audit_log()` se llama dentro de `audit_proposals()`, antes de devolver.

### 6.4 · Ajuste en `src/self_review.py`

Añadir un check específico del auditor. El prompt de autoevaluación semanal (Sonnet) recibe como input extra:

```json
{
  "auditor": {
    "propuestas_auditadas": 3,
    "propuestas_disputadas": 1,
    "ratio_disputas": 0.33,
    "rango_saludable": [0.08, 0.25],
    "en_rango": false,
    "propuestas_flagged": 0
  }
}
```

Sonnet evalúa si el ratio está fuera del rango saludable definido en [ESTUDIO-COSTES-AUDITOR.md §12.1](ESTUDIO-COSTES-AUDITOR.md). Si está fuera, lo anota en la autoevaluación (nota <7 en dimensión *rigor*). El parte del lunes (iteración) lee esta señal como trigger.

### 6.5 · Qué NO tocamos

- **`src/extract.py::retry_with_opus`** se queda como está. En el MVP sigue siendo fallback implícito cuando la validación corta Sonnet marca `valid: false`. D1 formaliza como capa 4 explícita en la iteración posterior.
- **`src/verify.py`** sigue siendo la fuente de `verify: {...}` en el log. El auditor no duplica: llama a `verify.check_proposal(...)` y guarda el resultado.
- **`src/balance.py`** no cambia. El balance trimestral corre aparte, sobre el histórico acumulado.
- **`src/rescue.py`** no cambia. El rescate de propuestas antiguas se audita igual que las nuevas (mismo flujo).

---

## 7 · Página `/correcciones/` como plantilla mínima

Archivo nuevo: `docs/correcciones.md`. Jekyll page, layout `page`, enlazada desde el footer. No se mete al prototipo HTML del Bloque B (pausado desde 2026-04-21); la integración visual se hace cuando el editor reabra ese bloque.

### 7.1 · Contenido mínimo (lenguaje llano)

```markdown
---
layout: page
title: Correcciones
permalink: /correcciones/
---

# ¿Has visto un error?

Este observatorio documenta lo que actores con nombre proponen en público. Si crees que hemos dicho algo incorrecto, o si falta una propuesta que debería estar, queremos saberlo.

## Cómo avisar

Dos canales. Elige el que te venga bien.

- **Por correo:** [correcciones@radaribiza.com](mailto:correcciones@radaribiza.com) *(próximamente — el buzón se abrirá cuando cierre el nombre definitivo del observatorio).*
- **Por formulario:** aquí irá un formulario simple *(próximamente — lo conectamos en las próximas semanas).*

Mientras esos dos canales no están operativos, puedes escribir respondiendo a cualquier edición publicada o abrir un aviso en el [repositorio público del proyecto](https://github.com/otundra/ibiza-housing-radar/issues).

## Qué hacemos con tu aviso

1. **Lo anotamos en el registro público de la propuesta afectada.** Nada se edita en silencio — cada aviso queda fechado, con su origen y su resolución.
2. **Respondemos en 72 horas.** Si es un error claro (URL caída, cita mal transcrita), corregimos en ese plazo. Si el asunto es más dudoso, te respondemos con lo que hemos visto y decidimos juntos.
3. **Publicamos la corrección con traza visible.** La edición original queda marcada como *corregida*, con enlace a esta nota.

## Qué NO hacemos

- Editar el pasado en silencio. Las ediciones semanales son inmutables; las correcciones se añaden, no sobreescriben.
- Retirar una propuesta porque moleste al actor que la formuló. Solo se corrigen errores de hecho, no de opinión.
- Responder a polémicas políticas. Este observatorio documenta, no opina.

## Registro público de correcciones

*(De momento, vacío — no ha entrado ninguna corrección. Cuando entren, aparecerán aquí con fecha, propuesta afectada y resolución.)*

---

*Protocolo vigente desde el lanzamiento del observatorio documental (2026-04-21). Reglas editoriales completas en [/politica-editorial/](/politica-editorial/).*
```

### 7.2 · Cambios en el footer del sitio

En `docs/_includes/footer.html` (o equivalente), añadir:

```html
<a href="/correcciones/">Correcciones</a>
```

Junto a los enlaces existentes (`/acerca/`, `/politica-editorial/` cuando esté, `/ediciones/`).

### 7.3 · Apuntado para revisión legal futura

**Compromiso operativo de las 72 h.** El protocolo se publica antes de que el formulario y el buzón estén operativos. Durante ese margen, la ruta alternativa es el issue en GitHub (visible públicamente). El editor indicó el 2026-04-24 que la exposición es baja porque la web no será visible públicamente hasta mucho después del arranque (sin fecha, [D15](DECISIONES.md)). Aun así:

- Se revisa formalmente al **cerrar el estudio legal del titular** ([D2](DECISIONES.md), Hito 3).
- Se revisa también **antes de abrir al público** (apuntado en STATUS.md).

---

## 8 · Fuera del mínimo viable (iteración posterior)

D1 dejó estas piezas fuera del MVP. Arrancan tras cerrar el Hito 1 (~15 h de trabajo del editor adicionales; sin calendario, [D15](DECISIONES.md)).

| Pieza | Qué es | Cuándo entra |
|---|---|---|
| Capa 4 Opus formalizada | Formalizar `retry_with_opus` como paso explícito del auditor (no fallback implícito de extract). Solo arbitra cuando `compare.severity == critical`. Actualiza bloque `arbitraje` en `signals`. | Iteración, semana 1 |
| Página `/revision-pendiente/` | Cuarentena navegable con propuestas tier 🔴 o flagged. | Iteración, semana 1 |
| Tablero público `/auditor/` | Métricas de las últimas 4 semanas: distribución de tiers, ratio de disputas, flagged/mes, coste. Regenerado tras cada edición. | Iteración, semana 2 |
| Repaso mensual IA (capa 5bis) | Opus lee cuarentena + logs de un mes y propone ajustes YAML; editor firma por Telegram. | Iteración, semana 2 |
| Formulario con webhook | Formulario en `/correcciones/` → webhook → issue GitHub → notificación Telegram. | Iteración, semana 3 |
| `compute_tier()` real | Lee bloque `signals` del log y devuelve color según árbol de decisión (ESTUDIO-TIERS.md §3). Conecta tras D9 + PI10. | Iteración, semana 3 |

**Tareas que quedan fuera incluso de la iteración posterior:**

- Medición empírica del sesgo por actor en tiers (RT25) — requiere 3 meses de ediciones auditadas. Post-relanzamiento.
- Tests unitarios del pipeline completo (RT5) — D4 los difiere al post-backfill como bloque único.
- Buzón email real — diferido hasta cierre del nombre del observatorio (D2).
- Mockup visual de `/correcciones/` dentro del prototipo HTML — cuando se reanude Bloque B.
- Parte Telegram consolidado del lunes del auditor — depende de la capa 5bis y del tablero `/auditor/`. Iteración posterior.

---

## 9 · Fases de construcción

Cuatro fases en cascada. Cada una se cierra cuando sus entregables están verificados; la siguiente arranca cuando el editor lo indica. **Sin calendario ni rango de días** ([D15](DECISIONES.md)); las estimaciones de horas son esfuerzo relativo del editor, no compromiso de reloj. Referencia completa: [ESTUDIO-COSTES-AUDITOR.md §10](ESTUDIO-COSTES-AUDITOR.md).

### Fase 1 — Capa 2 + comparador (~7-10 h de trabajo del editor) ✅ cerrada 2026-04-25

**Entregables.**

- [x] `src/audit.py` con `run_blind_audit()` operativa. Batch único Sonnet con `EXTRACT_SYSTEM`.
- [x] `src/audit_compare.py` con `compare_extractions()`. Comparación campo a campo, severidad.
- [x] Prueba manual: corrida sobre 4 propuestas (3 de W17 + 1 adicional) vía `scripts/test_audit_phase1.py`. Comparador clasifica los desajustes en `critical`/`minor`/`none` correctamente. Coste real 0,042 €.

**Sin integración aún** con `src/report.py`. Se prueba vía REPL o script adhoc.

**Apuntes registrados al cierre** (no bloquean Fase 1; mitigación prevista en fases siguientes):

1. *Desajustes cosméticos en nombres de actor* (Sonnet usa nombre largo, Haiku usa el corto) → mitigación en Fase 2 vía whitelist + alias.
2. *Número distinto de propuestas entre Haiku y Sonnet* → mitigación en Fase 3 vía señal `layers.compare.count_mismatch`.
3. *Sonnet desviándose ocasionalmente del actor declarado en el hint* → mitigación en iteración posterior al Hito 1 vía capa 4 Opus formalizada como árbitro.

### Fase 2 — Heurísticas + whitelist + hueco tier (~8-12 h de trabajo del editor) ✅ cerrada 2026-04-25

**Entregables.**

- [x] `src/audit_heuristics.py` con las 3 heurísticas (`check_cross_source`, `check_verbatim_match`, `check_whitelist`).
- [x] `data/actor_domains.yml` curado (§5).
- [x] Caché HTTP local en `.cache/http/` (TTL 30 días). Añadido a `.gitignore`.
- [x] Función `compute_tier(signals)` en `src/audit.py` que devuelve siempre `{value: null, reason: "pendiente_estudio", signals: {...}}`. Extra: `build_signals()` helper para construir el bloque a partir del comparador + heurísticas.
- [x] Prueba manual `scripts/test_audit_phase2.py` sobre las 3 propuestas de W17. 11 señales pobladas en cada una. Cross-source clasifica `[1, 2, 2]`. Whitelist clasifica `[debilita, debilita, neutro]`. Verbatim ratio = 1.0 cuando la propuesta apunta a su propia URL fuente.

**Apuntes para Fase 4 (calibración con W10):**

1. *Huecos en la whitelist V1*: `cadenaser.com` y `lavozdeibiza.com` no figuran en `medios_cobertura_aceptada`; coaliciones largas tipo `"Consell d'Eivissa, patronales, sindicatos"` no casan con la entrada simple `Consell d'Eivissa`. Refinamiento post-backfill ([D3](DECISIONES.md)).
2. *Ruido en `verbatim_match`*: cross-checks (verbatim de A contra body de B) devuelven ratios 0.65-0.93 por solapamiento de vocabulario común. Calibrar umbrales o cambiar a métrica más estricta (longest-match sobre `len(needle)`) en Fase 4.

### Fase 3 — Log + integración + página /correcciones/ (~8-12 h de trabajo del editor) ✅ construcción cerrada 2026-04-25

**Entregables.**

- [x] `src/audit.py::write_audit_log()` escribe JSON en `data/audit/YYYY-wWW/`.
- [x] Integración de `audit_proposals()` en `src/report.py` entre `extract` y `generate`.
- [x] `docs/correcciones.md` publicada, enlazada desde el footer.
- [x] Ajuste en `src/self_review.py` con señal `auditor_disputes_ratio`.
- [ ] Corrida end-to-end en una edición piloto (la que toque tras cerrar la fase) con el auditor activo en modo silencioso (log se escribe; la edición no visibiliza tier todavía). Se dispara automáticamente en la próxima ejecución del cron lunes.

### Fase 4 — Prueba empírica sobre W10 (~5-8 h de trabajo del editor)

**Entregables.**

- [ ] Backfill solo de la semana W10 (2-8 marzo 2026, dato histórico). Una semana sola, no las 12.
- [ ] Medir: coste real vs proyección, ratio de disputas, tiempo, tamaño del log, distribución de señales.
- [ ] Ajustar umbrales de heurísticas si los tiers quedan mal calibrados (revisar bloque `signals` de las propuestas).
- [ ] Decisión go / no-go para el backfill completo de 12 semanas.

**Cierre del Hito 1.** Se cumple cuando el criterio de éxito de §10 se da en la corrida sobre W10. [D1](DECISIONES.md) revisa el MVP con esos datos + los de la edición piloto de la Fase 3.

---

## 10 · Criterios de éxito del MVP

El MVP se considera cerrado si, tras la prueba empírica sobre W10, se cumplen los 6 criterios:

1. **Las propuestas de W17 (3) y las de W10 pasan por el auditor sin errores bloqueantes.** Log JSON escrito correctamente para cada una.
2. **El log contiene las 11 señales pobladas** (algunas con valores por defecto declarados, como `arbitraje: no_hubo`).
3. **El ratio de disputas sobre el total de propuestas** está entre 5 % y 30 % (rango saludable ampliado para muestras pequeñas; el estudio apunta 8-25 % como objetivo estable con más datos).
4. **El coste real por edición auditada** se mantiene por debajo de 0.50 € (margen amplio sobre la proyección 0.40 €).
5. **Ninguna heurística falla silenciosamente.** Si `verbatim_match_ratio` o `check_whitelist` devuelven `null` por error técnico (timeout, HTML roto), el log lo anota explícitamente en el campo correspondiente + en `timestamps.errors`.
6. **La edición pública sigue siendo legible.** El auditor en modo silencioso no rompe la renderización Jekyll ni cambia el formato de las propuestas.

**Si alguno falla** → se itera sobre esa pieza antes de cerrar. **Si ≥3 fallan** → el hito se reabre y se revisa el diseño.

---

## 11 · Enlaces y trazabilidad

- [ESTUDIO-COSTES-AUDITOR.md](ESTUDIO-COSTES-AUDITOR.md) — por qué y cuánto (cerrado 2026-04-22).
- [ESTUDIO-TIERS.md](ESTUDIO-TIERS.md) — árbol de decisión de tiers (cerrado 2026-04-23, D9).
- [DECISIONES.md](DECISIONES.md) — D1 (partición MVP), D2 (log público + correcciones), D3 (whitelist V1), D4 (tests diferidos), D5 (tiers en paralelo), D6 (marco de hitos), D9 (tiers cerrado).
- [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md) — PI9 (auditor MVP), RT9 (stub correcciones), RT15 (tiers estudio).
- [ARQUITECTURA.md](ARQUITECTURA.md) — pipeline actual.
- [CLAUDE.md](CLAUDE.md) — reglas fundacionales del proyecto.
- [`src/extract.py`](src/extract.py) — capas 1 y 4 preexistentes.
- [`src/verify.py`](src/verify.py) — 5 checks que alimentan capa 3.
- [`src/costs.py`](src/costs.py) — registro y topes.
- [`src/self_review.py`](src/self_review.py) — autoevaluación (se ajusta en la Fase 3).

---

*Documento vivo. Se archiva como histórico al cerrar el Hito 1. Sin fecha estimada ([D15](DECISIONES.md)).*
