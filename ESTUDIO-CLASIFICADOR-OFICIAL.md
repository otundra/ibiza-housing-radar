# Estudio — Clasificador IA experto en derecho administrativo balear

**Fecha de apertura:** 2026-05-08
**Estado:** abierto, esqueleto base de las cuestiones a cerrar
**Sub-estudio de:** [ESTUDIO-FUENTES-OFICIALES.md](ESTUDIO-FUENTES-OFICIALES.md)

**Origen.** Punto crítico que el editor identificó en la sesión 2026-05-08: *"el clasificador IA sobre fuente oficial debe dedicársele un estudio muy profundo que armonice con nuestras necesidades y reduzca el fallo a lo máximo posible. Si la web falla en esto, puede que falle todo"*. Este sub-estudio responde a esa exigencia.

**Frontera dura del editor (no negociable).** *"No sé de asuntos jurídicos, ni tengo idea de leer textos técnicos de este tipo, ni me interesan. Esto debe ir tan fino hilado que no tenga que hacer nada al respecto"*. Cualquier diseño que requiera al editor leer textos jurídicos rutinariamente está descartado por construcción.

---

## 1. Por qué este sub-estudio existe

El clasificador actual del pipeline (`src/classify.py`) está diseñado para procesar **titulares y entradillas periodísticas en español**. La integración del BOIB plantea condiciones distintas que el clasificador actual no resuelve sin redesarrollo. Y lo que está en juego es la **autoridad documental del observatorio**: si publicamos una clasificación errónea de un decreto o un decreto erróneo como propuesta vigente, la credibilidad cae rápido y es difícil de recuperar.

La regla complementaria del proyecto (*automatización máxima + veracidad pública*) implica que la clasificación tiene que ser fiable **sin supervisión humana del editor**. Eso obliga a montar un sistema interno con redes de seguridad propias.

---

## 2. Diferencia con el clasificador actual de prensa

| Dimensión | Clasificador actual (prensa) | Clasificador BOIB necesario |
|---|---|---|
| Filtro previo | El periodista ya filtró por relevancia social | Sin filtro humano previo: hay que distinguir lo material de lo administrativo interno |
| Tipo de input | Titular + entradilla en español | Texto jurídico-administrativo en catalán y castellano |
| Volumen | ~50-100 noticias/semana tras filtro RSS | Estimado: 200-400 disposiciones/semana antes del filtro de palabras clave |
| Fallo de relevancia | Bajo coste (la cuarentena recoge dudosos) | Alto coste si no filtra ruido — la cuarentena no aguanta el volumen |
| Riesgo principal | Falso negativo (perderse propuesta real) | Falso positivo (publicar como propuesta lo que es trámite interno) |
| Lenguaje | Coloquial-periodístico | Técnico-jurídico, con citas a normas, fechas y procedimientos |
| Ground truth | El editor con criterio editorial | Sistema IA experto interno (frontera dura del editor) |

---

## 3. Las seis cuestiones que tiene que cerrar el estudio

Lo que tiene que dejar resuelto el estudio, en orden:

### 3.1 Taxonomía de actos del BOIB con criterio editorial

¿Qué tipos de actos publica el BOIB? ¿Cuáles son material editorial, cuáles son ruido?

**Catálogo orientativo a refinar con muestras reales:**

**Material:**
- Orden con bases reguladoras de subvenciones de vivienda.
- Decreto-ley en materia de vivienda, urbanismo, suelo.
- Plan especial / modificación del PTI con afectación a suelo residencial.
- Resolución de convocatoria de IBAVI (ayudas, listas de espera, adjudicaciones).
- Acuerdos de pleno con rango normativo del Consell d'Eivissa.
- Ordenanzas municipales sobre alquiler turístico, habitabilidad, rehabilitación.
- Anuncios de información pública de planes urbanísticos.
- Resoluciones agregables: tandas de sanciones a alquiler turístico ilegal cuando son patrón.

**Ruido (descartable):**
- Modificación de la relación de puestos de trabajo (RPT) interna del IBAVI.
- Nombramientos de cargos administrativos.
- Contrataciones administrativas rutinarias (mantenimiento, suministros).
- Anuncios de notificación a particulares por procedimiento individual.
- Concursos de empleo público interno.

**Frontera (caso por caso):**
- Modificaciones puntuales de plantilla del IBAVI cuando son grandes (puede señalar política de vivienda).
- Sanciones individuales cuando suman a un patrón estadístico mayor.
- Convocatorias de empleo público en organismos relacionados (puede ser ruido o señal).

**Esta tabla la refinará el panel cruzado IA leyendo 4-6 boletines reales completos.** No el editor.

### 3.2 Filtrado por sección antes que la IA

