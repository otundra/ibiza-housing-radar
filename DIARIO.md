# Diario del proyecto — Ibiza Housing Radar

Registro cronológico de hitos, decisiones y cambios relevantes.

Formato: agrupar por fecha, cada cambio una viñeta con el tema en **negrita** y una línea breve (qué/por qué/impacto combinados).

Reglas:
- Más recientes arriba.
- Solo cambios con valor de memoria futura. No entradas para commits triviales.
- No duplicar lo que ya dice Git: aquí va el contexto, no el diff.
- Si un cambio altera arquitectura o stack, también actualizar `CLAUDE.md` y `README.md`.

---

## 2026-04-20 — Revisión de coherencia + registro de ajustes

- **Revisión sistemática de incoherencias** tras petición del editor ("revisa todo el proyecto a ver si hay incoherencias"). 5 encontradas y corregidas:
  1. **Topes obsoletos de 8 €** en [`README.md`](README.md), [`STATUS.md`](STATUS.md), [`CLAUDE.md`](CLAUDE.md) del proyecto y [`docs/acerca.md`](docs/acerca.md) → actualizados a 12 € blando / 20 € duro + nuevas capas (verde <6 / amarilla 6-9 / naranja 9-12 / roja blanda 12-20 / dura >20).
  2. **Coste esperado "~2 €/mes"** → actualizado a "~6-7 €/mes" (pivote documental + 3 niveles de autoevaluación).
  3. **`src/rescue.py` docstring decía "Haiku confirma vigencia"** pero el código nunca llama a Haiku. Docstring corregida para coincidir con el código real (rescate 100% determinista basado en reglas). Nota de diseño sobre posible ampliación futura conservada.
  4. **`ARQUITECTURA.md` tabla del reparto de modelos** listaba `quarterly_audit.py` y `model_rebench.py` como si estuvieran implementados. Añadida columna "Estado implementación" con ✅/⏸ y clarificación: `self_review.py` y `generate_gold.py` ✅; `quarterly_audit.py` ⏸ (tarea A13); `model_rebench.py` ⏸ (tarea A14); fact-check de precedentes externos en `verify.py` ⏸ (no aplica en el modelo documental actual porque el pipeline solo reproduce precedentes del input, no genera).
  5. **`docs/acerca.md` describía el modelo antiguo** (3 secciones: señales/lectura/propuestas/a-vigilar con formato anterior al pivote). Añadido callout al inicio avisando que la reescritura completa es parte del Bloque B.
- **Nueva infraestructura de trazabilidad: [`private/adjustments-log.md`](private/adjustments-log.md)** — registro vivo de cambios voluntarios (prompts, umbrales, modelos, reglas). Complementa `postmortems.md`:
  - `postmortems.md` → errores con coste.
  - `adjustments-log.md` → cambios voluntarios con hipótesis y efecto medido.
  - Formato estándar por entrada: qué se cambió, motivo, datos que lo soportan, efecto esperado, efecto medido, reversible sí/no.
  - 5 entradas iniciales con los cambios de hoy (tope blando 12 €, mejoras prompt generate, mejora clasificación institucional en extract, verify tolerante, inicialización del log).
  - Sección **"Propuestas en evaluación sin aplicar"** para decisiones deferidas. Primera entrada: propuesta del editor de subir umbral de rigor de `<7` a `<8`, con criterio explícito de aplicación: *"si en 4 ediciones consecutivas el rigor observado es ≥8, se sube el umbral sin riesgo de ruido"*. Revisión prevista 2026-05-20.
- **Banner de estado en `ROADMAP.md`** — tabla resumen al inicio con los 9 bloques y su estado (A cerrado, B-H pendientes, I parcial). Lectura rápida del progreso del Bloque 0. Links a `adjustments-log` y `postmortems` para contexto de decisiones y errores.
- **Toda decisión futura tiene ya su sitio auditable:**
  - Ver errores pasados → `private/postmortems.md` (con patrones transversales al principio).
  - Ver decisiones pasadas y efecto medido → `private/adjustments-log.md`.
  - Ver coste real y tendencias → `private/costs.md` + `data/costs.csv`.
  - Ver calidad de cada edición → `private/self-review/YYYY-wWW.md`.
  - Ver reparto de actores → `private/balance.md` + `docs/balance.md` (público).
  - Ver estado operativo → `data/proposals_history.json` + `data/bench/results_v1.json`.
- **Bloque B arranca cuando el editor confirme** — rediseño web sin coste API, 2-3 turnos para páginas principales (home reescrita, `build_index.py` documental, `/radar/`, `/propuestas/`, `/actores/`, `/balance/`, `/sin-dato/`, `/estadisticas/`, `/estado/`, `/politica-editorial/`, `/metodologia/`, `/correcciones/`, `/cita-esto/`).

---

## 2026-04-20 — Política de aprendizaje de errores formalizada

- **Patrones transversales añadidos al principio de `private/postmortems.md`** — 4 patrones conocidos hasta la fecha con salvaguardas vinculantes. Cada error nuevo se coteja primero con estos patrones antes de añadir uno nuevo. Si encaja, la causa es repetición (agravante); si no, se documenta nuevo patrón.
  - **P1. Flujos multi-paso sin orquestador** — corregido con `bench_full.py` y `regen_edition.py`.
  - **P2. Verificadores demasiado estrictos** — corregido con distinción 404/410 bloquea vs 403/5xx avisa en `verify.py`.
  - **P3. Umbrales calibrados sin datos** — pendiente de primera revisión mensual con ≥4 ediciones publicadas.
  - **P4. Contaminación del contexto del LLM por contenido de versiones antiguas** — se resolverá en Bloque C cuando W16-W17 antiguas se eliminen y las 8 ediciones retroactivas W10-W17 se regeneren bajo modelo documental.
- **Confirmado: política de contenido retroactivo** — W16 y W17 actuales (modelo antiguo) se **borran** al arrancar Bloque C. Originales quedan en histórico git para auditoría futura. Las 8 nuevas ediciones se generarán desde cero bajo modelo documental, sin contaminar unas a otras (orden de producción: W17 → W10 hacia atrás; publicación en orden cronológico natural W10 → W17 con commits separados).
- **Umbral de rigor pendiente de revisión** — hoy salta alerta en `<7`. Propuesta editor: considerar subir a `<8`. Decisión deferida hasta tener 4-5 ediciones bajo modelo documental. Subirlo ahora sin datos podría saturar de alertas. Registrado como P3.
- **Auditabilidad del sistema confirmada** — toda la información queda en archivos para revisión del editor:
  - `private/postmortems.md` — errores + patrones + salvaguardas.
  - `private/self-review/YYYY-wWW.md` — cada self-review archivado.
  - `private/self-review-log.md` — agregado de los que dispararon alerta.
  - `private/bench-log.md` — historial de ejecuciones de benchmark.
  - `private/balance.md` — dashboard privado actualizado tras cada edición.
  - `private/costs.md` — gasto y capa actual.
  - `data/costs.csv` — cada llamada API registrada (append-only).
  - `data/proposals_history.json` — histórico de propuestas documentadas.
  - `data/bench/results_v1.json` — resultados crudos del benchmark.

