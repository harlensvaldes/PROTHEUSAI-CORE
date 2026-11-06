# DELIVERY-001 · Gate 2: revisión independiente

Fecha: 2026-11-06. Dictamen: **FAIL**. La implementación examinada no satisface los controles explícitos de exclusión y enlaces del plan aprobado. No habilita Gate 3 ni aceptación. Mi revisión es independiente de autoría según mi declaración, pero **I0**, no cumple el mínimo I1/G1 de una aprobación HIGH v3; FAIL no requiere esos mínimos. El registro de identidad es declarativo, no certifica identidad ni aislamiento. No he implementado la misión.

## Versión y alcance

Referencia transmitida por Orchestrator: `GATE2-INPUT-01.sha256`, `sha256_lf:b38913d5098eacfc5ddbde9fc419c9dfc843a672810f976ac59a1c371c169bca`. Recalculé el hash LF del anchor y los 23 archivos listados: coincidieron. `git rev-parse HEAD` devolvió `1b14c34ad4a87792a73d4fc9de20d209bfdb4565`; `git status --porcelain --untracked-files=all` identificó los archivos sin seguimiento registrados, además del propio anchor. Git avisó que no podía leer el ignore global; no se afirma inventario completo de archivos ignorados. Inspeccioné bytes reales de implementación, pruebas, receta, semilla, scripts de aislamiento, documentación y evidencia, junto con el mandato original y el plan. La verificación posterior al commit y lectura independiente del anchor desde registro runtime exigidas por `docs/QUALITY_EVIDENCE_PROTOCOL.md:29-33` siguen pendientes.

## Hallazgos

1. **ALTO — exclusión de bases privadas, logs y secretos por ruta incompleta.** El plan `01-PLAN-02.md:12` exige control estricto que impida bases privadas, logs y secretos. `scripts/delivery001.py:13-14,24-26,89-90` solo prohíbe nombres y sufijos concretos y aplica un patrón heurístico. Una ejecución de lectura de `relative_path` aceptó `data/client.db3`, `data/client.sqlite3`, `log/session.txt` e `id_rsa`; un archivo seleccionado con esos nombres y contenido sin coincidencia heurística puede ser empaquetado. La revisión manual exigida por `docs/DELIVERY-001.md` reduce riesgo pero no implementa el control estricto aprobado. El escáner tampoco es garantía universal, tal como ya reconoce la documentación. Es necesaria una política concreta de exclusión compatible con el contrato y pruebas adversas; resolver ambigüedades de datos privados con el Owner si hace falta.
2. **ALTO — enlaces en raíces eludidos.** `scripts/delivery001.py:63,113` resuelve las raíces de fuente y verificación antes de comprobar sus componentes; `regular_under` solo examina componentes posteriores a esa raíz (`:30-39`). Por tanto una raíz proporcionada como enlace o reparse point se sigue sin rechazo, en contradicción con `01-PLAN-02.md:12`, que exige rechazo de enlaces o reparse points en rutas, y con `docs/DELIVERY-001.md` que afirma rechazarlos. No ejecuté una reproducción con enlaces en Windows; el hallazgo deriva directamente de la secuencia del código. El aislamiento frente a sustituciones concurrentes tampoco se garantiza: el plan reconoce límites de carrera, pero no elimina esta omisión inicial.
3. **MEDIO — pruebas previstas insuficientes para el contrato.** `tests/test_delivery001.py:11-55` contiene dos pruebas y no verifica modificaciones y ausencias, duplicados, enlaces/reparse points, colisiones, error de copia, cambios concurrentes, contenido secreto, rutas de taller, ni la semilla real como exige `01-PLAN-02.md:29-31`. Algunas comprobaciones declaradas en ejecución son ajenas a estas pruebas y requieren revisión propia de Gate 3; no suplen los casos negativos ausentes. `isolated_smoke.py:49-51` imprime integridad y números iniciales sin hacer assertions sobre esos valores, por lo que salida cero por sí sola no los fuerza. Tampoco se conservan aquí los logs originales del ensayo ni montajes completos; `EJECUCION-01.md` es un resumen del ejecutor.

## Verificaciones y límites

`python scripts/delivery001.py verify --directory dist/delivery001-app004/delivery` devolvió 0 en esta revisión: verifica consistencia con el manifiesto editable, no autenticidad. Las tres imágenes del paquete coinciden con sus metadatos SHA-256 y los archivos presentes en APP-004; esto no acredita licencia o titularidad. Un sondeo literal de tres identificadores de rutas de taller no encontró coincidencias en archivos del paquete; no es prueba universal de ausencia de rutas, claves o datos privados. No ejecuté suite, instalación, semilla, build, lint ni ensayo aislado. La descripción del ensayo y sus posibles resultados no son evidencia de ejecución independiente por esta revisión. **E2E NO EJECUTADO**. Revisión limitada a Gate 2, sin validación legal de Pexels ni aceptación funcional o comercial.

```protheusai-review
{
  "mission": "DELIVERY-001",
  "gate": "gate2",
  "risk": "HIGH",
  "decision": "FAIL",
  "reviewer": "codex /root/quality_gate2",
  "artifact": {
    "name": "Gate 2 input DELIVERY-001 01",
    "ref": "sha256_lf:b38913d5098eacfc5ddbde9fc419c9dfc843a672810f976ac59a1c371c169bca",
    "path": "GATE2-INPUT-01.sha256"
  },
  "effective_authors": ["terra-root"],
  "authorship_independent": true,
  "isolation": "I0_CONTEXTO_COMPARTIDO",
  "evidence": [{"kind":"identity","path":"IDENTIDAD-QUALITY-GATE2-01.md","sha256_lf":"d5e018571f0ef80f758bb8a6604dcc89020da0cd30421e61236d77741a50193e"}],
  "date": "2026-11-06"
}
```