El BOIB tiene 5 secciones. El filtro previo barato:

- **Disposiciones generales** → pasa siempre. Es donde están leyes, decretos, planes.
- **Otras disposiciones** → pasa siempre. Es donde están órdenes, resoluciones, convocatorias.
- **Contratación** → ignorar salvo lista blanca estricta de palabras clave (vivienda, IBAVI, rehabilitación). El 95% es ruido administrativo.
- **Procedimientos judiciales** → ignorar salvo lista blanca estricta. Casi todo es procedimiento individual.
- **Anuncios** → ignorar salvo lista blanca estricta (información pública de planes urbanísticos, convocatorias de subvención, anuncios materiales).

Este filtro previo baja el volumen a IA en ~70-80% antes de gastar un token.

### 3.3 Prompt específico del clasificador oficial

Distinto del de prensa. Tiene que decidir tres cosas:

1. **¿Es de vivienda o tema conexo?** (alquiler, urbanismo residencial, suelo dotacional, rehabilitación, alquiler turístico, infravivienda, asentamientos).
2. **¿Es acto material o trámite interno?** (orden de bases vs. modificación de RPT).
3. **¿Hay actor con potestad detrás (no solo informe técnico)?** (decreto del Govern vs. propuesta técnica de un servicio).

Output estructurado: `{material: bool, palanca: enum, actor: str, razón: str, confianza: float}`.

### 3.4 Validación cruzada con Sonnet

Más estricta que en prensa. Cualquier disposición que el clasificador marca como "material" pasa por validador antes de entrar al pipeline. Si Sonnet discrepa con el clasificador → segunda ronda con Opus + razonamiento extendido.

### 3.5 Conjunto de prueba etiquetado

**Aquí está la decisión clave.** Como el editor no puede etiquetar a mano (frontera dura), el conjunto de prueba lo genera el sistema IA experto interno. Detalle completo en §4.

### 3.6 Criterios objetivos de éxito

Propuesta inicial:
- **Precisión ≥85%** (de las disposiciones marcadas como "material", al menos el 85% lo son de verdad). Poco falso positivo.
- **Exhaustividad ≥80%** (de las disposiciones que de verdad son material, capturamos al menos el 80%). No perdernos disposiciones materiales.
- **Tasa de cuarentena <15%** (las disposiciones que el sistema no resuelve con confianza alta no superan ese porcentaje del total).

Por debajo de estos umbrales, el sistema se considera no apto y o se ajusta o se para.

**Criterios medidos contra el conjunto de prueba etiquetado por el sistema IA experto.**

---

## 4. El patrón "panel cruzado IA" — ground truth sin humano editor

### 4.1 Diseño del panel

En lugar de un humano etiquetando lo que es material vs. ruido, montamos una mesa donde tres modelos opinan sobre la misma disposición de forma independiente:

**Capa 1 — Opus 4.7 con razonamiento extendido**
- Prompt de rol: *"experto en derecho administrativo balear que evalúa si un acto del BOIB es material editorial para un observatorio de vivienda"*.
- Ejecución con razonamiento extendido habilitado.
- Output estructurado: clasificación + razón en lenguaje claro + cita literal de la norma aplicable cuando proceda.
- Coste: alto por disposición. Se usa para conjunto de prueba (única vez) y para casos fronterizos (raro).

**Capa 2 — Sonnet 4.6**
- Mismo prompt, ejecución independiente.
- Sirve como segunda opinión. No ve la respuesta de Opus.
- Coste: medio. Se usa en producción rutinaria.

**Capa 3 — Haiku 4.5**
- Prompt de filtro grueso (es lo que iría en producción para el primer cribado).
- Opina rápido y barato.
- Coste: bajo. Se usa para todo el volumen.

### 4.2 Reglas de consenso

- **Consenso fuerte (los tres coinciden)** → la disposición se etiqueta automáticamente. Pasa al pipeline si es "material", se descarta si es "ruido".
- **Discrepancia parcial (2 vs 1)** → entra en cola de "casos fronterizos". Segunda ronda con Opus + razonamiento extendido + acceso al texto completo, que decide y deja registro auditable de su razonamiento. **No llega al editor.**
- **Discrepancia persistente tras la segunda ronda** → la disposición va a la cuarentena pública existente como `pendiente_clasificacion`. Queda visible pero no en edición. La cuarentena ya es parte del proyecto (cerrada en PI11), así que no se inventa infraestructura nueva.

### 4.3 Continuismo arquitectónico

Este patrón no es exótico al proyecto. El propio proyecto ya usa "Opus thinking + Sonnet validador" como referencia automática para los re-benchmarks mensuales (ver `src/model_rebench.py` y `ESTUDIO-3-MODELOS.md`). Lo nuevo es:

