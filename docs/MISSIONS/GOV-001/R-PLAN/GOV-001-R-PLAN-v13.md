# GOV-001 · Revisión focalizada del plan v8 (v13) — decisión del Owner del 2026-11-05 09:53

**Estado:** DRAFT v13 — PENDING Quality y Owner.
- Corrige el PWR de Quality ciclo 12 (`GOV-R-REVIEW-12.md`, sha256_lf `847b70dd…e621`; GR-40 y OB-13..OB-17) sobre v12 (sha256_lf `5e59a4c9…e255`).
- Sustituye a v9–v12. Base: `GOV-001-R-PLAN-v8.md` (sha256_lf `0d6bcca0…2a93`).

**Autor (Architect, declarado):** copilot-sdk-main · **Repo:** PROTHEUSAI-CORE `6e5e929`, limpio.
**Decisión del Owner de 09:53:** solo consta en el mensaje de la sesión `e5be03ee…`. Se transcribirá literalmente en `OWNER-DECISION-02.md`, junto con la autorización.

## 0. Prelación sobre v8 (GR-26, GR-36)
**Regla:** v13 prevalece sobre v8 en lo que modifica; lo demás de v8 sigue vigente.

| Sección de v8 | Estado |
|---|---|
| Clasificación | R01 Bloqueo (aprobado); R03 Bloqueo (rediseñado en §1–§4); R02 Mejora futura (§6) |
| GOV-R01 completo, incluida su verificación con `GATE2-INPUT-04` y `POST-GATE-VALIDATION-R01.md` | **Conservada** sin cambios (APROBADO) |
| GOV-R03 · Principio, mitigación GR-19, O-2, O-3, último Gate (O-7) | **Conservada y adaptada** en §5 |
| GOV-R03 · Token `ACREDITADA`/`NO_ACREDITADA`, `independence`, `evidence_sha256_lf`, «sin cambio de schema» | **Obsoleta**; la sustituyen §1–§4 |
| GOV-R03 · Rutas canónicas (`fullmatch`, `os.listdir`, `resolve`+`is_relative_to`), definición de `sha256_lf`, subcomando `hash` | **Conservada** |
| GOV-R03 · Gates, entradas `GATE2-INPUT-05…` y comprobación tras el commit | **Conservada** (§5) |
| GOV-R02 | **Sustituida** por §6 |
| Cierre de GOV-001 (opciones A/B) | **Sustituida** por §7 |
| Secuencia de v8 | Se **conservan** los pasos 1–4. Los pasos 5–6 (opción A/B y GOV-002) quedan **sustituidos** por §7: migración a v3, Gate de revalidación y aprobación final del Owner. |
| Detención | **Conservada.** La autorización de R03 se redacta en §9 (D4) (OB-2). |
| Carácter de los Gates de R01/R03 | **Conservado**, cambiando «marcarán `NO_ACREDITADA`» por «se clasificarán según §1» |
| Decisiones del Owner | **Sustituidas** por §9 |

## 1. Modelo: tres dimensiones
| Dimensión | Qué expresa | Cómo se establece | Qué comprueba la CLI | Qué no se acredita |
|---|---|---|---|---|
| **A. Independencia de autoría** | El revisor no produjo ni modificó lo revisado | Roles del manifiesto + `authorship_independent: true` en el bloque del revisor | id canónico del revisor ∉ {orchestrator, architect, developer}; booleano `true`; **rol pertinente no vacío** en toda decisión registrada y `effective_authors` no vacío y ⊆ ids canónicos de ese rol (Gate 1: architect; Gate 2/3: developer) (GR-33) | La veracidad de la declaración; que los roles estén completos |
| **B. Aislamiento operativo** | Separación de contexto, permisos y entorno | Nivel enumerado declarado por el revisor | Enumeración válida y ≥ mínimo | **Siempre declarado**: la CLI nunca acredita aislamiento |
| **C. Trazabilidad y verificación de evidencias** | Qué respaldo documental existe y quién lo verificó | **Se calcula** a partir de evidencias tipadas y de registros `verification` | Existencia, tipo, exclusiones, ruta canónica y `sha256_lf`; forma de los registros de terceros | Veracidad del contenido de las evidencias |

