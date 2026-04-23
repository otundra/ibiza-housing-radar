# Estudio del sistema de tiers de confianza

**Fecha:** 2026-04-23
**Estado:** 🟡 primer pase — secciones 1-3 redactadas (contexto + señales + árbol de decisión). Secciones 4-11 pendientes de segundo pase.
**Origen:** tarea de la revisión fundacional, ficha RT15 en [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md:238). Bloquea la función `compute_tier()` real dentro del auditor y la página pública con el badge de cada propuesta.
**Dependencia cerrada:** [`ESTUDIO-COSTES-AUDITOR.md`](ESTUDIO-COSTES-AUDITOR.md) define qué señales produce el auditor. Este estudio decide cómo combinarlas en un color.

---

## 1 · Punto de partida

### 1.1 Qué se aprobó rápido el 2026-04-21 (y no basta)

La noche del 21-abr se aprobó el "Plan A — tiers de confianza públicos" con estas reglas gruesas ([REVISION-FASE-0.5.md:45](REVISION-FASE-0.5.md:45)):

- 🟢 **Alta:** dos capas del auditor IA coinciden + verificación técnica OK + dos o más fuentes. Se publica sin aviso.
- 🟡 **Media:** dos capas IA coinciden + verificación OK + fuente única. Lleva la nota *"Fuente única. Si tienes información, ayúdanos"*.
- 🟠 **Baja:** Opus dudó o la verificación devolvió avisos menores. Nota prominente: *"Baja confianza. Verificación pendiente"*.
- 🔴 **No publicada:** va a cuarentena en [`/revision-pendiente/`](docs/revision-pendiente.md) hasta que aparezca segunda fuente o se archive.

Eso es un boceto, no un árbol. Falta:

- Qué combinación **exacta** de señales asigna cada color.
- Qué pasa cuando más de una señal tira en direcciones opuestas (p. ej. consenso IA completo pero verbatim flojo).
- Dónde viven las reglas en el código y cómo se cambian sin tocar `audit.py`.
- Qué hacer con propuestas ya publicadas si cambian los umbrales.
- Cómo se comunica cada color al lector no técnico sin parecer jerga.
- Si se muestran a todos los visitantes o solo al lector que quiere ese nivel de detalle.
- Cómo se cuenta la historia de una propuesta cuando su color cambia con el tiempo.
- Si el sistema perjudica sistemáticamente a actores con menos cobertura mediática (riesgo de sesgo estructural).

### 1.2 Qué está hoy en el código

El auditor mínimo viable (Hito 1 de la Fase 1, cierre previsto ~2 semanas) se construye con esta convención pactada ([DECISIONES.md D5](DECISIONES.md)):

```json
{
  "proposal_id": "...",
  "tier": {
    "value": null,
    "reason": "pendiente estudio",
    "signals": { ... }
  },
  "layers": { "haiku": {...}, "sonnet_blind": {...}, "compare": {...}, "heuristics": {...} },
  "verify": { ... }
}
```

Las señales se calculan y guardan desde el día uno. El campo `value` queda en `null` hasta que este estudio cierre y defina `compute_tier()`. Los logs antiguos no necesitan migración: cuando `compute_tier()` exista, lee del bloque `signals` acumulado.

Implicación: este estudio no bloquea el arranque del auditor. Solo bloquea la **publicación del badge** en las fichas públicas (PI10 en la revisión fundacional) y la página `/auditor/` con la distribución de tiers.

### 1.3 Restricciones de entorno

El árbol de decisión tiene que respetar cuatro reglas ya cerradas:

1. **Automatización máxima — el editor no audita contenido.** El color se calcula solo con señales del auditor. Nada de "el editor marca esta como 🟢 manualmente" ([PIVOTE.md](PIVOTE.md) §regla complementaria).
2. **Coherencia con la cuarentena.** 🔴 significa "no entra en edición semanal", va a `/revision-pendiente/`. 🟠 **sí** entra en edición con aviso visible. Esa frontera no es negociable: si una propuesta se publica en la edición, es porque algo la empuja al menos a 🟠.
3. **Coherencia con el protocolo de correcciones 72 h.** El color puede cambiar tras publicación si llega información nueva (segunda fuente que corrobora, error verificado que la destruye). El sistema tiene que permitir ese cambio sin reescribir la edición original ([DECISIONES.md D2](DECISIONES.md)).
4. **Regla dura de fuente única.** Nunca 🟢 con una sola URL. Ya está en la calibración del auditor ([ESTUDIO-COSTES-AUDITOR.md §4 · Capa 3](ESTUDIO-COSTES-AUDITOR.md:119)). Este estudio la mantiene y la refuerza.

