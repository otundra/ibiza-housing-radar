# Diario del proyecto — Radar Ibiza (repo: ibiza-housing-radar)

Registro cronológico de hitos, decisiones y cambios relevantes.

Formato: agrupar por fecha, cada cambio una viñeta con el tema en **negrita** y una línea breve (qué/por qué/impacto combinados).

Reglas:
- Más recientes arriba.
- Solo cambios con valor de memoria futura. No entradas para commits triviales.
- No duplicar lo que ya dice Git: aquí va el contexto, no el diff.
- Si un cambio altera arquitectura o stack, también actualizar `CLAUDE.md` y `README.md`.
- **Cabecera obligatoria con fecha ISO + etiqueta temática** (desde 2026-04-23, [D0](DECISIONES.md)). Formato: `## YYYY-MM-DD [tema]`. Temas: `[pipeline]`, `[diseno]`, `[editorial]`, `[arquitectura]`, `[docs]`, `[costes]`, `[legal]`, `[feedback]`, `[sesion]`. Entradas anteriores al 2026-04-23 sin etiqueta se mantienen tal cual.

---

## 2026-04-23 [sesion] — Cierre del turno: mockup de /correcciones/, paso 0 del /cierre, regla de lenguaje llano

Cierre de la misma sesión que abrió la partición del auditor. Tres ítems cortos tras los commits `ae10613` (partición del auditor) y los tres commits paralelos de la otra conversación sobre el experimento `APRENDIZAJE.md` (entrada siguiente).

- **Mockup estático de la página de correcciones** entregado en [`docs/prototype/correcciones.html`](docs/prototype/correcciones.html). Copy del protocolo firme (las cuatro fases, canales, formulario visual), botón del formulario deshabilitado con suffix *"(pendiente)"*, banner *"mockup en rodaje"* al inicio. Canales (email y formulario) esperan al cierre del nombre del observatorio y del titular legal. Deriva de [D2](DECISIONES.md). Link en la navegación principal se deja para el Paso 2 del prototipo.

- **Regla general de lenguaje llano en cara pública** guardada como memoria del asistente (`feedback_lenguaje_llano_publico.md`). El editor pidió evitar `JSON`, `append-only`, `log`, `diff`, `trazar`, `schema`, `endpoint`, `pipeline` en textos visibles al público y traducirlos a español común. La regla 2 de `CLAUDE.md` ya tenía esta norma para *badges*; esta generalización cubre cualquier copy público. La sintaxis técnica sigue en docs internos (arquitectura, estudios), no en la web.

- **Comando `/cierre` mejorado**: añadido paso 0 de chequeo de concurrencia (`git fetch` + comparación local vs remoto al arrancar, para detectar otra sesión que haya commiteado a la vez), nota de paralelización en paso 2 (Edits independientes en tool calls paralelos), aclaración en paso 3 (un commit puede tocar varios archivos si es la misma decisión lógica). Disparado por el incidente de hoy con dos sesiones concurrentes editando archivos a la vez — la otra cerró sin conflicto por coincidencia, no por diseño.

**Decisiones pequeñas tomadas autónomamente en este turno** ([D7](DECISIONES.md)):
- Nombre del archivo del mockup: `correcciones.html` (español, precedente `metodo.html`).
- Wordmark del mockup en `radar))vivienda_ibiza` (orden antiguo) para no romper consistencia con los otros prototipos pausados; migración al wordmark oficial `radar))ibiza_vivienda` se hará cuando arranque el Paso 2 del prototipo.
- Botón del formulario deshabilitado con suffix visual *"(pendiente)"* en vez de `alert()`.
- Footer del mockup se auto-enlaza (`href="correcciones.html"` con `aria-current="page"`); los otros prototipos mantienen `href="#"` hasta el Paso 2.
- Regla de lenguaje llano guardada como memoria, sin propagación a `CLAUDE.md` (no hubo OK explícito del editor para generalizar la regla 2). Queda apuntado.

---

## 2026-04-23 [docs] — Experimento APRENDIZAJE.md: feedback formativo al cierre (solo-ibiza)

Nuevo archivo [`APRENDIZAJE.md`](APRENDIZAJE.md) en la raíz como log experimental de feedback formativo sobre cómo el editor desarrolla el proyecto. Cada `/cierre` (Paso 6 añadido) evalúa si hay algo concreto observable (decisiones, alcance, priorización, comunicación, docs, coste, proceso, verificación); si lo hay, una entrada con formato fijo (Observación / Patrón / Mejor próxima vez). Si no, *"sin feedback hoy"* y no fuerza.

**Diseño decidido en esta sesión** ([D8](DECISIONES.md)):

- **Primera propuesta:** archivo global `~/.claude/APRENDIZAJE.md` + Paso 6 en la plantilla + replicado en los 4 proyectos. El editor redujo a **solo este proyecto** y pidió reversibilidad explícita antes de aprobar.
- **Entregado:** `APRENDIZAJE.md` local + Paso 6 en [`.claude/commands/cierre.md`](.claude/commands/cierre.md) con sección *"Cómo desactivar"* (dos pasos, ~30 seg).
- **Revertidos en la misma sesión:** el `~/.claude/APRENDIZAJE.md` global, la sección *"Aprendizaje transversal"* de `~/.claude/CLAUDE.md`, y el Paso 6 de `~/Documents/GitHub/.claude-template/commands/cierre.template.md` (los proyectos futuros creados desde plantilla no heredan el experimento).
- **Mantenidas como mejora independiente del experimento** en la plantilla: `(si existe)` en la tabla de docs opcionales del cierre y la regla de *"NO toqué"* basada en existencia real (evita ruido en proyectos con menos docs).

**Principio registrado:** reversibilidad explícita y alcance mínimo son **prerrequisitos** de cualquier experimento operativo, no características opcionales. Primera entrada en `APRENDIZAJE.md` refleja la observación.

**Cómo desactivar si deja de aportar:** `git rm APRENDIZAJE.md` + quitar Paso 6 de `.claude/commands/cierre.md`. Commit único `chore(cierre): retira experimento de feedback formativo`.

---

## 2026-04-23 [arquitectura] — Partición del auditor en mínimo viable + iteración, opción (d) del log, marco de tres hitos grandes

Sesión completa de rediseño del plan del auditor con el editor, abierta tras el cierre del estudio de costes. Contexto: el plan de 4 semanas con las 5 capas desde el día uno estaba aprobado, pero al arrancar el editor expresó *"no siento que llevo las riendas"* con las 34 tareas de la Revisión Fase 0.5 abiertas en paralelo. Reencuadre completo del alcance del auditor, del frame de trabajo de la Fase 1 y del protocolo de correcciones.

**Decisiones cerradas ([D1](DECISIONES.md) a [D7](DECISIONES.md)):**

- **Partición del auditor en mínimo viable + iteración** ([D1](DECISIONES.md)). PI9 se parte en dos bloques. MVP (2 sem): capa 2 ciega Sonnet + comparador determinista + tres heurísticas (cruce de fuentes, verbatim match, whitelist V1) + log público con protocolo de correcciones + integración con el pipeline. Sin Opus formalizado como capa, sin cuarentena navegable, sin dashboard, sin repaso mensual IA. Iteración posterior (2-3 sem): Opus explícito, página `/revision-pendiente/`, dashboard `/auditor/`, capa 5bis. Motivo: el 80 % de la transparencia ya está en el MVP; la iteración es confort y optimización, no defensa. Reduce la escalada de complejidad para el editor mientras aprende el sistema.

- **Log público desde el día uno + protocolo formal de correcciones en 72 h** ([D2](DECISIONES.md)). Opción (d) elegida entre cuatro alternativas evaluadas (público tal cual / retraso 30 días / privado con métricas públicas / público + protocolo). Campo `corrections` append-only en cada JSON. Canales email (diferido hasta cierre del nombre) + formulario con backend webhook → issue GitHub → notificación Telegram. Página pública `/correcciones/` con el protocolo en lenguaje llano. Alerta legal apuntada: el estudio del titular (RT20/LG1) sigue abierto; cuando cierre, hereda el log existente sin migración. El protocolo de correcciones es el escudo legal real — demuestra buena fe y due process, más defendible que retrasar o privatizar.

