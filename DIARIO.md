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

## 2026-05-05 [pipeline] — Trazabilidad como sexta dimensión del self-review + fix umbral n≥3 ([D22](DECISIONES.md#d22--trazabilidad-de-fuente-como-sexta-dimensión-del-self-review))

- **Disparador.** Alerta automática del self-review de la edición W19 (rigor=5, balance=6). Lectura crítica con el editor identificó dos problemas distintos: (1) bug del prompt del revisor que tira rigor a 5 cuando solo se ha auditado una propuesta y los dos lectores discrepan (n=1 → ratio=1.0 → fuera de rango → penalización obligatoria); (2) los warnings de fuentes agregadas y cifras sin origen citable se repiten en W17, W18 y W19, escondidos dentro de "rigor", sin un eje propio que permita atacarlos.
- **Fix del umbral.** El revisor sigue añadiendo warning sobre el desacuerdo Haiku↔Sonnet con muestra escasa pero no toca la nota de rigor por este motivo. Con n≥3 la regla original se mantiene. La nota de rigor sigue bajando si las cifras o las fuentes del cuerpo son flojas. Cubierto por D17 sin abrir decisión nueva.
- **Trazabilidad como sexta dimensión.** Añadida al prompt del revisor, al JSON de salida y al aviso de Telegram. Mide cifras con fuente identificable, fuente primaria vs agregador, agregadores etiquetados visiblemente, estimaciones con etiqueta inline de naturaleza. D22 abierta con revisión tras W20-W23 y tres criterios de revocación (dimensión constante / correlación con rigor / fuentes oficiales casi siempre).
- **Claridad en seguimiento.** Tres semanas dando 9 sin warnings concretos. Si tras W20-W21 sigue siendo dimensión muerta, propuesta de retirarla y consolidar en cinco dimensiones útiles. Apunte en `APRENDIZAJES.md`.
- **Loop de aprendizaje cerrado en commit aparte.** Las cinco sugerencias acumuladas de W18 y W19 (heredar tipología actor, cerrar items "a vigilar", marcar fuente agregada, generar lista de actores al final, identificar cargo público completo) van al prompt del generador. Detalle en `APRENDIZAJES.md` y commit `feat(generate)`.

---

## 2026-04-29 [pipeline] — Nou Diari incorporada como fuente RSS; Hora Ibiza descartada (FU3)

- **Hora Ibiza descartada.** El dominio `horadeibiza.com` no responde y el medio no tiene presencia rastreable. No es una fuente viable.
- **Nou Diari incorporada** (`https://www.noudiari.es/feed/`). Medio digital de Eivissa y Formentera, castellano, sin paywall. Publica 8-15 artículos/día con cobertura directa de vivienda, alquiler y trabajadores de temporada. Añadida como fuente nativa en `src/sources.yaml`. Entrará en el pipeline a partir del próximo cron del lunes.

---

## 2026-04-29 [editorial] — Horizonte temporal del observatorio aclarado en las páginas públicas (ED4)

- **Fecha de origen oficial fijada: semana del 3-9 de febrero de 2026 (W06).** Es la primera semana cubierta por el archivo retroactivo. "Primera vez documentada" significa siempre en este observatorio, no en la historia del debate.
- **Dos sitios actualizados:** sección *"Desde cuándo"* añadida a [`/que-documentamos/`](docs/que-documentamos.md) con párrafo explicativo; sesgo de horizonte temporal añadido a [`/metodo/`](docs/metodo.md) bajo *"Sesgos declarados"*.
- **Tooltip contextual diferido** a la fase de Diseño (depende del formato de la ficha de propuesta en la web final).

---

## 2026-04-29 [docs] — Cierre de RT8 y RT13 de la Revisión Fase 0.5

- **RT8 cerrada.** La decisión de estructura `/acerca/` + `/metodo/` estaba pendiente desde 2026-04-21; quedó resuelta en esta sesión al crear `/metodo/` con contenido completo (RT9). `/acerca/` ya es la página de identidad breve que se buscaba. Marcada como cerrada.
- **RT13 cerrada.** La regla fundacional de automatización máxima ya estaba publicada en `CLAUDE.md` (sección *Regla complementaria*) y en `/politica-editorial/` (sección pública). Solo faltaba marcarla formalmente.

---

## 2026-04-29 [arquitectura] — Copia de seguridad automática del repo fuera de GitHub (EX4)

- **Decisión cerrada: pull mirroring nativo de GitLab, sin tocar el repo.** GitLab copia el repo de GitHub cada hora de forma autónoma. No requiere GitHub Actions adicional, no requiere tokens (el repo es público), cero mantenimiento. Enfoque elegido frente a un workflow Actions porque el proyecto ya corre un cron semanal y 1 hora de desfase en el espejo es completamente asumible.
- **Pasos para configurar (una sola vez en la web de GitLab):** (1) Crear proyecto privado `ibiza-housing-radar` en gitlab.com. (2) Settings → Repository → Mirroring repositories. (3) URL: `https://github.com/otundra/ibiza-housing-radar.git`, dirección Pull, sin autenticación. (4) Guardar. El espejo se actualiza solo cada hora.
- **Coste:** 0 €. GitLab gratuito incluye pull mirroring para repos públicos.
- **Configurado y operativo** 2026-04-29.

---

## 2026-04-29 [editorial] — Página pública del criterio de admisión de propuestas (ED1, parcial)

- **Qué entra y qué no, escrito.** Creada [`docs/que-documentamos.md`](docs/que-documentamos.md) (`/que-documentamos/`) con los criterios reales que aplica el sistema, sintetizados desde tres lugares dispersos: filtro de fuentes y palabras clave (`src/sources.yaml`), prompt del clasificador Haiku (`src/classify.py`), prompt del extractor Sonnet + validador (`src/extract.py`) y verificador final (`src/verify.py`). La página cubre: tres puertas de admisión, tres tipos de propuesta (formal / en movimiento / descartada) con ejemplos reales del histórico W17-W18 y de noticias clasificadas como "ninguna" en la última corrida, reglas estrictas del sistema, niveles de fiabilidad ([D9](DECISIONES.md)) y procedimiento si el lector echa en falta una propuesta. Sin ningún ejemplo inventado.
- **Enlazada en footer** junto a las otras páginas estructurales y referenciada desde [`docs/metodo.md`](docs/metodo.md) y [`docs/politica-editorial.md`](docs/politica-editorial.md).
- **Tarea ED1 cerrada parcial.** La parte editorial pública está cubierta. El detalle técnico interno (árbol de decisión de `verify.py` ante errores HTTP, política de URLs que caen meses después, criterio de URL primaria vs secundaria) queda abierto como tarea del pipeline.
- **Coste.** 0 € de API.

---

## 2026-04-29 [diseno] — Páginas públicas de política editorial y método (RT9)

- **Dos páginas que faltaban y prometíamos.** Creadas [`docs/politica-editorial.md`](docs/politica-editorial.md) y [`docs/metodo.md`](docs/metodo.md), ambas en lenguaje llano para el lector público. La política editorial recoge las 5 reglas duras + la regla complementaria de automatización. El método explica el ciclo semanal en 8 pasos, los tres modelos de IA con su lógica de reparto, la taxonomía de actores (8 categorías), los sesgos declarados y lo que el observatorio no hace. Enlazadas desde `/acerca/` y añadidas al pie de todas las páginas. Las tres páginas exigidas por las reglas fundacionales (`/politica-editorial/`, `/metodo/`, `/correcciones/`) ya existen. Tarea RT9 de la Revisión Fase 0.5 cerrada.
- **Coste.** 0 € de API.

---

## 2026-04-29 [operacional] — Protocolo interno de correcciones (OP1)

- **Protocolo cuando llega una rectificación.** Creado `private/protocolo-correcciones.md`: guion paso a paso para el editor con los dos casos posibles (error de hecho verificable vs. reclamación de actor sobre interpretación), plazos (24 h acuse de recibo, 72 h resolución), criterio de decisión único (¿es un error de hecho comprobable con la fuente?), tres plantillas de respuesta, lista de qué no ceder bajo ningún concepto, y cuándo escalar si llega amenaza legal. Cierra el hueco entre la promesa pública de `/correcciones/` y la ausencia de proceso interno. Revisión anclada al Hito 3 legal. Tarea OP1 de la Revisión Fase 0.5 cerrada.
- **Coste.** 0 € de API.

---

## 2026-04-28 [editorial] — Régimen de rodaje pre-lanzamiento (D21) + rediseño Cronología/Radar + regeneración W17 y W18

Al revisar la edición W18 publicada el 27-abr salieron dos secciones espesas: la *Cronología* era un párrafo denso de prosa con todas las fechas embebidas (difícil de escanear), y la *Radar: señales en movimiento* mostraba 9 campos verticales por propuesta con la mitad rellenos de "ninguno registrado esta semana" / "no evaluada — sin evaluación pública". El editor preguntó si conviene hacer cambios solo desde W19 o también retroactivos a W17 y W18. Su lógica: la regla 1 fundacional (contenido editorial inmutable) protege el contrato con el lector, pero hoy no hay lector — la web no se ha empujado al público. Aplicarla durante la fase de prototipo congela formato cuando todavía estamos calibrando.

