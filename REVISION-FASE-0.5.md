# Revisión Fase 0.5 — auditoría fundacional previa a construcción

**Fecha apertura:** 2026-04-21
**Contexto:** antes de entrar en diseño visual y desarrollo de la web, el editor abre una fase de revisión crítica del concepto completo (método editorial, fuentes, pipeline, UX, marca, legal, financiación). Objetivo: asegurarse de que los cimientos son sólidos antes de invertir en capas de implementación.
**Método de trabajo:** Claude lanza las tareas una a una, en el orden de prioridad de abajo. Editor responde. Cuando se cierra una, se marca ✅ y se pasa a la siguiente. Si una tarea destapa decisión nueva que afecta a docs maestros, se actualizan y se registra en `DIARIO.md`.
**Estado de la web:** congelada en Paso 1 del prototipo (4 páginas HTML). No se toca el diseño visual hasta cerrar esta fase.

---

## Reglas permanentes fijadas por el editor (aplicar siempre en este proyecto)

1. **Vigilar barreras pasadas de rosca.** Cada filtro, check o regla nueva debe aportar valor real. Si complica sin aportar, se simplifica o se descarta. Si dudo, pregunto.
2. **Badges y decisiones visibles al público se explican en lenguaje llano**, no técnico. Y son ajustables sin refactor — tratadas como factor crítico de la plataforma.
3. **Pregunto antes de commit** cuando el cambio no estaba ya validado explícitamente por el editor.
4. **Códigos internos (PI9, ED5, etc.) fuera de la conversación.** En conversación hablo con nombres de cosa. Los códigos solo viven dentro de este documento.
5. **Rol del editor = operador, no revisor experto.** Estimación: 15-45 min/semana reactivos. No está obligado a revisar propuestas. El sistema (tiers + cuarentena + sanity check externo) absorbe la validación; el editor responde a emails, mira la web los lunes 3 min, y escala cuando algo excepcional llega.

---

## Decisiones cerradas durante la revisión

### 2026-04-21 · Backfill de 12 semanas + Camino A + auditor IA
- **Backfill retroactivo de 12 semanas (W06-W17, ~2 feb → 20 abr)** con Google News + RSS nativos + BOIB (si factible). Motivo: tener 3 meses de corpus real para validar criterios editoriales con evidencia, no con hipótesis.
- **Camino A confirmado:** las 12 ediciones retroactivas se publican con fecha real + banner *"procesada a posteriori bajo modelo documental"*. Refuerza SEO de lanzamiento, ofrece contexto al público, y la arquitectura del schema (state + proposals_history append-only + PI3 grafo de evolución) hace defendible mostrar cambios de posición de actores como linaje, no como "pillada".
- **Sistema de auditoría IA de 5 capas** en lugar de revisión humana exhaustiva:
  - Capa 1: extracción primaria (Haiku).
  - Capa 2: auditoría ciega independiente (Sonnet).
  - Capa 3: comparador determinístico Python + verify.py (5 checks: URL 200, dominio-actor, verbatim en HTML, fecha coherente, Wayback archive).
  - Capa 4: arbitraje Opus solo para discrepancias (~15%).
  - Capa 5: editor revisa solo lo flagged. ~~Muestreo aleatorio 10% de auto-aprobadas~~ **eliminado el 2026-04-23** (rompía la regla fundacional).
  - **Capa 5bis (añadida 2026-04-23):** repaso IA mensual de cuarentena. Opus lee cuarentena + logs + whitelist + umbrales y propone ajustes YAML; editor firma con OK por Telegram en 5 min. ~0,4 €/mes.
- **Heurísticas sin IA:** cross-source confirmation, single-source penalty, verbatim substring match obligatorio, domain-actor whitelist, viability sanity checks.
- **Log de auditoría completo** (`data/audit/YYYY-wWW/{proposal_id}.json`) con todas las capas, timestamps y decisiones — transparencia radical como escudo legal.
- **Coste cerrado:** ~~~3,50 € totales~~ **corregido 2026-04-23**: backfill 12 semanas ~5,4 € (one-shot, incluye generate retro Opus + self-review), régimen estable ~2,4 €/mes desde mes 4, meses 1-3 de arranque ~5,7 €/mes con auditoría Opus mensual de calibración. Detalle completo en [`ESTUDIO-COSTES-AUDITOR.md`](ESTUDIO-COSTES-AUDITOR.md).
- **Tiempo editor estimado:** ~4 h (antes 15 h).

### 2026-04-21 · Ajustes al auditor IA y al presupuesto
- **Verbatim match diferenciado por `statement_type`**: si la propuesta contiene cita textual entrecomillada (`quote`), el substring match en el HTML es obligatorio. Si es reporte paráfrasico del periodista (`reported`), se relaja a (a) nombre del actor en página + (b) términos clave de la propuesta presentes + (c) sin contradicción lógica con el texto. Motivo: exigir literal siempre rechazaba propuestas legítimas reportadas en estilo indirecto.
- **Dos URLs que cubren la misma propuesta**: se guarda una `url_source` principal + lista `url_corroboration`. Jerarquía para elegir principal: (1) URL del propio actor, (2) diario local con cita entrecomillada, (3) empate → la más antigua. Las demás quedan visibles como *"también cubierto por:"*. Beneficio: si la principal cae, la red de corroboración es el respaldo natural.
- **Tope duro mensual subido a 50 €** (antes 20). Blando sigue en 12 €. Margen para backfill + experimentación sin bloqueos. Actualizado en `src/costs.py` v3.

### 2026-04-21 · Sistema de tiers + cuarentena + rol operador (reemplaza modo entrenamiento)
El editor expresa preocupación honesta: *"no se si mi conocimiento del tema puede llegar a afectar seriamente al proyecto"*. Tras explorar alternativas, se descarta el modo entrenamiento de 4 semanas (ED5 inicialmente planteada) por ser incompatible con el rol realista del editor. Se aprueban tres mecanismos complementarios que hacen el proyecto independiente de la experticia del editor:

**Plan A · Tiers de confianza públicos (APROBADO con condiciones).**
Cada propuesta lleva badge visible calculado por el auditor IA:
- 🟢 Alta: dos capas IA coinciden + verify OK + 2+ fuentes. Publicada sin aviso.
- 🟡 Media: dos capas IA coinciden + verify OK + fuente única. Nota: *"Fuente única. Si tienes información, ayúdanos"*.
- 🟠 Baja: Opus dudó o verify con warnings menores. Nota prominente: *"Baja confianza. Verificación pendiente"*.
- 🔴 No publicada: va a cuarentena.

Condiciones del editor:
- Criterios de cada badge explicados al público en lenguaje llano (regla permanente 2).
- Los umbrales son **ajustables** y se tratan como factor crítico de plataforma.

**Plan B · Cuarentena pública (APROBADO).**
Página `/revision-pendiente/` visible con las propuestas 🔴 no publicadas. Copy público: *"Detectadas pero no verificadas con rigor suficiente. Esperan (a) segunda fuente, (b) lector que conozca el caso, o (c) archivo como 'no verificada' tras 60 días"*. La duda se publica, no se esconde. Alineado con radical transparency.

**Plan C · Rol del editor como operador, no revisor (APROBADO).**
El editor no revisa propuestas. Su compromiso asumible:
- **Una mirada visual de 3 min los lunes** después de publicar (la Telegram alert ayuda).
- **Responder emails a /contacto/ en 48-72 h** (estimación 0-3/semana).
- **Escalar cuando algo excepcional llegue** (impugnación, medio, umbral disparado).
Total: 15-45 min/semana reactivos.

**Plan externo complementario · Sanity check pre-lanzamiento (pendiente de contratar).**
1-2 h pagadas a periodista local o académico UIB auditan 30 propuestas del backfill antes de publicar. 50-100 €. Registrado como tarea.

### 2026-04-21 · Alerta Telegram de lunes — resumen corto + alertas proactivas
Mezcla de A+C del diseño discutido. `_build_summary` en `src/report.py` enriquecido para emitir:
- Título de edición + URL pública en GitHub Pages.
- Conteo de propuestas extraídas + lista de actores (cap 6, +N suffix).
- Línea de pipeline OK + gasto mes + capa.
- Bloque `⚠ Atención esta semana` condicional (solo aparece si hay cuarentena activa o alerta de balance). Se alimenta de `data/balance_status.json` y `data/quarantine.json` — los módulos upstream se conectan cuando existan (tarea pendiente). Si no hay datos, bloque invisible.

Horario: 07:15 Madrid (al terminar pipeline). Canal: Telegram. Email queda anotado como tarea futura.

### 2026-04-21 · Orden de ejecución reordenado
Antes de retomar ED1 (criterios de admisión), se ejecutan primero las tareas que producen la materia prima y la infraestructura para validar con datos reales:
1. **PI2-A** (append-only inmediato).
2. **PI2-B** (backfill 12 semanas).
3. **PI9** (sistema auditoría IA).
4. **ED1** (criterios validados con corpus real).
5. Resto de P0/P1 en orden original.

### 2026-04-23 · Partición del auditor + log opción (d) + marco de tres hitos grandes

Sesión de rediseño del plan del auditor con el editor tras abrir el arranque de PI9. El editor expresa que no siente llevar las riendas con 34 tareas abiertas en paralelo y pide honestidad sobre el alcance. Resultado: reencuadre de la Fase 1 bajo un marco de tres hitos grandes, partición del auditor y cierre de decisiones de protocolo.

- **Partición del auditor en mínimo viable + iteración** ([D1](DECISIONES.md)). PI9 se parte en PI9-MVP (2 sem: capa 2 ciega + heurísticas + log con correcciones + integración, ver sección §10.0 del estudio de costes) y PI9-Iteración (2-3 sem: Opus formalizado + cuarentena + dashboard + capa 5bis). Reduce escalada de complejidad; entrega el 80 % de la transparencia en el MVP.
- **Log público desde día uno + protocolo formal de correcciones en 72 h** ([D2](DECISIONES.md)). Opción (d) elegida entre cuatro evaluadas. Campo `corrections` append-only en cada JSON, canales email + formulario, backend webhook → issue GitHub → notificación Telegram, página pública `/correcciones/`. El email queda **diferido hasta cierre del nombre** (cadena apuntada en memoria del proyecto). Alerta legal activa: el estudio del titular (RT20/LG1) sigue abierto; cuando cierre, hereda el log existente sin migración.
- **Whitelist V1 antes del backfill** ([D3](DECISIONES.md)). 15-20 actores conocidos curados ya, refinamiento de dominios reales con los datos del backfill. Misses no bloquean publicación, repaso mensual IA propone ampliaciones.
- **Tests del auditor diferidos a RT5** ([D4](DECISIONES.md)). Cobertura en un solo bloque con fixtures reales del backfill. Validación durante construcción del auditor = prueba empírica sobre W10.
- **Re-estudio del sistema de tiers en paralelo** ([D5](DECISIONES.md)). RT15 deja de bloquear el auditor. El auditor MVP escribe `signals` en el log con hueco `tier: { value: null, reason: "pendiente estudio", signals: {...} }`; cuando RT15 cierre, la función `compute_tier()` lee del bloque sin migrar logs antiguos. RT15 pasa a bloquear solo PI10 (visualización pública).
- **Marco de tres hitos grandes como frame de la Fase 1** ([D6](DECISIONES.md)). Hito 1: auditor MVP publicado con una edición real. Hito 2: sistema de tiers cerrado e integrado (en paralelo). Hito 3: titular legal resuelto (en paralelo, bloquea empuje público). Las 34 tareas restantes quedan en cola; no se abren en paralelo.
- **Rastro de decisiones pequeñas** ([D7](DECISIONES.md)). Anotadas en `DIARIO.md` como líneas cortas; resumen al `/cierre` con opción de revertir por git.