- **Whitelist V1 antes del backfill** ([D3](DECISIONES.md)). 15-20 actores conocidos (Consell, Govern, IBAVI, ayuntamientos, partidos, sindicatos, patronales, tercer sector, colectivos) curados en `data/actor_domains.yml` antes del backfill. Refinamiento de dominios reales con los datos del propio backfill como calibración. Actor no reconocido durante backfill: el sistema lo anota como `whitelist_miss: true`, no bloquea publicación por sí solo, el repaso mensual IA propone ampliaciones.

- **Tests del auditor diferidos a RT5** ([D4](DECISIONES.md)). No montar `tests/` ni pytest solo para el auditor. La tarea de cobertura del pipeline (RT5) absorbe `audit.py` + `verify.py` + `balance.py` + `extract.py` + `rescue.py` en un solo bloque con fixtures reales del backfill. Validación durante construcción del auditor = corrida empírica sobre la semana W10 (2-8 marzo 2026).

- **Re-estudio del sistema de tiers en paralelo** ([D5](DECISIONES.md)). Opción (b) elegida. El auditor se construye con hueco reservado `tier: { value: null, reason: "pendiente estudio", signals: {...} }`; las señales se acumulan desde el día uno y cuando RT15 cierre, la función `compute_tier()` lee del bloque sin migrar logs antiguos. RT15 deja de bloquear el auditor y pasa a bloquear solo PI10 (visualización pública de tiers).

- **Marco de tres hitos grandes como frame de la Fase 1** ([D6](DECISIONES.md)). Hito 1: auditor MVP publicado con una edición real (activo). Hito 2: sistema de tiers cerrado e integrado (en paralelo). Hito 3: titular legal resuelto (en paralelo, bloquea empuje público). El editor decide puntos de entrada y de cierre de cada hito; Claude lleva los pequeños dentro y pide OK por bloque. Las 33 tareas restantes quedan en cola; no se abren en paralelo en la cabeza del editor.

- **Rastro de decisiones pequeñas + resumen al `/cierre`** ([D7](DECISIONES.md)). Decisiones autónomas de Claude dentro de un hito se anotan en el diario como línea corta (fecha, qué, por qué). Al cierre de sesión, resumen agrupado *"decisiones pequeñas de esta sesión"*. El editor deja correr, revierte o pide detalle.

**Memoria del asistente actualizada** (fuera del repo): `feedback_vigilancia_legal_activa.md` (alerta legal como conducta continua — Claude avisa en el mismo turno cualquier cambio que mueva exposición legal), `idea_version_premium.md` (hipótesis de monetización pendiente de validar si el producto alcanza calidad fiable, no proponer proactivamente), `nombre_proyecto.md` (cadena de dependencias `email ← nombre ← estructura final` añadida).

**Pendiente inmediato del Hito 1:**
- Diseño sobre papel del módulo `src/audit.py` (estructura de funciones, contratos de datos, orden de fases) — revisar antes de escribir código.
- Mockup estático de la página `/correcciones/` en el prototipo (mockup sin backend activo; el backend real espera al cierre del nombre y del estudio del titular).

---

## 2026-04-23 [docs] — Propagación del cierre del estudio del auditor a REVISION-FASE-0.5

Sincronización pendiente detectada por el editor: el cierre de [`ESTUDIO-COSTES-AUDITOR.md`](ESTUDIO-COSTES-AUDITOR.md) del 23-abr (tarde) actualizó el propio estudio y el DIARIO, pero no propagó las decisiones a los documentos vivos donde vivían como abiertas. Una sesión paralela abrió `REVISION-FASE-0.5.md`, leyó que RT2 seguía ⏳ y que la capa 5 del auditor aún listaba el muestreo del 10 %, y se atascó. Causa raíz: al hacer el commit `063dc50`, se trató el estudio como autocontenido cuando cerraba decisiones que tenían estado abierto en otros docs. El comando [`/cierre`](.claude/commands/cierre.md) existe precisamente para forzar este paso en el futuro; no estaba disponible cuando se hizo el commit anterior (se creó en `d532531`, posterior).

Cambios aplicados:

- **RT2 marcada cerrada** (`REVISION-FASE-0.5.md` §RT2 + tabla de seguimiento). Decisión: opción 2 (eliminar muestreo humano 10 %).
- **RT14 marcada cerrada** (`REVISION-FASE-0.5.md` §RT14 + tabla). Entregable: el propio `ESTUDIO-COSTES-AUDITOR.md`. Desbloquea PI9.
- **Decisión fundacional del auditor actualizada** en `REVISION-FASE-0.5.md` sección "2026-04-21 · Backfill de 12 semanas + Camino A + auditor IA": capa 5 sin muestreo + capa 5bis IA añadida + coste corregido con link al estudio.
- **Descripción del PI9 actualizada** en `REVISION-FASE-0.5.md`: 5 capas + 5bis, heurísticas con referencias a `actor_domains.yml`, panel de éxito en tres canales.
- **STATUS.md no se toca**: ya refleja el cierre en la línea del auditor de costes.

Regla aprendida (se apunta como memoria futura): al cerrar un estudio que resuelve decisiones, **buscar todos los docs vivos donde esas decisiones aparecen como abiertas y propagar** antes de commit. El comando `/cierre` cubre esto; aplicarlo desde ahora.

---

## 2026-04-23 [docs] — Tres reglas baratas de gestión documental + comando /cierre + estudio congelado

Conversación con el editor sobre la tarea roadmap *"Revisión profunda de arquitectura documental y gestión del conocimiento"*. Valoración: 20 docs en raíz, ~7.850 líneas, DIARIO 100 KB, triple registro de decisiones, STATUS desincronizado, sin contrato de arranque. Diagnóstico y plan completo congelados en [`ESTUDIO-GESTION-CONOCIMIENTO.md`](ESTUDIO-GESTION-CONOCIMIENTO.md) para revisar post-lanzamiento; no se ejecuta la reorganización completa ahora porque hay frentes abiertos (Revisión Fase 0.5, prototipo pausado) y churn documental arriesga merges sucios. Cambios aplicados hoy:

- **Regla 1 — DIARIO con fecha ISO + `[tema]`.** Cabecera obligatoria en entradas nuevas. Registrada arriba y en CLAUDE.md del proyecto.
- **Regla 2 — [`DECISIONES.md`](DECISIONES.md) fuente única.** Append-only, una fila por decisión con ID `D{N}`. Migración histórica de D1-D13 y DECISIONES-PENDIENTES queda para la revisión post-lanzamiento.
- **Regla 3 — STATUS.md ≤ 100 líneas.** Reducido de 181 a 58 líneas. Solo estado vigente; lo histórico se apoya en DIARIO/CLAUDE/PIVOTE.
- **Comando `/cierre`** en [`.claude/commands/cierre.md`](.claude/commands/cierre.md). Checklist fijo para cerrar sesiones sin perder pasos: inventario de cambios, auditoría cruzada de docs vivos, commits atómicos, push y reporte de qué se tocó y qué no.
- **Tarea post-lanzamiento añadida al ROADMAP** (Fase 7 "Diferido con criterio claro"): ejecutar la reorganización completa cuando el observatorio esté lanzado, 90 días evaluados y Revisión Fase 0.5 cerrada. Releer el estudio antes, porque parte estará obsoleta.
- **Decisión registrada:** [D0](DECISIONES.md).

---

## 2026-04-23 (tarde) — Cierre del estudio del auditor: capa 5bis delegada a IA, Telegram consolidado, reportes mensuales → trimestrales → semestrales

Segunda vuelta sobre [`ESTUDIO-COSTES-AUDITOR.md`](ESTUDIO-COSTES-AUDITOR.md) tras feedback del editor. Decisiones cerradas:

