# GOV-001 · Propuesta — Integridad de identidad y autoría (PROTHEUSAI v1.1)

**Estado:** DRAFT v5 — incorpora decisión Owner (D1–D4, C1–C3) sobre v4 `09D2451F…CF10` (Quality PASS ciclo 4). Cambios materiales marcados **[v5]**; PENDING Quality ciclo 5.
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
**[v5, C1]** `IDENT` = `{"id": str, "evidence": EVID|null, "verification": VERIF|null}`
`EVID` = `{"method": str, "ref": str}` · `VERIF` = `{"by": str, "method": str, "ref": str, "date": str}`
- `id`: identificador **declarado**, opaco (agente, handle de runtime, usuario). Comparación canónica: NFKC + strip + casefold.
- Tres niveles distintos, derivados de los campos (no hay campo de nivel editable):
  1. **Declarada** — solo `id`. Registra autoría; no habilita Gates.
  2. **Con evidencia** — `evidence` presente: método (`spawn-handle`, `signed-commit`, `platform-account`, `human-signature`…) y `ref` reproducible. Aún no verificada.
  3. **Verificación registrada** — `verification` presente (exige `evidence`): quién (`by`) comprobó efectivamente la evidencia, cómo, referencia y fecha. `by` canónico ≠ `id` (sin autoverificación).
- La CLI **nunca** afirma haber comprobado identidades externas: comprueba presencia y coherencia de registros declarados. `status`/`validate` lo expresan literalmente ("verificación registrada por X; no comprobada por la CLI"). Alineado con `QUALITY_EVIDENCE_PROTOCOL.md` "Manipulación de registros".
- Listas por rol: soporta varios Developers/ciclos sin nuevo esquema.
- Developer vacío al crear la misión: **ningún valor por defecto**.
- Quality: identidad por Gate (`gates.*.reviewer`, mismo `IDENT`).
- Universal: sin campos de dominio ni de Appointments.

