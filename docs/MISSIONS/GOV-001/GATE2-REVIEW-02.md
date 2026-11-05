# GOV-001 · Gate 2 — Diff review, ciclo 2

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-g23-c2
**Verificación de identidad:** solo declarada. Es el nombre asignado por el agente principal (copilot-sdk-main) al lanzar este subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime. Ni este informe ni la CLI verifican identidades.
**Independencia verificada:** no — la separación es solo contextual. No redacté PROPOSAL-v1..v8 ni implementé el diff, pero soy un subagente del mismo runtime que el autor (copilot-sdk-main) y no hay prueba operativa de separación.
**Artefacto revisado:** GOV-001 árbol de trabajo GATE2-INPUT-02.sha256 sha256:171cd00541602426e6220fa1a5be8b5aeb089e9b3de4707431967fa35f2e5e28
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática del diff completo respecto a `29d741e` (17 archivos rastreados y 23 archivos nuevos en `docs/MISSIONS/GOV-001/`) contra PROPOSAL-v8, GATE2-REVIEW-01 y `03-IMPLEMENTATION.md` §«Reapertura de Gate 2 — ciclo 2». Además ejecuté casos adversariales propios y 3 mutaciones en una copia en `%TEMP%\g23c2_adv`, ya borrada. No modifiqué ningún archivo del repositorio ni del piloto. Usé siempre `python -B`.

> Por la línea `Independencia verificada: no`, este informe no puede servir como `evidence_file` de un Gate v2 en PASS/PWR (R4b). Este dictamen vale solo para la versión identificada arriba y no se transfiere a versiones posteriores.

## Integridad de la entrada
- `Get-FileHash GATE2-INPUT-02.sha256` = `171CD005…5E28`: coincide con la instrucción.
- El manifiesto contiene 40 líneas `<sha256>  <ruta>`. Las 40 coinciden con los archivos actuales (0 discrepancias, 0 ausentes). Lo comprobé al empezar (08:35) y al terminar (08:38).
- `git status --porcelain --untracked-files=all` tiene 41 entradas: las 40 del manifiesto más el propio `GATE2-INPUT-02.sha256`, excluido por diseño. No hay archivos fuera del manifiesto. HEAD = `29d741e`. `git diff --stat 29d741e` = `17 files changed, 801 insertions(+), 134 deletions(-)`, igual que el manifiesto.
- `GATE2-REVIEW-01.md` (`68A4B5D5…2DF8`) y `GATE3-EVIDENCE-01.md` (`323EFBFD…B055`) son byte-idénticos a los originales de la carpeta de sesión. Los hashes coinciden con los que cita `03-IMPLEMENTATION.md:88`.
- Finales de línea: los 41 archivos están en CRLF puro, sin LF suelto. `core.autocrlf=true`. No existe `.gitattributes`. Todos los archivos rastreados modificados son `i/lf w/crlf`.

## Estado de los hallazgos del ciclo 1
| ID | Estado | Evidencia |
|---|---|---|
| G2-01 / G3-02 | **CERRADO** | `scripts/quality_cli.py:45-61`: `report_text()` captura `(OSError, ValueError, UnicodeError)` y devuelve `None`. `has_evidence()` (`:64-65`) y `v2_errors` (`:247`) la usan. Tests: `tests/test_governance.py:163-168` (NUL y no UTF-8). Mutación M3 (quitar la captura) → `FAILED (errors=1)`. |
| G2-02 / G3-01 | **CERRADO** | N35 «Autor efectivo» duplicado: `tests/test_governance.py:225`. N39 FAIL sin «Autor efectivo»: `:271-273`. N39 FAIL con artefacto sin hash: `:274-276`. N7 `verification` sin un campo: `:340`. |
| G2-03 | **CERRADO** (en este host) | Los 41 archivos están en CRLF. Con `core.autocrlf=true`, un checkout reproduce esos bytes. Queda un riesgo residual: ver G2-13. |
| G2-04 | **CERRADO** | `scripts/quality_cli.py:379`: «Identidades: verificación registrada, no comprobada por la CLI». El literal `NOT_CHECKED` (`:23`) se conserva. |
| G2-05 | **CERRADO PARCIALMENTE** | `scripts/quality_cli.py:22` rechaza «si — no», «sí — no.», «sí — NO», «sí —no» y «sí — n\u200bo» (casos propios). Se puede eludir con signos antes de «no» (ver G2-08). Test: `tests/test_governance.py:226`. Mutación M2 → `FAILED (failures=1)`. |
| G2-06 | **CERRADO** (con la corrección propuesta) | `scripts/quality_cli.py:41` elimina la categoría Cf. Casos propios: U+200B, U+00AD y U+2060 ahora se detectan como autoaprobación. Test: `tests/test_governance.py:149`. Mutación M1 → `FAILED (failures=1)`. Los invisibles que no son Cf siguen en el riesgo residual §8 (ver G2-11). |
| G2-07 | **ACEPTADO SIN CAMBIO** | Declarado en `03-IMPLEMENTATION.md`. La decisión corresponde al Owner. |
| G3-03 | **CERRADO** | No había `__pycache__` antes de mis ejecuciones (0 directorios) y sigue sin haberlo después. |

