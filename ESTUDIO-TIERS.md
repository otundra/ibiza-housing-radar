# Estudio del sistema de tiers de confianza

**Fecha:** 2026-04-23 (primer pase) · 2026-04-23 tarde (segundo pase) · 2026-04-23 noche (5 decisiones cerradas, ver [D9](DECISIONES.md))
**Estado:** ✅ **cerrado** salvo §8.5 (medición empírica del sesgo por tipo de actor), que depende de tener el backfill de 12 semanas ejecutado. Ficha de seguimiento de esa medición en RT25 de la revisión fundacional.
**Origen:** tarea de la revisión fundacional, ficha RT15 en [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md:238). Desbloquea la función `compute_tier()` real dentro del auditor y la página pública con el badge de cada propuesta (PI10).
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

## 4 · Umbrales ajustables

### 4.1 Dónde viven las reglas — tres opciones

**Opción 1 · Constantes en `src/tiers.py`.** Umbrales como variables de módulo al principio del archivo. Cambio = editar código + commit + push. Pros: versionado en git, sin parser externo. Contras: cambio obliga a despliegue; un editor no técnico no los toca directamente.

**Opción 2 · YAML externo `data/tiers.yml`.** Umbrales declarativos en YAML. `src/tiers.py` los lee al arrancar. Cambio = editar YAML + commit. Pros: legible, separación datos/código, encaja con la capa 5bis del auditor (Opus propone bloque YAML mensual, editor firma). Contras: dos lugares coherentes; un typo en YAML rompe el cálculo.

**Opción 3 · Híbrido.** Constantes por defecto en código + override opcional en YAML. Arranque sin YAML; override donde aporta. Pros: flexibilidad. Contras: complejidad conceptual.

**Recomendación: opción 2 (YAML).** Encaja con la capa 5bis ya definida en [`ESTUDIO-COSTES-AUDITOR.md §4 · Capa 5bis`](ESTUDIO-COSTES-AUDITOR.md). Los umbrales son datos editoriales, no lógica. El coste del typo se mitiga con un validador al cargar (aborta el pipeline con error claro; mejor que calcular mal en silencio). `src/tiers.py` queda mínimo: solo el árbol.

### 4.2 Qué va al YAML

```yaml
# data/tiers.yml — umbrales ajustables del sistema de tiers
umbrales_verify:
  verbatim_quote_min: 0.95        # cita textual: ratio mínimo
  verbatim_reported_min: 0.60     # estilo indirecto: mínimo bloqueante
  verbatim_reported_verde: 0.80   # estilo indirecto: mínimo para 🟢

techos:
  fuente_unica: amarillo
  arbitraje_opus_resolvio: amarillo
  whitelist_debilita: amarillo
  viability_sin_cifra_declarada_alta: amarillo
  sin_wayback_en_dominio_inestable: naranja

dominios_estables:
  - "boib.caib.es"
  - "caib.es"
  - "conselldeivissa.es"
  - "diariodeibiza.es"
  - "periodicodeibiza.es"
  - "ibestat.cat"

politica_cambio_retroactivo: congelar   # congelar | recalcular | hibrido
default_paso_6: naranja
```

Lo que **no** va al YAML: las reglas de taxonomía (qué campo es crítico vs menor, qué señales computan el consenso). Forman parte del árbol, no son ajuste operativo. Viven en `src/tiers.py`.

### 4.3 Política de cambios retroactivos

Si mañana se baja `verbatim_reported_verde` de 0.80 a 0.75, ¿qué pasa con las propuestas ya publicadas?

- **Congelar.** Tier calculado una sola vez al publicar, inmutable en log. Cambios futuros afectan solo a nuevas. Pros: estabilidad, ediciones no mutan a espaldas del lector. Contras: umbrales antiguos se acumulan como legado.
- **Recalcular.** Cada cambio re-ejecuta `compute_tier()` sobre todo el corpus con las señales guardadas. Ficha muestra siempre el tier con la política vigente. Pros: coherencia. Contras: historia del tier se borra por ajustes que no son información real.
- **Híbrido.** Log guarda `tier_al_publicar` inmutable y `tier_vigente` recalculable. Ficha muestra vigente con nota si difiere. Pros: lo mejor de ambos. Contras: dos tiers visibles confunden.

