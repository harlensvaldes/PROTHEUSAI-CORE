# GOV-001 · Revisión Quality del plan v11 (GOV-R03 rediseñado, GOV-R02 a GOV-002), ciclo 11

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r11
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) me asignó este nombre al lanzarme como subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento ni existe firma u otro mecanismo que lo acredite.
**Independencia verificada:** no — la autoría independiente es solo declarada: no redacté v1–v11 ni GOV-R-REVIEW-01..10 y no implementaré la misión. Comparto runtime, sesión anfitriona, usuario SO, workspace y credenciales con el autor, y el encargo lo redactó el autor. Clasificación v11 al final: A declarada · I1 (con resumen no contrastable declarado) · G0.
**Artefacto revisado:** GOV-001-R-PLAN-v11.md sha256:b46c32581c421faa18b0251c85f5fc6a09ee4e68dd9abd498d7778bd39d07b05
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v11 contra:
- v10 (diff palabra a palabra con `git diff --no-index --word-diff`), v8 (regla de prelación) y `GOV-R-REVIEW-10.md`;
- `AGENTS.md` y `agents/quality.md`;
- PROTHEUSAI-CORE `6e5e929`: `scripts/quality_cli.py`, `tests/test_governance.py`, `quality/controls.json`, `quality/RISK_MATRIX.md`, `docs/QUALITY_POLICY.md`, `docs/QUALITY_EVIDENCE_PROTOCOL.md`, `docs/MISSIONS/README.md`, `docs/templates/GATE*_REVIEW.md` y `docs/MISSIONS/GOV-001/*`.

Ejecuté la suite y `validate` en solo lectura con `python -B`. No hice prototipo de la CLI v3.

