# GOV-001 · Gate 1 — Revisión independiente, ciclo 5

**Dictamen:** FAIL
**Revisor:** quality-gov001-c5
**Verificación de identidad:** solo declarada. Es el nombre asignado por el agente principal al lanzar este subagente. Podría acreditarse con el registro de lanzamiento del runtime (spawn handle/log de sesión e5be03ee…), pero no tengo acceso a ese registro. Ni este informe ni la CLI verifican esta identidad.
**Independencia verificada:** no — separación solo contextual: en este contexto no redacté v1–v5 ni implementaré la misión. Sin embargo, soy un subagente del mismo runtime que el autor (copilot-sdk-main) y, posiblemente, de la misma familia de modelo; no dispongo de una prueba operativa de separación.
**Artefacto revisado:** GOV-001-PROPOSAL-v5.md sha256:991A3B2AFE2A3420FD90E0A18853197CA60A1E821406999ABA4993EFC27A6B6E
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** estático, contrastado con el código real de PROTHEUSAI-CORE `29d741e`, además de ejecuciones de solo lectura de la CLI y los tests base (ver §Evidencia ejecutada).

## Integridad del artefacto y del entorno
- `Get-FileHash GOV-001-PROPOSAL-v5.md` = `991A3B2A…6B6E`: coincide con el hash declarado. `GOV-001-PROPOSAL.md` tiene el mismo hash. El hash de v4 es `09D2451F…CF10` y también coincide.
- PROTHEUSAI-CORE: `git log -1` = `29d741e`; `git status --short` vacío antes y después de la revisión.
- Piloto protheus-efd: `ebf10ea`; árbol limpio; solo lectura. `scripts/quality_cli.py` es idéntico byte a byte al de CORE (sha256 `8C080050…1F68`).
- No había informes de los ciclos 1–4 en `files/`; solo están las propuestas v1–v5.

## Evidencia ejecutada (solo lectura, `python -B`)
| Comando | Exit | Resultado |
|---|---|---|
| protheus-efd: `python -B scripts\quality_cli.py validate` | 0 | OK estructura |
| protheus-efd: `python -B scripts\quality_cli.py can-close --mission APP-001` | 1 | BLOCKED (owner PENDING) |
| CORE: `python -B -m unittest discover -s tests -q` | 0 | Ran 4 tests, OK |

