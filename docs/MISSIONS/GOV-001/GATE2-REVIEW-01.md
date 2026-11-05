# GOV-001 · Gate 2 — Diff review, ciclo 1

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-g23
**Verificación de identidad:** solo declarada. Es el nombre asignado por el agente principal (copilot-sdk-main) al lanzar este subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime. Ni este informe ni la CLI verifican identidades.
**Independencia verificada:** no — la separación es solo contextual. No redacté v1–v8 ni implementé el diff, pero soy un subagente del mismo runtime que el autor (copilot-sdk-main) y no hay prueba operativa de separación.
**Artefacto revisado:** GOV-001 árbol de trabajo GATE2-INPUT.sha256 sha256:f0f7392a971467ad7816da81ae7bef57323249e36f0ac10c0838dbc1768c4a9b
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática del diff real (`git diff 29d741e` y 21 archivos nuevos) contra PROPOSAL-v8 (R0–R8, D1–D4, C1–C3, §5–§7). Además, 25 casos adversariales propios y 12 mutaciones del CLI, ejecutados en `%TEMP%` (ya borrado). No modifiqué ningún archivo del repositorio ni del piloto.

> Por la línea `Independencia verificada: no`, este informe no puede servir como `evidence_file` de un Gate v2 en PASS/PWR (R4b/N29). Este dictamen es solo para la versión identificada arriba y no se transfiere a versiones posteriores.

## Integridad de la entrada
- `Get-FileHash GATE2-INPUT.sha256` = `F0F7392A…4C9B`: coincide con la instrucción.
- Las 38 líneas `<sha256>  <ruta>` coinciden con los archivos actuales (0 discrepancias, comprobado antes y después de la revisión).
- `git status --porcelain --untracked-files=all` tiene 39 entradas: las 38 listadas más el propio `GATE2-INPUT.sha256`, que se excluye por diseño. `git diff --shortstat 29d741e` da `17 files changed, 761 insertions(+), 125 deletions(-)`, igual que el manifiesto. HEAD = `29d741e`.
- Las copias `PROPOSAL-v1..v8`, `GATE1-REVIEW-05..08` y `OWNER-DECISION-01` son byte-idénticas a los originales de la carpeta de sesión (mismo SHA-256). `PROPOSAL-v8` = `252C71CA…ED7F` y `OWNER-DECISION-01` = `7F9103CF…76AE`, como se esperaba.

## Fidelidad a PROPOSAL-v8 (verificado)
| Requisito | Evidencia | Resultado |
|---|---|---|
| R0.a–R0.d, función pura previa | `scripts/quality_cli.py:92-147`, llamada en `:265-268`; `status` imprime INVALID + errores (`:308-311`, `:381-383`) | conforme; casos propios: float 2.0, `id` int, título null, `evidence` con clave extra → error controlado |
| R1, R1b, R2 | `:237-244` | conforme (mutaciones detectadas por los tests) |
| R3/R4 | `:225-226` para toda decisión distinta de PENDING | conforme |
| R4b (roles pertinentes y línea de independencia) | `:245-249`, `:199-203`, regex `:22` | conforme; ver G2-05 |
| R5 Revisor/Dictamen únicos y coherentes | `:186-191`, `labels` `:54-55` | conforme; informes CRLF correctos por la traducción de nuevas líneas |
| R5b a–c | `:21`, `:227-229`, `:192-198` | conforme; 63/65 hex rechazados; solo hashes sin nombre rechazado |
| R6 v1 histórico | `:150-180` (semántica idéntica a la base `29d741e`), `:299-300`, `:357-373` | conforme; AVISO con exit 0; `can-*` = 1 |
| R7 PASS exacto, PWR no habilita | `:250-253`, `:255-257`, `:364`, `:374-375` | conforme; reapertura (Gate 1 PENDING con 2/3 PASS) → error |
| R8 | `:260-261` | conforme, también con ancho completo NFKC |
| C1, N42 | `:23`, `:84-89`, `:343`, `:365`; únicos «verificad…»: `:200` (etiqueta) y `:244` («registrado como verificado») | conforme |
| D2 `--author` | `scripts/new_mission.py:19`, `:65-71`; developer nunca por defecto (`:43-45`) | conforme |
| D3/D4 documentación | `AGENTS.md` (+1 viñeta), `docs/ROLE_MATRIX.md` | conforme; ver G2-07 |
| C2 política | `docs/QUALITY_POLICY.md:9`, `:27` | conforme |
| Plantillas §5/§7 | `docs/templates/GATE1/2/3*.md`: una línea por etiqueta; las etiquetas antiguas se eliminaron | conforme (lo prueba P6) |
| EXAMPLE-001 v2, todo PENDING | `docs/MISSIONS/EXAMPLE-001/mission.json` | conforme |
| Registro GOV-001 | `mission.json` v2 con identidades con evidencia, sin `verification`; Gates PENDING; `01`/`02` son índices con hash; `04`/`05`/`06` son plantillas PENDING; la nota de los ciclos 1–4 es del Orchestrator | conforme con §5 y la secuencia (paso 4) |
| Alcance: sin skills, frameworks ni Appointments | búsqueda de las líneas añadidas del diff: sin coincidencias reales («explícita» es un falso positivo) | conforme |
| Tests eliminados o debilitados | los 4 tests base se conservan en intención; sus aserciones se migraron a v2 (autoaprobación, plantilla, path traversal, orden de Gates y FileExistsError siguen comprobándose) | sin debilitamiento |
| Falsos PASS | el CLI de la base `29d741e` con los tests nuevos da 44 fallos y 4 errores; 12 mutaciones dirigidas (R1, R1b, R2, R4b, R5b-c, R7-PWR, R8, autoverificación, independencia, bloqueo v1 y otras) son todas detectadas | sin falsos PASS detectados |