- **Muestreo humano del 10 % de auto-aprobadas: eliminado.** Contradecía la regla fundacional (editor opera, no audita). La red de seguridad la cubren capas 2-4 + heurísticas + log público + cuarentena pública + formulario externo.
- **Capa 5bis (repaso mensual de cuarentena) delegada a Opus.** Lee cuarentena + logs + whitelist + umbrales y devuelve diagnóstico narrativo + bloque YAML de ajustes propuestos. Nunca se aplica sin OK explícito del editor por Telegram. Coste ~0,4 €/mes. Tiempo editor: 5 min/mes (vs 30 min si lo hace a mano). Alternativa más alineada con *"el editor cuida la vía, no lee cada vagón"*. Riesgo de ciclo cerrado mitigado con (a) OK humano obligatorio antes de aplicar ajustes, (b) la auditoría Opus general sobre el corpus es independiente y detectaría desvíos sistémicos.
- **Alertas Telegram consolidadas en un solo parte del lunes.** Sin sobrealertar: si hay varias señales fuera de rango, van juntas. Si todo verde, silencio total. Excepción solo para alertas críticas (tope duro cruzado, pipeline roto), que siguen sueltas e inmediatas.
- **Reportes con cadencia escalonada + página `/reportes/`.** Mensuales los primeros 3 meses (may-jul 2026, calibración rápida), trimestrales desde el mes 4 (agosto 2026), semestrales desde el mes 7 (noviembre 2026) en adición. Envío por Telegram con headline + link; texto completo en `/reportes/YYYY-MM/`, `/reportes/YYYY-qN/`, `/reportes/YYYY-hN/` como archivos markdown permanentes.
- **Revisión de cadencias apuntada explícitamente:** al mes 4 se decide si el mensual se extiende, se fija permanente o se cierra. Al mes 7 se decide si el trimestral sigue, pasa a semestral puro o se combina. Criterio en ambos casos: valor informativo real, no costumbre.
- **Números actualizados** con la capa 5bis IA incluida: régimen estable desde mes 4 ≈ 2,4 €/mes. Meses 1-3 con auditoría Opus mensual de arranque ≈ 5,7 €/mes. Mes pico mayo 2026 (backfill + auditoría mensual + re-bench + capa 5bis) ≈ 10,1 €/mes — capa naranja, sin cruce de tope blando (12 €), lejísimos del duro (50 €).
- **Feedback del editor apuntado en memoria** (`feedback_esperar_ok_antes_de_editar.md`): en modo de intercambio de feedback sobre documentos, proponer → esperar OK → ejecutar. No aplicar ediciones al repo sin el "sí" del editor aunque la propuesta parezca obvia. Ocurrió en esta sesión; el editor lo corrigió y queda como regla.

Con esto el estudio del auditor queda cerrado. Siguiente paso del roadmap: construcción del módulo `src/audit.py` (semana 1 del plan — auditoría ciega con Sonnet + comparador determinista + tests con dataset W17).

---

## 2026-04-23 — Dos tareas nuevas añadidas al ROADMAP + ESTUDIO-COSTES-AUDITOR.md commiteado

- **Tarea: revisión profunda de arquitectura de archivos y gestión del conocimiento** — añadida como ítem 2 de la ruta crítica de Fase 1 (entre el estudio de costes del auditor y los tests básicos). Objetivo: que cada nueva conversación arranque con visión clara del proyecto; que un estudio completo al inicio de chat sea óptimo en tokens; que el feedback del editor y la gestión de tareas se acumulen y organicen de forma útil; optimizar consumo de tokens sin perder calidad ni detalle.
- **Tarea: resiliencia a cambios de modelo Anthropic** — añadida a Fase 3 junto al health check de fuentes. Cubre: detección de deprecaciones o versiones nuevas, alerta Telegram si un modelo activo desaparece, protocolo documentado para actualizar versión y re-ejecutar estudio de costes (RT14). Modelo: `models_health.py` espejo de `sources_health.py`.
- **`ESTUDIO-COSTES-AUDITOR.md` commiteado** — estaba sin trackear desde la sesión del 22-abr. Documento cerrado: auditor de 5 capas añade entre 0,08 € y 0,20 €/mes; backfill retroactivo 12 semanas ~5,4 € one-shot; cuello de botella real sigue siendo `generate` con Opus (~85 % del gasto por edición). Decisión: construir el auditor con las 5 capas completas sin recortes.

---

## 2026-04-22 (tarde · cierre) — Regla editorial: no expandir foco sin problema definido y demanda orgánica

- **Exploración del corpus W17 (19 noticias housing) para la palanca turismo** devolvió solapamiento muy alto vivienda-turismo (~75% de noticias housing tocan turismo directa o indirectamente, dominadas por el evento sa Joveria). El asistente propuso instrumentar preparatoriamente (extender schema con campos `tourism_connection`, `tourism_lever`, `tourism_actors` + tracking CSV). **Editor rechaza la propuesta.**
- **Razonamiento del editor:** en vivienda el problema está formulado con una frase clara (*"gente que trabaja en Ibiza no puede alojarse a precio digno"*). En turismo hay al menos seis formulaciones candidatas distintas (saturación, alquiler turístico, modelo monodependiente, destrucción de recursos, ocio descontrolado, ecotasa mal redistribuida), cada una con actores y palancas propias. Instrumentar sin problema formulado dispersa el foco editorial. El cuello de botella real es el tiempo de revisión de los lunes, no la capacidad técnica del pipeline.
- **Decisión:** no se instrumenta turismo. Centrarse en vivienda y escuchar si algo "grita naturalmente" (cita literal: *"de momento no es más que añadir diluir el foco, centrémonos en vivienda y si algo grita naturalmente ya lo oiremos como quien dice"*).
- **Regla editorial general derivada** (aplica a cualquier expansión del proyecto — temas, provincias, idiomas, secciones): no abrir un nuevo eje sin (a) formulación clara del problema, (b) demanda orgánica manifiesta en señales externas (búsquedas, emails, palancas que aparecen solas en el corpus, prensa que las pide). No por proactividad interna. Guardada en memoria como `feedback_esperar_demanda_organica.md`.
- **Documentación:** [`EXPANSION-TEMATICA.md`](EXPANSION-TEMATICA.md) actualizado con sección 8 que recoge las seis formulaciones candidatas, la decisión del editor y la regla. Las secciones 1-7 pasan a ser referencia histórica del análisis; la parte viva es el bloque 8.
- **Feedback adicional del editor apuntado a memoria** (`feedback_referencias_con_contexto.md`): no mencionar identificadores internos del proyecto (`RT23`, `PI9`, `D11`, `W17`, etc.) sin glosar qué son la primera vez en cada respuesta o documento introductorio. Rompe el flujo de lectura y obliga a ir a buscar. Siglas del dominio público (BOIB, IBAVI, GEN-GOB, CCOO, PIMEEF...) sí son válidas sin glosar.

---

## 2026-04-22 (tarde) — Hipótesis de escalabilidad provincial y de expansión temática documentadas

- **Posibilidad de replicar el modelo a otras provincias**: discutida y documentada en [`ROADMAP.md`](ROADMAP.md) como "Hipótesis post-tracción — Escalabilidad provincial". Condicionada a tracción demostrada en Ibiza (framework RT23 a 90 días). Arquitectura prevista: monorepo motor + `config/<provincia>.yaml` + repos de output por provincia con GitHub Pages propio. La lógica temporal específica de Ibiza (temporada/pre-temporada por ciclo de clubs) queda en su yaml y no contamina el motor común. URLs con fechas ISO son el eje universal, compatible con cualquier geografía. No hay decisión técnica que tomar ahora; queda documentado para cuando haya tracción (Q3 2026 como pronto).

- **Posibilidad de expandir a otros temas "hermanos" de vivienda en Ibiza**: estudio profundo documentado en [`EXPANSION-TEMATICA.md`](EXPANSION-TEMATICA.md) y resumido en [`ROADMAP.md`](ROADMAP.md) como "Hipótesis post-tracción — Expansión temática en Ibiza". Misma condición de activación que la escalabilidad provincial (RT23 verde). Evaluados 10+ temas en tres tiers: Tier 1 (turismo, agua, movilidad) con encaje casi directo; Tier 2 (trabajo de temporada, medio ambiente, residuos) con adaptación; Tier 3 (sanidad, educación, energía, patrimonio, seguridad, gobernanza) descartados como verticales y reservados como palancas transversales. Recomendación de orden: primero palancas dentro del radar actual (Modelo C híbrido, coste marginal ~0,5 €/mes), graduar a vertical propio solo si la palanca demuestra demanda. Primer candidato: turismo. Interacción clave con escalabilidad provincial: misma arquitectura técnica (motor + config por instancia); el orden sensato es primero turismo en Ibiza (misma geografía, distinto tema) y luego provincias (mismo tema, distinta geografía). Decisión editorial honesta apuntada: el cuello de botella no es técnico sino de tiempo del editor para revisar múltiples lunes.

