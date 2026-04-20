# Post-mortems — registro de errores evitables

Registro de errores que costaron dinero, tiempo o credibilidad innecesarios. Cada entrada: qué pasó, coste real, causa raíz, prevención aplicada, lección.

No es lista de excusas. Es herramienta de mejora. Revisable en cualquier momento por el editor.

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