- **D21 nueva — régimen de rodaje pre-lanzamiento.** Mientras la web no esté empujada al público activamente, las ediciones publicadas son revisables libremente: formato, contenido editorial, estructura. Sin nota en `/correcciones/`, sin marca pública de *"edición corregida"*. Trigger del cierre del rodaje: compra del dominio definitivo, anuncio activo (newsletter/redes/prensa/comunicación a actores citados), o compartir URL fuera del círculo del proyecto con intención de que la lea. En ese momento se hace commit de cierre (`chore: cierre del rodaje`) y la regla 1 fundacional vuelve a operar plena. D21 supera parcialmente a D18 (política retroactiva del 27-abr) durante el rodaje. STATUS.md refleja el régimen actual en el bloque *Próximos hitos*.
- **Hito 3 (legal) diferido.** El editor confirmó que no le corre prisa hasta antes del empuje público. Apuntado en STATUS.md (marco de trabajo + próximos hitos). No bloquea nada del rodaje.
- **Rediseño de la Cronología.** Pasa de un párrafo de prosa a 3-8 bullets con fecha en negrita al inicio (`**Sáb 18**`, `**Dom 19**`, `**Lun 20**`). Mismo contenido editorial, estructura escaneable. Cambio en el prompt de `src/generate.py` líneas 80-93.
- **Rediseño del Radar y Propuestas en circulación.** Cabecera más limpia (actor + tipo + fuente en una línea, statement como párrafo sin etiqueta `**Qué:**`). Y regla dura nueva: omitir líneas de campos vacíos en vez de imprimir "ninguno registrado" / "no evaluada — sin evaluación pública". Si una viabilidad SÍ tiene evaluación, se imprime; si no, no aparece. Estado y Horizonte siempre se imprimen. Resultado: una propuesta sin evaluaciones ni apoyos pasa de ~16 líneas a ~6.
- **Script reutilizable `scripts/regen_week.py`.** Acepta `--week 2026-wNN`, lee datos de `data/archive/{YYYY-WNN}/` si existe (semana pasada) o de `data/` (semana en curso), llama a `src.generate.generate()` con `now=lunes 05:00 UTC` (igual que el cron real, para que `date:` del frontmatter quede coherente con la edición original) y escribe a `docs/_editions/{slug}.md`. Solo regenera el `.md`; no toca `proposals_history`, `balance`, `self_review` ni costes acumulados.
- **W18 y W17 regeneradas.** W18 tomada de `data/` actual; W17 de `data/archive/2026-W17/`. Cronología en bullets, Radar/Propuestas con campos vacíos omitidos. Frontmatter `date:` correcto (lunes original, no fecha de hoy). Carry-over funcionando. Validación: el verificador automático no se ha corrido en local porque el script no lo invoca — la próxima corrida del cron (W19) sí pasará por verify y, si algo está roto, lo veremos.
- **Coste real: ~1,17 €** distribuido en tres llamadas a Opus 4.7 (W18 con fecha mal por bug del script primer intento = 0,43 €, W18 buena = 0,34 €, W17 = 0,40 €). Mi estimación inicial fue *"~0,05 €"*: error grande, no consideré que el output de Opus 4.7 (~3000-4000 tokens) cuesta solo en salida ~0,30-0,40 € por corrida, aunque la caché del system prompt funcione bien. Apuntado en `data/costs.csv`. Sigue dentro del tope blando del mes (12 €), pero importa para futuras regeneraciones: cada corrida de Opus son ~0,40 €, no céntimos.
- **Lo que NO se tocó.** Layout HTML (`_layouts/edition.html` no toca estas secciones), CSS, frontmatter (mismos campos), métricas (`proposals_*_count` siguen calculados igual), `data/proposals_history.json` (no se regenera con este script — la próxima corrida del cron sí lo actualizará). Tampoco la página `/correcciones/`: como D21 establece, durante el rodaje no hace falta marca pública.

---

## 2026-04-28 [arquitectura] — Reformulación del cierre del Hito 1: calibración en vivo W19-W22 en vez de backfill de W10 (D20)

> Nota sobre numeración: en la misma sesión se detectó un hueco en `DECISIONES.md` — saltaba de D18 a D20 sin D19. El hueco entró en el commit `2b4baf8` del 2026-04-27 (D18 política retroactiva + D20 página `/propuestas/` añadidos juntos saltando un ID). Hoy se cierra renumerando la página `/propuestas/` de D20 a **D19** y asignando la decisión nueva del cierre del Hito 1 a **D20** (en una primera edición de la sesión se había escrito como D21). Excepción consciente a la regla *"nunca editar una fila cerrada"* (regla 1 del registro): el cambio toca solo el ID, no el contenido, y restaurar la correlación numérica vale más que la pureza append-only en este caso. Las referencias cruzadas en `STATUS.md`, `DISENO-AUDITOR-MVP.md`, `ROADMAP.md` y este `DIARIO.md` quedan sincronizadas en el mismo commit.

Al revisar qué tocaba para Fase 4 del auditor MVP, salió el problema de fondo: la Fase 4 estaba descrita como *"backfill solo de la semana W10 (2-8 marzo 2026)"* pero el repo no tiene datos de W10, la ingesta solo recupera ventana RSS reciente (`lookback_days: 10`), y no existe `src/backfill.py` (es tarea de Fase 2 del ROADMAP, no de Fase 1). Mientras tanto, la Fase 3 ya integró el auditor en `src/report.py` y desde W18 corre vivo en el pipeline. El commit-back persiste `data/audit/` cada lunes (verificado en el workflow línea 91, fix del 2026-04-27). Calibrar antes de seguir bloqueaba Fase 2 sin mejorar lo que el cron en vivo ya da gratis cada lunes.

- **D20 nueva.** El criterio de cierre del Hito 1 pasa de *"prueba empírica sobre el backfill de W10"* a *"primera corrida limpia del cron en W19 + revisión de métricas tras 3-4 ediciones consecutivas (W19-W22)"*. Las métricas a revisar siguen siendo las del §10 del plano del auditor (ratio de disputas en rango saludable, coste <0,50 €/edición, 11 señales pobladas, ninguna heurística silenciosa, edición pública legible). Próxima revisión tras W22. Criterio de revocación triple: muestra insuficiente, ruido en producción, o ediciones perdidas.
- **D1 *Próxima revisión* apunta a D20.** El campo se reescribe siguiendo la práctica establecida tras D15 (los campos de revisión son metadata operativa actualizable; la decisión en sí no se edita).
- **Plano del auditor reformulado.** `DISENO-AUDITOR-MVP.md` actualiza §1 (cierre del Hito 1), §9 (Fase 4 entera, pasa de ~5-8 h a ~2-3 h distribuidas en 4 lunes) y §10 (criterio 1 de éxito).
- **Docs vivos sincronizados.** `STATUS.md` (Hito 1 en activo + en curso) y `ROADMAP.md` (Fase 1, tres líneas) actualizados al criterio nuevo.
- **Lo que NO se toca.** Las menciones tangenciales a W10 en D4 ("validación empírica = corrida sobre W10") y `REVISION-FASE-0.5.md` se mantienen intactas — su decisión principal no cambia (D4: tests diferidos a RT5; REVISION: el RT1 sigue siendo válido como tarea de Fase 2 para evaluar viabilidad del backfill grande). D20 las supera operativamente sin invalidar el archivo cerrado.
- **Coste.** 0 € de API. Solo edición de documentos.

---

## 2026-04-27 [editorial] — Página `/propuestas/`, política de actualización retroactiva (D18) y tercer bug del commit-back

Tres piezas que cierran un hueco del observatorio: hasta hoy no había vista global del histórico de propuestas. El lector solo veía cada edición aislada; la agregación se quedaba dentro de `data/proposals_history.json` sin salida pública. Resuelto con la página `/propuestas/` (D19) y, de paso, política clara para actualizaciones retroactivas (D18) y un tercer bug encontrado en el commit-back.

