# DESIGN-001 · Corrección del plan de bootstrap

Autor: Architect `codex /root/arquitectura`; 2026-11-06. Esta propuesta corrige el defecto señalado en `02B-GATE1-ADENDA.md` y sustituye la exclusión del test propuesta en `01A-BOOTSTRAP-ADENDA.md`. El FAIL de Quality permanece intacto. El plan corregido requiere revisión independiente antes de implementar el cambio afectado; no crea un Gate.

## Alcance y dependencias

Además del contrato creativo previsto en `01-PLAN.md`, incluir en `bootstrap/allowlist.json` estas cinco rutas, con sus destinos equivalentes: `docs/CONTEXT-001.md`, `docs/templates/CHECKPOINT.md`, `docs/MET-001.md`, `scripts/met001.py` y `tests/test_met001.py`. El test importa `json`, `tempfile`, `unittest`, `pathlib` y `sys` de la biblioteca estándar e importa `met001` desde `scripts/` (`tests/test_met001.py:1-8`); usa archivos temporales con datos ficticios. `scripts/met001.py` también usa biblioteca estándar. No incorporar expedientes, logs ni otra infraestructura.

## Verificación y reversión

Ampliar `tests/test_bootstrap001.py` para comprobar las cinco rutas, el contrato creativo y la ausencia de expedientes históricos y registros en el proyecto generado. Desde ese proyecto ejecutar `python -m unittest discover -s tests -p test_met001.py` y comprobar que descubre y ejecuta pruebas efectivamente, con código de salida cero; cero pruebas no es PASS. Ejecutar también `python scripts/met001.py --help` y las pruebas de bootstrap; registrar comandos, códigos y resultados. Contrastar contenido y procedencia de las rutas empaquetadas, distinguiendo fixture sintético de bootstrap desde commit real. No usar registros de sesión reales en estas pruebas.

MET depende del formato de registros y no acredita soporte de otros runners ni facturación; las cifras históricas existentes en su guía son ejemplos, no resultados actuales. Una regresión o fallo exige corrección y nueva revisión. Revertir las entradas y comprobaciones mediante reversión del commit correspondiente, preservando trabajo posterior. No se borran datos ni se modifican expedientes históricos.
