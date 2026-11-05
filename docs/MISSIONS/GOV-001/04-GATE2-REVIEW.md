# GOV-001 · Gate 2 — Diff review, ciclo 3

**Dictamen:** PASS
**Revisor:** quality-gov001-g23-c3
**Verificación de identidad:** solo declarada. Es el nombre asignado por el agente principal (copilot-sdk-main) al lanzar este subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime. Ni este informe ni la CLI verifican identidades.
**Independencia verificada:** no — la separación es solo contextual. No redacté PROPOSAL-v1..v8 ni implementé el diff ni sus correcciones, pero soy un subagente del mismo runtime que el autor (copilot-sdk-main) y no hay prueba operativa de separación.
**Artefacto revisado:** GOV-001 árbol de trabajo GATE2-INPUT-03.sha256 sha256:386928494e5ccdafdb580ecb2298f6538e49247ef38a13e6e4e8920ee7e8d29c
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática del diff completo respecto a `29d741e` (17 archivos rastreados y 27 archivos en `docs/MISSIONS/GOV-001/`), centrada en los cambios del ciclo 3 contra PROPOSAL-v8, OWNER-DECISION-01, GATE2-REVIEW-02/GATE3-EVIDENCE-02 y `03-IMPLEMENTATION.md` §«Reapertura de Gate 2 — ciclo 3». Además, 50 casos adversariales propios y 4 mutaciones en una copia en `%TEMP%\g23c3_adv`, ya borrada (`Test-Path` = False). No modifiqué ningún archivo del repositorio ni del piloto. Usé siempre `python -B`.

> El dictamen PASS es **técnico** y vale solo para la versión identificada arriba; no se transfiere a versiones posteriores. Por la línea `Independencia verificada: no`, este informe no puede servir como `evidence_file` de un Gate v2 en PASS/PWR (R4b): registrar el Gate exige que un tercero (Owner) resuelva la independencia y la verificación de identidades.

## Integridad de la entrada
- `Get-FileHash GATE2-INPUT-03.sha256` = `38692849…D29C`: coincide con la instrucción. Lo comprobé al empezar (08:41) y al terminar (08:43).
- 43 entradas `<sha256>  <ruta>`; las 43 coinciden con el árbol (0 discrepancias, 0 ausentes) al empezar y al terminar.
- `git status --porcelain --untracked-files=all`: 44 entradas = las 43 del manifiesto + el propio `GATE2-INPUT-03.sha256` (excluido por diseño). HEAD `29d741e`. `git diff --stat 29d741e` = `17 files changed, 810 insertions(+), 134 deletions(-)`, igual que el manifiesto.
- Diferencias entre las entradas `-02` y `-03` (comparación de hashes): solo `scripts/quality_cli.py`, `scripts/new_mission.py`, `tests/test_governance.py`, `03-IMPLEMENTATION.md`, y los añadidos `GATE2-INPUT-02.sha256`, `GATE2-REVIEW-02.md`, `GATE3-EVIDENCE-02.md`. El resto (documentación, plantillas, `controls.json`, EXAMPLE-001) no cambió desde el ciclo 2.
- `GATE2-INPUT-02.sha256` (`171CD005…5E28`), `GATE2-REVIEW-02.md` (`9980D46D…`) y `GATE3-EVIDENCE-02.md` (`10A4B43B…`) se conservan y son byte-idénticos a los originales de la carpeta de sesión; coinciden con los hashes citados en `03-IMPLEMENTATION.md`.
- `core.autocrlf=true`; sin `.gitattributes`; 0 `__pycache__` antes y después.

