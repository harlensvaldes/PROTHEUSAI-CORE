# GOV-001 · Gate 1 — Revisión independiente, ciclo 6

**Dictamen:** FAIL
**Revisor:** quality-gov001-c6
**Verificación de identidad:** solo declarada. Es el nombre que el agente principal asignó al lanzar este subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime, y ni este informe ni la CLI verifican la identidad.
**Independencia verificada:** no — la separación es solo contextual: no redacté v1–v6 ni implementaré la misión, pero soy un subagente del mismo runtime que el autor (copilot-sdk-main) y no existe una prueba operativa de separación.
**Artefacto revisado:** GOV-001-PROPOSAL-v6.md sha256:91C4591459D0C7629B0644D0CC478DBF18EF660F3C29BB5DC410A4ADC3E089DF
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v6 y del diff v5→v6 (Compare-Object), contrastada con PROTHEUSAI-CORE `29d741e`. Ejecuté también comandos de solo lectura con `python -B`; ver §Evidencia.

## Integridad y entorno
- `Get-FileHash`: v6 = `91C45914…89DF` (coincide); v5 = `991A3B2A…6B6E` (coincide); GATE1-REVIEW-05 = `8D67E282…6AF9` (coincide). `GOV-001-PROPOSAL.md` tiene el mismo tamaño que v6 (22533 B); no calculé su hash.
- Leí `AGENTS.md` y `agents/quality.md` de PROTHEUSAI-CORE.
- PROTHEUSAI-CORE: `git log` = `29d741e`; `git status --short` estaba vacío antes y después de la revisión.
- Piloto protheus-efd: `ebf10ea`, árbol limpio. Solo lo leí.

## Evidencia ejecutada (solo lectura)
| Comando | Exit | Resultado |
|---|---|---|
| CORE `python -B -m unittest discover -s tests -q` | 0 | Ran 4 tests, OK |
| CORE `python -B scripts\quality_cli.py validate` | 0 | OK estructura |
| piloto `python -B scripts\quality_cli.py validate` | 0 | OK estructura |
| piloto `python -B scripts\quality_cli.py can-close --mission APP-001` | 1 | BLOCKED |

## Estado de G1-08..G1-17
| ID | Estado | Evidencia |
|---|---|---|
| G1-08 | CERRADO (queda la reserva G1-18) | v6:65 añade R8: `approved_by` ∉ developer ∪ architect, con can-close=1. N38 (v6:95) cubre al Orchestrator-Developer normalizado. v6:70 está corregido. Hoy `quality_cli.py:84-88` solo exige que `approved_by` no esté vacío. |
| G1-09 | CERRADO en lo que pedía G1-09 (G1-19 añade un problema de alcance) | v6:81 incluye `QUALITY_POLICY.md:9,27` en §5. v6:64 (R7) establece que no hay excepciones sin una política de waivers, que se exigirán política **y** autorización humana y que un waiver nunca se registra como PASS. Esto encaja con C2. |
| G1-10 | CERRADO | v6:54 y v6:61: la trazabilidad (revisor, `evidence_file`, fecha, R3/R4, R5, R5b) se aplica también a FAIL, sin exigir R1/R2/R4b. N39 (v6:95). N22 sigue siendo coherente: un error no es un PASS. |
| G1-11 | CERRADO | v6:83: solo informes originales desde el ciclo 5, con su hash. Para los ciclos 1–4, una nota de autoría del Orchestrator que remite a la sesión y que no puede usarse como `evidence_file`. |
| G1-12 | PARCIAL (ver G1-19 y G1-20) | v6:84 define la secuencia y precisa que el registro se crea después, pero no referencia ningún artefacto de la autorización del Owner, y el orden de los pasos 4→5 deja contenido sin revisar. |
| G1-13 | CERRADO (queda la reserva G1-21) | v6:94 (P7): proyecto temporal con los `FILES` de CORE y la carpeta APP-001 completa. Es coherente con `quality_cli.py:11-16,49-50,93` y con el `validate` del piloto, que devuelve 0. |
| G1-14 | CERRADO | v6:62 y v6:100: «reglas actuales + R0.b/R0.c» y un v1 anómalo pasa a INVALID. APP-001 (`mission.json`) y EXAMPLE-001 cumplen R0.b/R0.c (`created_at`, tipos y `reviewer_id` str/null). |
| G1-15 | CERRADO | v6:75 establece el aviso literal y N41 (v6:95) lo comprueba. |
| G1-16 | CERRADO (con una observación editorial, G1-22) | v6:55 («revisor sin verificación registrada»), v6:85 (`identity_verification_record_required`, informativo) y N42. |
| G1-17 | CERRADO | v6:61 R5b(c): subconjunto no vacío del rol pertinente; R2 sigue usando la unión. N40. La CLI no puede comprobar que el subconjunto sea completo, así que eso queda a cargo de Quality (riesgo residual aceptable). |