Memoria del asistente actualizada con `feedback_vigilancia_legal_activa.md` (alerta legal como conducta continua), `idea_version_premium.md` (monetización como opción abierta) y `nombre_proyecto.md` (cadena de dependencias email ← nombre ← estructura final).

---

## Cómo leer esta lista

Cada tarea tiene:
- **Código** (ej. `ED1`, `FU2`) para referencias cruzadas y commits.
- **Resumen** de la pregunta/decisión pendiente.
- **Estado**: ⏳ pendiente · 🔄 en discusión · ✅ cerrada · ⏸ pausada.
- **Salida esperada**: qué debe quedar escrito/decidido/implementado al cerrarla.

Orden: **P-1 (hallazgos de la revisión técnica, antes de relanzar)** → P0 (fundacional, bloquea lo demás) → P1 (estructural) → P2 (UX) → P3 (operacional) → P4 (identidad/negocio) → P5 (misc).

---

## P-1 — Hallazgos nuevos de la revisión técnica 2026-04-21 noche (antes del relanzamiento)

Tareas abiertas tras el barrido de coherencia profundo que el editor pidió el 2026-04-21 noche. Todas son bloqueantes de algún aspecto del relanzamiento o del backfill; por eso van delante del resto.

### RT1 · Backfill empírico — prototipar 1 semana antes de comprometer 12 ⏳
El plan del backfill (12 semanas W06-W17, Camino A) está estimado en ~3,50 € de API y ~4 h de trabajo del editor. Esa estimación asume reconstrucción limpia de prensa local con Google News operadores `after:/before:`, RSS nativos y Wayback. En la práctica: los RSS locales devuelven vacío, Google News cambia resultados según contexto del usuario, Wayback no siempre archivó la URL exacta, y los diarios locales reorganizan URLs cada 6-12 meses.

**Riesgo:** comprometer 12 semanas a ciegas y descubrir a mitad del proceso que las semanas W06-W10 tienen cobertura muy pobre, forzando a descartarlas o bajar el estándar de verificación.

**Acción:** ejecutar el backfill de **una sola semana antigua** (W10, 2-8 marzo 2026) como prueba empírica. Medir: (a) % de URLs que siguen vivas y responden 200; (b) % de URLs con verbatim recuperable; (c) % de propuestas que pasan el verify; (d) tiempo real de revisión humana; (e) coste API real. Con esos 5 datos se decide si el backfill final cubre 12 semanas, 6, o solo las últimas 4. La decisión vuelve a abrirse tras la prueba.

**Salida esperada:** informe corto en `private/estudios/backfill-prueba-W10.md` con los 5 números + recomendación al editor + ajuste del plan en `CONTENIDO-RETROACTIVO.md`.

**Medición adicional para cerrar el estudio de tiers (ver [`ESTUDIO-TIERS.md §3.8`](ESTUDIO-TIERS.md)):** sobre las 3-5 propuestas extraídas de la W10, calcular la distribución preliminar de tiers 🟢/🟡/🟠/🔴 y validar que encaja con la expectativa 70/20/8/2. Si la distribución real difiere >20 puntos del target, los umbrales del árbol necesitan ajuste antes del backfill grande. Resultados se anotan en el mismo informe.

**Prioridad de ejecución:** ANTES del backfill grande.

### RT2 · Rol editor operador vs muestreo 10% — resolver contradicción ✅ CERRADA 2026-04-23

**Decisión del editor (2026-04-23):** opción 2 — **eliminar el muestreo humano del 10 %**. Coherente con la regla fundacional (editor opera, no audita). La red de seguridad la cubren:

- Capas 2-4 del auditor IA (ciego Sonnet + comparador determinista + heurísticas + arbitraje Opus).
- Log público de auditoría por propuesta en `data/audit/`.
- Cuarentena pública `/revision-pendiente/`.
- Formulario externo *"¿falta algo?"* de escrutinio ciudadano.
- **Capa 5bis nueva:** repaso IA mensual de cuarentena por Opus, que propone ajustes al sistema (umbrales, whitelist, prompts) que el editor firma con OK en 5 min.

**Descartadas:** opción 1 (rompe la regla) y opción 3 (200-600 €/año sin aportar cuando el sistema IA ya cubre la red). La opción 3 queda en reserva solo si a los 3-6 meses la auditoría trimestral detecta tasa de error silencioso > 5 %.

Estudio completo en [`ESTUDIO-COSTES-AUDITOR.md`](ESTUDIO-COSTES-AUDITOR.md) (cierre 2026-04-23). Entrada de diario: [DIARIO.md 2026-04-23 (tarde)](DIARIO.md).

### RT3 · Tiers de confianza — validar UX con los dos públicos ⏳
El sistema de tiers públicos 🟢/🟡/🟠 con cuarentena 🔴 fue aprobado para reemplazar el modo entrenamiento. La intuición: el periodista entiende lo que significa "fuente única" y lo valora; el primer visitante (temporero, ciudadano) puede no entender el código de colores o directamente percibirlo como ruido.

El proyecto tiene dos públicos declarados en `DISENO-WEB.md`: primer visitante vs profesional recurrente. Los tiers sirven al segundo y potencialmente confunden al primero. No hay evidencia de cómo se percibe realmente porque no se ha probado.

**Acción:** antes de lanzar los tiers en abierto, ejecutar el test definido en [`ESTUDIO-TIERS.md §10`](ESTUDIO-TIERS.md) — n = 5 (2 periodistas + 2 temporeros + 1 ciudadano control), versión A (tiers visibles a todos) vs versión B (toggle), 6 preguntas neutras, métricas de comprensión a 5 segundos + efecto en la confianza + preferencia de visibilidad. Tiempo total ~3 h (1,5 h campo + 30 min análisis + 30 min ajustes de copy). Salida: decisión de UI y ajustes a §5 de ese estudio. **Depende del editor con su red personal — el asistente no ejecuta esto.**

**Salida esperada:** notas cortas del test + decisión de UI (tier visible para todos / solo para lector que elige "modo profesional" / tier invisible pero filtro silencioso en el backend) + copy ajustado al resultado.

### RT4 · Techo de cobertura + banner de limitaciones hasta datos propios ⏳
El PLAN estratégico reconoce que el observatorio es "refrito de prensa" y que los datos propios (Vía A agregación oficial + Vía B crowd-sourcing de precios) son el diferencial que convertirá el proyecto en fuente primaria. Hasta que esas vías estén operativas (previsto Fase 2, 3-6 meses tras el relanzamiento), el proyecto sigue siendo lectura estructurada de prensa local, con un techo de impacto limitado.

El modelo documental resuelve dos problemas reales (alucinación del LLM, sesgo en la generación de propuestas) pero **no** resuelve el techo de cobertura ni el problema de valor diferencial. Si el copy público del relanzamiento vende "observatorio de referencia" y el producto real es "lectura estructurada de prensa local con tracker de propuestas", el lector profesional nota el gap a la segunda semana.

**Acción en dos partes:**

1. **Banner visible en fase de rodaje.** Copy estable que reconozca honestamente dónde estamos: *"Observatorio en fase de rodaje. N ediciones documentadas. Próximo hito: observatorio de precios con datos propios (agregación oficial + crowd-sourcing ciudadano), previsto para \[fecha\]. Transparencia radical: `/metodologia/` y `/balance/`"*. Se mantiene visible hasta que exista la primera publicación con datos propios.

2. **Plan de datos propios priorizado.** Revisar el cronograma de Fase 2 en PLAN.md y decidir si se adelanta al menos la Vía A (agregación de informes públicos Idealista, Fotocasa, INE, IBESTAT) al mismo tiempo que el relanzamiento. La Vía A es scraping ético de fuentes oficiales, no de portales. Coste 0 € si se hace con scripts sencillos. Tiempo de montaje: 2-3 días.

**Salida esperada:** (a) bloque de banner en `_layouts/` con copy cerrado; (b) decisión sobre si Vía A entra en Fase 0 o se queda en Fase 2; (c) actualización de `PLAN.md` con el cronograma resultante.

### RT5 · Tests básicos del pipeline ⏳
Hoy no hay carpeta `tests/` y no hay ningún test automatizado. Un cambio en `classify.py` puede romper `extract.py` sin que nada lo avise hasta que falle el cron del lunes. Con el pipeline ya en producción (W17 publicada) y el backfill por delante (reprocesar 12 semanas de datos), el coste de un fallo silencioso sube.

**Acción mínima (5-6 h):**
- `tests/fixtures/` con 3 noticias reales: una con propuesta formal, una con propuesta en movimiento, una sin propuesta.
- Mock de la API de Anthropic que devuelva respuestas deterministas.
- Tests end-to-end: `tests/test_pipeline.py` que verifica que `ingest → classify → extract → rescue → generate → verify` produce un markdown válido sin llamar a la API real.
- Tests específicos: `tests/test_verify.py` (URL rota bloquea, verbo prohibido bloquea, propuesta sin actor bloquea), `tests/test_rescue.py` (criterios duros), `tests/test_balance.py` (ventanas correctas, silencio con N<20).

**Salida esperada:** carpeta `tests/` con cobertura mínima + entrada en `.github/workflows/` para ejecutar tests en cada PR.

### RT6 · Balance — rediseño completo tras 3 meses de datos ⏳
El fix aplicado hoy en `src/balance.py` es un parche temporal: silencia las alertas mientras el histórico sea menor de 20 propuestas. La regla 4 vinculante del observatorio es *"si un bloque supera 50% durante dos trimestres consecutivos"*. Eso requiere comparar la ventana actual con la anterior, no solo mirar la actual.

**Acción diferida a 3 meses:** cuando el histórico tenga al menos 3 meses de datos (esperado julio 2026), rediseñar `balance.py` para:
1. Guardar snapshot semanal del balance en `data/balance_snapshots/YYYY-wWW.json`.
2. Comparar ventana actual (últimos 90d) con anterior (90d previos).
3. Disparar alerta solo si concentración >50% **y** tendencia sostenida.
4. Añadir test determinista con datos sintéticos de 2 trimestres.

**Salida esperada:** rediseño implementado, snapshots acumulados desde hoy, alerta fiable desde el 3er mes post-relanzamiento.

### RT7 · `build_index.py` — adaptar al schema documental ✅
**Cerrada 2026-04-21 noche** como parte del barrido de esta revisión técnica. El regenerador de la home buscaba campos del modelo antiguo (`Actor responsable`, `Precedente`, `Coste`, `Primer paso`, `Por qué ahora`) que no existen en las ediciones documentales. Resultado: cards vacíos en la home. Actualizado el parser para el schema nuevo (`Actor que la propone`, `Estado`, `Horizonte`, `Actor que tendría que ejecutarla`) + copy de la home reescrito para no vender "propuestas accionables" del modelo antiguo.

### RT8 · Banner de "página en reescritura" en `/acerca/` ✅ CERRADA 2026-04-29
Decisión tomada 2026-04-29: split `/acerca/` + `/metodo/` (opción recomendada). `/metodo/` creada con contenido completo (pipeline, modelos, taxonomía, sesgos) en RT9. `/acerca/` reescrita como página de identidad breve: qué es el proyecto, fase de rodaje, quién edita, licencias, financiación, contacto. Enlaza explícitamente a `/metodo/` y `/politica-editorial/` para el detalle técnico y editorial. Ambas páginas enlazadas desde el pie de todas las páginas.

