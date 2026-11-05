# GOV-001 · Propuesta — Integridad de identidad y autoría (PROTHEUSAI v1.1)

**Estado:** DRAFT v4 — corrige ciclos 1–3 (v1 `293E4A64…FF68`, v2 `28F54A37…7D7B`, v3 `F4EF7796…A52A`; último: G1-07); PENDING Quality y Owner
**Autor (Architect, declarado):** agente Copilot SDK, sesión principal
**Repo:** PROTHEUSAI-CORE · baseline `29d741e` · árbol limpio
**Riesgo propuesto:** HIGH (afecta controles de independencia)

## 1. Evidencia del defecto
| Ref | Hecho verificado |
|---|---|
| `scripts/new_mission.py:18,34-35` | Un único `--author`; se copia en `author` **y** `implementation_author`. |
| `scripts/quality_cli.py:63` | Autoaprobación: Gate 1 compara con `author`; Gates 2/3 con `implementation_author`. Solo un string, `casefold`. |
| `scripts/quality_cli.py:62-77` | Solo `decision=='PASS'` se valida; `PASS_WITH_RESERVATIONS` cae en `else` sin control de revisor, evidencia ni autoaprobación. |
| `scripts/quality_cli.py:24-35` | `has_evidence` no comprueba que el informe identifique al mismo revisor que `mission.json`. |
| `docs/MISSIONS/README.md` | Documenta `--author "dev-01"`: ambigüedad Orchestrator/Developer. |
| `AGENTS.md:25`, `docs/ROLE_MATRIX.md` | Orchestrator existe en AGENTS.md pero no en Roles §2, matriz RACI ni `agents/`. |
| Piloto `protheus-efd` APP-001 `mission.json` | `author`=`implementation_author`=`LUNA` (Orchestrator); plan: Architect `/root/architect`; Developer distinto. `EXPERIMENT-LOG.md:10` ya advertía que era "valor inicial automático". |

## 2. Causa raíz
1. **Modelo de datos**: el manifiesto no tiene roles; colapsa Orchestrator, Architect y Developer en `author`, y la herramienta inventa `implementation_author` por defecto (dato fabricado, viola AGENTS §1).
2. **Control derivado erróneo**: la independencia se evalúa contra ese dato fabricado, no contra el autor real; un Developer real revisando su Gate 2 pasaría el control.
3. **Sin nivel de verificación**: un identificador declarado y uno acreditado por el entorno son indistinguibles.
4. Contribuyentes: hueco `PASS_WITH_RESERVATIONS`; sin cruce informe↔manifiesto; rol Orchestrator no contractualizado.

## 3. Modelo mínimo (schema_version 2)
```json
"roles": {
  "orchestrator": [IDENT],
  "architect":    [IDENT],
  "developer":    []
},
"gates": { "gate1": { "decision": "PENDING", "reviewer": null, "reviewed_artifact": null, "evidence_file": null, "date": null } }
```
`IDENT` = `{"id": str, "verification": "DECLARED"|"VERIFIED", "method": str|null, "ref": str|null}`
- `id`: identificador opaco (agente, handle de runtime, usuario). Comparación canónica: NFKC + strip + casefold.
- `DECLARED`: autodeclarado; vale para registrar autoría, **no** para emitir Gate.
- `VERIFIED`: requiere `method` (p. ej. `spawn-handle`, `signed-commit`, `platform-account`, `human-signature`) y `ref` reproducible (sha, ruta de log en la misión, id de ejecución). La CLI **nunca** eleva DECLARED→VERIFIED ni certifica la veracidad; solo exige presencia y coherencia (alineado con `QUALITY_EVIDENCE_PROTOCOL.md` "Manipulación de registros").
- Listas por rol: soporta varios Developers/ciclos sin nuevo esquema.
- Developer vacío al crear la misión: **ningún valor por defecto**.
- Quality: identidad por Gate (`gates.*.reviewer`, mismo `IDENT`).
- Universal: sin campos de dominio ni de Appointments.