No reabro G1-01..G1-07; no hay evidencia nueva. No encontré regresiones funcionales v5→v6: todas las líneas modificadas son las de [v6] más la referencia R0 «R1–R8». Hay una incoherencia editorial (G1-22).

## Hallazgos nuevos
| ID | Gravedad | Evidencia | Problema | Corrección mínima |
|---|---|---|---|---|
| G1-20 | **MEDIUM (bloqueante)** | v6:84 pasos «4) Gate 2/3 Quality … 5) Crear registro GOV-001 y commits»; v6:83 «creado tras la implementación»; `docs/QUALITY_POLICY.md:36` («Reabrir Gate 2 si cambia código tras revisión»); AGENTS.md «Una aprobación no se transfiere automáticamente a versiones posteriores»; `quality_cli.py:101-109` (`validate` recorre todas las carpetas de `docs/MISSIONS`) | **Contenido sin revisar después de los Gates (falso PASS).** El registro GOV-001 incluye un `mission.json` v2 que `validate`/CI consumen, junto con propuestas y una nota. Se crearía y se comitearía después de Gate 2/3. El diff comiteado no sería el diff revisado, y la ejecución de `validate` en Gate 3 no incluiría ese manifiesto. Esto reproduce el tipo de defecto que GOV-001 quiere eliminar. | Crear el registro (mission.json v2 con Gates PENDING, propuestas, nota de ciclos 1–4) **antes** de Gate 2, para que entre en el diff y en el `validate` de Gate 3. Después de los Gates solo se permitirá añadir informes y rellenar los campos `gates`/`owner_acceptance`, y habrá que volver a ejecutar `validate` y registrar el comando, el exit y el hash como evidencia. Cualquier otro cambio reabre Gate 2. |
| G1-19 | LOW | v6:84 paso 2 («autorización expresa del Owner de 2026-11-05 (decisión humana documentada…)»), sin ruta ni hash; v6:84 paso 5 «commits»; AGENTS.md:36 y §4 («No usar Git de escritura … sin autorización aplicable»); precedente en el piloto: `docs/MISSIONS/APP-001/OWNER-IMPLEMENTATION-AUTHORIZATION.md`; v6:64 «no se admiten excepciones» | La autorización del Owner que sustituye a `can-implement` y la autorización de commit no tienen un artefacto verificable. La única constancia es el §9, redactado por el Architect. Además, el ámbito de «no se admiten excepciones» (R7, QUALITY_POLICY) no excluye expresamente esta autorización de nivel 1 para GOV-001, lo que genera ambigüedad. | Antes de implementar, referenciar un registro de la decisión del Owner (archivo `OWNER-AUTHORIZATION` o id de evento de la sesión, con su hash) que incluya expresamente si autoriza commits. Incluirlo en el registro GOV-001. Precisar que la regla de C2 limita los waivers sobre PWR/Gates y que esta autorización es una decisión del Owner sobre la ausencia de verificación registrada, no un waiver ni un PASS. |
| G1-18 | LOW | v6:65 (R8 excluye developer ∪ architect, no orchestrator); v6:82 (Orchestrator «nunca … aprueba … su propio trabajo», que incluye el registro de identidades y evidencias); R0.b v6:50 (`approved_by` es un str declarado, no un IDENT) | Un Orchestrator que no es Developer puede registrar `owner_acceptance` APPROVED con su propio id, aunque su trabajo (el registro y las verificaciones) forma parte de lo que se acepta. Además, R8 solo compara cadenas declaradas: un alias lo elude, y §8 no lo menciona para `approved_by`. | Añadir `roles.orchestrator` al conjunto excluido por R8 (y a N38), o justificar la exclusión de forma explícita. En §8, indicar que `approved_by` está solo declarado y que R8 es un control de coherencia, no una prueba. |
| G1-21 | LOW | v6:94 (P7 usa la carpeta APP-001 «del piloto»); v6:87 «unittest, sin red»; v6:45 «Universal: sin … Appointments» | P7 en `tests/` de CORE dependería de una ruta externa (protheus-efd), que no es hermética. Copiar APP-001 como fixture introduciría contenido de dominio de Appointments en CORE. | Ejecutar P7 como verificación manual documentada en Gate 3 (comando, exit y hash), o como test con `skipUnless(ruta)` que se declare NOT_RUN cuando falte la ruta. No copiar datos de dominio a CORE. |
| G1-22 | LOW (editorial) | v6:76 «`quality_cli.py` \| R0–R7» frente a R8 (v6:65); mensaje R1b v6:56 «revisor verificado por el autor revisado» | §5 omite R8. El mensaje de R1b afirma una verificación y contradice el vocabulario C1 que N42 pretende proteger: N42 solo busca «verificada». | Escribir «R0–R8». Cambiar el mensaje a «verificación registrada del revisor hecha por el autor revisado» y ampliar N42 a «verificad[oa]». |