## Revisión del diff completo (ciclo 2)
- **Regresiones:** no encontré ninguna. Los 19 tests pasan. La semántica de v1 (`legacy_errors`, `:162-196`) es la de la base. La compatibilidad con APP-001 del piloto se mantiene (GATE3-EVIDENCE-02).
- **Falsos PASS:** no encontré ninguno. `can-implement` exige `gate1 == 'PASS'` exacto (`:378`) y `can-close` exige tres PASS más APPROVED (`:388-389`). PWR no habilita (C2), lo cubre `tests/test_governance.py:278-298`.
- **Excepciones no controladas:** las de `report_text` están corregidas. Quedan dos casos preexistentes y fuera de alcance (G2-12).
- **Mensajes:** ninguna salida afirma que se comprueben identidades. Las únicas apariciones de «verific…» son etiquetas o expresiones como «verificación registrada», «sin verificación registrada», «registrado como verificado por» y «no comprueba identidades» (`scripts/quality_cli.py:92-100`, `:256-263`, `:344`, `:357`, `:379`).
- **Alcance:** las líneas añadidas del diff rastreado no mencionan skills, frameworks ni Appointments. Las menciones en `docs/MISSIONS/GOV-001/*` son citas de exclusión del alcance o referencias históricas.
- **Coherencia entre scripts:** `new_mission.py` no usa la misma canonización que `quality_cli.py` (G2-09).

## Evaluación de la incidencia declarada
`03-IMPLEMENTATION.md:96-97`: el Orchestrator/Developer borró `GATE2-INPUT.sha256` del ciclo 1 (`F0F7392A…4C9B`). He comprobado que el archivo no existe (`Test-Path` = False). Su hash y la coincidencia de sus 38 entradas solo constan en `GATE2-REVIEW-01.md`, que está intacto e idéntico al original de sesión.

Impacto: ya no se puede reverificar la entrada del ciclo 1 de forma independiente. La trazabilidad del ciclo 1 depende de la palabra del revisor de ese ciclo. No afecta a este ciclo, porque mi verificación se basa en la entrada `-02`, y el ciclo 1 queda superado. La incidencia se declaró de forma transparente y se adoptó una mitigación (numerar las entradas y no borrarlas). Aun así, borrar un artefacto de entrada de Quality sin autorización contradice AGENTS.md §4 («eliminar datos … sin autorización»). Ver G2-10.