### 1.4 Qué queda fuera del alcance

- No se decide aquí si los colores se muestran siempre o solo al lector en "modo profesional" (va en sección 10 de este estudio, segundo pase, y conecta con el test de usabilidad previsto en la ficha RT3 de la revisión).
- No se decide aquí la paleta visual exacta de los badges (va en el estudio de diseño y en los mockups de sección 9, segundo pase).
- No se entra en cómo presenta el auditor sus resultados al editor en el parte Telegram del lunes — eso lo cierra el propio auditor, no este estudio.

---

## 2 · Señales disponibles del auditor

El auditor deja 10 señales computables por cada propuesta. Todas están en `data/audit/YYYY-wWW/{proposal_id}.json` bajo `signals`. Son la materia prima del árbol.

### 2.1 Consenso entre las dos extracciones IA

**`ia_consenso` — enumerado {completo, parcial, disputa}.**

- **completo:** Haiku (capa 1 de extracción primaria) y Sonnet (capa 2 de auditoría ciega) coinciden en **todos** los campos críticos: `actor`, `target_actor`, `palanca`, `state`, `url_source`, `statement_verbatim`. Diferencias en campos menores (`viability_economic`, `horizon`) no rompen el consenso.
- **parcial:** diff solo en campos menores, nunca en críticos.
- **disputa:** diff en al menos un campo crítico → se dispara arbitraje Opus (capa 4).

Calculado por `src/audit_compare.py::compare_extractions()`.

### 2.2 Arbitraje Opus (capa 4)

**`arbitraje` — enumerado {no_hubo, opus_confirma_haiku, opus_confirma_sonnet, opus_discrepa_ambas}.**

- **no_hubo:** `ia_consenso` fue completo o parcial → no se gasta Opus.
- **opus_confirma_haiku / opus_confirma_sonnet:** hubo disputa, Opus re-extrajo ciego con el mismo prompt y coincidió con uno de los dos. Resolución clara.
- **opus_discrepa_ambas:** Opus no coincide ni con Haiku ni con Sonnet. Es la señal más fuerte de que algo no cuadra.

Ver [ESTUDIO-COSTES-AUDITOR.md §4 · Capa 4](ESTUDIO-COSTES-AUDITOR.md:128).

### 2.3 Verificación técnica — 5 checks de `verify.py`

Cinco valores, todos booleanos salvo el cuarto:

- **`url_ok`:** la URL fuente devuelve HTTP 200 en el momento de auditar. Si devuelve 4xx/5xx persistente tras dos reintentos, es False.
- **`traza_dominio_actor`:** el dominio de la URL encaja con un dominio conocido del actor declarado o con un medio de cobertura aceptado (lista en `data/actor_domains.yml`). Ver §2.6.
- **`fecha_coherente`:** la fecha del artículo cae dentro de la ventana de la edición (últimos 7-14 días al ejecutar) o es un rescate declarado.
- **`verbatim_match_ratio`:** float en [0, 1]. `difflib.SequenceMatcher` sobre el HTML limpio de la URL contra `statement_verbatim`. Umbrales distintos según `statement_type` (§2.7).
- **`wayback_snapshot`:** existe snapshot en Wayback Machine en las últimas 72 h. No es bloqueante si falla por fallo transitorio del servicio, pero resta confianza.

### 2.4 Cross-source

**`n_fuentes_independientes` — entero ≥ 1.**

Número de URLs de **dominios distintos** que cubren la misma propuesta (mismo actor + misma palanca + mismo target_actor). Calculado al agregar propuestas equivalentes tras la extracción.

- `=1` dispara la regla dura: techo 🟡, nunca 🟢.
- `≥2` habilita el camino a 🟢.

### 2.5 Whitelist dominio-actor

**`whitelist_match` — enumerado {refuerza, neutro, debilita}.**