### RT9 · Prototipo de páginas mínimas que las reglas duras exigen ✅ CERRADA PARCIAL 2026-04-29
Las 5 reglas duras del observatorio asumen que existen tres páginas públicas: `/politica-editorial/` (texto de las reglas), `/metodologia/` (cómo funciona el pipeline y sesgos declarados), `/correcciones/` (log público de enmiendas). Hoy ninguna existe. El pipeline emite ediciones que hacen afirmaciones editoriales fuertes ("las 5 reglas duras", "balance auditado", "correcciones públicas") sin soporte público.

**Cerrada 2026-04-29 (huecos críticos).** Creadas [`docs/politica-editorial.md`](docs/politica-editorial.md) (`/politica-editorial/`) y [`docs/metodo.md`](docs/metodo.md) (`/metodo/`), ambas con contenido completo: reglas fundacionales en lenguaje público, pipeline semanal, modelos, taxonomía de actores, sesgos declarados y qué no hace el observatorio. Enlazadas desde `/acerca/` y desde el pie de todas las páginas. `/correcciones/` ya existía desde 2026-04-23. Las tres páginas exigidas por las reglas duras están operativas.

**Pendiente menor:** las páginas diferidas referenciadas en el prototipo (`/estado/`, `/costes/`, `/auditoria/`, `/datos-abiertos/`) siguen como tareas futuras — no son exigidas por las reglas duras.

### RT11 · Copy y tono de la home — decisión editorial en la etapa de Diseño ⏳
El fix mecánico aplicado en el barrido 2026-04-21 ya quita el copy del modelo antiguo de la home (cambios en `build_index.py`: *"propuestas accionables con precedente"* → *"propuestas documentadas en circulación"*, bloque final reescrito para reflejar que el observatorio no genera propuestas propias). Queda pendiente la **decisión editorial** sobre el tono, jerarquía visual, qué se ve above-the-fold, cómo se comunica a los dos públicos (primer visitante vs profesional recurrente) y cómo se integra con los tiers de confianza (RT3).

Esa decisión se toma cuando se reanude la etapa de Diseño, tras cerrar los hallazgos técnicos (RT1-RT10). Depende de:
- Resultado del test de usabilidad con los dos públicos (RT3).
- Qué copy final tienen los tiers y la cuarentena cuando existan.
- Si la Vía A de precios (RT12) entra antes del relanzamiento; en ese caso la home debe darle espacio.

**Salida esperada:** copy final de la home cerrado, componentes del dashboard revisados contra las decisiones D1-D13 del estudio de diseño, `build_index.py` emite el copy definitivo.

### RT13 · Regla fundacional — automatización máxima + niveles de veracidad públicos ✅ CERRADA 2026-04-29 [FILOSOFÍA]
**Decisión del editor 2026-04-21 noche:** la filosofía del proyecto se fija como **automatización máxima con transparencia radical sobre niveles de veracidad**. El editor opera, no audita contenido. El sistema se audita a sí mismo mediante auditor IA de 5 capas + tiers públicos 🟢🟡🟠🔴 + cuarentena + log de auditoría abierto.

**Cerrada 2026-04-29.** La regla está documentada en dos sitios: (a) [`CLAUDE.md#regla-complementaria`](CLAUDE.md) — regla interna del proyecto con toda la especificación técnica; (b) [`docs/politica-editorial.md`](docs/politica-editorial.md) — versión pública en lenguaje llano bajo el título *"Automatización máxima con transparencia sobre niveles de fiabilidad"*, con el rol del editor como operador y el mecanismo de escalado. Enlazada desde el pie de todas las páginas.

### RT14 · Estudio preciso de costes del auditor IA ✅ CERRADA 2026-04-23

Entregable: [`ESTUDIO-COSTES-AUDITOR.md`](ESTUDIO-COSTES-AUDITOR.md) cerrado 2026-04-23 con 14 secciones + tabla por capa + proyección mensual + plan de implementación en 4 semanas.

**Conclusiones principales:**
- Delta neto del auditor sobre el pipeline existente: +0,2 €/mes en régimen estable. No hay presión presupuestaria que limite su diseño.
- Régimen estable desde mes 4: ~2,4 €/mes total pipeline + auditor.
- Meses 1-3 post-lanzamiento con auditoría Opus mensual de calibración: ~5,7 €/mes.
- Backfill 12 semanas one-shot: ~5,4 € (corregido desde la estimación inicial de 3,5 € — no incluía generate retro ni self-review).
- Mes pico realista (mayo 2026 con backfill + auditoría mensual + re-bench): ~10,1 €/mes, capa 🟠 naranja, sin cruce de tope blando (12 €).

**Decisiones derivadas cerradas el mismo 2026-04-23:** eliminar muestreo 10 % (cierra RT2), añadir capa 5bis IA, Telegram consolidado, reportes escalonados mensual→trimestral→semestral, revisiones de cadencia al mes 4 y mes 7. Detalle en el estudio, entrada cronológica en [DIARIO.md 2026-04-23 (tarde)](DIARIO.md).

**Siguiente paso:** construir `src/audit.py` (semana 1 del plan del estudio).

### RT15 · Re-estudio profundo del sistema de tiers de confianza ✅ CERRADA 2026-04-23

**Entregable:** [`ESTUDIO-TIERS.md`](ESTUDIO-TIERS.md), 11 secciones redactadas + §11.6 con las 5 decisiones cerradas por el editor ([D9](DECISIONES.md)).

**Resumen del cierre:** árbol determinista de 6 pasos (bloqueantes → techos → 🟢 → 🟡 → 🟠 → default 🟠), 10 señales computables del auditor, umbrales ajustables en `data/tiers.yml` con política de congelar, copy público llano (tabla de palabras prohibidas con traducciones), interacción con cuarentena (tres caminos de promoción, archivo a 60 días), historia del tier con `tier.history[]` append-only, plan de test con n=5, mockups textuales para ficha/lista/cuarentena/dashboard/home.

**Único bloque dependiente de datos:** §8.5 (medición empírica del sesgo por tipo de actor). Se resuelve con el backfill de 12 semanas ejecutado (ficha RT25 de esta revisión). Si se confirma el sesgo, activa mitigación M1 (relajación del techo de fuente única solo en 4 categorías de actor) escrita en `data/tiers.yml`.

**Desbloqueos:** PI10 (sistema de tiers público) listo para construirse sobre `src/tiers.py` + `data/tiers.yml`. El auditor mínimo viable sigue escribiendo `signals` en el log, y `compute_tier()` real se conecta ahora sin migrar logs antiguos.

**Preguntas originales del primer pase (ahora todas cerradas en §11.6 del estudio):**
- **Cálculo.** ¿Qué combinaciones de señales del auditor asignan cada color exactamente? Árbol de decisión determinista, no heurística.
- **Umbrales ajustables.** ¿Dónde viven las reglas en el código? ¿Cómo se cambian sin refactor? ¿Qué pasa si cambian retroactivamente con el corpus existente?
- **Comunicación al público en llano.** Copy para cada tier ("alta confianza, dos fuentes coincidentes" vs "fuente única, si conoces el caso ayúdanos"). Test con lector no técnico.
- **Dos públicos.** ¿Se muestran a todos o solo a lector en modo profesional? ¿Se puede filtrar por tier?
- **Interacción con cuarentena.** 🔴 va a cuarentena pero puede promoverse si aparece segunda fuente. ¿Cómo se comunica esa historia al lector?
- **Historia del tier.** Un tier puede cambiar con el tiempo (una propuesta 🟡 se vuelve 🟢 cuando aparece corroboración). ¿Se muestra esa evolución? ¿Cómo?
- **Sesgo de tier por tipo de actor.** Verificar empíricamente si el sistema asigna sistemáticamente peor tier a ciertos actores (colectivos ciudadanos con menos cobertura mediática). Si sí, mitigar.

**Salida:** documento `ESTUDIO-TIERS.md` con árbol de decisión cerrado + copy público ejemplo + mockups de cómo se ven en ficha de propuesta + tabla + dashboard + plan de test con usuarios (complementa RT3). Antes de implementar PI10.

### RT16 · Experimento de Claude Design — estudio en fase de Diseño ⏳ [MEDIA]
El editor probó Claude Design 2026-04-21 y generó un experimento de exploración visual. **Entregado el 2026-04-22** y archivado en [`private/claude-design-experiment/`](../../private/claude-design-experiment/) con README propio explicando su estado.

**Condiciones explícitas del editor:** el paquete es un experimento, usa datos antiguos (pre-modelo documental), no tiene en cuenta ninguna de las decisiones ya cerradas (D1-D13 del estudio de diseño, taxonomía de actores, 5 reglas duras, regla complementaria de automatización, nombre del wordmark `radar))ibiza_vivienda`, etc.). **No es referencia de nada hasta que el editor lo indique explícitamente.** Se estudia únicamente en la fase de Diseño (Fase 4 del roadmap V2).

**Proceso cuando toque:**
1. Claude Code abre el paquete.
2. Compara contra [`ESTUDIO-DISENO.md`](ESTUDIO-DISENO.md) (D1-D13 cerradas) y contra todas las decisiones posteriores.
3. Identifica qué elementos visuales pueden incorporarse como evolución sin contradecir las reglas fijadas.
4. Marca explícitamente qué del experimento no encaja y por qué (taxonomía cerrada, partidos en gris neutro, modelo documental vs propuestas del observatorio, etc.).
5. Presenta propuesta de integración para decisión del editor.

**Salida:** documento comparativo + propuesta de integración + actualización del estudio de diseño con el conjunto final + ajuste de los 9 componentes si aplica.

### RT17 · Navegación exhaustiva mobile-first ⏳ [ALTA]
Con 15+ páginas nuevas, la navegación es crítica. El editor pide explícitamente 2026-04-21 noche que el usuario pueda cruzar secciones con soltura y criterio. Elementos a diseñar:
- **Top-nav con subniveles por sección** (menús desplegables con las sub-páginas de cada área).
- **Sidebars contextuales** en páginas con muchos sub-apartados (método, política editorial, metodología, datos abiertos) para que el lector tenga la estructura siempre presente.
- **Sitemap visual siempre accesible** — como elemento de navegación global, no una página solitaria. Puede ser un modal invocable desde cualquier página, o un footer expandido. La idea es que nunca se pierda el mapa completo.
- **Breadcrumbs** en cada página interna.
- **Internal linking denso:** edición ↔ actor ↔ propuesta ↔ explica ↔ glosario ↔ edición, con links contextuales dentro del cuerpo.
- **CTAs de exploración al final de cada vista** (no solo al inicio).
- **Mobile-first:** todas las decisiones de navegación se prueban primero en móvil. Menú hamburguesa con subniveles, sitemap modal, sidebars plegables.

**Salida:** documento `NAVEGACION.md` propio (no sub-sección de otro) con mapa de enlaces, patrones, estados, heurísticas, prototipos mobile y desktop, reglas de UX. Se hace después de UX1 (wireframes) y antes de la construcción de las páginas.

### RT18 · Trilingüe ES/CA/EN — activar antes del SEO ⏳ [ALTA]
**Decisión del editor 2026-04-21 noche:** el trilingüe debe estar operativo antes de activar el SEO serio. Implica que entra en Fase 4 (web completa), no diferido como estaba.