---

## 2026-04-22 (mañana) — Claude Design archivado, decisiones de Fase 1-2 + retirada de "pivote" como término activo

**Respuestas del editor a las 3 preguntas abiertas del roadmap V2:**

- **Claude Design recibido y archivado** en [`private/claude-design-experiment/`](private/claude-design-experiment/). El editor lo envió como ZIP (`Ibiza vivienda.zip`, 58 KB) con HTML + JSX + CSS + data.js + prompt. Advertencia explícita: es un experimento con datos antiguos (pre-modelo documental), no tiene en cuenta ninguna de las decisiones D1-D13 ni las 5 reglas duras, **no es referencia de nada** hasta que el editor lo indique. Se estudia únicamente en la fase de Diseño (Fase 4 del roadmap V2). README propio dentro de la carpeta explicando estas condiciones. Tarea RT16 actualizada a "🔄 archivado, no es referencia".
- **Trilingüe desde el backfill.** Las 12 ediciones retroactivas salen en ES/CA/EN desde el relanzamiento. Coste puntual +3-4 € absorbido por el tope duro de 50 €. Consistencia de corpus desde el día 1. Tarea RT18 actualizada.
- **Termómetro de precios — nombre provisional.** El módulo de precios lleva ese nombre de momento, con nota explícita de revisión cuando el proyecto esté más asentado. Alternativas en reserva: Observatorio de precios, Radar de precios, Precios vivienda Ibiza. Tarea RT21 actualizada.

**BOIB watcher — Fase 2 confirmado.** El editor prioriza tener la base legal presente desde el relanzamiento como diferencial claro frente al "refrito de prensa". Se mantiene el estudio de factibilidad técnica previo de 2-4 horas (robots.txt, falsos positivos, scraping vs filtro Google News) como primera tarea dentro de Fase 2. Tarea RT22 confirmada.

**Framework de señales de tracción a 90 días (RT23) aprobado** como mecanismo para decidir si el proyecto escala, se replantea o se mantiene como experimental. Se evaluará 90 días tras el relanzamiento.

**Retirada del término "pivote" como adjetivo activo del proyecto.** A petición del editor 2026-04-22. Cambios:

- El término "pivote" se reserva para describir el **evento histórico** del 2026-04-20 (cambio de modelo). No se usa como adjetivo del proyecto vigente.
- El proyecto se refiere a sí mismo como **"observatorio documental"** o por su nombre (`radar))ibiza_vivienda`).
- Documentos activos actualizados: [CLAUDE.md](CLAUDE.md), [README.md](README.md), [STATUS.md](STATUS.md), [ROADMAP.md](ROADMAP.md), [ARQUITECTURA.md](ARQUITECTURA.md), [SEO.md](SEO.md), [DISENO-WEB.md](DISENO-WEB.md), [ESTUDIO-DISENO.md](ESTUDIO-DISENO.md), [CONTENIDO-RETROACTIVO.md](CONTENIDO-RETROACTIVO.md), [ESTUDIOS-PENDIENTES.md](ESTUDIOS-PENDIENTES.md), [ESTUDIO-3-MODELOS.md](ESTUDIO-3-MODELOS.md), [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md).
- Documentos históricos intactos: entradas previas del DIARIO (registran el evento en su momento), [DECISIONES-PENDIENTES.md](DECISIONES-PENDIENTES.md) (acta del momento), logs privados.
- [PIVOTE.md](PIVOTE.md) conserva el nombre de archivo (rompería enlaces renombrarlo) pero lleva nota de cabecera explicando que el término es histórico.
- Identificador interno `model: "pivote-documental-v1"` renombrado a `model: "documental-v1"` en `src/generate.py` (SYSTEM + frontmatter mínimo + edición vacía) y en la W17 ya publicada. Identificador técnico, no visible al público.

---

## 2026-04-21 (noche · roadmap V2 y decisiones fundacionales) — 7 fases, 12 tareas nuevas, nombre cerrado, regla complementaria

Cierre de sesión larga de revisión técnica y estratégica. El editor pide crear el mejor roadmap posible con las tareas nuevas de la revisión + las originales del bloque fundacional. Responde a las 7 preguntas de Claude con decisiones y plantea meta-preguntas que obligan a repensar el proyecto.

**Respuesta honesta de Claude sobre el potencial del proyecto:**
- Hoy es "ordenar noticias con método". Sin datos propios + tracker de evolución + distribución relacional, se queda en herramienta útil pero no referente.
- Tres palancas que elevan: observatorio de precios (Vía A + Vía B), tracker de propuestas con estados públicos, lista curada de 20-30 contactos que reciben edición directa.
- Framework de señales de tracción a 90 días post-relanzamiento decide si se escala o se mantiene como side-project experimental. Verde/amarillo/rojo con 6 métricas medibles.
- Escenario B (rodaje privado 1 año) es legítimo y barato (84 € en API + tiempo voluntario). Se mantiene como opción si al terminar Fase 6 el estado no está maduro.

**Decisiones cerradas hoy:**

- **Nombre del wordmark: `radar))ibiza_vivienda`** (formato `lugar_tema`). Actualizado en [CLAUDE.md](CLAUDE.md), [STATUS.md](STATUS.md), [ESTUDIO-DISENO.md](ESTUDIO-DISENO.md), [docs/acerca.md](docs/acerca.md). ID1 cerrada. Prototipo HTML pendiente de actualización cuando se retome Diseño (coordinado con RT16 Claude Design).
- **Regla complementaria a las 5 duras del pivote:** automatización máxima + niveles de veracidad públicos. El editor opera, no audita. El sistema se audita a sí mismo (auditor IA + tiers + cuarentena + log abierto). Añadida a [PIVOTE.md](PIVOTE.md) como regla complementaria.
- **Rol del editor:** opción B (sin muestreo humano del 10%) durante rodaje + opción C (revisor externo pagado) cuando haya tracción.
- **Trilingüe ES/CA/EN activo antes del SEO:** sube de "diferido" a Fase 4 de la nueva estructura. Web multilingüe desde el lanzamiento.
- **Escenarios de lanzamiento:** A soft launch mayo-junio, B rodaje 1 año. La naturalidad decide al terminar Fase 6.

**12 tareas nuevas añadidas al inicio de [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md) (P-1):**

- RT13 — Regla fundacional: automatización + veracidad pública (✅ documentada en PIVOTE).
- RT14 — Estudio preciso de costes del auditor IA (backfill + mantenimiento). Bloquea PI9.
- RT15 — Re-estudio profundo del sistema de tiers. Antes de implementar PI10.
- RT16 — Propuesta visual de Claude Design incorporada al estudio de diseño. Requiere archivos del editor.
- RT17 — Navegación exhaustiva mobile-first con sitemap visual siempre accesible. Documento `NAVEGACION.md` propio.
- RT18 — Trilingüe ES/CA/EN activado en Fase 4 antes del SEO.
- RT19 — Seguimiento visual de evolución de problemáticas y soluciones. Diferencial editorial.
- RT20 — Estudio titular legal con detenimiento. Bloquea empuje público.
- RT21 — Vía A precios: nombre público ("Observatorio de precios") y presupuesto operativo.
- RT22 — BOIB watcher: decisión de ubicación Fase 2 vs Fase 3 con estudio de factibilidad previo.
- RT23 — Framework de señales de tracción a 90 días post-lanzamiento.
- RT24 — Escenarios de lanzamiento A (soft mayo-junio) y B (rodaje 1 año).

**Nuevo Roadmap V2 en 7 fases ejecutables** añadido al inicio de [ROADMAP.md](ROADMAP.md). La estructura original de Bloques A-I queda como anexo histórico para referencia. Duración estimada 9-12 semanas a ritmo 15 h/semana. Fases: (1) Cimientos firmes, (2) Backfill + fuentes primarias, (3) Afinado ingesta, (4) Web completa + trilingüe, (5) SEO + distribución, (6) Pre-empuje, (7) Empuje público + medición 90 días.

**Pendiente de confirmación del editor:**
- Archivos / screenshots de la propuesta visual de Claude Design (RT16).
- Decisión operativa: activar trilingüe desde el backfill (corpus consistente) o solo desde empuje público (ahorra unos euros puntuales).
- Decisión final BOIB: subir a Fase 2 o mantener en Fase 3, tras estudio de factibilidad.

