# DESIGN-001 · Adenda de plan: continuidad en bootstrap

Autor: Architect `codex /root/arquitectura`; 2026-11-06. Complementa `01-PLAN.md`; requiere revisión independiente de Quality antes de implementar el cambio afectado. No constituye dictamen ni crea un Gate.

## Hallazgo y alcance

`AGENTS.md` exige consultar `docs/CONTEXT-001.md`; este remite a `docs/templates/CHECKPOINT.md`, `scripts/met001.py` y `docs/MET-001.md` (líneas 3, 7 y 11). Ninguno figura actualmente en `bootstrap/allowlist.json`. Una copia nueva puede contener el rol creativo pero carecer de instrucciones de continuidad requeridas. El script MET usa biblioteca estándar de Python; su compatibilidad con otros runners y disponibilidad de registros no están garantizadas.

Añadir a la lista positiva exactamente esos cuatro archivos, conservando el rol creativo previsto en el plan, sin incorporar expedientes, resultados, registros ni infraestructura nueva. No modificar el comportamiento de bootstrap ni sus contratos de procedencia. `docs/MET-001.md:7` cita también `tests/test_met001.py`, fuera de esta lista: su comando de pruebas no estará disponible en el proyecto generado; documentar esta limitación en la evidencia, sin afirmar que todas las referencias de documentación se resuelven.

## Verificación y retorno

Ampliar la prueba de bootstrap existente para verificar los cuatro archivos generados y las referencias operativas anteriores, junto al contrato creativo; comprobar que no se incluyen expedientes históricos ni logs. Ejecutar la prueba de bootstrap y registrar comando y código de salida; verificar también que `python scripts/met001.py --help` funciona en el proyecto generado, sin datos de sesión reales. Inspeccionar el diff y la lista positiva por rutas y contenido; distinguir fixture sintético de ejecución desde un commit real.

Riesgos: arrastrar ejemplos históricos presentes en la documentación, referencias de prueba no copiadas y suponer portabilidad de MET. Revisar el contenido incorporado, mantener explícitas las limitaciones y no exportar registros de sesión. Si falla la verificación, corregir antes de Gate 2/3. Reversión: retirar las cuatro entradas y las comprobaciones añadidas mediante reversión del commit correspondiente, preservando cualquier trabajo posterior. No se eliminan datos ni se alteran misiones históricas.