## 4. Reglas de bloqueo (en `mission_errors`)
R0 (G1-03, G1-05) **Validación estructural previa por versión**, sin excepciones no controladas. Si R0 falla no se evalúan R1–R6, el manifiesto es inválido (`can-*` = 1) y `status` imprime "INVALID" + errores sin lanzar excepción.
- R0.a Despacho: `schema_version` debe ser `int` (no bool) ∈ {1,2}; otro valor/tipo → error y fin.
- R0.b Común (v1 y v2): `id`, `title`, `risk`, `created_at` str; `gates` objeto con exactamente `gate1..gate3`, cada uno objeto; `decision` str ∈ DECISIONS; `reviewed_artifact`, `evidence_file`, `date` str o null; `owner_acceptance` objeto con `status` str ∈ {PENDING, APPROVED, REJECTED}, `approved_by`/`date` str o null.
- R0.c Solo v1: `author`, `implementation_author` str no vacíos; por Gate `reviewer_id` str o null. Sin exigir `roles`/`reviewer`. Después se aplica R6.
- R0.d Solo v2: sin `author`/`implementation_author`/`reviewer_id` (presentes → error, evita esquemas mixtos); `roles` objeto con exactamente `orchestrator`, `architect`, `developer`, cada uno lista; `orchestrator` no vacío; cada IDENT objeto con exactamente `id`, `evidence`, `verification`; `id` str de canónico no vacío; `evidence` null u objeto con exactamente `method`, `ref` str no vacíos; `verification` null u objeto con exactamente `by`, `method`, `ref`, `date` str no vacíos; `verification` sin `evidence` → error; `verification.by` canónico = `id` → "autoverificación"; IDs canónicos duplicados en un rol → error; por Gate `reviewer` null o IDENT válido.
- Implementación: una función `structure_errors(m)` pura, llamada al principio de `mission_errors`; `status` usa la misma función y `.get` defensivo.
Aplican a decisiones PASS **y** PASS_WITH_RESERVATIONS:
R1 `reviewer` con verificación registrada → si no, "identidad de revisor no verificada".
R1b **[v5, D4]** `reviewer.verification.by` ∉ autores pertinentes del artefacto revisado (Gate 1: architect; Gate 2/3: developer) → "revisor verificado por el autor revisado". Si el Orchestrator figura también como Developer, la identidad del revisor de Gates 2/3 debe verificarla otra persona (p. ej. Owner).
R2 Revisor ∉ {orchestrator ∪ architect ∪ developer} (canónico) → "autoaprobación/independencia".
R3 Gate 2/3 con `developer` vacío → "autor del diff desconocido: independencia no evaluable". R4 Gate 1 con `architect` vacío → idem.
R4b (G1-02) Las identidades **pertinentes** contra las que se evalúa independencia deben tener también verificación registrada: Gate 1 → architect y orchestrator; Gate 2/3 → developer, architect y orchestrator. Una identidad solo declarada o solo con evidencia en esos roles bloquea el Gate. El informe debe contener **exactamente una** línea `**Independencia verificada:** sí — <evidencia>` (G1-07): valor afirmativo (`sí`/`si`, canónico) seguido de evidencia no vacía y distinta del marcador de plantilla; negativa, vacía, marcador o duplicada → "independencia no acreditada en el informe". La CLI comprueba **presencia/coherencia**; Quality verifica externamente que los `ref` vinculan a cada autor con su artefacto y lo separan del revisor. No se presenta como autenticación.
R5 (G1-01) `evidence_file` debe contener **exactamente una** línea `**Revisor:** <id>` y **exactamente una** línea `**Dictamen:** <valor>`; `<id>` canónico = `reviewer.id` y `<valor>` = `decision` del manifiesto. Etiquetas ausentes, duplicadas o contradictorias → "inconsistencia informe/manifiesto". (Exige plantillas con etiquetas uniformes, §5.)
R5b **[v5, C3]** Trazabilidad de cada revisión PASS/PWR: (a) `reviewed_artifact` contiene ruta/nombre y al menos un identificador de versión `sha256:<64 hex>` o `git:<7–40 hex>` (rango `git:<a>..<b>` admitido); (b) el informe contiene exactamente una línea `**Artefacto revisado:**` cuyo valor, con espacios normalizados, es igual a `reviewed_artifact`; (c) exactamente una línea `**Autor efectivo:**` con IDs separados por comas cuyo conjunto canónico es igual al de los autores pertinentes (Gate 1: architect; Gate 2/3: developer); (d) revisor (R5) y `evidence_file` ya exigidos. Discrepancia → "trazabilidad incompleta".
R6 **[v5, D1]** schema v1 = **histórico**. `validate` aplica las comprobaciones v1 vigentes sin cambios (R0.b+R0.c + reglas actuales) y, si pasa, informa `AVISO: <id> v1 histórico; no habilita autorizaciones` con exit 0; sus dictámenes no se modifican. `can-implement`/`can-close` sobre v1 → siempre `BLOCKED: manifiesto v1; migrar o revalidar en v2` (exit 1). R1–R5b solo se aplican a v2.
**Migración/revalidación (procedimental, documentada en `docs/MISSIONS/README.md`):** renombrar `mission.json` v1 a `mission.v1.json` sin alterar bytes (registrar SHA-256 antes/después), crear `mission.json` v2 con identidades reales; cada Gate queda PENDING salvo revalidación por Quality bajo reglas v2 (informe nuevo con etiquetas v2; los informes históricos se conservan intactos). La CLI ignora `mission.v1.json`.
R7 **[v5, C2]** Se mantienen y amplían: Gate N con PASS **o PWR** exige PASS **exacto** en N-1 (hoy solo se exige para PASS); `can-implement` exige Gate 1 PASS exacto; `can-close` exige tres PASS y owner APPROVED; owner APPROVED exige tres PASS. PWR nunca equivale a PASS ni habilita transiciones. La CLI no implementa waivers: cualquier excepción sigue `AGENTS.md:36` (decisión humana documentada) fuera de la CLI y no se registra como PASS.
`can-implement`/`can-close` heredan el bloqueo (dependen de `mission_errors` y de PASS exacto).

**Reapertura (G1-04):** procedimental — al reabrir Gate N, el Orchestrator pone N y posteriores en PENDING y conserva informes previos; Quality comprueba que `reviewed_artifact` corresponde a la versión vigente. Comprobado por la CLI: ningún Gate posterior puede estar en PASS/PWR si uno anterior no está en PASS (ya existe), y owner APPROVED exige tres PASS. No comprobado por la CLI: que el hash revisado sea el actual.

No se impide que Architect sea Developer ni **[v5, D4]** que Orchestrator sea Developer si figura explícitamente en `roles.developer`; R2 y R1b impiden que revise, apruebe o verifique la identidad de quien revisa su trabajo.