---

## 2026-04-21 (post-revisión · decisiones del editor) — /acerca/ reescrita + 2 tareas nuevas (RT11 home, RT12 precios)

- **`docs/acerca.md` reescrita** (opción A, breve ~250 palabras). Qué es el observatorio + quién lo edita + licencias + financiación + contacto + avisos. El detalle técnico (reglas duras, pipeline, modelos, sesgos) se delega a la futura `/metodo/`. Copy sin prometer nada que no tenga ya; banner de "página en reescritura" retirado.
- **RT11 — Copy y tono de la home.** Añadida como tarea P-1 para resolver en la etapa de Diseño. El fix mecánico del barrido ya limpia el copy del modelo antiguo; la decisión editorial final (tono, jerarquía, integración con tiers, UX dual) se toma cuando se reanude el bloque de diseño, tras cerrar RT1-RT10.
- **RT12 — Vía A de precios, estudio en profundidad.** Añadida como tarea P-1 prioridad ALTA. Objetivo: valorar si adelantar al pre-relanzamiento la agregación mensual de informes públicos (Idealista, Fotocasa, INE, IBESTAT, Ministerio de Vivienda, BOIB). Coste 0 €, sin riesgo legal, convierte el proyecto de "lectura estructurada de prensa" a "observatorio con datos primarios". Salida: `ESTUDIO-PRECIOS.md` con matriz de fuentes + esquema normalizado + recomendación de cronograma.
- **Método queda en RT8** como estaba: stubs + split `/acerca/` + `/metodo/` cuando se retome Diseño, basado en el prototipo `docs/prototype/metodo.html` ya construido.

---

## 2026-04-21 (cierre · revisión técnica profunda y fixes de coherencia) — Borrado de W16 + fixes pipeline + 10 tareas nuevas

Revisión crítica solicitada por el editor sobre concepto y proceso. Detectadas 19 inconsistencias de distinta gravedad entre documentación, código y web pública. Ejecutados los fixes inequívocos y apuntadas como tareas las decisiones que requieren criterio editorial.

**Fixes aplicados en este commit:**

- **W16 antigua borrada** ([`docs/_editions/2026-w16.md`](docs/_editions/2026-w16.md)). Era modelo antiguo, con propuestas firmadas por el observatorio ("Censo-a-contrato en 90 días", "Residencias modulares") y precedentes detectados como probablemente alucinados en el [estudio crítico del 20-abril](private/estudios/2026-04-20-propuestas.md). La W17 se conserva: es del modelo documental y el único ejemplo público limpio del pivote. Histórico git mantiene la W16 para auditoría.
- **`proposals_history.json` regenerado** desde `extracted.json` vigente. El histórico tenía (a) bug "Marí = actor_type `otro`" heredado de una ejecución vieja cuando el extractor era menos estricto, (b) entrada duplicada de la coalición "Consell + patronales + sindicatos" (una con nombre corto, otra con nombre largo — dedup por actor literal no la capturó). Quedan 3 entradas correctas con IDs 001-003.
- **Temperature fijada en `generate.py`** a 0,2. La regla 2 del pivote ("el observatorio no genera propuestas propias") exige cero inferencia; el modelo corría con temperature default (≈1,0), lo que dejaba margen para alucinación. Una línea de fix, impacto directo en calidad.
- **Check bloqueante en `verify.py`**: propuesta sin actor en `extracted.json` bloquea la publicación. Extract ya lo prohíbe en su prompt, pero verify ahora lo atrapa como red de seguridad.
- **Alerta de `balance.py` silenciada hasta N≥20 propuestas**. Con el histórico actual (3 propuestas) cualquier bloque supera el 50% por artefacto estadístico. Parche temporal; el rediseño completo (comparación de trimestres consecutivos, como dicta la regla 4) se hace cuando haya 3 meses de datos reales (ver RT6 en la revisión fundacional). La página pública `/balance/` muestra ahora un bloque "Fase de rodaje" hasta alcanzar el umbral.
- **Schema de `classify.py` alineado en [`ARQUITECTURA.md`](ARQUITECTURA.md)**. La doc decía `has_explicit_proposal: bool`; el código devuelve `proposal_type: formal|en_movimiento|ninguna`. Actualizado el doc, no el código (el código está bien).
- **Topes y costes unificados en todos los docs**: blando 12 €, duro **50 €** (antes mezcla de 8/12/20 en distintos sitios), coste proyectado ~6-7 €/mes con nota "revisable tras 3 meses de datos reales". Sitios tocados: [README](README.md), [CLAUDE](CLAUDE.md), [STATUS](STATUS.md), [docs/acerca](docs/acerca.md). PLAN.md queda como documento histórico con los números originales.
- **`build_index.py` adaptado al schema documental**. El regenerador de la home buscaba campos del modelo antiguo (`Actor responsable`, `Precedente`, `Coste`, `Primer paso`, `Por qué ahora`) → cards vacíos. Ahora busca los campos reales (`Actor que la propone`, `Estado`, `Horizonte`, `Actor que tendría que ejecutarla`). Copy reescrito: *"propuestas accionables con precedente"* → *"propuestas documentadas en circulación"*. Eliminado el copy "observatorio automatizado con propuestas con actor, coste y primer paso" → *"observatorio documental, no genera propuestas propias"*. `docs/index.md` regenerado.
- **docs/balance.md regenerado** con el fix de silencio + bloque "Fase de rodaje".

**10 tareas nuevas añadidas al inicio de [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md) como categoría P-1** (antes del resto):

- RT1 — Backfill empírico: ejecutar 1 semana antigua (W10) como prueba antes de comprometer 12.
- RT2 — Resolver contradicción editor operador vs muestreo 10%.
- RT3 — Validar tiers UX con los dos públicos (periodista + temporero).
- RT4 — Techo de cobertura + banner de fase de rodaje + adelantar Vía A de precios si es posible.
- RT5 — Tests básicos del pipeline (no hay `tests/`).
- RT6 — Balance: rediseño completo con persistencia tras 3 meses de datos.
- RT7 — `build_index.py` al schema documental (✅ cerrada en este commit).
- RT8 — Split `/acerca/` + `/metodo/` (basado en prototipo `metodo.html`).
- RT9 — Stubs de las 3 páginas que las reglas duras exigen: política editorial, metodología, correcciones.
- RT10 — LG1 + LG2 promovidas a prioridad alta: anonimato legal resuelto antes del empuje público.

**Pendiente del mismo barrido (no en este commit, requiere confirmación):**

- Borrador de reescritura conceptual de la home (el copy actual generado por `build_index.py` es mejor que el de ayer, pero el editor pidió ver draft antes de aplicar cambios conceptuales mayores).
- Borrador de reescritura de `/acerca/` para apuntarlo al modelo documental o dividirla en `/acerca/` (corta) + `/metodo/` (detalle técnico, basado en el prototipo `docs/prototype/metodo.html`).
- Propuesta concreta de Vía A (observatorio de precios por agregación oficial) como posible adelanto a Fase 0.

---

## 2026-04-21 (cierre · barrido documental post-merge) — Eliminadas referencias al branch del pivote