- **Página `/propuestas/` (D19).** Vista global del histórico, agrupada por estado (implementada → en ejecución → aprobada → en debate → en movimiento → propuesta → descartada → judicial → desconocido). Cada tarjeta lleva actor + tipo, resumen, palanca, horizonte, edición de origen y fuente original. Generada por [`src/build_proposals.py`](src/build_proposals.py) que lee `data/proposals_history.json`. Integrada en el cron tras `build_index`. Enlace en menú principal. CSS mínimo (`.prop-*`) en `main.css`. Sin filtros JS en V1 — agrupación por estado es suficiente para escanear con los ~3-30 elementos esperados a corto plazo. Validada con preview Jekyll local: layout limpio, navegación con anclas funciona, sin errores de consola.
- **Política de actualización retroactiva (D18).** Tres categorías con políticas distintas para no romper la promesa documental: contenido editorial (texto del análisis) **no se toca** (regla 5 cubre correcciones); metadata estructurada (tipologías, etiquetas, estados) **se actualiza retroactivamente sin marca pública**; presentación visual (CSS, layout) **libre**. Sienta el principio que rige cómo aplicar futuras mejoras al histórico sin contradecir el modelo documental.
- **Tercer bug del commit-back.** El workflow no incluía `data/proposals_history.json` ni `data/feed_health.json` en el `git add`. Por eso el histórico de propuestas se quedó congelado en W17 (3 entradas) aunque el cron W18 publicó 7 propuestas nuevas. Mismo patrón exacto que los dos bugs anteriores (self-review y audit). **Consecuencia visible:** la página `/propuestas/` arranca con solo las 3 propuestas históricas; las del W18 entrarán en el repo cuando el próximo cron actualice el JSON. Si el editor quiere acelerar, se puede regenerar localmente desde la edición W18 publicada.
- **Tareas apuntadas en ROADMAP** ([Diferido con criterio claro](ROADMAP.md)). Rediseño de la sección "Cronología" en las ediciones (hoy un párrafo denso de prosa) y rediseño de la sección "Radar: señales en movimiento" (hoy ~30 líneas de viñetas verticales por propuesta, espesa de leer). Ambas se ejecutan juntas porque tocan la misma plantilla y prompt.
- **Coste.** 0 € de API. Todo es estructura, plantilla, CSS y script de lookup.

## 2026-04-27 [pipeline] — Formato unificado de notificaciones Telegram + fix de auditoría interna perdida

Tras la corrida W18 llegaron tres avisos por Telegram (éxito del pipeline, score bajo de la autoevaluación) sin separación visual entre ellos, el aviso de score bajo era críptico (no explicaba qué era ni qué hacer) y solo el resumen final llevaba el coste mensual — los demás avisos no llevaban coste de ninguna clase. Resuelto centralizando el formato en `src/notify.py`: cada mensaje sale con cabecera de separador + cuerpo + pie común con coste de edición y mes acumulado.

- **Cabecera y pie unificados.** `notify._wrap_message()` envuelve cualquier mensaje con un separador `━━━━━━━━━━━━━━━━━━` al inicio y un pie `Edición YYYY-WNN: X,XX € · Mes YYYY-MM: X,XX €` al final. El pie se calcula con `edition_spend_eur(slug)` y `current_month_spend_eur()`. Si el cálculo falla (CSV ausente en local, datos vacíos, etc.) el pie se omite — la notificación sigue saliendo.
- **Aviso de éxito final más limpio.** Como el pie ya trae los costes, `report.py` deja de meterlos en el cuerpo del mensaje. El cuerpo queda con identidad + URL pública + recuento de propuestas + actores + capa de color. Resultado: una sola línea de costes (en el pie), sin duplicación.
- **Aviso de score bajo autoexplicativo.** El mensaje de `self_review.py` cuando alguna nota cae bajo umbral 7 ahora explica qué es la autoevaluación (segunda lectura interna con Sonnet 4.6), la escala (1-10), incluye una descripción corta de cada dimensión afectada (rigor → "cifras o generalizaciones sin trazabilidad"; balance → "actores concentrados") y termina con acción concreta. Antes el editor recibía solo "rigor: 5, balance: 6" sin contexto.
- **Fix de auditoría interna perdida.** Detectado al comprobar local: el archivo `private/self-review/2026-w18.md` que el bot generó en el runner **no estaba en el repo**. Causa: el `git add` del workflow `weekly-report.yml` solo incluía `private/costs.md` y `private/panel.md`, no la carpeta `private/self-review/` ni el log `private/self-review-log.md`. Bug existente desde el primer self-review. Añadidos al commit-back. Toda la auditoría interna queda accesible en local desde la próxima corrida.
- **Coste.** 0 € de API. Cambios de presentación y configuración del workflow.
- **Próximo cron lunes** estrenará el formato. El detalle del self-review W18 ya no se va a perder cuando el cron vuelva a correr (aunque el de esta semana ya se perdió: solo lo vimos en el aviso truncado de Telegram).

## 2026-04-27 [pipeline] — Sistema de auto-recuperación en tres capas tras incidente W18

El cron del lunes a las 05:00 UTC abortó con dos fallos en cadena: clasificador truncó la respuesta JSON al procesar 67 noticias (la opening de los clubs disparó volumen) y, al arreglarlo, salió a la luz un segundo fallo oculto (parámetro `temperature` deprecado en Opus 4.7). Tras dos relanzamientos manuales la edición W18 publicó (~0,70 € de coste). El incidente expuso que la promesa editorial *"cada lunes una edición"* dependía de que el editor estuviese delante del Telegram. Resuelto con sistema de auto-recuperación en tres capas. Detalle en [D16](DECISIONES.md).

- **Fix 1 — techo del clasificador.** `max_tokens` de 4.096 → 16.384 en `src/classify.py`. Cubre ediciones con hasta ~180 noticias sin riesgo de truncado. Solo se cobra lo emitido, no el techo.
- **Fix 2 — parser tolerante a respuestas cortadas.** Función `_salvage_truncated_array` en classify: si llega JSON cortado, recorta al último cierre de objeto válido y procesa lo recuperable. La red de seguridad ya existente cubre los items perdidos con fallback conservador.
- **Fix 3 — quitar `temperature` de Opus 4.7.** La API ya no admite ese parámetro en Opus 4.7. Quitado de `src/generate.py`. No afecta al output (modelo usa su default).
- **Capa 1 — reintentos automáticos transitorios.** `max_retries=5` en los 5 clientes Anthropic (classify, extract, audit, generate, self_review). El SDK reintenta con back-off exponencial ante 408/409/429/5xx y errores de conexión. Cubre saturación temporal de la API sin que el editor se entere.
- **Capa 2 — auto-relanzar tras push de fix.** Workflow nuevo [`auto-retry.yml`](.github/workflows/auto-retry.yml) se dispara con cada push a `src/**` en main. Tres guardias antes de relanzar: (a) marca de fallo viva, (b) edición de la semana actual no publicada, (c) cooldown de 5 min desde último intento. Si las tres se cumplen, dispara `weekly-report.yml`.
- **Capa 3 — marca persistente + check de recuperación + coste por edición.** Marca `data/PIPELINE_FAILED.flag` se escribe al fallar y se borra al recuperar; viaja con el commit-back. El siguiente run la lee al arrancar y, si publica bien, el aviso lleva prefijo *"✅ Recuperado tras fallo de [edición]"*. Workflow ahora corre el commit con `if: always()` para que la marca sobreviva a abortos. Aviso de éxito incluye dos costes: edición concreta + mes acumulado.
- **Coste de la edición W18.** ~0,70 € (clasificar 0,03 € + extraer 0,02 € + auditor 0,02 € + generate Opus con caché 0,60 € + self-review 0,03 €). Mes 2026-04 acumulado en capa 🟢 verde.
- **Coste del nuevo sistema.** 0 € de API. Todo es lógica de orquestación.
- **Trazabilidad de costes mejorada.** Hasta hoy, las llamadas de classify/extract/extract_validate se etiquetaban como `adhoc` en `data/costs.csv` porque `report.py` no propagaba la variable `EDITION`. A partir de W19 todas las llamadas de un lunes irán etiquetadas con la semana, lo que permite agregar coste real por edición. La función `edition_spend_eur(slug)` en `costs.py` lo calcula con matching case-insensitive (tolerante al formato histórico mixto W17/w17).
- **Pendiente.** Validar el flujo completo en el próximo incidente real: (a) que un fallo deje marca correctamente, (b) que un push tras alerta dispare auto-retry, (c) que el aviso de recuperación llegue. Decisión D16 con criterios de revocación claros si aparecen bucles o enmascaramiento.

## 2026-04-25 [editorial] — Auditoría de tecnicismos en cara pública: 9 fixes aplicados

Tarea de relleno mientras esperamos al cron del lunes. Revisión página a página de todo lo que el lector ve (home, /balance/, /ediciones/, /correcciones/, edición W17, footer) cazando jerga técnica prohibida por las dos reglas de lenguaje del proyecto. Se aplicaron los 9 fixes detectados + las 2 notas, en cuatro commits atómicos. La cara pública queda libre de códigos crudos, números de semana ISO y referencias internas.