**Recomendación: congelar.** Motivos:

- Coherente con el principio editorial del proyecto: las ediciones no se reescriben, se corrigen con nota fechada.
- Un tier es un juicio en un momento dado con los criterios vigentes entonces. Cambiarlo silenciosamente hacia atrás es ucronía.
- Si un cambio de umbral descubre un error sistemático en propuestas pasadas, la vía correcta es el **protocolo de correcciones 72 h** — una entrada por propuesta afectada en [`/correcciones/`](docs/correcciones.md). Eso es información pública. El recálculo masivo silencioso no lo es.

En YAML: `politica_cambio_retroactivo: congelar`.

---

## 5 · Copy público llano por tier

Nivel lector temporero o ciudadano sin contexto técnico. Sin *auditor*, *heurística*, *ratio*, *consenso IA*. Conceptos traducidos a acciones observables.

### 5.1 Texto corto junto al badge en la ficha

```
🟢 Alta confianza
   Dos medios lo recogen y la revisión automática no encontró pegas.

🟡 Confianza media
   Un solo medio lo recoge, o hubo alguna duda durante la revisión.
   Si conoces el caso, ayúdanos: [formulario de contacto].

🟠 Confianza baja
   La revisión automática dejó avisos. Publicamos porque tiene interés,
   pero fíjate bien en el enlace de origen antes de citarla.

🔴 No publicada — en revisión
   Detectada pero no pasa los controles mínimos.
   Esperamos segunda fuente o a que alguien nos confirme.
```

### 5.2 Texto largo en `/metodologia/#tiers`

```
Cada propuesta publicada lleva un color que resume la confianza que
tenemos en ella en el momento de publicar. Lo calculamos automática-
mente con reglas fijas; no las decide una persona caso a caso.

🟢 Alta confianza. Dos medios distintos recogen la misma propuesta,
la URL de origen está viva, la cita del actor aparece literal en el
artículo, y la revisión automática la ha procesado sin discusión
interna.

🟡 Confianza media. Cumple los controles mínimos pero falta algo de
redundancia: fuente única, o una cifra declarada sin respaldo, o una
discusión interna entre capas de la revisión que se resolvió con una
tercera pasada. Se publica, con aviso.

🟠 Confianza baja. Publicable pero con reservas. Hay avisos no
bloqueantes — por ejemplo no hay copia guardada en Wayback Machine,
o el medio no está en la lista de fuentes estables. El lector debe
ir al enlace original antes de citar.

🔴 No publicada. La propuesta existe en la prensa pero no supera los
controles: URL caída, cita que no se encuentra en el artículo, o la
revisión automática no se pone de acuerdo ni tras arbitraje. Va a
/revision-pendiente/ y se archiva a los 60 días si nada cambia.

Los controles son los mismos para todos los actores: partidos
políticos, sindicatos, patronales, asambleas vecinales, tercer
sector. No se pondera la reputación del actor ni del medio que lo
recoge más allá de una lista dura de fuentes aceptadas (ver
/metodologia/#fuentes).

Los umbrales concretos viven en data/tiers.yml, públicos y
auditables. Los cambios se anotan en /correcciones/ y no se aplican
hacia atrás.
```

### 5.3 Palabras prohibidas en copy público (traducciones)

| En el código | En cara pública |
|---|---|
| heurística | regla automática |
| ratio, umbral | cuánto coincide / nivel mínimo |
| consenso IA, capa 1/2 | revisión automática |
| árbol de decisión | reglas fijas |
| whitelist | lista de fuentes aceptadas |
| verbatim match | cita literal, cita textual |
| verify, cross-source | segunda fuente, verificación técnica |
| arbitraje Opus | tercera pasada de revisión |
| log, append-only | registro público |
| schema, endpoint | — (no aparece en cara pública) |

### 5.4 Prueba de comprensión antes de publicar

