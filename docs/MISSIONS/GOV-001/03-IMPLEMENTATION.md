# GOV-001 · Registro de implementación

**Gate 1 aprobado:** `GATE1-REVIEW-08.md` PASS (diseño) sobre `PROPOSAL-v8.md`, 2026-11-05. Registro formal PENDING (ver `01-PLAN.md`). Implementación autorizada por `OWNER-DECISION-01.md`.
**Developer (autor efectivo):** copilot-sdk-main
**Base commit:** `29d741e641c77f8569ee74d2262bb70bc8b38be7`
**Trabajo previo local:** ninguno; árbol limpio antes de empezar (`git status --short` vacío, verificado también por Quality en los ciclos 5 a 8).

## Archivos realmente modificados
| Archivo | Qué cambió | Por qué | PROPOSAL-v8 |
|---|---|---|---|
| `scripts/quality_cli.py` | R0 estructural por versión; reglas v2 R1–R5b, R7, R8; v1 histórico con aviso y bloqueo de `can-*`; `status` con niveles de identidad; comparación canónica NFKC | causa raíz, C1–C3, D1, D4 | §3, §4 |
| `scripts/new_mission.py` | manifiesto v2; `--orchestrator`/`--architect`; `--author` obsoleto con aviso; Developer nunca por defecto | causa raíz, D2 | §5 |
| `tests/test_governance.py` | fixtures migradas a v2; 4 tests originales conservados en intención; 15 tests nuevos | §6 | §6 |
| `docs/templates/GATE1_REVIEW.md`, `GATE2_REVIEW.md`, `GATE3_EVIDENCE.md` | cabecera uniforme (Dictamen, Revisor, Verificación de identidad, Independencia verificada, Artefacto revisado, Autor efectivo); secciones finales renombradas a «Justificación del dictamen» | R5, R5b, G1-06 | §5, §7 |
| `docs/templates/MISSION_PLAN.md`, `IMPLEMENTATION_REPORT.md` | Architect/Orchestrator; Developer (autor efectivo) | C3 | §5 |
| `docs/MISSIONS/EXAMPLE-001/mission.json` | migrado a v2; Gates PENDING sin cambios | §5 | §5 |
| `docs/QUALITY_POLICY.md` | PASS_WITH_RESERVATIONS no habilita; sin política de waivers no hay excepciones | C2, G1-09 | §5 |
| `docs/QUALITY_EVIDENCE_PROTOCOL.md` | sección «Identidades (manifiesto v2)» | C1, C3, D1 | §5 |
| `docs/MISSIONS/README.md` | uso v2, alias obsoleto, niveles de identidad, migración v1 | D1, D2 | §5 |
| `AGENTS.md`, `docs/ROLE_MATRIX.md` | rol Orchestrator (una viñeta; columna, fila y registro de herramientas) | D3, D4 | §5 |
| `quality/controls.json` | `identity_verification_record_required: true` (informativo) | G1-16 | §5 |
| `README.md` | ejemplo de `new_mission.py` sin `--author` | documentación directamente afectada | — |
| `FILE_INDEX.md` | entrada `docs/MISSIONS/GOV-001/` | inventario | — |
| `docs/MISSIONS/GOV-001/*` | registro de la misión | secuencia, paso 4 | §5 |

## Diferencias de alcance
- Ninguna de diseño. Dos adiciones documentales no listadas en §5: `README.md:24`, que usaba `--author`, y la entrada en `FILE_INDEX.md`.
- `controls.json`: el valor es `true`, tal como dice el plan.

## Pruebas locales ejecutadas
Entorno: Windows, Python 3.12.0, PROTHEUSAI-CORE con base `29d741e` más el árbol de trabajo de esta misión, 2026-11-05T08:24+01:00.

| Comando | Exit | Resultado |
|---|---|---|
| `python -m unittest discover -s tests -v` | 0 | 19 tests OK |
| `python scripts/quality_cli.py validate` | 0 | OK (estructura; no certifica Quality ni identidades) |
| `python scripts/quality_cli.py can-implement --mission GOV-001` | 1 | BLOCKED, como se espera: Gates PENDING |
| Control de mutación: los mismos tests con `scripts/quality_cli.py` de `29d741e`, en una copia temporal fuera del repositorio | 1 | 44 fallos y 4 errores; los tests detectan la ausencia del cambio |