- **Fix crítico 1 — footer reescrito.** El texto anterior "Las propuestas son sugerencias generadas por IA" contradecía la regla 2 (el observatorio NO genera propuestas). Sustituido por "Documenta propuestas formuladas por actores con nombre y fuente verificable". También fuera "Automatización con Claude API"; entra "Sin tracking de terceros" para alinear con `/acerca/`.
- **Fix crítico 2 — códigos taxonómicos traducidos.** Nuevo módulo `src/labels.py` con cuatro mapas (actor_type, palanca, state, horizon) desde snake_case a frases legibles ("en_debate" → "En debate", "coalicion_institucional" → "Coalición institucional", "oferta_vivienda" → "Oferta de vivienda", "enforcement" → "Aplicación de norma"). Lo importan `build_index.py`, `balance.py` y `generate.py`. Idempotente: si llega texto ya legible pasa intacto. Toda la home, todo `/balance/` (público y privado) y la edición W17 quedan limpios.
- **Fix crítico 3 — números de semana ISO fuera de etiquetas visibles.** Eliminado el `<span>{{ e.week }}</span>` del listado `/ediciones/` que imprimía "2026-W17" debajo de cada item. La fecha (2026-04-20) y el título ("Semana 4 - Abril 2026") ya transmiten el periodo. La numeración ISO queda como metadata interna (frontmatter, slug de URL, logs). Carry-over de la edición W17 también se reformula con rango de fechas humano.
- **Fix crítico 4 — enlace muerto y ruta interna fuera de `/balance/`.** Retirado el enlace a `/metodologia/` (página inexistente) y la mención a `data/proposals_history.json` (jerga técnica). Sección Metodología simplificada a una frase con anuncio de página dedicada en preparación.
- **Fixes de estilo.** "pipeline lee la prensa" → "sistema automático lee" en el bloque sobre el proyecto de la home. "URL caída" → "enlace caído" en `/correcciones/`. Emojis fuera de todos los H2 de la edición W17 ("📡 Señales detectadas" → "Señales detectadas", etc.).
- **Generación futura blindada.** El SYSTEM prompt de `generate.py` se actualiza para emitir labels en el cuerpo (`<state_label>`, `<horizon_label>`, `<actor_type_label>`) y mantener códigos solo en el frontmatter (`blocks_cited`). Carry-over con rango de fechas humano (lunes-domingo de la semana anterior). Regla emoji endurecida: "no uses emojis en ningún lugar del documento". Próximas ediciones nacerán ya limpias.
- **Verificado en navegador.** Home, `/balance/`, `/ediciones/`, edición W17 y `/correcciones/` revisados con preview Jekyll vivo. Sin códigos crudos visibles, sin enlaces rotos, sin errores de consola. Todas las páginas conservan layout y enlaces internos.
- **No tocado.** Los 8 prototipos en `docs/prototype/` ya tenían `<meta name="robots" content="noindex,nofollow">` desde antes — Nota A del audit cumplida sin acción. Reescritura editorial profunda de copia (titulares, "Cada lunes...", tono general) queda para más adelante: depende de cerrar tiers de confianza y la decisión de Vía A en la revisión Fase 0.5, que están en cola del Hito 1.
- **Coste.** 0 € de API. Trabajo enteramente local + Jekyll.

## 2026-04-25 [pipeline] — Salud de fuentes RSS con alertas proactivas (OP2)

Cerrado OP2 de la revisión Fase 0.5 mientras esperamos al cron del lunes que validará la Fase 3 del auditor. El pipeline ya no es ciego ante caídas o degradación silenciosa de los RSS: si una fuente deja de publicar, baja la frecuencia o cambia de estructura, el editor recibe un aviso consolidado por Telegram.

- **Módulo nuevo `src/sources_health.py`.** Dos funciones: `record_run()` añade la ejecución actual al histórico append-only `data/feed_health.json` (solo escribe cuando `GITHUB_ACTIONS=true`; las corridas locales solo evalúan en memoria), y `evaluate_alerts()` pura sin I/O devuelve mensajes humanos para Telegram.
- **Cuatro reglas de alerta calibrables.** Fuente caída (2 ejecuciones seguidas con fallo), estructura cambiada (bozo cuando antes era ok), bajada de noticias (>50 % vs media de los 4 runs anteriores) y vacío inesperado (ok pero 0 entradas con base ≥5). Validadas con histórico sintético — las 4 disparan correctamente, el caso sano devuelve `[]`. Umbrales se ajustarán cuando haya 4-8 semanas de `feed_health.json` real.
- **Integración mínima en `src/ingest.py`.** Recolecta métricas por feed (estado, totales, kept, en ventana, excepción) durante la iteración existente y al terminar llama a sources_health. Las alertas se consolidan en un único mensaje por ejecución vía `notify.py` con `level=warning`. Cualquier fallo del módulo se loguea pero no bloquea la edición — la editorial es prioritaria.
- **Tres ideas registradas como tareas a futuro en `REVISION-FASE-0.5.md`.** OP3 auto-recuperación de feeds caídos (probar URLs alternativas; pendiente datos reales de qué espejos sirven), OP4 dashboard visual del estado de feeds (decisión de UX pendiente, privado vs público), OP5 alerta al primer fallo aislado (bajar umbral solo si llega ruido real). Las tres con condición de revisión clara — no implementar preventivamente.
- **Coste y disparo.** 0 € de API. La primera escritura real del histórico ocurre el lunes 05:00 UTC en el cron.

Siguiente paso natural: tras la corrida del cron del lunes (que estrenará OP2 y validará Fase 3 del auditor), abrir Fase 4 del auditor sobre la semana W10 del 2-8 marzo 2026.

---

## 2026-04-25 [editorial] — Banner de fase de rodaje en home + refinamientos en /acerca/ (RT4, RT8)

Cierre de la parte mecánica de RT4 (techo de cobertura + banner de limitaciones) y RT8 (banner temporal en /acerca/). Lo que queda abierto en ambas es decisión editorial profunda que depende de inputs ausentes (RT3 test de usabilidad, tiers en producción, Vía A de precios): se cierra hoy solo lo que no requiere esos inputs.

- **Banner persistente en la home.** Nuevo `docs/_includes/banner_rodaje.html` con copy que se compromete públicamente: *"Hoy todavía no es fuente primaria: el módulo de precios con datos propios llegará en una fase posterior"*. Layout `home.html` lo inyecta antes del contenido. Estilos en `assets/css/main.css` reusando tokens existentes (`--accent`, `--accent-bg`, `--max-dash`) — sin variables nuevas. Verificado en el preview Jekyll: render correcto en escritorio y móvil, claro y oscuro.
- **Tres pequeñas ediciones a `/acerca/` alineadas con el banner.** Sección nueva *"En fase de rodaje"* entre la intro y el bloque de Método. Aviso del pie reescrito: *"Este observatorio documenta — no opina ni propone"* (más nítido que el genérico anterior). Promesa muerta a `/financiacion/` reemplazada por *"Si esto cambia, se publicará aquí con detalle"* — sin enlazar páginas que no existen.
- **Por qué la parte mecánica cierra y la decisión editorial profunda no.** El banner protege contra el malentendido del primer visitante: alguien que lo ve sin contexto no debe creer que es fuente primaria de precios. Eso ya se entrega. La pieza editorial que falta (separar `/acerca/` en quién-lo-edita y `/método/` en cómo-funciona, reescribir copy de la home con los tiers visibles, ajustar tono al lector profesional) depende de inputs futuros y se aborda cuando se retome Diseño.

Archivos tocados: `docs/_includes/banner_rodaje.html` (nuevo), `docs/_layouts/home.html`, `docs/assets/css/main.css`, `docs/acerca.md`.

---

## 2026-04-25 [arquitectura] — Auditor MVP fase 3 cerrada (registro JSON + integración + página /correcciones/)

Tercer trozo del auditor mínimo construido sobre lo que dejaron las fases 1 y 2 esta misma sesión. El plano (DISENO-AUDITOR-MVP.md §9) parte la fase 3 en cinco entregables; los cuatro que dependen del editor cierran ahora. El quinto (corrida end-to-end en edición piloto) se dispara solo cuando el cron lunes ejecute la próxima vez — código y docs listos para que ocurra sin intervención.

- **`write_audit_log()` y `audit_proposals()` en `src/audit.py`.** Escriben JSON append-only en `data/audit/YYYY-wWW/{proposal_id}.json` con el esquema completo del registro de auditoría (§3.1 del plano). Si el archivo ya existe, lanzan `FileExistsError`; el orquestador lo registra con aviso y sigue. El identificador de propuesta viene de `extracted.json` (formato estable `YYYY-wWW-NNN` desde la edición de la W17). Cruce extraído ↔ clasificado por URL, no por índice (evita desfase tras los filtros previos).
- **Paso `audit` integrado en `src/report.py`.** Entre `rescue` y `generate`. La edición se sigue componiendo igual; el auditor solo escribe en paralelo. Si el módulo falla, el plano §6.2 lo deja como modo silencioso del MVP — no aborta el pipeline. Visible en el orden del orquestador: ingest → classify → extract → rescue → audit → generate → verify → ...
- **Señal `auditor_disputes_ratio` en `src/self_review.py`.** Función nueva `auditor_signal()` lee los JSON de la semana, calcula `propuestas_disputadas / propuestas_auditadas`, lo compara con el rango saludable [0.08, 0.25] de [`ESTUDIO-COSTES-AUDITOR.md §12.1`](ESTUDIO-COSTES-AUDITOR.md), y mete el bloque entero en el envío al revisor Sonnet. Prompt del sistema actualizado: si `en_rango: false`, el revisor anota un aviso concreto y baja la nota de `rigor` a 6 o menos. Si hay propuestas marcadas para revisión manual, las cita por id.
- **Página `/correcciones/` mínima en `docs/correcciones.md`.** Layout `page`, permalink limpio, protocolo de 72 h, registro público vacío de momento. Buzón `correcciones@radaribiza.com` y formulario quedan etiquetados *próximamente*. Enlace al inicio del bloque de pie en `docs/_includes/footer.html`. Verificado con la previsualización Jekyll en :4000.
- **Buzón aplazado al cierre del Hito 3 legal.** El editor preguntó por dejar `correcciones@radaribiza.com` operativo en el momento. Se aplazó con tres bloqueos: el dominio `radaribiza.com` no está comprado, el nombre `radar))ibiza_vivienda` sigue siendo provisional ([D2](DECISIONES.md)), y abrir un buzón antes de cerrar el estudio legal del titular añade exposición que no toca asumir. Se queda en *próximamente* hasta que se cierre el Hito 3.
- **Prueba sin coste de extremo a extremo.** `python -m src.audit --dry-run` reusa la salida de Haiku como capa 2 ficticia y escribe los 3 JSON con el esquema completo. Re-ejecutar dispara el `FileExistsError` esperado. Validación: archivos creados, esquema completo, regla de no sobreescribir respetada.
- **Coste real de Fase 3.** 0 € de API (corrida sin llamadas reales con datos en disco). La primera ejecución real con cron del lunes debería sumar ~0,01-0,02 € a la línea `audit_blind` del registro de costes (proyección §6.1).

