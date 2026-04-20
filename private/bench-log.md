# Log de ejecuciones del benchmark

Registro automático de cada ejecución de `scripts/generate_gold.py` y `scripts/run_benchmark.py`. Append-only. No se edita a mano.

**Alertas Telegram asociadas:**

- `generate_gold.py` completado → resumen con válidos/discrepancias/coste.
- `run_benchmark.py` completado → resumen con scores/ganadores/coste.
- Si ratio calidad/coste cambia >20% respecto al mes anterior → alerta atención.

## Histórico

*Aún no hay ejecuciones registradas. La primera se anotará al ejecutar `python -m scripts.generate_gold` seguido de `python -m scripts.run_benchmark` con `ANTHROPIC_API_KEY` en el entorno.*