## Estado de los hallazgos previos
| ID | Estado | Evidencia |
|---|---|---|
| G2-08 | **CERRADO** | `scripts/quality_cli.py:216-217`: se quitan los caracteres no alfanuméricos iniciales (`re.sub(r'^\W+','',…)`) y se rechaza si la evidencia empieza por `no\b`; además se rechaza la evidencia vacía tras quitarlos. Casos propios rechazados (18/18): `sí -- no`, `sí — «no»`, `sí — — no`, `sí: - no`, `sí — (no)`, `sí — 'no'`, `sí — "no"`, `sí — ¿no?`, `sí — ¡no!`, `sí — No.`, `SÍ — NO`, `sí — n\u200bo`, `sí — ｎｏ`, `sí —\u00a0no`, `sí — …no`, `sí — no\u00ad`, `sí , no`, `sí; no`. Controles positivos aceptados: `sí — nota: log:x`, `sí — nombre del log`, `si: log:abc`. Mutaciones: quitar el `re.sub` → `FAILED (failures=2)`; quitar la regla `no\b` → `FAILED (failures=3)`. |
| G3-04 | **CERRADO** | `tests/test_governance.py:232-233` añaden `sí -- no` y `sí — «no»`; detectan la mutación anterior (failures=2). |
| G2-09 | **CERRADO** | `scripts/new_mission.py:10` importa `canon` de `quality_cli`; `:32` y `:34` lo aplican a `orchestrator` y `architect` antes de `mkdir` (no se crea carpeta al rechazar). Casos propios: U+200B, U+2060, U+00AD, U+FEFF, `' \u200b '`, `' '`, `'\t'` → `ValueError`, sin carpeta; CLI con `--orchestrator`, `--author` y `--architect` invisibles → exit 2, sin carpeta. Coherencia: los identificadores que `new_mission` acepta (U+3164, U+034F, U+2800, `\u200bx`) también los acepta `validate` (0 errores); ya no hay creación de manifiestos que `validate` rechace. Invocación del script desde otro cwd: exit 0 (el import funciona). Tests `tests/test_governance.py:119-123`; mutaciones `orchestrator.strip()` y `architect.strip()` → `FAILED (failures=1)` cada una. |
| G2-10 | **DECISIÓN DEL OWNER** (no defecto de código) | Incidencia de proceso del ciclo 2 (borrado de `GATE2-INPUT.sha256`). Declarada en `03-IMPLEMENTATION.md`; la regla de no borrar entradas se ha respetado en el ciclo 3 (`GATE2-INPUT-02.sha256` conservado e íntegro). Falta el conocimiento/aceptación del Owner en `06-DECISION.md` u `OWNER-DECISION-*` (`06-DECISION.md` sigue en plantilla PENDING). |
| G2-11 | **DECISIÓN DEL OWNER** (riesgo residual §8) | Sin cambio; confirmado: U+3164, U+034F, U+2800 siguen aceptándose como identificadores. |
| G2-12 | **DECISIÓN DEL OWNER** (preexistente, falla cerrado) | Sin cambio; `read_json` (`scripts/quality_cli.py:26-33`) no captura `RecursionError`, igual que la base. |
| G2-13 | **DECISIÓN DEL OWNER** | Sin cambio; sigue sin `.gitattributes`. |
| G2-14 | **DECISIÓN DEL OWNER** (fuera de v8) | Sin cambio; `v2_errors` no exige `evidence_file` distintos por Gate. |