**Implicaciones:**
- Pipeline se complica: generate ES (Opus) + translate CA (Sonnet) + translate EN (Sonnet) + validador de consistencia (mismas URLs, mismas cifras, mismo nº de bullets).
- Web multilingüe desde el lanzamiento: carpetas `/ca/` y `/en/`, diccionario `_data/i18n.yml`, selector de idioma global, `<html lang>` correcto por página, hreflang en cada una.
- SEO multilingüe: 3 feeds RSS (`feed.xml`, `feed.ca.xml`, `feed.en.xml`), title/description optimizados por idioma (no solo traducidos), JSON-LD con `inLanguage`, sitemap con `xhtml:link rel="alternate"`.
- Coste operativo +1,15 €/mes (de ~6-7 a ~8 €/mes). Dentro del tope blando 12 €/mes con margen.
- Glosario eivissenc con topónimos y cargos oficiales + regla de preservar mayúsculas interiores (Can Toni, Sa Penya).
- Variante catalán: estándar IEC (no balear), alineado con IB3 Notícies, Ara Balears, Vilaweb.

**Decisión del editor 2026-04-22:** el trilingüe se activa **desde el backfill**. Las 12 ediciones retroactivas salen en 3 idiomas desde el relanzamiento. Coste puntual adicional +3-4 € absorbido por el tope duro subido a 50 €. Consistencia de corpus desde el día 1.

**Salida:** pipeline de traducción operativo + chrome trilingüe + SEO multilingüe + backfill trilingüe ejecutado. Entregable en Fase 4 antes de Fase 5.

### RT19 · Seguimiento visual de evolución de problemáticas y soluciones ⏳ [DIFERENCIAL]
**Petición del editor 2026-04-21 noche:** una vista pública que permita seguir de forma muy visual y rápida cómo evolucionan las problemáticas de vivienda y sus propuestas de solución en Ibiza. El objetivo es alimentar el empuje hacia mejorar la vivienda: si algo está traccionando, que se destaque — manteniendo imparcialidad.

Esto es **un diferencial editorial real** y se solapa solo parcialmente con otras tareas:
- Complementa PI3 (grafo de evolución de cada propuesta individual).
- Se relaciona con UX7 (sección "avances o éxitos") pero más visual y agregado.
- Distinto de `/balance/` (que mide reparto de actores, no progreso de propuestas).

**Posibles formatos (por estudiar):**
- **Heatmap de propuestas × estado × tiempo.** Eje X: semanas. Eje Y: propuestas. Celdas coloreadas por estado (propuesta/debatida/aprobada/en ejecución/implementada/descartada).
- **Sankey del flujo** propuesta → debate → implementación. Muestra qué % de propuestas avanzan y dónde se atascan.
- **Timeline agregado por problemática** (residencias temporeros, desalojos, alquiler turístico, etc.) con hitos marcados.
- **Kanban público** con propuestas en columnas por estado, filtrable.
- **Combinación** — vista principal tipo timeline + drill-down a fichas individuales.

**Requisito duro de imparcialidad:** el "destacar si tracciona" no puede sesgar por ideología. Las propuestas del PP que avanzan se destacan igual que las de Més. El algoritmo de "tracción" es estado + apoyos citados + cobertura mediática, no alineación editorial.

**Salida:** documento `ESTUDIO-SEGUIMIENTO-VISUAL.md` con comparativa de formatos + decisión + mockup + algoritmo de "tracción" imparcial + implementación (probablemente post-backfill para tener datos suficientes que mostrar).

### RT20 · Estudio del titular legal con detenimiento ⏳ [ALTA · BLOQUEA EMPUJE PÚBLICO]
Coincide con LG1 (anonimato legal) pero la tarea pide un estudio formal antes de decidir. Opciones a comparar con datos reales:
- **(a) Servicio de representación legal externa.** Empresa especializada actúa como titular declarado en el aviso legal. Editor queda como "responsable editorial" sin aparición legal. Coste típico 50-150 €/año. Ejemplos: ProPrivacy España, Easylegal, pequeños gestores. Rápido.
- **(b) Asociación sin ánimo de lucro.** Constitución con 3 personas (60-300 € inicial + ~100-200 €/año gestoría). Más robusto, abre puertas a grants. Requiere aliados.
- **(c) SL de 1 €** (forma societaria especial 2022). Fiscalmente más complejo, menos alineado con misión no lucrativa, pero da protección patrimonial clara.
- **(d) Fundación paraguas con aliados existentes.** Si Cáritas Ibiza, GEN-GOB, sindicato local, UIB acepta albergar el proyecto bajo su paraguas. Cero coste, máximo prestigio, pero pérdida de autonomía editorial potencial.
- **(e) Pseudónimo + buzón virtual.** Riesgo legal real: LSSI exige titular identificable; pseudónimo solo funciona si hay una figura legal detrás.

**Cruzar variables:** coste, complejidad fiscal, flexibilidad editorial, tiempo de montaje, riesgo real de inspección LSSI, escalabilidad si el proyecto crece. Añadir plan de implementación concreto de la opción recomendada.

**Salida:** documento `ESTUDIO-TITULAR-LEGAL.md` con tabla comparativa + recomendación firme + plan de implementación en días. Decisión del editor + arranque de trámite. Bloquea empuje público: sin titular declarado legalmente, abrir al público es riesgo.

### RT21 · Módulo de precios — nombre provisional y presupuesto ⏳
Antes de implementar la vía A (RT12 estudio de fuentes), cerrar:
- **Nombre público del módulo — provisional 2026-04-22: "Termómetro de precios"** con URL `/precios/`. **Pendiente de revisión** — el editor pide apuntar que el nombre hay que revisarlo cuando el módulo esté más maduro, el proyecto más asentado, o cuando se decida el dominio. Alternativas en reserva: "Observatorio de precios" (descriptivo clásico), "Radar de precios" (refuerza marca principal), "Precios vivienda Ibiza" (SEO puro).
- **Presupuesto operativo proyectado.** Coste de scraping/descarga mensual (la mayoría de fuentes son PDF/CSV descargables, pero IBESTAT tiene API, el Ministerio de Vivienda publica CSV). Coste de almacenamiento (no supera ~5 MB). Coste de mantenimiento cuando cambia un formato de origen (estimar ~2-3 h cada 6 meses). Coste API si se usa Claude para normalizar entre fuentes (probablemente no hace falta — las fuentes oficiales ya vienen estructuradas).
- **Estructura de URLs.** `/precios/` índice, `/precios/ibiza/`, `/precios/formentera/`, `/precios/serie-historica/`, `/precios/fuentes/`? O todo en una sola página con filtros.
- **Modelo de actualización.** Cron mensual que descarga, normaliza, publica. Alerta si alguna fuente cambia formato.

**Salida:** nombre cerrado + presupuesto cuantificado + estructura de URLs + plan de ejecución. Entrada al `ESTUDIO-PRECIOS.md` que contempla RT12.

### RT22 · BOIB watcher — decisión de ubicación en el roadmap ⏳
**Pregunta del editor 2026-04-21 noche** sobre si la ubicación actual del BOIB watcher (Fase 3 afinado + diferido como servicio activo) es la correcta. Análisis honesto:

**Pro subirlo a Fase 2** (junto al backfill):
- BOIB es **fuente primaria pura** (no prensa): leyes, decretos, resoluciones, convocatorias IBAVI. Diferencial claro.
- Si está operativo en el relanzamiento, el corpus cubre normativa oficial desde el día 1.
- Refuerza la narrativa de "observatorio serio con datos primarios" que el editor busca.
- Se integra naturalmente con el tracker de evolución de propuestas (si una propuesta se aprueba por BOIB, el tracker detecta el salto automático).

**Contra subirlo a Fase 2:**
- BOIB no tiene RSS robusto. Requiere scraping del buscador o búsqueda Google News filtrada por `site:caib.es/boib`.
- Complejidad técnica adicional encima de la del backfill.
- Si se hace mal, genera falsos positivos ruidosos (normativa urbanística no relacionada con vivienda).

**Decisión del editor 2026-04-22: Fase 2 confirmada.** El editor considera importante que la base legal esté presente desde el relanzamiento — es el diferencial más claro frente a "refrito de prensa". Se mantiene el estudio de factibilidad técnica previo de 2-4 horas (robots.txt del buscador BOIB, tasa de falsos positivos de búsqueda filtrada, decisión entre scraping ético vs filtro Google News) como primera tarea dentro de Fase 2.

**Salida:** estudio de factibilidad + implementación del watcher + integración con el corpus del backfill + entrada del BOIB como fuente primaria oficial desde el relanzamiento.

### RT23 · Framework de señales de tracción a 90 días post-relanzamiento ⏳ [DIFERIDO POST-LANZAMIENTO]
Para decidir si el proyecto escala a "dedicar energía seria" o se mantiene como side-project experimental, se definen señales medibles que se evalúan 90 días después del relanzamiento.

**Verde (escalar, dedicar energía seria):**
- ≥ 1 cita de prensa local como fuente (no como curiosidad anecdótica).
- ≥ 25 suscriptores reales al newsletter (no familia, no conocidos directos del editor).
- ≥ 1 mención institucional identificable (Cáritas, UIB, sindicato, Consell, ayuntamiento).
- ≥ 500 impresiones/mes en Search Console para búsquedas relacionadas con vivienda + Ibiza.
- ≥ 5 aportes serios vía formulario universal (correcciones, datos, testimonios, pistas).
- ≥ 1 uso identificable de los datos abiertos (CSV descargado) en análisis de terceros.

**Amarilla (replantear ángulo):** 1-2 de las 6 anteriores se cumplen. Tráfico orgánico 50-200/mes. Formulario con 1-2 mensajes al mes.

**Roja (mantener como side-project experimental o aparcar):** 0 citas de prensa a 3 meses, <10 suscriptores, tráfico <50/mes, formulario en silencio.

Tres escenarios de acción según color:
- **Verde →** se activan Vía B crowd-sourcing precios, bots sociales, envío personalizado semanal a periodistas, consejo editorial honorífico, primera aplicación a grant.
- **Amarilla →** conversación abierta sobre qué no funciona (¿tono?, ¿distribución?, ¿cobertura?), ajuste de prompt, ampliación de fuentes, cambio de marca si procede.
- **Roja →** el proyecto queda como corpus experimental. El pipeline sigue generando ediciones porque el coste es trivial (~7 €/mes), pero no se invierte más energía en UX, distribución o expansión. Se reevalúa a 180 días.

**Salida:** documento `SEÑALES-TRACCION.md` con umbrales formales + plan de acción por color + ritual de evaluación a 90 días. Revisión automática cada 90 días en adelante.

### RT24 · Escenarios de lanzamiento y horizonte ⏳
**Decisión del editor 2026-04-21 noche:** el proyecto admite dos escenarios válidos y la naturalidad del proceso decide cuál aplica. No se fuerza ninguno.

**Escenario A — Soft launch mayo-junio + extensión si señales tibias.**
- Relanzamiento suave: web abierta, newsletter activo, envío manual a lista curada de 15-25 contactos. Sin nota de prensa, sin ruido.
- Medición a 90 días con el framework de señales (RT23).
- Verde → se escala con las fases post-lanzamiento del roadmap.
- Amarilla/Roja → se extiende rodaje privado 3-6 meses más antes de reintentar empuje.

**Escenario B — Rodaje privado largo.**
- Web existe con `noindex,nofollow`. El editor opera el pipeline semanal sin buscar audiencia.
- 6-12 meses para acumular corpus sólido, afinar criterios empíricamente, pulir metodología.
- Relanzamiento formal en primavera 2027 con mucha más confianza.
- Coste: ~84 € en API durante el año + tiempo voluntario del editor.
- Sentido: si durante la preparación del relanzamiento A aparece que el método aún necesita afinarse, se migra a B sin drama.