## 4. Reglas de bloqueo (en `mission_errors`)
R0 (G1-03, G1-05) **Validación estructural previa por versión**, sin excepciones no controladas. Si R0 falla no se evalúan R1–R6, el manifiesto es inválido (`can-*` = 1) y `status` imprime "INVALID" + errores sin lanzar excepción.
- R0.a Despacho: `schema_version` debe ser `int` (no bool) ∈ {1,2}; otro valor/tipo → error y fin.
- R0.b Común (v1 y v2): `id`, `title`, `risk`, `created_at` str; `gates` objeto con exactamente `gate1..gate3`, cada uno objeto; `decision` str ∈ DECISIONS; `reviewed_artifact`, `evidence_file`, `date` str o null; `owner_acceptance` objeto con `status` str ∈ {PENDING, APPROVED, REJECTED}, `approved_by`/`date` str o null.
- R0.c Solo v1: `author`, `implementation_author` str no vacíos; por Gate `reviewer_id` str o null. Sin exigir `roles`/`reviewer`. Después se aplica R6.
- R0.d Solo v2: sin `author`/`implementation_author`/`reviewer_id` (presentes → error, evita esquemas mixtos); `roles` objeto con exactamente `orchestrator`, `architect`, `developer`, cada uno lista; `orchestrator` no vacío; cada IDENT objeto con exactamente `id`, `verification`, `method`, `ref`; `id` str de canónico no vacío; `verification` ∈ {DECLARED, VERIFIED}; si VERIFIED `method`/`ref` str no vacíos, si DECLARED pueden ser null; IDs canónicos duplicados en un rol → error; por Gate `reviewer` null o IDENT válido.
- Implementación: una función `structure_errors(m)` pura, llamada al principio de `mission_errors`; `status` usa la misma función y `.get` defensivo.
Aplican a decisiones PASS **y** PASS_WITH_RESERVATIONS:
R1 `reviewer` VERIFIED con `method`+`ref` → si no, "identidad de revisor no verificable".
R2 Revisor ∉ {orchestrator ∪ architect ∪ developer} (canónico) → "autoaprobación/independencia".
R3 Gate 2/3 con `developer` vacío → "autor del diff desconocido: independencia no evaluable". R4 Gate 1 con `architect` vacío → idem.
R4b (G1-02) Las identidades **pertinentes** contra las que se evalúa independencia deben ser también VERIFIED con `method`+`ref`: Gate 1 → architect y orchestrator; Gate 2/3 → developer, architect y orchestrator. Una identidad DECLARED en esos roles bloquea el Gate. El informe debe contener **exactamente una** línea `**Independencia verificada:** sí — <evidencia>` (G1-07): valor afirmativo (`sí`/`si`, canónico) seguido de evidencia no vacía y distinta del marcador de plantilla; negativa, vacía, marcador o duplicada → "independencia no acreditada en el informe". La CLI comprueba **presencia/coherencia**; Quality verifica externamente que los `ref` vinculan a cada autor con su artefacto y lo separan del revisor. No se presenta como autenticación.
R5 (G1-01) `evidence_file` debe contener **exactamente una** línea `**Revisor:** <id>` y **exactamente una** línea `**Dictamen:** <valor>`; `<id>` canónico = `reviewer.id` y `<valor>` = `decision` del manifiesto. Etiquetas ausentes, duplicadas o contradictorias → "inconsistencia informe/manifiesto". (Exige plantillas con etiquetas uniformes, §5.)
R6 schema v1 (tras R0.b+R0.c): válido solo si todos los Gates ∈ {PENDING, FAIL} y owner ≠ APPROVED; si no → "migrar a v2". R1–R5 solo se aplican a v2.
R7 Se mantienen: orden de Gates (Gate N exige PASS **exacto** en N-1), evidencia no-plantilla, ruta dentro de la misión, owner APPROVED solo con tres PASS.
`can-implement`/`can-close` heredan el bloqueo (ya dependen de `mission_errors` y de PASS exacto).

**Reapertura (G1-04):** procedimental — al reabrir Gate N, el Orchestrator pone N y posteriores en PENDING y conserva informes previos; Quality comprueba que `reviewed_artifact` corresponde a la versión vigente. Comprobado por la CLI: ningún Gate posterior puede estar en PASS/PWR si uno anterior no está en PASS (ya existe), y owner APPROVED exige tres PASS. No comprobado por la CLI: que el hash revisado sea el actual.

No se impide que Architect sea Developer (la política no lo prohíbe); sí que cualquiera de ellos u Orchestrator revise.

## 5. Cambios mínimos (sin frameworks; stdlib `unicodedata`)
| Archivo | Cambio |
|---|---|
| `scripts/new_mission.py` | `--orchestrator` (obligatorio), `--architect` (opcional), `--verification` por defecto DECLARED; `--author` alias deprecado → orchestrator con aviso; elimina `implementation_author`; v2. |
| `scripts/quality_cli.py` | R1–R6; normalización; `status` muestra roles y nivel. |
| `tests/test_governance.py` | Migrar **todas** las fixtures a v2 (helper que crea misión con architect/developer VERIFIED e informe coherente; elimina `reviewer_id`) y añadir §6. |
| `docs/MISSIONS/EXAMPLE-001/mission.json` | Migrar a v2 (gates PENDING). |
| `docs/templates/*` | MISSION_PLAN: `**Architect:**`/`**Orchestrator:**`; IMPLEMENTATION_REPORT: `**Developer:**`; GATE1/GATE2/GATE3: cabecera uniforme con una sola línea de cada: `**Dictamen:**`, `**Revisor:**`, `**Verificación de identidad:** [método + ref]`, `**Independencia verificada:** [sí/no + evidencia]` (G1-06: GATE2 sustituye `No autor del diff`, GATE3 sustituye `Responsable QA`). |
| `docs/MISSIONS/README.md`, `QUALITY_EVIDENCE_PROTOCOL.md` | Uso nuevo; DECLARED vs VERIFIED. |
| `AGENTS.md §2`, `docs/ROLE_MATRIX.md` | Añadir Orchestrator: coordina y registra identidades; no es autor por defecto ni revisor. **Requiere aprobación Owner (fuente de nivel 3).** |
| `quality/controls.json` | `"identity_verification_required": true` (informativo). |