- **Merge del pivote consolidado 2026-04-21 12:04 CEST** (commit `b24a6ad`) pero la documentación seguía describiendo el pivote como trabajo vivo en branch separado. Barrido en 7 documentos para que el repo diga la verdad.
- **Archivos actualizados:** [CLAUDE.md](CLAUDE.md) (callout de cabecera reescrito + estructura de `src/` y `data/` al día con `extract.py`/`verify.py`/`rescue.py`/`balance.py`/`self_review.py`/`archive.py`), [README.md](README.md) (aviso de pivote + sección "Qué hace" con los pasos reales del pipeline documental + aviso final simplificado), [STATUS.md](STATUS.md) (callout "PIVOTE EN MARCHA" → "MODELO DOCUMENTAL ACTIVO" + eliminado "TL;DR del modelo antiguo"), [PIVOTE.md](PIVOTE.md) (cabecera + sección Reversibilidad adaptadas a merge consolidado), [PLAN.md](PLAN.md) (aviso pivote → documento histórico), [CONTENIDO-RETROACTIVO.md](CONTENIDO-RETROACTIVO.md) y [DECISIONES-PENDIENTES.md](DECISIONES-PENDIENTES.md) (frases "pre-merge" contextualizadas con fecha), [ARQUITECTURA.md](ARQUITECTURA.md) (sección "Migración desde el código actual" aclara dónde vive el modelo antiguo).
- **Tabla de seguimiento del ROADMAP arreglada:** A1-A7, A9-A12, A16 marcadas ✅ (cerradas tras merge). A8 (tests) sigue pendiente — no hay carpeta `tests/`. A13, A14, A17 ⏸ diferidos. A15 (dashboard costes ampliado) pendiente. Se añadió PI2-A (archivado append-only) al listado como cerrada 21-abr.
- **Qué NO se tocó:** entradas históricas del DIARIO que mencionan el branch (son registro de lo que pasó en su momento, no se reescribe). `docs/acerca.md` sigue con su callout *"esta página refleja el modelo antiguo"* porque su reescritura es tarea pendiente del Bloque B, no un error de actualización.
- **Impacto:** cero código tocado. Documentación ahora coherente con la realidad del repo. Cualquier Claude que abra una sesión nueva lee un callout de cabecera que dice la verdad (modelo documental único, activo en `main`).

---

## 2026-04-21 (noche · Fase 0.5 cierre de sesión) — Rol operador + tiers públicos + alerta lunes

- **Rol del editor redefinido como operador, no revisor experto.** El editor expresa: *"en principio yo no voy a revisar nada"*. Tras diálogo honesto sobre qué absorbe el sistema y qué no, queda claro el mínimo no delegable: responder emails de `/contacto/` en 48-72 h (0-3/semana), mirar la web los lunes 3 min tras publicar, escalar cuando llegue algo excepcional. Total estimado 15-45 min/semana reactivos. El conocimiento experto del tema NO es requisito para sostener el proyecto — el sistema (tiers + cuarentena + sanity check externo pre-lanzamiento) absorbe la validación.
- **Modo entrenamiento de 4 semanas (ED5) descartado** por incompatible con el rol real del editor. Reemplazado por tres mecanismos complementarios:
  - **Plan A aprobado · Tiers de confianza públicos:** cada propuesta lleva badge 🟢/🟡/🟠 visible. 🔴 va a cuarentena. Criterios ajustables, explicados al público en lenguaje llano.
  - **Plan B aprobado · Cuarentena pública `/revision-pendiente/`:** las propuestas que no pasan el corte no se esconden, se publican con aviso de que esperan corroboración o verificación comunitaria. A 60 días sin confirmar se archivan como "no verificada". Alineado con filosofía de radical transparency.
  - **Plan C aprobado · Editor = operador.** Cero obligación de revisar propuestas. Solo operación reactiva.
- **Alerta Telegram del lunes mezcla A+C.** `src/report.py` enriquecido: emisión de título + URL pública + conteo de propuestas + lista de actores (cap 6) + pipeline OK/coste + bloque condicional `⚠ Atención` que solo aparece si hay cuarentena activa o alerta de balance. Se alimenta de `data/balance_status.json` y `data/quarantine.json` — invisible hasta que los módulos upstream existan. Horario 07:15 Madrid. Canal Telegram. Email anotado como tarea futura.
- **Cinco reglas permanentes fijadas por el editor y registradas en la cabecera de [REVISION-FASE-0.5.md](REVISION-FASE-0.5.md):**
  1. Vigilar barreras pasadas de rosca — no sobrediseñar.
  2. Badges y decisiones públicas explicados en lenguaje llano + ajustables.
  3. Preguntar antes de commit cuando no haya validación explícita previa.
  4. Códigos internos fuera de la conversación (son solo para el documento).
  5. Rol del editor = operador, no revisor experto.
- **Verbatim match diferenciado por tipo de cita** registrado como criterio del auditor: `statement_type=quote` exige substring literal en HTML; `statement_type=reported` relaja a nombre del actor + términos clave + sin contradicción lógica. El editor frenó la versión estricta anterior (*"¿lo que me propones tiene sentido o estamos haciendo demasiado estricta la selección?"*) y el ajuste queda como aplicación directa de la regla permanente 1.
- **Meta-feedback del editor sobre velocidad del trabajo:** *"has ido muy rápido esta vez publicando cambios. si me notas perdido debes preguntarme antes"*. Asumido como regla permanente 3.
- **Tareas nuevas añadidas a Fase 0.5:** PI10 (tiers), PI11 (cuarentena), PI12 (alerta lunes — parcialmente implementado hoy), PI13 (email futuro), EX5 (sanity check externo 50-100 €). ED5 marcada como ❌.

---

## 2026-04-21 (noche · Fase 0.5 continuación) — PI2-A archivado append-only + ajustes auditor + tope 50 €

- **PI2-A cerrada:** nuevo módulo [`src/archive.py`](src/archive.py) con `snapshot_to_archive()` que copia `ingested/classified/extracted/rescue/verification_report.json` a `data/archive/YYYY-WNN/` + `snapshot_meta.json` (timestamp, slug, gasto del mes hasta ese momento). Integrado en [`src/report.py`](src/report.py) tras `append_to_history()` — no bloqueante si falla. Primera snapshot ejecutada: `data/archive/2026-W17/` con los 5 archivos de esta semana. A partir de ahora no se pierde materia prima nunca más.
- **Tope duro mensual subido a 50 €** (antes 20 €) en [`src/costs.py`](src/costs.py) v3. Motivo: absorber backfill 12 semanas + auditor IA 5 capas + experimentación sin bloqueos. Blando se mantiene en 12 €.
- **Verbatim match diferenciado por `statement_type`**: si la propuesta contiene cita entrecomillada (`quote`) exigimos substring match literal; si es paráfrasis del periodista (`reported`) se relaja a nombre del actor + términos clave + sin contradicción lógica. El criterio original habría rechazado propuestas legítimas en estilo indirecto — pillado por el editor.
- **Elección entre dos fuentes sobre la misma propuesta**: jerarquía determinística (URL del actor > diario local con cita > más antigua). Se guarda una `url_source` principal + lista `url_corroboration`; las otras fuentes no se ocultan, se muestran como *"también cubierto por:"*.
- **Tres salvaguardas nuevas ante preocupación del editor sobre su propia competencia para auditar**:
  - **ED5 (nueva) · Modo entrenamiento 4 semanas:** tras relanzamiento, todas las propuestas pasan por el editor con resumen corto + veredicto IA. Se calibran mutuamente antes de activar auto-aprobación.
  - **EX5 (nueva) · Sanity check externo pre-lanzamiento:** pagar 1-2 h a periodista local o académico UIB para auditar 30 propuestas del backfill (50-100 €). Escudo de validación independiente.
  - **Refuerzo de OP1:** correcciones visibles son la regla 5 en acción, no fracaso. Observatorio sin correcciones = observatorio que miente.

---

## 2026-04-21 (noche · revisión Fase 0.5) — Backfill 12 semanas + auditor IA + Camino A