- Leer los tres textos cortos a alguien sin contexto técnico y preguntar *"¿qué significa este color?"* — tiene que contestar en 10 segundos con frase propia.
- El texto largo no debe obligar a ir a otra página para entender un término. Si menciona "Wayback Machine" o "fuentes estables", lo explica ahí mismo o con tooltip.

---

## 6 · Interacción con cuarentena y promoción

### 6.1 Qué pasa cuando algo es 🔴

La propuesta se escribe en el registro del auditor igual que las demás, con `tier.value = "rojo"` y `tier.reason` explicando la causa. **No entra en la edición semanal.** Aparece en [`/revision-pendiente/`](docs/revision-pendiente.md) con: actor, resumen corto, URL, motivo del rojo, fecha de detección y fecha prevista de archivo (detección + 60 días).

### 6.2 Cómo se promueve de 🔴 a 🟡 / 🟠

Tres caminos:

1. **Llega segunda fuente antes de los 60 días.** El pipeline detecta en la ingesta de una semana siguiente una propuesta equivalente (mismo actor + misma palanca + mismo target_actor) en URL de dominio distinto. El auditor recalcula: si el verbatim ahora coincide y los demás checks pasan, el tier sube a 🟡 o 🟠 según el árbol. La propuesta entra en la edición de la semana en que llegó la segunda fuente.
2. **Corrección manual vía formulario.** Un lector notifica que la URL funcionaba, que la cita correcta es otra, o que hay segunda fuente no detectada. El editor (no audita contenido pero sí valida si la corrección es procesable) decide: actualizar la lista de fuentes aceptadas si era problema de dominio no listado; añadir la segunda fuente al registro y relanzar; o rechazar la corrección con nota fechada.
3. **Propuesta evoluciona públicamente.** El actor convierte una declaración suelta en propuesta formal publicada en BOIB o pleno municipal. El pipeline la detecta como propuesta nueva, con `state = formal`. El registro antiguo queda como antecedente enlazado.

### 6.3 Cómo se cuenta al lector

En la edición semanal, cuando una propuesta sube de 🔴 a 🟡, lleva una mini-nota lateral:

> *Estuvo en /revision-pendiente/ entre 3 y 10 de mayo. Entra en edición esta semana tras aparecer segunda fuente en Periódico de Ibiza.*

En [`/revision-pendiente/`](docs/revision-pendiente.md), la propuesta promovida no se borra: queda marcada como "resuelta — ver edición del 10 de mayo" con enlace. Histórico íntegro.

### 6.4 Reglas de promoción

- El tier solo puede **subir** por aparición de nueva evidencia (segunda fuente, URL recuperada, corrección aceptada).
- El tier puede **bajar a cuarentena** solo por corrección verificada de un error de hecho (vía protocolo de 72 h, [D2](DECISIONES.md)). Una bajada técnica por recálculo de umbrales **no** la hace: `politica_cambio_retroactivo = congelar` en §4.
- Nunca se modifica el tier asignado en el log original. Los cambios son entradas nuevas en `tier.history[]`, append-only.

### 6.5 Archivo a 60 días

Si una propuesta 🔴 no recibe segunda fuente en 60 días, se mueve a `/propuestas/?status=no_verificada` con nota:

> *Detectada el 3 de mayo de 2026, mantenida en revisión 60 días. Sin segunda fuente ni corrección aceptada. Archivada como no verificada el 2 de julio de 2026.*

No se elimina. El archivo es público. Si años después alguien aporta segunda fuente, el auditor puede desarchivarla.

---

## 7 · Historia del tier

### 7.1 Cómo se registra

En el registro de auditoría, `tier` pasa de objeto único a estructura con `current` + `history[]` append-only:

```json
{
  "proposal_id": "...",
  "tier": {
    "current": "amarillo",
    "history": [
      {
        "value": "rojo",
        "at": "2026-05-03T07:00:00Z",
        "reason": "fuente única + whitelist debilita"
      },
      {
        "value": "amarillo",
        "at": "2026-05-10T07:00:00Z",
        "reason": "segunda fuente en periodicodeibiza.es, whitelist neutro"
      }
    ]
  }
}
```