- **refuerza:** el dominio de la URL coincide con el dominio oficial del actor (p. ej. `conselldeivissa.es` para Consell d'Eivissa). Señal fuerte de fuente primaria.
- **neutro:** el dominio pertenece a la whitelist de medios de cobertura aceptados (Diario de Ibiza, Periódico de Ibiza, IB3, Ara Balears...). La propuesta es cobertura de tercera parte, no primaria.
- **debilita:** el dominio no está ni en la lista de actores ni en la de medios aceptados. Puede ser cobertura legítima pero no confirmada. No bloqueante, pero baja el techo.

Whitelist versión 1 (15-20 actores más frecuentes) cerrada en [DECISIONES.md D3](DECISIONES.md).

### 2.6 Viability sanity

**`viability_con_cifra` — booleano.**

Si la propuesta declara `viability_economic` alta o media **y** no hay una cifra numérica en `statement_verbatim` ni en el cuerpo de la noticia, el auditor rebaja `viability_economic` a `"no_evaluada"` automáticamente y marca esta señal como False. No bloqueante para la publicación, pero entra como indicador débil.

### 2.7 Tipo de declaración

**`statement_type` — enumerado {quote, reported}.**

- **quote:** cita textual entre comillas atribuida al actor.
- **reported:** texto en estilo indirecto, atribuido al actor por el periodista.

Afecta a los umbrales de `verbatim_match_ratio`:
- quote: umbral mínimo 0.95 (texto casi idéntico).
- reported: umbral mínimo 0.60 **y** presencia literal del nombre del actor **y** al menos 2 términos clave de la palanca.

Los umbrales actuales son los aprobados el 2026-04-21 para la capa 3 del auditor.

### 2.8 Ausente a propósito

**No se usan estas señales**, aunque técnicamente estarían disponibles:

- **Reputación del medio.** No se pondera Diario de Ibiza como más fiable que un blog local. Todos los medios de la whitelist son "neutros". Si un medio concreto empieza a fallar de verdad, se saca de la whitelist, pero no se jerarquiza dentro.
- **Edad del actor en el corpus.** Tampoco se premia a actores que llevan más semanas apareciendo. El corpus no es una reputación acumulada.
- **Bloque político del actor.** Prohibido por la regla fundacional de imparcialidad. Un partido, un sindicato, una patronal, una asamblea vecinal producen señales de la misma forma.

---

## 3 · Árbol de decisión determinista

Evaluación en orden. El primer paso que aplique decide el tier. Cortocircuito estricto: si el paso 1 dispara, no se evalúan 2-6.

### 3.1 Paso 1 — Bloqueantes → 🔴 cuarentena

La propuesta **no entra en la edición semanal**. Va a [`/revision-pendiente/`](docs/revision-pendiente.md). Se escribe en el log con `tier.value = "rojo"` y `tier.reason` indicando la causa exacta.

Dispara 🔴 cualquiera de estas condiciones:

| Condición | Por qué bloquea |
|---|---|
| `url_ok = False` | No hay forma de verificar si el artículo sigue existiendo. Publicar una propuesta con fuente muerta destruye la trazabilidad. |
| `traza_dominio_actor = False` **y** `whitelist_match = debilita` | Ni el dominio es del actor ni es un medio aceptado. Riesgo alto de contenido de terceros no verificable. |
| `verbatim_match_ratio` por debajo del umbral mínimo (0.60 reported / 0.95 quote) | Lo que dice la propuesta no se encuentra en la URL citada. Es la señal más fuerte de error de extracción o de alucinación. |
| `fecha_coherente = False` y no hay rescate declarado | La noticia no encaja en la ventana temporal y no está marcada como recuperación intencional de una semana anterior. |
| `arbitraje = opus_discrepa_ambas` | Las tres capas IA no se ponen de acuerdo. El auditor no puede resolver. |

### 3.2 Paso 2 — Reglas duras de techo

Si la propuesta sobrevive al paso 1, se aplican los techos antes de evaluar caminos positivos. Un techo **baja** el tier máximo alcanzable; nunca lo sube.

| Condición | Techo aplicado | Motivo |
|---|---|---|
| `n_fuentes_independientes = 1` | Máximo 🟡 | Regla dura de fuente única. Una sola URL no justifica "alta confianza" por más que el resto vaya bien. |
| `arbitraje ∈ {opus_confirma_haiku, opus_confirma_sonnet}` | Máximo 🟡 | Hubo disputa real entre capas IA. Aunque Opus resolvió, el lector merece saber que no fue consenso de serie. |
| `whitelist_match = debilita` | Máximo 🟡 | Dominio no verificado como del actor ni como medio aceptado. Publicable, pero sin "alta confianza". |
| `viability_con_cifra = False` y la propuesta declaraba viability alta | Máximo 🟡 | El auditor tuvo que rebajar la viabilidad declarada. Nota pública de ese ajuste. |
| `wayback_snapshot = False` y el dominio no es un medio muy estable (BOIB, diarios establecidos) | Máximo 🟠 | Sin respaldo de archivo, la URL podría desaparecer. Señal débil pero real. |

Si se acumulan varios techos, aplica el más restrictivo.

### 3.3 Paso 3 — Camino a 🟢 (alta confianza)

Para alcanzar 🟢 tienen que darse **simultáneamente** todas estas condiciones, y no haber disparado ningún techo del paso 2:

- `ia_consenso = completo` (o `parcial` sin arbitraje necesario)
- `url_ok = True`
- `traza_dominio_actor = True`
- `fecha_coherente = True`
- `verbatim_match_ratio ≥ 0.95` si `quote`, o `≥ 0.80` si `reported` (más estricto que el mínimo de 0.60 del paso 1)
- `wayback_snapshot = True`
- `n_fuentes_independientes ≥ 2`
- `arbitraje = no_hubo`
- `whitelist_match ∈ {refuerza, neutro}`
- `viability_con_cifra = True` (si la propuesta declara viability alta o media)

Lectura: 🟢 es el tier más exigente. Requiere consenso IA limpio, verificación completa, al menos dos fuentes independientes, dominio aceptado y coherencia interna de la propuesta.

### 3.4 Paso 4 — Camino a 🟡 (media confianza)

Se llega a 🟡 si:

- Sobrevive al paso 1 (no bloqueante).
- Tiene al menos un techo del paso 2 que limita a 🟡.
- No tiene condiciones que degraden a 🟠 (paso 5).
- La verificación técnica básica está OK: `url_ok = True`, `traza_dominio_actor = True` **o** `whitelist_match ≠ debilita`, `verbatim_match_ratio` por encima del mínimo.

La diferencia operativa entre 🟡 y 🟢 es el nivel de redundancia: 🟡 puede ser fuente única o con disputa resuelta; 🟢 no.

### 3.5 Paso 5 — Camino a 🟠 (baja confianza)

Se llega a 🟠 si sobrevive al paso 1 pero:

- Hay techo del paso 2 que limita a 🟠 (sin Wayback en dominio inestable).
- **O** tiene avisos no bloqueantes en verify que no se reflejan en 🟡 (p. ej. `wayback_snapshot = False` y `whitelist_match = debilita` simultáneamente, sin bloquear).
- **O** `arbitraje = opus_confirma_*` **y** además `n_fuentes_independientes = 1` (disputa resuelta + fuente única, doble motivo de cautela).

🟠 **entra en edición** pero con nota prominente visible al lector: *"Baja confianza. Verificación pendiente"*. El copy exacto se cierra en sección 5 (segundo pase).

### 3.6 Paso 6 — Default → 🟠

Si una propuesta sobrevive a paso 1 y no encaja en ninguno de los caminos anteriores por combinación rara de señales, se asigna 🟠 por defecto con `tier.reason = "default_path"`. Esa asignación se revisa en la auditoría mensual de cuarentena (capa 5bis) como señal de que el árbol tiene un caso no cubierto y hay que añadir regla explícita.

### 3.7 Cómo se lee el árbol en una propuesta real

Ejemplo sintético basado en una propuesta tipo observada en la semana del 20-26 abril:

```
Propuesta: "El Consell d'Eivissa propone limitar a 30.000 las licencias turísticas"
URL: diariodeibiza.es/ibiza/2026/...
statement_type: reported

Señales calculadas:
  ia_consenso: completo (Haiku y Sonnet coinciden en actor, palanca, state, verbatim)
  arbitraje: no_hubo
  url_ok: True
  traza_dominio_actor: False (dominio del diario, no del Consell)
  whitelist_match: neutro (Diario de Ibiza está en la lista de medios aceptados)
  verbatim_match_ratio: 0.82 (reported, por encima del 0.80 exigido para 🟢)
  fecha_coherente: True
  wayback_snapshot: True
  n_fuentes_independientes: 2 (sale también en Periódico de Ibiza)
  viability_con_cifra: True (30.000 es la cifra)

Evaluación:
  Paso 1 (bloqueantes): ninguno dispara.
  Paso 2 (techos): ninguno aplica (whitelist_match=neutro permite 🟢; arbitraje=no_hubo; n_fuentes=2).
  Paso 3 (camino a 🟢): cumple todo.

Tier final: 🟢
tier.reason: "consenso IA completo + verify OK + 2 fuentes + whitelist aceptada"
```

Segundo ejemplo — la misma propuesta pero solo en Diario de Ibiza:

```
n_fuentes_independientes: 1

Paso 2 (techos): n_fuentes=1 → techo 🟡.
Paso 3 (camino a 🟢): no puede, techo activo.
Paso 4 (camino a 🟡): cumple.

Tier final: 🟡
tier.reason: "fuente única; resto de señales en consenso"
```

### 3.8 Propiedades que tiene este árbol (y que falta validar)

**Propiedades deseables** que ya cumple por diseño:

- **Determinista.** Mismas señales → mismo tier. Sin aleatoriedad ni heurística opaca.
- **Auditable.** Cada asignación guarda `tier.reason` legible. El log público permite reproducir la decisión.
- **Conservador.** Ante duda, baja tier antes que subirlo. Un 🟡 que debería ser 🟢 cuesta menos que un 🟢 que debería ser 🟡.
- **Explicable al lector.** Cada color tiene justificación en señales concretas, no en un score compuesto.

**Propiedades pendientes de validar empíricamente** (material para sección 8, segundo pase):

- **No perjudica sistemáticamente a actores con menos cobertura.** Hipótesis: un colectivo vecinal que solo aparece en un blog local queda siempre en 🟡 por `n_fuentes_independientes=1` aunque el contenido sea impecable. El árbol "funciona bien" técnicamente, pero el resultado agregado podría ser un sesgo estructural contra actores débiles. Hay que medirlo sobre el backfill de 12 semanas y decidir si se mitiga (p. ej. relajar el techo de fuente única si `whitelist_match = refuerza`, o aceptar el sesgo como coste justo de la regla dura).
- **Distribución esperada ~70/20/8/2.** Meta operativa del auditor ([ESTUDIO-COSTES-AUDITOR.md §12](ESTUDIO-COSTES-AUDITOR.md:404)). Si el árbol real asigna 20/60/15/5, las heurísticas son demasiado estrictas o los umbrales verbatim están mal calibrados.

Estas dos validaciones se hacen ejecutando `compute_tier()` sobre el backfill piloto de la semana del 2-8 marzo (W10 como slug interno) en la semana 4 del plan del auditor, antes de ejecutar las 11 semanas restantes.

---

## Secciones pendientes (segundo pase)

- **§4 · Umbrales ajustables.** Dónde viven (archivo `src/tiers.py` o `data/tiers.yml`), cómo se cambian sin refactor, política de cambios retroactivos sobre corpus publicado (¿se recalculan tiers antiguos o se congelan?).
- **§5 · Copy público llano por tier.** Texto exacto que ve el lector junto al badge. Testeable. Versión ES, luego CA/EN en la fase trilingüe.
- **§6 · Interacción con cuarentena y promoción.** Cómo se mueve una propuesta de 🔴 a 🟡 cuando aparece segunda fuente, cómo se comunica esa historia, qué pasa con el enlace permanente.
- **§7 · Historia del tier.** Un tier puede cambiar con el tiempo; se muestra la evolución en la ficha, se registra en el log append-only, se genera un micro-timeline.
- **§8 · Sesgo por tipo de actor.** Medición sobre backfill, decisión sobre mitigación (relajación del techo de fuente única en casos concretos, o aceptación explícita del sesgo con nota metodológica).
- **§9 · Mockups.** Ficha de propuesta, lista de edición, dashboard `/auditor/`, cuarentena `/revision-pendiente/`.
- **§10 · Plan de test con usuarios.** Enganche con el test de usabilidad previsto (ficha RT3 de la revisión fundacional). Dos públicos: periodista local vs temporero/ciudadano. Métrica: comprensión del código de colores a los 5 segundos.
- **§11 · Decisiones que necesito del editor.** Lista cerrada de preguntas que solo puede responder Raúl (si los colores se muestran a todos los visitantes o solo en modo profesional, si el techo de fuente única se relaja con whitelist refuerza, si el default del paso 6 es 🟠 o 🔴).

---

## Apéndice · Qué cambia en el código cuando cierre este estudio

Tres archivos tocados:

1. **`src/tiers.py` (nuevo).** Contiene `compute_tier(signals: dict) -> dict` que ejecuta el árbol y devuelve `{value, reason, path}`. 100 líneas aprox. Tests unitarios con fixtures del backfill.
2. **`src/audit.py` (modificado).** La línea que hoy escribe `tier: {value: null, reason: "pendiente estudio", signals: {...}}` pasa a llamar a `compute_tier(signals)` y guardar su salida.
3. **`data/tiers.yml` (nuevo, opcional).** Si sección 4 decide externalizar umbrales. Contiene los valores numéricos (0.60, 0.80, 0.95, 1) y las reglas de techo en formato declarativo. Permite ajustar sin tocar `src/tiers.py`.

Coste del cambio: cero € API (es código Python puro). 4-6 h de desarrollo + 2-3 h de tests sobre backfill piloto. Absorbido por la semana 2 iteración del plan del auditor (Hito 2 del marco de tres hitos).