**Reglas fijas en código** (no configurables, GR-25):
- A es absoluta en todo riesgo y en todo Gate PASS/PWR.
- `I0` nunca basta para PASS/PWR.
- PWR nunca habilita una transición.
- R8: la aprobación final no puede venir de autores.

**B · Aislamiento (ordenado):**
- `I0_CONTEXTO_COMPARTIDO`: revisor distinto que recibe el historial, la memoria o el contexto de trabajo del autor (O-1).
- `I1_CONTEXTO_SEPARADO`: instancia de agente o persona sin historial ni memoria del autor. Puede compartir runtime, usuario del sistema, workspace y credenciales. *Es el caso de agentes separados de LUNA o Cline en un mismo entorno.*
  - **Frontera del encargo (OB-4):** recibe objetivo, referencias y hashes. Puede incluir resúmenes del autor solo si cada uno puede contrastarse con una fuente citada. Si no es así, el revisor lo declara en su narrativa.
- `I2_PERMISOS_SEPARADOS`: I1 y, además, el revisor no puede modificar lo revisado (solo lectura impuesta, usuario del sistema o token distinto).
- `I3_ENTORNO_SEPARADO`: otra máquina, organización o custodia. Está disponible para el Owner y la matriz propuesta no lo usa (O-8).

**C · Evidencias tipadas (GR-24):** cada evidencia es `{"kind", "path", "sha256_lf"}`.
- **Tipos:**
  - `identity`: registro de lanzamiento o identificador del runtime.
  - `isolation`: configuración de permisos o de sesión.
  - `execution`: salida de los comandos ejecutados por el revisor.
- **Excluidos como evidencia:** el propio informe, `mission.json`, los seis `MISSION_FILES` y el artefacto revisado si tiene `path`.
- **Niveles calculados (GR-35):**
  - `G0_DECLARADA`: no se exige ninguna evidencia.
  - `G1_EVIDENCIA_REGISTRADA`: existe y está fijada al menos una evidencia de **cada** tipo que la matriz exige para ese Gate. Prueba integridad desde la fijación, no veracidad.
  - `G2_VERIFICACION_REGISTRADA` (O-2): G1 y, además, registros `verification` de un tercero para la identidad del revisor y de los autores pertinentes.
    - **El tercero** tiene `by` ∉ {orchestrator, architect, developer} y ≠ revisor (OB-5).
    - **Ubicación (GR-34, GR-38):** para los autores, en `roles` (registros C1 existentes); para el revisor, en `gates.<n>.review.reviewer_verification` `{id, by, method, ref, date}` del manifiesto, con `canon(id)` igual al `reviewer` del bloque. Lo escribe el tercero y nunca va dentro del informe del revisor.
    - **No cubre el aislamiento**, que sigue declarado.

## 2. Matriz proporcional (riesgo × Gate), razonada (GR-28, GR-31, GR-35)
Ubicación: `quality/controls.json` → `independence_minimums`, con `schema_version` 2.
- La CLI **falla cerrado** si la matriz falta, está incompleta o contiene valores no enumerados. Un G1 o G2 con un conjunto de tipos vacío es inválido (OB-11).
- **Monotonía:** para cada Gate, al subir el riesgo, I y G no pueden bajar y el conjunto de tipos exigidos debe incluir al del nivel anterior. Si se exige un artefacto fijado en un nivel, se exige en los superiores.
- **Reapertura (OB-1, OB-13):** cambiar `independence_minimums` o el `risk` de una misión **no aceptada** después de su Gate 1 reabre Gate 1 y requiere al Owner (`QUALITY_POLICY.md` § Reapertura). Las misiones aceptadas no se reabren. Esto es relevante porque GOV-001 introduce la matriz que rige su propia revalidación.
- **Cambios de la matriz y Gates ya decididos (GR-39):**
  - `can-implement` y `can-close` aplican **siempre** la matriz vigente: ninguna transición se obtiene por debajo de los mínimos actuales.
    - Consecuencia declarada (OB-17): si la matriz se endurece, una misión ya cerrada queda con `can-close` = 1 de forma permanente. No requiere más transiciones; su cierre consta en el historial.
  - `validate` aplica los mínimos solo a las misiones con `owner_acceptance` ≠ APPROVED.
    - Para las aceptadas, comprueba estructura e integridad: hashes, igualdades, A, R7 (orden de Gates y «owner APPROVED exige tres PASS») y R8 (OB-14).
    - Si no cumplen la matriz vigente emite el AVISO «no cumple la matriz vigente». La CLI no conserva matrices anteriores, así que **no** distingue entre «ya no cumple» y «nunca cumplió» (OB-13). No reescribe su historial.
  - Marcar APPROVED no permite eludir la matriz: `can-close` la reevalúa.