`current` es derivado del último elemento de `history`. Se calcula al leer; no se serializa redundantemente (evita desincronización).

### 7.2 Cómo se muestra en la ficha pública

Si `history.length > 1`, línea debajo del badge:

```
🟡 Confianza media
   Historia: 🔴 (3 may) → 🟡 (10 may)  [ver detalle]
```

Click en "ver detalle" abre sección `#historia-tier` de la ficha con narrativa:

> *Detectada el 3 de mayo con fuente única (Diario de Ibiza). Marcada 🔴 en revisión. El 10 de mayo apareció también en Periódico de Ibiza, lo que permitió promoverla a 🟡. Sin cambios desde entonces.*

### 7.3 Cuándo NO mostrar historia

Si `history.length = 1`, no hay nada que contar: la propuesta nació en su tier y sigue ahí. Sin sección de historia, sin ruido visual.

### 7.4 Relación con `/correcciones/`

Son dos cosas distintas aunque ambas queden registradas:

- **Cambio de tier por evolución natural** (segunda fuente, promoción desde cuarentena) = información nueva. Entra en `tier.history[]`. **No** en `/correcciones/`.
- **Cambio de tier por error verificado** (una 🟢 que resulta ser apócrifa, cae a 🔴) = corrección. Entra en `/correcciones/` **y** añade entrada a `tier.history[]`. Las dos cosas.

La distinción importa: `/correcciones/` es el log de errores admitidos; `tier.history[]` es el log de evolución de la certidumbre. Mezclar los dos confunde al lector.

---

## 8 · Sesgo por tipo de actor (diseño, medición pendiente)

### 8.1 Hipótesis

El árbol tiene una regla dura: nunca 🟢 con fuente única. Por diseño, la redundancia es la base de la confianza. Pero la cobertura mediática no se reparte igual entre actores:

- **Actores con megáfono propio** (instituciones, partidos grandes, sindicatos mayoritarios, patronales) consiguen casi siempre ≥2 medios.
- **Actores con menos presencia mediática** (colectivos vecinales, asambleas, sindicatos minoritarios, tercer sector pequeño) quedan con frecuencia en fuente única aunque la propuesta sea impecable.

**Resultado esperado sin mitigación:** distribución desigual de 🟢 por tipo de actor. Los primeros acaparan verdes; los segundos viven en amarillos crónicos. El color "Alta confianza" deja de comunicar solo fiabilidad y pasa a comunicar también "actor con megáfono". Riesgo: el sistema proyecta estructura de poder mediático como si fuera fiabilidad factual.

### 8.2 Método de medición

Se hace **tras el backfill de 12 semanas**. Hoy no hay datos suficientes.

Con las ~36 propuestas del backfill, calcular:

```
distribucion_tiers[actor_type] = {
  "verde":    n_verde    / n_total,
  "amarillo": n_amarillo / n_total,
  "naranja":  n_naranja  / n_total,
  "rojo":     n_rojo     / n_total
}
```

8 categorías de actor del proyecto (taxonomía cerrada): institución, partido, sindicato, patronal, tercer sector, colectivo ciudadano, académico, otro.

**Test:** comparar proporción de 🟢 por categoría contra el promedio global. Si alguna categoría tiene una tasa de 🟢 más del 30 % por debajo del promedio global, y n ≥ 5 propuestas, sesgo confirmado.

**Umbrales de alerta:**

| Tasa de 🟢 en la categoría | Acción |
|---|---|
| ≥ 65 % del promedio global | OK, sin acción |
| 50 % — 65 % | Nota metodológica pública + revisión en 3 meses |
| < 50 % | Mitigación obligatoria |

### 8.3 Mitigaciones candidatas

**M1 — Relajar el techo de fuente única si el dominio está en la lista de fuentes aceptadas como "refuerza".** Permite 🟢 con una sola URL si es el dominio oficial del actor (p. ej. nota de prensa en `conselldeivissa.es`). Riesgo: un comunicado propio no es prensa independiente. Mitigación del riesgo: **restringir M1 a actores con `actor_type ∈ {colectivo ciudadano, tercer sector, sindicato minoritario, asamblea}`** — los que sufren el sesgo. No se aplica a instituciones ni partidos grandes (ellos consiguen redundancia solos y un comunicado propio sin rebote mediático es sospechoso).