Correspondencia con §6 de `PROPOSAL-v8.md`:

| Test | Casos de §6 |
|---|---|
| test_new_mission_starts_pending_and_preserves_existing | P1, N1 |
| test_full_chain_with_registered_verifications | P2, N37 |
| test_v1_manifests_are_historical | P3, P5, P7a, N11, legado v1 |
| test_author_alias_is_deprecated_and_only_sets_orchestrator | P4, N36, N41 |
| test_filled_templates_satisfy_report_rules | P6 |
| test_gate2_requires_known_developer | N2 |
| test_no_self_approval_or_missing_evidence | N3, N4, N5, N9, N12, evidencia y path traversal |
| test_identities_need_registered_verification | N6, N7, N17, N18, R1b |
| test_report_must_match_manifest | N8, N13–N16, N19, N29, N30, N35 (informe) |
| test_reviewed_artifact_requires_name_and_version | N35 (manifiesto) |
| test_effective_author_may_be_subset_of_developers | N40 |
| test_fail_must_be_traceable_but_never_enables | N22, N39 |
| test_pass_with_reservations_never_enables | N10, N21, N34 |
| test_owner_approval_cannot_come_from_authors | N23, N38 |
| test_orchestrator_acting_as_developer | N33 |
| test_must_pass_gate1_before_gate2 | N24 |
| test_malformed_records_fail_without_exceptions | N20, N25–N28, N31, N32 |
| test_cli_never_claims_identity_checks | N37, N42 |
| test_package_has_all_required_files_and_example_pending | compatibilidad de la plantilla |

### P7b — piloto histórico, solo lectura
CLI nueva de CORE con `--root C:\0.-REPOSITORIOS-DESARROLLO\0003. EN DESARROLLO\protheus-efd` (HEAD `ebf10ea`, árbol limpio):

| Comando | Exit | Resultado |
|---|---|---|
| `validate` | 0 | AVISO: APP-001 y EXAMPLE-001 v1 históricos; OK |
| `can-implement --mission APP-001` | 1 | BLOCKED: manifiesto v1 histórico |
| `can-close --mission APP-001` | 1 | BLOCKED: manifiesto v1 histórico |
| `status --mission APP-001` | 0 | tres PASS históricos visibles, revisor `/root/quality` |

`APP-001/mission.json` SHA-256 antes y después: D3E1AA17F89E01C72D0787EC846AC22B69A17B783D534E41E30E91EBFECBA39F (sin cambios). `git status --porcelain` del piloto vacío antes y después.

E2E NO EJECUTADO (no aplica: herramienta de gobernanza sin interfaz).

## Incidencias
- Pasar un script de Python por un pipe de PowerShell 5.1 sustituyó «ó» por «?» en `GOV-001/mission.json` (`ref`). Se corrigió escribiendo con escape `\u00f3`, y se revisaron todos los archivos cambiados: no hay más sustituciones ni caracteres U+FFFD.

## Riesgos y deuda técnica
- Los alias de una misma entidad no son detectables por comparación de texto; las reglas de verificación registrada los mitigan, no los eliminan.
- `approved_by` sigue siendo una cadena declarada (riesgo residual aceptado en §8).
- La convención de hash CRLF/LF para artefactos copiados está documentada, no automatizada.
- Ningún Gate de GOV-001 puede registrarse como PASS hasta que un tercero (Owner) registre la verificación de las identidades.

## Reapertura de Gate 2 — ciclo 2
Motivo: Gate 2 y Gate 3 ciclo 1 PASS_WITH_RESERVATIONS (`GATE2-REVIEW-01.md` sha256:68A4B5D59E17319FF4C54045BA9CC758EB62C66931971F631912DF2C61232DF8, `GATE3-EVIDENCE-01.md` sha256:323EFBFD6CA55FFF130AA08108D9A365F8DFAC31EB9149E0D3A4960E61ABB055). Por C2, un PASS_WITH_RESERVATIONS no habilita el commit. Sin cambios de diseño, así que no se reabre Gate 1.