---

## 2026-04-20 — Pipeline end-to-end + 2ª iteración con rigor subido a 7

- **Primera ejecución completa del pipeline documental** — `python -m src.report` corrió de principio a fin: ingest (35 items, 2 RSS locales vacíos), classify (19 housing, 2 formal, 2 en_movimiento), extract (4 candidatos → 3 propuestas, 0 disputas Opus), rescue (vacío, primera vez), generate (Opus con prompt documental), verify (11 URLs OK, 0 verbos prohibidos), balance (dashboard público + privado), self_review (score rigor=6, resto ≥7). Coste real: ~2,25 €.
- **Self-review detectó 8 warnings útiles** — propuestas duplicadas (residencias × 2 fuentes contadas como 2 propuestas separadas), Marí mal clasificada como `otro` en lugar de `institucional_publico`, cifras sin declarar naturaleza ("~200 trabajadores" sin marcar como estimación periodística), carry-over no marcado en señales del 11-abr, `blocks_cited` inflado con "policial" (Policía aparece en señales pero no propone). Las 3 sugerencias de Sonnet para ajustar prompt se aplicaron literal.
- **4 mejoras del prompt de `generate.py`** — (1) deduplicación: fusionar propuestas con mismo objetivo+actor_type+horizon en una sola con fuentes secundarias listadas; (2) etiquetar naturaleza de cada cifra la primera vez que aparece (`(dato oficial)` / `(estimación periodística)` / `(orientativa)`); (3) marcar carry-over: señales anteriores al lunes de la semana cubierta se marcan con `*(carry-over de la semana ISO XX)*`; (4) `blocks_cited` solo incluye tipos de actor que PROPONEN, no los de señales.
- **Mejora del prompt de `extract.py`** — regla específica para clasificar cargos institucionales (Consell, Govern, IBAVI, Ayuntamientos, cargos como "conseller", "director general", etc.) como `institucional_publico`, no `otro`. Eliminada la ambigüedad que llevó a Marí a `otro`.
- **Nuevo script `scripts/regen_edition.py`** — orquestador ligero que re-ejecuta extract → rescue → generate → verify → balance → self_review sin gastar API en ingest/classify. Para iterar prompts rápido. Asume que existe `data/classified.json` de una ejecución previa.
- **Post-mortem #2: verify bloqueó por 403 de Cadena SER** — `httpx` sin User-Agent estándar es rechazado por medios grandes (SER, El País, La Vanguardia, IB3). Verify hacía exit 1 con 403, borraba la edición y alertaba crítico (issue #2 en GitHub como fallback). Coste del falso positivo: ~1,10 €. Fix: `httpx.Client` con User-Agent Chrome + `Accept-Language` + `Accept`, y distinguir bloqueantes (404/410 — URL rota) de soft_warnings (401/403/405/429 — bloqueo de bots, URL viva). Issue cerrado. Registrado en [`private/postmortems.md`](private/postmortems.md).
- **2ª iteración (regen_edition tras fixes)** — resultados limpios: reglas=7, rigor=**7 (subió de 6)**, balance=8, cobertura=8, claridad=9. Todos ≥7, no dispara alerta. `proposals_formal_count` cayó de 2 a 1 tras fusión (residencias es una sola propuesta). `(estimación periodística)` y `(dato oficial)` presentes en las señales. Dos señales marcadas correctamente como `*(carry-over de la semana ISO 15)*`. Marí clasificada como `institucional_publico`. Coste: ~0,80 €.
- **7 warnings menores pendientes para próxima iteración** — Marí sin apellido/cargo explícito en el cuerpo, "patronales" y "sindicatos" usados genéricamente sin identificar CAEB/PIMEEF/UGT/CCOO, informe sectorial sin autor nombrado, aviso visual de carry-over inconsistente en mapa de posiciones, metodología de la cifra 200 de El País no explicitada, blocks_cited sin glosario, **edición W16 antigua en contexto del generador contamina** (incluye propuestas propias del modelo antiguo). Los 6 primeros son detalles a iterar. El séptimo se resuelve con el Bloque C (borrar W16-W17 antiguas al regenerar 8 ediciones retroactivas bajo modelo documental).
- **Gasto acumulado del día: 6,11 €** (de los cuales ~1,67 € desperdiciados en dos errores documentados). Gasto mes en curso: **5,02 €** (capa 🟢 verde, <6 €). Margen tope blando: 6,98 €. Margen tope duro: 14,98 €.
- **Bloque A del ROADMAP: cerrado**. Pipeline funcional end-to-end, verificado, con self-review que supera umbral 7/10. Siguiente: Bloque B (web rediseñada) o Bloque C (8 ediciones retroactivas).

---

## 2026-04-20 — Benchmark final + reparto de modelos decidido + classify/extract reescritos

- **Benchmark final sobre gold auto (17 items validados)** — resultados:
  - classify: los 3 modelos empatan al 94,1%.
  - detect: los 3 al 94,1%.
  - extract: Haiku y Sonnet 97,1%, Opus 70,6%.
  - Coste total benchmark (2º run correcto): 0,59 €.