Siguiente paso natural: Fase 4 (prueba empírica sobre la semana W10 del 2-8 marzo 2026 para calibrar umbrales antes del backfill completo de 12 semanas).

---

## 2026-04-25 [arquitectura] — Auditor MVP fase 2 cerrada (heurísticas + whitelist + bloque signals)

Encadenado a la fase 1 en el mismo turno. Tres comprobaciones deterministas sin IA + lista blanca de actores + hueco para los tiers.

- **Tres archivos nuevos.** `src/audit_heuristics.py` con las tres heurísticas: cruce de fuentes (cuántos dominios distintos cubren la propuesta en la misma semana), coincidencia textual del verbatim contra el cuerpo de la URL fuente (con caché HTTP local en `.cache/http/`, TTL 30 días) y encaje dominio-actor contra la whitelist. `data/actor_domains.yml` con la whitelist V1 cerrada en 20 actores y 12 medios. `scripts/test_audit_phase2.py` para corrida manual sin API.
- **Extensiones a `src/audit.py`.** Helper `build_signals()` que combina comparador + heurísticas (+ verify cuando esté disponible) en las 11 señales del registro de auditoría. Función `compute_tier(signals)` como hueco — siempre devuelve `value=null`, `reason='pendiente_estudio'`, y conserva el bloque signals para que la fórmula real (PI10) lo lea cuando se conecte el estudio de tiers.
- **Caché HTTP en `.gitignore`.** Carpeta `.cache/` añadida. La primera corrida real bajó tres páginas (~820 KB) y a partir de ahora reutiliza el cuerpo durante 30 días sin pegar al medio.
- **Validación con datos reales.** Las 3 propuestas de la última edición pasaron la corrida con las 11 señales pobladas en cada una. Cruce de fuentes dio `[1, 2, 2]` (la propuesta de Marí en cadenaser.com queda single-source; las dos coaliciones por residencias temporeros tienen dos diarios cubriendo). Encaje con whitelist dio `[debilita, debilita, neutro]`. Coincidencia textual real entre verbatim y cuerpo del artículo dio ratio 1.000 cuando la propuesta apunta a su propia URL fuente, y 0.65-0.93 en cross-checks (verbatim de A contra cuerpo de B).
- **Dos apuntes para la Fase 4 (calibración con la semana W10 del 2-8 marzo 2026).**
   1. *Huecos esperables de la whitelist V1.* `cadenaser.com` y `lavozdeibiza.com` no están en la lista de medios aceptados; coaliciones largas (`"Consell d'Eivissa, patronales, sindicatos"`) no casan con la entrada simple del actor. Refinamiento previsto en la revisión post-backfill ([D3](DECISIONES.md)).
   2. *Ruido en la coincidencia textual.* La métrica actual (suma de `matching_blocks` de `SequenceMatcher` dividida por la longitud del verbatim) es generosa: cross-checks de verbatim de A contra cuerpo de B sacan ratios 0.65-0.93 sólo por solapamiento de vocabulario común (`Ibiza`, `alquileres`, `residencias`). Calibrar umbrales o cambiar a *longest contiguous match / len(needle)* tras ver la distribución sobre 12 propuestas reales de W10.
- **Coste real de Fase 2.** 0 € de API. Tres descargas HTTP de páginas públicas. Caché ya escrita en `.cache/http/` para futuras corridas.

Siguiente paso natural: Fase 3 (registro JSON append-only en `data/audit/YYYY-wWW/`, integración del paso `audit` entre `extract` y `generate` en `src/report.py`, página `/correcciones/` mínima publicada).

---

## 2026-04-25 [arquitectura] — Auditor MVP fase 1 cerrada (segunda lectura ciega + comparador)

Primer trozo del auditor mínimo viable construido y verificado de extremo a extremo sobre datos reales. El plano de obra (DISENO-AUDITOR-MVP.md §9) parte la construcción en cuatro fases; esta entrada cierra la primera. Sin integración aún con el pipeline principal — el auditor todavía no se enchufa al cron semanal.

- **Tres archivos nuevos.** `src/audit.py` con `run_blind_audit()` lanza una llamada batch a Sonnet 4.6 con el mismo prompt y mismo payload que ya usa Haiku en `src/extract.py`, sin ver la salida de la primera lectura. `src/audit_compare.py` con `compare_extractions()` compara las dos fichas campo a campo y clasifica los desajustes en `critical` / `minor` / `none` siguiendo el árbol del plano (5 campos críticos, 4 menores, umbral textual sobre `statement_verbatim` con `SequenceMatcher`). `scripts/test_audit_phase1.py` permite probar manualmente con dos modos: `--dry-run` (sin API, valida el comparador con casos sintéticos) y modo real con cuota.
- **Ajuste sobre el plano.** El árbol de severidad citaba campos `viability_political`, `viability_tecnica` y `statement_type` que no existen en la ficha real que emite `EXTRACT_SYSTEM`. El comparador usa los campos reales (`viability_legal`, `viability_economic`, `actor_type`) y deja documentado el ajuste en su propio docstring. `statement_type` entrará cuando se añada a la ficha en una fase posterior.
- **Validación con datos reales.** Corrida sobre 4 propuestas de la última edición con tipo `formal` o `en_movimiento`. Coste real 0,042 € (4 propuestas + 4 llamadas), muy por debajo de la proyección del estudio de costes. Resultado del comparador: 1 ficha idéntica, 2 desajustes críticos legítimos (los dos modelos discrepan de verdad sobre el actor), 1 caso de número distinto de propuestas entre las dos lecturas.
- **Tres apuntes registrados para fases siguientes** (no bloquean el cierre; cada uno tiene mitigación prevista en el plano).
   1. **Desajustes cosméticos en nombres de actor.** Sonnet emite el nombre con prefijo institucional completo (*"Patronales y sindicatos de Ibiza"*) donde Haiku usa la forma corta. Disparan severidad `critical` aunque el actor es el mismo. Mitigación: **Fase 2 vía whitelist de dominios + alias de actor** (`data/actor_domains.yml`), que normalizará nombres antes de comparar.
   2. **Número distinto de propuestas entre las dos lecturas.** En 1 de las 4 noticias, Haiku encontró 1 propuesta y Sonnet encontró 0 (porque la noticia citaba un actor distinto al *hint* de la ficha; ambos modelos siguieron la regla bien, pero llegaron a partes distintas del titular). Mitigación: **Fase 3 vía señal explícita en el registro de auditoría** (`layers.compare.count_mismatch`), de modo que `compute_tier()` real (PI10) pueda penalizar.
   3. **Sonnet desviándose ocasionalmente del actor declarado.** En 1 caso, Sonnet emitió una ficha con un actor que no aparecía en el *hint*. Con un prompt idéntico, una segunda lectura ciega no garantiza que respete los mismos contratos. Mitigación: **iteración posterior al Hito 1** vía capa 4 Opus formalizada como árbitro (hoy es fallback implícito en `src/extract.py`).
- **Documentos sincronizados.** Plano del auditor con las marcas `[x]` en los tres entregables de Fase 1 (§9). Estado operativo movido a *"Fase 1 cerrada, Fase 2 en curso"*. Esta entrada del diario.
- **Coste acumulado del cierre de fase.** Validación + corrida de prueba: 0,046 USD ≈ 0,042 €. Capa de costes en verde holgada; el dashboard interno (`private/costs.md`) y el tablero (`private/panel.md`) lo recogen al regenerarse.

Siguiente paso, ya en marcha en este turno: arrancar Fase 2 (heurísticas deterministas + whitelist V1 + caché HTTP local + hueco para `compute_tier()`).

---

## 2026-04-24 [docs] — Sin calendario público ni fecha de lanzamiento. El ritmo lo marca el editor