**M2 — Aceptar el sesgo con nota metodológica pública.** El color sigue siendo lo que es. La página `/metodologia/` explica en lenguaje llano que el sistema premia la redundancia mediática y eso favorece a actores con más capacidad comunicativa. Honesto pero no resuelve.

**M3 — Tier adicional "🟢 con fuente única oficial".** Variante visual (🟢ᵃ o doble anillo). Semántica: "alta confianza, respaldo documental único". Riesgo: complica la comunicación, añade ruido visual, obliga a explicar 4 colores + variante. Coste pedagógico alto.

**M4 — Ampliar la recogida de fuentes.** Si el problema es que el pipeline no detecta segundas fuentes cuando existen (blogs locales, boletines asociativos, canales Telegram), ampliar `ingest.py`. No es mitigación del tier, es mejora de recogida. Más limpia conceptualmente, más cara.

### 8.4 Decisión diferida

Las 4 mitigaciones se evalúan **tras la medición**. Preliminar:

- **M1 solo para las 4 categorías señaladas** + **M2 como nota metodológica siempre** parece el mejor equilibrio.
- **M3 descartado** por coste pedagógico.
- **M4 como mejora de largo plazo**, no bloquea lanzamiento.

### 8.5 Qué falta para cerrar §8

- Backfill de 12 semanas ejecutado.
- Script `scripts/tier_bias_audit.py` que calcule la tabla de distribución por `actor_type` desde `data/audit/*.json`. ~2 h de desarrollo.
- Reunión de decisión con el editor con los datos del backfill en la mano.

Tarea registrada en el roadmap como **medición empírica del sesgo de tiers por tipo de actor** (ver §11 y la ficha RT25 de la revisión fundacional).

---

## 9 · Mockups textuales

Esquemas ASCII. Los HTML de verdad se hacen al reanudar el prototipo en la Fase 4 del roadmap (decisión Q5 en §11).

### 9.1 Badge en ficha de propuesta

```
┌──────────────────────────────────────────────────────┐
│  Consell d'Eivissa propone limitar a 30 000 las      │
│  licencias turísticas                                │
│                                                      │
│  🟢 Alta confianza                                   │
│  Dos medios lo recogen y la revisión automática no  │
│  encontró pegas.                                     │
│                                                      │
│  Actor: Consell d'Eivissa (institución)              │
│  Estado: propuesta formal en pleno                   │
│  Horizonte: 2027 (tras reforma normativa)            │
│  Fuentes: diariodeibiza.es · periodicodeibiza.es     │
│                                                      │
│  [Ver cita textual]  [Historia del tier]             │
└──────────────────────────────────────────────────────┘
```

### 9.2 Lista de edición semanal

```
Edición del 4-10 mayo 2026

───────────────────────────────────────────────────────
🟢  Consell d'Eivissa · Limitar licencias turísticas a 30 000
    Institución · formal
───────────────────────────────────────────────────────
🟡  CCOO · Convenio de hostelería + cláusula vivienda
    Sindicato · negociación · fuente única: Diario de Ibiza
───────────────────────────────────────────────────────
🟠  PIMEEF · Revisión IBI segunda residencia
    Patronal · declarativa · sin copia en Wayback
───────────────────────────────────────────────────────

Ver /revision-pendiente/ para las propuestas detectadas
pero no publicadas esta semana.
```

### 9.3 Página `/revision-pendiente/` (cuarentena)

