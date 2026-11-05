# GOV-001 · Revisión Quality del plan v10 (GOV-R03 rediseñado, GOV-R02 a GOV-002), ciclo 10

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r10
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) me asignó este nombre al lanzarme como subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c (usuario SO `fayat\cvaldes`, equipo `CAF5PM82JL`). No tengo acceso al registro de lanzamiento ni hay firma u otro mecanismo que la acredite.
**Independencia verificada:** no — autoría independiente solo declarada (no redacté v1–v10 ni GOV-R-REVIEW-01..09 y no implementaré la misión); comparto runtime, sesión anfitriona, usuario SO, workspace y credenciales con el autor, y el encargo lo redactó el autor. Clasificación v10 al final: A declarada · I1 (en el límite) · G0.
**Artefacto revisado:** GOV-001-R-PLAN-v10.md sha256:fc7296abece599085539b3b8f2cfce1d1454f420e4013ba5b9e2cdfb7cf79204
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v10 frente a v8 (regla de prelación), v9, `GOV-R-REVIEW-09.md`, `OWNER-DECISION-01.md`, `AGENTS.md`, `agents/quality.md` y PROTHEUSAI-CORE `6e5e929` (`scripts/quality_cli.py`, `scripts/new_mission.py`, `tests/test_governance.py`, `quality/controls.json`, `quality/RISK_MATRIX.md`, `docs/QUALITY_EVIDENCE_PROTOCOL.md`, `docs/QUALITY_POLICY.md`, `docs/MISSIONS/README.md`, `docs/templates/GATE2_REVIEW.md`, `docs/MISSIONS/GOV-001/*`). Suite y `validate` en solo lectura con `python -B`. Sin prototipo de la CLI v3.