- **«Artefacto fijado» (GR-31):**
  - `artifact.ref` = `sha256_lf:` con `path` a la entrada `GATE2-INPUT-0N.sha256` dentro de la misión, recalculado por la CLI; **o bien**
  - `git:<sha>` cuando lo revisado ya está comiteado (por ejemplo, en el Gate de revalidación de §7).

| Riesgo | Gate 1 (plan) | Gate 2 (diff) | Gate 3 (ejecución) |
|---|---|---|---|
| LOW | I1 · G0 | I1 · G0 | I1 · G0 |
| MEDIUM | I1 · G0 | I1 · G0 · artefacto fijado | I1 · G1{execution} |
| HIGH | I1 · G1{identity} | I1 · G1{identity} · artefacto fijado | I1 · G1{identity, execution} |
| CRITICAL | I2 · G2{identity, isolation} | I2 · G2{identity, isolation} · artefacto fijado | I2 · G2{identity, isolation, execution} |

**Razonamiento:**
- **Gate 1:** que el revisor pudiera escribir el plan es poco relevante, porque el plan queda fijado por referencia. Basta I1; en HIGH se exige evidencia de identidad.
- **Gate 2:** el riesgo es que el revisor altere lo revisado. La mitigación es **general** (GR-37): un procedimiento de Gate 2 para MEDIUM y superiores, que se incorpora a `QUALITY_EVIDENCE_PROTOCOL.md` § Gate 2 y a `docs/templates/GATE2_REVIEW.md`:
  1. Antes de la revisión, el Orchestrator fija la entrada `GATE2-INPUT-<n>.sha256` en la misión: `git status --porcelain --untracked-files=all` y el `sha256_lf` de cada archivo modificado o nuevo. Es append-only y numerada por ciclo.
     - **Vínculo externo (GR-40):** el Orchestrator calcula el `sha256_lf` de la entrada **antes** de encargar la revisión y lo incluye en la instrucción al revisor. Así queda en el registro del runtime o de la conversación, fuera del workspace.
     - El revisor cita en `artifact` esa entrada con ese hash, o `git:` si lo revisado ya está comiteado.
  2. Tras el commit, el Orchestrator compara cada archivo comiteado con la entrada. Comprueba también que el hash citado en el bloque del revisor coincide con el de la instrucción. Lo registra por adición en `POST-GATE-VALIDATION-<sufijo>.md`; el sufijo identifica la entrada o el incremento, y en GOV-001 es `R01` o `R03` (OB-15).
  3. Esa comparación se revisa antes de la aceptación del Owner: la revisa el revisor de Gate 3 si el commit es anterior a Gate 3 y, si no, Quality o el Owner en la revisión de aceptación.

  **Adiciones permitidas tras los Gates (v8, OB-15):** los informes originales (sustituyendo las plantillas 04/05), `POST-GATE-VALIDATION-*` y las citas de hash. Cualquier otro cambio reabre Gate 2.

  **Riesgo residual declarado (GR-40):** con un revisor I1 con permisos de escritura, nada **dentro** del workspace es inalterable. Si el revisor modifica a la vez el árbol y la entrada:
  - se detecta **solo** si en el paso 2 el hash citado se compara con el registrado en la instrucción, fuera del workspace;
  - la CLI no hace esa comparación;
  - si los pasos 2 y 3 no se ejecutan, la alteración no se detecta.

  Por eso, I1 en Gate 2 hasta HIGH queda condicionado a ese procedimiento. La alternativa estricta es exigir I2 en Gate 2 desde HIGH (D3).