## Hallazgos
| ID | Gravedad | Evidencia | Problema | Corrección mínima |
|---|---|---|---|---|
| G1-08 | **HIGH (bloqueante)** | v5:69 («R2 y R1b impiden que revise, **apruebe**…»); v5:50 (R0.b: `approved_by` solo se valida como str/null); v5:64 (R7: owner APPROVED solo exige tres PASS); `scripts/quality_cli.py:84-88,153-156` | **D4 no se cumple en la aprobación.** R2 y R1b solo afectan a los revisores de Gate y a quien verifica su identidad. Nada impide `owner_acceptance.approved_by` = Developer u Orchestrator-Developer. Con tres PASS independientes, `can-close` devolvería 0 aunque el autor hubiera aprobado su propio trabajo. Esto contradice D4 («nunca podrá … aprobar su propio trabajo») y AGENTS.md:20. La afirmación de v5:69 es inexacta. | En v2, añadir la regla: si `owner_acceptance.status`=APPROVED, `approved_by` canónico (NFKC+strip+casefold) ∉ `roles.developer` → «aprobación por autor del trabajo». Añadir un test N38 con un Orchestrator-Developer como `approved_by` → error y `can-close`=1. Corregir el texto de v5:69. |
| G1-09 | MEDIUM | v5:64 (excepciones «siguen AGENTS.md:36» fuera de la CLI); `docs/QUALITY_POLICY.md:27` («PWR … admisibilidad para avanzar exige política/owner»), `:9`; v5:79 (QUALITY_POLICY.md no figura en §5) | **C2 parcial.** C2 exige a la vez una política explícita de waivers y una autorización humana. No existe ninguna política de waivers. v5 remite solo a la decisión humana (AGENTS.md:36, que trata FAIL/BLOCKED). Además, QUALITY_POLICY.md:27 sigue diciendo que basta «política/owner», en contradicción con C2. No hay un falso PASS en la CLI, pero sí una norma contradictoria (AGENTS §1). | Añadir `docs/QUALITY_POLICY.md` a §5. Reescribir :9 y :27: PWR ≠ PASS y no habilita transiciones. Solo habrá excepciones mediante una política de waivers explícita y aprobada **y** autorización humana documentada; mientras esa política no exista, no se admiten excepciones. Un waiver nunca se registra como PASS. |
| G1-10 | MEDIUM | v5:61 (R5b solo PASS/PWR); v5:105 (§9 «C3 … en cada revisión → R5b»); v5:87 (N22: FAIL sin revisor no produce falso PASS) | **C3 limitado.** C3 se aplica a «cada revisión». Un Gate FAIL registrado en `mission.json` puede carecer de revisor, artefacto, hash, autor efectivo e informe y aun así superar `validate`. No produce un falso PASS, pero la trazabilidad exigida no se cumple y §9 afirma lo contrario. | Aplicar R0/R5/R5b(a–c) y la presencia de `reviewer`/`evidence_file`/`date` también a `decision`=FAIL, sin R1/R4b. Añadir test. Otra opción: declarar explícitamente la limitación y someterla a aceptación del Owner. |
| G1-11 | MEDIUM | v5:81 («informes Quality (ciclos 1–4 como transcripción literal declarada…)»); directorio `files/` sin informes GATE1-REVIEW-01..04 | **Riesgo de registro de autoría ajena (C3, AGENTS §1).** El autor de la propuesta reconstruiría los dictámenes de Quality. Ni la CLI ni Quality pueden comprobar que esa transcripción sea «literal», y el texto no tendría la autoría efectiva del revisor. | Incorporar solo los informes originales, con su hash. Si alguno no se conserva, sustituirlo por una nota de autoría del Orchestrator: «original no conservado; dictamen según <ref verificable: id de evento/log>». Esa nota no debe usarse nunca como `evidence_file` de un Gate. |
| G1-12 | LOW | v5:81 (Gates de GOV-001 PENDING «mientras no exista verificación efectiva por un tercero»; registro «creado con la nueva CLI») | Secuencia indefinida. La nueva CLI no existe antes de implementarse, y con Gate 1 en PENDING `can-implement`=1. Implementar en ese estado exige una decisión humana documentada (AGENTS.md:36) o la verificación del Owner, pero v5 no lo establece. | Declarar en el plan qué ocurrirá: o el Owner verifica las identidades (y se registra `verification.by`=Owner), o el Owner emite una excepción documentada para implementar con el registro PENDING. Precisar que el registro GOV-001 se crea tras la implementación. |
| G1-13 | LOW | v5:91 (P7: «copia del `mission.json` de APP-001 … en carpeta temporal → `validate` 0»); `quality_cli.py:49-50,71,93` | Tal como está redactado, P7 no es ejecutable. Una copia que solo contenga `mission.json` fallaría por `falta 01-PLAN.md…`, por `has_evidence` de GATE1-REVIEW-03.md/GATE2/3-OWNER-VISUAL-01.md y por los FILES de raíz. Hoy el piloto completo valida con 0 (verificado). | Copiar la carpeta APP-001 completa dentro de un proyecto temporal con los FILES requeridos. Otra opción es invocar `mission_errors` sobre la copia completa de la carpeta. |
| G1-14 | LOW | v5:62 («comprobaciones v1 vigentes **sin cambios** (R0.b+R0.c + reglas actuales)»); `quality_cli.py:42-89` no exige `created_at` ni tipos de `reviewed_artifact`/`date`/`approved_by` | Contradicción interna. R0.b/R0.c endurecen la validación de v1. Proyectos derivados con v1 válidos hoy podrían pasar a INVALID, en contra de §7 («CI no se rompe»). El piloto APP-001 cumple R0.b/R0.c (verificado en mission.json:1-37). | Corregir la redacción («v1 = reglas actuales + R0.b/R0.c») y documentar en §7 que los v1 con tipos o claves anómalos pasan a INVALID. Alternativa: limitar R0 en v1 a lo que hoy ya se exige. |
| G1-15 | LOW | v5:74 (`--author` → `roles.orchestrator`); `docs/MISSIONS/README.md:6` (`--author "dev-01"`) | D2 se cumple: el alias nunca se copia a implementation_author ni a developer. Pero el uso documentado hoy registraría a un desarrollador como orchestrator, que es un rol que el usuario no declaró. No produce un falso PASS, porque R2 usa la unión de roles y R4 exige architect. | El aviso DEPRECATED debe decir literalmente «registrado como orchestrator; developer/architect no asignados». Incluir esa comprobación en N36. |
| G1-16 | LOW | v5:55 (mensaje «identidad de revisor no **verificada**»); v5:82 (`identity_verification_required`) | Vocabulario C1. Mezcla «sin verificación registrada» con «no verificada» y sugiere que la CLI verifica. | Usar «sin verificación registrada» y `identity_verification_record_required`, o añadir una nota indicando que la clave es informativa. |
| G1-17 | LOW | v5:42 (listas para varios ciclos); v5:61 R5b(c) (conjunto de «Autor efectivo» = todos los `developer`) | Si hay varios ciclos con distintos Developers, el informe de una versión debe listar como «autor efectivo» a autores que no tocaron esa versión. Es una atribución inexacta frente a C3. | Documentarlo como riesgo residual o como regla de proceso: al reabrir Gate 2/3, `roles.developer` debe reflejar los autores efectivos del diff vigente, conservando el histórico en informes. No añadir campos. |