```
REVISIÓN PENDIENTE                     /revision-pendiente/

Propuestas detectadas por el pipeline que no superan los
controles mínimos para entrar en edición semanal. Esperamos
segunda fuente, corrección aceptada, o archivo a 60 días.

─── Activas (5) ─────────────────────────────────────────

🔴 Asamblea PCI Ibiza · Cesión de suelo municipal
   Detectada 3 may 2026. Fuente: blog independiente (dominio
   no reconocido). Esperando segunda fuente hasta 2 jul 2026.
   [Si conoces otra fuente, avísanos]

🔴 Asociación Sa Llavor · Comedor social en Sant Antoni
   Detectada 6 may 2026. URL fuente devuelve 404 desde el día
   siguiente. Esperando URL recuperada o duplicado.

─── Resueltas este mes (3) ──────────────────────────────

✅ Sindicato temporeros · Exigencia alojamiento empleador
   En /revision-pendiente/ del 12 al 19 abr. Promovida a 🟡
   tras segunda fuente. Ver edición del 20 abr.

─── Archivadas a 60 días (1) ────────────────────────────

📁 Colectivo X · Propuesta Y
   Sin segunda fuente en 60 días. Archivada 30 jun 2026.
   Sigue consultable en /propuestas/?status=no_verificada.
```

### 9.4 Dashboard `/auditor/`

```
AUDITORÍA EN ABIERTO                            /auditor/

Últimas 4 semanas — del 13 abr al 10 may 2026

Distribución de tiers:
  🟢 Alta confianza ........ 12 propuestas (60 %)
  🟡 Media ................   5 (25 %)
  🟠 Baja .................   2 (10 %)
  🔴 Cuarentena ...........   1 (5 %)

Ratio de discusión interna del pipeline: 18 %
Propuestas con aviso: 2
Cuarentena abierta: 3 propuestas
Última tercera pasada Opus: 2 may 2026 (2 errores detectados)
Coste del auditor este mes: 0,21 €

Ver /auditor/distribucion-por-actor/ para el reparto por
tipo de actor (auditoría de sesgo).

Ver /correcciones/ para el log completo de enmiendas.
```

### 9.5 Badge pequeño para home / vista previa densa

```
🟢  Consell · Licencias turísticas 30 000
🟡  CCOO · Convenio hostelería + vivienda
🟠  PIMEEF · IBI segunda residencia
```

Sin texto del tier al lado en la vista más densa; el color + símbolo ya comunican. Hover o click lleva a la ficha completa con explicación.

---

## 10 · Plan de test con usuarios

### 10.1 Enganche con el roadmap

La revisión fundacional ya tiene ficha abierta para validar la UX de los tiers con dos públicos (ficha RT3). Este estudio define el **contenido operativo del test**. Tras ejecutarlo, RT3 cierra y sus resultados afectan a §5 (copy) y §11 (Q1 de visibilidad).

### 10.2 Participantes (n = 5)

- **2 periodistas locales** o gestores de comunicación de tercer sector (público profesional, lector recurrente esperado).
- **2 trabajadores de temporada** sin contexto técnico (primer visitante realista, usuario objetivo del proyecto).
- **1 ciudadano sin vínculo con el tema**, como control (cómo se entiende desde frío).

Contacto por red personal del editor. Incentivo: café o 15 €. Sin incentivo, pocos detalles críticos.

### 10.3 Material

- Maqueta con 3 ediciones reales del backfill que cubran los 4 tiers.
- **Versión A** (tiers visibles a todos con leyenda discreta) y **versión B** (tiers ocultos por defecto con toggle "ver nivel de confianza"). Impresas o en laptop.
- Hoja de preguntas neutras (sin inducir respuesta).

### 10.4 Tareas del test (15 min por persona)

1. *"Ojea esta edición durante 60 segundos. ¿Qué crees que cuenta?"*
2. *"Te voy a señalar esto [el badge 🟢]. ¿Qué significa?"* (sin explicar).
3. *"Ahora lee esta mini-explicación [texto corto de §5.1]. ¿Cambia tu respuesta?"*
4. *"Si estuvieras citando una de estas propuestas en un artículo o conversación, ¿cuál de los colores te haría parar a verificar antes?"*
5. *"¿Prefieres ver el color siempre o solo si lo activas?"*
6. *"¿Te distrae, ayuda o te es indiferente?"*

### 10.5 Métricas