- **Gate 3:** el riesgo es la integridad de los resultados. Se exige evidencia `execution` (salida real fijada) desde MEDIUM.
- **MEDIUM frente a HIGH:** HIGH añade evidencia de identidad en todos los Gates, en línea con `RISK_MATRIX.md` («revisor independiente»).
- **CRITICAL (OB-6):** exige **declarar** I2 y aportar evidencia `isolation` fijada (la CLI no comprueba su contenido), además de la verificación de identidad por un tercero.

**Relajación que se somete a decisión (GR-24):** hoy R1/R4b exigen verificación registrada por un tercero en **todo** PASS/PWR. Con la matriz, LOW, MEDIUM y HIGH dejan de exigirla y pierden atribución a un tercero, que pasa a ser solo trazabilidad. **No es redundancia:** es una relajación deliberada para que el Owner no sea el verificador rutinario.

**Conflicto de interés declarado (O-6):** este Architect, autor de GOV-001 (HIGH), propone para HIGH un mínimo (I1·G1) que permitiría cerrar su propia misión sin un tercero, con evidencias producidas por el mismo Orchestrator. El Owner decide (D3).

## 3. Bloque estructurado y anclaje frente a cambios del autor (GR-25, GR-30, O-3, O-4, O-7)
- **Ubicación:** exactamente un bloque cercado en el informe, que empieza con una línea ` ```protheusai-review ` y termina con ` ``` `, sin cercas anidadas.
  - Se analiza después de normalizar CRLF a LF, con `json.loads`.
  - La narrativa libre no se lee.
- **Campos (claves exactas):**
  ```json
  {"mission": "GOV-001", "gate": "gate2", "risk": "HIGH", "decision": "PASS",
   "reviewer": "quality-x",
   "artifact": {"name": "diff GOV-001 ciclo N", "ref": "sha256_lf:<64 hex>", "path": "GATE2-INPUT-05.sha256"},
   "effective_authors": ["dev-1"],
   "authorship_independent": true,
   "isolation": "I1_CONTEXTO_SEPARADO",
   "evidence": [{"kind": "identity", "path": "evidence/launch-q.log", "sha256_lf": "<64 hex>"}],
   "date": "AAAA-MM-DD"}
  ```
- **Igualdades exigidas:** `mission` = id del manifiesto; `gate` = clave del Gate; `risk` = `mission.risk`; `decision` = decisión registrada.
  - Así, bajar el riesgo del manifiesto después de la revisión rompe la igualdad y se detecta (GR-25).
  - Un mismo informe no puede servir para dos Gates ni para dos misiones.
- **`artifact`:** `name` es texto no vacío que identifica el artefacto (C3, GR-33).
  - `ref`, gramática exacta: `git:<7–40 hex>`, `git:<7–40 hex>..<7–40 hex>`, `sha256:<64 hex>` o `sha256_lf:<64 hex>`.
  - `path` es null o una ruta canónica dentro de la misión; si la hay y `ref` es `sha256_lf:`, la CLI lo recalcula.
- **Plantilla:** el esqueleto lleva `"decision": "PENDING"`, que el bloque no admite, así que una plantilla sin rellenar falla cerrado.
- **FAIL (O-4):** exige un bloque válido y coherente (trazabilidad: igualdades, `artifact`, rol pertinente no vacío y `effective_authors` ⊆ rol), pero no aplica los mínimos de A (revisor ∉ roles), B y C. Así se puede registrar un FAIL de cualquier revisor. PASS/PWR aplican todo.

## 4. Hashes: recalculado frente a declarado (GR-30)
- **Recalculados por la CLI** (siempre `sha256_lf` = `sha256(bytes.replace(b'\r\n', b'\n'))`, lectura binaria):
  - `review.sha256_lf` del manifiesto;
  - `evidence[].sha256_lf`;
  - `artifact` cuando trae `path` y `sha256_lf:`.
- **Declarados:** cualquier otro hash, sea `sha256:` (bytes originales) o `sha256_lf:` sin `path`, las referencias `git:` (la CLI no ejecuta git; OB-9) y todos los hashes históricos de GOV-001 ciclos 1–3 y de las propuestas. Son identificadores; la CLI no los comprueba. G2-13 sigue abierto para ellos.
- **`hash <ruta>`:** imprime `sha256_lf` y `sha256` (bytes), cada uno con su etiqueta.
- `VERSION_ID` se sustituye por la gramática de `artifact.ref`.