## Hallazgos nuevos
| ID | Gravedad | Evidencia | Descripción | Corrección mínima |
|---|---|---|---|---|
| G2-08 | LOW | `scripts/quality_cli.py:22`, `:215` | La regla «no» de G2-05 se elude con puntuación antes de «no». Con PASS, se aceptan `sí -- no`, `sí — — no`, `sí: - no`, `sí — «no»` y `sí — (no)` (reproducido). La causa es que `(?!no\b)` solo mira el primer carácter después de `\s*`. Ningún test cubre estas variantes. Falla en modo abierto solo en la comprobación de presencia que v8 asume, y Quality lo detecta al leer el informe. | Consumir los separadores y la puntuación antes de la negación: `^s[ií]\s*[—–:;,\-]+[\s\W]*(?!no\b)(\w.*)$`, o rechazar si la primera palabra (`\w+`) de la evidencia es «no». Añadir 2 o 3 variantes a `tests/test_governance.py:226`. |
| G2-09 | LOW | `scripts/new_mission.py:31`, `:33` frente a `scripts/quality_cli.py:41` | `new_mission` valida `--orchestrator`/`--architect` con NFKC + `strip()`, sin eliminar los caracteres Cf. Con `--orchestrator "\u200b"` crea una misión cuyo manifiesto `validate` rechaza: `roles.orchestrator[0].id vacío` (reproducido). Falla en modo cerrado. Esta incoherencia la introdujo la corrección de G2-06. | Reutilizar `canon()` (o la misma regla) en `new_mission.py` para rechazar identificadores vacíos tras la canonización. |
| G2-10 | LOW (proceso) | `03-IMPLEMENTATION.md:96-97`; `GATE2-INPUT.sha256` inexistente | Se borró sin autorización la entrada de Quality del ciclo 1 (AGENTS.md §4). Se declaró y se mitigó, pero la pérdida no es reversible. | Ningún cambio de código. El Owner debe conocerla y aceptarla en `06-DECISION.md` u `OWNER-DECISION-*`, y la regla de no borrar entradas debe mantenerse. |
| G2-11 | INFO (riesgo residual §8) | `scripts/quality_cli.py:41` | Hay invisibles o confundibles que no son Cf y siguen sin detectarse como alias del developer: U+034F y U+FE0F (Mn), U+3164 (Lo), U+2800 (So) y el homoglifo cirílico `dеv-1` (reproducido). Están dentro del riesgo §8 aceptado («alias … mitigado por R1»). | Opcional: eliminar también los Default_Ignorable_Code_Point, o aplicar un control de confusables (UTS #39) en una misión posterior. |
| G2-12 | INFO (preexistente, fuera de alcance) | `scripts/quality_cli.py:28`, `:326` | (a) Un `mission.json` con anidamiento muy profundo provoca un `RecursionError` sin capturar en `read_json`. (b) `status` con un título que no es cp1252 y la salida redirigida provoca `UnicodeEncodeError`. Los dos terminan con exit ≠ 0 y traceback, sin falso PASS. En `29d741e` es igual (`read_json` idéntico y la base también imprime el título). | Opcional: capturar `RecursionError` y configurar `sys.stdout.reconfigure(errors='replace')`. |
| G2-13 | INFO | Sin `.gitattributes`; `core.autocrlf=true` | La reproducibilidad de los hashes de `GATE2-INPUT-02.sha256` tras un checkout depende de la configuración local (`autocrlf`). En un clon con `autocrlf=false` o en Linux, los hashes no coincidirán aunque el contenido sea el mismo. | Documentarlo en el paso 7 o fijar `.gitattributes` (`* text=auto eol=crlf`) en una misión posterior. |
| G2-14 | INFO (fuera de v8) | `scripts/quality_cli.py:240-247` | Un mismo `evidence_file` sirve como informe de Gate 2 y de Gate 3 si coinciden revisor, dictamen, artefacto y autor (reproducido: 0 errores). v8 no lo prohíbe y la base tampoco lo hacía. | Opcional: exigir `evidence_file` distintos por Gate. |

No encontré ningún BLOCKER, HIGH ni MEDIUM. No hay cambios de diseño que obliguen a reabrir Gate 1.

## Justificación del dictamen
Los hallazgos del ciclo 1 están cerrados (G2-01 a G2-04, G2-06 y G3-01 a G3-03), aceptados sin cambio (G2-07) o cerrados parcialmente (G2-05). Las tres correcciones de código se confirman con mutación. No hay regresiones, falsos PASS, mensajes que afirmen verificar identidades ni cambios de alcance. Quedan reservas LOW explícitas: G2-08 (elusión de la regla «no»), G2-09 (incoherencia en `new_mission`) y G2-10 (incidencia de proceso, que necesita conocimiento del Owner). Por eso el dictamen no es PASS. PASS_WITH_RESERVATIONS no equivale a PASS ni habilita transiciones (C2).

## Qué NO verifiqué
- La identidad real de copilot-sdk-main ni la mía. La veracidad de las `evidence.ref` de `GOV-001/mission.json`.
- El contenido exacto del `GATE2-INPUT.sha256` borrado, ni el diff entre el árbol del ciclo 1 y el del ciclo 2 (no es reconstruible). Revisé el árbol actual completo frente a `29d741e`.
- Otras plataformas, otras versiones de Python (solo probé Windows con Python 3.12.0) y otras configuraciones de `core.autocrlf`.
- El commit y el paso 7 de la secuencia v8.

## Limitación de independencia
Soy un subagente lanzado por el mismo agente principal que redactó el plan, implementó el diff y corrigió el ciclo 1. Mi separación es de contexto, no operativa. No puedo acreditar independencia, y este dictamen no suple la verificación de identidad que debe registrar un tercero (Owner).

**E2E NO EJECUTADO** (no aplica a una revisión de diff; ver GATE3-EVIDENCE-02).