- **Comprensión a los 5 segundos** (pregunta 2): el tier transmite algo legible sin leer explicación. Umbral: ≥ 3 de 5 contestan algo coherente.
- **Efecto en la confianza** (pregunta 4): el lector actúa distinto según el color. Umbral: ≥ 3 de 5 declaran parar en 🟠 o 🔴.
- **Preferencia de visibilidad** (pregunta 5): mayoría pide siempre visible o bajo toggle. Decide la versión A o B por defecto.

### 10.6 Salida

- Notas cortas del test.
- Decisión de UI: tiers visibles a todos / toggle / solo modo profesional / mixto (ver Q1 en §11).
- Ajustes al copy del §5 si alguna palabra confunde.

### 10.7 Lo que falta

- Ejecutar el test con personas reales. **Esto no lo puede hacer el asistente.** Es trabajo del editor con su red personal.
- Tiempo estimado: 1,5 h de investigación de campo + 30 min de análisis + 30 min de ajustes de copy. Total ~3 h.
- Momento: antes de cerrar §11 Q1 y antes de lanzar tiers en abierto.

---

## 11 · Decisiones que necesito del editor

Cinco preguntas. Contestarlas cierra el estudio y desbloquea la construcción de `src/tiers.py` real + el deployment del badge público.

### Q1 — ¿Tiers visibles a todos o solo en modo profesional?

Los temporeros y el ciudadano sin contexto pueden no entender el código de colores y percibirlo como ruido. Tres opciones:

- **Todos:** 4 colores siempre visibles con leyenda discreta. Máxima transparencia, potencial ruido.
- **Toggle:** botón *"ver nivel de confianza"* apagado por defecto. Solo profesionales lo activan. Menos ruido, pero esconde la transparencia radical del proyecto a la vista por defecto.
- **Mixto:** 🟢 sin badge (asumido), 🟡/🟠/🔴 con badge (aviso). La norma es *"confía por defecto, salvo aviso"*. Reduce ruido manteniendo avisos donde importan.

**Recomendación del asistente: mixto.** Coherente con la filosofía del proyecto (lo que pasa los controles se publica sin aspavientos; lo que no, se señaliza). Valida luego en el test UX (§10) si esta intuición se confirma.

### Q2 — ¿Techo de fuente única se relaja con whitelist "refuerza"?

Contexto en §8. Opciones:

- **No relajar nunca:** integridad de la regla, sesgo aceptado con nota metodológica pública.
- **Relajar solo para 4 categorías** (colectivo, tercer sector, sindicato minoritario, asamblea) cuando el dominio es oficial del actor: compensa el sesgo, riesgo acotado.
- **Relajar para todos:** simplifica la regla pero quita seguridad.

**Recomendación del asistente: decidir después del backfill.** Hasta entonces, regla dura en vigor. Tras la medición, si el sesgo supera el umbral del 30 %, aplicar relajación solo a las 4 categorías. Ver ficha RT25 en el roadmap.

### Q3 — ¿Default del paso 6 del árbol es 🟠 o 🔴?

El árbol tiene un caso por defecto para combinaciones raras. Hoy propuesto en 🟠 (entra con aviso):

- **🟠 default:** publica con aviso; obliga a revisar el árbol para tapar el caso.
- **🔴 default:** cuarentena; más conservador, puede acumular propuestas bien formadas que caen en casos raros.

**Recomendación del asistente: 🟠 default + alerta Telegram cada vez que se dispara.** Así se detectan casos raros rápido sin perder editorial.

### Q4 — ¿Política de cambios retroactivos es "congelar"?

Contexto en §4.3. Opciones: congelar / recalcular / híbrido.

**Recomendación del asistente: congelar.** Coherente con el principio de ediciones no reescribibles. Correcciones vía `/correcciones/`.

### Q5 — ¿Mockups visuales HTML ahora o en Fase 4?

- **Ahora:** romper la pausa activa del prototipo del Bloque B, extender con página de tiers. Coste: 2-3 h.
- **Fase 4:** dejar los mockups textuales del §9 como referencia conceptual; los HTML se integran cuando se retome Diseño.

**Recomendación del asistente: Fase 4.** La pausa del prototipo está por una razón (arquitectura primero, ver [`STATUS.md`](STATUS.md)). Los textuales bastan para validar el árbol y el copy.