## 5. Mitigaciones conservadas de v8 (GR-26)
- **GR-19:**
  - el revisor indica en su respuesta el `sha256_lf` de su informe;
  - el Orchestrator lo cita por adición en `POST-GATE-VALIDATION-R03.md`;
  - Quality compara ese valor con `review.sha256_lf` en el Gate siguiente.
  - Solo detecta cambios posteriores a la cita.
- **GR-23:**
  - entradas append-only `GATE2-INPUT-05…` con `git status --porcelain --untracked-files=all` y `sha256_lf` de cada archivo;
  - tras el commit, comparación con la última entrada, más tests y `validate` en un clon limpio, registrados en `POST-GATE-VALIDATION-R03.md`.
- **O-7:** la revisión independiente de esos registros queda asignada al Gate de revalidación de cierre de §7.

## 6. GOV-R02 → GOV-002 (investigación)
- Las firmas SSH quedan como línea de investigación para atribución e integridad. **No** son un requisito ni una dependencia de proyectos ordinarios.
- Con este modelo, una firma futura sería un `kind` más de evidencia que eleva C, sin cambiar A ni B.

## 7. Cierre de GOV-001 (resuelve la contradicción de v9, GR-26)
- El cierre formal ya **no** depende de GOV-002. Requiere:
  1. R01 y R03 implementados con PASS técnico en sus Gates;
  2. migrar `GOV-001/mission.json` a v3;
  3. un **Gate de revalidación** de GOV-001 con informes v3, **uno por Gate (gate1, gate2, gate3)** (OB-10), que cumplan la fila de riesgo vigente de GOV-001, sea la HIGH propuesta o la que fije el Owner (D3), con un revisor que cumpla A;
  4. la aprobación final del Owner (R8).
- Hasta entonces, los Gates y `owner_acceptance` siguen en PENDING.

## 8. Esquema, compatibilidad e inventario (GR-27, GR-29)
**Dos ejes independientes:**

| Eje | Opción 1 | Opción 2 |
|---|---|---|
| Formato | **F1** etiquetas Markdown + espejo en el manifiesto | **F2** bloque JSON único en el informe. Por Gate, el manifiesto guarda solo `decision` y `review`: null o `{file, sha256_lf, reviewer_verification}` (claves exactas; `reviewer_verification` null o `{id, by, method, ref, date}`) (GR-38) |
| Política | **P1** R1/R4b universales (verificación por terceros en todo PASS) | **P2** matriz proporcional §2 |

**Combinaciones:**

| Combinación | Qué es | Consecuencias |
|---|---|---|
| **F1+P1** | La opción mínima real | Elimina la regla del «no» y añade los campos A/B/C como etiquetas. El Owner, u otro tercero, sigue verificando identidades en todo PASS. Más duplicación. **No satisface** el requisito de aislamiento proporcional (OB-3). |
| **F1+P2** | Cumple la decisión sin el bloque JSON | La matriz evita la verificación rutinaria. Se mantienen el análisis de etiquetas y la duplicación informe↔manifiesto. Es necesario volver a fijar el informe por hash. |
| **F2+P2** · **recomendada** | Fuente única | Elimina el análisis de etiquetas, la detección de plantilla por texto y cuatro campos duplicados. La matriz evita la verificación rutinaria. Reescribe las fixtures de informe. |

F2+P1 es posible, pero no se recomienda: mantendría al Owner como verificador rutinario.

**Versión del esquema (cualquier combinación):**
- Sube a `schema_version: 3`, porque cambian las condiciones de validez de un PASS.
- **Los v1 y los v2 con alguna decisión ≠ PENDING son históricos (GR-32, opción a):**
  - se validan **solo estructuralmente** (`structure_errors` de v1/v2) con AVISO;
  - **se pierden todas** las reglas de contenido v1/v2, entre ellas: autoaprobación contra `author`/`implementation_author`, informes no plantilla, etiquetas, orden de Gates, «owner APPROVED sin tres PASS» y R8 de v2 (OB-7);
  - es aceptable porque nunca habilitan `can-*` y sus dictámenes quedan como registro histórico, no como autorización;
  - no hay que reescribir informes ni renombrar archivos.
  - **Alternativa (b), no recomendada:** congelar el código v1/v2 como ruta legacy con sus tests. Conserva esas comprobaciones a cambio de mantener dos validadores.
