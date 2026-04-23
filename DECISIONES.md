# DECISIONES — Radar Vivienda Ibiza

Registro **append-only** de decisiones del proyecto. Fuente única desde 2026-04-23.

## Reglas

1. **Una fila por decisión.** Nunca editar una fila cerrada; si cambia algo, añadir una nueva decisión que la reemplace y marcar la antigua como `superada_por: DXX`.
2. **ID correlativo `D0`, `D1`, `D2`…** Sin huecos, sin reutilizar.
3. **Decisión nueva entra aquí primero.** Otros docs referencian por ID (ej. *"ver [D7]"*), no duplican el contenido.
4. **Migración histórica pendiente.** D1-D13 de `ESTUDIO-DISENO.md` y las 16 de `DECISIONES-PENDIENTES.md` se moverán aquí durante la revisión profunda post-lanzamiento (ver `ESTUDIO-GESTION-CONOCIMIENTO.md` §3.4). Hasta entonces, ambos docs siguen siendo fuentes válidas de sus decisiones propias.

## Formato de fila

```
### D{N} — {título corto}
- **Fecha:** YYYY-MM-DD
- **Tema:** {pipeline | diseno | editorial | arquitectura | docs | costes | legal | otro}
- **Decisión:** {qué se decide, en una frase}
- **Por qué:** {motivo en 1-3 líneas}
- **Docs afectados:** {lista de archivos}
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
- **Estado:** vigente

### D1 — Partir construcción del auditor en mínimo viable + iteración posterior

- **Fecha:** 2026-04-23
- **Tema:** arquitectura
- **Decisión:** la construcción del auditor IA se parte en dos bloques. **Mínimo viable (2 semanas):** auditoría ciega con Sonnet + tres heurísticas (cruce de fuentes, verbatim match, whitelist de dominios) + log público con protocolo de corrección + integración con el pipeline. Sin Opus formalizado como capa separada (se queda como fallback de extracción actual), sin página de cuarentena, sin dashboard del auditor, sin repaso mensual IA. **Iteración posterior (2-3 semanas):** Opus capa explícita, página pública `/auditor/` con métricas, página `/revision-pendiente/` navegable, repaso mensual IA de la cuarentena (capa 5bis).
- **Por qué:** el plan cerrado en [ESTUDIO-COSTES-AUDITOR.md](ESTUDIO-COSTES-AUDITOR.md) construía las 5 capas completas desde el día uno. Es ambicioso para un editor operador no-programador que está validando el producto al mismo tiempo. El mínimo viable entrega el 80 % de la transparencia (doble-ojo automático + log público + protocolo de corrección) y llega antes al punto *"funciona y lo entiendo"*. La iteración posterior añade autoresolución + vitrina + autocalibración como confort y optimización, no como defensa.
- **Docs afectados:** `ESTUDIO-COSTES-AUDITOR.md` (§10.1 nueva), `REVISION-FASE-0.5.md` (PI9 partido), `ROADMAP.md` (Fase 1 reordenada), `STATUS.md` (próximo hito).
- **Estado:** vigente

### D2 — Log del auditor público desde el día uno + protocolo formal de correcciones en 72 h

- **Fecha:** 2026-04-23
- **Tema:** arquitectura
- **Decisión:** opción (d) elegida entre cuatro alternativas evaluadas (público tal cual / retraso 30 días / privado con métricas públicas / público + protocolo). Cada propuesta lleva un campo `corrections` en el JSON del log, vacío al crearse, que crece con notas fechadas sin tocar el original. Canal de corrección: email al buzón del proyecto **+** formulario en la página de contacto. Backend del formulario: webhook que crea issue en GitHub (auditable). Notificación al editor: Telegram. Compromiso operativo: respuesta en 72 horas. Página pública `/correcciones/` con el protocolo en lenguaje llano.
- **Por qué:** coherente con la regla fundacional de transparencia radical. El auditor no crea exposición legal nueva — la noticia original ya está en internet; el log solo la estructura. El protocolo de correcciones es el escudo legal real: demuestra buena fe y due process, más defendible que retrasar o privatizar. No depende de cerrar el estudio del titular legal (RT20 + LG1): cuando ese estudio cierre, hereda el log existente sin migraciones. Riesgo residual aceptado: 72 h de exposición si entra algo difamatorio antes de que nadie lo dispute, que es el mismo riesgo de la noticia original.
- **Dependencia apuntada:** el buzón de email del proyecto queda **diferido** hasta que cierre el nombre definitivo del observatorio, y el nombre cierra cuando el editor vea la estructura final. No se crea buzón provisional. Cadena registrada en memoria del proyecto.
- **Docs afectados:** `ESTUDIO-COSTES-AUDITOR.md` (schema del log con campo `corrections`), `REVISION-FASE-0.5.md` (RT9 activa antes la página de correcciones como stub).
- **Estado:** vigente

### D3 — Whitelist de dominios por actor: V1 con actores conocidos antes del backfill

- **Fecha:** 2026-04-23
- **Tema:** pipeline
- **Decisión:** montar `data/actor_domains.yml` con 15-20 actores conocidos (Consell d'Eivissa, Govern Balear, IBAVI, ayuntamientos principales, partidos con representación, UGT, CCOO, CAEB, PIMEEF, Cáritas, Creu Roja, Sindicat de Llogaters, PAH local) antes del backfill. Refinamiento de dominios reales (subdominios, variaciones) se hace con los datos del propio backfill como calibración.
- **Por qué:** la taxonomía de actores está cerrada en 8 categorías desde el 20-abr y los actores principales de vivienda en Ibiza son un conjunto conocido y corto. El backfill no va a descubrir actores nuevos, solo dominios reales. Montar V1 ahora desbloquea el arranque del auditor mínimo. Si aparece un actor no reconocido durante el backfill: el sistema lo anota como `whitelist_miss: true` en el log, nunca bloquea publicación por sí solo (otras heurísticas compensan), el parte Telegram del lunes agrupa los misses de la semana y el repaso mensual IA propone ampliaciones que el editor firma con OK.
- **Docs afectados:** `ESTUDIO-COSTES-AUDITOR.md`, `REVISION-FASE-0.5.md` (PI9).
- **Estado:** vigente

### D4 — Tests del auditor diferidos a la tarea de cobertura del pipeline (RT5)

- **Fecha:** 2026-04-23
- **Tema:** pipeline
- **Decisión:** no montar `tests/` ni `pytest` como parte del auditor mínimo. Los tests unitarios con 3 noticias fake previstos en el plan original se difieren a RT5 (*"Tests básicos del pipeline"*), que cubrirá auditor + verify + balance + extract + rescue en un solo bloque con fixtures reales extraídas del backfill. La validación del auditor durante su construcción es empírica: corrida sobre la semana W10 (2-8 marzo 2026) como prueba antes de comprometer las 12 semanas.
- **Por qué:** montar tests ahora sin fixtures del backfill obliga a usar fakes que prueban poco. Los tests con fixtures reales son más robustos y cubren los cinco módulos de una vez. La corrida empírica sobre una semana antigua es la validación real del auditor antes del backfill grande.
- **Docs afectados:** `REVISION-FASE-0.5.md` (RT5 con alcance ampliado), `ESTUDIO-COSTES-AUDITOR.md` (plan de construcción).
- **Estado:** vigente

### D5 — Re-estudio del sistema de tiers en paralelo a la construcción del auditor

- **Fecha:** 2026-04-23
- **Tema:** arquitectura
- **Decisión:** opción (b) elegida entre dos caminos. El re-estudio profundo del sistema de tiers (RT15) se ejecuta **en paralelo** a la construcción del auditor mínimo, no como prerrequisito bloqueante. El auditor se construye con un hueco reservado en el JSON del log: `tier: { value: null, reason: "pendiente estudio", signals: {} }`. El auditor calcula y guarda las señales que ya conoce (cruce de fuentes, verbatim match ratio, whitelist hit, viabilidad), pero no las combina en un badge público hasta que el estudio de tiers cierre y defina el árbol de decisión. En ese momento, la función final lee el bloque `signals` y devuelve el color sin migrar logs antiguos.
- **Por qué:** la opción secuencial (estudio primero, auditor después) bloquearía la construcción del auditor 1-2 semanas adicionales. La paralela desbloquea: el auditor funciona igual sin la etiqueta final; los tiers son capa de presentación, no de cálculo. El log queda coherente, las señales se acumulan desde el día uno, y al cierre del estudio solo se conecta la función de lectura. RT15 deja de ser prerrequisito del auditor y pasa a ser prerrequisito solo de PI10 (visualización pública de tiers).
- **Docs afectados:** `ESTUDIO-COSTES-AUDITOR.md` (schema del log con hueco tier), `REVISION-FASE-0.5.md` (RT15 reclasificada).
- **Estado:** vigente

### D6 — Marco de tres hitos grandes como frame de trabajo de la Fase 1

- **Fecha:** 2026-04-23
- **Tema:** docs
- **Decisión:** el trabajo de la Fase 1 se organiza en tres hitos grandes donde el editor decide los puntos de entrada y de cierre, y Claude lleva los puntos pequeños dentro de cada hito. **Hito 1:** auditor mínimo viable publicado con una edición real. **Hito 2:** sistema de tiers cerrado e integrado. **Hito 3:** titular legal resuelto. El resto de las 34 tareas de la Revisión Fase 0.5 queda en cola; no se abren en paralelo. Al cerrar un hito, el editor elige el siguiente.
- **Por qué:** el editor expresó 2026-04-23 *"no siento que llevo las riendas"* con 34 tareas abiertas simultáneamente, cada una con ramificaciones en las demás. El marco de tres hitos reduce la carga cognitiva: fijar hitos grandes y delegar los pequeños dentro. Dentro de cada hito, Claude propone y el editor da OK por bloque, no por decisión unitaria. Si algo grande cambia de rumbo dentro de un hito, Claude para y pregunta.
- **Docs afectados:** `STATUS.md` (marco de trabajo + próximo hito), `ROADMAP.md` (Fase 1).
- **Estado:** vigente

### D7 — Rastro de decisiones pequeñas en DIARIO + resumen al `/cierre`

- **Fecha:** 2026-04-23
- **Tema:** docs
- **Decisión:** cuando Claude tome una decisión autónoma dentro de un hito (nombre de una función, orden de heurísticas, formato de un campo, elección entre dos alternativas equivalentes), la anota en `DIARIO.md` como línea corta: fecha, qué decidió, por qué. Formato integrado en las entradas existentes, no en documento nuevo. Al cierre de sesión o bloque (comando `/cierre`), Claude entrega al editor un resumen agrupado *"decisiones pequeñas de esta sesión"* con la lista en lenguaje llano. El editor puede: dejar correr (no hacer nada, quedan marcadas), revertir una (*"la decisión X no me encaja"*, vuelta atrás por git), o pedir detalle (*"por qué decidiste X"*).
- **Por qué:** el editor pidió 2026-04-23 poder seguir el rastro del proceso y revertir si algo no encaja. El diario + git ya dan reversibilidad; solo faltaba el hábito de anotación y el resumen al cierre. Mantiene autonomía de ejecución dentro del hito sin perder control editorial.
- **Docs afectados:** `DIARIO.md` (convención aplicada desde esta entrada).
- **Estado:** vigente

### D8 — Experimento APRENDIZAJE.md: log de feedback formativo al cierre (solo-ibiza)

- **Fecha:** 2026-04-23
- **Tema:** docs
- **Decisión:** introducir un archivo `APRENDIZAJE.md` en la raíz del proyecto como log experimental de feedback formativo sobre cómo el editor desarrolla el proyecto. El Paso 6 del comando `/cierre` evalúa cada sesión si hay algo concreto que anotar (decisiones, alcance, priorización, comunicación, docs, coste, proceso, verificación); si no hay, reporta *"sin feedback hoy"* y no añade entrada. **Alcance: solo este proyecto**, no global ni plantilla. Incluye sección *"Cómo desactivar"* con dos pasos (~30 seg).
- **Por qué:** el editor pidió un loop de aprendizaje sobre su propia práctica sin comprometerse a mantenerlo si no aporta. La propuesta inicial era global (cruza proyectos) con replicación a los 4 proyectos del usuario; el editor la redujo a este proyecto y exigió reversibilidad explícita antes de aprobar. Cumple alcance conservador (memoria `feedback_alcance_proyecto.md`) y principio de no escalar sin demanda orgánica (memoria `feedback_esperar_demanda_organica.md`).
- **Docs afectados:** `APRENDIZAJE.md` (nuevo), `.claude/commands/cierre.md` (Paso 6 añadido), `CLAUDE.md` (mención en sección *"Cierre de sesión"*), `STATUS.md` (lista de docs vivos +1). Revertidos en la misma sesión: `~/.claude/APRENDIZAJE.md`, `~/.claude/CLAUDE.md` sección *"Aprendizaje transversal"*, y `~/Documents/GitHub/.claude-template/commands/cierre.template.md` Paso 6.
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
- **Estado:** vigente