- Añadir el rol *"experto jurídico"* en los prompts.
- Aumentar la exigencia de consenso (los tres tienen que coincidir, no solo dos).
- Conectar con la cuarentena pública existente cuando no hay consenso.

Es continuista, no rupturista.

---

## 5. Generación automática del conjunto de prueba

### 5.1 Pipeline de generación

1. Tomamos 100-150 disposiciones reales del BOIB de las últimas 8 semanas.
2. Cada una se procesa con **Opus 4.7 + razonamiento extendido + prompt de rol jurídico exhaustivo** (modo *"profesor de derecho que dictamina con cita literal de norma aplicable"*).
3. Cada dictamen Opus pasa por **Sonnet validador** que confirma o cuestiona.
4. Cuando ambos coinciden, esa disposición entra al conjunto de prueba con etiqueta *"alta confianza"*.
5. Cuando discrepan, se descarta del conjunto de prueba (no se fuerza). Estas disposiciones se reservan como "casos difíciles" que el sistema en producción tendría que manejar — son ejemplos del límite del clasificador.

**Resultado:** un conjunto de 70-100 disposiciones bien etiquetadas, generadas sin intervención del editor, con razonamiento auditable detrás de cada una.

### 5.2 Calidad del ground truth automatizado

¿Es fiable un ground truth generado por IA? Análisis honesto:

- **Riesgo:** los modelos comparten entrenamiento. Sesgo común no detectable internamente.
- **Mitigación 1:** usar dos generaciones de modelo (Opus thinking primero, Sonnet validador después). Discrepancias se descartan.
- **Mitigación 2:** validación periódica con asesor jurídico externo opcional. Una hora cada 6 meses revisando una muestra del conjunto de prueba detecta sesgos sistemáticos. Coste prorrateado: ~15-25 €/mes si se contrata; cero si se usa la red de aliados (consejo editorial honorífico de fase 4).
- **Mitigación 3:** el modo cuarentena agresiva inicial (ver §6) corrige errores en producción cuando llegan correcciones externas.

**El ground truth no es perfecto, pero no necesita serlo.** Necesita ser suficientemente bueno para que el clasificador en producción cumpla los criterios de éxito de §3.6, y que las desviaciones se detecten en el primer mes de operación bajo modo cuarentena agresiva.

---

## 6. Modo "cuarentena agresiva" al inicio

Para que la frontera "cero supervisión humana" no se convierta en *"hemos publicado tres errores jurídicos antes de darnos cuenta"*, el módulo BOIB nace en este modo las primeras 4-6 semanas:

1. **Toda disposición clasificada como material entra al pipeline** pero no se publica directamente en edición. Va a `/revision-pendiente/` (cuarentena pública existente, cerrada en PI11) marcada como `pendiente_validacion_oficial`.
2. **La edición semanal cita la cuarentena de forma agregada:** *"Esta semana 4 nuevas disposiciones del BOIB entran en revisión pública"*, con enlace a `/revision-pendiente/`.
3. **Si tras 2-3 semanas ningún caso recibe corrección externa que demuestre error**, el modo se relaja: las disposiciones con consenso fuerte del panel pasan directas a edición; solo las dudosas quedan en cuarentena.
4. **Si llega una corrección que demuestra error material** → caso entra al conjunto de prueba como ejemplo negativo, el clasificador se re-calibra automáticamente (re-generación del conjunto de prueba con el nuevo ejemplo), modo cuarentena agresiva se mantiene una semana más.

**La cuarentena pública ya tiene la regla de archivo a 60 días** — el sistema absorbe los casos no resueltos sin intervención del editor.

---

## 7. Asesor jurídico externo opcional

Honestidad pura: hay un escenario donde se necesita criterio jurídico humano externo. Pasaría si:

1. Una disposición clasificada como "material" provoca corrección externa que demuestra error.
2. La corrección se valida.
3. El caso se acumula con otros similares formando patrón.

Cuando eso ocurra (probablemente raro), **no es el editor quien dictamina**. Es:

### 7.1 Vía contratada

Asesor jurídico puntual externo. Abogado especializado en derecho administrativo balear contratado por horas sueltas, no como mantenimiento. Tarifa típica 80-150 €/hora. Si se usa 1 hora cada 6 meses para revisar un lote acumulado de 5-10 casos fronterizos → coste ~160-300 €/año = ~15-25 €/mes prorrateado. **Opcional y reactivo, no recurrente.**

### 7.2 Vía red de aliados

Alguno de los actores aliados en `/recursos/` (Cáritas, sindicatos, GEN-GOB) suele tener jurista propio dispuesto a revisar 5 minutos por buena voluntad. La fase 4 del plan general contempla un consejo editorial honorífico — un jurista en ese consejo cierra esta vía sin coste.