- **Los v2 con todos los Gates en PENDING** son válidos y migran mecánicamente.
- **Migración v2→v3:** se registra el SHA-256 y se renombra a `mission.v2.json` sin alterar bytes, igual que en v1. El paso es opcional para PENDING.

**Inventario de cambios (F2+P2):**
- `scripts/quality_cli.py`:
  - **sale:** `labels`, `report_errors`, `INDEPENDENCE`, la regla «no», `VERSION_ID`, la detección de plantilla por texto, R1/R4b universales, `legacy_errors` y las reglas de contenido v2 para manifiestos históricos (GR-32);
  - **se conservan, trasladadas al bloque (GR-33):** rol pertinente no vacío, `effective_authors` ⊆ rol, nombre del artefacto, R2, R8, orden de Gates y PWR no habilitante;
  - **entra:** parser del bloque, validación de la matriz, evidencias tipadas, `reviewer_verification`, rutas canónicas, `content_sha256_lf`, `hash` y v1/v2-histórico estructural.
  - Estimación (O-5), contando funciones afectadas en `6e5e929`: unas 120 líneas retiradas (incluidas `legacy_errors` y las reglas de contenido v2) y unas 160 añadidas.
- `scripts/new_mission.py`: genera v3 con Gates `{"decision": "PENDING", "review": null}`.
- `quality/controls.json`: `schema_version` 2 y `independence_minimums`; retira `identity_verification_record_required`.
- `docs/templates/GATE1_REVIEW.md`, `GATE2_REVIEW.md` y `GATE3_EVIDENCE.md`: el esqueleto del bloque más la narrativa. `GATE2_REVIEW.md` incluye además los pasos del procedimiento de Gate 2 (GR-37).
- `docs/QUALITY_EVIDENCE_PROTOCOL.md`:
  - § Identidades se reescribe: A/B/C, matriz y hashes;
  - § Para todo Gate: «prueba operativa de separación» pasa a ser el nivel B declarado más la evidencia que exija la matriz;
  - § Gate 2 incorpora el procedimiento general `GATE2-INPUT-<n>` / `POST-GATE-VALIDATION-<n>` y su revisión antes de la aceptación, con el riesgo residual declarado (GR-37).
- `docs/QUALITY_POLICY.md`: referencia a la matriz.
- `docs/MISSIONS/README.md`: v3, migración y v2 históricos. Los proyectos derivados deben actualizar `quality/controls.json` a la versión 2 con `independence_minimums`: sin ella, la CLI v3 falla cerrado (OB-12).
- `docs/MISSIONS/EXAMPLE-001/mission.json` → v3; `EXAMPLE-001/02-GATE1-REVIEW.md:5` → esqueleto nuevo.
- `docs/MISSIONS/GOV-001/mission.json` → v3, con el v2 conservado como `mission.v2.json`.

**Inventario de tests (`tests/test_governance.py` a `6e5e929`, 19 tests):**
- **Adaptar:**
  - los helpers `ident()`, `mission()` y `record()` (`:24-79`);
  - `:104` (`assertEqual(2, …)` → 3);
  - `test_new_mission_starts_pending…` (v3);
  - el subcaso `'schema 3'` de `test_malformed_records…` (`:327`), que pasa a probar `schema 4`;
  - `test_identities_need_registered_verification` (`:187-201`), que pasa a probar G2 solo donde lo exige la matriz.
  - `test_v1_manifests_are_historical`: se retira la aserción de autoaprobación v1 (`ORCH-X`), por GR-32; se conservan el AVISO, `can-*` = 1 y los bytes intactos.
  - `test_gate2_requires_known_developer`, `test_effective_author_may_be_subset_of_developers`, `test_fail_must_be_traceable_but_never_enables`, `test_reviewed_artifact_requires_name_and_version`: se adaptan al bloque y a `review.file`, conservando los casos de rol vacío, autor efectivo ⊆ rol, FAIL trazable y artefacto con nombre y referencia (GR-33).