Tras redactar el plano del auditor con su calendario de 4 semanas fechadas (28 abr – 25 may) y tras haber fijado el 23-abr lunes 13 jul 2026 como fecha objetivo de relanzamiento ([D11](DECISIONES.md)), el editor cortó en seco: *"vamos a olvidarnos de las fechas, no son reales. no hay fechas de lanzamiento, ni nada por el estilo"*. Registrado como [D15](DECISIONES.md) y aplicado de golpe.

- **Decisión paraguas.** El proyecto no tiene fecha de lanzamiento público, calendario de fases con rango día-día, ni objetivos del tipo *"relanzamos el lunes X"*. Todo se organiza por **hitos** (qué queda cerrado) y por **esfuerzo relativo** cuando aporta (*"~10 h de trabajo del editor"*), nunca por fecha futura.
- **Por qué.** Ninguna de las fechas propuestas era real. Mantenerlas forzaba un sistema (panel con decisiones vencidas, avisador semanal) que apuntaba a metas imaginarias y creaba sensación falsa de atraso en cada mirador del lunes. Más honesto borrar la ficción que mantenerla.
- **Efecto en el registro de decisiones.** [D11](DECISIONES.md) queda superada por [D15](DECISIONES.md) (se mantiene como histórica). Las *"Próximas revisiones"* de [D1](DECISIONES.md), [D3](DECISIONES.md), [D4](DECISIONES.md), [D6](DECISIONES.md), [D9](DECISIONES.md) y [D14](DECISIONES.md) se reescriben como eventos o hitos (*"al cerrar el Hito 1"*, *"tras el backfill"*, *"tras 2-4 ediciones"*), no como fechas ISO. La pregunta abierta del editor de la mañana (*"¿pueden las caducidades ser por hito?"*) queda resuelta: sí, y son el único formato aceptado salvo *"permanente"*.
- **Efecto en los documentos vivos.** [STATUS.md](STATUS.md) pierde el bloque de próximos hitos con fecha (lunes 27 abr, viernes 8 may, lunes 13 jul, lunes 12 oct). El plano del auditor pasa de *"Semanas 1-4 (fechas)"* a *"Fases 1-4"* sin calendario en [`DISENO-AUDITOR-MVP.md §9`](DISENO-AUDITOR-MVP.md). [ROADMAP.md](ROADMAP.md) cabecera y sección de estimaciones reescritas; [ESTUDIOS-PENDIENTES.md §6](ESTUDIOS-PENDIENTES.md) archivada como histórica.
- **Efecto en el código de monitorización.** No toco código. El avisador semanal (`src/decisions_watch.py`) seguirá leyendo *"Próxima revisión"*: como casi ninguna decisión tendrá fecha ISO parseable, quedará silencioso — comportamiento correcto (no hay nada que avisar). El tablero interno (`private/panel.md`) mostrará las revisiones pendientes como texto libre en vez de con orden temporal en la próxima regeneración. Si con 2-4 ediciones el sistema no dispara nada, [D14](DECISIONES.md) contempla simplificar o desmantelar.
- **Qué sí se mantiene.** Fechas históricas (cuándo se tomó una decisión, cuándo salió una edición, rangos reales de semanas publicadas como la W10 del 2-8 mar 2026, fechas de commits). El calendario editorial de *temporada/pre-temporada* sigue anclado a *opening/closing* reales de Ibiza: es dato observable, no objetivo de lanzamiento.

Archivos tocados: registro de decisiones (D11 superada + D15 nueva + 6 *Próximas revisiones* reescritas + D14 con criterio de revocación ajustado), estado operativo, plano del auditor, roadmap, estudios pendientes, y este diario.

---

## 2026-04-24 [arquitectura] — Plano de obra del auditor mínimo viable

Tras cerrar el sistema de monitorización y confirmar con el editor arrancar Hito 1, se redacta el documento de diseño del módulo de auditoría. No es un estudio nuevo: el estudio de costes ya estaba cerrado desde 2026-04-22 con todas las decisiones económicas y de alcance. El plano traduce ese estudio a contratos de código: qué archivos nuevos, qué funciones, qué estructura exacta del registro de auditoría, qué señales de confianza se capturan desde el primer día aunque la fórmula llegue más tarde, qué whitelist arranca cerrada, qué hueco deja para la iteración posterior.

- **Nuevo documento [`DISENO-AUDITOR-MVP.md`](DISENO-AUDITOR-MVP.md) (~500 líneas, 11 secciones).** Módulos a crear (`src/audit.py`, `src/audit_compare.py`, `src/audit_heuristics.py`, `data/actor_domains.yml`). Estructura completa del registro JSON con 11 señales de confianza (9 se rellenan en el mínimo viable, 2 se dejan en null a la espera de la fórmula de asignación). Tres heurísticas deterministas (confirmación por fuente cruzada, coincidencia literal, dominio en lista blanca). Lista blanca V1 cerrada con 20 actores en 6 de las 8 categorías de la taxonomía. Integración al flujo actual como paso nuevo entre extract y generate. Plantilla mínima de la página de correcciones con protocolo 72 h publicado. Calendario partido en 4 semanas con entregables por semana.
- **Por qué el diseño ahora y no durante el estudio.** El estudio de costes resolvió el *qué y cuánto* (alcance de capas, fórmulas de coste, dimensionado del backfill, ratio de disputas). El plano resuelve el *cómo*: contratos de funciones, forma del registro, puntos exactos de integración, criterios de éxito. Separarlos permitió no mezclar discusión económica con discusión técnica, y deja el estudio como referencia estable para revisiones futuras.
- **Riesgos explícitos dejados por escrito.** La página de correcciones queda publicada con protocolo de 72 h antes de que el buzón sea operativo; el editor acepta el riesgo acotado mientras la web no tiene tráfico, con apunte de revisión legal antes del relanzamiento público (anclado al Hito 3 legal). La fórmula de asignación de tiers se deja explícitamente fuera del mínimo viable: las señales se capturan y se guardan, pero el badge público no aparece hasta cerrar el estudio correspondiente (queda el estudio cerrado pero la integración pasa a iteración posterior).
- **Pregunta abierta del editor registrada.** ¿Pueden las caducidades del registro de decisiones ser por hito además de por fecha? (Por ejemplo: *"revisar al cerrar Hito 1"* en lugar de una fecha ISO.) Recomendación del asistente: dejar apuntado para la revisión del sistema de monitorización fijada al 2026-05-08, no implementar ahora. Añadido al apunte de esa fecha.
- **Estado al cierre del turno.** Plano entregado, estado operativo sincronizado (hito 1 en curso con diseño cerrado, calendario de 4 semanas apuntado, puntos de entrada actualizados), diario al día. La construcción empieza cuando el editor dé visto bueno al plano.
- **Propagación posterior del puntero.** Tras el commit del plano, se sincronizan las referencias en los cuatro documentos vivos que hablaban del auditor sin señalarlo: el registro de decisiones ([D1](DECISIONES.md) añade el plano a docs afectados), la hoja de ruta ([`ROADMAP.md`](ROADMAP.md) Hito 1 punto 1), la auditoría fundacional ([`REVISION-FASE-0.5.md`](REVISION-FASE-0.5.md) entrada PI9-MVP) y el estudio de costes ([`ESTUDIO-COSTES-AUDITOR.md §10.0`](ESTUDIO-COSTES-AUDITOR.md) con nota destacada). Aplicación directa de la regla *"propagar decisiones cerradas a todos los docs vivos"*.

---

## 2026-04-24 [docs] — Sistema de monitorización de decisiones del proyecto

El editor pidió panel único, alertas a Telegram y normas permanentes sobre las decisiones del proyecto — *"ligero pero potente"*. Diagnóstico previo identificó cuatro capas de vigilancia ya montadas (costes, autoevaluación semanal, verificación por capas, balance trimestral) pero dispersas. Decisión: no duplicar, agregar. Registrada como [D14](DECISIONES.md).

- **Formato del registro ampliado con dos campos obligatorios.** `Próxima revisión` (fecha ISO o `permanente`) y `Criterio de revocación` (qué señal rompería la decisión). En D0-D13 se añadió retroactivamente solo `Próxima revisión`; el criterio no se redactó hacia atrás porque la mayoría caen como permanentes o están cerca de hito natural. Estado de D10 corregido a superada parcialmente por D13 (tiers de arranque sustituidos por los 4 modos + ampliar); el índice de comandos que introdujo D10 sigue vigente.
- **Regla permanente en el documento de instrucciones.** Cuarta regla de gestión documental: toda decisión nueva exige los dos campos. Sin ellos, no entra al registro. Cierra el círculo sin depender de memoria.
- **Tarea automática semanal** (`src/decisions_watch.py`, enganchada al workflow lunes 05:00 UTC). Avisa por Telegram si alguna decisión tiene revisión vencida o próxima (≤7 días). Reutiliza `src/notify.py` sin infra nueva.
- **Refuerzo en el arranque de Claude.** Cualquier modo de arranque cita las decisiones vencidas en primera línea si las detecta al leer el registro. Triple red con Telegram y tablero.
- **Tablero interno único** en `private/panel.md` (nuevo, vía `src/panel.py`). Agrega gasto del mes, estado de verificación, autoevaluación, decisiones con revisión pendiente, última edición. No genera datos propios: solo agrega lo que otros módulos ya escriben. Primer tablero generado hoy; siguiente revisión fechada es la propia D14 el 2026-05-08.