**Criterio de decisión del escenario:** al terminar Fase 6 (pre-empuje), mirar el estado real del proyecto con honestidad — métodos afinados, corpus consistente, autoría limpia, datos propios operativos o no, tiers funcionando, banner de rodaje con copy creíble. Si todo está en verde, Escenario A. Si algo cruje, Escenario B sin pena.

**Salida:** sección explícita en el roadmap + revisión formal del escenario al terminar Fase 6 + mismo ritual cada 3 meses si se está en Escenario B.

### RT12 · Vía A de precios — estudio en profundidad antes del relanzamiento ⏳ [ALTA]
Adelantar la [Vía A del observatorio de precios](PLAN.md) (agregación mensual de informes públicos) al pre-relanzamiento es la palanca más fuerte para convertir el proyecto de "lectura estructurada de prensa local" a **fuente primaria con datos propios**. Coste 0 €, sin riesgo legal (son informes públicos descargables), sin scraping contra TOS. El PLAN la dejaba en Fase 2 (3-6 meses post-relanzamiento); el editor 2026-04-21 noche acepta adelantarla y pide estudio profundo antes de comprometer trabajo.

**Preguntas que debe responder el estudio:**

1. **Fuentes efectivas.** Cuáles publican datos agregados de Ibiza (no solo Baleares, no solo España) con granularidad útil:
   - **Idealista — Informe de Precios.** Trimestral, por provincia y municipio. Descargable en PDF. ¿Desglosa Ibiza vs Formentera? ¿Separa habitación vs vivienda completa? ¿Distingue temporada vs anual?
   - **Fotocasa — Índice Inmobiliario.** Mensual, ahora disponible por municipio. Revisar cobertura real de Ibiza en su panel.
   - **INE** — Estadística Continua de Viviendas (ECV), Encuesta de Población Activa (EPA, para alquiler como gasto). ¿Granularidad Ibiza?
   - **IBESTAT** (Institut d'Estadística de les Illes Balears). Es la fuente más local; probablemente la que mejor encaja. ¿Qué series tienen sobre vivienda?
   - **Ministerio de Vivienda — Observatorio del Alquiler.** Nacional con desglose por provincia y municipio desde 2024. ¿Datos descargables en CSV?
   - **BOIB.** Convocatorias del IBAVI (adjudicaciones, precios de VPO) como dato primario.
   - **Portales menores:** Habitaclia, Pisos.com, Engel & Völkers (si publican agregado).

2. **Frecuencia y latencia.** Cada fuente publica con qué frecuencia y cuántos días de retraso. La página `/precios/` necesita actualización mínima mensual.

3. **Scraping ético vs API.** Qué fuentes tienen API abierta (IBESTAT sí, INE sí, Ministerio depende), cuáles exigen descarga manual del PDF/XLS, cuáles requieren registro.

4. **Normalización de datos.** Las fuentes no comparten tipología. Hay que definir un esquema propio (zona, tipo de vivienda, periodo, precio medio, mediana, percentil 25/75, método de cálculo declarado) y mapear cada fuente contra él.

5. **Presentación visual.** Gráfico de líneas por zona y tipo, tabla comparativa trimestral, ficha por fuente con link al PDF original, CSV descargable (alimenta `/datos-abiertos/`).

6. **Disclaimer de limitaciones.** Cada fuente mide cosas distintas (oferta vs contrato firmado, portal vs BOE) y tiene sesgos (Idealista infra-representa alquiler de temporada, el Ministerio sobre-representa nuevos contratos). Hay que declararlo para no inducir a error.

7. **Coste operativo y tiempo de mantenimiento.** Script mensual que se ejecuta por GitHub Action. Tiempo estimado de mantenimiento cuando cambia un formato de origen.

8. **Encaje con el relanzamiento.** Si el estudio concluye que Vía A es viable con 2-3 días de trabajo, se monta antes del relanzamiento y la página `/precios/` sale con 3-6 meses de datos agregados (Q1 2026 hasta fecha de lanzamiento). Si concluye que es más complejo, se mantiene en Fase 2.

**Salida esperada:** documento `ESTUDIO-PRECIOS.md` con (a) matriz de fuentes × granularidad × coste de extracción, (b) esquema de datos normalizado, (c) recomendación firme sobre si adelantar al pre-relanzamiento o mantener en Fase 2, (d) si se adelanta, plan de ejecución en días de trabajo.

**Prioridad:** ALTA. Adelantarla al pre-relanzamiento cambia la narrativa de "observatorio documental de prensa" a "observatorio documental de prensa **+** datos primarios de precios". Es el diferencial que el lector profesional espera.

### RT10 · Promover LG1 y LG2 a prioridad alta antes del relanzamiento ⏳
Las tareas de identidad/legalidad del editor ([LG1 anonimato, LG2 portfolio sin nombre](REVISION-FASE-0.5.md)) están catalogadas en P4. El editor confirmó 2026-04-21 noche que el proyecto se relanza sin su nombre completo ("Raúl S." sin email directo). Sin resolver la legalidad (LSSI exige identificar titular del sitio), cualquier atención pública antes del relanzamiento es un riesgo.

**Acción:** subir LG1 y LG2 a prioridad alta dentro de P-1. Resolución sugerida: buzón virtual + servicio de representación legal mínimo (50-150 €/año) que actúe como titular declarado, con el editor como "responsable editorial" sin aparición en el aviso legal. Alternativas: pseudónimo + referencia a entidad paraguas (asociación o fundación pequeña) si existe aliado disponible.

**Salida esperada:** aviso legal redactado, titular declarado legalmente identificable, editor protegido mediante estructura intermedia. Todo previo al primer empuje público del relanzamiento.

---

## P0 — Fundacional (método editorial y fuentes)

### ED1 · Criterio de "OK" para admitir una propuesta ✅ CERRADA PARCIAL 2026-04-29
En qué se basa el pipeline exactamente para dar luz verde a *"autor identificado + URL verificable"*. ¿Qué cuenta como URL primaria? ¿Qué hace `verify.py` hoy vs qué debería hacer? ¿Qué pasa cuando la URL cae meses después?
**Salida:** checklist formal de verificación + árbol de decisión + actualización de `ARQUITECTURA.md §verify.py`.

**Cerrada parcial 2026-04-29 — criterio editorial público.** Documentado en [`docs/que-documentamos.md`](docs/que-documentamos.md) (`/que-documentamos/`): tres puertas de admisión (origen, tema, propuesta verificable), tres tipos de propuesta (formal, en movimiento, descartada) con ejemplos reales del histórico W17-W18, reglas estrictas que aplica el sistema (sin actor con nombre no entra, sin enlace vivo no entra, no se inventan firmantes, cifras solo si aparecen literales, verbos opinativos prohibidos), niveles de fiabilidad (D9), y procedimiento si el lector cree que falta una propuesta. Enlazada desde footer, `/metodo/` y `/politica-editorial/`.

**Pendiente técnico interno:** árbol de decisión formal de `verify.py` (qué hace ante 403/5xx/timeout), política de URLs caídas a posteriori (¿se retira la propuesta? ¿se marca?), criterio de URL primaria vs URL secundaria. Queda abierta como tarea técnica del pipeline, no editorial.

### ED2 · Imparcialidad medible y alertable ⏳
La imparcialidad es pilar. Hoy se mide a trimestre vista en `/balance/`. Hace falta:
- Umbrales numéricos automáticos (p.ej. si un bloque supera 55% a 8 semanas vista → alerta Telegram).
- Métrica por actor-destinatario (no solo por emisor).
- Métrica de tono (¿se cita verbatim o parafraseado? ¿con qué verbo?).
**Salida:** sección en `ARQUITECTURA.md` + umbrales en `balance.py` + hooks de notify.

### ED3 · Presencia editorial de "Omisiones" ⏳
Hoy Omisiones vive como sección 6 de la edición. ¿Es suficiente? ¿Merece página propia `/omisiones/` como tracker? ¿Debería tener peso visual en la home? Es uno de los tres diferenciales editoriales.
**Salida:** decisión sobre peso + posible nueva página + ajuste a `DISENO-WEB.md`.

### ED5 · Modo entrenamiento — DESCARTADA ❌
Descartada 2026-04-21. Incompatible con el rol realista del editor (operador, no revisor). Reemplazada por sistema de tiers públicos + cuarentena + sanity check externo.

### ED4 · Horizonte temporal = fecha de inicio del proyecto ✅ CERRADA 2026-04-29
Regla dura: cuando una propuesta dice *"primera vez documentada"*, se refiere al **observatorio**, no a la historia.
**Cerrada 2026-04-29.** Disclaimer añadido en dos sitios: sección *"Desde cuándo"* en [`/que-documentamos/`](docs/que-documentamos.md) y sesgo adicional en [`/metodo/`](docs/metodo.md). Ambos dicen "primera semana del archivo" sin fecha concreta — la fecha exacta se rellena cuando el backfill real (PI2-B) confirme la semana más antigua del corpus. El tooltip contextual queda diferido a la fase de Diseño.

### FU1 · Fuentes — estáticas vs vivas ⏳
Hoy `sources.yaml` es estático. No hay proceso de revisión. Debería haber:
- Revisión trimestral de qué fuentes están aportando señal vs ruido.
- Health-check de RSS (si un feed lleva 2 semanas sin nada útil, alerta).
- Horizonte realista de "cobertura ≈100%" o asumir que nunca lo es y cuantificar el gap.
**Salida:** proceso documentado + script `sources_health.py` + nota en metodología sobre cobertura declarada.

### FU2 · Google News — estudio de búsquedas temáticas ⏳
Las 4 búsquedas actuales (Ibiza vivienda, Ibiza trabajadores temporada, Consell Eivissa vivienda, Ibiza desahucio caravanas) se pusieron sin debate. Merece análisis: qué queries cubren mejor, qué términos faltan (ej. *"bolsa alquiler"*, *"vivienda protegida"*, *"mobbing inmobiliario"*, *"chabolismo"*, *"HUT"*, *"Llei habitatge"*), en catalán y en castellano.
**Salida:** matriz de queries puntuada por recall/precision + `sources.yaml` ampliado + método de revisión anual.

### FU3 · Hora Ibiza + Nou Diari — reevaluar ✅ CERRADA 2026-04-29
- **Hora Ibiza:** descartada definitivamente. El dominio `horadeibiza.com` no responde, el medio no tiene presencia rastreable en directorios ni redes sociales. No existe como fuente activa.
- **Nou Diari (`noudiari.es`):** incorporada. Feed RSS `https://www.noudiari.es/feed/` activo y funcional, 8-15 artículos/día, cobertura directa de vivienda y trabajadores de temporada en Ibiza/Formentera, sin paywall, todo en castellano. Añadida a `src/sources.yaml` 2026-04-29.

### FU4 · BOIB / legal — conexión al pipeline ⏳
El Boletín Oficial de las Illes Balears publica leyes, decretos, resoluciones del Govern y Consell. Es fuente primaria pura. Hoy no está conectado. ¿Tiene RSS? ¿Hay que scrappear el buscador? ¿Coste de mantenimiento?
**Salida:** informe de factibilidad + si es viable, módulo `ingest_boib.py` o búsqueda Google News *"site:caib.es/boib"*.

---

## P1 — Estructural (pipeline, datos, contenido)

### PI1 · Revisión global del pipeline ⏳
Pasar revista a ingest → classify → extract → rescue → generate → verify → balance. Buscar:
- Pasos redundantes.
- Huecos (ej. deduplicación entre ediciones, detección de misma propuesta rebautizada).
- Seguridad: qué pasa si Anthropic cae, si un feed devuelve HTML inválido, si Opus alucina un URL.
- Innovaciones: ¿detectar cambio de posición de un actor entre ediciones? ¿agrupar propuestas equivalentes de distintos actores?
**Salida:** diff documentado sobre `ARQUITECTURA.md` + issues creados.

### PI2-A · Archivado append-only desde hoy 🔄
Hoy `ingested.json` y `classified.json` se sobreescriben en cada ejecución. Cambiar pipeline para que cada ejecución semanal archive a `data/archive/YYYY-wWW/` (ingested + classified + extracted + verify_report). No se pierde materia prima nunca más.
**Salida:** pipeline modificado + estructura `data/archive/` + nota en `ARQUITECTURA.md`.
**Prioridad ejecución:** primera del día (~1 h).

### PI2-B · Backfill retroactivo de 12 semanas ⏳
Script one-shot `src/backfill.py` que recorre Google News con operadores temporales (`after:X before:Y`) + buscadores nativos de Diario de Ibiza / Periódico de Ibiza semana a semana desde W06 (2 feb) hasta W17 (20 abr). Dedup por URL. Salida a `data/archive/YYYY-wWW/ingested.json`. Luego ejecuta classify + extract + auditor + verify sobre todo el corpus.
**Salida:** 12 semanas de corpus real con propuestas extraídas, auditadas, verificadas y con snapshot Wayback.
**Coste:** ~3 € API + ~1 h ejecución.
**Prioridad ejecución:** tras PI2-A y PI9.
**Tarea asociada al cerrar:** actualizar la fecha de origen en [`/que-documentamos/`](docs/que-documentamos.md) y [`/metodo/`](docs/metodo.md) con la semana real más antigua del corpus generado. Ambas páginas ahora dicen "primera semana del archivo" sin fecha concreta — rellenar cuando el backfill confirme la semana real. Ver ED4 cerrada.

### PI10 · Sistema de tiers de confianza públicos ⏳ [NUEVO 2026-04-21]
Implementa Plan A aprobado. Cada propuesta publicada lleva badge 🟢/🟡/🟠 calculado por el auditor IA. Las 🔴 van a cuarentena. Criterios:
- 🟢 Alta: dos capas IA coinciden en todos los campos críticos + verify.py pasa los 5 checks + propuesta corroborada por 2+ fuentes independientes.
- 🟡 Media: dos capas IA coinciden + verify.py pasa + fuente única.
- 🟠 Baja: arbitraje Opus resolvió una discrepancia, o verify.py devolvió warnings no bloqueantes.
- 🔴 No publicada: flagged grave, verify.py bloqueante, o arbitraje no pudo resolver.
Los umbrales son ajustables (config en `src/tiers.py` o similar). Copy visible al público explicando cada tier en lenguaje llano.
**Salida:** módulo `src/tiers.py` + campo `confidence_tier` en schema de propuesta + plantilla visual del badge en edición + fichas + tracker.

### PI11 · Cuarentena pública `/revision-pendiente/` ⏳ [NUEVO 2026-04-21]
Implementa Plan B aprobado. Las propuestas 🔴 no entran en edición semanal; viven en página pública `/revision-pendiente/` con explicación en lenguaje llano y tabla filtrable. Regla automática: a los 60 días sin corroboración se archivan como "no verificada" en `/propuestas/?status=no_verificada`.
**Salida:** página Jekyll + lista generada desde `data/quarantine.json` + regla de archivo 60d + integración con alerta Telegram.

### PI12 · Alerta Telegram de lunes enriquecida ⏳ [PARCIAL 2026-04-21]
Mezcla A+C decidida. Implementado base en `src/report.py` (_build_summary y helpers). Falta conectar `balance_status.json` y `quarantine.json` (cuando existan los módulos upstream). Email queda como tarea futura.
**Salida pendiente:** activar bloque de alertas cuando PI10/PI11/balance.py emitan sus archivos status.

### PI13 · Notificación por email (futuro) ⏳ [NUEVO 2026-04-21]
Cuando el proyecto tenga buzón de correo propio, la alerta del lunes también se envía por email (para tener archivo consultable). Baja prioridad hasta que el buzón exista.
**Salida:** envío por SMTP o servicio (Resend, Brevo) + plantilla HTML simple.

### PI9 · Sistema de auditoría IA — partido en mínimo viable + iteración ⏳ [partición 2026-04-23, [D1](DECISIONES.md)]
Módulo `src/audit.py` que implementa la arquitectura decidida el 21-abr, afinada el 23-abr y **partida en dos bloques de construcción** el 23-abr:

**PI9-MVP · Auditor mínimo viable (2 semanas · Hito 1 del frame de tres hitos, [D6](DECISIONES.md)):**
1. **Extract Haiku** (ya existe en `src/extract.py`).
2. **Audit ciego Sonnet** (re-extracción sin ver la primera, batch único).
3. **Comparador determinista** Python + 5 checks de `verify.py` + tres heurísticas sin IA (cross-source, verbatim substring con umbrales diferenciados por `statement_type`, domain-actor whitelist V1 de 15-20 actores en `data/actor_domains.yml` — ver [D3](DECISIONES.md)).
4. **Capa 4 Opus como fallback actual** (no formalizada como paso separado todavía).
5. **Log público por propuesta** en `data/audit/YYYY-wWW/{proposal_id}.json` con campo `corrections` append-only ([D2](DECISIONES.md)) + hueco reservado `tier: { value: null, reason: "pendiente estudio", signals: {...} }` ([D5](DECISIONES.md)).
6. **Protocolo formal de correcciones en 72 h** + página pública `/correcciones/` con el protocolo en lenguaje llano + canal email (diferido hasta cierre del nombre) + canal formulario con backend webhook → issue GitHub → notificación Telegram ([D2](DECISIONES.md)).
7. **Integración con `report.py`** y prueba empírica sobre la semana W10 (2-8 marzo 2026) antes del backfill completo.

Sin Opus formalizado como capa separada, sin página `/revision-pendiente/`, sin dashboard `/auditor/`, sin capa 5bis, sin tests unitarios propios (diferidos a RT5 con fixtures reales del backfill, ver [D4](DECISIONES.md)).

**PI9-Iteración · Completar las 5 capas + vitrina pública (2-3 semanas, puede solaparse con Fase 2):**
- Formalización explícita de **capa 4 Opus** como paso auditor separado.
- **Capa 5bis** — repaso IA mensual de cuarentena (Opus lee cuarentena + logs + whitelist, propone ajustes YAML, editor firma con OK por Telegram en 5 min).
- Página pública `/revision-pendiente/` con la cuarentena navegable.
- Dashboard público `/auditor/` — canal 1 del panel de éxito (§12.1 del estudio de costes).
- Parte Telegram consolidado del lunes — canal 2.
- Página `/reportes/` con narrativa mensual → trimestral → semestral — canal 3.
- Conexión de `compute_tier()` real cuando RT15 cierre, leyendo del bloque `signals` del log.

Detalle completo en [`ESTUDIO-COSTES-AUDITOR.md §10.0`](ESTUDIO-COSTES-AUDITOR.md).

**Salida PI9-MVP:** `src/audit.py` + `src/audit_compare.py` + `src/audit_heuristics.py` + `data/actor_domains.yml` V1 + log público en `data/audit/` + página `/correcciones/` + integración en `report.py`.
**Coste por ejecución semanal:** ~0,15 € en MVP (sin capa 5bis ni auditoría Opus mensual). Completo con iteración: ~0,25 €/semana + ~0,4 €/mes de capa 5bis.
**Plano de obra cerrado 2026-04-24:** [`DISENO-AUDITOR-MVP.md`](DISENO-AUDITOR-MVP.md) (11 secciones — contratos de módulos, schema del registro con 11 señales, whitelist V1 cerrada de 20 actores, algoritmos de las tres heurísticas, calendario partido en 4 semanas). Documento de referencia durante la construcción; se archiva al cerrar el Hito 1.

### PI3 · Enlace entre ediciones y evolución de propuestas ⏳
Esto es donde hay *oro oculto*: una propuesta que nace W15, se debate W17, se rechaza W19. Hoy el tracker enlaza débilmente. Debería haber:
- Grafo de evolución visible por propuesta.
- Detección automática de *"esta propuesta es variante de aquella"*.
- Sección "qué pasó con lo de la semana pasada" en cada edición.
**Salida:** diseño de la relación entre propuestas + ajustes a schema + nueva vista en `/propuestas/{id}/`.

### PI4 · Datos abiertos — disclaimer sobre citabilidad ⏳
Si alguien descarga el CSV, debe quedar claro: para fuente fiable, acuda al **URL original** que está en cada fila. Nuestro dato es trazabilidad, no la fuente en sí.
**Salida:** disclaimer prominente en `/datos-abiertos/` + licencia CC-BY con atribución a fuentes primarias.

### PI5 · GitHub — techos y plan B ⏳
Todo vive en GitHub (repo + Pages + Actions). Límites reales:
- Actions: 2.000 min/mes gratis en repo privado, ilimitado en público.
- Pages: 100 GB/mes bandwidth, 1 GB tamaño repo.
- Baneo político/comercial (poco probable pero contemplable).
**Salida:** análisis de techos + estrategia de migración si algún día toca (Cloudflare Pages, Netlify) + backup automático del repo a otro remoto.

### PI6 · Modelos IA — documentación viva de la decisión ⏳
Haiku clasifica/extrae, Sonnet verifica, Opus compone. ¿Cómo sabemos que es óptimo? Hace falta:
- Log de coste real por fase.
- Test periódico: mismo input con modelos distintos, comparar output.
- Criterio de upgrade si sale un modelo mejor (p.ej. Haiku 5).
**Salida:** `docs/MODELOS.md` con criterios + script de benchmark + revisión semestral.

### PI7 · Registro completo de costes ⏳
Auditar que `costs.csv` captura 100% de llamadas (incluidas las fallidas, reintentos, tests manuales). ¿Hay huecos? ¿Tenemos coste por fase/modelo/edición?
**Salida:** auditoría de 4 semanas + fixes si hay huecos + dashboard más granular.

### PI8 · Contenido — página maestra "cómo funciona" + tooltips contextuales ⏳
El resumen que se le hizo al editor hoy debe convertirse en página pública (adaptada). Decisión: qué entra, qué queda para `/metodologia/` técnica, qué va en `/politica-editorial/`. Añadir tooltips `ⓘ` al lado de cada titular de sección en ediciones + mini-tagline debajo con bajo impacto visual.
**Salida:** copy de la página + sistema de tooltips + componente reutilizable.

---

## P2 — UX y diseño

### UX1 · Mockup/wireframe antes de diseño visual ⏳
El editor nota que se está entrando en CSS antes de validar estructura. Construir wireframes low-fi de todas las páginas (grises, sin tipografía final) para iterar rápido y validar flujos.
**Salida:** wireframes de home + edición + propuestas + ficha propuesta + ficha actor + balance + recursos + cómo usarlo, en formato rápido de iterar (HTML sin CSS o Figma/Excalidraw).

### UX2 · Navegación flagship ⏳
La navegación debe invitar a cruzar secciones en cualquier dirección. Menús en múltiples lugares (top, footer, inline, breadcrumbs, "related"), versión mobile y desktop diferenciadas, links contextuales dentro del contenido, CTAs de exploración al final de cada vista.
**Salida:** estudio aparte con mapa de enlaces, patrones, estados, heurísticas. Documento propio `NAVEGACION.md`.

### UX3 · Dos públicos — toggle, versiones o home dual bien calibrada ⏳
Decidir si se mantiene home dual, se saca toggle "soy curioso / soy profesional", o se hacen dos landings distintas con misma backend.
**Salida:** decisión + prototipo de la elegida.

### UX4 · Guía rápida en el fold ⏳
En el fold de la home, guía rápida que no ocupe más del 50%. Qué es, cómo se usa, 3 claves. Reemplaza parte del hero actual.
**Salida:** copy + mockup del bloque.

### UX5 · Balance accesible a todo el público ⏳
Hoy `/balance/` es técnico. Debería tener versión *"qué está pasando con la imparcialidad esta semana, explicado"* para público general. Visualizaciones claras, lenguaje llano.
**Salida:** rediseño de `/balance/` con doble capa (resumen público + detalle técnico).

### UX6 · Semana flaca — comunicación honesta ⏳
Si una semana nadie propone nada, la edición queda vacía. Hay que tener plantilla y tono: *"esta semana no hemos detectado propuestas nuevas. El silencio también es información. Aquí lo que sí ha pasado (hechos) y propuestas anteriores que siguen vivas (rescate)."*
**Salida:** plantilla + criterio editorial + componente UI.

### UX7 · Sección "avances o éxitos" — ¿es mojarse? ⏳
Pregunta abierta: ¿se puede documentar de forma neutra qué propuestas se han implementado/avanzado/descartado sin tomar partido? Una página `/seguimiento/` o columna en `/propuestas/` con estado *implementada/descartada/en ejecución* sin valorar *"bueno/malo"*. Hay que estudiarlo.
**Salida:** decisión + si va adelante, diseño de la sección.

### UX8 · Construir la web entera aunque no se publique toda ⏳
Editor propone construir todas las páginas aunque en la Fase 1 pública solo se abra un subconjunto. Definir qué se abre en lanzamiento vs qué queda draft visible solo para editor.
**Salida:** matriz de páginas × fase pública + flag `draft: true` por página.

---

## P3 — Operacional y meta

### OP1 · Plan de respuesta a rectificación de actor ✅ CERRADA 2026-04-29
Qué pasa si un partido/institución escribe diciendo *"esa cita no es mía"* o *"el contexto es otro"*. Hoy hay `/correcciones/` pero sin SLA ni proceso.
**Salida:** protocolo + plantillas + tiempos + quién decide.

**Cerrada 2026-04-29.** Protocolo interno en [`private/protocolo-correcciones.md`](private/protocolo-correcciones.md): dos casos (error de hecho vs. reclamación de actor), plazos (24 h acuse de recibo, 72 h resolución), criterio de decisión, qué actualizar al corregir, tres plantillas de respuesta, lista de qué no ceder, y cuándo escalar si hay amenaza legal. Revisión antes del empuje público (Hito 3).

### OP2 · Health de feeds — alertas proactivas ✅
Si un RSS deja de publicar, si baja la frecuencia, si Google News cambia su formato → alerta Telegram.

**Implementación 2026-04-25 (alcance acotado):**
- Módulo nuevo `src/sources_health.py` con dos funciones: `record_run(metrics)` que añade una línea al histórico `data/feed_health.json` (append-only), y `evaluate_alerts(history)` que compara la última ejecución con las anteriores y devuelve la lista de problemas detectados.
- Modificación pequeña a `src/ingest.py`: recolectar métricas por feed durante la iteración (estado, entradas totales, entradas que pasan keywords, entradas dentro de la ventana, excepción si la hubo). Al terminar la ingesta, llamar a `sources_health.record_run()` y, si hay alertas, mandar un único mensaje consolidado vía `notify.py` con `level="warning"`.
- Histórico solo se escribe en GitHub Actions (`GITHUB_ACTIONS=true`) — las ejecuciones locales no contaminan los datos de salud.

**Reglas de alerta:**
- **Feed muerto:** dos ejecuciones seguidas con estado distinto a *ok*.
- **Frecuencia caída:** la media de noticias dentro de la ventana cae más de un 50 % respecto a las cuatro ejecuciones anteriores.
- **Feed vacío inesperado:** estado *ok* pero cero entradas, cuando la base de runs anteriores era ≥5.
- **Estructura cambiada:** estado malformado (`bozo` de feedparser) cuando antes estaba bien.

**Fuera de scope hoy** (registrados como OP3, OP4, OP5 más abajo).

**Salida:** módulo `sources_health.py` + integración en `ingest.py` + alertas consolidadas vía Telegram.

**Estado:** ✅ cerrada 2026-04-25. Pendiente solo la calibración de umbrales (50 % de caída, ≥5 runs como base, etc.) cuando haya 4-8 semanas de `feed_health.json` acumulado del cron real.

### OP3 · Auto-recuperación de feeds caídos ⏳
Si un feed cae, probar URLs alternativas automáticamente (espejo del medio, query alternativa de Google News, RSS de respaldo) antes de marcarlo como muerto. Hoy OP2 solo notifica; el editor decide qué hacer manualmente.
**Salida:** estrategia + lista de fallbacks por feed + lógica de prueba en `ingest.py`. Pendiente hasta tener datos reales (3-4 caídas) que digan qué fuentes fallan más y qué espejos serían útiles.

### OP4 · Dashboard visual del estado de feeds ⏳
Página interna o pública con la salud de cada feed (uptime, frecuencia media, última ejecución exitosa, gráfico de noticias/semana). Decisión de UX: ¿privada en `private/` o pública en `/metodologia/feeds/`? Lo segundo refuerza honestidad pero expone fragilidades. Decidir cuando haya 4-8 semanas de `feed_health.json` acumulado.
**Salida:** decisión de ubicación + diseño + script `build_feeds_dashboard.py` que regenera la página.

### OP5 · Alerta al primer fallo aislado ⏳ [BAJA]
Hoy OP2 espera dos ejecuciones consecutivas con fallo antes de avisar (baja ruido por caídas temporales del medio). Si el editor empieza a notar que pierde 5-7 días de cobertura por esperar el segundo fallo, valorar bajar el umbral a 1 fallo + canal silencioso (Telegram con icono distinto, sin acción urgente).
**Salida:** ajuste de umbral en `evaluate_alerts()` + diferenciación de niveles de severidad. Esperar señal real de demanda — no implementar preventivamente.

---

## P4 — Identidad, legal, financiación

### ID1 · Nombre definitivo — `radar))ibiza_vivienda` ✅
**Cerrada 2026-04-21 noche.** El editor cierra el wordmark en **`radar))ibiza_vivienda`** (formato `lugar_tema`) por sentir que se lee más natural en español. Futuros verticales: `radar))ibiza_turismo`, `radar))ibiza_medioambiente`, `radar))formentera_vivienda`. Documentos actualizados: CLAUDE.md, STATUS.md, ESTUDIO-DISENO.md. El prototipo HTML queda por actualizar cuando se retome Diseño (coordinado con RT16 Claude Design).

### LG1 · Anonimato legal del editor ⏳
Investigar cómo mantener el nombre del editor oculto en:
- Aviso legal (obligatorio identificar responsable según LSSI).
- Registro de dominio (WHOIS privacy).
- Cuentas redes sociales.
- GitHub (posible).
Opciones gratis (pseudónimo + buzón virtual, fundación paraguas, etc.) y de pago baratas (servicios de representante legal, SL de 1 €, etc.).
**Salida:** informe con opciones, costes y riesgos legales reales.

### LG2 · Página de estudio sin nombre del editor ⏳
Editor quiere mencionar en `/acerca/` un link a un portfolio de *"proyectos IA del estudio"* sin revelar su identidad. Ver cómo articular esto legalmente y editorialmente.
**Salida:** decisión sobre si procede + copy + link a página externa a crear.

### FI1 · Financiación desde el lanzamiento ⏳
Activar canales de ingreso desde día 1 (sin agresividad, pero presentes): Ko-fi/Buy Me a Coffee, Open Collective, Patreon, botón "donación única PayPal", propuesta de mecenazgo institucional (fundaciones, Consell Social UIB, etc.). Decidir cuáles encajan con la neutralidad del proyecto.
**Salida:** estrategia de financiación + página `/apoyar/` + criterios de qué donaciones se aceptan y cuáles no (p.ej. ¿patronal hotelera? ¿partido político?).

---

## P5 — Misc (sugerencias de Claude añadidas)

### EX1 · Test de usabilidad pre-lanzamiento con 2-3 personas reales ⏳
Antes de lanzar público, pasar la web a una periodista, un temporero y un técnico municipal. Observar. Grabar si se puede.
**Salida:** informe + ajustes.

### EX2 · SEO técnico — schema.org para propuestas ⏳
Que cada `/propuestas/{id}/` tenga structured data (ClaimReview, NewsArticle). Google adora esto. Puede traer mucho tráfico.
**Salida:** implementación + validación Rich Results Test.

### EX3 · Estrategia de lanzamiento — soft vs hard ⏳
Cómo se lanza. A quién se le dice primero. Embargo con periodista afín. Nota de prensa. O sigiloso y que el SEO haga su trabajo.
**Salida:** plan de lanzamiento con fases y fechas.

### EX4 · Backup automático del repo ✅ CERRADA 2026-04-29
Mirror automático a GitLab. Cero coste, seguro ante cualquier incidencia en GitHub.
**Decisión:** Pull mirroring nativo de GitLab (sin workflow GitHub Actions). GitLab copia el repo cada hora. El repo de GitHub es público → no requiere token. Cero cambios al repo. Instrucciones de configuración en DIARIO 2026-04-29.
**Salida:** configuración en GitLab Settings → Repository → Mirroring.

### EX5 · Sanity check externo pre-lanzamiento ⏳ [NUEVO 2026-04-21]
Contratar 1-2 h a periodista local o académico UIB para auditar una muestra de 30 propuestas del backfill antes de hacer público el sitio. Coste estimado 50-100 €. Sirve para (a) detectar sesgos que el editor y la IA no ven por proximidad al tema, (b) validar que el tono y la neutralidad funcionan para lector profesional local, (c) tener un escudo de validación independiente documentado en `/metodologia/`.
**Salida:** selección de revisor + informe escrito + ajustes previos a lanzamiento + mención pública en metodología (con consentimiento del revisor).

### RT25 · Medición empírica del sesgo de tiers por tipo de actor ⏳ [ALTA — depende del backfill]

Deriva de [`ESTUDIO-TIERS.md §8`](ESTUDIO-TIERS.md). La regla dura "nunca 🟢 con fuente única" protege la fiabilidad pero puede proyectar el desequilibrio mediático (quién tiene megáfono propio) como si fuera fiabilidad factual. Actores con menos presencia en prensa local (colectivos vecinales, asambleas, sindicatos minoritarios, tercer sector pequeño) quedan en 🟡 crónicos aunque sus propuestas sean impecables.

**Acción (tras el backfill de 12 semanas):**

1. Construir `scripts/tier_bias_audit.py` (~2 h) que lee `data/audit/*.json` y calcula la distribución de tiers 🟢/🟡/🟠/🔴 por `actor_type` (8 categorías de la taxonomía).
2. Ejecutar sobre el corpus del backfill (~36 propuestas).
3. Comparar tasa de 🟢 por categoría contra el promedio global.
4. **Umbral de alerta:** si alguna categoría queda > 30 % por debajo del promedio y n ≥ 5, aplicar mitigación M1 de §8 (relajar el techo de fuente única en las 4 categorías señaladas, cuando el dominio es oficial del actor).
5. Aplicar M2 (nota metodológica pública) independientemente del resultado — honestidad.
6. Actualizar `data/tiers.yml` si M1 entra en vigor + documentar en [`ESTUDIO-TIERS.md §8.5`](ESTUDIO-TIERS.md).

**Salida:** informe en `private/estudios/tier-bias-audit-post-backfill.md` + `data/tiers.yml` ajustado si aplica + nota metodológica redactada + [`ESTUDIO-TIERS.md §8`](ESTUDIO-TIERS.md) cerrada.

**Prerrequisito:** backfill 12 semanas completo (PI2-B).

### RT26 · Cierre de las 5 decisiones abiertas del estudio de tiers ✅ CERRADA 2026-04-23

El editor dio OK en bloque a las cinco recomendaciones del asistente. Registrado en [D9](DECISIONES.md) y en [`ESTUDIO-TIERS.md §11.6`](ESTUDIO-TIERS.md):

- **Q1 Visibilidad = mixto** (🟢 sin badge, 🟡🟠🔴 con badge + aviso).
- **Q2 Techo de fuente única = decidir tras backfill** (mitigación M1 solo si RT25 confirma sesgo > 30 % en alguna categoría con n ≥ 5; aplicable solo a colectivos ciudadanos, tercer sector, sindicatos minoritarios y asambleas).
- **Q3 Default del paso 6 = 🟠 + alerta Telegram** al dispararse.
- **Q4 Política de cambios retroactivos = congelar** (correcciones vía `/correcciones/`).
- **Q5 Mockups visuales HTML = Fase 4** (mantiene pausa del prototipo del Bloque B).

Desbloquea PI10 (sistema de tiers público). Siguiente paso de implementación: `src/tiers.py` con `compute_tier(signals)` + `data/tiers.yml` con los valores cerrados + plantilla del badge + `/metodologia/#tiers` con el copy de §5.

---

## Leyenda de estados

- ⏳ pendiente — aún no tocada
- 🔄 en discusión — editor y Claude la están trabajando ahora
- ✅ cerrada — decisión tomada y docs actualizados
- ⏸ pausada — deliberadamente en espera

## Registro de progreso

| Código | Tarea | Estado | Notas |
|---|---|---|---|
| **RT1** | **Backfill empírico W10 antes de las 12** | ⏳ | **P-1 · antes del backfill grande** |
| **RT2** | **Rol editor vs muestreo 10% — decidir** | ✅ | **Cerrada 2026-04-23: opción 2 (eliminar muestreo). Añadida capa 5bis IA. Ver ESTUDIO-COSTES-AUDITOR** |
| **RT3** | **Tiers UX — validar con dos públicos** | ⏳ | **P-1 · antes de lanzar tiers** |
| **RT4** | **Techo cobertura + banner limitaciones + Vía A adelantada** | ⏳ | **P-1 · antes del relanzamiento. Banner de fase de rodaje aplicado en la home 2026-04-25 (parte mínima del audit de tecnicismos). Reescritura editorial profunda + Vía A de precios siguen pendientes** |
| **RT5** | **Tests básicos del pipeline** | ⏳ | **P-1 · absorbe cobertura de `audit.py`, `verify.py`, `balance.py`, `extract.py`, `rescue.py` con fixtures reales del backfill ([D4](DECISIONES.md))** |
| **RT6** | **Balance — rediseño con persistencia (tras 3 meses)** | ⏳ | **P-1 · diferido a ~julio 2026** |
| **RT7** | **build_index.py adaptado al schema documental** | ✅ | **Cerrada 2026-04-21 noche** |
| **RT8** | **Banner temporal en `/acerca/` + split acerca/metodo** | ✅ | **Split cerrado 2026-04-29: /acerca/ identidad breve, /metodo/ detalle técnico** |
| **RT9** | **Páginas mínimas (política editorial, método, correcciones)** | ✅ | **Cerrada 2026-04-29. `/politica-editorial/` y `/metodo/` creadas. `/correcciones/` ya existía.** |
| **RT10** | **LG1 + LG2 promovidas a alta — anonimato legal pre-relanzamiento** | ⏳ | **P-1 · antes de empuje público** |
| **RT11** | **Copy y tono de la home — decisión editorial** | ⏳ | **P-1 · en la etapa de Diseño, depende de RT3, RT12 y RT16** |
| **RT12** | **Vía A de precios — estudio en profundidad** | ⏳ | **P-1 · ALTA · adelantarla al pre-relanzamiento si el estudio da viable** |
| **RT13** | **Regla fundacional — automatización + niveles de veracidad públicos** | ✅ | **CLAUDE.md + /politica-editorial/ cerrados 2026-04-29** |
| **RT14** | **Estudio preciso de costes del auditor IA** | ✅ | **Cerrada 2026-04-23. Entregable: ESTUDIO-COSTES-AUDITOR.md. Régimen estable ~2,4 €/mes; backfill ~5,4 € one-shot. Desbloquea PI9** |
| **RT15** | **Re-estudio profundo del sistema de tiers** | ✅ | **Cerrada 2026-04-23. Entregable [`ESTUDIO-TIERS.md`](ESTUDIO-TIERS.md) completo. 5 decisiones operativas cerradas en [D9](DECISIONES.md) (mixto / congelar / 🟠 default / Q2 tras backfill / HTML en Fase 4). §8.5 medición empírica = RT25. Desbloquea PI10.** |
| **RT16** | **Experimento Claude Design — archivado** | 🔄 | **P-1 · archivo en `private/claude-design-experiment/` · no es referencia · se estudia en fase Diseño** |
| **RT17** | **Navegación exhaustiva mobile-first** | ⏳ | **P-1 · ALTA · NAVEGACION.md propio** |
| **RT18** | **Trilingüe ES/CA/EN desde el backfill** | ⏳ | **P-1 · ALTA · editor confirmó 22-abr: activar desde el backfill** |
| **RT19** | **Seguimiento visual de evolución de problemáticas** | ⏳ | **P-1 · DIFERENCIAL · formato por decidir** |
| **RT20** | **Estudio titular legal con detenimiento** | ⏳ | **P-1 · ALTA · bloquea empuje público** |
| **RT21** | **Precios — "Termómetro de precios" provisional** | ⏳ | **P-1 · nombre por revisar cuando proyecto más asentado** |
| **RT22** | **BOIB watcher — Fase 2 confirmado** | ⏳ | **P-1 · editor confirmó 22-abr · base legal presente desde relanzamiento** |
| **RT23** | **Framework de señales de tracción a 90 días** | ⏳ | **P-1 · DIFERIDO POST-LANZAMIENTO** |
| **RT24** | **Escenarios de lanzamiento y horizonte** | ⏳ | **P-1 · A soft mayo-junio / B rodaje 1 año** |
| **RT25** | **Medición empírica del sesgo de tiers por tipo de actor** | ⏳ | **ALTA · depende del backfill 12 sem (PI2-B) · cierra §8 de [`ESTUDIO-TIERS.md`](ESTUDIO-TIERS.md) · puede activar mitigación M1 en `data/tiers.yml`** |
| **RT26** | **Cierre de las 5 decisiones abiertas del estudio de tiers** | ✅ | **Cerrada 2026-04-23 con OK en bloque del editor. Ver [D9](DECISIONES.md) y [`ESTUDIO-TIERS.md §11.6`](ESTUDIO-TIERS.md). Desbloquea PI10.** |
| ED1 | Criterio OK propuestas | ✅ parcial | Editorial público cerrado 2026-04-29 (`/que-documentamos/`). Técnico interno (árbol verify.py, URLs caídas a posteriori) queda como tarea del pipeline |
| ED2 | Imparcialidad alertable | ⏳ | |
| ED3 | Presencia de Omisiones | ⏳ | |
| ED4 | Horizonte desde inicio | ✅ | Fecha origen W06 (3 feb 2026); disclaimer en /que-documentamos/ y /metodo/ |
| ED5 | Modo entrenamiento 4 semanas | ❌ | Descartada 2026-04-21, reemplazada por tiers+cuarentena |
| FU1 | Fuentes vivas | ⏳ | |
| FU2 | Queries Google News | ⏳ | |
| FU3 | Hora Ibiza + Nou Diari | ✅ | Hora Ibiza inexistente; Nou Diari incorporada a sources.yaml |
| FU4 | BOIB | ⏳ | |
| PI1 | Revisión pipeline | ⏳ | |
| PI2-A | Archivado append-only desde hoy | ✅ | Cerrada 2026-04-21, W17 snapshot ok |
| PI2-B | Backfill retroactivo 12 semanas | ⏳ | Tras PI2-A y PI9 |
| PI9-MVP | Auditor mínimo viable (2 sem) | ⏳ | Hito 1 del frame · capa 2 ciega + heurísticas + log con correcciones + protocolo 72 h ([D1](DECISIONES.md), [D2](DECISIONES.md), [D3](DECISIONES.md)) |
| PI9-Iteración | Iteración posterior del auditor (2-3 sem) | ⏳ | Tras cierre del Hito 1 · Opus formalizado + cuarentena + dashboard + capa 5bis |
| PI10 | Tiers de confianza públicos | ⏳ | Nuevo, Plan A aprobado |
| PI11 | Cuarentena pública /revision-pendiente/ | ⏳ | Nuevo, Plan B aprobado |
| PI12 | Alerta Telegram lunes enriquecida | 🔄 | Base implementada, upstream pendiente |
| PI13 | Notificación por email (futuro) | ⏳ | Baja prioridad |
| PI3 | Enlace entre ediciones | ⏳ | |
| PI4 | Datos abiertos disclaimer | ⏳ | |
| PI5 | Techos GitHub | ⏳ | |
| PI6 | Modelos IA docs | ⏳ | |
| PI7 | Costes completos | ⏳ | |
| PI8 | Página "cómo funciona" + tooltips | ⏳ | |
| UX1 | Mockup/wireframe | ⏳ | |
| UX2 | Navegación flagship | ⏳ | |
| UX3 | Dos públicos | ⏳ | |
| UX4 | Guía en fold | ⏳ | |
| UX5 | Balance accesible | ⏳ | |
| UX6 | Semana flaca | ⏳ | |
| UX7 | Avances/éxitos | ⏳ | |
| UX8 | Construir entera | ⏳ | |
| OP1 | Rectificación actor | ✅ | Cerrada 2026-04-29. Protocolo interno en `private/protocolo-correcciones.md` |
| OP2 | Health feeds — alertas proactivas | ✅ | Cerrada 2026-04-25. Calibración de umbrales pendiente de datos del cron (4-8 sem) |
| OP3 | Auto-recuperación de feeds caídos | ⏳ | Pendiente datos reales (3-4 caídas) que orienten qué espejos sirven |
| OP4 | Dashboard visual de estado de feeds | ⏳ | Decisión UX (privado/público) cuando haya 4-8 sem de `feed_health.json` |
| OP5 | Alerta al primer fallo aislado | ⏳ | BAJA · esperar señal real de demanda antes de bajar umbral |
| ID1 | Nombre definitivo `radar))ibiza_vivienda` | ✅ | Cerrada 2026-04-21 noche |
| LG1 | Anonimato legal | ⏳ | |
| LG2 | Portfolio sin nombre | ⏳ | |
| FI1 | Financiación | ⏳ | |
| EX1 | Test usabilidad | ⏳ | |
| EX2 | SEO schema.org | ⏳ | |
| EX3 | Estrategia lanzamiento | ⏳ | |
| EX4 | Backup repo | ✅ | Pull mirroring GitLab nativo; operativo desde 2026-04-29 |
| EX5 | Sanity check externo pre-lanzamiento | ⏳ | Nuevo, 50-100 € |