## Estado D1–D4 / C1–C3
- **D1** se cumple (R6, N11, P7). **D2** se cumple (v6:75, N36/N41). **D3** se cumple (v6:82).
- **D4** se cumple en revisión y aprobación (R1b, R2, R8), con la reserva G1-18.
- **C1** se cumple, con la reserva editorial G1-22.
- **C2** se cumple en la CLI y en la política, con la ambigüedad de alcance G1-19.
- **C3** se cumple en el modelo (R5b para PASS/PWR/FAIL). En la secuencia no se cumple: el registro posterior a los Gates no queda revisado (G1-20).

## Qué NO verifiqué
- No hay implementación de v6, así que todas las pruebas P/N son NOT_RUN. E2E NO EJECUTADO (no aplica a Gate 1).
- No verifiqué mi identidad, la de copilot-sdk-main ni la autenticidad de la decisión del Owner; usé el resumen que recibí en la instrucción.
- No calculé el hash de `GOV-001-PROPOSAL.md` ni revisé v1–v4.
- No revisé `docs/ROLE_MATRIX.md`, `QUALITY_EVIDENCE_PROTOCOL.md`, `docs/templates/*`, `tests/test_governance.py` (solo comprobé que existe y que pasa), ARCHITECTURE, CHARTER ni RISK_MATRIX.
- Del piloto solo revisé el listado de APP-001 y `mission.json`, sin leer los informes.

## Limitación de independencia
Soy un subagente lanzado por el mismo runtime que el autor (copilot-sdk-main), posiblemente con la misma familia de modelo. La separación es solo de contexto. Según las propias reglas de v6 (R1, R4b), este informe no podría habilitar un Gate v2 sin que un tercero (por ejemplo, el Owner) registre la verificación de las identidades. Como el dictamen es FAIL, no habilita nada.
