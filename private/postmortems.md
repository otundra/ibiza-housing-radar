# Post-mortems — registro de errores evitables

Registro de errores que costaron dinero, tiempo o credibilidad innecesarios. Cada entrada: qué pasó, coste real, causa raíz, prevención aplicada, lección.

No es lista de excusas. Es herramienta de mejora. Revisable en cualquier momento por el editor.

---

## Patrones identificados — lecciones transversales

Cada vez que aparece un error nuevo, cotejar primero con estos patrones. Si encaja con uno ya conocido, la prevención ya existe y la causa es repetida (agravante). Si no encaja, añadir patrón nuevo al final.

### P1 — Flujos multi-paso con coste sin orquestador

Cuando dos scripts producen input para el siguiente y el editor debe lanzarlos en orden correcto, la integración es el punto de fallo más común. Un paso lee output desactualizado; otro paso asume estado que no existe; el editor olvida la secuencia.

**Casos previos:** post-mortem 2026-04-20 17:42 (gold manual vs auto).

**Salvaguarda vinculante:** siempre que haya flujo N→M con coste API, **crear orquestador que conecte por código y no dependa de la memoria del editor**. El orquestador verifica por defecto que lee el output del paso anterior y aborta limpiamente si no encaja.

### P2 — Verificadores demasiado estrictos

Un verificador que rechaza por exceso genera falsos positivos que cuestan dinero y retrasan publicación. Confundir "problema operacional puntual" con "error de contenido" es el modo típico.

**Casos previos:** post-mortem 2026-04-20 18:24 (verify 403 Cadena SER).

**Salvaguarda vinculante:** **distinguir `error real` de `inconveniente superable`**:
- Error real (bloquea): URL 404/410, schema JSON inválido, actor inventado, verbo prohibido en cuerpo, cifra sin soporte en input.
- Inconveniente (avisa, no bloquea): 401/403/405/429 (bot-blocked), 5xx (servidor caído), timeout puntual.

Cualquier verificador nuevo debe declarar explícitamente en su docstring qué clasifica como uno u otro.

### P3 — Umbrales calibrados sin datos reales

Los umbrales de alerta (score `<7` dispara, gasto `>8 €` avisa, disputas `>20%` escala) son hipótesis hasta que se observen con al menos 4-5 ejecuciones reales. Subirlos o bajarlos antes de tener datos puede saturar de ruido o silenciar problemas reales.

**Casos previos:** implícito, pendiente de primera revisión mensual tras Fase 0.

**Salvaguarda vinculante:** revisión de umbrales **solo con ≥4 ediciones publicadas** + dato de correcciones recibidas del público. Cualquier cambio de umbral se registra en este documento con el rango observado y la justificación.

### P4 — Contaminación del contexto del LLM por contenido de versiones antiguas

Cuando el pipeline evoluciona (pivote, cambio de prompt) pero el histórico contiene producto antiguo, el LLM puede leer ese histórico como ejemplo y degradar su output.

**Casos previos:** self-review 2026-04-20 detectó que la W16 antigua (modelo propuestas propias) aparece en el contexto del generador y viola la regla 2 del pivote.

**Salvaguarda vinculante:** cuando se cambia el modelo editorial, el contenido antiguo **se purga del contexto del LLM** (no del repo — queda en histórico git). Regenerar contenido retroactivo bajo el modelo nuevo antes de publicar ediciones nuevas que dependan de él.

---

## 2026-04-20 17:42 — Benchmark duplicado por desajuste de fuentes de gold

**Qué pasó.** `scripts/run_benchmark.py` se ejecutó contra `gold_standard_v1.json` (gold manual, 20 items) en lugar de `gold_auto_v1.json` (gold auto validado Opus+Sonnet, 17 items). Tras ver resultados se detectó el desajuste y se relanzó contra el gold correcto.

**Coste del error.** ~0,57 € de API desperdiciados (primer benchmark). Sin impacto en credibilidad externa (error interno, no publicado). Sin impacto en calendario.

**Causa raíz.** Los dos scripts se diseñaron por separado y no se conectaron. `run_benchmark` tenía hardcoded `GOLD_PATH = "gold_standard_v1.json"`. Cuando `generate_gold` produjo `gold_auto_v1.json`, ninguna lógica actualizaba automáticamente qué gold debía leer el benchmark. Responsable: Claude (diseño inicial del flujo).