- **Hallazgo metodológico**: Opus sin thinking cae en extract porque el gold lo generó Opus CON thinking. Opus+thinking llega a conclusiones más elaboradas que Opus sin thinking, y eso penaliza al Opus "normal" del pipeline. No es que Haiku sea intrínsecamente mejor; es que el benchmark mide "acuerdo con Opus-thinking" y los pequeños coinciden mejor con ese árbitro.
- **Dataset v1 limitado**: solo 4-5 propuestas reales de 17 items. Acertar "vacío" es tarea fácil. Extract está poco estresado. Conclusión: ampliar dataset con más propuestas complejas para el re-benchmark mensual.
- **Decisión del editor: opción C (belt and suspenders)** — Haiku como base en las 3 tareas de entrada; Sonnet valida cada extracción no vacía; Opus reextrae si Sonnet marca invalid. Cláusula de reevaluación al primer re-benchmark mensual: si Haiku alucina mucho (correcciones recibidas o fallback Opus >20%), promovemos extract a Sonnet como principal.
- **Coste mensual proyectado total con reparto final: ~6-7 €/mes** (incluye pipeline operativo + self_review semanal + auditoría trimestral + re-benchmark mensual). Dentro del tope blando 12 €.
- **Reparto documentado en [`ARQUITECTURA.md`](ARQUITECTURA.md#reparto-de-modelos--decisión-2026-04-20)** con tabla completa, razonamiento, proyección de costes y cláusula de reevaluación.
- **`src/classify.py` reescrito** — nuevo schema con `proposal_type` (formal|en_movimiento|ninguna) y `proposal_actor_hint`. Integra detect dentro de classify para una sola llamada Haiku. Resiliencia: si Haiku devuelve menos items que el input, sigue con fallback conservador (marca items sin clasificación como no-housing). Prompt caching activado.
- **`src/extract.py` nuevo** — pipeline de tres pasos Haiku base → Sonnet valida → Opus fallback si disputa. Output incluye metadata por propuesta (`produced_by`, `validator_verdict`, `was_disputed`). Alerta si ratio de disputas >20%. Campos del schema actualizado (coaliciones, state=en_movimiento, statement_verbatim). Principio "cero inferencia" explícito en el prompt.
- **Coste total del día (pipeline + estudios): ~1,96 €** de los cuales 0,57 € desperdiciados por el error del gold manual (registrado en `private/postmortems.md`).
- **Pendiente próximo turno**: `src/verify.py` (URLs + trazabilidad + verbos prohibidos), `src/rescue.py`, `src/balance.py`, `src/generate.py` (reescribir con nuevo prompt documental), `src/self_review.py`, adaptar `src/report.py`. Todo bajo el reparto decidido.

---

## 2026-04-20 — Primer benchmark ejecutado + post-mortem del desajuste gold

- **`generate_gold.py` ejecutado con éxito** — Opus con `thinking.type=adaptive` + `output_config.effort=high` generó gold para 20 items; Sonnet validó 17; 3 discrepancias apartadas. Coste real: 0,80 € (muy por debajo de los 3 € estimados gracias a prompt caching). Discrepancias: n08 (coalición: classify pierde sindicatos por limitación del enum actor), n09 (Opus infirió nombres concretos CAEB/PIMEEF/CCOO/UGT que la noticia solo dice genéricamente — exactamente el tipo de alucinación que el pivote quiere evitar, el sistema lo atrapó), n10 (inconsistencia interna de Opus entre detect y extract). Primer uso real del sistema de gold autogenerado: funcionó como se diseñó.
- **Fix `thinking` API desactualizada** — el formato `{"type": "enabled", "budget_tokens": N}` ya no es válido en `claude-opus-4-7`. Cambiado a `{"type": "adaptive"}` + `output_config={"effort": "high"}`. Error 400 con mensaje claro → fix en una línea. Sin coste (400 no cobra).
- **Fix `notify.py`: no crear issues en ejecución local** — el fallback a issue GitHub disparaba en local cuando no hay `TELEGRAM_BOT_TOKEN`. Ahora solo dispara si `GITHUB_ACTIONS=true` o si `level=critical`. En local basta con el log en stdout. Issue #1 (falso positivo del primer test) cerrado.
- **Post-mortem abierto: [`private/postmortems.md`](private/postmortems.md)** — registro público-interno de errores evitables con coste o impacto. Primera entrada: desajuste entre `generate_gold.py` (produjo `gold_auto_v1.json`) y `run_benchmark.py` (leía `gold_standard_v1.json` manual hardcoded). El primer benchmark costó 0,57 € desperdiciados antes de detectar el problema. Causa raíz: los dos scripts se diseñaron por separado sin conexión. Responsable: Claude. Lección: flujos multi-paso con coste deben orquestarse por código, no por costumbre.
- **Prevención aplicada:**
  1. `run_benchmark.py` prefiere gold_auto con fallback a manual + aviso visible en log.
  2. Nuevo orquestador [`scripts/bench_full.py`](scripts/bench_full.py) — un solo comando que genera gold si falta y ejecuta benchmark contra gold_auto. Verificaciones entre pasos. Abort si falta ANTHROPIC_API_KEY.
  3. `ESTUDIO-3-MODELOS.md` actualizado: el comando recomendado pasa a ser `python -m scripts.bench_full`. Los individuales quedan como bajo nivel.
- **Primer benchmark con gold auto: pendiente de ejecución por el editor con el orquestador `bench_full`**.

---

## 2026-04-20 — Schema con coaliciones, página /radar/, gold autogenerado

- **Coaliciones en el schema** — nuevos valores de `actor_type`: `coalicion_intersectorial` (patronal + sindicato) y `coalicion_institucional` (con administración o con sociedad civil organizada). Regla: cuando varios actores firman una propuesta juntos, el campo `actor` contiene los nombres literales de todos los firmantes separados por coma, sin elegir "primario". Fidelidad al consenso real firmado. Caso W15 (CAEB+PIMEEF+CCOO+UGT sobre residencias) es el ejemplo canónico.
- **Nueva página pública `/radar/`** — señales en movimiento: todo lo que un actor con nombre ha anunciado pero aún no ha concretado (intenciones, estudios encargados, debates abiertos, anuncios sin plan). Tres niveles nuevos en el schema de la tarea `detect`: `formal` (va a `/propuestas/`), `en_movimiento` (va a `/radar/`), `ninguna` (no se extrae). Juego con la marca "Housing Radar": el proyecto literalmente tiene su radar interno de señales tempranas. Ciclo de vida: `en_movimiento` → promovida a `propuesta` cuando se concreta, con trazabilidad.
- **Caso n17 del benchmark** (encargo de estudio de viviendas vacías del Consell) reclasificado de `formal` a `en_movimiento`. Criterio estricto: si no hay medida concreta, no es propuesta. Aparece en `/radar/` hasta que el Consell anuncie medida.
- **Nuevo estado `en_movimiento`** añadido al enum `state`. Horizonte `temporada_2027` añadido a `horizon`.
- **Gold standard automatizado** (`scripts/generate_gold.py`) — el editor no revisa el gold manualmente. Opus 4.7 con extended thinking genera la solución ideal para cada tarea y Sonnet 4.6 la valida. Items con consenso entran en gold; discrepancias se apartan. Coste una vez: ~3 €. Re-ejecutable en cada re-benchmark mensual. Output: `data/bench/gold_auto_v1.json` + `data/bench/gold_discrepancies.json`.
- **Sistema de seguimiento mixto** — Telegram para alertas puntuales (benchmark completado, auditoría trimestral lista, self-review con score <7, coste cruza capa, modelo cambia ratio) + logs persistentes en repo para profundizar cuando se quiera: `private/bench-log.md`, `private/auditoria-log.md`, `private/self-review-log.md`, `data/bench/trends.csv`, `data/audit/trends.csv`. Editor no revisa nada activamente; el sistema escribe y avisa.
- **Apunte estratégico** — el nombre del proyecto ("Ibiza Housing Radar") se reevaluará al elegir dominio propio. La página `/radar/` queda diseñada para ser independiente del nombre final del proyecto: el juego con "radar" se conserva aunque el proyecto se llame de otra forma. Registrado en [`ESTUDIOS-PENDIENTES.md #2`](ESTUDIOS-PENDIENTES.md).
- **Documentos actualizados** — `ARQUITECTURA.md` (schema ampliado + coaliciones + niveles de propuesta), `DISENO-WEB.md` (página `/radar/` con estructura y ciclo de vida), `ROADMAP.md` (tareas B31 `/radar/`, B32 gold autogenerado, B33 sistema de seguimiento), `ESTUDIOS-PENDIENTES.md` (apunte sobre renombrar proyecto), `ESTUDIO-3-MODELOS.md` (flujo con gold auto), `data/bench/gold_standard_v1.json` (v1.1 con schema nuevo). Nuevos: `scripts/generate_gold.py`, `private/bench-log.md`, `private/auditoria-log.md`, `private/self-review-log.md`, `data/bench/trends.csv`, `data/audit/trends.csv`.

---

## 2026-04-20 — Refuerzo del pivote: autoevaluación, archivo de huecos, tracking potente

- **Restricción estructural asumida** — el editor no es experto en vivienda ni en derecho; la revisión humana se limita a un check visual de 2-3 min tras cada publicación (Telegram OK, web carga bien, 2 URLs al azar funcionan, indicadores de transparencia verdes). El pipeline **no puede depender del editor para fact-checking experto**. De ahí el principio nuevo: **"cero inferencia del LLM"** — solo reproduce y ordena lo que está en la fuente, nunca infiere, nunca deduce. Si no hay dato, se marca "no evaluada" o "sin dato público"; si no hay URL, no publica. Esto refuerza las 5 reglas duras del pivote y las hace más estrictas.
- **Archivo público `/sin-dato/`** — nueva página que convierte los "no evaluada" en oportunidad de enriquecimiento por el público. Tabla filtrable con todas las propuestas que tengan al menos un campo pendiente, con botón "aportar este dato" → formulario Formspree con URL obligatoria. Cada aportación verificada se incorpora con `dateModified` y traza en `/correcciones/`. Triple ventaja: oro oculto adicional (preguntas sin respuesta pública visibles), refuerzo de "cero inferencia" (mejor decir "no sé"), SEO (contenido dinámico + backlinks de aportantes).
- **Tres niveles de autoevaluación** para compensar la revisión humana limitada:
  1. **Semanal con Sonnet** (`src/self_review.py`): tras publicar cada edición, Sonnet puntúa 1-10 en 5 dimensiones (cumplimiento de reglas, rigor factual, balance, cobertura, claridad) y detecta warnings. Si algún score <7, Telegram urgente con link. Coste: ~0,60 €/mes.
  2. **Trimestral con Opus** (`src/quarterly_audit.py`): cada 13 semanas, Opus lee las 13 ediciones + self-reviews + balance y genera informe público en `/auditoria/YYYY-qN/` con cumplimiento sostenido de reglas, patrones emergentes, comparativa de calidad, recomendaciones concretas, señales sistemáticamente perdidas. Coste: ~1,50 €/mes promediado.
  3. **Re-benchmark mensual de modelos** (`src/model_rebench.py`): 10 noticias nuevas, ejecutar las 6 tareas del pipeline con los 3 modelos, detectar desviación >20% en ratio calidad/coste. Coste: ~1 €/mes.
- **Sexto criterio del estudio de modelos: impacto real (correcciones recibidas/edición)**. Proxy directo de calidad percibida. Si el modelo barato genera más correcciones que el caro, el "ahorro" se paga en credibilidad. Se mide a partir del segundo mes cuando `/correcciones/` acumule datos; entra en el re-benchmark mensual, no en el benchmark inicial.
- **Coste mensual proyectado total bajo pivote + autoevaluación: ~9,86 €/mes** (7,36 € operación + 3,10 € autoevaluación). Cruza el tope blando actual (8 €). **Decisión: subir tope blando a 12 €** con nueva capa 🟠 naranja 9-12 €, capa 🔴 roja blanda 12-20 €. Misma filosofía "avisa pero publica". Tope duro sigue en 20 €.
- **Tracking de costes potente** (ampliación de `src/costs.py`): dashboard privado con coste por módulo + coste por modelo + cache hit rate + tendencia 8 semanas + estimaciones semanal/mensual/anual + alertas de desviación >30% + alertas de cache hit <70%. Dashboard público `/costes/` simplificado con agregados y capa actual. Todo con datos reales medibles.
- **Página pública `/auditoria/YYYY-qN/`** — las auditorías trimestrales salen públicas. El proyecto se audita a sí mismo en abierto. Transparencia radical = presión sana sobre el pipeline.
- **Página pública `/estado/`** estilo Solar Low-Tech — histórico operacional del pipeline (ejecuciones, retrasos, versiones, contadores globales). Complementa `/correcciones/` (errores editoriales) con errores operacionales.
- **Newsletter confirmado como modelo híbrido** — gratis en Fase 0, tier Pro opcional en Fase 2. Nunca paywall al lunes.
- **Estudio 3 modelos a ejecutar primero** — pendiente de OK del editor para arrancar curación del dataset (20-30 noticias curadas + gold standard manual). Coste del estudio: ~3-5 € una vez. Tiempo: ~6 h de trabajo de Claude + ~30 min de consulta al editor para casos ambiguos.
- **Documentos actualizados** — [`ARQUITECTURA.md`](ARQUITECTURA.md) con 3 módulos nuevos + nuevo coste estimado + sistema de capas. [`DISENO-WEB.md`](DISENO-WEB.md) con 4 páginas nuevas (`/sin-dato/`, `/auditoria/`, `/costes/`, `/estado/`). [`ESTUDIOS-PENDIENTES.md`](ESTUDIOS-PENDIENTES.md) con 6º criterio y re-benchmark continuo. [`ROADMAP.md`](ROADMAP.md) con tareas A12-A16, B27-B30, E4-E6.

---

## 2026-04-20 — Decisiones del editor sobre Fase 0 del pivote

- **16 decisiones resueltas** por el editor — documento [`DECISIONES-PENDIENTES.md`](DECISIONES-PENDIENTES.md) actualizado con cabecera nueva de "decisiones resueltas" y detalle de cada una.
- **W16-W17 se borran** (no se reescriben). Decisión más drástica que la recomendación inicial: archivo público arranca limpio bajo modelo documental sin residuos del modelo antiguo. Originales conservadas en histórico git pre-merge.
- **Contenido retroactivo a 2 meses, 8 ediciones (W10-W17)**, cubriendo marzo y abril 2026. Arco narrativo "de planificación pre-temporada al desalojo de asentamientos en vísperas de mayo". Veracidad alta con nota metodológica visible. Coste puntual ~13,52 € puede cruzar el tope blando de abril; asumido. Tiempo humano estimado 10-17 h. Orden de producción sugerido: hacia atrás desde W17 (más fácil con RSS reciente) hasta W10 (mayor búsqueda manual en archivos de diarios). [`CONTENIDO-RETROACTIVO.md`](CONTENIDO-RETROACTIVO.md) reescrito con el plan completo.
- **Firma "Raúl S." sin foto ni email directo**, solo formulario. Apunte de pasar a nombre completo + email propio cuando haya dominio.
- **Dominio propio confirmado, pero con estudio previo** antes de comprar. Apuntado en [`ESTUDIOS-PENDIENTES.md #2`](ESTUDIOS-PENDIENTES.md).
- **Analítica ambiciosa** — el editor pide algo "muy potente": GoatCounter + Search Console + dashboard público de estadísticas del corpus editorial + transparencia operacional tipo Solar Low-Tech. Apuntado como [`ESTUDIOS-PENDIENTES.md #7`](ESTUDIOS-PENDIENTES.md).
- **Newsletter de pago valorado y descartado como modelo puro**. Contradice misión, mercado demasiado pequeño, rompe citabilidad, asimetría web/email absurda, complejidad operativa. Recomendación: **modelo híbrido** (gratis base + tier Pro opcional) en Fase 2, no en Fase 0. Detalle y razones en [`ESTUDIOS-PENDIENTES.md #4`](ESTUDIOS-PENDIENTES.md).
- **Página `/recursos/` sale de Fase 0**, se estudia en Fase 1.
- **Balance público con prioridad alta** — se convierte en diferenciador principal del proyecto junto con el pivote documental. Se publica desde día 1 y se amplía continuamente con estadísticas del corpus.
- **Diseño: mantener + inspiración Solar Low-Tech**. Nueva sección en [`DISENO-WEB.md`](DISENO-WEB.md) con 8 elementos a importar: indicadores de transparencia en footer, tipografía mono para datos, notas al margen, posible dithering en OG images, manifiesto visible, rechazo de JS innecesario, accesibilidad radical, página `/estado/` con histórico operacional.
- **Redes sociales fuera de Fase 0** — se estudian en Fase 1. Se quita Bluesky y Mastodon del Bloque F.
- **🔴 Estudio urgente: integración de 3 modelos IA** (Haiku + Sonnet + Opus). Reparto por tarea: Haiku para clasificación y vigencia; Sonnet para extracción estructurada y fact-check; Opus para composición y auditorías cualitativas. Coste estimado ~1,69 €/edición, ~6,76 €/mes. Primera semana de Fase 0 antes de contenido retroactivo. Detalle en [`ESTUDIOS-PENDIENTES.md #1`](ESTUDIOS-PENDIENTES.md).
- **Licencia CC-BY 4.0 confirmada** para dataset de propuestas y contenido editorial.
- **Fecha de relanzamiento propuesta: lunes 18 de mayo de 2026** — deja 4 semanas desde hoy, 2 semanas de margen sobre inicio de temporada, tiempo para los 3 estudios urgentes. Pendiente de confirmación del editor.
- **Nuevo documento [`ESTUDIOS-PENDIENTES.md`](ESTUDIOS-PENDIENTES.md)** consolida los 8 estudios pendientes (urgentes + diferidos) con prioridad, plazo y entregable cada uno.
- **[`ROADMAP.md`](ROADMAP.md) actualizado**: Bloque C a 8 ediciones, Bloque G ajustado (quita `/recursos/`), Bloque F ajustado (quita bots sociales), nuevo Bloque I con 5 estudios/tareas previas bloqueantes antes del lanzamiento.

---

## 2026-04-20 — Pivote estratégico aprobado: observatorio documental

- **Decisión aprobada por el editor** — tras el estudio crítico del corpus W16-W17, se confirma el pivote de "generador de propuestas" a "observatorio documental". El LLM deja de generar propuestas y pasa a extraer, ordenar y verificar las propuestas reales que los actores con nombre formulan cada semana. Documento fundacional en [`PIVOTE.md`](PIVOTE.md).
- **Branch aislado de trabajo** — `pivote/observatorio-documental` creado desde main el 2026-04-20. Todo el trabajo del pivote vive ahí hasta merge. `main` intacto como salvaguarda de reversibilidad.
- **Expediente estratégico completo** — 7 documentos consolidan la decisión, el roadmap, la arquitectura técnica, el diseño web y el plan SEO: [`PIVOTE.md`](PIVOTE.md), [`ROADMAP.md`](ROADMAP.md), [`ARQUITECTURA.md`](ARQUITECTURA.md), [`DISENO-WEB.md`](DISENO-WEB.md), [`SEO.md`](SEO.md), [`CONTENIDO-RETROACTIVO.md`](CONTENIDO-RETROACTIVO.md), [`DECISIONES-PENDIENTES.md`](DECISIONES-PENDIENTES.md). `PLAN.md` se mantiene como referencia histórica con aviso al inicio que redirige al nuevo expediente.
- **Cinco reglas duras del pivote** — publicables en `/politica-editorial`: (1) solo propuestas con autor identificado y URL verificable; (2) el observatorio no genera propuestas propias; (3) ningún actor excluido por filiación; (4) balance de actores auditado y público cada trimestre; (5) correcciones públicas con traza. Vinculantes y no negociables.
- **Fase 0 ambiciosa** — relanzamiento completo con pipeline técnico nuevo (módulos `extract.py`, `verify.py`, `rescue.py`, `balance.py`), 15+ páginas web (home dual, `/politica-editorial`, `/balance`, `/actores`, `/propuestas`, `/recursos`, `/glosario`, `/como-usarlo`, `/cita-esto`, `/aportar`, `/datos-abiertos`, `/explica/*`), SEO masivo (schema.org JSON-LD, OG images por edición, sitemap, 8 páginas long-tail), contenido retroactivo de 4 ediciones simuladas (W14-W17), analítica GoatCounter, newsletter Buttondown, bots Bluesky y Mastodon. Coste API estimado ~5,85 €/mes dentro del tope blando 8 €.
- **Regla dura de diseño visual** — los partidos políticos se muestran siempre en gris neutro, nunca con su color de marca. Decisión editorial para reforzar imparcialidad visual. Bloques no partidistas (sindicatos, patronales, tercer sector, académicos, judicial, institucional público) tipificados con paleta ampliada.
- **16 decisiones pendientes del editor** — listadas en [`DECISIONES-PENDIENTES.md`](DECISIONES-PENDIENTES.md) con opciones y recomendaciones. Bloquean el arranque de ejecución. La más relevante: reescribir W16-W17 bajo nuevo modelo (recomendado) o mantener con nota; comprar dominio propio ya (recomendado) o esperar tracción; relanzar en W18 (apretado) o W20 (recomendado, 3 semanas de preparación).

---

## 2026-04-20 — Estudio crítico de las propuestas (corpus W16-W17)

- **Auditoría completa de las 8 propuestas publicadas** — revisión sobre 9 dimensiones (concreción, rigor numérico, trazabilidad a señal, verificabilidad del precedente, viabilidad jurídica, viabilidad política, equilibrio ideológico, diversidad de actor, originalidad intra-serie). Documento completo en [`private/estudios/2026-04-20-propuestas.md`](private/estudios/2026-04-20-propuestas.md). Resumen: formato bien calibrado, control de calidad del contenido inexistente.
- **Tres hallazgos críticos** — (1) precedentes sospechosos de alucinación en al menos 3 propuestas (Jooble Workers Portugal, Reallotjament Barcelona con cifra específica, Zermatt cantón 1.200 temporeros 2019); (2) errores técnicos concretos (aritmética W17.1, error jurídico W17.2 sobre afectación retroactiva de 2 M€ ya recaudados, inviabilidad W17.3 bajo Directiva de Servicios); (3) sesgo estructural no declarado: 6/8 intervencionistas puras, 5/8 cargan sobre el Consell (PP+Vox), 0/8 sobre Govern Balear pese a ser competente en vivienda.
- **Palancas ciegas del generador** — cero propuestas en: derecho laboral (obligación empresa de alojar), fiscalidad penalizadora de vacío (LEH 12/2023), judicial (agilizar desahucios por subarriendo fraudulento, pese a caso documentado en señales), cooperativismo ciudadano. El modelo tiene un mapa mental restringido de qué es "política de vivienda".
- **Redundancia detectada** — W16.2 y W17.4 son la misma idea (residencias modulares en suelo público) en dos semanas consecutivas. Sin anti-duplicado, la temporada se llena de variantes.
- **Riesgo reputacional concretado** — el `PLAN.md` ya mencionaba "Opus tiende a propuestas progresistas" como riesgo sin mitigación; este estudio lo cuantifica y propone mitigación operativa.
- **Plan de mitigación en tres tiers** — Tier 1 (2-4 h, antes de la edición del 27-abr): fact-checker automático de precedentes con Haiku + declaración explícita de sesgo en `/metodologia`. Tier 2 (1 día, próximas semanas): regla de diversidad de actor + regla de pluralidad ideológica + rango obligatorio en cifras + anti-duplicado intra-serie, todo en el prompt. Tier 3 (2-4 h, cuando toque): verificador jurídico ligero + metadata por propuesta en front-matter + auditoría trimestral automática + checklist de revisión humana. Añadido a [`PLAN.md`](PLAN.md) como bloque nuevo "Calidad editorial de las propuestas (salvaguardas)" y filas dedicadas en la tabla de seguimiento.

---

## 2026-04-20 — Bloque operativo implementado: Telegram + privatización costes + euros

- **Bot de Telegram operativo** — `@ibiza_vivienda_bot` creado por Raúl vía @BotFather. Token y `chat_id` configurados como GitHub Secrets (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`). Ping de prueba recibido OK antes de cablear nada. Smoke test local de `src.notify` confirma entrega end-to-end.
- **`src/notify.py` nuevo** — módulo con `send_telegram(message, level)` usando `httpx` (ya en requirements, sin dependencia nueva) y `notify(message, level)` que delega a Telegram y cae a `gh issue create` si falla. Niveles soportados: `ok` ✅, `info` ℹ️, `warning` ⚠️, `critical` 🚨. Silencioso ante fallos de notificación para no romper el pipeline.
- **Refactor `src/costs.py` a euros + filosofía no-cortar-editorial** — mantiene USD como unidad interna (precisión, consistencia histórica del CSV) pero todo el display y topes en euros (tipo de cambio fijo 1 USD = 0,92 EUR, revisable cada 3 meses). Nuevos topes: `MONTHLY_SOFT_CAP_EUR = 8.00`, `MONTHLY_HARD_CAP_EUR = 20.00`. `assert_budget_available()` solo lanza excepción si se supera el duro. Añadido `_maybe_notify_threshold_crossing()`: detecta cruces de umbral (4/6/8/20 €) tras cada `record_call()` y notifica por Telegram solo el cruce más alto, sin spam. Dashboard movido a `private/costs.md` con nueva sección "Capa actual" y columnas en € y USD.
- **`private/costs.md` fuera de Jekyll** — carpeta `private/` al nivel raíz del repo, fuera de `docs/`, así que GitHub Pages no la sirve. El CSV `data/costs.csv` sigue en repo (visible vía GitHub UI), pero el dashboard ya no está indexado en la web pública. Eliminado `docs/costs.md`, `docs/_includes/header.html` sin enlace "Costes", `docs/_includes/footer.html` sin enlace "Transparencia de costes", `docs/acerca.md` y `src/build_index.py` actualizados para referir a "topes automáticos" en lugar de enlazar.
- **`src/report.py` con resumen Telegram + try/except global** — al terminar envía mensaje OK con semana, gasto mes y capa actual. Si cualquier fase lanza excepción, envía alerta `critical` con stack y re-lanza para que Actions marque el run como fallido. Importación de `notify` perezosa dentro del except para que un fallo en la red de seguridad no tape el error original.
- **Workflow actualizado** — `.github/workflows/weekly-report.yml` pasa `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` y `GH_TOKEN` al job. Permisos ampliados con `issues: write` para habilitar el fallback de alertas a issue. `git add` apunta a `private/costs.md` en lugar del desaparecido `docs/costs.md`.
- **README, STATUS, CLAUDE.md actualizados** — ruta del dashboard, nuevos topes en € y capas de alerta, nuevo módulo `notify.py`, filosofía no-cortar-editorial documentada. Tabla de troubleshooting con entradas específicas para Telegram caído y corte por tope duro.
- **Verificación local** — `python -m src.costs` regenera `private/costs.md` con formato correcto (gasto actual 1,78 €, 22 % del tope blando, capa 🟢 verde). `python -m src.build_index` regenera home sin enlace a `/costes/`. `python -m src.notify` entrega mensaje Telegram HTTP 200.

---

## 2026-04-20 — Trilingüe diferido, seguimos con privatización de costes + Telegram

- **Trilingüe ES/CA/EN pasa a diferido** — decisión revisada en la misma sesión. Razón: el concepto editorial todavía no está cerrado (identidad, metodología, newsletter, primera cita en prensa están pendientes). Montar 3 idiomas antes de validar demanda es gastar tokens y complejidad sin retorno. Todo el análisis hecho se conserva en PLAN.md bajo "Trilingüe — diferido" (Opción A estándar IEC + glosario eivissenc basado en estudio de medios locales, infra manual sin polyglot, pipeline Sonnet con validador, estructura de carpetas, SEO multilingüe). No se repite cuando se reactive.
- **Criterios de reactivación explícitos** — basta que se cumpla uno: (a) analítica muestra >10 % tráfico de fuera de España 4 semanas seguidas, (b) una cita o mención en medio catalán/anglófono, (c) newsletter >50 subs con al menos 5 de fuera de España o catalanohablantes, (d) Raúl lo pide. Claude debe proponer retomarlo en cuanto se cumpla alguno, límite una sugerencia por sesión, respetando el nivel de proactividad global.
- **Siguen activos: privatización de costes + alertas Telegram + refactor `costs.py` a €** — valor standalone, no dependen del trilingüe. Privatización saca `docs/costs.md` del sitio público y mueve dashboard a `private/costs.md`. Telegram con bot propio (token + chat_id como GitHub Secrets) notifica resumen semanal, excepciones y alertas por capas de coste (verde <4 €, amarilla 4-6 €, naranja 6-8 €, roja blanda 8-20 € con publicación intacta, roja dura >20 € con corte por runaway). Fallback a issue de GitHub si Telegram cae. Refactor `costs.py` migra a € y cambia filosofía: `assert_budget_available()` deja de lanzar excepción en tope blando; solo lanza en tope duro (20 €), blando solo alerta. Coste marginal del bloque: 0 €.
- **Topes calibrados para cubrir escenario trilingüe sin retocar** — coste actual ~2 €/mes, esperado trilingüe ~3,15 €/mes. Tope blando 8 € (≈4× actual, ≈2,5× trilingüe). Tope duro 20 € (≈10× actual, ≈6× trilingüe). Cuando se active el diferido no hay que volver a tocar la configuración.

---

## 2026-04-20 — Decisión previa (ahora superada): web y ediciones trilingües + privacidad de costes + alertas Telegram

- **Trilingüe ES/CA/EN desde el día 1, no solo chrome** — la versión EN para temporeros internacionales y CA para audiencia balear son parte del valor diferencial, no añadidos tardíos. Castellano sigue siendo fuente de verdad; CA y EN se generan traduciendo el ES con Sonnet para garantizar datos idénticos (cifras, URLs, actores, orden de bullets). Validador pre-publicación corta solo la versión traducida si hay divergencia, nunca la editorial en ES. Implementación Jekyll sin plugins externos (carpetas `/ca/` `/en/` manuales + `_data/i18n.yml`); `polyglot` descartado porque no está en allowlist de GitHub Pages y la infra manual cubre lo necesario.
- **Variante de catalán: estándar IEC + glosario eivissenc (Opción A)** — estudio previo del ecosistema periodístico local (IB3, Diario de Ibiza, Periódico de Ibiza, NouDiari, Última Hora) confirma que el hard news en catalán en las Pitiusas se hace en estándar IEC. IB3 abandonó el article salat en informativos en 2015 y es la referencia pública. Periódico de Ibiza usa balear solo en columnas de opinión ("Sa cadira des majors"). Diario de Ibiza y Última Hora ni siquiera editan en catalán. El balear escrito en registro periodístico carece de corpus amplio, riesgo de fallo del LLM alto. Opción A alinea el proyecto con IB3 y elimina el riesgo. Glosario obligatorio en el prompt: Eivissa (nunca Ibiza), eivissenc/a (nunca ibicenc), topónimos oficiales (Sant Antoni de Portmany, Santa Eulària des Riu…), microtopónimos literales (Sa Penya, Can Toni, Dalt Vila), siglas institucionales literales (Consell d'Eivissa, IBAVI, GOIB). Regla dura: nunca alterar palabras con mayúscula interior.
- **Privatización de costes** — `docs/costs.md` sale del sitio público; enlace "Costes" fuera del nav. Dashboard regenerado a `private/costs.md` (carpeta excluida de Jekyll). CSV `data/costs.csv` se queda en repo pero fuera del HTML indexable. Raúl lo consulta desde su clon o desde GitHub directo. Motivo: transparencia editorial no requiere exponer la contabilidad interna; simplifica la línea "proyecto coste-cero salvo IA" sin perder auditabilidad privada.
- **Topes de coste a €, tope duro a 20 €** — refactor de `src/costs.py`: todo el cálculo pasa a euros (antes en USD). Sistema de capas: verde <4 €, amarilla 4-6 €, naranja 6-8 €, roja blanda 8-20 € (**sigue publicando, solo avisa**), roja dura >20 € (corta). Filosofía explícita: "no podemos perder editorial por sobrecoste salvo runaway real". Tope blando (8 €) ≈ 2,5× coste esperado trilingüe (~3,15 €/mes); tope duro (20 €) ≈ 6× esperado, margen para detectar bugs sin quemar dinero.
- **Alertas Telegram + fallback a GitHub issue** — bot nuevo (Raúl crea con `@BotFather`, token y chat_id como GitHub Secrets). Módulo `src/notify.py` con `send_telegram(message, level)`. Notifica: resumen semanal tras publicar, alertas por capas de coste, fallos de validación de traducción (publicó solo ES), excepciones no controladas, API key inválida. Si Telegram cae, crea issue automático en el repo con la misma alerta. Doble red. Coste: 0 €.
- **SEO multilingüe apuntado como tarea dedicada** — no se improvisa dentro del montaje trilingüe; se aborda en sesión propia post-trilingüe (~2 h). Checklist: `hreflang` por página, canonical por idioma, OG `locale` + `locale:alternate`, JSON-LD `NewsArticle` con `inLanguage`, RSS separado por idioma (`feed.xml`, `feed.ca.xml`, `feed.en.xml`), sitemap con `xhtml:link`, títulos/descripciones optimizados por idioma (no solo traducidos). Fila dedicada en tabla de seguimiento de PLAN.md.
- **Coste revisado trilingüe** — ~3,15 €/mes (antes ~2 €/mes). Partidas: Haiku clasificación 0,06 €, Opus ES 2,70 €, Sonnet CA 0,30 €, Sonnet EN 0,30 €. Incremento +1,15 €/mes asumible. Decisión registrada en `PLAN.md` sección "Bloque trilingüe — privacidad de costes — alertas" y tabla de seguimiento.

---

## 2026-04-20 — Rediseño de la web a panel editorial

- **Home pasa de archivo de ediciones a panel de la última edición** — el problema era que el "oro" (señales con enlace a fuente, propuestas accionables, calendario A vigilar) vivía un click por debajo, dentro de cada edición. Ahora la home es un dashboard: headline serif gigante (excerpt de la edición) + lectura + CTAs en cover, con aside de 4 propuestas numeradas + 5 puntos A vigilar visible above-the-fold en desktop; debajo secciones completas de señales, cards de propuestas (actor/coste/primer paso, ancla directa a la edición para precedente y por-qué-ahora), A vigilar íntegra, archivo compacto con las 4 ediciones más recientes y línea "sobre el proyecto".
- **Refactor de collection Jekyll: `docs/editions/` → `docs/_editions/`** — Jekyll exige el prefijo `_` para que los archivos sean documentos de colección accesibles vía `site.editions` en Liquid; con `editions/` a secas estaban servidos como páginas sueltas pero `site.editions` venía vacío y la nueva página `/ediciones/` mostraba "sin ediciones". Permalinks dentro del front-matter inalterados (`/ediciones/YYYY-wWW/`), URLs públicas idénticas. Ajustados `generate.py`, `build_index.py`, `weekly-report.yml`, `edition.html` (incluido fix para que la fecha se renderice `YYYY-MM-DD` en vez del timestamp completo que Jekyll promociona al ser ahora documento).
- **`build_index.py` reescrito como parser de secciones** — antes extraía solo la sección "Lectura" de cada edición para el home cronológico. Ahora parsea la última edición completa: título, excerpt, lectura, señales, propuestas (con sus campos Qué/Actor/Precedente/Coste/Primer paso/Por qué ahora), A vigilar. Las propuestas se emiten como cards estructuradas con dl y enlace ancla a la edición. El slug del ancla se calcula replicando el auto_id de kramdown GFM (testeado contra kramdown real: conserva acentos y dígitos). Las ediciones anteriores salen en el archivo compacto. Coste API extra: 0 €, todo parsing.
- **Nueva página `/ediciones/` como archivo completo** — lista densa de todas las ediciones usando `site.editions | sort: date | reverse`. Pensada para crecer sin que sature la home.
- **CSS +667 líneas (`main.css`)** — nueva sección "Dashboard" con cover two-column en desktop (breakpoint 1024), grid de propuestas 1→2→4 columnas según ancho, señales en dos columnas a partir de 1024, archive densa y about minimalista. Mobile-first: base 1 columna, breakpoints en 640/720/1024/1280. Aprovecha las variables del tema existente (terracota + crema + serif + mono). Preview verificado en 375 y 1280 px, light y dark.
- **`.claude/launch.json` para preview local con Jekyll** — configurado `jekyll serve --baseurl ''` para desarrollo; `.gitignore` ignora `docs/_site/`, cachés Jekyll y `.claude/settings.local.json`.

---

## 2026-04-20 — Plan de mejora estratégico

- **Diagnóstico y plan de ruta** — auditoría completa del proyecto tras la primera edición automática. Conclusión: parte técnica sólida, pero impacto cero porque no hay distribución, ni tracking, ni feedback, ni fuente primaria propia. Creado [`PLAN.md`](PLAN.md) con 4 fases (base, distribución, contenido diferencial, red) + deuda técnica puntual + prioridades honestas + qué NO hacer. Documento vivo; cada punto cerrado se registra aquí.
- **Pivot a coste-cero salvo IA** — revisión del PLAN para que todo el roadmap sea 0 € directo. Único gasto aceptado: API Anthropic (~2 €/mes, ya en marcha). Dominio propio diferido hasta tracción (criterios explícitos en PLAN.md). Sustituciones clave: Plausible → GoatCounter, scraping Idealista → agregación de informes oficiales + crowd-sourcing ciudadano, evento pagado → co-organización con entidad local. Ahorro estimado: ~76 €/año sin pérdida relevante del 90 % del valor.
- **Sección de monetización añadida al PLAN** — estudio realista de 12 vías con rango de ingreso año 1 y año 3, esfuerzo, riesgo de misión. Techo honesto año 3-5: 5-20 k€/año combinados, nunca salario completo. Verdes: donaciones pasivas, grants periodísticos, consultoría institucional con transparencia, partnership institucional, charlas, libro anual, membership voluntario sin paywall del informe principal, licencia premium de dataset, servicios freelance derivados. Grises: merchandising simbólico en eventos. Rojas descartadas: publicidad, sponsored content, affiliate, paywall total, encargo del actor fiscalizado, ocultar financiación. Roadmap: 2026 Ko-fi pasivo + `/financiacion`; 2027 asociación + primer grant; 2028+ diversificación. Regla vinculante: transparencia radical publicando cada ingreso en `/financiacion`.
- **Observatorio de precios concretado y scraping descartado** — Fase 3.1 del PLAN detallada con Vía A (agregación de fuentes oficiales: Idealista/Fotocasa/INE/IBESTAT/Ministerio) + Vía B (formulario crowd-sourcing con cobertura de toda la isla, solo acuse automático, publicación en CSV anónimo, umbral mínimo de 10 respuestas por segmento para evitar reidentificación, sesgo muestral declarado). Scraping directo de portales descartado con justificación explícita (contradicción reputacional con la línea editorial, riesgo legal real por jurisprudencia Idealista, coste real de consulta legal 500-1.500 € vs los 80 € originalmente estimados, valor marginal sobre las vías limpias, mantenimiento frágil). Ruta de reserva vía API oficial condicionada a Fase 4.1 cerrada.

---

## 2026-04-20 — Día 1: montaje y primer informe

- **Scaffold inicial** — estructura `src/` (pipeline Python) + `docs/` (Jekyll root) + `.github/workflows/` (cron semanal + validación de key) + `data/` (estado). Base para todo lo demás.
- **Workflow de validación de key** — `validate-key.yml` con dispatch manual hace ping mínimo a la API de Anthropic con Haiku. Confirma HTTP 200 antes del primer run real sin consumir presupuesto.
- **Pipeline end-to-end + tema Jekyll custom** — ingest → classify → generate → build_index → costs → report. Tema editorial (Instrument Serif + Inter + JetBrains Mono, paleta terracota-crema, dark mode). Primera edición W16 escrita a mano como semilla.
- **Fix imports absolutos desde `src`** — primer run falló con `ModuleNotFoundError: No module named 'costs'` al ejecutar con `python -m src.report`. Cambiado `from costs import …` → `from src.costs import …` en `classify.py` y `generate.py`.
- **`max_tokens=8192` en Opus** — la W17 salió truncada exactamente a 4096 tokens. Subido el límite para que no corte ediciones largas.
- **Fix slug del link a GitHub** — `build_index.py` generaba link mal por mayúsculas en el week (`2026-W16` vs `2026-w16`). Resuelto con `| downcase`.
- **Jekyll: plugins SEO + feed + sitemap** — habilitados `jekyll-feed`, `jekyll-sitemap`, `jekyll-seo-tag`. `/feed.xml` y `/sitemap.xml` disponibles desde el día 1.
- **Push con retry + rebase** — race condition: el workflow falló porque se pushearon commits en paralelo durante la ejecución. Loop de 3 intentos con `git pull --rebase` en el step de commit.
- **`STATUS.md` de despertar** — documento único con TL;DR, estado, qué revisar, decisiones tomadas sin preguntar y troubleshooting. Punto de entrada para reengancharse al proyecto.
- **Fix URLs de Google News** — los enlaces iban a `news.google.com/rss/articles/…` firmado. Instalado `googlenewsdecoder>=0.1.7`, decodifica el protocolo firmado y devuelve la URL original. Ahora los enlaces apuntan a `elpais.com`, `diariodeibiza.es`, etc.
- **Limpieza de limitación conocida** — eliminada sección en `STATUS.md` sobre URLs de Google News tras verificar el fix en producción. Documentación consistente con el estado real.
- **`DIARIO.md` del proyecto** — creado el diario con formato viñetas + enlaces desde `README.md` y `CLAUDE.md`. Norma: toda decisión o fix estructural se registra aquí.
- **Títulos de edición en lenguaje natural** — sustituido `"Semana 17 · 2026"` por `"Semana 4 - Abril 2026"` (número = posición del jueves ISO dentro de su mes). Helper `human_week_title()` en `generate.py`. Aplicado a W16/W17 y al template del system prompt para futuras ediciones.
- **Home con lectura completa** — la tarjeta de cada edición en la home ahora muestra, además del excerpt de una línea, toda la sección "Lectura" (2-3 frases con enlaces y negritas). `build_index.py` extrae la sección del markdown y la vuelca con `markdown="1"` para que kramdown procese el contenido. Nueva clase `.edition-lectura` en `main.css`.
