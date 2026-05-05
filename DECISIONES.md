# DECISIONES — Radar Vivienda Ibiza

Registro **append-only** de decisiones del proyecto. Fuente única desde 2026-04-23.

## Reglas

1. **Una fila por decisión.** Nunca editar una fila cerrada; si cambia algo, añadir una nueva decisión que la reemplace y marcar la antigua como `superada_por: DXX`.
2. **ID correlativo `D0`, `D1`, `D2`…** Sin huecos, sin reutilizar.
3. **Decisión nueva entra aquí primero.** Otros docs referencian por ID (ej. *"ver [D7]"*), no duplican el contenido.
4. **Migración histórica pendiente.** D1-D13 de `ESTUDIO-DISENO.md` y las 16 de `DECISIONES-PENDIENTES.md` se moverán aquí durante la revisión profunda post-lanzamiento (ver `ESTUDIO-GESTION-CONOCIMIENTO.md` §3.4). Hasta entonces, ambos docs siguen siendo fuentes válidas de sus decisiones propias.
5. **Dos campos obligatorios desde 2026-04-24** (ver [D14](#d14--sistema-de-monitorización-de-decisiones-del-proyecto)): toda decisión nueva lleva `Próxima revisión` (fecha ISO o `permanente`) y `Criterio de revocación` (qué señal rompería la decisión). En D0-D13 se añadió retroactivamente solo `Próxima revisión`; el criterio de revocación no se redactó hacia atrás.

## Formato de fila

```
### D{N} — {título corto}
- **Fecha:** YYYY-MM-DD
- **Tema:** {pipeline | diseno | editorial | arquitectura | docs | costes | legal | otro}
- **Decisión:** {qué se decide, en una frase}
- **Por qué:** {motivo en 1-3 líneas}
- **Docs afectados:** {lista de archivos}
- **Próxima revisión:** YYYY-MM-DD | permanente
- **Criterio de revocación:** {qué señal rompería esta decisión}
- **Estado:** vigente | superada_por:DXX | revocada
```

---

## Decisiones

### D0 — Adoptar tres reglas baratas de gestión documental

- **Fecha:** 2026-04-23
- **Tema:** docs
- **Decisión:** (1) DIARIO con fecha ISO y etiqueta temática en cada entrada; (2) DECISIONES.md como fuente única para decisiones nuevas a partir de hoy; (3) STATUS.md reducido a ≤100 líneas.
- **Por qué:** frenar entropía documental sin ejecutar la reorganización completa (ver `ESTUDIO-GESTION-CONOCIMIENTO.md`), que se deja para después del lanzamiento. Las reglas son baratas, reversibles y no rompen enlaces existentes.
- **Docs afectados:** `CLAUDE.md`, `DIARIO.md`, `STATUS.md`, `DECISIONES.md` (nuevo), `ESTUDIO-GESTION-CONOCIMIENTO.md` (nuevo), `ROADMAP.md` (tarea diferida añadida).
- **Próxima revisión:** permanente
- **Estado:** vigente

### D1 — Partir construcción del auditor en mínimo viable + iteración posterior

- **Fecha:** 2026-04-23
- **Tema:** arquitectura
- **Decisión:** la construcción del auditor IA se parte en dos bloques. **Mínimo viable (2 semanas):** auditoría ciega con Sonnet + tres heurísticas (cruce de fuentes, verbatim match, whitelist de dominios) + log público con protocolo de corrección + integración con el pipeline. Sin Opus formalizado como capa separada (se queda como fallback de extracción actual), sin página de cuarentena, sin dashboard del auditor, sin repaso mensual IA. **Iteración posterior (2-3 semanas):** Opus capa explícita, página pública `/auditor/` con métricas, página `/revision-pendiente/` navegable, repaso mensual IA de la cuarentena (capa 5bis).
- **Por qué:** el plan cerrado en [ESTUDIO-COSTES-AUDITOR.md](ESTUDIO-COSTES-AUDITOR.md) construía las 5 capas completas desde el día uno. Es ambicioso para un editor operador no-programador que está validando el producto al mismo tiempo. El mínimo viable entrega el 80 % de la transparencia (doble-ojo automático + log público + protocolo de corrección) y llega antes al punto *"funciona y lo entiendo"*. La iteración posterior añade autoresolución + vitrina + autocalibración como confort y optimización, no como defensa.
- **Docs afectados:** `ESTUDIO-COSTES-AUDITOR.md` (§10.1 nueva), `REVISION-FASE-0.5.md` (PI9 partido), `ROADMAP.md` (Fase 1 reordenada), `STATUS.md` (próximo hito), `DISENO-AUDITOR-MVP.md` (plano de obra derivado, cerrado 2026-04-24).
- **Próxima revisión:** al cerrar el Hito 1 según el criterio reformulado en [D20](#d20--cierre-del-hito-1-con-calibración-en-vivo-desde-w19-no-por-backfill-de-w10) (calibración en vivo W19-W22, no backfill de W10).
- **Estado:** vigente

### D2 — Log del auditor público desde el día uno + protocolo formal de correcciones en 72 h

- **Fecha:** 2026-04-23
- **Tema:** arquitectura
- **Decisión:** opción (d) elegida entre cuatro alternativas evaluadas (público tal cual / retraso 30 días / privado con métricas públicas / público + protocolo). Cada propuesta lleva un campo `corrections` en el JSON del log, vacío al crearse, que crece con notas fechadas sin tocar el original. Canal de corrección: email al buzón del proyecto **+** formulario en la página de contacto. Backend del formulario: webhook que crea issue en GitHub (auditable). Notificación al editor: Telegram. Compromiso operativo: respuesta en 72 horas. Página pública `/correcciones/` con el protocolo en lenguaje llano.
- **Por qué:** coherente con la regla fundacional de transparencia radical. El auditor no crea exposición legal nueva — la noticia original ya está en internet; el log solo la estructura. El protocolo de correcciones es el escudo legal real: demuestra buena fe y due process, más defendible que retrasar o privatizar. No depende de cerrar el estudio del titular legal (RT20 + LG1): cuando ese estudio cierre, hereda el log existente sin migraciones. Riesgo residual aceptado: 72 h de exposición si entra algo difamatorio antes de que nadie lo dispute, que es el mismo riesgo de la noticia original.
- **Dependencia apuntada:** el buzón de email del proyecto queda **diferido** hasta que cierre el nombre definitivo del observatorio, y el nombre cierra cuando el editor vea la estructura final. No se crea buzón provisional. Cadena registrada en memoria del proyecto.
- **Docs afectados:** `ESTUDIO-COSTES-AUDITOR.md` (schema del log con campo `corrections`), `REVISION-FASE-0.5.md` (RT9 activa antes la página de correcciones como stub).
- **Próxima revisión:** al cerrar el estudio legal del titular (Hito 3) — fecha por fijar cuando arranque ese hito
- **Estado:** vigente

### D3 — Whitelist de dominios por actor: V1 con actores conocidos antes del backfill

- **Fecha:** 2026-04-23
- **Tema:** pipeline
- **Decisión:** montar `data/actor_domains.yml` con 15-20 actores conocidos (Consell d'Eivissa, Govern Balear, IBAVI, ayuntamientos principales, partidos con representación, UGT, CCOO, CAEB, PIMEEF, Cáritas, Creu Roja, Sindicat de Llogaters, PAH local) antes del backfill. Refinamiento de dominios reales (subdominios, variaciones) se hace con los datos del propio backfill como calibración.
- **Por qué:** la taxonomía de actores está cerrada en 8 categorías desde el 20-abr y los actores principales de vivienda en Ibiza son un conjunto conocido y corto. El backfill no va a descubrir actores nuevos, solo dominios reales. Montar V1 ahora desbloquea el arranque del auditor mínimo. Si aparece un actor no reconocido durante el backfill: el sistema lo anota como `whitelist_miss: true` en el log, nunca bloquea publicación por sí solo (otras heurísticas compensan), el parte Telegram del lunes agrupa los misses de la semana y el repaso mensual IA propone ampliaciones que el editor firma con OK.
- **Docs afectados:** `ESTUDIO-COSTES-AUDITOR.md`, `REVISION-FASE-0.5.md` (PI9).
- **Próxima revisión:** tras el backfill de 12 semanas (refinar dominios reales con datos empíricos)
- **Estado:** vigente

### D4 — Tests del auditor diferidos a la tarea de cobertura del pipeline (RT5)

- **Fecha:** 2026-04-23
- **Tema:** pipeline
- **Decisión:** no montar `tests/` ni `pytest` como parte del auditor mínimo. Los tests unitarios con 3 noticias fake previstos en el plan original se difieren a RT5 (*"Tests básicos del pipeline"*), que cubrirá auditor + verify + balance + extract + rescue en un solo bloque con fixtures reales extraídas del backfill. La validación del auditor durante su construcción es empírica: corrida sobre la semana W10 (2-8 marzo 2026) como prueba antes de comprometer las 12 semanas.
- **Por qué:** montar tests ahora sin fixtures del backfill obliga a usar fakes que prueban poco. Los tests con fixtures reales son más robustos y cubren los cinco módulos de una vez. La corrida empírica sobre una semana antigua es la validación real del auditor antes del backfill grande.
- **Docs afectados:** `REVISION-FASE-0.5.md` (RT5 con alcance ampliado), `ESTUDIO-COSTES-AUDITOR.md` (plan de construcción).
- **Próxima revisión:** al arrancar la tarea de cobertura del pipeline (RT5), tras el backfill
- **Estado:** vigente

### D5 — Re-estudio del sistema de tiers en paralelo a la construcción del auditor

- **Fecha:** 2026-04-23
- **Tema:** arquitectura
- **Decisión:** opción (b) elegida entre dos caminos. El re-estudio profundo del sistema de tiers (RT15) se ejecuta **en paralelo** a la construcción del auditor mínimo, no como prerrequisito bloqueante. El auditor se construye con un hueco reservado en el JSON del log: `tier: { value: null, reason: "pendiente estudio", signals: {} }`. El auditor calcula y guarda las señales que ya conoce (cruce de fuentes, verbatim match ratio, whitelist hit, viabilidad), pero no las combina en un badge público hasta que el estudio de tiers cierre y defina el árbol de decisión. En ese momento, la función final lee el bloque `signals` y devuelve el color sin migrar logs antiguos.
- **Por qué:** la opción secuencial (estudio primero, auditor después) bloquearía la construcción del auditor 1-2 semanas adicionales. La paralela desbloquea: el auditor funciona igual sin la etiqueta final; los tiers son capa de presentación, no de cálculo. El log queda coherente, las señales se acumulan desde el día uno, y al cierre del estudio solo se conecta la función de lectura. RT15 deja de ser prerrequisito del auditor y pasa a ser prerrequisito solo de PI10 (visualización pública de tiers).
- **Docs afectados:** `ESTUDIO-COSTES-AUDITOR.md` (schema del log con hueco tier), `REVISION-FASE-0.5.md` (RT15 reclasificada).
- **Próxima revisión:** permanente (el estudio de tiers cerró en D9; esta decisión ya cumplió su función)
- **Estado:** vigente

### D6 — Marco de tres hitos grandes como frame de trabajo de la Fase 1

- **Fecha:** 2026-04-23
- **Tema:** docs
- **Decisión:** el trabajo de la Fase 1 se organiza en tres hitos grandes donde el editor decide los puntos de entrada y de cierre, y Claude lleva los puntos pequeños dentro de cada hito. **Hito 1:** auditor mínimo viable publicado con una edición real. **Hito 2:** sistema de tiers cerrado e integrado. **Hito 3:** titular legal resuelto. El resto de las 34 tareas de la Revisión Fase 0.5 queda en cola; no se abren en paralelo. Al cerrar un hito, el editor elige el siguiente.
- **Por qué:** el editor expresó 2026-04-23 *"no siento que llevo las riendas"* con 34 tareas abiertas simultáneamente, cada una con ramificaciones en las demás. El marco de tres hitos reduce la carga cognitiva: fijar hitos grandes y delegar los pequeños dentro. Dentro de cada hito, Claude propone y el editor da OK por bloque, no por decisión unitaria. Si algo grande cambia de rumbo dentro de un hito, Claude para y pregunta.
- **Docs afectados:** `STATUS.md` (marco de trabajo + próximo hito), `ROADMAP.md` (Fase 1).
- **Próxima revisión:** al cerrar el Hito 1 (auditor mínimo viable publicado; sirve como puerta de entrada al Hito 2)
- **Estado:** vigente

### D7 — Rastro de decisiones pequeñas en DIARIO + resumen al `/cierre`

- **Fecha:** 2026-04-23
- **Tema:** docs
- **Decisión:** cuando Claude tome una decisión autónoma dentro de un hito (nombre de una función, orden de heurísticas, formato de un campo, elección entre dos alternativas equivalentes), la anota en `DIARIO.md` como línea corta: fecha, qué decidió, por qué. Formato integrado en las entradas existentes, no en documento nuevo. Al cierre de sesión o bloque (comando `/cierre`), Claude entrega al editor un resumen agrupado *"decisiones pequeñas de esta sesión"* con la lista en lenguaje llano. El editor puede: dejar correr (no hacer nada, quedan marcadas), revertir una (*"la decisión X no me encaja"*, vuelta atrás por git), o pedir detalle (*"por qué decidiste X"*).
- **Por qué:** el editor pidió 2026-04-23 poder seguir el rastro del proceso y revertir si algo no encaja. El diario + git ya dan reversibilidad; solo faltaba el hábito de anotación y el resumen al cierre. Mantiene autonomía de ejecución dentro del hito sin perder control editorial.
- **Docs afectados:** `DIARIO.md` (convención aplicada desde esta entrada).
- **Próxima revisión:** permanente
- **Estado:** vigente

### D8 — Experimento APRENDIZAJE.md: log de feedback formativo al cierre (solo-ibiza)

- **Fecha:** 2026-04-23
- **Tema:** docs
- **Decisión:** introducir un archivo `APRENDIZAJE.md` en la raíz del proyecto como log experimental de feedback formativo sobre cómo el editor desarrolla el proyecto. El Paso 6 del comando `/cierre` evalúa cada sesión si hay algo concreto que anotar (decisiones, alcance, priorización, comunicación, docs, coste, proceso, verificación); si no hay, reporta *"sin feedback hoy"* y no añade entrada. **Alcance: solo este proyecto**, no global ni plantilla. Incluye sección *"Cómo desactivar"* con dos pasos (~30 seg).
- **Por qué:** el editor pidió un loop de aprendizaje sobre su propia práctica sin comprometerse a mantenerlo si no aporta. La propuesta inicial era global (cruza proyectos) con replicación a los 4 proyectos del usuario; el editor la redujo a este proyecto y exigió reversibilidad explícita antes de aprobar. Cumple alcance conservador (memoria `feedback_alcance_proyecto.md`) y principio de no escalar sin demanda orgánica (memoria `feedback_esperar_demanda_organica.md`).
- **Docs afectados:** `APRENDIZAJE.md` (nuevo), `.claude/commands/cierre.md` (Paso 6 añadido), `CLAUDE.md` (mención en sección *"Cierre de sesión"*), `STATUS.md` (lista de docs vivos +1). Revertidos en la misma sesión: `~/.claude/APRENDIZAJE.md`, `~/.claude/CLAUDE.md` sección *"Aprendizaje transversal"*, y `~/Documents/GitHub/.claude-template/commands/cierre.template.md` Paso 6.
- **Próxima revisión:** N/A (revocada)
- **Estado:** **revocada 2026-04-23**. El editor abortó el experimento en la misma sesión: no aportó señal útil en la única entrada generada + añadía tiempo al cierre sin compensar. Retirados `APRENDIZAJE.md`, Paso 6 del `/cierre`, y menciones en CLAUDE y STATUS. La reversibilidad explícita diseñada en D8 funcionó: desmontaje en minutos.

### D9 — Cierre del sistema de tiers de confianza: 5 reglas operativas

- **Fecha:** 2026-04-23
- **Tema:** arquitectura
- **Decisión:** cerradas las cinco preguntas abiertas de [`ESTUDIO-TIERS.md §11`](ESTUDIO-TIERS.md) con las recomendaciones del asistente aceptadas en bloque:
  - **Visibilidad de los tiers (Q1) = mixto.** 🟢 sin badge visual (asumido: lo que pasa los controles se publica sin aspavientos). 🟡 / 🟠 / 🔴 con badge + copy de aviso. Coherente con la filosofía editorial del proyecto.
  - **Techo de fuente única (Q2) = decidir tras backfill.** Regla dura en vigor hasta entonces (nunca 🟢 con una sola URL). Si la medición empírica del sesgo (RT25) muestra que alguna categoría de actor queda más de un 30 % por debajo del promedio global de 🟢 con n ≥ 5, aplicar mitigación M1: permitir 🟢 con fuente única **solo** para colectivos ciudadanos, tercer sector, sindicatos minoritarios y asambleas, y **solo** cuando el dominio es el oficial del actor (whitelist = refuerza).
  - **Default del paso 6 del árbol (Q3) = 🟠 + alerta Telegram.** Combinaciones raras de señales se publican con aviso, no se cuarentenan. Cada vez que se dispara el default, alerta al canal del editor para revisar y añadir regla explícita al árbol.
  - **Política de cambios retroactivos (Q4) = congelar.** Tier calculado una vez al publicar, inmutable en log. Cambios de umbrales afectan solo a nuevas. Si un cambio destapa errores en pasadas, corrección vía `/correcciones/` ([D2](DECISIONES.md)), no recálculo masivo silencioso.
  - **Mockups visuales HTML (Q5) = Fase 4.** Los mockups textuales del §9 bastan para validar el árbol y el copy. Los HTML se integran cuando se retome el prototipo del Bloque B, mantenido en pausa activa desde 2026-04-21.
- **Por qué:** el asistente propuso las cinco recomendaciones con razonamiento en el estudio; el editor las aceptó en bloque tras leer el documento completo. Coherencia interna alta (mixto encaja con "confía por defecto, señala excepciones"; congelar encaja con "ediciones no se reescriben"; 🟠 default encaja con "no perder editorial por combinación rara, pero vigilar"). Q2 se deja para datos reales, evitando una decisión anticipada sobre un sesgo que puede no existir o ser menor del esperado.
- **Docs afectados:** [`ESTUDIO-TIERS.md §11`](ESTUDIO-TIERS.md) (decisiones registradas + estudio pasa a ✅ cerrado salvo §8 empírico dependiente de RT25). [`REVISION-FASE-0.5.md`](REVISION-FASE-0.5.md): RT15 → ✅, RT26 → ✅. [`ROADMAP.md`](ROADMAP.md): Fase 1 Hito 2 refleja cierre. [`STATUS.md`](STATUS.md): actualizado.
- **Pendiente de implementación** (no bloquea D9 como decisión, entra en PI10): crear `src/tiers.py` con `compute_tier(signals)` + `data/tiers.yml` con los umbrales operativos + plantilla visual del badge en Jekyll + página `/metodologia/#tiers` con el copy de §5.
- **Próxima revisión:** tras el backfill de 12 semanas (medición empírica del sesgo por actor para resolver Q2 y afinar umbrales)
- **Estado:** vigente

### D10 — Tres niveles de arranque de sesión + índice vivo de comandos

- **Fecha:** 2026-04-23
- **Tema:** docs
- **Decisión:** adoptar tres comandos de arranque escalonados — `/arranque` (Tier 1, default: STATUS + DECISIONES + DIARIO reciente), `/arranque-fase` (Tier 2: añade PLAN, ARQUITECTURA y el estudio del área), `/arranque-auditoria` (Tier 3: escaneo completo). Más un índice vivo `COMANDOS.md` en raíz que lista todos los slash commands del proyecto y los globales; todo comando nuevo entra en la tabla en el mismo commit que lo crea.
- **Por qué:** el editor pidió romper el patrón de *"escanea todo el proyecto"* cada vez que abre sesión. Un único modo profundo desperdicia contexto en sesiones pequeñas; tres escalones encajan con la intensidad real del trabajo. El índice hace descubrible el sistema tanto al editor humano como al asistente al arrancar (vía puntero en `CLAUDE.md`). Encaja con [D0](#d0--adoptar-tres-reglas-baratas-de-gestión-documental) como otra convención durable sobre cómo se trabaja en el proyecto.
- **Docs afectados:** `.claude/commands/arranque.md`, `.claude/commands/arranque-fase.md`, `.claude/commands/arranque-auditoria.md`, `COMANDOS.md`, `CLAUDE.md` (sección renombrada a *"Slash commands del proyecto"*), `.claude/commands/cierre.md` (separador visual del bloque añadido).
- **Próxima revisión:** N/A (superada parcialmente por D13)
- **Estado:** **superada_por:D13** (parcialmente). D13 elimina `/arranque-fase` y sustituye los tres niveles por cuatro modos (sin comando + `/arranque` + `/arranque-auditoria` + `/arranque-total`) más el comando transversal `/ampliar`. El índice vivo `COMANDOS.md` introducido aquí **sigue vigente** y ha sido actualizado por D13.

### D12 — Arranque por defecto sin informe + recomendaciones 1-3 en los tres arranques + lenguaje llano en chat + cero códigos sueltos (refuerzo)

- **Fecha:** 2026-04-24
- **Tema:** docs
- **Decisión:** cuatro cambios sobre cómo el asistente arranca y habla en este proyecto.
  - **(a) Arranque por defecto sin informe.** Al abrir sesión sin invocar ningún comando, el asistente lee `STATUS.md`, `DECISIONES.md` y las primeras 120 líneas de `DIARIO.md` en silencio y responde directo al prompt del editor. El informe ordenado + 1-3 recomendaciones + pregunta *"¿qué hacemos?"* solo se dispara cuando el editor escribe `/arranque` explícito.
  - **(b) Recomendaciones 1-3 en los tres arranques.** Los comandos `/arranque`, `/arranque-fase` y `/arranque-auditoria` incorporan un paso nuevo tras la síntesis y antes de la pregunta de cierre: entre 1 y 3 recomendaciones de siguiente paso concreto, una línea cada una, nombre de la cosa primero, verbo de acción + por qué corto + identificador opcional entre paréntesis al final. Si solo hay una o dos naturales, no forzar tres.
  - **(c) Lenguaje llano en el chat del proyecto.** En las conversaciones con el editor dentro de este proyecto, bajar un punto el nivel técnico: traducir tecnicismos evitables al español común (flujo, registro, estructura, diferencias, envío…). La palabra técnica se mantiene en documentos internos de arquitectura, estudios y código. Alcance solo este proyecto.
  - **(d) Cero códigos sueltos en el chat (refuerzo con tolerancia cero).** Siempre empezar por el nombre de la cosa; el identificador va entre paréntesis al final y solo si aporta trazabilidad. Nunca como etiqueta principal, nunca como primer elemento de una línea. Cuarta recaída acumulada a 2026-04-24 — próxima = fallo grave.
- **Por qué:** el editor señaló 2026-04-24 dos problemas en el mismo turno. Primero, que el arranque explícito saca informe incluso cuando él ya traía la tarea definida, lo que añade fricción en sesiones de continuidad; el modo por defecto silencioso resuelve eso y deja el comando explícito para cuando sí quiere panorámica. Segundo, cuarta recaída del patrón de códigos sueltos (*"sigues mencionando códigos RT26/Q1-Q5 sin explicar que son, lo he dicho mil veces y sigues haciendolo"*), más el pedido paralelo de *"bajar un punto el lenguaje técnico"* en la conversación del proyecto. Las cuatro piezas son coherentes entre sí: bajan la fricción de lectura del editor al hablar con el asistente.
- **Docs afectados:** `CLAUDE.md` (sección *Slash commands* con regla del modo por defecto + sección nueva *Lenguaje en el chat del proyecto* + refuerzo en *Qué NO hacer*), `COMANDOS.md` (tabla y criterio de arranque con cuatro modos), `.claude/commands/arranque.md` (Paso 3 recomendaciones + nota del modo por defecto), `.claude/commands/arranque-fase.md` (Paso 4 recomendaciones), `.claude/commands/arranque-auditoria.md` (Paso 6 recomendaciones), memorias del asistente `feedback_referencias_con_contexto.md` (endurecida) y `feedback_lenguaje_llano_chat.md` (nueva), `MEMORY.md` (índice actualizado).
- **Próxima revisión:** permanente (convenciones operativas; solo se revisan si el editor expresa queja)
- **Estado:** vigente

### D13 — Rediseño del sistema de arranque: se elimina el intermedio, se añade el total con inventario veraz y el comando transversal `/ampliar`

- **Fecha:** 2026-04-24
- **Tema:** docs
- **Decisión:** el sistema de arranque pasa a cuatro modos más un comando transversal.
  - **(a) Sin comando** — modo por defecto silencioso (confirmado en D12).
  - **(b) `/arranque`** — ligero, informe de ~200 palabras + recomendaciones + pregunta.
  - **(c) `/arranque-auditoria`** — profundo, mapa de estudios + código (como antes).
  - **(d) `/arranque-total`** — nuevo. Escaneo completo del proyecto sin huecos. Al arrancar, el asistente hace inventario silencioso de las carpetas, contrasta con el mapa que ya tiene cargado del documento de instrucciones, lee cabeceras solo de archivos nuevos o raros, presenta al editor **solo la lista de exclusiones razonadas** (nunca el inventario completo con conteos), y tras confirmación del editor lee todo lo acordado en profundidad. Sin reglas codificadas en el archivo del comando. Uso escaso (2-3 veces al año).
  - **(e) `/ampliar [área o descripción]`** — nuevo, transversal. Carga documentos de un área concreta del proyecto sin sacar informe. Dos formas: palabra clave con mapeo interno (*diseño*, *auditor*, *tiers*, *costes*, *legal*, *pipeline*, *contenido*, *seo*, *modelos*, *docs*, *web*) o descripción libre interpretada por el asistente. Salida = una línea confirmando qué se leyó y sigue atendiendo la tarea.
  - **(f) Se elimina `/arranque-fase`** (el intermedio tier 2 añadido en D10). Queda absorbido entre el ligero y `/ampliar`, que cubren los mismos casos con menos ceremonia.
- **Por qué:** el editor señaló 2026-04-24 dos cosas. Primero, que raramente tenía claro cuándo usar el intermedio — las sesiones son o pequeñas (ligero basta) o grandes (profundo hace falta), y el caso intermedio (*"hoy toco diseño una mañana"*) se cubre mejor con un comando de ampliación explícito que con un tier completo. Segundo, que el arranque profundo no escanea literalmente todo el proyecto — se queda fuera el README, las ediciones publicadas, los prototipos, las tareas automáticas, los comandos del propio proyecto, etc. — y para los pocos casos donde hace falta ver todo hacía falta un nivel más. La versión calibrada del total (contraste con el mapa conocido del documento de instrucciones + cabeceras solo de novedades) evita leer cabeceras de 80 archivos cada vez sin perder veracidad donde importa.
- **Docs afectados:** `.claude/commands/arranque-total.md` (nuevo), `.claude/commands/ampliar.md` (nuevo), `.claude/commands/arranque-fase.md` (eliminado), `.claude/commands/arranque.md` (referencias al intermedio reemplazadas por ampliar/total), `.claude/commands/arranque-auditoria.md` (paso 1 reescrito sin referencia al intermedio), `CLAUDE.md` (sección *Slash commands del proyecto* reescrita), `COMANDOS.md` (tabla + criterio de arranque + convención de nombres actualizados).
- **Próxima revisión:** permanente (convenciones operativas; solo se revisan si el editor expresa queja)
- **Estado:** vigente

### D11 — Modelo de tiempos del proyecto: calendario / esfuerzo editor / esfuerzo Claude + fecha de relanzamiento lunes 13 jul 2026 [SUPERADA por D15]

> ⚠️ **Superada 2026-04-24 por [D15](DECISIONES.md).** El proyecto elimina calendario público y fecha objetivo de relanzamiento. El modelo de tres números (calendario / esfuerzo editor / esfuerzo Claude) queda fuera: las estimaciones se expresan ahora solo como esfuerzo relativo, sin convertirlo en fecha. Esta decisión se mantiene como histórica para trazabilidad del razonamiento.

- **Fecha:** 2026-04-23
- **Tema:** docs
- **Decisión (histórica):** (a) toda estimación de tiempo del proyecto se expresa con tres números distintos, nunca uno solo: **calendario** (semanas de reloj real), **esfuerzo editor** (horas reales del editor, a ritmo sostenible asumido 15 h/sem) y **esfuerzo Claude** (horas del asistente, que no colapsa calendario porque el cuello de botella es la decisión/revisión del editor). (b) fecha objetivo del relanzamiento público fijada en **lunes 13 jul 2026** (opción A del análisis del §6 de `ESTUDIOS-PENDIENTES.md`), con escenario B (lunes 12 oct 2026, cierre de temporada) como red de seguridad si el ritmo no acompaña sin cambiar roadmap ni alcance.
- **Supuestos que tenía que cumplir el lunes 13 jul:** ritmo 15 h/sem sostenido del editor, sin imprevistos personales mayores de 1 semana, cero re-alcances grandes, prueba empírica del auditor MVP sobre la semana de 2-8 mar 2026 pasa a la primera.
- **Por qué (modelo de tiempos):** el editor avisó 2026-04-23 noche que no tomaba en cuenta las estimaciones porque mezclaban tres cosas distintas bajo la misma etiqueta ("2 semanas" usado indistintamente para calendario, esfuerzo técnico que el asistente desbroza en una tarde, o esfuerzo real del editor).
- **Por qué se supera:** 2026-04-24 el editor constató que ninguna de las fechas propuestas era real ni útil. Las fechas creaban presión ficticia y pedían mantener un sistema (avisador, panel con vencidas) apuntando a metas imaginarias. Mejor eliminar la ficción.
- **Docs afectados (originales):** `ROADMAP.md` (sección *"Cómo leer las estimaciones de tiempo"* + fecha objetivo en Fase 7), `STATUS.md` (próximos hitos con fecha 13 jul), `ESTUDIOS-PENDIENTES.md` (§6 marcada como superada por esta decisión).
- **Próxima revisión:** permanente (decisión cerrada; la sustitución vive en D15)
- **Estado:** superada por [D15](DECISIONES.md) (2026-04-24)

### D15 — Sin calendario público ni fecha de lanzamiento. El ritmo lo marca el editor, no el reloj

- **Fecha:** 2026-04-24
- **Tema:** docs
- **Decisión:** el proyecto **no tiene** fecha de lanzamiento público, calendario de fases con rango día-día, ni metas del tipo *"relanzamos el lunes X"* o *"la semana 1 va del día A al día B"*. Todo se organiza por **hitos** (qué queda cerrado) y por **esfuerzo relativo** (si aporta: *"~10 h de trabajo del editor"*, *"~20 h acumuladas"*), nunca por fecha futura. Las *Próximas revisiones* del registro de decisiones dejan de aceptar fechas ISO de calendario: se reescriben como eventos (*"al cerrar el Hito 1"*, *"post-backfill"*, *"tras N ediciones"*, *"permanente"*). Las que no tengan disparador natural quedan *"permanente"* hasta que algo las mueva.
- **Por qué:** las fechas planteadas hasta aquí (relanzamiento el lunes 13 jul 2026, calendario de 4 semanas del auditor, *"revisar el 2026-05-15"*, *"revisar el 2026-06-15"*) no son reales. El ritmo lo marca el editor, no el calendario, y no hay compromiso público que dependa de llegar a una fecha. Mantener fechas ficticias fuerza un sistema (panel con vencidas, avisador semanal) que apunta a metas imaginarias y crea sensación falsa de atraso cada vez que pasan por el mirador del lunes. Más honesto borrar la ficción que mantenerla.
- **Efectos inmediatos:** (a) [D11](DECISIONES.md) queda superada (histórica). (b) *Próxima revisión* con fecha ISO en [D1](DECISIONES.md), [D3](DECISIONES.md), [D4](DECISIONES.md), [D6](DECISIONES.md), [D9](DECISIONES.md), [D14](DECISIONES.md) se reescribe como evento o hito. (c) `STATUS.md` pierde el bloque de próximos hitos con fecha. (d) El plano del auditor (`DISENO-AUDITOR-MVP.md` §9) pasa de *"Semanas 1-4"* con rangos de días a *"Fases 1-4"* sin fecha. (e) `ROADMAP.md` cabecera y `ESTUDIOS-PENDIENTES.md` §6 se reescriben. (f) El avisador semanal (`src/decisions_watch.py`) queda ocioso hasta que una decisión vuelva a tener fecha ISO parseable (comportamiento correcto, no hay nada que avisar). El tablero interno (`private/panel.md`) mostrará las revisiones pendientes como texto libre en vez de con orden temporal.
- **Qué sí se mantiene:** fechas históricas (cuándo se tomó una decisión, cuándo salió una edición, rangos reales de semanas ya publicadas como la W10 del 2-8 mar 2026, fechas de commits). El calendario editorial de temporada/pre-temporada sigue anclado a los datos reales de *opening/closing* de Ibiza: es dato observable, no objetivo de lanzamiento.
- **Docs afectados:** `DECISIONES.md` (D11 superada + D15 nueva + reescritura de 6 *Próximas revisiones*), `STATUS.md`, `DISENO-AUDITOR-MVP.md`, `ROADMAP.md`, `ESTUDIOS-PENDIENTES.md`, `DIARIO.md`.
- **Próxima revisión:** permanente (si alguna vez reaparece la necesidad de fijar fecha pública, se abrirá con decisión nueva)
- **Criterio de revocación:** si el proyecto llega a un nivel de madurez en que fijar un objetivo público ancla positivamente (por ejemplo, *"lanzamiento alineado con cierre de temporada"*) y hay compromiso externo que lo justifique, reabrir.
- **Estado:** vigente

### D19 — Página global `/propuestas/` con vista agregada del histórico

- **Fecha:** 2026-04-27
- **Tema:** editorial
- **Decisión:** crear página pública `/propuestas/` que muestra **todas** las propuestas documentadas en el histórico, agrupadas por estado actual (implementada, en ejecución, aprobada, en debate, en movimiento, propuesta, descartada, pendiente judicial, desconocido). Cada tarjeta incluye actor + tipo, resumen, palanca, horizonte, edición de origen y enlace a la fuente. Sin filtros JavaScript en V1 (anclas + secciones agrupadas son suficientes para escanear). Generada por `src/build_proposals.py` que lee `data/proposals_history.json` y emite `docs/propuestas.md`. Integrada en el cron del lunes tras `build_index`. Enlace añadido al menú principal.
- **Por qué:** sin esta página el "mapa" del observatorio se queda dentro de cada edición semanal aislada — el lector no podía ver el conjunto de propuestas documentadas. Es exactamente lo que diferencia al observatorio de cualquier diario: la agregación. Demanda explícita del editor 2026-04-27 al revisar W18.
- **Docs afectados:** `src/build_proposals.py` (nuevo), `docs/propuestas.md` (nuevo, generado), `docs/_includes/header.html` (enlace añadido), `docs/assets/css/main.css` (estilos `.prop-*`), `src/report.py` (paso `build_proposals` tras `build_index`), `.github/workflows/weekly-report.yml` (commit-back de `data/proposals_history.json` + `data/feed_health.json` que también faltaban).
- **Próxima revisión:** tras 4-6 ediciones con datos acumulados (~mediados de junio 2026)
- **Criterio de revocación:** (a) si el lector no encuentra valor en la vista agregada (medible solo cuando haya tráfico real), (b) si la lista crece demasiado (>200 propuestas) y la agrupación por estado no basta para escanear — entonces añadir filtros por palanca/actor o paginación, (c) si los estados resultan inestables y las tarjetas saltan de grupo entre semanas confundiendo al lector.
- **Estado:** vigente

### D18 — Política de actualización retroactiva de ediciones publicadas

- **Fecha:** 2026-04-27
- **Tema:** editorial
- **Decisión:** las ediciones publicadas se tratan según tres categorías. (1) **Contenido editorial** (texto del análisis, redacción, citas, cita de actores en prosa): NO se toca. La regla fundacional 5 cubre los errores: corrección visible en `/correcciones/` con fecha y motivo, edición original marcada como "corregida" con enlace a la nota. Romper "lo que dijimos cuando lo dijimos" rompe la promesa documental. (2) **Metadata estructurada** (tipología de actor, etiquetas de bloque, palanca, estado de propuesta, frontmatter en general): SÍ se actualiza retroactivamente y sin marca pública, siempre que no altere el texto del cuerpo. Cambios silenciosos a la estructura para coherencia agregada (taxonomía consistente entre ediciones). (3) **Presentación visual** (CSS, plantillas Jekyll, layout, navegación, footer): SÍ se actualiza libremente. La presentación no afecta al texto histórico.
- **Por qué:** sin esta separación, dos demandas contradictorias chocan: la promesa documental ("registro fiel a la fecha") exige no tocar, pero la promesa de calidad agregada (taxonomía consistente, navegación coherente entre ediciones) exige actualizar. La separación las concilia porque cada una opera sobre un sustrato distinto (texto vs. estructura vs. presentación). El editor planteó la pregunta en sesión 2026-04-27 al detectar inconsistencia de tipología del actor "Marí" entre W17 y W18.
- **Docs afectados:** `CLAUDE.md` (sección nueva *Política de actualización retroactiva*, pendiente), `APRENDIZAJES.md` (sugerencia 1 del W18 sobre heredar tipología pasa a aplicarse retroactivamente cuando se ejecute).
- **Próxima revisión:** tras 3-4 actualizaciones retroactivas reales (medir si la separación es operativa)
- **Criterio de revocación:** (a) si una actualización de metadata cambia la lectura efectiva del texto del cuerpo (no debería; si pasa, indica mala separación), (b) si el público interpreta un cambio retroactivo de metadata como una corrección encubierta y eso erosiona la confianza, (c) si la complejidad operativa de mantener las tres categorías separadas no compensa el beneficio.
- **Estado:** vigente

### D17 — Ritual de aprendizaje semanal + temperature=0 en self-review

- **Fecha:** 2026-04-27
- **Tema:** pipeline
- **Decisión:** (1) Adoptar ritual semanal de aprendizaje: cada arranque de sesión, Claude revisa el self-review más reciente, cruza con `APRENDIZAJES.md` y trae informe corto al editor con propuesta de decisión por sugerencia (aplicar / descartar con motivo / dejar en seguimiento). El editor decide en una palabra; aplicado se commitea citando la edición de origen. (2) Aplicar `temperature=0` en la llamada de `src/self_review.py` para reducir varianza entre lecturas (Sonnet 4.6 sigue admitiéndolo; Opus 4.7 ya no). (3) Mantener la política actual de alerta `nota <7 → Telegram` durante 4-6 ediciones más; revisar el 2026-06-08 (lunes, ≈6 semanas) si conviene migrar a una política basada en warnings recurrentes en lugar de notas absolutas.
- **Por qué:** sin ritual fijo, las sugerencias del self-review se diluyen en `private/self-review/{edicion}.md` y la promesa de "mejorar semana a semana" se queda en intención. Llevarlo Claude (no el editor) reduce fricción a casi cero. La varianza de notas detectada en el regenerado de W18 (rigor 5 → 8 entre dos lecturas idénticas) hace ruidoso el umbral fijo; `temperature=0` mitiga sin eliminar (los warnings cualitativos siguen siendo la fuente fiable). La revisión a 6 semanas evita rediseñar la política sin datos suficientes.
- **Docs afectados:** `APRENDIZAJES.md` (nuevo, raíz), `CLAUDE.md` (sección *Ritual de aprendizaje semanal*), `src/self_review.py` (`temperature=0`).
- **Próxima revisión:** 2026-06-08
- **Criterio de revocación:** (a) si el ritual genera fricción real (editor abriendo sesiones específicas en 3+ semanas seguidas para discutir propuestas), (b) si `temperature=0` reduce la varianza por debajo de lo útil (notas pegadas en 8-9 sin variar), (c) si tras 4-6 ediciones los warnings recurrentes son más fiables que las notas y conviene migrar la política de alerta.
- **Estado:** vigente

### D16 — Sistema de auto-recuperación del pipeline en tres capas

- **Fecha:** 2026-04-27
- **Tema:** arquitectura
- **Decisión:** ningún lunes se queda sin edición. El pipeline se cubre con tres capas de recuperación: (1) reintentos automáticos del SDK Anthropic ante errores transitorios (`max_retries=5` para 408/409/429/5xx y conexión, con back-off exponencial), aplicado en los 5 módulos que llaman a la API; (2) workflow nuevo `auto-retry.yml` que se dispara con cada push a `src/**` en main y, si detecta marca de fallo viva + edición no publicada + cooldown de 5 min, relanza `weekly-report.yml`; (3) marca persistente `data/PIPELINE_FAILED.flag` que sobrevive entre runs vía commit-back, lleva edición + error + timestamp del fallo y sirve de señal para identificar la recuperación. Cuando un run termina bien tras un fallo previo, el aviso de Telegram lleva prefijo *"✅ Recuperado tras fallo de [edición]"* y borra la marca. El aviso de éxito ahora incluye dos costes: edición concreta y mes acumulado.
- **Por qué:** el incidente del 2026-04-27 (W18) reveló dos fallos en cadena: techo bajo en el clasificador (truncado JSON con 67 noticias) tapaba un segundo fallo (parámetro `temperature` deprecado en Opus 4.7). Hasta arreglar y relanzar manualmente, la promesa editorial *"cada lunes una edición"* dependía de que el editor estuviese delante del Telegram. Con el sistema de tres capas: los fallos transitorios se autoresuelven sin que el editor se entere; los estructurales avisan claro, y el sistema vuelve a publicar solo cuando se empuja el fix. Coste cero (no consume API extra).
- **Docs afectados:** `src/costs.py` (`edition_spend_eur`), `src/report.py` (propagación EDITION + marca + recuperación + coste por edición), `src/classify.py` `src/extract.py` `src/generate.py` `src/audit.py` `src/self_review.py` (max_retries=5), `.github/workflows/weekly-report.yml` (`if: always()` + commit-back de la marca), `.github/workflows/auto-retry.yml` (nuevo).
- **Próxima revisión:** tras 2-4 ediciones del sistema funcionando con incidentes reales (no sintéticos)
- **Criterio de revocación:** (a) si el auto-relanzar dispara bucles (>2 relanzamientos por incidente único), (b) si los reintentos automáticos enmascaran fallos reales que requieren intervención humana, (c) si la marca persistente queda atascada en estado fallido por bug en el flujo de borrado.
- **Estado:** vigente

### D14 — Sistema de monitorización de decisiones del proyecto

- **Fecha:** 2026-04-24
- **Tema:** docs
- **Decisión:** montar un sistema ligero de vigilancia sobre las decisiones del proyecto en seis piezas concretas, sin infra nueva:
  - **(a) Formato del registro ampliado con dos campos obligatorios.** `Próxima revisión` (fecha ISO o `permanente`) y `Criterio de revocación` (qué señal rompería la decisión). Obligatorios para decisiones nuevas; en D0-D13 se añadió retroactivamente solo `Próxima revisión`.
  - **(b) Regla 4 permanente en CLAUDE.md.** Toda decisión nueva exige ambos campos; sin ellos, la decisión no entra al registro. Hace durable la convención sin depender de memoria.
  - **(c) Tarea automática semanal que avisa por Telegram** (nuevo módulo `src/decisions_watch.py`, enganchado al workflow `weekly-report.yml` lunes 05:00 UTC). Lee `DECISIONES.md`, extrae fechas, y manda alerta si hay `Próxima revisión` vencida o próxima (≤7 días). Reutiliza `src/notify.py` existente.
  - **(d) Refuerzo en el arranque de Claude.** En cualquier modo de arranque (por defecto, ligero, profundo, total), si al leer el registro se detecta decisión con revisión vencida, el asistente la cita en la primera línea antes de responder al prompt del editor. Triple red con Telegram + tablero interno.
  - **(e) Tablero interno único** en `private/panel.md` (generado por `src/panel.py`, enganchado al workflow). Agrega señales existentes (última edición, gasto del mes, nota de autoevaluación, verificación, decisiones con revisión pendiente). No genera datos; solo agrega. Archivo privado, no servido por GitHub Pages.
  - **(f) Pendientes apuntados.** Panel público en `/estado/` (diferido a segunda fase tras ver el interno una semana). Aviso 2 (patrón estructural en autoevaluación = dos semanas consecutivas con nota <7 en misma dimensión). Aviso 3 (acumulación de 5 decisiones pequeñas autónomas mías sin resumen al editor). Revisar activación de 2 y 3 tras 2-4 ediciones del sistema funcionando.
- **Por qué:** el editor pidió 2026-04-24 un sistema para monitorizar las decisiones del proyecto (las suyas y las del asistente) con panel, alertas a Telegram y normas permanentes — *"ligero pero potente"*. El diagnóstico previo identificó que ya existían cuatro capas de vigilancia montadas pero dispersas (costes, autoevaluación semanal, verificación por capas, balance trimestral) y tres huecos reales: (1) decisiones sin fecha de caducidad; (2) no había punto único para saber si la semana va bien; (3) falsos positivos de ingesta sin contar. Esta decisión cubre (1) y (2) apalancando lo existente, sin duplicar. (3) queda fuera por carecer de demanda orgánica (memoria `feedback_esperar_demanda_organica.md`).
- **Docs afectados:** `DECISIONES.md` (formato ampliado + campo retroactivo en D0-D13 + corrección de estado de D10 a superada_por:D13 parcial), `CLAUDE.md` (regla 4 de gestión documental), `src/panel.py` (nuevo), `private/panel.md` (nuevo), `src/decisions_watch.py` (nuevo), `.github/workflows/weekly-report.yml` (pasos nuevos antes de la generación), `DIARIO.md` (entrada 2026-04-24 [docs]).
- **Próxima revisión:** tras 2-4 ediciones del sistema funcionando (decidir si activar avisos 2 y 3, y validar que aporta más que lo que pesa)
- **Criterio de revocación:** si tras 2-4 ediciones el aviso 1 no se ha disparado sobre ninguna decisión vencida (ahora mismo ocurre porque D15 deja casi todas las decisiones sin fecha ISO — ver su *Efecto (f)*), el sistema requiere más de 30 min/mes de mantenimiento, o el editor lo percibe como fricción > valor, simplificar o desmantelar. Reversibilidad: borrar `src/panel.py` + `src/decisions_watch.py` + paso del workflow + regla 4 de CLAUDE.md + campos ampliados de DECISIONES.md. Reversión total en <15 min.
- **Estado:** vigente

### D20 — Cierre del Hito 1 con calibración en vivo desde W19, no por backfill de W10

- **Fecha:** 2026-04-28
- **Tema:** arquitectura
- **Decisión:** el criterio de cierre del Hito 1 (auditor MVP) deja de ser *"prueba empírica sobre el backfill de la semana W10 (2-8 mar 2026)"* y pasa a ser *"primera corrida limpia del cron en W19 + revisión de métricas tras 3-4 ediciones consecutivas con el auditor activo (W19-W22)"*. Las métricas a revisar siguen siendo las del §10 del plano del auditor (ratio de disputas en rango saludable, coste por edición <0,50 €, las 11 señales pobladas, ninguna heurística falla en silencio, edición pública sigue legible).
- **Por qué:** la Fase 3 ya integró el auditor en `src/report.py` y desde W18 corre vivo. El backfill de W10 requería primero construir `src/backfill.py` (tarea de Fase 2 del ROADMAP, todavía no abordada) porque la ingesta solo recupera ventana RSS reciente. Calibrar antes de seguir bloquea Fase 2 sin mejorar lo que el cron en vivo ya da gratis cada lunes. Calibrar con datos en vivo desde W19 acumula muestra real (3-4 ediciones × 3-7 propuestas semanales) sin coste extra ni nuevas dependencias. El commit-back ya cubre la persistencia: `data/audit/` está incluido en `git add` del workflow desde el fix del 2026-04-27 (verificado 2026-04-28).
- **Efectos inmediatos:** (a) Fase 4 del plano se reformula como *"observación en vivo W19-W22"* en vez de *"backfill W10"*. (b) D1 *Próxima revisión* apunta a este D20. (c) `DISENO-AUDITOR-MVP.md` actualiza §1, §9 (Fase 4), §10 (criterios). (d) STATUS y ROADMAP reflejan la observación en vivo. (e) Las menciones tangenciales a W10 en D4 y REVISION-FASE-0.5 se mantienen — su decisión principal no cambia y D20 las supera operativamente sin invalidar el archivo cerrado.
- **Docs afectados:** `DECISIONES.md` (D20 nuevo + D1 *Próxima revisión*), `DISENO-AUDITOR-MVP.md` (§1, §9, §10), `STATUS.md` (Hito 1), `ROADMAP.md` (Fase 1, Hito 1 detalle), `DIARIO.md` (entrada nueva 2026-04-28).
- **Próxima revisión:** tras la edición W22 (4ª corrida live del auditor) — momento en que se evalúan las métricas acumuladas y se cierra o reabre el Hito 1.
- **Criterio de revocación:** (a) si tras 3-4 ediciones la muestra acumulada (~10-25 propuestas) sigue siendo demasiado pequeña para concluir nada sobre umbrales, reabrir y construir backfill de verdad antes de cerrar el Hito 1; (b) si las heurísticas del auditor disparan ruido continuo en producción que afecta a la edición pública, parar y revisar antes de cumplir las 4 ediciones; (c) si el cron sufre incidentes que invalidan ediciones consecutivas (>1 edición perdida en la ventana W19-W22), prolongar la observación.
- **Estado:** vigente

### D21 — Régimen de rodaje pre-lanzamiento: ediciones revisables hasta el empuje público

- **Fecha:** 2026-04-28
- **Tema:** editorial
- **Decisión:** mientras la web no esté empujada al público activamente (sin tráfico esperado, sin anuncio, sin difusión), las ediciones publicadas son revisables libremente: formato, contenido editorial, estructura. Sin nota en `/correcciones/`, sin marca pública de *"edición corregida"*. Las ediciones funcionan como borrador en vivo. Tras el lanzamiento, vuelve a aplicar plena la regla 1 de las cinco fundacionales: el contenido editorial se congela y los errores van por la página de correcciones con traza visible.
- **Trigger del cierre del rodaje** (cualquiera de las tres dispara el cierre): (a) se compra y conecta el dominio definitivo; (b) se publica un anuncio activo (newsletter, redes, prensa, comunicación a actores citados); (c) se da la URL a alguien fuera del círculo del proyecto con intención de que la lea. En el momento que ocurra una, se hace un commit explícito (`chore: cierre del rodaje, ediciones congeladas desde aquí`) y la regla 1 fundacional vuelve a operar.
- **Por qué:** la regla 1 fundacional protege el contrato con el lector, pero hoy no hay lector real y aplicarla durante la fase de prototipo congela formato y estructura cuando todavía estamos calibrando. Iterar ahora ahorra deuda al lanzar: los lectores que vean la web post-lanzamiento la verán con formato coherente en todas las ediciones. El git log mantiene transparencia (rastro completo de versiones disponible para cualquier investigador), pero el compromiso público de inmutabilidad solo se asume cuando hay público.
- **Esta decisión supera parcialmente [D18](#d18--política-de-actualización-retroactiva-de-ediciones-publicadas)** (política retroactiva del 2026-04-27): durante el rodaje, las tres categorías que D18 separaba (contenido editorial / metadata / presentación) son todas modificables sin marca pública. D18 vuelve a aplicar plena tras el cierre del rodaje.
- **Docs afectados:** `DECISIONES.md` (D21 nuevo), `CLAUDE.md` (referencia futura cuando se cierre el rodaje), `DIARIO.md` (entrada nueva 2026-04-28). El cambio de prompt y la regeneración de W17 + W18 que motivan esta decisión se hacen en commits separados que cita esta D21.
- **Próxima revisión:** al cerrar el rodaje (trigger arriba) o si el editor decide adoptar inmutabilidad antes (a su criterio).
- **Criterio de revocación:** (a) si la facilidad para tocar ediciones publicadas lleva a perder rastro editorial útil (ej. el editor regenera y pierde una versión que tenía contexto valioso) — se restablecen pasos manuales de archivo antes de regenerar; (b) si en algún momento el editor decide que prefiere asumir inmutabilidad de tipo soft antes del lanzamiento, se cierra el rodaje voluntariamente; (c) si se comparten URLs informalmente sin que cuente como "lanzamiento" formal pero ya hay lectores, redefinir el trigger.
- **Estado:** vigente

### D22 — Trazabilidad de fuente como sexta dimensión del self-review

- **Fecha:** 2026-05-05
- **Tema:** pipeline
- **Decisión:** el revisor interno (Sonnet 4.6) puntúa de 1 a 10 una sexta dimensión, **trazabilidad**, además de las cinco existentes (reglas, rigor, balance, cobertura, claridad). Mide cuatro cosas: (a) cada cifra cita fuente identificable; (b) la fuente es primaria (BOIB, nota oficial, web institucional, cabecera original) o agregador (MSN, Google News, otro reagregador); (c) los agregadores van etiquetados visiblemente como tales en el cuerpo; (d) las estimaciones llevan etiqueta inline declarando su naturaleza (*"estimación periodística"*, *"dato oficial"*, *"orientativa"*). Penaliza fuerte cuando una cifra clave proviene solo de agregador sin marca, o cuando hay estimación sin etiqueta de naturaleza. La nueva dimensión entra en `scores`, en el aviso de Telegram cuando dispara y en los logs de self-review.
- **Por qué:** durante W17, W18 y W19 los warnings recurrentes del revisor convergieron en un patrón claro — fuentes agregadas sin marca y cifras sin origen citable. Esa señal quedaba escondida dentro de "rigor" y se mezclaba con problemas de naturaleza distinta (cifras inventadas, redondeo). Separarla en dimensión propia da resolución y permite atacar el problema con un eje específico sin contaminar la nota global de rigor. La dimensión "claridad" ha dado 9 invariablemente las tres semanas sin warnings concretos: si tras W20-W21 sigue siendo dimensión muerta, se propondrá retirarla y consolidar el sistema en cinco dimensiones (las cuatro útiles + trazabilidad).
- **Docs afectados:** `src/self_review.py` (prompt SYSTEM, JSON de salida, dim_hint del aviso), `APRENDIZAJES.md` (entrada de seguimiento sobre claridad como dimensión muerta).
- **Próxima revisión:** tras 4 ediciones publicadas con la nueva dimensión (W20-W23). Encaja con la ventana de calibración del auditor (D20) que cierra en W22 y con la revisión de la política de alerta del self-review (D17, fecha 2026-06-08).
- **Criterio de revocación:** (a) si trazabilidad da nota constante sin warning concreto durante W20-W23, fusionarla de vuelta en rigor por dimensión muerta; (b) si trazabilidad y rigor se mueven siempre juntas (correlación >0,9 en las cuatro semanas), trazabilidad no añade información y se retira; (c) si las cifras del observatorio empiezan a venir mayoritariamente de fuentes oficiales (INE, IBESTAT, BOIB, Govern), la dimensión deja de ser informativa porque casi todas las semanas darán 9-10.
- **Estado:** vigente

### D23 — Sistema de revisiones post-publicación como registro narrativo

- **Fecha:** 2026-05-05
- **Tema:** docs
- **Decisión:** se crea registro nuevo de **revisiones post-publicación** en `private/revisiones/` con archivo por revisión (`YYYY-wWW.md`) e índice raíz `REVISIONES.md`. Cada archivo sigue plantilla fija: resumen ejecutivo, diagnóstico de la edición, debate y alternativas, decisiones tomadas, cambios aplicados, seguimiento, criterios de revocación. Se crea un archivo cada vez que (a) dispare alerta del self-review y la conversación con el editor produzca cambios, (b) el editor pida lectura proactiva sin alerta y genere debate sustantivo, (c) una observación externa obligue a debatir corrección o ajuste. Revisiones triviales (typos, fix puntual sin debate) no crean archivo. Append-only: si una decisión se reabre meses después, abrir nueva revisión que cite la antigua.
- **Por qué:** durante el rodaje pre-lanzamiento (D21) cada lunes la alerta del self-review obliga a conversación crítica con el editor para decidir corregir, ajustar prompt, afinar reglas o dejar pasar. Esa conversación contiene material de mucho valor — alternativas evaluadas, motivos de cada decisión, opciones descartadas con razón explícita — que no cabe ni en `DIARIO.md` (cronológico de hitos, no narrativa larga), ni en `APRENDIZAJES.md` (tabla de sugerencias del revisor con estado, no debate humano), ni en `DECISIONES.md` (decisión canónica con criterio de revocación, no narrativa). Si dentro de tres meses una decisión envejece mal, el archivo de revisión deja entender el contexto original sin reconstruirlo de cero. Editor lo planteó explícitamente en sesión 2026-05-05 al detectar que las revisiones semanales se iban a repetir hasta que el sistema rodara solo.
- **Distinción operativa con APRENDIZAJES.md:** APRENDIZAJES guarda la lección destilada del revisor automático (1-3 líneas, estado pendiente/aplicada). REVISIONES guarda el debate humano (200-800 palabras por archivo, narrativa cerrada). Pueden cruzarse: si una revisión genera lección que se traslada al generador, esa lección entra en APRENDIZAJES como sugerencia aplicada con enlace al archivo de revisión que la originó. La revisión es el origen, APRENDIZAJES el destino destilado.
- **Docs afectados:** `REVISIONES.md` (nuevo, raíz, índice + plantilla + reglas), `private/revisiones/` (nuevo directorio), `private/revisiones/2026-w19.md` (primera revisión, narrativa de la sesión 2026-05-05), `DIARIO.md` (entrada nueva).
- **Próxima revisión:** tras W23 (4 revisiones acumuladas si todas las semanas disparan archivo) — momento de evaluar si el formato es proporcionado, si genera fricción o si aporta lo que se espera.
- **Criterio de revocación:** (a) si tras 4 semanas no hay revisión nueva (alertas que se resuelven sin debate), el formato es excesivo y se simplifica a sección dentro de APRENDIZAJES; (b) si el editor percibe fricción real en mantener el archivo cada lunes, rebajar plantilla a mínimo más pequeño; (c) si el contenido se solapa sustancialmente con APRENDIZAJES o DIARIO durante 4 semanas, plegar; (d) si las decisiones tomadas en revisiones se contradicen entre semanas sin que el editor lo perciba, la narrativa no está cumpliendo su función de memoria viva.
- **Estado:** vigente
