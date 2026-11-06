# DESIGN-001 · Bootstrap y reversión desde el commit real

Developer `/root`, 2026-11-06. En un directorio temporal se clonó el commit `e75ffff565ceb3b2712dad3c53d13f5fb4e9744f` con `git clone --quiet --no-hardlinks -c core.autocrlf=false`. Se ejecutó `python -B scripts/bootstrap001.py --name "Design Fixture" --id design-fixture --destination <directorio-temporal>` desde el clon: salida 0. No se creó ningún producto fuera del directorio temporal.

El rol generado coincide byte a byte con el blob del commit y su provenance registra el commit y SHA-256 correctos; la guía, plantilla, herramienta y test MET están presentes; `docs/MISSIONS` contiene solo `README.md`. En el generado se ejecutaron `python -B -m unittest discover -s tests -p test_met001.py` (salida 0, cinco pruebas) y `python -B scripts/met001.py --help` (salida 0). Resultados verificables y campos booleanos en `10-BOOTSTRAP-REAL.json`; el análisis no certifica otros runners.

En ese mismo clon, con identidad local ficticia, `git revert --no-edit e75ffff565ceb3b2712dad3c53d13f5fb4e9744f` salió 0 y `git diff --quiet 1162d89 HEAD` salió 0. La reversión real en otra rama puede requerir resolver conflictos posteriores. No se modificó el árbol principal. La prueba de creación de enlaces simbólicos omitida en `TEST-BOOTSTRAP-02.log` sigue sin verificar; **E2E NO EJECUTADO** para un producto real.