## Revisión del diff completo (ciclo 3)
- **Regresiones:** ninguna. 19 tests pasan (mismo número de métodos que el ciclo 2; los casos nuevos son subcasos). Las líneas eliminadas de `tests/test_governance.py` respecto a la base son la migración v1→v2 ya revisada en ciclos 1-2; los 4 métodos originales siguen presentes. La semántica v1 (`legacy_errors`) no cambió. Compatibilidad con APP-001 confirmada (GATE3-EVIDENCE-03).
- **Falsos PASS:** ninguno. `can-implement` exige `gate1 == 'PASS'` exacto (`:379`); `can-close` exige tres PASS y APPROVED (`:389-390`). PWR no habilita (C2). Con un Gate PASS completo y válido, `can-close` devuelve 1 si el owner no está APPROVED (caso propio).
- **Excepciones no controladas:** ninguna nueva. `canon()` acepta cualquier tipo (devuelve `''` si no es texto), así que `create_mission` con un orchestrator no textual da `ValueError` en lugar de `AttributeError`. Persisten solo las de G2-12 (preexistentes).
- **Mensajes:** ninguna salida afirma comprobar identidades. `status`/`can-implement` dicen «verificación registrada por …; no comprobada por la CLI» (comprobado en caso propio).
- **Alcance:** los cambios del ciclo 3 se limitan a G2-08/G2-09/G3-04 y al registro de la misión. No hay skills, frameworks multiagente ni otras funciones de v1.1. Sin cambios de diseño: no procede reabrir Gate 1.
- **Acoplamiento nuevo:** `new_mission.py` depende ahora de `quality_cli.py` (mismo directorio). Es la corrección propuesta en G2-09 y funciona por invocación directa del script; no es un defecto.

## Hallazgos nuevos
| ID | Gravedad | Tipo | Evidencia | Descripción | Corrección mínima |
|---|---|---|---|---|---|
| G2-15 | INFO | Riesgo residual (decisión del Owner, misma clase que G2-11/§8) | `scripts/quality_cli.py:216-217`; casos propios | La regla «no» es una heurística de presencia. Se aceptan como evidencia de independencia: `sí — nо` (о cirílica), `sí — n\u0336o` (combinante Mn), `sí — _no`, `sí — 1) no`, y negaciones semánticas (`sí — falso`, `sí — ninguna evidencia`). En sentido contrario, `sí — no-op` se rechaza (falla cerrado). Requiere un informe deliberadamente engañoso; Quality/Owner leen el informe. | Opcional, misión posterior: control de confusables (UTS #39) o declaración estructurada de independencia. |

No encontré ningún defecto BLOCKER, HIGH, MEDIUM ni LOW. No hay hallazgos G2 nuevos que exijan cambio de código.

## Decisiones pendientes del Owner (no son defectos)
- G2-10: conocimiento y aceptación de la incidencia de borrado del ciclo 1.
- G2-11, G2-12, G2-13, G2-14, G2-15: aceptar como riesgo residual o programar en misión posterior.
- Verificación de identidades de los roles y del revisor por un tercero, e independencia operativa de Quality (sin ellas ningún Gate de GOV-001 puede registrarse como PASS en el manifiesto, R4b).

## Justificación del dictamen
Las tres reservas técnicas del ciclo 2 (G2-08, G2-09, G3-04) están cerradas y cada corrección se confirma con casos propios y mutación. No hay regresiones, falsos PASS, excepciones nuevas no controladas, mensajes que afirmen verificar identidades ni cambios de alcance. Lo que queda (G2-10..G2-15) son decisiones del Owner o riesgos residuales aceptados en §8, identificados como tales; según la instrucción del Owner no impiden el PASS técnico. Este PASS no habilita por sí solo ninguna transición: este informe declara `Independencia verificada: no` y no puede usarse como `evidence_file` de un Gate en PASS.

## Qué NO verifiqué
- La identidad real de copilot-sdk-main ni la mía; la veracidad de las `evidence.ref` de `GOV-001/mission.json`.
- El diff textual exacto entre el árbol del ciclo 2 y el del ciclo 3 (no hay instantánea; solo comparé hashes y revisé el estado actual completo frente a `29d741e`).
- Otras plataformas, versiones de Python (solo Windows con Python 3.12.0) y configuraciones de `core.autocrlf`.
- El commit y el paso 7 de la secuencia v8.

## Limitación de independencia
Soy un subagente lanzado por el mismo agente principal que redactó el plan, implementó el diff y corrigió los ciclos 1 y 2. Mi separación es de contexto, no operativa. No puedo acreditar independencia, y este dictamen no suple la verificación de identidad que debe registrar un tercero (Owner).

**E2E NO EJECUTADO** (no aplica a una revisión de diff; ver GATE3-EVIDENCE-03).
