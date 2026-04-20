# Estudio de 3 modelos IA — metodología y guía

**Fecha:** 2026-04-20
**Origen:** [ESTUDIOS-PENDIENTES.md #1](ESTUDIOS-PENDIENTES.md#1--urgente--integración-de-los-tres-modelos-de-ia-haiku--sonnet--opus).
**Objetivo:** elegir qué modelo de Anthropic asignar a cada tarea del pipeline del observatorio documental para maximizar calidad al menor coste.
**Estado:** dataset + gold standard + script listos. Pendiente de ejecución con `ANTHROPIC_API_KEY`.

---

## 1. Filosofía

**Excelencia al menor coste = el modelo más barato que aguante cada tarea, no el mejor en abstracto.** Opus solo donde la calidad editorial no es negociable. Haiku donde el patrón es simple. Sonnet en el medio.

Tres reglas operativas:

- **Prompt caching agresivo** en todas las llamadas. Reduce el coste de input ~90% tras la primera.
- **Dividir tareas complejas** para poder usar modelos baratos en cada subtarea.
- **Fallback inteligente**: si el modelo asignado falla (JSON malformado, respuesta corta), reintento con modelo superior. Pipeline nunca se para, pero solo escala al caro cuando el barato no llega.

---

## 2. Tareas evaluadas en el benchmark inicial

Solo las **3 tareas de input** del pipeline. La composición editorial (tarea 6) se evalúa en otra iteración con criterios cualitativos.

| # | Tarea | Qué hace | Por qué importa |
|---|---|---|---|
| 1 | `classify` | Etiqueta cada noticia con `is_housing`, `actor`, `lever` | Filtra ruido y enrutan al resto del pipeline |
| 2 | `detect` | Decide si la noticia contiene propuesta explícita de actor con nombre | Gatekeeper de la extracción; evita falsos positivos en el tracker de propuestas |
| 3 | `extract` | Extrae la ficha estructurada completa de cada propuesta | Corazón del pivote; aquí es donde el modelo puede alucinar más |

Tareas NO evaluadas en este benchmark:

- 4. Rescate de propuestas vigentes: requiere historial, se evalúa tras 4+ ediciones.
- 5. Fact-check de precedentes internos: depende de que las propias noticias citen precedentes, muy pocos casos en dataset v1.
- 6. Composición de edición: evaluación cualitativa, otra metodología.
- 7. Verificación técnica (URLs, verbos): no usa LLM.

---

## 3. Criterios de evaluación (6 variables)

1. **Calidad contra gold standard** — precisión por campo comparada con solución ideal manual.
2. **Coste real en €** — tokens × precio × ratio de caché.
3. **Robustez contra alucinación** — especialmente para `extract`. Cero-tolerance.
4. **Cumplimiento de instrucciones estrictas** — % de respuestas válidas sin reintento.
5. **Fiabilidad técnica** — JSON malformado, timeouts, variabilidad.
6. **Impacto real (correcciones recibidas / edición)** — *solo en re-benchmarks mensuales*, no en el inicial (no hay histórico).

---

## 4. Dataset

**20 noticias reales** del corpus público del proyecto, cubriendo W16-W17 de 2026 + señales adyacentes verificadas.

Mix deliberado:

- 5 con propuesta explícita (25%).
- 15 sin propuesta (75% — ruido, información descriptiva, acciones ya ejecutadas, testimonios).
- 2 casos ambiguos deliberados marcados con `ambiguous: true` en el gold.
- 4 grupos de duplicados (misma propuesta cubierta por varios diarios) para probar consolidación.
- Variedad de actores: ayuntamiento, consell, tercer_sector, patronal, sindicato, propietarios, trabajadores, judicial, govern_balear.
- Variedad de palancas: enforcement, oferta_vivienda, denuncia_social, precio, normativa, otro.

Ubicación: [`data/bench/dataset_v1.json`](data/bench/dataset_v1.json).

### Ampliación pendiente (dataset v2)

El dataset v1 tiene sesgo de dominio (100% housing). Para medir falsos positivos de la tarea `classify`, el v2 añadirá 5-10 noticias NO de vivienda (turismo general, política sin ángulo vivienda, cultura, deportes). Queda para la iteración siguiente.

---

## 5. Gold standard — autogenerado, sin revisión humana

Desde la decisión editor 2026-04-20, el gold standard del benchmark **no depende de mi criterio manual**. Se genera automáticamente con `scripts/generate_gold.py`:

1. **Opus 4.7 con extended thinking** responde cada tarea sobre cada noticia.
2. **Sonnet 4.6** actúa como validador crítico de cada respuesta de Opus.
3. Items donde Opus y Sonnet coinciden → gold definitivo.
4. Items donde discrepan → se apartan en `gold_discrepancies.json`, **no entran en el benchmark**.

El editor no revisa nada. Las discrepancias quedan documentadas por trazabilidad, pero la decisión recae en el consenso Opus↔Sonnet.

- Gold auto: [`data/bench/gold_auto_v1.json`](data/bench/gold_auto_v1.json) (se genera al ejecutar).
- Discrepancias: [`data/bench/gold_discrepancies.json`](data/bench/gold_discrepancies.json).
- Gold manual de referencia (histórico, no usado en benchmark): [`data/bench/gold_standard_v1.json`](data/bench/gold_standard_v1.json).

### Schema del gold (v1.1)

- `task_1_classify`: `is_housing` + `actor` + `lever`.
- `task_2_proposal_detect`: `proposal_type` ∈ {`formal`, `en_movimiento`, `ninguna`} + `proposal_actor_hint`.
- `task_3_extract`: lista de propuestas con todos los campos del schema, incluyendo soporte para coaliciones (`coalicion_intersectorial`, `coalicion_institucional`) y propuestas en movimiento (`state: "en_movimiento"`).

---

## 6. Prompts por tarea

Definidos en [`scripts/run_benchmark.py`](scripts/run_benchmark.py) como constantes `CLASSIFY_SYSTEM`, `DETECT_SYSTEM`, `EXTRACT_SYSTEM`. Cada prompt incluye:

- Rol + contexto.
- Schema de salida con valores permitidos.
- Reglas duras (especialmente en `extract`: "URL obligatoria del input", "nunca inventes", "no añadas interpretación").
- Ejemplo implícito del esquema.

Los prompts son idénticos entre los 3 modelos para que la comparación sea justa.

---

## 7. Cómo ejecutar

### Paso 1: generar gold automático (primero)

```bash
cd ~/Documents/GitHub/ibiza-housing-radar
export ANTHROPIC_API_KEY=sk-ant-...
python -m scripts.generate_gold
```

Opus con thinking + Sonnet validador producen `data/bench/gold_auto_v1.json` sin intervención humana. Coste ~3 €. Telegram avisa al terminar con válidos/discrepancias. Los items donde Opus y Sonnet discrepan van a `data/bench/gold_discrepancies.json` (no entran en el benchmark).

### Paso 2: correr el benchmark contra los 3 modelos

```bash
python -m scripts.run_benchmark
```

El script lee el gold auto y evalúa Haiku, Sonnet y Opus sobre las 3 tareas.

### Dry-run previo (sin coste, valida estructura)

```bash
python -m scripts.generate_gold --dry-run
python -m scripts.run_benchmark --dry-run
```

Opciones:

- `--tasks classify,detect` — solo subset.
- `--models haiku,sonnet` — solo subset de modelos.
- `--out ruta.json` — cambiar destino del JSON de resultados crudos.

### Coste estimado por ejecución completa

3 modelos × 3 tareas × 20 noticias en batching (una llamada por tarea × modelo, no por noticia):

| Modelo | Coste estimado (€) |
|---|---|
| Haiku | ~0,30 |
| Sonnet | ~0,95 |
| Opus | ~4,80 |
| **TOTAL** | **~6 €** una vez |

Registro: cada llamada va a `data/costs.csv` con `stage="bench_{task}"` y `edition="bench-{task}"` para trazabilidad. Cuenta dentro del tope blando del mes.

### Output del script

Al terminar:

- [`data/bench/results_v1.json`](data/bench/results_v1.json) — resultados crudos (output completo de cada llamada + tokens + coste + latencia).
- [`REPORTE-BENCHMARK.md`](REPORTE-BENCHMARK.md) — informe legible con tablas comparativas + recomendación de reparto + coste mensual proyectado.
- Dashboard privado `private/costs.md` actualizado.

---

## 8. Algoritmo de recomendación

Para cada tarea, el script elige el modelo según reglas explícitas:

```
Si algún modelo tiene score ≥ 0.95:
    Ganador = el más barato entre los que llegan a 0.95.
    Razón: "≥95% de calidad y el más barato entre los que cumplen."
Si no:
    Buscar modelos dentro de 10 puntos del mejor score.
    Ganador = el más barato de ese grupo.
    Razón: "dentro de 10 puntos del mejor, N× más barato."
```

Esta lógica implementa "**excelencia al menor coste**": solo pagamos por calidad diferencial cuando de verdad existe.

Si el editor prefiere criterios distintos (p.ej. exigencia 0.98 para `extract` que es crítica para "cero inferencia"), se ajusta la función `derive_recommendation` en el script.

---

## 9. Qué hacer con los resultados

Tras ejecución, el editor revisa [`REPORTE-BENCHMARK.md`](REPORTE-BENCHMARK.md) y decide:

- **Aceptar** la recomendación automática → se aplica al código del pipeline (`classify.py`, `extract.py` usan los modelos recomendados).
- **Matizar** algún reparto por criterio editorial → ajustar y volver a correr dry-run para verificar.

Tras la decisión, se actualiza [`ARQUITECTURA.md`](ARQUITECTURA.md) con los modelos finales por módulo.

---

## 10. Re-benchmark continuo

Tras el benchmark inicial, el módulo `src/model_rebench.py` (del pivote, [ROADMAP.md tarea A14](ROADMAP.md)) ejecuta una versión ligera de este proceso **cada 4 semanas**:

- Dataset: 10 noticias nuevas del mes.
- Gold standard: generado con Opus + razonamiento extendido (validación del editor opcional).
- Coste: ~1 €/mes.
- Alertas: Telegram si algún modelo cambia su ratio calidad/coste >20% respecto al benchmark inicial.

Adicionalmente, a partir del segundo mes, se incorpora el **sexto criterio (impacto real = correcciones recibidas/edición)** como validación a posteriori de la decisión.

---

## 11. Coste acumulado del estudio

| Concepto | Coste |
|---|---|
| Benchmark inicial (una vez) | ~6 € |
| Re-benchmark mensual | ~1 €/mes |
| Auditoría trimestral con Opus | ~1,50 €/mes promediado |
| **Total anual del sistema de afinado** | **~36 €/año** |

Un coste manejable frente al retorno: un 10% de ahorro en el coste base del pipeline (que es ~80 €/año bajo el pivote) supera el coste del sistema que lo produce. Y además lo que ganamos no es solo ahorro — es **confianza** en la decisión, porque se mide.

---

## 12. Referencias

- [`data/bench/dataset_v1.json`](data/bench/dataset_v1.json) — 20 noticias curadas.
- [`data/bench/gold_standard_v1.json`](data/bench/gold_standard_v1.json) — solución ideal manual.
- [`scripts/run_benchmark.py`](scripts/run_benchmark.py) — script ejecutable.
- [`REPORTE-BENCHMARK.md`](REPORTE-BENCHMARK.md) — resultados tras ejecución (se regenera).
- [`ARQUITECTURA.md`](ARQUITECTURA.md) — destino de las decisiones finales.
- [`ESTUDIOS-PENDIENTES.md`](ESTUDIOS-PENDIENTES.md) — este estudio en contexto.
