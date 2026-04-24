# Estudios pendientes antes o durante Fase 0

**Fecha:** 2026-04-20
**Origen:** decisiones del editor 2026-04-20 tras presentación del expediente del cambio de modelo (reglas fundacionales en [CLAUDE.md](CLAUDE.md#reglas-fundacionales)).
**Uso:** cada punto es un estudio específico que necesita trabajo analítico propio antes de tomar la decisión final. Ninguno bloquea el arranque del pipeline técnico y del contenido retroactivo, pero algunos condicionan el lanzamiento público.

---

## 1. 🔴 URGENTE — Integración de los tres modelos de IA (Haiku + Sonnet + Opus)

**Contexto:** hoy el pipeline usa Haiku (clasificar) y Opus (componer). El editor pide valorar integrar también Sonnet para repartir carga, optimizar coste y calibrar calidad por tarea.

**Mapa mental del reparto por modelo (hipótesis a validar):**

| Tarea | Modelo ideal | Motivo |
|---|---|---|
| Clasificar noticia (is_housing, actor, palanca) | **Haiku 4.5** | Tarea estructural simple, coste marginal |
| Detectar si hay propuesta explícita en la noticia | **Haiku 4.5** | Patrón lingüístico simple |
| Extraer ficha estructurada de la propuesta (actor, estado, viabilidad) | **Sonnet 4.6** | Requiere comprensión + clasificación matizada; Haiku puede fallar, Opus es overkill |
| Verificar vigencia de propuestas del rescate | **Haiku 4.5** | Sí/no sobre contexto acotado |
| Fact-check de precedentes externos | **Sonnet 4.6** | Haiku puede alucinar confianza, Sonnet calibra mejor |
| Componer edición semanal completa | **Opus 4.7** | Pieza editorial principal, donde sí importa el matiz |
| Auditoría trimestral de balance (análisis cualitativo) | **Opus 4.7** | Razonamiento complejo sobre corpus |

**Coste estimado por edición con reparto de 3 modelos:**

| Fase | Modelo | Coste/edición (€) |
|---|---|---|
| Clasificación | Haiku | 0,015 |
| Detección propuestas | Haiku | 0,010 |
| Extracción estructurada | Sonnet | 0,18 |
| Rescate (vigencia) | Haiku | 0,005 |
| Fact-check precedentes | Sonnet | 0,08 |
| Generación | Opus (con cache) | 1,40 |
| **Total/edición** | | **~1,69 €** |
| **Total mes (4 eds)** | | **~6,76 €** |

Comparado con propuesta original (solo Haiku + Opus, ~5,85 €/mes), el coste sube ~0,90 €/mes a cambio de mejor calibración de calidad por tarea. Sigue dentro del tope blando 8 €.

**Preguntas a resolver:**

1. ¿Qué tareas caen mejor en Sonnet vs Haiku? Benchmark con 20 noticias reales.
2. ¿El prompt caching funciona igual en los 3 modelos? (sí en Opus, confirmar en Sonnet/Haiku).
3. ¿Hace falta fallback? (p.ej. si Sonnet falla, caer a Haiku con prompt simplificado, nunca parar el pipeline).
4. ¿Se puede pasar contexto de clasificación a extracción sin repetir tokens? (sí vía cache).
5. Coste trilingüe revisado: Sonnet ya se usaba para traducción CA/EN; integrarlo en el pipeline principal amortiza mejor.

**Entregable del estudio:** documento `ESTUDIO-3-MODELOS.md` con benchmark + decisión de reparto + código de `classify.py`, `extract.py`, `verify.py` con modelo por fase configurable.

**Plazo:** ejecutar en la primera semana del arranque de Fase 0, antes de producir el contenido retroactivo para que las 8 ediciones se beneficien del nuevo reparto.

### 6 criterios de evaluación por tarea

Tras reunión con editor 2026-04-20, se amplían a **6 criterios**:

1. **Calidad contra gold standard.** Output comparado con solución ideal sobre dataset curado. Métricas: precisión, recall.
2. **Coste real en €.** Tokens × precio × ratio de caché.
3. **Robustez contra alucinación** (crítico para "cero inferencia" del editor). Zero-tolerance en extract y verify.
4. **Cumplimiento de instrucciones estrictas.** % de respuestas que respetan las 5 reglas duras sin reintento.
5. **Fiabilidad técnica.** JSON malformado, timeouts, variabilidad entre ejecuciones idénticas.
6. **Impacto real (correcciones recibidas / edición).** Proxy directo de calidad percibida. Se mide a partir del segundo mes cuando `/correcciones/` acumule datos. Si el modelo barato genera >2× correcciones que el caro, el ahorro se paga en credibilidad. **Esta variable entra en el re-benchmark mensual, no en el benchmark inicial (no hay datos acumulados todavía).**

### Re-benchmark continuo (cada 4 semanas)

Con los 5 criterios iniciales + el 6º cuando haya datos, el benchmark se re-ejecuta cada mes con 10 noticias nuevas. Módulo `src/model_rebench.py` descrito en [ARQUITECTURA.md](ARQUITECTURA.md#srcmodel_rebenchpy-nuevo--re-benchmark-mensual-de-modelos).

Objetivos:

- Detectar modelos nuevos que cambien el ratio calidad/coste.
- Detectar degradación silenciosa de versiones actuales.
- Detectar cambios de precios de Anthropic.
- Validar que el 6º criterio (impacto real) confirma o contradice la decisión original.

Coste: ~1 €/mes. Se convierte en parte del presupuesto operativo permanente.

### Filosofía de afinado continuo

No queremos pagar de más, pero si un modelo superior multiplica el impacto (menos correcciones recibidas, mejor cobertura editorial, menos sesgo), compensa el precio. La variable 6 cuantifica esto.

Regla operativa: **el reparto de modelos se revisa cada trimestre** con datos reales de los 4 re-benchmarks intermedios + el trimestre de auditoría Opus. Si cambia, se aplica al mes siguiente.

---

## 2. Dominio propio — estudio previo antes de comprar

**Contexto:** decidido que compraremos dominio, pero el editor quiere valorar con calma las opciones antes.

**Preguntas a resolver:**

1. Nombre: `radaribiza.org`, `habitatgeibiza.org`, `observatoriovivienda.org`, `habitatge.cat` (si disponible), `radar.eivissa`, otros.
2. Extensión: `.org` (ONG/sin lucro), `.cat` (Països Catalans, alinea con bilingüe futuro), `.es`, `.com`, `.net`.
3. Registrador: Namecheap, Porkbun, OVH, Cloudflare Registrar (sin markup).
4. Whois privacy incluido (protege datos del editor en registro público).
5. DNS: gestión en el registrador o Cloudflare (añade CDN gratis).
6. Plan de migración de `otundra.github.io/ibiza-housing-radar` a dominio propio con redirección 301 completa para no perder SEO.
7. Impacto en emails (ver estudio 5).
8. Coste anual real (comparar registradores).

**Criterios para elegir nombre:**

- Memorable en catalán y castellano.
- Corto (≤15 caracteres).
- Pronunciable por alguien que lo oye por primera vez.
- Libre de connotaciones.
- Disponible `.org` y si puede `.cat` para futuro bilingüe.

**Entregable:** documento `ESTUDIO-DOMINIO.md` con shortlist de 3-5 candidatos, comprobación de disponibilidad, recomendación con justificación. El editor compra.

**Plazo:** antes de abrir al público. Sin fecha ([D15](DECISIONES.md)).

**Apunte editor 2026-04-20:** cuando se elija dominio, **reevaluar también el nombre del proyecto** ("Ibiza Housing Radar"). Puede que quede corto, largo, o que no encaje con el dominio elegido. Mantener página `/radar/` funciona independientemente del nombre final del proyecto (el juego semántico con "radar" se conserva aunque el proyecto cambie de nombre).

---

## 3. Página `/recursos/` — qué incluir y cómo verificar

**Contexto:** decidido que NO va en Fase 0, pero sí se estudia para lanzar en Fase 1.

**Preguntas a resolver:**

1. Qué servicios son realmente útiles y accesibles para afectados.
2. Cómo verificar cada teléfono, horario y dirección (llamada directa, no web).
3. Qué pasa cuando un recurso cambia (cómo mantenemos el listado vivo).
4. Cómo evitar la responsabilidad implícita: la página debe dejar claro que no sustituye a servicios sociales profesionales.
5. Idiomas: muchos temporeros no hablan castellano; el listado debería incluir al menos versión inglesa.
6. Formato accesible en móvil con teléfonos clicables (`tel:` links).
7. ¿Integrar con un `/emergencia` más prominente para casos graves?

**Riesgos a cubrir:**

- Desactualización (un teléfono que ya no funciona es peor que no dar el teléfono).
- Saturación de los servicios mencionados si el tráfico crece.
- Responsabilidad percibida: evitar que el proyecto se convierta en intermediario no deseado.

**Entregable:** documento `ESTUDIO-RECURSOS.md` + página lista para lanzar en Fase 1 (primer mes post-relanzamiento).

**Plazo:** Fase 1.

---

## 4. Newsletter de pago vs gratis vs híbrido

**Contexto:** el editor plantea newsletter de pago con la tesis "el que no paga que mire la web". Valoración inicial hecha en la respuesta conversacional del 2026-04-20.

**Conclusión preliminar:**

- **Pago puro: no.** Contradice misión, mercado demasiado pequeño, rompe citabilidad, asimetría web/email absurda.
- **Gratis puro: sí en Fase 0** como base de distribución.
- **Modelo híbrido (gratis base + tier Pro opcional): evaluar en Fase 2** cuando haya datos de audiencia.

**Tier Pro — valor diferencial propuesto (todo por definir):**

- Dataset agregado con granularidad fina (tendencias mensuales, tablas cruzadas).
- Adelanto del lunes (edición llega el sábado al suscriptor Pro).
- Resumen mensual ejecutivo con análisis de tendencias que no va en las ediciones semanales.
- CSV extendido con metadatos.
- Posible newsletter mensual "entre bambalinas" sobre errores detectados y correcciones.
- Acceso a mesa redonda anual (Fase 4.4 del PLAN).

**Preguntas a resolver (en Fase 2):**

1. ¿Hay tracción suficiente para que la conversión sea relevante?
2. Precio: 3, 5, 7, 10 €/mes. Anualidad con descuento.
3. Qué infraestructura: Buttondown Pro Tier, Substack, Beehiiv.
4. Fiscalidad: IRPF como rendimiento de actividad económica. ¿Constituir asociación primero?
5. Política de reembolso.
6. Cómo evitar que el Pro canibalice el gratis.

**Entregable futuro:** documento `ESTUDIO-MODELO-NEWSLETTER.md` en Fase 2 con recomendación firme.

**Plazo:** 3-6 meses tras lanzamiento Fase 0.

---

## 5. Redes sociales — estrategia antes de activar

**Contexto:** el editor dice "lo hablamos más adelante, apunta". No se activan en Fase 0.

**Preguntas a resolver:**

1. Bluesky vs. Mastodon vs. ambas (PLAN.md recomienda ambas).
2. Qué handle: `@ibizahousing.bsky.social`, `@radaribiza.bsky.social`, etc. Depende del nombre de dominio final.
3. Automatización: GitHub Action que publica hilo los lunes vs. publicación manual.
4. Formato del hilo: post de lanzamiento + post por propuesta principal + post con mapa de posiciones.
5. Política de réplica a menciones (prefiero silencio con redirección a web o interacción acotada).
6. Moderación: si alguien nos cita con mala leche, qué hacemos (ignorar / clarificar / no responder).
7. Métrica de éxito: ¿cuántos seguidores justifican el mantenimiento? ¿cuántos clicks a web son aceptables?
8. Posible tercer canal: LinkedIn para audiencia profesional (concejales, técnicos, consultores).

**Entregable:** documento `ESTUDIO-REDES.md` con decisión tras lanzamiento.

**Plazo:** Fase 1, tras ver primeros datos de tráfico web.

---

## 6. Fecha concreta del relanzamiento — SUPERADA 2026-04-24 por [D15](DECISIONES.md)

**Sin fecha de relanzamiento.** 2026-04-24 el proyecto elimina calendario público y fecha de lanzamiento ([D15](DECISIONES.md)). El avance se organiza por hitos, no por fechas. Esta sección queda archivada como contexto histórico.

**Fechas propuestas (todas descartadas).** La propuesta original del 20-abr apuntaba lunes 18 may 2026. Luego la Revisión Fase 0.5 amplió alcance y el 23-abr se fijó como opción cerrada lunes 13 jul 2026 (con red de seguridad 12 oct 2026, cierre de temporada, y escenario C en pre-temporada abr 2027 como contingencia), registrado en [D11](DECISIONES.md). El 24-abr, tras una sesión de limpieza, el editor constató que ninguna de las fechas planteadas era real ni útil y eliminó la idea de fecha del proyecto. [D11](DECISIONES.md) queda como superada por [D15](DECISIONES.md).

**Contexto original:** el editor no dio fecha explícita, solo "cuando tengamos cerrado el proyecto". La fecha depende de la velocidad de cierre de Fase 0.

**Estimaciones realistas:**

- A tiempo completo enfocado: 7-10 días de trabajo = relanzamiento ~28 abr - 4 may.
- A ritmo sostenible (15-20 h/semana): 3-4 semanas = relanzamiento ~11-18 may.
- Con dominio propio, estudio newsletter y estudio 3 modelos antes: +1 semana = relanzamiento ~18-25 may.

**Criterio duro para lanzar:**

- Pipeline técnico completo y verificado (Bloque A del ROADMAP).
- 8 ediciones retroactivas publicadas (Bloque C).
- 15+ páginas web lanzadas con calidad (Bloque B excepto `/recursos/`).
- SEO técnico completo (Bloque D).
- Analítica activa (Bloque E).
- Newsletter gratis activo (Bloque F parcial).
- Dominio propio configurado (si se cierra estudio 2 a tiempo).

**Criterio blando (mejor tenerlo pero no bloquea):**

- Bots sociales activos.
- Lista curada de periodistas preparada para envío manual.

**Decisión sugerida:** lanzar el **lunes 18 de mayo de 2026**. Deja:

- 4 semanas desde 20-abr para ejecutar Fase 0 sin prisa.
- 2 semanas de margen sobre el inicio de la temporada (1 mayo) — el relanzamiento se presenta como "el observatorio llega al arranque real de la temporada".
- Margen para que los 3 estudios urgentes (dominio, 3 modelos, inspiración Solar) se hagan bien.

**Decisión pendiente del editor:** confirmar fecha concreta.

---

## 7. Estadísticas y analítica potente (refuerzo de transparencia)

**Contexto:** el editor pide "darle mucha importancia a nivel de estadísticas, análisis, hacer algo muy potente aquí". Va más allá del simple contador GoatCounter.

**Ámbitos a estudiar:**

1. **Analítica de tráfico web** (qué páginas se visitan, desde dónde llegan, qué búsquedas traen tráfico).
   - GoatCounter cubre lo básico.
   - Complementar con Google Search Console (búsquedas reales).
   - Dashboard público en `/balance/` o `/estadisticas/` con:
     - Tráfico mensual a ediciones (agregado, sin identificar usuarios).
     - Ediciones más leídas.
     - Búsquedas que nos traen (de Search Console, top 20).
     - Referencias entrantes (qué sitios nos enlazan).

2. **Analítica del corpus editorial** (cuántas propuestas, qué actor las hace, cómo evolucionan).
   - `balance.py` ya lo cubre parcialmente.
   - Ampliar a: evolución de estado de propuestas (qué pasa de "propuesta" a "aprobada"), tasa de ejecución, tiempo medio propuesta→debate, actores más activos por trimestre.

3. **Analítica de red social** (si se activan bots).
   - Qué posts generan más interacciones.
   - Qué propuestas se reenvían más.

4. **Transparencia operativa** (inspirada en Solar Low-Tech):
   - Coste actual del sitio visible en footer o página dedicada.
   - Número de ediciones publicadas hasta hoy.
   - Número de actores documentados.
   - Número de propuestas en seguimiento.
   - Fecha de última actualización.
   - Estado del pipeline (última ejecución OK/KO).

**Entregable:** plan de dashboard público potente + modelo de página `/estadisticas/` complementaria a `/balance/`.

**Plazo:** Fase 0 lanza versión mínima. Fase 1 amplía.

**Este estudio se integra en DISENO-WEB.md y SEO.md; no hace falta documento dedicado, pero sí apuntarlo como área de atención durante Fase 0.**

---

## 8. Inspiración Solar Low-Tech Magazine — qué robar

**Contexto:** el editor señala https://solar.lowtechmagazine.com/ como referencia de aproximación ética y visual.

**Ver sección dedicada en [DISENO-WEB.md](DISENO-WEB.md) (bloque añadido tras decisión editor).**

Resumen de elementos que importar:

- **Indicadores transparentes en tiempo real** en footer (coste del mes, última edición, balance).
- **Tipografía monospace para datos técnicos** (ya parcialmente).
- **Notas al margen** en ediciones largas y páginas `/explica/` (tipo Edward Tufte / libro académico).
- **Dithering 1-bit en imágenes OG** (opcional, estéticamente muy distintivo y peso mínimo).
- **Manifiesto visible en footer**: filosofía + coste + política editorial + licencia, todo a la vista.
- **Rechazo de JS innecesario**. Ya lo hacemos; reforzar y declarar.
- **Accesibilidad radical**: todo el contenido legible sin JS, sin cookies, sin webfonts pesadas.
- **Transparencia operacional**: lista histórica de cuándo el pipeline falló o la edición se retrasó.

**Entregable:** la sección añadida a DISENO-WEB.md se ejecuta dentro de Fase 0 Bloque B (web). No necesita documento aparte.

**Plazo:** durante Fase 0.

---

---

## 9. Auditoría de fuentes de ingesta

**Contexto:** apunte del editor 2026-04-20 tras primera ejecución end-to-end del pipeline documental. Se detectó que:

- 4 queries de Google News funcionaron bien (vivienda, trabajadores temporada, Consell Eivissa vivienda, desahucios caravanas).
- **RSS directos de Diario de Ibiza y Periódico de Ibiza fallaron** ("Feed empty or malformed"). Google News los cubre indirectamente.
- Aparecen en las señales medios que NO están como feeds directos: NouDiari, La Voz de Ibiza, Cadena SER Baleares, Ara Balears (solo a través de Google News).

**Preguntas que responder:**

1. **Transparencia pública.** Crear página `/fuentes/` o sección en `/metodologia/` que liste:
   - Qué feeds consultamos esta semana.
   - Qué medios han aparecido en las señales (y cuáles no).
   - Ventana temporal (últimos N días).
   - Política de cobertura (idiomas, nacional vs local, tipo de medio).
2. **Cobertura real.** ¿Son todos los medios que deberían estar cubiertos?
   - Locales Pitiusas: Diario de Ibiza, Periódico de Ibiza, NouDiari, La Voz de Ibiza, IB3 Eivissa. Revisar si todos están en la ingesta directa o llegan solo vía Google News.
   - Regionales: Ara Balears, Última Hora, diariodemallorca.es (cobertura cruzada), IB3.
   - Nacionales con sección Baleares: El País, elDiario.es, La Vanguardia, ABC, 20 Minutos.
   - Radios: Cadena SER, COPE, Onda Cero, RNE (secciones Ibiza/Baleares).
   - Oficiales: BOIB, BOE (solo si publican normativa vivienda Baleares).
3. **Feeds rotos.** Los RSS directos de Diario y Periódico de Ibiza devuelven vacío. Opciones:
   - Probar URLs alternativas del feed.
   - Dejar solo Google News como captura y confiar en que cubre.
   - Crawling ligero de la sección local si los RSS siguen rotos (dentro de límites de robots.txt).
4. **Detección de vacíos.** ¿Hay temas que deberíamos cubrir y ningún medio publica? ¿Algún medio silencia sistemáticamente un tipo de actor?

**Entregable:** documento `ESTUDIO-FUENTES.md` + página pública `/fuentes/` (o sección en `/metodologia/`) con listado actualizado y política declarada. También: arreglo de los feeds locales si se detectan URLs válidas.

**Plazo:** Fase 1 del ROADMAP (primer mes post-lanzamiento).

---

## Resumen de prioridades

| Estudio | Prioridad | Bloquea Fase 0 | Plazo ejecución |
|---|---|---|---|
| 1. 3 modelos de IA | ✅ Cerrado | — | Benchmark ejecutado 2026-04-20. Reparto opción C aplicado |
| 2. Dominio propio | 🟠 Alta | Sí para lanzamiento público | 2ª semana |
| 3. `/recursos/` | 🟡 Media | No | Fase 1 |
| 4. Newsletter de pago | 🟢 Baja | No | Fase 2 (3-6 meses) |
| 5. Redes sociales | 🟡 Media | No | Fase 1 |
| 6. Fecha relanzamiento | 🟠 Alta | Sí | Decidir esta semana |
| 7. Estadísticas potentes | 🟡 Media | Parcial | Fase 0 versión mínima + Fase 1 |
| 8. Inspiración Solar | 🟢 Baja | No | Durante Fase 0 |
| 9. Auditoría de fuentes | 🟡 Media | No (documentable después) | Fase 1 (primer mes) |