## Hallazgos
| ID | Gravedad | Evidencia | Descripción | Corrección mínima |
|---|---|---|---|---|
| G2-01 | LOW (preexistente) | `scripts/quality_cli.py:44`, `:49`, `:235` | Hay excepciones no controladas en `has_evidence`. Un `evidence_file` con NUL produce `ValueError: embedded null character`, y un informe que no es UTF-8 produce `UnicodeDecodeError`. Afecta a `validate`, `status` y `can-*`, que terminan con traceback. Falla en modo cerrado (exit ≠ 0, nunca da un falso PASS). La base `29d741e` se comporta igual (reproducido). Queda fuera de R0, que es estructural, pero no es coherente con su espíritu de no lanzar excepciones. | Capturar `(OSError, ValueError, UnicodeError)` en `has_evidence` y en la lectura de `:235` y devolver un error controlado. Puede hacerse en una misión posterior. |
| G2-02 | LOW | `tests/test_governance.py:202-226`, `:244-260`; `03-IMPLEMENTATION.md`, tabla N35/N39 | Algunos subcasos de §6 no están en los tests, aunque el informe del Developer los da por cubiertos: N35 `**Autor efectivo:**` duplicado; N39 FAIL sin `**Autor efectivo:**` y FAIL con `reviewed_artifact` con nombre pero sin hash; N7 `verification` con un campo ausente. Lo comprobé con casos propios y el comportamiento es correcto en los cuatro. | Añadir esos 4 subcasos a los tests existentes o matizar la tabla de correspondencia. |
| G2-03 | LOW | `core.autocrlf=true`; `scripts/quality_cli.py`, `scripts/new_mission.py`, `tests/test_governance.py` y `EXAMPLE-001/mission.json` están en LF, mientras `AGENTS.md` y el resto están en CRLF | Mezcla de finales de línea. El paso 7 de la secuencia v8 compara el SHA-256 del árbol con `GATE2-INPUT.sha256`. Si estos archivos se vuelven a extraer (checkout/reset) tras el commit, pasarán a CRLF y darán una falsa discrepancia. | Comparar sin volver a extraer los archivos, o normalizar los finales de línea antes del commit y regenerar la entrada. Documentarlo. |
| G2-04 | LOW | `scripts/quality_cli.py:365` | Mensaje con concordancia incorrecta: «identidades no comprobada por la CLI». | Usar «identidades no comprobadas por la CLI» y mantener el literal `NOT_CHECKED` en otra parte del mensaje, porque N37 lo busca. |
| G2-05 | LOW | `scripts/quality_cli.py:22`, `:201-202` | `**Independencia verificada:** si — no` se acepta como afirmación con evidencia. Es una debilidad semántica de una comprobación de presencia que v8 asume, y Quality la detecta externamente. | Opcional: rechazar una evidencia que empiece por «no». |
| G2-06 | LOW (riesgo residual §8) | `scripts/quality_cli.py:36-38` | NFKC + casefold no elimina los caracteres de ancho cero. Un revisor `dev\u200b-1` frente al developer `dev-1` supera R2 (reproducido). Es un caso del riesgo de alias ya aceptado en §8, mitigado por R1. | Opcional: eliminar las categorías Unicode Cf en `canon`. |
| G2-07 | LOW | `docs/ROLE_MATRIX.md` | v8 §5 decía «una viñeta y una fila/columna». Se añadieron una columna, una fila de acción y una fila en el registro de herramientas. Es coherente con D3 y está declarado en `03-IMPLEMENTATION.md`. | Ninguna, salvo que el Owner lo objete. |

No encontré ningún BLOCKER, HIGH ni MEDIUM. No hay cambios de diseño que obliguen a reabrir Gate 1.

## Justificación del dictamen
La implementación es fiel a v8 en R0–R8, D1–D4 y C1–C3. No hay regresiones, tests eliminados ni falsos PASS detectados. Ningún mensaje afirma verificar identidades, y el alcance es el aprobado. Las reservas G2-01 a G2-07 son explícitas y no bloqueantes. Las de mayor valor son G2-02 (cobertura prometida en §6 que falta) y G2-03 (riesgo para la comprobación posterior al commit). PASS_WITH_RESERVATIONS no equivale a PASS ni habilita transiciones (C2): queda a decisión del Owner corregir las reservas o aceptarlas.

## Qué NO verifiqué
- La identidad real de copilot-sdk-main ni la mía. La veracidad del contenido de los informes Gate 1 de los ciclos 1–4 (sin archivo original).
- El comportamiento en Linux/macOS ni en otras versiones de Python: solo probé Windows con Python 3.12.0. `str | None` en `new_mission.py:26` requiere Python ≥ 3.10, y el repositorio no declara versión mínima.
- Los commits posteriores ni el paso 7 de la secuencia.

## Limitación de independencia
Soy un subagente lanzado por el mismo agente principal que redactó el plan e implementó el diff. Mi separación es de contexto, no operativa. No puedo acreditar independencia, y este dictamen no suple la verificación de identidad que debe registrar un tercero (Owner).