- **Abierta Fase 0.5 de revisión crítica** ([REVISION-FASE-0.5.md](REVISION-FASE-0.5.md)) tras detectar el editor que necesita entender el concepto con más profundidad antes de entrar en diseño visual. 34 tareas organizadas en 6 categorías (P0 método/fuentes, P1 estructural, P2 UX, P3 operacional, P4 identidad/legal/financiación, P5 misc). Trabajo a una tarea por vez.
- **Primera tarea (ED1, criterios de admisión de propuestas) desvió a infraestructura** al constatar que `ingested.json` / `classified.json` se sobreescriben (diseño temporal heredado del modelo antiguo) y solo hay corpus de 10 días. No hay material histórico para validar criterios con datos reales. El editor pide solución de raíz: 3 meses de backfill para cimientos sólidos.
- **Decisión fundacional — backfill retroactivo de 12 semanas (W06→W17, ~2 feb → 20 abr)**. Script `src/backfill.py` one-shot que recorre Google News con operadores temporales + buscadores nativos + BOIB si factible. Salida a `data/archive/YYYY-wWW/`. Alimenta simultáneamente el archivo público de ediciones, la base de datos de propuestas, actores, balance con 3 meses reales, grafo de evolución (PI3) y omisiones retroactivas.
- **Camino A confirmado para publicación retroactiva** (frente a B corpus privado o C pieza única): las 12 ediciones salen con fecha real + banner *"procesada a posteriori bajo modelo documental"*. Razonamiento del editor: tomar información del pasado no pierde legitimidad, construye pre-temporada, ofrece contexto al público, es defendible al 100%. La tensión legal por cambios de posición de actores queda mitigada por el schema de evolución (state + proposals_history append-only + PI3 grafo visible).
- **Sistema de auditoría IA de 5 capas (PI9, nueva)** sustituye la revisión humana exhaustiva: (1) Haiku extrae, (2) Sonnet audita ciego, (3) comparador determinístico Python + verify.py 5-checks, (4) Opus arbitra discrepancias (~15%), (5) editor revisa solo flagged + muestreo 10%. Reduce tiempo editor de ~15 h a ~4 h sin sacrificar calidad (dos modelos independientes detectan más errores que uno). Heurísticas sin IA: cross-source confirmation, verbatim substring match, domain-actor whitelist, viability sanity.
- **Log de auditoría radical** en `data/audit/YYYY-wWW/{proposal_id}.json` con output literal de cada capa + timestamps + decisión final. Trazabilidad completa como escudo legal. 10 KB por propuesta.
- **Coste cerrado:** ~3,50 € totales (backfill ~0,50 € + auditor sobre 12 semanas ~2,70 € + pieza retroactiva Opus ~0,30 €). Dentro del tope blando mensual (12 €) con amplio margen.
- **Orden de ejecución reordenado:** PI2-A (append-only inmediato) → PI2-B (backfill) → PI9 (auditor) → ED1 (criterios validados con corpus real) → resto P0/P1. ED1 ya no se cierra en abstracto, se cierra con evidencia empírica de ~150 propuestas reales.
- **[CONTENIDO-RETROACTIVO.md](CONTENIDO-RETROACTIVO.md) ampliado de 8 a 12 ediciones** (W06-W17 en vez de W10-W17). Arco narrativo extendido: *"del cierre de temporada 2025 al desalojo de los asentamientos en vísperas de temporada 2026"*.

---

## 2026-04-21 (tarde · publicación) — Prototipo visitable en GitHub Pages