Los hallazgos G1-01..G1-07 no se reabren. Las reglas R0, R4b y R5 de v4 se mantienen sin regresión aparente.

## Estado D1–D4 / C1–C3
| Decisión | Estado | Justificación |
|---|---|---|
| D1 | Cumple, con una reserva (G1-14, G1-13) | R6 deja `can-*`=1 para todo v1, `validate` devuelve 0 con AVISO y los bytes permanecen intactos (N11). La migración y la revalidación son explícitas y los informes se conservan. |
| D2 | Cumple, con una reserva (G1-15) | El alias rellena solo `orchestrator`, emite DEPRECATED, no se puede combinar con `--orchestrator` y nunca rellena developer ni implementation_author. |
| D3 | Cumple | Cambio mínimo en AGENTS.md §2 y ROLE_MATRIX.md (una viñeta y una fila/columna). Hoy Orchestrator solo aparece en AGENTS.md:25. |
| D4 | **NO cumple** (G1-08) | Revisión: R2 y R1b sí lo impiden. Aprobación: `owner_acceptance.approved_by` no se controla. |
| C1 | Cumple, con una reserva (G1-16) | Hay tres niveles derivados, sin autoverificación, y N37 prohíbe afirmar una verificación hecha por la CLI. |
| C2 | Parcial (G1-09) | En la CLI es correcto: R7 y N34 impiden que PWR habilite transiciones. Falla en la política: QUALITY_POLICY:27 contradice C2 y no hay política de waivers. |
| C3 | Parcial (G1-10, G1-11, G1-17) | R5b cubre PASS/PWR, pero no FAIL. Además hay transcripciones redactadas por el autor y una atribución multi-ciclo. |

No encontré sobreingeniería ni requisitos de dominio. Los cambios fuera de alcance (skills, frameworks multiagente) no aparecen.

## Qué NO verifiqué
- No ejecuté ninguna implementación de v5 porque no existe. Las pruebas P/N son solo previstas: NOT_RUN.
- No verifiqué la identidad real de copilot-sdk-main ni la mía, ni la autenticidad de la decisión Owner (usé el resumen que me proporcionaron). Tampoco revisé los informes Quality de los ciclos 1–4, que no están disponibles.
- No revisé `EXPERIMENT-LOG.md` del piloto ni los informes de APP-001 más allá de la lista de archivos y de `mission.json`.
- No revisé `docs/ARCHITECTURE.md`, `PROJECT_CHARTER.md` ni `quality/RISK_MATRIX.md`.
- E2E NO EJECUTADO (no aplica a Gate 1).

## Limitación de independencia
Este informe procede de un subagente lanzado por el mismo runtime que el autor (copilot-sdk-main), posiblemente con la misma familia de modelo. Solo hay separación de contexto, sin prueba operativa de separación. Según la propia v5 (R1, R4b), este dictamen no podría habilitar un Gate en un manifiesto v2 sin que un tercero, como el Owner, verifique las identidades. Un FAIL no autoriza nada, por lo que este riesgo no genera un falso PASS.