**Prevención aplicada.**

1. `run_benchmark.py` ahora prefiere `gold_auto_v1.json` si existe, con fallback a manual y aviso claro en el log (`Usando gold AUTO ...` o `gold_auto no existe; usando gold manual como fallback`).
2. Nuevo orquestador `scripts/bench_full.py` que ejecuta gold_gen + benchmark en orden con verificaciones entre pasos. Es el comando recomendado; los dos scripts individuales quedan como de bajo nivel.
3. Entrada en este log para no olvidar.

**Lección general.** Cuando hay un flujo multi-paso que cuesta dinero (gold_gen → benchmark), el paso N debe validar por defecto que lee el output del paso N-1. No confiar en que el editor recuerde la secuencia. Orquestar por código, no por costumbre.

---

## 2026-04-20 18:24 — Verify bloqueó por 403 de Cadena SER (falso positivo)

**Qué pasó.** `scripts/regen_edition.py` ejecutó el pipeline documental y `verify.py` bloqueó la publicación porque Cadena SER devolvía `HTTP 403 Forbidden` al chequeo automático. La URL era válida y funcionaba en navegador; Cadena SER (igual que El País, La Vanguardia, IB3 y otros medios grandes) rechaza peticiones sin User-Agent realista. La edición recién generada se borró por el flujo de seguridad. Se creó issue #2 en el repo como fallback de alerta crítica.

**Coste del error.** ~1,10 € del run abortado (extract + generate ejecutados; self_review y balance no llegaron a correr). Suma de post-mortems hasta la fecha: **1,67 € de desperdicio** (0,57 € del primero + 1,10 € de este).

**Causa raíz.** `verify.py` usaba `httpx.Client` sin headers. Los medios profesionales filtran bots por User-Agent por defecto y devuelven 403. Diseño inicial asumía que cualquier 4xx era URL rota; tratamiento demasiado agresivo.

**Prevención aplicada.**

1. `httpx.Client` inicializado con User-Agent Chrome Mac + `Accept` + `Accept-Language` realistas. Chequeo honesto (URL pública, solo verificamos existencia) sin discriminar por UA.
2. `check_urls` devuelve ahora `(total, blocking, soft)`:
   - `401/403/405/429` → soft_warning (URL viva, bloqueo de bots o rate-limit).
   - `404/410` → bloqueante (URL de verdad rota).
   - `5xx` / excepción → soft_warning (fallo de servidor, no culpa nuestra).
3. Soft warnings no abortan la publicación; solo se anotan en el reporte. Queda registro pero la edición sale.
4. Issue #2 cerrado como falso positivo con traza al fix.

**Lección general.** Los verificadores pre-publicación deben distinguir entre "URL rota" y "URL bloqueando bots". Un verificador demasiado estricto genera falsos positivos que cuestan dinero y retrasan publicación. Política: bloquear solo cuando la URL NO existe (404/410); el resto, avisar.

---

## Resumen de costes — día 2026-04-20

| Concepto | Coste (€) | Estado |
|---|---|---|
| generate_gold | 0,80 | útil |
| benchmark v1 (gold manual, desajuste) | 0,57 | **desperdicio** |
| benchmark v2 (gold auto, correcto) | 0,59 | útil |
| report end-to-end primera ejecución | 2,25 | útil |
| regen_edition con verify fallando (403) | 1,10 | **desperdicio** |
| regen_edition con verify corregido (OK) | 0,80 | útil |
| **Total día** | **6,11 €** | de los cuales **1,67 € desperdicio (27%)** |

Gasto del mes en curso (abril 2026): **5,02 €** (capa 🟢 verde, <6 €). Margen al tope blando: 6,98 €. Margen al tope duro: 14,98 €.

El desperdicio se concentra en **errores de integración** (script A no conectado al output de B; verify demasiado estricto). Ambos corregidos con salvaguardas estructurales. El resto del gasto produjo información real: benchmark validado, pipeline funcional end-to-end, edición publicable con rigor ≥7 en self-review.

---