### 7.3 Vía nula

Asumir el error, corregir vía el canal `/correcciones/` cuando llegue, ajustar el clasificador con el caso etiquetado. No contratar nada. **Vía válida** mientras el flujo de correcciones externas sea bajo.

**La frontera "el editor no lee nada técnico" se mantiene en las tres vías.** Lo que cambia es de dónde sale el criterio externo cuando hace falta.

---

## 8. Riesgo residual honesto

Lo peor que puede pasar tras seguir todo el recorrido con disciplina:

1. **El panel IA tiene un sesgo común no detectado** y clasifica sistemáticamente mal un tipo de disposición. Probabilidad: baja pero no nula. Mitigación: el modo cuarentena agresiva inicial + canal `/correcciones/` activo. Cuando aparezca el primer reporte externo, el caso se identifica y se ajusta el prompt.
2. **Volumen del BOIB sobrecarga la cuarentena.** El umbral de 20 propuestas pendientes ya genera alerta en el sistema actual. Si BOIB satura, llegará Telegram. Mitigación: ajustar filtros previos por sección. No carga humana — trabajo técnico reactivo.
3. **El asesor externo no aparece cuando se necesita.** Si llega corrección compleja y no hay jurista accesible, el caso queda como "pendiente de revisión" en cuarentena pública el tiempo necesario. La regla 5 (correcciones públicas con traza) se cumple igual: *"caso reportado, en revisión, pendiente de criterio jurídico externo"*. Esto es honesto y no daña la credibilidad — la mata el silenciamiento, no la lentitud.
4. **El clasificador no llega a los criterios objetivos en la prueba en seco.** Decisión obligada: parar el módulo BOIB. La empresa no es heroica; es honesta. Mejor un observatorio fiable basado en prensa que un observatorio ambicioso que escupe ruido normativo.

Ninguno de estos riesgos obliga al editor a leer textos técnicos. Ninguno carga con horas recurrentes.

---

## 9. Calendario de cierre del estudio

Tres días de trabajo concentrado para cerrar este sub-estudio:

| Día | Tarea | Entregable |
|---|---|---|
| 1 | Lectura cruzada de 4-6 boletines reales con panel IA. Generación del catálogo refinado de tipos de actos materiales/ruido. | Tabla cerrada de §3.1 con muestras reales |
| 1-2 | Diseño del prompt del clasificador oficial. Iteración con muestras del día 1. | Prompt versión 1 + ejemplos |
| 2 | Generación del conjunto de prueba automatizado (Opus thinking + Sonnet validador sobre 100-150 disposiciones). | `data/test_set/boib_classifier_v1.json` con 70-100 disposiciones etiquetadas |
| 3 | Diseño del filtro previo por sección + lista blanca de palabras clave. Borrador del modo cuarentena agresiva. | Configuración cerrada en `data/boib_filter.yml` |

**Entregable final del sub-estudio:** este documento ampliado con todas las cuestiones cerradas + un anexo de implementación que sirva de plano de obra cuando se decida arrancar el código.

---

## 10. Próxima revisión y criterio de revocación

- **Próxima revisión:** al recibir respuesta del editor a las preguntas de §18 del estudio padre (`ESTUDIO-FUENTES-OFICIALES.md`) y decidir el alcance de la primera integración.
- **Criterio de revocación:** si tras los 3 días de cierre del estudio el panel IA no consigue generar conjunto de prueba con consenso fuerte en al menos 70 disposiciones, el sub-estudio se cierra con veredicto *"clasificador no viable con la arquitectura actual"* y se vuelve al estudio padre a reconsiderar el escenario 0 (no integrar BOIB).

---

## 11. Trazabilidad — referencias cruzadas

- [ESTUDIO-FUENTES-OFICIALES.md](ESTUDIO-FUENTES-OFICIALES.md) — estudio padre
- [ESTUDIO-3-MODELOS.md](ESTUDIO-3-MODELOS.md) — origen del patrón "Opus thinking + Sonnet validador"
- [ESTUDIO-COSTES-AUDITOR.md](ESTUDIO-COSTES-AUDITOR.md) — sistema auditor IA (sirve de modelo arquitectónico)
- [ESTUDIO-TIERS.md](ESTUDIO-TIERS.md) — sistema de tiers que el BOIB hereda
- [ARQUITECTURA.md](ARQUITECTURA.md) — pipeline técnico actual
- `src/quarantine.py` — módulo de cuarentena cerrado en PI11 al que se conecta este clasificador
- `src/classify.py` — clasificador actual de prensa, base de comparación
- `src/audit.py` — auditor IA actual, conecta el panel cruzado
