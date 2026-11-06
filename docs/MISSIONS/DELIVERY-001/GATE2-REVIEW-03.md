# DELIVERY-001 · Gate 2 revisión independiente 03

Fecha: 2026-11-06. Dictamen: **FAIL**. El nuevo contrato elimina la garantía categórica anterior y añade revisión por archivo y controles proporcionales, pero existe una vía reproducible para incorporar una raíz conocida del taller al manifiesto. No se habilita Gate 3 ni aceptación.

## Hallazgo bloqueante

**ALTO — una ruta Windows declarada puede quedar en el manifiesto.** `01-PLAN-03.md:48` exige comprobar raíces conocidas sin copiarlas al informe ni al manifiesto. `scripts/delivery001.py:118-119` escanea el JSON serializado del descriptor, donde las barras invertidas están escapadas; `:134,148-150` transfiere la procedencia al manifiesto sin escanear el resultado final. Reproduje con un archivo sintético revisado, raíz `C:\workshop\project` en `known_roots` y la misma cadena en `provenance`: `prepare` terminó con éxito y la cadena recuperada del JSON del manifiesto coincidió con la raíz. El escape en JSON hace que la búsqueda de bytes literales no la detecte. Esta reproducción no demuestra que la candidata APP-004 contenga rutas del taller. Debe bloquearse el caso para los metadatos y cubrirse con una prueba negativa; no se exige garantía universal de detección.

## Versión y revisión

El SHA-256 LF de `GATE2-INPUT-03.sha256` coincide con el transmitido `a845d4fb74a84b0e55c35b73bbac88e55f454514a4e6d476e20bd1d33e65c667`; los 39 hashes de archivos listados coinciden. HEAD es `1b14c34ad4a87792a73d4fc9de20d209bfdb4565`. Revisé archivos sin seguimiento directamente y status: Git no pudo leer el ignore global, por lo que no certifico inventario de ignorados. Una modificación posterior requiere nueva revisión. Comparación post-commit y lectura independiente del anchor desde registro runtime quedan pendientes según `docs/QUALITY_EVIDENCE_PROTOCOL.md`.

Leí `OWNER-DECISION-02.md`, `01-PLAN-03.md` y `GATE1-REVIEW-03.md`: el Gate 1 PASS está declarado en `mission.json` sobre el plan anclado; la identidad del Owner y del revisor no quedan autenticadas por esos registros. Se conserva el FAIL histórico `GATE2-REVIEW-02.md`. El código comprueba registros con hash, fecha, procedencia, justificación, revisor declarado y ausencia de hallazgos; rechaza `.env`, rutas y firmas seleccionadas, y usa escaneos limitados. La revisión humana declarada no se infiere del escáner ni prueba confidencialidad universal.

Contrasté los 17 hashes de `APP004-REVISION.json` con los bytes del paquete: coinciden. El manifiesto contiene 19 entradas y distingue `INSTALL.md` y `DELIVERY_REPORT.md` como generados sin atribuir revisión humana; `APP004-REVISION-GENERADOS.md` documenta una revisión separada de ambos y del manifiesto. El SHA-256 exacto del manifiesto es `3899099595637eedf75a13486b1a3d421afa89592acb95d6aa5372eacf2065cc`. La procedencia y la identidad en registros son declarativas; hashes no autentican autoría, licencia ni titularidad.

El 2026-11-06 ejecuté `python scripts/delivery001.py verify --directory dist/delivery001-app004-v3/delivery`, salida 0, y `python -m unittest discover -s tests -p test_delivery001.py`, salida 0, seis pruebas con una omitida por enlaces no disponibles en Windows. Esto verifica integridad contra un manifiesto editable y la suite focalizada, no autenticidad ni garantía de seguridad. `EJECUCION-03.md` e `ISOLATED-EXECUTION-03.txt` son evidencia aportada del ensayo aislado; no lo repetí ni certifiqué su aislamiento. **E2E NO EJECUTADO**. No se modifica producto, implementación o manifiesto de misión.

Revisor `codex /root/quality_gate2_v2`, distinto del autor declarado `terra-root`, sin participación en implementación. La declaración I1 y la evidencia G1 existente siguen aplicando a esta instancia; se comparten usuario, workspace y permisos. La evidencia es declarativa y no certifica identidad ni aislamiento real.

```protheusai-review
{
  "mission": "DELIVERY-001",
  "gate": "gate2",
  "risk": "HIGH",
  "decision": "FAIL",
  "reviewer": "codex /root/quality_gate2_v2",
  "artifact": {
    "name": "Gate 2 input DELIVERY-001 03",
    "ref": "sha256_lf:a845d4fb74a84b0e55c35b73bbac88e55f454514a4e6d476e20bd1d33e65c667",
    "path": "GATE2-INPUT-03.sha256"
  },
  "effective_authors": ["terra-root"],
  "authorship_independent": true,
  "isolation": "I1_CONTEXTO_SEPARADO",
  "evidence": [{"kind":"identity","path":"IDENTIDAD-QUALITY-GATE2-02.md","sha256_lf":"8a0390fbd5fe25f6a9691973d74728060aecd0fc0d277e788ace2906f0a8e051"}],
  "date": "2026-11-06"
}
```