### 11.6 Decisiones cerradas 2026-04-23 (OK del editor en bloque, registradas en [D9](DECISIONES.md))

| Pregunta | Decisión cerrada |
|---|---|
| Q1 — Visibilidad | **Mixto.** 🟢 sin badge (asumido). 🟡 / 🟠 / 🔴 con badge + copy de aviso. |
| Q2 — Techo de fuente única | **Decidir tras backfill.** Regla dura en vigor hasta entonces. Si la medición empírica (RT25) detecta sesgo > 30 % en alguna categoría con n ≥ 5, aplicar M1 solo a colectivos ciudadanos, tercer sector, sindicatos minoritarios y asambleas, y solo si el dominio es oficial del actor. |
| Q3 — Default del paso 6 del árbol | **🟠 + alerta Telegram** cada vez que se dispara el default. Permite detectar casos raros sin perder editorial. |
| Q4 — Política de cambios retroactivos | **Congelar.** Tier calculado una vez al publicar, inmutable en log. Cambios de umbrales afectan solo a nuevas. Correcciones vía `/correcciones/`. |
| Q5 — Mockups visuales HTML | **Fase 4.** Los textuales del §9 bastan. Los HTML se integran al reanudar el prototipo del Bloque B. |

Con estas cinco decisiones, el estudio queda cerrado operativamente. El único bloque pendiente de datos es §8.5 (medición empírica del sesgo) que se resuelve con el script `scripts/tier_bias_audit.py` ejecutado sobre el corpus del backfill (RT25). Todo lo demás es implementable hoy en `src/tiers.py` + `data/tiers.yml` bajo la tarea PI10.

---

## Resumen — qué falta para cerrar el estudio (actualizado 2026-04-23 noche)

| Pendiente | Qué se necesita | Dónde queda apuntado en el roadmap |
|---|---|---|
| ~~Cerrar Q1-Q5 (§11)~~ ✅ | ~~Respuesta del editor~~ | Cerrado 2026-04-23 en [D9](DECISIONES.md). RT26 ✅ |
| Medición empírica del sesgo por actor (§8.5) | Backfill 12 semanas ejecutado + `scripts/tier_bias_audit.py` (~2 h de código) | RT25 en la revisión fundacional |
| Test UX con 5 personas (§10) | Trabajo de campo del editor (~3 h) | RT3 (ficha existente), apunta a §10 de este estudio |
| Validación preliminar de distribución 70/20/8/2 | Backfill piloto de una semana (2-8 marzo 2026) del plan del auditor mínimo viable | RT1 (ficha existente), con línea sobre tiers |
| Mockups visuales HTML (§9) | Reanudar Bloque B (prototipo) en Fase 4 del roadmap V2 | Implícito en B34-B40 (Bloque B del roadmap original) |
| `src/tiers.py` y `data/tiers.yml` reales | ✅ Decisiones cerradas, se puede implementar | PI10 (sistema de tiers públicos) — Fase 2 del roadmap V2 |

---

## Apéndice · Qué cambia en el código cuando cierre este estudio

Tres archivos tocados:

1. **`src/tiers.py` (nuevo).** Contiene `compute_tier(signals: dict) -> dict` que ejecuta el árbol y devuelve `{value, reason, path}`. 100 líneas aprox. Tests unitarios con fixtures del backfill.
2. **`src/audit.py` (modificado).** La línea que hoy escribe `tier: {value: null, reason: "pendiente estudio", signals: {...}}` pasa a llamar a `compute_tier(signals)` y guardar su salida.
3. **`data/tiers.yml` (nuevo, opcional).** Si sección 4 decide externalizar umbrales. Contiene los valores numéricos (0.60, 0.80, 0.95, 1) y las reglas de techo en formato declarativo. Permite ajustar sin tocar `src/tiers.py`.

Coste del cambio: cero € API (es código Python puro). 4-6 h de desarrollo + 2-3 h de tests sobre backfill piloto. Absorbido por la semana 2 iteración del plan del auditor (Hito 2 del marco de tres hitos).