- **Sustituir:** los 18 subcasos de etiquetas y prosa de `test_report_must_match_manifest` (7 de independencia y 11 de etiquetas), y `test_filled_templates…`.
- **Añadir:**
  - positivos: I1 en el mismo entorno en LOW, MEDIUM y HIGH; una narrativa libre no influye; LF y CRLF dan el mismo hash; v2 histórico con aviso.
  - negativos (cada uno con control de mutación):
    - A: revisor que es autor (incluido Orchestrator-Developer y tras normalizar); `authorship_independent` en `false`, ausente o no booleano.
    - B: `I0` con PASS o PWR; nivel inferior al mínimo.
    - C: evidencia faltante del tipo exigido; evidencia excluida (plan, informe, manifiesto); G2 sin `verification` o sin `reviewer_verification`, con `by` en algún rol o con `by` = revisor.
    - Autoría y trazabilidad (GR-33): developer vacío con Gate 2 PASS o FAIL; `effective_authors` vacío o fuera del rol; `artifact.name` vacío.
    - Bloque y manifiesto: `risk`, `mission` o `gate` distintos (riesgo bajado tras la revisión, informe reutilizado); bloque ausente, duplicado, anidado, con JSON inválido, con claves extra o ausentes, o plantilla sin rellenar; `decision` distinta.
    - Gramática: `artifact.ref` fuera de la gramática; artefacto no fijado en Gate 2 desde MEDIUM (ni `sha256_lf:`+`path` recalculable ni `git:`); `sha256_lf` de la entrada alterada; `execution` ausente en Gate 3 desde MEDIUM.
    - Integridad y rutas: `review.sha256_lf` o una evidencia alterados; informe no UTF-8 o con NUL (OB-8); rutas no canónicas o que pasan por una unión de directorio.
    - Verificación del revisor (GR-38): `reviewer_verification` de otro revisor (`id` ≠ `reviewer` del bloque); claves extra en `review`.
    - Cambio de matriz (GR-39): misión APPROVED que ya no cumple la matriz vigente → `validate` 0 con AVISO y `can-close` 1; misión abierta → `validate` 1.
    - Matriz: ausente, incompleta, con valores no enumerados o no monótona en I, en G, en los tipos exigidos o en el artefacto fijado.
    - Reglas que se mantienen: v2 con PASS es histórico y `can-*` = 1; PWR nunca habilita; R8; ningún mensaje dice «verificad[oa]» sin calificar.
- Se registra el número de tests y subcasos antes y después.

## 9. Decisiones solicitadas al Owner
- **D1 · Combinación:** F2+P2 (recomendada), F1+P2 o F1+P1.
- **D2 · Modelo:** niveles I0–I3, G0–G2 y tipos de evidencia, y la relajación de R1/R4b fuera de CRITICAL (§2).
- **D3 · Matriz y riesgo de GOV-001:** la matriz §2, o una más exigente, con una variante concreta: I2 en Gate 2 desde HIGH (GR-37).
  - **Consecuencia de I2 (OB-16):** hoy no hay permisos de solo lectura acreditados en LUNA ni en Cline. Exigir I2 bloquearía los Gate 2 de nivel HIGH en esos runtimes hasta que se configuren y se evidencien esos permisos.
  - Además, el riesgo con el que se revalidará GOV-001, teniendo en cuenta el conflicto de interés declarado.
- **D4 · Autorización (`OWNER-DECISION-02.md`)**, con transcripción literal de la decisión de las 09:53 y de estas líneas:
  - R01 (aprobado): implementar las adiciones de v8; commit solo tras PASS técnico en su Gate 2/3.
  - R03: implementar según v13 y D1–D3, solo tras PASS técnico de su Gate 1 sobre esta versión; commit solo tras PASS técnico en su Gate 2/3.
  - Detención: un FAIL, PENDING o PASS_WITH_RESERVATIONS detiene el avance; una excepción solo por decisión humana documentada, nunca registrada como PASS.