> PASS_WITH_RESERVATIONS **no habilita avanzar**. v11 no puede citarse como plan aprobado en `OWNER-DECISION-02` ni someterse a D1–D4 como cerrado mientras no se corrija GR-37 (MEDIUM) y, en la misma edición, GR-38 y GR-39 (LOW), y se pase un nuevo ciclo.
>
> **Criterio de dictamen.** No es FAIL: los defectos son locales y se corrigen sin rediseño. El modelo A/B/C, la prelación y la matriz son fieles a la decisión del Owner. No es PASS: GR-37 es una afirmación de control no acreditada en el razonamiento de proporcionalidad, que es el núcleo del encargo del Owner. GR-38 y GR-39 son defectos reales de especificación (un implementador tendría que inventar la regla), no cuestiones editoriales. Lo editorial u opcional figura en Observaciones y no condiciona el dictamen. El dictamen se limita al hash indicado.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash de v11 | `hashlib.sha256(bytes)` y `sha256(bytes.replace(b'\r\n',b'\n'))` | `b46c3258…d07b05` y `sha256_lf 66cc6a26…efe968`. **Coinciden** con el encargo (21 088 bytes) |
| Bases citadas (v11:4-5) | mismo cálculo | v10 `35c89eaa…e36a` ✓; v8 `0d6bcca0…2a93` ✓; REVIEW-10 `ceabad4c…2ef5` ✓ |
| Repo | `git log -1 --oneline`; `git status --porcelain --untracked-files=all --ignored` | `6e5e929`; 0 líneas antes y después |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 (Python 3.12.0) |
| Validación | `python -B scripts\quality_cli.py validate` | `OK — estructura consistente…`, exit 0 |
| Decisión del Owner de 09:53 | `files\`, repo | Sin registro escrito. Solo existe la paráfrasis del encargo (v11:8 lo reconoce) |

## Estado de hallazgos previos (REVIEW-10)
| ID | Estado | Evidencia |
|---|---|---|
| GR-31 | **PARCIAL → GR-37** | Resuelta la contradicción con «commit solo tras PASS». «Artefacto fijado» admite `sha256_lf:` + `path` a `GATE2-INPUT-0N` recalculado (v11:67-69). Las negativas están en §8 (v11:209). Queda abierta la segunda mitad («quién y cuándo compara lo comiteado con lo revisado»): solo se resuelve para GOV-001 (§5, §7) y la matriz es general (GR-37). |
| GR-32 | **CERRADO** | Opción (a) declarada: histórico solo estructural (v11:166), pérdida explícita (v11:167), alternativa (b) con su consecuencia (v11:170) e inventario coherente (v11:176, 179, 198). El test v1 del repo (`tests/test_governance.py:389-391`) confirma que la aserción `ORCH-X` es la única de contenido que se retira. Matiz de completitud en OB-7. |
| GR-33 | **CERRADO** | A incluye «rol pertinente no vacío» y `effective_authors` ⊆ rol (v11:31), también en FAIL (v11:111), como hoy (`quality_cli.py:209-212, 240-241` aplican a toda decisión ≠ PENDING). `artifact.name` es obligatorio (v11:107). Hay tests para adaptar y añadir (v11:199, 207). Los casos `:152-174` quedan cubiertos por «rutas no canónicas» y «plantilla sin rellenar», y `:203-212` por la negativa Orchestrator-Developer (v11:204). Única omisión: no-UTF-8 (OB-8). |
| GR-34 | **PARCIAL → GR-38** | La ubicación está fijada (v11:59) y hay negativas (v11:206). El registro no queda ligado al revisor que verifica y contradice la forma F2 del manifiesto. |
| GR-35 | **CERRADO** | G0 y G1 definidos sin ambigüedad (v11:55-56). La celda MEDIUM·Gate 2 se reescribe como `G0 · artefacto fijado` (v11:74). La monotonía se define por componentes (v11:65). La matriz usa conjuntos de tipos `G1{…}` explícitos. |
| GR-36 | **CERRADO** | La fila de v11:23 sustituye los pasos 5-6 de v8 (`v8:191-192`) por §7. Los pasos 1-4 (`v8:187-190`) son coherentes con §9 D4. La mención de GOV-002 de `v8:59` y la de `v8:184` caen dentro de secciones marcadas como adaptadas o sustituidas (v11:16, 20). |
| OB-1 | ATENDIDA | v11:66. `QUALITY_POLICY.md:35-36` («reglas de autorización… o riesgos») la respalda. Su efecto sobre misiones ya cerradas queda sin definir → GR-39. |
| OB-2 | CERRADA | v11:24. |
| OB-3 | CERRADA | v11:157. |
| OB-4 | CERRADA | v11:44. Este informe la aplica (Limitación de independencia). |
| OB-5 | CERRADA | v11:58. |
| OB-6 | CERRADA | v11:83. |

No reabro GR-24..GR-30 ni O-1..O-8: no hay evidencia nueva y v11 no modifica sus líneas, salvo en lo indicado arriba.

## Regresiones v10→v11
El diff (`--word-diff`) contiene solo cambios trazables a GR-31..36 y OB-1..6. No encontré regresiones funcionales. La frase nueva de v11:80 (revisión independiente asignada a §7) es la que origina GR-37. La nueva clave `review.reviewer_verification` (v11:59) es la que origina GR-38.

## Hallazgos nuevos

### GR-37 · MEDIUM · La proporcionalidad de Gate 2 (I1 hasta HIGH) descansa en mitigaciones propias de GOV-001 que el proceso general no tiene
**Evidencia:**
- v11:80 justifica «I1 basta hasta HIGH» en Gate 2 con tres elementos: la entrada `GATE2-INPUT` fijada, «la comparación posterior al commit (§5)» y «la revisión independiente de esa comparación corresponde al Gate de revalidación (§7)».
- §5 (v11:126-131) y §7 (v11:137-142) son **específicos de GOV-001**: `POST-GATE-VALIDATION-R03.md`, entradas `-05…` que continúan la numeración de GOV-001 (`v8:136`) y el «Gate de revalidación de GOV-001».
- La matriz es **general**: `quality/controls.json` → `independence_minimums` (v11:63), aplicable a toda misión de PROTHEUSAI-CORE y de los proyectos derivados.
- El proceso general no prevé ninguno de los tres elementos:
  - `QUALITY_EVIDENCE_PROTOCOL.md` § Gate 2 solo dice «Diff real revisado…»;
  - `docs/templates/GATE2_REVIEW.md:7` solo pide `git:` o `sha256:` «del árbol revisado»;
  - `QUALITY_POLICY.md` no menciona comparación posterior al commit;
  - el grep de `GATE2-INPUT|POST-GATE` en `docs/QUALITY_*`, `docs/templates`, `docs/MISSIONS/README.md` y `quality/` da 0 coincidencias.
- El inventario §8 (v11:183-185) reescribe el protocolo solo en § Identidades y § Para todo Gate. No añade a § Gate 2 la entrada de árbol, la comparación posterior al commit ni quién la revisa.
- La CLI solo comprobará que `artifact.path` es un archivo de la misión cuyo `sha256_lf` coincide (v11:68, v11:209). No comprueba qué contiene ni que alguien lo compare con el commit (v11:118).

**Impacto:** en cualquier misión MEDIUM/HIGH que no sea GOV-001, «artefacto fijado» se cumple con cualquier archivo con hash. Nadie está obligado a comparar el commit con lo revisado, ni hay un Gate posterior que lo revise de forma independiente. La razón por la que la matriz admite que un revisor con permiso de escritura (I1) emita Gate 2 HIGH no existe fuera de GOV-001. El plan presenta como mitigación un control que, en general, no está implantado. Es el tipo de garantía no acreditada que el Owner pidió evitar, y afecta a D2 y D3.

**Corrección mínima (elegir una y declararla):**
- **(a) Generalizar el control.** Añadir al inventario `QUALITY_EVIDENCE_PROTOCOL.md` § Gate 2, `GATE2_REVIEW.md` y `MISSIONS/README.md` con estas reglas:
  - antes de Gate 2, el Orchestrator genera la entrada append-only `GATE2-INPUT-NN.sha256` (`git status --porcelain --untracked-files=all` + `sha256_lf` por archivo);
  - el revisor de Gate 3 comprueba que el árbol coincide con esa entrada antes de ejecutar las pruebas;
  - tras el commit, el Orchestrator compara y registra el resultado por adición, y el Owner lo ve antes de `owner_acceptance`.

  Consecuencia: un paso más por misión, sin código nuevo.
- **(b) Declarar el riesgo residual.** Reescribir v11:80: fuera de GOV-001, la alteración por el revisor de Gate 2 solo la detectaría una comparación del Orchestrator, que no es independiente ni obligatoria. Someterlo al Owner en D2/D3 como riesgo aceptado.
- **(c) Endurecer la matriz.** Exigir I2 en Gate 2 HIGH. Consecuencia: GOV-001 y los proyectos HIGH necesitarían permisos de solo lectura reales, que hoy no están acreditados en LUNA ni en Cline.

### GR-38 · LOW · `reviewer_verification` no está ligado al revisor verificado y contradice la forma F2 del manifiesto
**Evidencia:**
- v11:59 sitúa la verificación en `gates.<n>.review.reviewer_verification` `{by, method, ref, date}`, sin `id` del revisor verificado.
- En v2 la verificación va dentro de la identidad del revisor (`gates.<n>.reviewer = {id, evidence, verification}`, `quality_cli.py:76-96, 130-131`), así que queda ligada a un `id`.
- v11:150 (F2) dice que el manifiesto guarda «solo `decision` y `review: {file, sha256_lf}`». §8 tampoco fija las claves exactas de `review`.
- Las negativas de v11:206 no incluyen «verificación de otro revisor».

**Impacto:** en CRITICAL, si se sustituyen el informe (`review.file`/`sha256_lf`) por el de otro revisor, la verificación registrada por el tercero sigue siendo válida. G2 deja de atribuir la identidad verificada, y esto supone una regresión frente a v2. Además, dos implementaciones conformes podrían aceptar o rechazar `review` con tres claves.

**Corrección mínima:** `reviewer_verification` `{id, by, method, ref, date}`, con `canon(id)` igual a `reviewer` del bloque. Fijar las claves exactas de `review` (`file`, `sha256_lf` y `reviewer_verification` opcional, o null). Añadir la negativa «verificación de otro revisor».

### GR-39 · LOW · No se define cómo afecta un cambio de la matriz a los Gates ya decididos
**Evidencia:**
- La CLI valida cada PASS/PWR contra la matriz vigente y falla cerrado (v11:64, v11:31-32).
- v11:66 solo dice que cambiar la matriz «después de su Gate 1 reabre Gate 1». No distingue misiones en curso de misiones cerradas (`owner_acceptance` APPROVED).
- El bloque (v11:96-102) no registra qué matriz se aplicó.
- D3 (v11:218) admite expresamente «una más exigente», y GOV-002 (§6) podría elevar C más adelante.

**Impacto:** endurecer la matriz convierte en error de `validate` (CI en rojo) todo Gate decidido que no cumpla la nueva fila, incluidas las misiones cerradas. «Reabrir Gate 1» de una misión aprobada no es un proceso definido. Relajarla, a la inversa, legitima en retrospectiva informes que no cumplían. El implementador tendría que decidir esta política.

**Corrección mínima (una línea, elegir):**
- **(a)** Se valida siempre contra la matriz vigente. Endurecerla exige una decisión del Owner sobre las misiones ya decididas: revalidarlas o tratarlas como históricas, con AVISO.
- **(b)** Cada `review` registra el `sha256_lf` de `controls.json` aplicado y la CLI exige el valor vigente solo en Gates PENDING. Es más trazable, pero añade un campo y requiere conservar las matrices anteriores.

La opción (a) es la más sencilla.

## Valoraciones solicitadas
- **Independencia de autoría frente a aislamiento frente a garantía:** bien separadas (v11:31-33). Compartir runtime, usuario SO o workspace se admite en I1 sin negar la autoría (v11:43). B siempre se declara y nunca se acredita.
- **Nunca autoaprobación:** A es absoluta en PASS/PWR (v11:36). Se conservan el rol pertinente no vacío y `effective_authors` ⊆ rol (GR-33 cerrado). R8 se conserva.
- **Proporcionalidad por riesgo y Gate:** razonada para Gate 1 y Gate 3. En Gate 2 no está acreditada fuera de GOV-001 (GR-37).
- **schema_version:** manifiesto v3 y `controls.json` v2, justificados. Tratamiento de v1/v2 decididos coherente (GR-32 cerrado).
- **Hashes normalizados frente a bytes:** correcto. Solo `sha256_lf` se recalcula y `hash` imprime ambos con etiqueta (v11:113-119). Matiz de `git:` en OB-9.
- **Reducción de redundancia:** F2 elimina la duplicación entre informe y manifiesto y el análisis de etiquetas. La regresión de C3 ya está resuelta.
- **Sobrealcance:** no lo hay. GOV-R02 queda como investigación sin dependencias (§6) y GOV-001 no se amplía.

## Observaciones (no condicionan el dictamen)
Son mejoras de redacción o completitud sin efecto sobre la validez de un PASS, o casos cubiertos indirectamente.
- **OB-7.** v11:167 enumera las reglas v1/v2 que se pierden en los históricos, pero omite la regla R8 v2, el orden de Gates y «owner APPROVED sin tres PASS» (`quality_cli.py:184-193` en v1; `:265-276` en v2). No tiene efecto porque los históricos nunca habilitan `can-*`, pero conviene escribir «todas las reglas de contenido, entre ellas…».
- **OB-8.** Al inventario de negativas le falta «informe no UTF-8 o con NUL» (hoy `tests/test_governance.py:168-172`). Como el bloque se lee del archivo, conviene conservar el caso.
- **OB-9.** §4 (v11:118) no clasifica `git:` como declarado. En §2 (v11:69), `git:` satisface «artefacto fijado» sin que la CLI ejecute git. Conviene añadir «las referencias `git:` son declaradas».
- **OB-10.** §7 paso 3 (v11:141) habla de «un Gate de revalidación», pero el bloque exige `gate` igual a la clave (v11:104) y `can-close` exige los tres Gates. Conviene precisar que la revalidación produce un informe v3 por Gate (gate1..gate3).
- **OB-11.** v11:56: G1 con conjunto vacío (`G1{}`) queda sin clasificar como valor válido o no enumerado. La matriz propuesta no lo usa, pero conviene declararlo inválido.
- **OB-12.** El inventario de `MISSIONS/README.md` (v11:186) debería mencionar que los proyectos derivados deben actualizar `quality/controls.json` a v2: con la CLI v3, una matriz ausente falla cerrado (v11:64).

## Qué NO verifiqué
- El texto literal de la decisión del Owner de 09:53: solo dispongo de la paráfrasis del encargo, redactada por el autor.
- Ninguna implementación v3. No hay prototipo y no medí la estimación de unas 120 líneas retiradas y 160 añadidas (v11:179). Una suma aproximada de `legacy_errors`, `report_errors`, `labels`, `report_text`/`has_evidence`, constantes y R1/R4b en `6e5e929` da del orden de 100-120 líneas, compatible con la cifra.
- Que exista un registro de lanzamiento utilizable como evidencia `identity` en este runtime, y las propiedades reales de LUNA o Cline.
- La existencia de proyectos derivados con manifiestos v2 decididos o con `controls.json` v1.
- La identidad de ningún participante.
- Los pasos de R01 (aprobado, fuera de alcance).

**Archivos temporales:** ninguno creado por mí. La salida de una herramienta se guardó automáticamente en `%TEMP%` y la borré al terminar (`Test-Path` = False). La suite usa `TemporaryDirectory`, que se autoelimina. El repositorio no cambió: 0 líneas de `git status` antes y después.

## Limitación de independencia
- Soy un subagente lanzado por el autor (copilot-sdk-main) en el mismo runtime, sesión anfitriona, usuario SO, workspace y credenciales. Tengo permiso técnico de escritura sobre el artefacto revisado y sobre el repositorio. Me abstuve de usarlo, pero eso no es verificable.
- **Clasificación con el modelo v11:**
  - **A (autoría):** independiente **declarada**. Mi id no figura en ningún rol y no produje ni modifiqué lo revisado.
  - **B (aislamiento):** `I1_CONTEXTO_SEPARADO` declarado: contexto nuevo, sin historial ni memoria del autor. Según la frontera OB-4 (v11:44), declaro que el encargo incluye un resumen del autor sobre la decisión del Owner de 09:53 que **no puede contrastarse** con ninguna fuente escrita. Las demás referencias van con hash y las contrasté. No llego a I2 porque puedo escribir.
  - **C (trazabilidad):** `G0_DECLARADA`. No hay evidencia `identity`/`isolation`/`execution` fijada ni verificación de un tercero.
- Con la matriz propuesta, este informe **no alcanzaría** el mínimo de un Gate 1 formal de GOV-001 (HIGH: I1·G1{identity}). Es un dictamen técnico sobre el plan, no un Gate de `mission.json`.