## 5. Cambios mínimos (sin frameworks; stdlib `unicodedata`)
| Archivo | Cambio |
|---|---|
| `scripts/new_mission.py` | `--orchestrator` (obligatorio salvo alias) y `--architect` (opcional) crean IDENT **solo declaradas** (`evidence`/`verification` null; se completan editando el manifiesto con evidencia real); **[v5, D2]** `--author` alias obsoleto → únicamente `roles.orchestrator` (autoría inicial = creación de la misión), aviso `DEPRECATED` a stderr; `--author` + `--orchestrator` → error; nunca rellena `developer` ni `implementation_author`; v2. |
| `scripts/quality_cli.py` | R0–R7; normalización; `status` muestra roles y nivel con redacción C1; aviso v1 histórico. |
| `tests/test_governance.py` | Migrar **todas** las fixtures a v2 (helper que crea misión con identidades con verificación registrada e informe coherente; elimina `reviewer_id`) y añadir §6. |
| `docs/MISSIONS/EXAMPLE-001/mission.json` | Migrar a v2 (gates PENDING; es plantilla de ejemplo, no histórico real). |
| `docs/templates/*` | MISSION_PLAN: `**Architect:**`/`**Orchestrator:**`; IMPLEMENTATION_REPORT: `**Developer (autor efectivo):**`; GATE1/GATE2/GATE3: cabecera uniforme con una sola línea de cada: `**Dictamen:**`, `**Revisor:**`, `**Verificación de identidad:**`, `**Independencia verificada:**`, **[v5, C3]** `**Artefacto revisado:**`, `**Autor efectivo:**` (GATE1 sustituye `Plan exacto`; GATE2 sustituye `Revisor independiente`, `No autor del diff`, `Diff exacto`; GATE3 sustituye `Responsable QA`, `Código/artefacto probado`). |
| `docs/MISSIONS/README.md`, `QUALITY_EVIDENCE_PROTOCOL.md` | Uso nuevo; tres niveles de identidad (C1); PWR no habilita (C2); trazabilidad (C3); procedimiento de migración v1 (D1). |
| `AGENTS.md §2`, `docs/ROLE_MATRIX.md` | **[v5, D3 autorizado]** Añadir Orchestrator: coordina y registra identidades y evidencias; no es autor por defecto; puede ser Developer si se registra (D4); nunca revisa, aprueba ni verifica la identidad del revisor de su propio trabajo. Cambio mínimo: una viñeta y una fila/columna. |
| **[v5]** `docs/MISSIONS/GOV-001/` | Registro de esta misión creado con la nueva CLI: plan v1–v5, informes Quality (ciclos 1–4 como transcripción literal declarada; siguientes escritos por Quality), informe de implementación, evidencias. Gates en `mission.json` quedan PENDING mientras no exista verificación efectiva de identidades por un tercero (Owner): autor y revisores son agentes del mismo runtime y la CLI lo bloquearía correctamente. |
| `quality/controls.json` | `"identity_verification_required": true` (informativo). |

## 6. Pruebas previstas (unittest, sin red)
Positivas: P1 nueva misión v2 válida, developer vacío, Gates PENDING · P2 cadena completa con identidades VERIFIED distintas e informes coherentes → `can-implement`/`can-close` 0 · P3 v1 todo PENDING sigue válido · P4 alias `--author` → orchestrator, nunca developer.
Negativas: N1 regresión causa raíz: developer ≠ orchestrator por defecto · N2 Gate2 PASS sin developer → bloqueo · N3 revisor = architect (Gate1) · N4 revisor = developer (Gate2/3) · N5 revisor = orchestrator · N6 revisor DECLARED · N7 VERIFIED sin method/ref · N8 **suplantación**: manifiesto `quality-2`, informe `**Revisor:** developer-1` · N9 evasión por normalización (`" Developer-1"`, mayúsculas, ancho completo NFKC) · N10 PASS_WITH_RESERVATIONS por developer · N11 v1 con PASS → migrar · N12 revisor = segundo developer de la lista · N13 informe sin etiqueta `**Revisor:**`.
Añadidas en v2: N14 informe `**Dictamen:** FAIL` con manifiesto PASS · N15 informe PWR con manifiesto PASS · N16 etiquetas `Revisor`/`Dictamen` duplicadas o contradictorias · N17 developer DECLARED con Gate 2 PASS (G1-02) · N18 architect DECLARED con Gate 1 PASS · N19 informe sin `**Independencia verificada:**` real · N20 R0: `id` vacío/espacios, rol con `[{"id":""}]`, tipos incorrectos, `verification` desconocida, `schema_version` 3, clave de rol desconocida, IDs duplicados — todos error controlado, nunca excepción · N21 Gate 1 PWR válido: registro consistente pero `can-implement` = 1 y Gate 2 PASS → "Gate anterior no tiene PASS" · N22 FAIL/PENDING con revisor ausente no producen falso PASS · N23 owner APPROVED sin tres PASS · N24 reapertura: Gate 1 PENDING con Gate 2/3 PASS → error.
Añadidas en v3: N25 R0.b estructura común inválida — `gates` lista, Gate no objeto, Gate ausente/extra, `decision: []`/`null`/valor desconocido, `owner_acceptance` no objeto o `status` no str — error controlado en `mission_errors`, `validate`, `status`, `can-implement`, `can-close` (exit ≠ 0, sin traceback) · N26 `schema_version` `true`/`"2"`/3 · N27 manifiesto mixto v2 con `implementation_author` o `reviewer_id` · N28 v2 sin `orchestrator` · P5 (G1-05) v1 PENDING (EXAMPLE-001 actual) valida sin exigir `roles` · P6 (G1-06) informes generados rellenando cada plantilla GATE1/2/3 con datos válidos superan R4b/R5.
Añadidas en v4: N29 (G1-07) `**Independencia verificada:** no; …` con PASS y con PWR → error · N30 `sí` sin evidencia, solo marcador, o línea duplicada → error.
**[v5]** Ajustes: en P1–N30 "VERIFIED" se lee "verificación registrada" y "DECLARED" "solo declarada"; N7 → `evidence`/`verification` con campo vacío o ausente · P3/P5 → v1 PENDING valida con AVISO, `can-implement` = 1 · N11 → v1 con PASS: `validate` 0 con AVISO, `can-implement`/`can-close` = 1, archivo byte-idéntico tras validar (D1) · N6/N17/N18 → identidad solo declarada y solo con evidencia, ambos bloquean (C1).
Nuevas: N31 `verification` sin `evidence` · N32 autoverificación (`by` = `id`, también tras normalización) · N33 (D4) Orchestrator también Developer: registro válido; revisor = orchestrator → error; revisor de Gate 2 verificado por ese Orchestrator-Developer → error; verificado por Owner → válido · N34 (C2) Gate 2 PWR con Gate 1 PWR → "Gate anterior no tiene PASS"; tres PWR + owner APPROVED → error; `can-close` = 1 · N35 (C3) `reviewed_artifact` sin `sha256:`/`git:`; hash de 63 hex; informe con artefacto distinto; `**Autor efectivo:**` ausente, duplicado, con autor distinto, incompleto o con autor extra → error · N36 (D2) `--author` emite DEPRECATED, rellena solo orchestrator; `--author` + `--orchestrator` → error · N37 (C1) salida de `status` no contiene "verificada por la CLI" y sí "no comprobada por la CLI" · P7 compatibilidad histórica: copia del `mission.json` de APP-001 (piloto, solo lectura) en carpeta temporal → `validate` 0 con AVISO, `can-close` 1, bytes intactos.

