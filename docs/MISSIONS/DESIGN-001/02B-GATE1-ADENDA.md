# DESIGN-001 · Gate 1 de adenda bootstrap

Fecha: 2026-11-06. Revisor declarado `codex /root/quality`; no redacté la adenda ni implementé el incremento. Identidad y aislamiento no certificados. Artefacto revisado: `01A-BOOTSTRAP-ADENDA.md`, SHA-256 de bytes `a64cd19fb23083d22a7b3dd74f50bf487fc9424911e9b921fd70f7fd851b7647`. **Dictamen: FAIL.** Este dictamen afecta a la adenda y conserva los dictámenes históricos sobre el plan anterior.

## Hallazgo

La adenda propone copiar `docs/MET-001.md`, pero omitir deliberadamente `tests/test_met001.py` y documentar la limitación únicamente en la evidencia de misión. La guía distribuida indica ejecutar `python -m unittest discover -s tests -p test_met001.py` (`docs/MET-001.md:7`), mientras la lista positiva no incluye ese test ni otros archivos bajo `tests/`. La evidencia de misión no acompaña al proyecto generado: el consumidor recibe una instrucción de verificación que no puede ejecutar como está; no debe interpretarse una ausencia o cero pruebas como PASS. Esto es un defecto actual del diseño de empaquetado, no una mera incertidumbre de portabilidad.

Una corrección proporcionada es incluir también el test, previa revisión de su contenido y dependencias, y verificar en el proyecto generado que se descubren y ejecutan pruebas; alternativamente, adaptar la guía distribuida para indicar de forma visible que la prueba no se suministra y cómo obtenerla, sin alterar evidencia histórica. Quality revisará la solución y su alcance. No se requiere una nueva autorización de riesgo para corregir este defecto dentro del mandato de componentes bootstrap; el entorno conserva sus permisos.

## Resto y límites

La inclusión propuesta de `docs/CONTEXT-001.md`, la plantilla de checkpoint, la guía y el script MET atiende una referencia obligatoria de `AGENTS.md:28`; la plantilla es condicional y MET se aplica al medir (`docs/CONTEXT-001.md:3,7,11`). El script usa biblioteca estándar; `tests/test_met001.py` importa `scripts/met001.py` y utiliza fixtures temporales. La adenda acierta al exigir exclusión de expedientes, cotejo de commit y prueba del CLI; permanecen pendientes la revisión del contenido completo empaquetado y la ejecución de pruebas reales, incluidos casos negativos y reversión. No ejecuté pruebas en esta revisión. **E2E NO EJECUTADO**.