**Pendientes apuntados (revisar 2026-05-08):** panel público en `/estado/` diferido hasta ver una semana del interno funcionando. Aviso por patrón estructural en autoevaluación (dos semanas seguidas con nota <7 en misma dimensión). Aviso por acumulación de 5 decisiones pequeñas autónomas del asistente sin resumen al editor.

**Coste real:** 0 € de API. Todo el trabajo es pegamento sobre capas ya existentes. Reversibilidad completa en <15 min (criterio de revocación explícito en D14).

Archivos tocados: registro de decisiones (14 decisiones con campo retroactivo + D14 nueva + estado de D10 corregido), documento de instrucciones del proyecto (regla 4 nueva), estado operativo (recordatorio 2026-05-08), dos módulos Python nuevos, workflow semanal ampliado con dos pasos, tablero interno nuevo, y este diario.

---

## 2026-04-24 [docs] — Reglas fundacionales migradas de PIVOTE.md a CLAUDE.md

- **Migración de las 5 reglas duras y la regla complementaria** a `CLAUDE.md §Reglas fundacionales`. El contenido operativo vive ahora en el documento principal; PIVOTE.md queda como archivo histórico con redirect. Motivo: consolidar el modelo documental en un solo sitio y que borrar PIVOTE.md en el futuro no rompa nada.
- **18 archivos actualizados** para apuntar a `CLAUDE.md#reglas-fundacionales`. Entradas históricas del diario intactas. El único enlace activo que queda a PIVOTE.md es el de CLAUDE.md línea 49 (aposta, contexto histórico del cambio de modelo).

---

## 2026-04-24 [docs] — Rediseño del sistema de arranque: fuera el intermedio, dentro el total con inventario veraz y el comando transversal de ampliar

Segundo turno del mismo día, continuación natural del anterior. Cuatro cambios conceptuales al cómo arranca la sesión, registrados en [D13](DECISIONES.md).

- **Se elimina `/arranque-fase` (el intermedio).** El editor señaló que raramente tenía claro cuándo usarlo: las sesiones son o pequeñas (el ligero basta) o grandes (el profundo hace falta); el caso intermedio (*"hoy toco diseño una mañana"*) se cubre mejor con un comando de ampliación puntual que con un arranque completo.
- **Nuevo `/arranque-total`.** Escaneo del proyecto sin huecos para los pocos casos donde hace falta tener literalmente todo sobre la mesa (pivote, auditoría integral, reestructura documental profunda). Flujo calibrado: inventario silencioso de carpetas → contraste con el mapa conocido del documento de instrucciones → lectura de cabeceras **solo de archivos nuevos o raros** → presentación al editor de **solo la lista de exclusiones razonadas** → confirmación en una línea → lectura en profundidad. Sin reglas codificadas que se puedan desincronizar; cero mantenimiento del archivo del comando. Uso esperado: 2-3 veces al año como mucho.
- **Nuevo `/ampliar [área o descripción]`.** Comando transversal para cargar documentos de un área concreta del proyecto sin sacar informe. Usable tras cualquier arranque (para subir de nivel sin repetir síntesis) o como carga puntual al empezar. Dos formas: palabra clave (*diseño, auditor, tiers, costes, legal, pipeline, contenido, seo, modelos, docs, web*) o descripción libre que el asistente interpreta.
- **Los dos arranques anteriores (ligero y profundo) siguen iguales.** Solo se limpian referencias al intermedio eliminado.

**Por qué la versión calibrada del total (cabeceras de novedades) y no la ambiciosa (cabeceras de todo):** leer cabeceras de los ~80 archivos del proyecto cada vez cuesta lo suyo. Como al arrancar ya tengo cargado el mapa de estructura del documento de instrucciones, el 90 % de las decisiones de exclusión están resueltas sin releer nada. Solo hace falta leer cabeceras de lo que aparece en la estructura real pero no en el mapa, que suele ser un puñado de archivos. Relación coste/beneficio mucho mejor.

Docs tocados: dos comandos nuevos, uno eliminado, dos actualizados (ligero y profundo), el documento de instrucciones del proyecto, el índice de comandos, y este diario + el registro de decisiones.

---

## 2026-04-24 [docs] — Arranque por defecto sin informe, recomendaciones 1-3 en los tres arranques, lenguaje llano en chat y refuerzo de cero códigos sueltos

Cuatro cambios en cómo el asistente arranca y habla en este proyecto, registrados en [D12](DECISIONES.md) tras un turno en el que el editor señaló dos fricciones a la vez: el arranque explícito sacaba informe aunque él ya traía la tarea definida, y cuarta recaída del patrón de códigos sueltos (*"sigues mencionando códigos RT26/Q1-Q5 sin explicar que son, lo he dicho mil veces y sigues haciendolo"*).

- **Arranque por defecto sin informe.** Al abrir sesión sin invocar ningún comando, el asistente lee los tres documentos clave en silencio (estado, decisiones, diario reciente) y responde directo al prompt del editor. El informe ordenado, las recomendaciones y la pregunta *"¿qué hacemos?"* solo se disparan cuando el editor escribe `/arranque` explícito.
- **Recomendaciones 1-3 en los tres comandos de arranque.** Paso nuevo tras la síntesis y antes de la pregunta de cierre, en los tres niveles. Entre 1 y 3 recomendaciones según haya (sin forzar las tres), una línea cada una, nombre de la cosa primero, verbo de acción + por qué corto + identificador opcional entre paréntesis al final.
- **Lenguaje llano en el chat del proyecto.** Nueva memoria del asistente (`feedback_lenguaje_llano_chat.md`) y sección nueva en el documento de instrucciones del proyecto: bajar un punto el nivel técnico al hablar con el editor. Traducciones de ejemplo: *flujo* en vez de *pipeline*, *registro* en vez de *log*, *estructura* en vez de *schema*, *diferencias* en vez de *diff*, *envío* en vez de *payload*. La palabra técnica sigue siendo precisa en documentos internos de arquitectura, estudios y código; en la conversación se traduce. Alcance solo este proyecto.
- **Cero códigos sueltos en chat — tolerancia cero.** Refuerzo de la regla ya existente con redacción más dura tras la cuarta recaída. Siempre el nombre de la cosa primero; el identificador va entre paréntesis al final y solo si aporta trazabilidad. Nunca como etiqueta principal, nunca como primer elemento de una línea. Memoria `feedback_referencias_con_contexto.md` reescrita con las cuatro fechas de recaída y la regla ejecutiva definitiva. Próxima recaída = fallo grave.

Archivos tocados: el documento de instrucciones del proyecto, el índice de comandos, los tres archivos de arranque, el registro de decisiones (D12 nueva), este diario, y dos memorias del asistente (una endurecida, otra nueva).

---

## 2026-04-23 [docs] — Sistema de arranque de sesión en tres niveles + índice vivo de comandos

El editor expuso el patrón recurrente al abrir sesión: *"no tienes todo el contexto y te tengo que decir escanéalo todo"*. Respuesta: tres escalones de arranque con coste escalado + índice vivo.

- **`/arranque` (Tier 1, default).** Lee STATUS, DECISIONES y últimas entradas del DIARIO; síntesis de 200 palabras y pregunta *"¿qué hacemos?"*. Cubre el 80 % de sesiones (continuaciones, tareas pequeñas).
- **`/arranque-fase` (Tier 2).** Añade PLAN, ARQUITECTURA y el estudio del área (costes del auditor, tiers de confianza, diseño, contenido retroactivo, gestión documental). Para pausas mayores a una semana o cambios de foco.
- **`/arranque-auditoria` (Tier 3).** Escaneo completo de capa fundacional + todos los estudios + módulos de `src/` cuando toque. Uso escaso (aprox. 15-20 mil tokens).
- **[`COMANDOS.md`](COMANDOS.md) en raíz.** Índice vivo con todos los slash commands del proyecto + los globales. Regla: todo comando nuevo entra en la tabla en el mismo commit que lo crea.
- **Puntero en [`CLAUDE.md`](CLAUDE.md).** Sección *"Cierre de sesión"* ampliada a *"Slash commands del proyecto"* con enlace al índice, para que el contexto auto-cargado recuerde que existen.
- **Regla nueva en memoria.** Si una tarea pide más contexto del cargado, el asistente avisa en el mismo turno con opción concreta (*"¿leo X?"*, *"¿lanzo `/arranque-fase`?"*) antes de ejecutar. Memoria `feedback_avisar_si_falta_contexto.md`.
- **Separador visual del bloque `/cierre`.** Nueva convención: el comando abre y cierra con línea de guiones para distinguirlo visualmente del resto de la conversación ([`.claude/commands/cierre.md`](.claude/commands/cierre.md)).
- **Registrado como [D10](DECISIONES.md).**