| Hallazgo | Corrección |
|---|---|
| G2-01 / G3-02 | `report_text()` lee el informe sin lanzar excepciones (`OSError`, `ValueError`, `UnicodeError` → informe ausente). `has_evidence()` delega en ella. Tests: `evidence_file` con NUL y con informe no UTF-8. |
| G2-02 / G3-01 | Subcasos añadidos: `**Autor efectivo:**` duplicado (N35); FAIL sin `**Autor efectivo:**` y FAIL con artefacto sin hash (N39); `verification` sin un campo (N7). |
| G2-03 | Los archivos escritos en LF se normalizan a CRLF en el árbol de trabajo, el formato que produce `core.autocrlf=true` al hacer checkout. Así los hashes de `GATE2-INPUT-02.sha256` son reproducibles tras un checkout en Windows. |
| G2-04 | Mensaje de `can-implement` corregido: «Identidades: verificación registrada, no comprobada por la CLI». |
| G2-05 | `**Independencia verificada:**` rechaza una evidencia que empiece por «no» (p. ej. «si — no»). Test añadido. |
| G2-06 | `canon()` elimina los caracteres Unicode de categoría Cf (p. ej. U+200B) antes de comparar. Test de suplantación con un carácter de ancho cero. |
| G2-07 | Sin cambio; declarado arriba. |
| G3-03 | Los `__pycache__` (ignorados por Git) se eliminan antes de la revisión. |

Control de mutación del ciclo 2: al revertir por separado el filtro Cf, la regla «no» y la captura de excepciones, cada mutación hace fallar al menos un test (exit 1).

### Incidencia del ciclo 2
Al regenerar la entrada de Gate 2, el Orchestrator/Developer borró `GATE2-INPUT.sha256` del ciclo 1 (sha256 F0F7392A971467AD7816DA81AE7BEF57323249E36F0AC10C0838DBC1768C4A9B) en lugar de conservarlo. No es reconstruible byte a byte porque `scripts/quality_cli.py` y `tests/test_governance.py` ya habían cambiado. Su existencia, su hash y la coincidencia de sus 38 entradas con el árbol de entonces constan en `GATE2-REVIEW-01.md`, que se conserva intacto. Desde el ciclo 2, cada entrada se guarda con su propio número (`GATE2-INPUT-02.sha256`) y no se borra.

### Ejecución del ciclo 2 (2026-11-05T08:34:43+01:00, Windows, Python 3.12.0, tras normalizar a CRLF)
| Comando | Exit | Resultado |
|---|---|---|
| `python -B -m unittest discover -s tests` | 0 | 19 tests OK |
| `python -B scripts/quality_cli.py validate` | 0 | OK |
| `python -B scripts/quality_cli.py can-implement --mission GOV-001` | 1 | BLOCKED (se espera: Gates PENDING) |

## Reapertura de Gate 2 — ciclo 3
Motivo: Gate 2 y Gate 3 ciclo 2 PASS_WITH_RESERVATIONS (`GATE2-REVIEW-02.md` sha256:9980D46D03185A853B430AF4A1A7E80C48B3473F28C597C619EC00C4DEA46D3C, `GATE3-EVIDENCE-02.md` sha256:10A4B43B3F4FFACEBF2E6B5E51B4A550D8E47F7A3CBF31A3673ED9426415D3D9). Sin cambios de diseño.

| Hallazgo | Corrección |
|---|---|
| G2-08 / G3-04 | La evidencia de independencia se compara tras quitar la puntuación inicial; se rechaza si su primera palabra es «no» (`sí -- no`, `sí — «no»`). Tests añadidos. |
| G2-09 | `new_mission.py` usa `canon()` de `quality_cli.py`: un orchestrator o architect formado solo por caracteres invisibles se rechaza al crear la misión. Test añadido. |
| G2-10 | Incidencia ya declarada (ciclo 2); pendiente de conocimiento y aceptación del Owner. |
| G2-11, G2-12, G2-13, G2-14 | INFO, sin cambio: riesgo residual de alias (§8); errores preexistentes que fallan cerrado; ausencia de `.gitattributes`; reutilización de `evidence_file`. Se elevan al Owner. |

Control de mutación: al revertir la regla de G2-08 fallan 3 aserciones; al revertir G2-09, 1.

### Ejecución del ciclo 3 (2026-11-05T08:40:59.2381612+01:00, Windows, Python 3.12.0)
| Comando | Exit | Resultado |
|---|---|---|
| `python -B -m unittest discover -s tests` | 0 | Ran 19 tests in 0.653s OK |
| `python -B scripts/quality_cli.py validate` | 0 | OK |
| `python -B scripts/quality_cli.py can-implement --mission GOV-001` | 1 | BLOCKED (se espera) |