## 7. Compatibilidad
- Plantilla: EXAMPLE-001 migra sin pérdida (todo PENDING). Tests actuales: los 4 se conservan en intención; 3 requieren migrar fixtures (`reviewer_id`→`reviewer` IDENT, roles, informe con etiquetas). No se elimina ninguna aserción existente.
- Plantillas GATE1/2/3: R5 exige una sola línea `**Revisor:**` y una sola `**Dictamen:**`; GATE2 (`Revisor independiente`, `## Dictamen`) y GATE3 (`Responsable QA`) se uniforman. Las secciones narrativas finales `[PENDING / FAIL / …]` se renombran para no duplicar la etiqueta.
- **[v5, D1]** Proyectos derivados v1 con PASS (p. ej. APP-001): `validate` sigue en 0 con AVISO (CI no se rompe, dictámenes intactos), pero no obtienen nuevas autorizaciones (`can-*` = 1) hasta migrar/revalidar. No se migra APP-001 aquí.
- Informes antiguos de Gate 2/3 usan `Revisor independiente`/`Responsable QA`: R5 solo se aplica a v2.

## 8. Riesgos residuales
- Alias distintos de la misma entidad (`dev-1` vs `/root/developer`) no detectables por string: mitigado por R1 (método+ref), no eliminado.
- Quien registra `verification` podría hacerlo falsamente. Mitigación: `by`/`ref` explícitos y auditables por Quality, sin autoverificación ni verificación del revisor por el autor revisado; endurecer con commits firmados en versión futura (fuera de alcance).
- La CLI valida forma, no veracidad (sin cambios respecto a la política vigente).

## 9. Decisiones Owner (2026-11-05, aprobadas con condiciones)
D1 v2 aprobado; v1 con PASS no obtiene nuevas autorizaciones sin migración/revalidación; dictámenes históricos intactos → R6. D2 `--author` alias obsoleto con aviso, solo autoría inicial, nunca copiado a implementación → §5. D3 modificaciones mínimas de `AGENTS.md`/`ROLE_MATRIX.md` autorizadas → §5. D4 Orchestrator puede ser Developer si se registra; nunca revisa/aprueba su trabajo → R2, R1b. C1 tres niveles de identidad; la CLI no afirma verificación externa → §3, N37. C2 PWR no habilita transiciones; excepciones por política humana explícita → R7, N34. C3 artefacto+versión, autor efectivo, revisor y evidencias en cada revisión → R5b, N35.
Fuera de alcance (Owner): skills, frameworks multiagente, otras funciones v1.1.