## 6. Pruebas previstas (unittest, sin red)
Positivas: P1 nueva misión v2 válida, developer vacío, Gates PENDING · P2 cadena completa con identidades VERIFIED distintas e informes coherentes → `can-implement`/`can-close` 0 · P3 v1 todo PENDING sigue válido · P4 alias `--author` → orchestrator, nunca developer.
Negativas: N1 regresión causa raíz: developer ≠ orchestrator por defecto · N2 Gate2 PASS sin developer → bloqueo · N3 revisor = architect (Gate1) · N4 revisor = developer (Gate2/3) · N5 revisor = orchestrator · N6 revisor DECLARED · N7 VERIFIED sin method/ref · N8 **suplantación**: manifiesto `quality-2`, informe `**Revisor:** developer-1` · N9 evasión por normalización (`" Developer-1"`, mayúsculas, ancho completo NFKC) · N10 PASS_WITH_RESERVATIONS por developer · N11 v1 con PASS → migrar · N12 revisor = segundo developer de la lista · N13 informe sin etiqueta `**Revisor:**`.
Añadidas en v2: N14 informe `**Dictamen:** FAIL` con manifiesto PASS · N15 informe PWR con manifiesto PASS · N16 etiquetas `Revisor`/`Dictamen` duplicadas o contradictorias · N17 developer DECLARED con Gate 2 PASS (G1-02) · N18 architect DECLARED con Gate 1 PASS · N19 informe sin `**Independencia verificada:**` real · N20 R0: `id` vacío/espacios, rol con `[{"id":""}]`, tipos incorrectos, `verification` desconocida, `schema_version` 3, clave de rol desconocida, IDs duplicados — todos error controlado, nunca excepción · N21 Gate 1 PWR válido: registro consistente pero `can-implement` = 1 y Gate 2 PASS → "Gate anterior no tiene PASS" · N22 FAIL/PENDING con revisor ausente no producen falso PASS · N23 owner APPROVED sin tres PASS · N24 reapertura: Gate 1 PENDING con Gate 2/3 PASS → error.
Añadidas en v3: N25 R0.b estructura común inválida — `gates` lista, Gate no objeto, Gate ausente/extra, `decision: []`/`null`/valor desconocido, `owner_acceptance` no objeto o `status` no str — error controlado en `mission_errors`, `validate`, `status`, `can-implement`, `can-close` (exit ≠ 0, sin traceback) · N26 `schema_version` `true`/`"2"`/3 · N27 manifiesto mixto v2 con `implementation_author` o `reviewer_id` · N28 v2 sin `orchestrator` · P5 (G1-05) v1 PENDING (EXAMPLE-001 actual) valida sin exigir `roles` · P6 (G1-06) informes generados rellenando cada plantilla GATE1/2/3 con datos válidos superan R4b/R5.
Añadidas en v4: N29 (G1-07) `**Independencia verificada:** no; …` con PASS y con PWR → error · N30 `sí` sin evidencia, solo marcador, o línea duplicada → error.

## 7. Compatibilidad
- Plantilla: EXAMPLE-001 migra sin pérdida (todo PENDING). Tests actuales: los 4 se conservan en intención; 3 requieren migrar fixtures (`reviewer_id`→`reviewer` IDENT, roles, informe con etiquetas). No se elimina ninguna aserción existente.
- Plantillas GATE1/2/3: R5 exige una sola línea `**Revisor:**` y una sola `**Dictamen:**`; GATE2 (`Revisor independiente`, `## Dictamen`) y GATE3 (`Responsable QA`) se uniforman. Las secciones narrativas finales `[PENDING / FAIL / …]` se renombran para no duplicar la etiqueta.
- Proyectos derivados v1 con PASS (p. ej. APP-001) fallarán `validate` al adoptar v1.1: **intencional**; migración manual registrando identidades reales con evidencia, nunca inferidas. No se migra APP-001 aquí.
- Informes antiguos de Gate 2/3 usan `Revisor independiente`/`Responsable QA`: R5 solo se aplica a v2.

## 8. Riesgos residuales
- Alias distintos de la misma entidad (`dev-1` vs `/root/developer`) no detectables por string: mitigado por R1 (método+ref), no eliminado.
- El Orchestrator registra `VERIFIED`; podría registrar falsamente. Mitigación: `ref` reproducible y auditable por Quality; endurecer con commits firmados en versión futura (fuera de alcance).
- La CLI valida forma, no veracidad (sin cambios respecto a la política vigente).

## 9. Decisiones Owner pendientes
D1 Aprobar esquema v2 y bloqueo de v1 con PASS. D2 ¿Mantener alias `--author` (recomendado, deprecado) o eliminarlo? D3 Aprobar modificación de `AGENTS.md`/`ROLE_MATRIX.md` para el rol Orchestrator. D4 ¿Prohibir Orchestrator=Developer? (recomendación: permitir, pero entonces nunca revisor).
