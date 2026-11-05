# GOV-001 · Propuesta — Integridad de identidad y autoría (PROTHEUSAI v1.1)

**Estado:** DRAFT — PENDING Quality review y aprobación Owner
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

## 4. Reglas de bloqueo (en `mission_errors`, aplican a PASS **y** PASS_WITH_RESERVATIONS)
R1 `reviewer` presente y `verification=VERIFIED` con `method`+`ref`; si no → "identidad de revisor no verificable".
R2 Revisor ∉ {orchestrator ∪ architect ∪ developer} (canónico) → "autoaprobación/independencia".
R3 Gate 2/3 con `developer` vacío → "autor del diff desconocido: independencia no evaluable".
R4 Gate 1 con `architect` vacío → idem.
R5 `evidence_file` debe contener `**Revisor:** <id>` igual (canónico) a `reviewer.id` → si no, "inconsistencia informe/manifiesto".
R6 schema v1: válido solo si ningún Gate ≠ PENDING/FAIL; si hay PASS/PASS_WITH_RESERVATIONS → "migrar a v2".
R7 Los Gates/orden/evidencia existentes se mantienen.
`can-implement`/`can-close` heredan el bloqueo (ya dependen de `mission_errors`).

No se impide que Architect sea Developer (la política no lo prohíbe); sí que cualquiera de ellos u Orchestrator revise.

## 5. Cambios mínimos (sin frameworks; stdlib `unicodedata`)
| Archivo | Cambio |
|---|---|
| `scripts/new_mission.py` | `--orchestrator` (obligatorio), `--architect` (opcional), `--verification` por defecto DECLARED; `--author` alias deprecado → orchestrator con aviso; elimina `implementation_author`; v2. |
| `scripts/quality_cli.py` | R1–R6; normalización; `status` muestra roles y nivel. |
| `tests/test_governance.py` | Ajustar test existente (informe con `**Revisor:**`) y añadir §6. |
| `docs/MISSIONS/EXAMPLE-001/mission.json` | Migrar a v2 (gates PENDING). |
| `docs/templates/*` | MISSION_PLAN: `**Architect:**`/`**Orchestrator:**`; IMPLEMENTATION_REPORT: `**Developer:**`; GATE2/GATE3: etiqueta uniforme `**Revisor:**` + `**Verificación de identidad:** [método + ref]` (GATE1 añade esta línea). |
| `docs/MISSIONS/README.md`, `QUALITY_EVIDENCE_PROTOCOL.md` | Uso nuevo; DECLARED vs VERIFIED. |
| `AGENTS.md §2`, `docs/ROLE_MATRIX.md` | Añadir Orchestrator: coordina y registra identidades; no es autor por defecto ni revisor. **Requiere aprobación Owner (fuente de nivel 3).** |
| `quality/controls.json` | `"identity_verification_required": true` (informativo). |

## 6. Pruebas previstas (unittest, sin red)
Positivas: P1 nueva misión v2 válida, developer vacío, Gates PENDING · P2 cadena completa con identidades VERIFIED distintas e informes coherentes → `can-implement`/`can-close` 0 · P3 v1 todo PENDING sigue válido · P4 alias `--author` → orchestrator, nunca developer.
Negativas: N1 regresión causa raíz: developer ≠ orchestrator por defecto · N2 Gate2 PASS sin developer → bloqueo · N3 revisor = architect (Gate1) · N4 revisor = developer (Gate2/3) · N5 revisor = orchestrator · N6 revisor DECLARED · N7 VERIFIED sin method/ref · N8 **suplantación**: manifiesto `quality-2`, informe `**Revisor:** developer-1` · N9 evasión por normalización (`" Developer-1"`, mayúsculas, ancho completo NFKC) · N10 PASS_WITH_RESERVATIONS por developer · N11 v1 con PASS → migrar · N12 revisor = segundo developer de la lista · N13 informe sin etiqueta `**Revisor:**`.

## 7. Compatibilidad
- Plantilla: EXAMPLE-001 migra sin pérdida (todo PENDING). Tests actuales: 1 requiere ajuste del texto de informe (N13 lo justifica).
- Proyectos derivados v1 con PASS (p. ej. APP-001) fallarán `validate` al adoptar v1.1: **intencional**; migración manual registrando identidades reales con evidencia, nunca inferidas. No se migra APP-001 aquí.
- Informes antiguos de Gate 2/3 usan `Revisor independiente`/`Responsable QA`: R5 solo se aplica a v2.

## 8. Riesgos residuales
- Alias distintos de la misma entidad (`dev-1` vs `/root/developer`) no detectables por string: mitigado por R1 (método+ref), no eliminado.
- El Orchestrator registra `VERIFIED`; podría registrar falsamente. Mitigación: `ref` reproducible y auditable por Quality; endurecer con commits firmados en versión futura (fuera de alcance).
- La CLI valida forma, no veracidad (sin cambios respecto a la política vigente).

## 9. Decisiones Owner pendientes
D1 Aprobar esquema v2 y bloqueo de v1 con PASS. D2 ¿Mantener alias `--author` (recomendado, deprecado) o eliminarlo? D3 Aprobar modificación de `AGENTS.md`/`ROLE_MATRIX.md` para el rol Orchestrator. D4 ¿Prohibir Orchestrator=Developer? (recomendación: permitir, pero entonces nunca revisor).