> PASS_WITH_RESERVATIONS **no habilita avanzar**: v10 no puede citarse como plan aprobado en `OWNER-DECISION-02` ni someterse a D1–D4 como cerrado hasta corregir GR-31..GR-33 (MEDIUM) y pasar un nuevo ciclo. No es FAIL: el modelo A/B/C, la matriz y la prelación son fieles a la decisión del Owner, y los defectos son locales, corregibles sin rediseño. El dictamen se limita al hash indicado.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash de v10 | `Get-FileHash -Algorithm SHA256`; `sha256(bytes.replace(b'\r\n',b'\n'))` | `FC7296AB…F79204` y `sha256_lf 35c89eaa…e17e36a`: **coinciden** con el encargo (17 262 bytes) |
| Bases citadas en v10:4-5 | mismo cálculo | v9 `0f3c6982…8468` ✓; v8 `0d6bcca0…2a93` ✓; REVIEW-09 `f242868e…de8e` ✓ |
| Repo | `git log -1`; `git status --porcelain --untracked-files=all --ignored` | `6e5e929`; 0 líneas |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 (Python 3.12.0) |
| Validación | `python -B scripts\quality_cli.py validate` | `OK — estructura consistente…`, exit 0 |
| Decisión del Owner 09:53 | `files\`, repo | Sin registro escrito; solo la paráfrasis del encargo (v10:8 lo reconoce) |

## Estado de hallazgos previos (REVIEW-09)
| ID | Estado | Evidencia |
|---|---|---|
| GR-24 | **CERRADO** | Evidencias tipadas `identity/isolation/execution` y exclusiones (v10:46-51); G1 exige el tipo que fija la matriz (v10:54); G2 no cubre aislamiento, declarado (v10:55); C renombrada a «trazabilidad y verificación» (v10:32); relajación de R1/R4b presentada como tal (v10:75). Residuos nuevos de definición en GR-34 y GR-35. |
| GR-25 | **CERRADO** | `risk`, `mission`, `gate`, `decision` en el bloque con igualdad (v10:94-96); matriz que falla cerrado (v10:59); reglas fijas en código (v10:34-38). El punto 4 (cambio de matriz/riesgo reabre Gate 1) no se recoge expresamente, pero `QUALITY_POLICY.md:36` ya lo cubre («reglas de autorización», «riesgos») → OB-1. |
| GR-26 | **PARCIAL → GR-36** | Tabla de prelación completa (v10:13-25), mitigaciones GR-19/GR-23/O-7 conservadas (§5), líneas de autorización (§9 D4) y contradicción del cierre resuelta (§7). Queda la «Secuencia» de v8 conservada con pasos que remiten a opciones A/B eliminadas. |
| GR-27 | **PARCIAL → GR-32, GR-33** | Inventario de archivos completo (§8: `new_mission.py`, protocolo, README, `EXAMPLE-001/02:5`, `controls.json`); v2 decididos tratados como históricos. Pero el tratamiento histórico contradice la lista de código retirado (GR-32) y el inventario de tests omite controles vigentes (GR-33). |
| GR-28 | **CERRADO** (requisito de razonamiento) | Razonamiento por Gate y MEDIUM/HIGH (v10:68-73). El contenido de la fila Gate 2 introduce un defecto nuevo → GR-31. |
| GR-29 | **CERRADO** | Ejes F/P ortogonales y combinaciones con consecuencias (v10:136-151). Matiz en OB-3. |
| GR-30 | **CERRADO** | §4: recalculado vs declarado; gramática exacta de `artifact.ref` (v10:97-99); `hash` imprime ambos con etiqueta. |
| O-1 | CERRADO | v10:41. |
| O-2 | CERRADO | `G2_VERIFICACION_REGISTRADA` (v10:55). |
| O-3 | CERRADO | Cerca exacta, CRLF→LF, sin anidadas; plantilla con `PENDING` falla cerrado; negativos de plantilla, `gate` distinto e informe reutilizado listados en §8. |
| O-4 | CERRADO | v10:101. |
| O-5 | ATENDIDA, condicionada | Método declarado (funciones afectadas en `6e5e929`), pero la cifra de retirada depende de resolver GR-32. |
| O-6 | CERRADO | Conflicto declarado (v10:77) y sometido a D3. |
| O-7 | CERRADO | `mission` en el bloque con igualdad. |
| O-8 | CERRADO | v10:44. |

## Hallazgos nuevos

### GR-31 · MEDIUM · El requisito `git:` para Gate 2 desde MEDIUM contradice el proceso conservado y su mitigación no es comprobable
**Evidencia:**
- Matriz v10:64-66 exige «artefacto `git:`» en Gate 2 desde MEDIUM; v10:70 lo justifica: «si el revisor modificara el código, la referencia ya no coincidiría».
- El proceso que v10 conserva revisa Gate 2 **antes** del commit: §5 (v10:118-121) mantiene `GATE2-INPUT-05…` sobre el árbol de trabajo y la comparación «tras el commit»; §9 D4 y v8 «Secuencia» exigen «commit solo tras PASS técnico en su Gate 2/3». La práctica registrada lo confirma: `docs/MISSIONS/GOV-001/04-GATE2-REVIEW.md:7` y `GATE2-REVIEW-01/02.md:7` identifican el artefacto como «árbol de trabajo GATE2-INPUT-0N.sha256 sha256:…», y la plantilla `docs/templates/GATE2_REVIEW.md:7` admite `sha256:<64 hex> del árbol revisado`.
- §4 (v10:108) declara que la CLI no comprueba refs `git:`; nada compara el commit final con el `git:` revisado (la comparación de §5 usa los `sha256_lf` de `GATE2-INPUT`, no la ref).

**Impacto:** con «commit solo tras PASS», un Gate 2 formal MEDIUM+ es inalcanzable salvo con commits previos no previstos (y que `AGENTS.md` §4 sujeta a autorización); y la razón que permite I1 hasta HIGH en Gate 2 descansa en un identificador declarado que nadie contrasta. Proporcionalidad mal fundada para el Gate más sensible a la escritura del revisor.

**Corrección mínima:** admitir para Gate 2 la fijación ya usada y **comprobable por la CLI**: `artifact.ref: sha256_lf:<hex>` con `path` a la entrada `GATE2-INPUT-0N` dentro de la misión (recalculada; excluida como evidencia por ser el artefacto). Exigir `git:` solo cuando el artefacto ya esté comiteado (p. ej., Gate de revalidación §7) o como alternativa. Reescribir v10:70 indicando quién y cuándo compara lo comiteado con lo revisado (la comparación de §5).

### GR-32 · MEDIUM · §8 se contradice: los históricos «se validan con sus reglas», pero se retira el código de esas reglas
**Evidencia:**
- v10:155-157: v1 y v2 decididos «se validan con sus reglas y un AVISO».
- v10:164 retira `labels`, `report_errors`, `INDEPENDENCE`, la regla «no», `VERSION_ID`, la detección de plantilla por texto y R1/R4b.
- Las reglas v1 usan la detección de plantilla: `legacy_errors` → `has_evidence` (`quality_cli.py:178`) → `report_text` (`:59`). Las reglas v2 son exactamente `report_errors`/`labels`/`INDEPENDENCE`/`VERSION_ID`/R1-R4b (`:197-215`, `:242-244`, `:252-264`).
- El inventario de tests sustituye los 18 subcasos v2 (v10:185) mientras afirma que un v2 con PASS se sigue validando (v10:196).

**Impacto:** cualquier implementación incumple una de las dos frases; la estimación de O-5 (≈70 líneas retiradas) y la «reducción de controles» dependen de cuál se elija, y el Owner decidiría D1 sin saberlo.

**Corrección mínima:** elegir y declarar: (a) históricos validados **solo estructuralmente** (`structure_errors`) con AVISO, declarando la pérdida de comprobaciones, aceptable porque nunca habilitan `can-*`; o (b) congelar el código v1/v2 en una ruta legacy con sus tests, sin contarlo como retirado. Ajustar §8 (código, tests, estimación) y el protocolo.

### GR-33 · MEDIUM · Regresión no declarada de controles de C3 y de soporte de A; inventario de tests incompleto
**Evidencia:**
- Hoy la CLI exige, en toda decisión registrada: autor efectivo no vacío y ⊆ rol pertinente (`quality_cli.py:209-212`), rol pertinente no vacío («independencia no evaluable», `:240-241`) y nombre + versión del artefacto (`:242-244`). Tests: `test_report_must_match_manifest` subcasos «autor efectivo …» (`tests/test_governance.py:227-230`), `test_gate2_requires_known_developer` (`:181-185`), `test_reviewed_artifact_requires_name_and_version` (`:250-258`, primer caso: `sha256:` sin nombre), `test_fail_must_be_traceable…` (`:273-283`).
- v10 solo exige igualdad de `mission/gate/risk/decision` (v10:94) y `effective_authors` no tiene regla; A comprueba «revisor ∉ roles» (v10:30). v10:185 sustituye los 4 subcasos de autor efectivo sin equivalente en «Añadir» (v10:186-196). `artifact.ref: sha256:<hex>` con `path: null` es válido (v10:97-99), sin nombre.
- Tampoco se inventarían `:152-174` (plantilla copiada, `evidence_file` fuera de la misión, NUL, no UTF-8), `:203-212` (Orchestrator-Developer, verificación por el autor) ni `:244-248`.

**Impacto:** con `roles.developer` vacío, el Developer real puede revisar su propio Gate 2 y satisfacer A (hoy bloqueado por `:240-241`): debilita la regla absoluta que el Owner reafirmó. Además, se pierde parte de C3 de `OWNER-DECISION-01` (autor efectivo, artefacto identificable).

**Corrección mínima:** añadir al bloque: `effective_authors` no vacío y ⊆ ids del rol pertinente (Gate 1: architect; Gate 2/3: developer), y rol pertinente no vacío en toda decisión registrada; decidir si `artifact` exige nombre o `path` cuando `ref` es `sha256:`. Completar el inventario de tests con los casos citados (adaptados al bloque y a `review.file`).

### GR-34 · LOW · G2 del revisor no tiene ubicación en el formato recomendado F2
**Evidencia:** G2 exige registros `verification` de un tercero para el revisor (v10:55). En F2 el manifiesto guarda solo `decision` y `review: {file, sha256_lf}` (v10:140, `new_mission.py` v3: `{"decision": "PENDING", "review": null}`, v10:167) y el bloque tiene claves exactas sin `verification` (v10:83-92). Los registros `verification` hoy viven en `gates.<n>.reviewer` (`quality_cli.py:130-131`, `:256-259`), que F2 elimina.

**Impacto:** CRITICAL no es implementable tal como se describe (falla cerrado o el implementador inventa dónde y quién escribe la verificación, decisión de diseño material). No afecta a GOV-001 (HIGH).

**Corrección mínima:** fijar la ubicación (p. ej., `gates.<n>.review.reviewer_verification {by, method, ref, date}` en el manifiesto, escrita por el tercero y nunca dentro del informe del revisor) y su prueba negativa.

### GR-35 · LOW · Cálculo de G y monotonía de la matriz sin definir en casos frontera
**Evidencia:** G0 = «sin evidencias»; G1 = «las evidencias que exige la matriz … existen» (v10:53-54). La celda MEDIUM·Gate 2 exige «G1» sin tipo (v10:64): G1 es vacuo (cero exigidas ⇒ cumplido) o exige ≥1 evidencia de cualquier tipo; ambas lecturas son posibles. «No monótona» (v10:59) no define cómo comparar conjuntos de tipos y la marca `git:`.

**Impacto:** dos implementaciones conformes darían resultados distintos; los tests «matriz no monótona» y «evidencia faltante» no son deterministas desde el plan.

**Corrección mínima:** escribir esa celda como `G0 · git:` o definir G1 como «≥1 evidencia y todas las exigidas»; definir la monotonía componente a componente (I y G no decrecientes, tipos ⊆, `git:` implicado).

### GR-36 · LOW · Residuo de GR-26: la «Secuencia» de v8 conservada remite a opciones eliminadas
**Evidencia:** v10:23 conserva «Secuencia» de v8, cuyos pasos 5-6 son «Decisión del Owner (A o B) en `06-DECISION.md`» y «GOV-002, si se elige A»; v10:22 y §7 sustituyen A/B y desvinculan el cierre de GOV-002. La Secuencia no incluye los pasos de §7 (migración a v3, Gate de revalidación).

**Impacto:** el texto que `OWNER-DECISION-02` debe citar sigue teniendo dos secuencias de cierre incompatibles; la regla «v10 prevalece en lo que modifica» no basta porque la tabla dice expresamente «Conservadas».

**Corrección mínima:** marcar los pasos 5-6 de la Secuencia de v8 como sustituidos por §7 y añadir allí los pasos 2-4 de §7.

## Valoraciones solicitadas
- **Autoría absoluta:** se mantiene como norma (v10:35, A en todo PASS/PWR, R8). Su apoyo automático pierde dos comprobaciones vigentes (GR-33).
- **Tres dimensiones sin afirmar aislamiento inexistente:** sí; B siempre declarado (v10:31), G1 «integridad desde la fijación, no veracidad» (v10:54). Compartir runtime/usuario/workspace se admite en I1 sin negar autoría: fiel al Owner.
- **Proporcionalidad por riesgo y Gate:** razonada; la fila Gate 2 está mal fundada (GR-31).
- **schema_version:** subida a 3 justificada; tratamiento de v2 decididos definido, pero contradictorio con el inventario (GR-32).
- **Hashes:** correcto (GR-30 cerrado).
- **Reducción de controles:** la eliminación del análisis de etiquetas y la prosa es correcta; la de controles C3 no está declarada (GR-33).
- **Sobrealcance:** no hay; GOV-R02 queda como investigación sin dependencias (§6).

## Observaciones (no condicionan el dictamen)
- **OB-1.** Añadir una línea: cambiar `independence_minimums` o `risk` después del Gate 1 reabre Gate 1 y requiere al Owner (ya implícito en `QUALITY_POLICY.md:36`). Es relevante porque GOV-001 introduce la matriz que rige su propia revalidación (O-6).
- **OB-2.** v10:23 «la autorización de R03 se redacta en §8» → está en §9 (D4).
- **OB-3.** F1+P1 (v10:147) no satisface «aislamiento proporcional al riesgo y tipo de Gate»; conviene decirlo en sus consecuencias.
- **OB-4.** I1 «recibe solo referencias» (v10:42): falta la frontera para encargos redactados por el autor que contienen resúmenes (como este). Propuesta: I1 admite un encargo con objetivo, referencias y hash, y los resúmenes deben poder contrastarse con una fuente; si no, declararlo.
- **OB-5.** G2: `by` ∉ autores del artefacto y ≠ revisor (v10:55) permite que el Orchestrator no autor, que lanza al revisor y produce las evidencias, sea el «tercero». Valorar excluir todos los roles, en coherencia con A.
- **OB-6.** v10:73 «exige que el revisor no pueda escribir»: lo que se exige es declarar I2 y aportar evidencia `isolation`, sin comprobación de contenido (v10:31). Ajustar la redacción.

## Qué NO verifiqué
- El texto literal de la decisión del Owner de 09:53 (solo la paráfrasis del encargo, redactada por el autor).
- Ninguna implementación v3: no hay prototipo y la estimación de líneas no se midió.
- Las propiedades reales de LUNA o Cline ni que los subagentes de GOV-001 cumplan I1.
- La existencia de proyectos derivados con manifiestos v2 decididos.
- La identidad de ningún participante.
- La ejecución de `GOV-R01-reconstruct.py` u otros pasos de R01 (aprobado, fuera de alcance).

Archivos temporales: una copia numerada de `tests/test_governance.py` en `%TEMP%` (borrada; `Test-Path` = False) y un volcado de salida de la herramienta en `%TEMP%` (borrado). La suite usa `TemporaryDirectory`, que se autoelimina. Repositorio sin cambios (0 líneas de `git status` antes y después).

## Limitación de independencia
- Soy un subagente lanzado por el autor (copilot-sdk-main) en el mismo runtime, sesión anfitriona, usuario del SO, workspace y credenciales. Tengo permiso técnico de escritura sobre el artefacto revisado; me abstuve de usarlo, pero eso no es verificable. El encargo lo redactó el autor e incluye un resumen suyo de la decisión del Owner, además de referencias con hash.
- **Clasificación con el modelo v10:**
  - **A (autoría):** independiente **declarada**; mi id no figura en ningún rol; no produje ni modifiqué lo revisado.
  - **B (aislamiento):** `I1_CONTEXTO_SEPARADO` declarado, en el límite: contexto nuevo sin historial ni memoria del autor, pero el encargo no contiene solo referencias (OB-4). No llego a I2 porque puedo escribir.
  - **C (trazabilidad):** `G0_DECLARADA`: sin evidencia `identity`/`isolation`/`execution` fijada ni verificación de un tercero.
- Con la matriz propuesta, este informe **no alcanzaría** el mínimo de un Gate 1 formal de GOV-001 (HIGH: I1·G1·`identity`). Es un dictamen técnico sobre el plan, no un Gate de `mission.json`.
