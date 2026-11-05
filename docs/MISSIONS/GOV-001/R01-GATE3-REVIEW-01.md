# GOV-R01 ? Gate 3 ? registro de pruebas independientes 01

**Dictamen:** PENDING ? Gate 2 FAIL. Las pruebas informadas no autorizan avanzar ni sustituyen el nuevo ciclo. No se emite PASS t?cnico ni formal.
**Revisor:** Codex /root/quality_r01, agente distinto del autor declarado copilot-sdk-main; mismo entorno y acceso de escritura, separaci?n de autor?a declarada y aislamiento operativo no acreditado.
**Artefacto revisado:** GATE2-INPUT-04.sha256 sha256_lf:29baf8ddcaed6b85b3730a75cdeee142b86e33814b740049af224bcec478b250; base git:6e5e92980a8ebeb58b13ca5a314242c14f67a467.
**Autor efectivo:** copilot-sdk-main (declarado).
**Fecha y entorno:** 2026-11-05; Windows, Python 3.12.0, Git 2.55.0.windows.3.

## Pruebas ejecutadas por este revisor

- Comprobaci?n Python de los 36 hashes sha256_lf listados en la entrada (bytes con CRLF sustituido por LF): exit 0, ninguna diferencia; hash de la entrada coincide con el ancla del encargo. La comprobaci?n y la lectura de bytes se efectuaron en el workspace sobre la entrada fijada.
- `python -B docs/MISSIONS/GOV-001/GOV-R01-reconstruct.py --repo . --commit 6e5e929`: exit 0, 12 hashes parciales OK, 38 entradas, hash crudo f0f7392a971467ad7816da81ae7bef57323249e36f0ac10c0838dbc1768c4a9b MATCH, archivo a?n no comiteado en HEAD.
- Ensayo propio en temporales: `git clone -q --no-hardlinks`, copiar ?nicamente `.gitattributes`, el archivo reconstruido y el script; `git add -- <tres rutas>` y `git -c user.name=Quality temporary -c user.email=quality@example.invalid commit -qm ...` en el clon desechable. Luego dos veces `git clone -q --no-checkout`, `git config core.autocrlf true` o `false`, `git checkout -q HEAD`, c?lculo SHA-256 crudo y ejecuci?n `python -B .../GOV-R01-reconstruct.py --repo <clon> --commit 6e5e929`. Todos los comandos exit 0. Ambos archivos extra?dos dieron f0f7392a971467ad7816da81ae7bef57323249e36f0ac10c0838dbc1768c4a9b; ambas ejecuciones dieron 38 entradas MATCH y Blob HEAD MATCH. Se eliminaron ?nicamente los temporales creados para el ensayo. El commit es desechable; no es commit real de la misi?n.
- `python -B .../GOV-R01-reconstruct.py --repo . --commit no-such-commit`: exit 1 y traceback. Rechazo sin MATCH; diagn?stico mejorable, sin requisito de salida limpia identificado en v8:25-30.
- `python -B -m unittest discover -s tests -q`: exit 0, 19 pruebas OK. Son pruebas del repositorio, no acreditaci?n de la trazabilidad del Owner.
- `python -B scripts/quality_cli.py validate`: exit 0, estructura consistente; la CLI declara no certificar Quality ni identidades.
- `git diff --check`: exit 0, solo diff rastreado; no verifica archivos no rastreados.

Las salidas anteriores fueron observadas directamente por este agente y resumidas aqu?; no se cre? un log separado fijado de ejecuci?n. Se han contrastado los resultados con el listado de la entrada, no con el commit real posterior, que a?n no existe. El registro posterior al commit, su revisi?n y aceptaci?n del Owner siguen PENDING. La procedencia del texto literal del Owner y de los hashes parciales sigue sin verificaci?n independiente. Ver G2-Q01 en R01-GATE2-REVIEW-01.md.

E2E NO EJECUTADO. No se alteraron archivos revisados ni mission.json. No se ejecut? commit en el repositorio de trabajo.