- **Prototipo movido de `prototype/` → [`docs/prototype/`](docs/prototype/)** para que GitHub Pages lo sirva sin arrancar servidor local. Motivo: el editor pide poder revisarlo en cualquier momento (incluidas las 2 preguntas abiertas que requieren iPhone real). Pages solo publica desde `/` o `/docs` en plan gratuito → mover es la vía de coste 0.
- **URLs públicas** (con `<meta name="robots" content="noindex,nofollow">` para no aparecer en Google): [home](https://otundra.github.io/ibiza-housing-radar/prototype/home.html) · [edition](https://otundra.github.io/ibiza-housing-radar/prototype/edition.html) · [actor](https://otundra.github.io/ibiza-housing-radar/prototype/actor.html) · [proposal](https://otundra.github.io/ibiza-housing-radar/prototype/proposal.html) · [preview logo](https://otundra.github.io/ibiza-housing-radar/prototype/logo/preview.html). Las 5 verificadas 200 tras el deploy.
- **Jekyll copia los HTML tal cual** porque no tienen front matter YAML — los trata como archivos estáticos. Sin interferencia con el sitio Jekyll principal.
- **Añadido `noindex,nofollow`** al `preview.html` del logo, que no lo tenía. El resto del prototipo ya lo llevaba desde la entrega original.
- **`launch.json` actualizado** al nuevo path. El preview local sigue operativo en `127.0.0.1:4100` con `preview_start("prototype")`.
- **Referencias actualizadas** `prototype/` → `docs/prototype/` en 5 docs del repo (CLAUDE, STATUS, DIARIO, ROADMAP, ESTUDIO) y 3 archivos de memoria.
- **Conversación pendiente sobre publicar el resto de páginas del Bloque B.** El editor preguntó cómo abordar las ~20 páginas restantes del ROADMAP (política editorial, metodología, balance, radar, actores, propuestas, correcciones, glosario, estado, sistema, sin-dato, auditoría, costes, etc.). Propuse tres niveles: (T1) shells navegables de 2-3 h, (T2) estructura real con placeholders 1-2 d, (T3) completas con datos tras Bloque C. El editor deja la decisión en espera — ningún nivel arrancado.

---

## 2026-04-21 (tarde · pausa) — Prototipo HTML Paso 1 entregado y pausado

- **Paso 1 del plan de prototipo del estudio (§10) completado y verificado** — 4 HTMLs estáticos en [`docs/prototype/`](docs/prototype/) + CSS + JS vanilla. Datos reales de la edición del 20-26 abril 2026 (W17 interno). Entregables: [`styles.css`](docs/prototype/styles.css) con tokens del §5 y 9 componentes del §6; [`theme.js`](docs/prototype/theme.js) con toggle tema ○/● y `localStorage` (`rvi-theme`), fab Escríbenos con Escape, auto-captura de URL origen, scroll-spy sidebar; [`home.html`](docs/prototype/home.html) dashboard editorial; [`edition.html`](docs/prototype/edition.html) con 7 secciones + margin notes Tufte + tabla mapa; [`actor.html`](docs/prototype/actor.html) Consell d'Eivissa con sidebar sticky + horizon toggle sin JS + timeline; [`proposal.html`](docs/prototype/proposal.html) Residencias temporeros con pill "en debate" + barra progreso 8 estados + ficha 13 campos + 6 chips coalición.
- **Verificado en navegador** con servidor estático en `127.0.0.1:4100`: consola limpia en las 4 páginas, toggle tema persiste entre navegaciones, sidebar sticky activa ≥900 px, horizon toggle sin JS (CSS `:checked ~`), progress bar respeta `prefers-reduced-motion`. A11y spot-checks: 1 H1 por página, `lang=es`, skip-link, landmarks completos, radios con `<label for>`, tabla con `<caption>` + `th scope`, 0 inputs sin label. Responsive OK en 375/768/1280 px. Lighthouse completo pendiente (herramienta no disponible en el entorno de verificación).
- **Pausa activa desde 2026-04-21 tarde.** El editor pide parar el tema diseño/frontend para estudiar primero la arquitectura antes de seguir. B34 queda **en revisión (no cerrado)** — el prototipo está entregado pero pendiente de visto bueno visual y de 3 preguntas abiertas: (1) lectura del wordmark V2 Split a 17 px en cabecera real, (2) comportamiento de 6 chips coalición en mobile real, (3) si la barra de progreso muestra siempre los 8 estados o solo los aplicables.
- **Fix técnico: launch.json usa `/opt/homebrew/bin/python3`** en vez de `/usr/bin/python3` para la config `prototype`. El python de Xcode está sandboxed y bloquea `os.getcwd()` (argparse lo llama al importar `http.server`). Sin este cambio, el servidor arranca pero da 500 en cada request.
- **Memoria nueva** [`prototipo_paso1_en_pausa.md`](../../.claude/projects/-Users-raulserrano-Documents-GitHub-ibiza-housing-radar/memory/prototipo_paso1_en_pausa.md) — consolida estado del prototipo, cómo retomar el preview, checks superados, preguntas abiertas. Enlazada desde MEMORY.md.
- **Cómo retomar:** leer la memoria anterior + §10 Paso 1 del estudio; arrancar preview con `preview_start("prototype")`; responder a las 3 preguntas; decidir si el estudio de arquitectura modifica algo antes de pasar al Paso 2 (Jekyll, tarea B35).

---

## 2026-04-21 (cierre identidad) — Variante V2 Split elegida + favicon `))` vectorial

- **D1 cerrado con V2 Split:** wordmark `radar))vivienda_ibiza` en JetBrains Mono con las `))` en terracota (`#c14a2d`) como único acento cromático, resto en tinta. La variante más sobria con economía radical de color: un solo elemento colorado, el resto monocromo.
- **D2 cerrado con favicon `))` vectorial** (glifo puro). Las dos `))` del wordmark aisladas como favicon — máxima coherencia: el elemento cromático del wordmark es la firma en pestañas y avatares. Archivo [`docs/prototype/logo/favicon.svg`](docs/prototype/logo/favicon.svg), dos paths Bezier cuadráticos, stroke-linecap round, stroke-width 2.4, color terracota. Escala limpio de 16 px a 512 px sin pérdida. No depende de carga de fuente.
- **Paquete completo de marca resuelto:** nombre + wordmark + favicon forman sistema tipográfico homogéneo sin necesidad de logo gráfico. Coherente con dirección "mono + seams".
- **Formatos pendientes de generar** (derivables del SVG en Paso 1 del prototipo): favicon-32.png, favicon-192.png (Android), apple-touch-icon.png (180×180 iOS), og-fallback.png (1200×630).

---

## 2026-04-21 (tarde) — Ajuste de nombre provisional y logo tipográfico

- **Nombre provisional actualizado:** "Radar Ibiza" pasa a "**Radar Vivienda Ibiza**" (provisional). Formato: minúsculas, descriptivo, deja la palabra "vivienda" explícita por claridad y SEO; marca explícitamente como provisional para reevaluar antes del relanzamiento. Dominio candidato `radaribiza.com` se mantiene de momento.
- **Logo gráfico descartado.** Las 3 direcciones SVG exploradas en docs/prototype/logo/ (punto limpio + arcos, "I" italic + arcos, "I" + arcos asimétricos) fueron valoradas como "muy feas" por el editor y quedan desechadas. La identidad se resuelve **enteramente con tipografía** — sin monograma gráfico separable.
- **Wordmark tipográfico** adoptado: `radar))vivienda_ibiza`. Todo en `JetBrains Mono`, minúsculas, las `))` evocan ondas de radar como glifo puro, el underscore separa *topic_location* preparando el futuro ecosistema (`radar))turismo_ibiza`, `radar))medioambiente_ibiza`, `radar))vivienda_formentera`, etc.). Refuerza la dirección visual "mono + seams" que ya estaba apuntada.
- **Preview tipográfico** en [`docs/prototype/logo/preview.html`](docs/prototype/logo/preview.html) con 4 variantes a distintos tamaños (14-72 px), claro y oscuro, simulaciones de cabecera, pestaña y OG image:
  - V1 · Mono plano — todo un color, peso medio.
  - V2 · Split — `))` en terracota, resto en tinta.
  - V3 · Tri — `radar` semibold, `))` terracota bold, `vivienda_ibiza` regular muted.
  - V4 · Underline — `radar` con subrayado fino (seam).
- **Favicon** también será tipográfico. Opciones a probar en Paso 1 del prototipo: `))` en terracota, `r))`, o iniciales `rvi`. Se evita depender de carga de fuente mediante path vectorial SVG.
- **Tagline simplificado:** *"Observatorio documental"* (antes *"Observatorio documental de vivienda"*). La palabra "vivienda" ya está en el nombre; evitar redundancia.
- **Docs actualizadas:** CLAUDE.md, STATUS.md, ESTUDIO-DISENO.md §4 (reescrita entera), ROADMAP.md (B38, I7 reformuladas).

---

## 2026-04-21 — Estudio de diseño completo + rebranding a "Radar Ibiza"

- **Rebranding del proyecto a "Radar Ibiza"** (antes "Ibiza Housing Radar"). Dominio objetivo `radaribiza.com` — compra pendiente del editor. Motivos: el nombre en inglés restaba credibilidad local (target real: ibicencos + temporeros castellanohablantes + extranjeros residentes, no internacional); "Housing" sonaba corporativo y mal SEO castellano; referentes españoles del género (Civio, Datadista, Maldita) no meten la temática en el dominio. Tagline estable: *"Observatorio documental de vivienda"*. El repo GitHub mantiene slug `ibiza-housing-radar` hasta que se compre el dominio; renombrado coordinado después.
- **Estudio de diseño completo** entregado en [`ESTUDIO-DISENO.md`](ESTUDIO-DISENO.md) (14 secciones, ~700 líneas). Incluye benchmark editorial comparado con 13 referentes (Solar Low-Tech, Bellingcat, The Pudding, Civio, Datadista, Tortoise, El Orden Mundial, The Intercept, ProPublica, Rest of World, TheyWorkForYou, GovTrack, OpenSecrets), sistema visual con tokens completos, 9 componentes especificados, plantilla OG, plan de prototipo en 6 pasos, 12 decisiones abiertas más D13 añadida (formulario universal).
- **13 decisiones de diseño (D1-D13) cerradas** por el editor. 11 eligió la recomendación A, D11 optó por híbrido (automático default + dos botones manuales ○/●), D2 (logo) diferida hasta revisar SVG. Detalle en ESTUDIO-DISENO.md §11.
- **Taxonomía de actores cerrada en 8 categorías con candado**: institucional público, partido (siempre gris neutro — regla dura), patronal, sindicato, tercer sector, académico, judicial, colectivo ciudadano. Casos fronterizos se asimilan con nota editorial documentada; abrir la 9ª requiere decisión consciente con entrada en `/correcciones/`. El color del chip de actor es **refuerzo**, nunca única información (etiqueta de texto siempre visible).
- **Calendario editorial anclado al ciclo real de Ibiza** — opening/closing de clubs grandes (Pacha, Hï, Ushuaïa, Amnesia). Referencia interna. En 2026: 24 abril → ~12 octubre. Etiquetas públicas: `Temporada YYYY` (abr-oct) y `Pre-temporada YYYY` (oct del año anterior → abr). Sin "invierno" (ambiguo). La pre-temporada se nombra por el verano al que apunta, no por el año que acaba.
- **Numeración de ediciones "W17" fuera de cara pública** — confundía a lectores no técnicos. URLs usan fecha ISO del lunes: `/ediciones/2026-04-20/`. Cabecera, OG, chrome operacional: rango de fechas (`Edición del 20-26 abril 2026`). "W17" solo como slug interno (archivos, logs, commits).
- **Formulario universal "Escríbenos"** (D13) añadido al alcance. Botón flotante en esquina inferior derecha, visible en todas las páginas. Campos: mensaje obligatorio + nombre y email opcionales + auto-captura de URL origen. Backend Formspree (50 envíos/mes gratis). Abierto a correcciones, datos nuevos, pistas, testimonios, dudas, críticas y colaboraciones — no cerrado a "feedback" de producto. Anonimato permitido (muchos informantes valiosos trabajan en la sombra); el filtro real es "URL verificable" para incorporar al corpus.
- **Nuevas tareas en ROADMAP Bloque B (derivadas del estudio):** B34 prototipo HTML estático · B35 9 componentes en Jekyll · B36 formulario Escríbenos · B37 `/sistema/` interna · B38 logo SVG final · B39 OG Puppeteer · B40 toggle modo oscuro manual. Y A17 script `update_temporadas.py`.
- **Automatización anual para fechas de temporada** — cron GitHub Action (feb/mar/abr de cada año) que consulta news sobre las fechas de opening del año siguiente y alerta a Telegram cuando ≥3 clubs top coinciden. Editor actualiza `data/temporadas.yml` manualmente. Coste ~0,02 €/ejecución.
- **Prototipo de logo creado** en [`docs/prototype/logo/`](docs/prototype/logo/) con 3 direcciones SVG (Dir 1 punto limpio + arcos / Dir 2 "I" italic centro + arcos / Dir 3 "I" + arcos asimétricos lado) + `preview.html` que los muestra a 5 tamaños reales (16/22/48/120/256 px) en modo claro y oscuro, con composición de wordmark y simulaciones de pestaña y OG. Editor decide tras revisión visual.
- **Dirección visual "mono + seams" apuntada** — peso tipográfico mono (JetBrains Mono) en más elementos editoriales + separadores tipo costura (dashed, líneas finas) + iconografía Unicode pura (no emoji coloreado). Queda por formalizar al construir prototipo HTML estático.
- **Memoria del proyecto actualizada** con 4 archivos en `~/.claude/projects/.../memory/`: `nombre_proyecto.md`, `taxonomia_actores.md`, `calendario_editorial.md`, `decisiones_diseno_D1-D13.md`. Todos referenciados en `MEMORY.md` como índice.
- **Pendientes al cierre del estudio:** (1) compra dominio `radaribiza.com`, (2) elección de dirección de logo del prototipo, (3) validación de "mono + seams" al construir Paso 1 del plan, (4) barrido coordinado para renombrar repo GitHub a `radar-ibiza` cuando se compre dominio.

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