---

## 2026-04-23 [docs] — Modelo de tiempos del proyecto + fecha de relanzamiento lunes 13 jul 2026

El editor avisó que no tomaba en cuenta las estimaciones del proyecto porque mezclaban tres cosas bajo la misma etiqueta: *"2 semanas"* significaba a veces calendario, a veces esfuerzo técnico que el asistente desbroza en una tarde, a veces esfuerzo real del editor a ritmo sostenible. Convención nueva registrada en [D11](DECISIONES.md):

- **Calendario** = semanas de reloj real. Marca la fecha de lanzamiento.
- **Esfuerzo editor** = horas reales del editor. Ritmo sostenible asumido = 15 h/sem. Cuello de botella.
- **Esfuerzo Claude** = horas del asistente. No colapsa calendario, porque decisión/revisión del editor es el límite real.

Formato corto en docs: *"N sem calendario / ~M h editor"*. Sección *"Cómo leer las estimaciones de tiempo"* añadida al principio de [`ROADMAP.md`](ROADMAP.md).

**Fecha de relanzamiento cerrada:** lunes 13 jul 2026 (opción A de las tres analizadas). Recomendación del asistente era B (12 oct, cierre de temporada) por narrativa y holgura, pero el editor eligió A porque A cabe si los supuestos se cumplen (15 h/sem sostenido, sin imprevistos mayores, sin re-alcances, prueba empírica del auditor pasa a la primera). Escenario B queda como red de seguridad automática: si el ritmo no acompaña, el banner de rodaje absorbe el deslizamiento sin re-planificar.

**Docs propagados:** [`DECISIONES.md`](DECISIONES.md) D11, [`ROADMAP.md`](ROADMAP.md) (sección nueva + fecha objetivo en cabecera), [`STATUS.md`](STATUS.md) (próximos hitos con fecha 13 jul), [`ESTUDIOS-PENDIENTES.md`](ESTUDIOS-PENDIENTES.md) §6 marcada como superada. Las estimaciones existentes del roadmap se reinterpretan como calendario hasta que se reescriban gradualmente con la convención nueva.

---

## 2026-04-23 [arquitectura] — Cierre del estudio de tiers de confianza con 5 decisiones operativas

Tras el segundo pase del estudio del mismo día, el editor da OK en bloque a las cinco recomendaciones del asistente sobre las preguntas abiertas (§11 del estudio). Registrado como [D9](DECISIONES.md) y en [`ESTUDIO-TIERS.md §11.6`](ESTUDIO-TIERS.md):

- **Visibilidad de los tiers = mixto.** 🟢 se publica sin badge visual (asumido). 🟡 / 🟠 / 🔴 llevan badge + copy de aviso. Coherente con la filosofía editorial ("confía por defecto, señala excepciones").
- **Techo de fuente única = decidir tras backfill.** Regla dura en vigor hasta entonces. La medición empírica (RT25) decide si se relaja la regla solo para colectivos ciudadanos, tercer sector, sindicatos minoritarios y asambleas cuando el dominio es oficial del actor, y solo si el sesgo detectado supera el umbral.
- **Default del paso 6 del árbol = 🟠 + alerta Telegram.** Combinaciones raras de señales se publican con aviso, no cuarentena. Alerta al canal del editor para ampliar el árbol cuando se repita.
- **Política de cambios retroactivos = congelar.** El tier se calcula una vez al publicar y queda inmutable en el log. Cambios de umbrales afectan solo a propuestas nuevas. Si un cambio destapa errores en pasadas, corrección vía `/correcciones/`.
- **Mockups visuales HTML = Fase 4.** Los mockups textuales de §9 del estudio bastan para validar el árbol y el copy. Los HTML se integran cuando se retome el prototipo del Bloque B.

**Efectos en el roadmap:** RT15 ✅ y RT26 ✅ cerradas en la tabla de progreso; Hito 2 de la Fase 1 queda cerrado conceptualmente (falta medición empírica de sesgo = RT25, que depende del backfill, y la implementación técnica = PI10). El auditor mínimo viable sigue su curso escribiendo `signals` en el log, y `compute_tier()` real se conecta cuando se construya PI10 sin migrar logs antiguos.

**Decisión del asistente al cierre:** no se crea `data/tiers.yml` todavía. El YAML nace junto a `src/tiers.py` dentro de la tarea PI10, no como documento conceptual aislado. El estudio lo deja especificado con ejemplo completo (§4.2) para que la construcción sea copiar-pegar con ajustes.

---

## 2026-04-23 [sesion] — Estudio de tiers casi cerrado (primer + segundo pase) + refuerzo de la regla de no citar códigos internos

Turno largo tras el cierre del experimento de aprendizaje. Tres ítems:

- **Primer pase del re-estudio del sistema de tiers de confianza** en [`ESTUDIO-TIERS.md`](ESTUDIO-TIERS.md). Secciones 1-3 redactadas: punto de partida (qué se aprobó rápido el 21-abr y qué falta), 10 señales computables del auditor (consenso IA, arbitraje Opus, 5 checks de verificación técnica, cruce de fuentes, whitelist, viabilidad, tipo de declaración), y árbol de decisión determinista en 6 pasos (bloqueantes → techos duros → camino 🟢 → 🟡 → 🟠 → default).

- **Segundo pase del mismo estudio** en el mismo turno tras OK del editor. Secciones redactadas: §4 umbrales ajustables (YAML en `data/tiers.yml` + política de cambios retroactivos = congelar), §5 copy público llano por tier con tabla de palabras prohibidas → traducciones, §6 interacción con cuarentena y tres caminos de promoción, §7 historia del tier con `tier.history[]` append-only y regla de cuándo se muestra, §8 al 50 % (diseño del método de medición de sesgo por tipo de actor + 4 mitigaciones candidatas; la medición empírica se posterga hasta tener el backfill de 12 semanas), §9 mockups textuales (ficha, lista, cuarentena, dashboard, home), §10 plan de test con usuarios (n=5, 6 preguntas, métricas), §11 lista de 5 preguntas al editor (Q1 visibilidad, Q2 relajación del techo de fuente única, Q3 default del paso 6, Q4 política de cambios retroactivos, Q5 mockups visuales ahora o en Fase 4).

- **Tareas nuevas en el roadmap** para lo que no se puede cerrar aún: **RT25** (medición empírica del sesgo por tipo de actor tras backfill 12 semanas, con `scripts/tier_bias_audit.py` y posible activación de mitigación M1 en el YAML) y **RT26** (cierre de las 5 decisiones abiertas del estudio, editor contesta Q1-Q5). Fichas existentes actualizadas: **RT1** (backfill piloto W10) ahora incluye línea sobre medir distribución preliminar 🟢/🟡/🟠/🔴 y validar expectativa 70/20/8/2 antes del backfill grande. **RT3** (test UX de tiers) ahora apunta al §10 del estudio como plan operativo. Reflejadas en la tabla de seguimiento de la revisión fundacional y en el Hito 2 de la Fase 1 del roadmap.

- **Refuerzo de la regla de no citar identificadores internos al editor sin nombrar primero la cosa.** Tercera recaída en dos días (listé *"RT15 · Sistema de tiers de confianza"* con el código como etiqueta principal; el editor: *"tras mil veces decirlo, no menciones códigos tipo RT1 sin explicar que son. no miro los codigos"*). Acciones: (a) regla añadida a [`CLAUDE.md`](CLAUDE.md) sección *"Qué NO hacer"* con redacción dura ("próxima recaída es fallo grave"), (b) memoria `feedback_referencias_con_contexto.md` reforzada con tolerancia cero — el código no va delante ni como etiqueta principal ni siquiera con glosa detrás; nombrar por el nombre de la cosa, ID opcional entre paréntesis al final solo si aporta trazabilidad.

**Estado del estudio al cierre del turno:** solo pendiente contestar las 5 preguntas del editor (RT26) y ejecutar la medición de sesgo tras backfill (RT25). Lo demás está redactado y es base suficiente para que el auditor mínimo viable siga escribiendo `signals` sin bloqueo.

---

## 2026-04-23 [docs] — Retirado el experimento APRENDIZAJE.md

Abortado a petición del editor tras una sola sesión de uso. Motivo: no aportó señal útil (ambas entradas eran auto-reflexión del asistente, no feedback para el editor) y el coste al cierre no compensa. La reversibilidad diseñada en [D8](DECISIONES.md) funcionó — desmontaje en minutos. Quitado: archivo `APRENDIZAJE.md`, Paso 6 del `/cierre`, bullet de feedback en el reporte final, menciones en `CLAUDE.md` y `STATUS.md`. [D8](DECISIONES.md) marcada revocada. Lección para futuras propuestas del asistente: el ejemplo en el prompt original era ambiguo — "cómo el editor desarrolla el proyecto" se puede leer como auto-reflexión o como feedback al editor; sin definición clara del sujeto el mecanismo no funciona. Si se vuelve a intentar, definir primero qué tipo concreto de feedback (carga, rumbo, alcance, etc.) y con formato de 2 líneas máximo.

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
