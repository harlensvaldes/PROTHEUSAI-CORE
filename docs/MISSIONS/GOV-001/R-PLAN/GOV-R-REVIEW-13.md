# GOV-001 · Revisión Quality del plan v13 (cierre de GR-40 y OB-13..OB-17), ciclo 13

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r13
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) me asignó este nombre al lanzarme como subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento ni hay firma u otro mecanismo que lo acredite.
**Independencia verificada:** no — la autoría independiente es solo declarada: no redacté v1–v13 ni GOV-R-REVIEW-01..12 y no implementaré la misión. Comparto runtime, sesión anfitriona, usuario SO (`fayat\cvaldes`), workspace y credenciales con el autor, y el encargo lo redactó el autor. Clasificación con el modelo v13 al final: A declarada · I1 (con resumen no contrastable declarado) · G0.
**Artefacto revisado:** GOV-001-R-PLAN-v13.md sha256:6b05bb3005223672bb0caaf57a9f97eadfc37feebac2800fdea7f413429b324a
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v13 contra v12 (diff palabra a palabra con `git diff --no-index --word-diff=plain`), v8 (v8:49, 57, 59, 139) y `GOV-R-REVIEW-12.md`; `AGENTS.md` y `agents/quality.md` de PROTHEUSAI-CORE `6e5e929`; listado de `docs/MISSIONS/GOV-001` y `EXAMPLE-001`, `POST-GATE-VALIDATION.md` y `GATE2-INPUT-03.sha256`; inspección de solo lectura (ACL con `Get-Acl`, búsqueda con `Select-String`) de la carpeta de estado de la sesión. Ejecuté la suite y `validate` en solo lectura con `python -B`. No hice prototipo de la CLI v3.

> PASS_WITH_RESERVATIONS **no habilita avanzar**. v13 no puede citarse como plan aprobado en `OWNER-DECISION-02` ni someterse a D1–D4 como cerrado mientras no se corrijan GR-41 y GR-42 (ambos LOW) y se pase un nuevo ciclo.
>
> **Criterio de dictamen.** No es FAIL: GR-40 queda cerrado en su núcleo (hay un ancla externa y el riesgo residual ya formula una condición necesaria, no suficiente), OB-13..OB-17 están cerrados, el modelo A/B/C sigue siendo fiel a la decisión del Owner y no hay sobrealcance. No es PASS por dos defectos reales, cada uno corregible con una o dos líneas:
> - **GR-41.** La nueva frontera de garantía («fuera del workspace») no es la frontera real cuando el revisor I1 comparte el usuario SO. Lo acredito con evidencia nueva (ACL). Es el mismo tipo de defecto que GR-40: una garantía no acreditada en el punto que el Owner pidió no sobrestimar, en el único control que justifica I1 en Gate 2 hasta HIGH.
> - **GR-42.** La frase nueva «cualquier otro cambio reabre Gate 2» contradice el propio plan, porque la matriz exige evidencias y registros del manifiesto que solo existen después de fijar la entrada. Es una regresión v12→v13: un implementador que la copie literalmente en el protocolo produciría una regla que no se puede cumplir.
>
> Lo editorial u opcional figura en Observaciones y no condiciona el dictamen. El dictamen se limita al hash indicado.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash de v13 | `hashlib.sha256(bytes)` y `sha256(bytes.replace(b'\r\n',b'\n'))` | `6b05bb30…324a` y `sha256_lf 324b669d…02f1` (25 349 bytes). **Coinciden** con el encargo |
| v12, REVIEW-12, v8 | mismo cálculo | sha256_lf de v12 `5e59a4c9…e255` ✓; REVIEW-12 `847b70dd…e621` ✓; v8 `0d6bcca0…2a93` ✓ |
| Repo | `git log -1`; `git status --porcelain --untracked-files=all --ignored` | `6e5e929…f467`; 0 líneas antes y después |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 (Python 3.12.0) |
| Validación | `python -B scripts\quality_cli.py validate` | `OK — estructura consistente…`, exit 0 |
| Decisión del Owner de 09:53 | `files\`, repo | Sin registro escrito. Solo existe la paráfrasis del encargo (v13:8 lo reconoce) |

## Estado de hallazgos previos (REVIEW-12)
| ID | Estado | Evidencia |
|---|---|---|
| GR-40 | **CERRADO en lo señalado → GR-41** | Aplica la opción (a) de REVIEW-12. **Ancla:** el Orchestrator calcula el `sha256_lf` de la entrada antes del encargo y lo incluye en la instrucción (v13:89). **Comparación:** el paso 2 comprueba que el hash citado por el revisor coincide con el de la instrucción (v13:91). Como la CLI recalcula `artifact` contra el archivo con `path` (v13:75, 130, 138), por transitividad la entrada presente es la que se encargó. Con ello cierran tres vías: alterar solo el árbol, alterar el árbol y la entrada citando el hash nuevo, o crear otra entrada. **Riesgo residual:** ya no sugiere que ejecutar los pasos baste; formula una condición necesaria («se detecta **solo** si…», v13:96-99). Quedan dos lagunas (GR-41): el ancla «fuera del workspace» no queda fuera del alcance de un I1 con el mismo usuario SO, y no se indica de dónde obtiene el valor del ancla quien revisa en el paso 3. |
| OB-13 | CERRADA | v13:66 añade «**no aceptada**» y «Las misiones aceptadas no se reabren». v13:72 renombra el AVISO a «no cumple la matriz vigente» y declara que no se distingue entre «ya no cumple» y «nunca cumplió». |
| OB-14 | CERRADA | v13:71 añade R7 (orden de Gates y «owner APPROVED exige tres PASS»). El rol no vacío y `effective_authors` ⊆ rol están incluidos en A según la tabla de §1 (v13:31). |
| OB-15 | CERRADA (→ GR-42 por el texto nuevo) | v13:91: el sufijo de `POST-GATE-VALIDATION-<sufijo>` es `R01`/`R03` en GOV-001, coherente con v8:49 y v8:59. v13:94: las adiciones permitidas recuperan la excepción de v8:139. La frase final que se añade («Cualquier otro cambio reabre Gate 2») es una regla nueva y origina GR-42. |
| OB-16 | CERRADA | v13:243 declara la consecuencia de exigir I2. |
| OB-17 | CERRADA | v13:69, coherente con la prueba de v13:234 (`validate` 0 con AVISO y `can-close` 1). |

No reabro GR-24..GR-39 ni O-1..O-8 ni OB-1..OB-12: no hay evidencia nueva y v13 no modifica sus líneas.

## Regresiones v12→v13
El diff solo contiene adiciones o sustituciones trazables a GR-40 y OB-13..OB-17, además de los cambios de versión (v13:1, 3-5, 14, 247). No hay cambios en §1 (salvo contexto), §3, §4, §6, §7 ni §8. La única regresión es la frase final de v13:94 (GR-42).

## Hallazgos nuevos

### GR-41 · LOW · El ancla de GR-40 se sitúa «fuera del workspace», pero con I1 y el mismo usuario SO ese registro también es escribible, y el paso 3 no tiene fuente para el ancla
**Evidencia:**
- v13:43: I1 «puede compartir runtime, usuario del sistema, workspace y credenciales».
- v13:89: el hash se incluye en la instrucción. «Así queda en el registro del runtime o de la conversación, fuera del workspace.»
- v13:96-97 traza la frontera de garantía en el workspace: «nada **dentro** del workspace es inalterable… se detecta **solo** si… se compara con el registrado en la instrucción, fuera del workspace».
- **Evidencia nueva (solo lectura):**
  - En este runtime, el registro de la conversación es `…\.copilot\session-state\e5be03ee-…\events.jsonl`.
  - Contiene la instrucción de este ciclo: 11 líneas con el `sha256_lf` de v13 (`Select-String -SimpleMatch`).
  - Su ACL concede `FullControl` a `FAYAT\cvaldes` (`Get-Acl`), que es el usuario con el que me ejecuto (`whoami`).
  - Este mismo informe lo escribo en esa carpeta de sesión.
  - Es decir, un revisor I1 del caso típico (v13:43, «agentes separados de LUNA o Cline en un mismo entorno») puede escribir en el registro persistido que el plan presenta como ancla externa.
- v13:92 (paso 3): quien revisa la comparación (revisor de Gate 3, Quality u Owner) no tiene, según el plan, ninguna fuente para el valor de la instrucción. Un revisor I1 de Gate 3 no recibe el historial del Orchestrator (v13:43). En la práctica, solo podría leer lo que el Orchestrator anote en `POST-GATE-VALIDATION-*` (dentro del workspace) o el `events.jsonl` (escribible), y el plan no lo declara.

**Impacto:**
- El ancla sí es fiable si el Orchestrator compara contra su propia copia viva (su contexto o el mensaje que ve el Owner).
- No lo es si compara contra el registro persistido, por ejemplo al reanudar o compactar la sesión. Tampoco cuando quien revisa en el paso 3 lo lee de disco.
- El Owner decidiría D2/D3 creyendo que el límite está en el workspace, cuando el límite real es el alcance de escritura del usuario SO compartido. Es el mismo tipo de sobrestimación que GR-40, y el Owner pidió expresamente no afirmar aislamiento inexistente.
- No invalida la elección de I1: la amenaza residual exige una manipulación deliberada y coordinada de tres puntos (árbol, entrada y registro del runtime). Pero debe declararse.

**Corrección mínima (elegir una y declararla):**
- **(a) Precisar la fuente y el límite (recomendada, dos líneas).**
  - Paso 2: el Orchestrator compara contra el valor que **él** envió (su contexto o el mensaje visible para el Owner), no contra un archivo, y lo anota en `POST-GATE-VALIDATION-<sufijo>` junto con su origen.
  - Riesgo residual: «fuera del workspace» se sustituye por «fuera del alcance de escritura del revisor». Se añade que, con el usuario SO compartido, el registro persistido del runtime también es escribible por un I1. Por tanto, en el paso 3 el valor anotado es una declaración del Orchestrator, salvo que quien revisa pueda contrastarlo con el mensaje original. El Owner sí puede hacerlo.
- **(b) Solo declarar.** Añadir al riesgo residual que, con el mismo usuario SO, el ancla solo resiste mientras se use la copia viva del Orchestrator. Someterlo así en D2/D3.

### GR-42 · LOW · «Cualquier otro cambio reabre Gate 2» contradice registros que el propio plan exige después de fijar la entrada
**Evidencia:**
- v13:94 (texto nuevo): «Adiciones permitidas tras los Gates: los informes originales…, `POST-GATE-VALIDATION-*` y las citas de hash. Cualquier otro cambio reabre Gate 2.»
- v13:91: el paso 2 compara **cada archivo comiteado** con la entrada fijada **antes** de la revisión (v13:88).
- Registros que el plan exige y que solo pueden existir después de fijar la entrada, todos dentro de la misión:
  - Las **evidencias tipadas** (v13:49-52, con `path` canónico y `sha256_lf` recalculado): `identity` para Gate 2 y Gate 3 en HIGH, y `execution` para Gate 3 desde MEDIUM (v13:78-83, 102). La de Gate 3 recoge salidas de una ejecución posterior a Gate 2.
  - Los **registros por Gate de `mission.json`**: `decision` y `review {file, sha256_lf, reviewer_verification}`, este último escrito por un tercero (v13:59, §8 F2).
- Esos registros no son «informes», ni `POST-GATE-VALIDATION-*`, ni (salvo `review.sha256_lf`) «citas de hash».
- v8:139 tenía la misma lista, pero sin la consecuencia y sin evidencias tipadas, que v8 no contemplaba. El precedente de GOV-001 no lo cubre: `POST-GATE-VALIDATION.md:11` registra que `mission.json` no cambió porque los Gates seguían en PENDING.

**Impacto:** leída literalmente, cualquier misión MEDIUM o superior que cumpla la matriz reabre Gate 2 en el paso 2, porque sus evidencias de Gate 3 y sus decisiones en el manifiesto no están en la entrada. La regla se incorpora a `QUALITY_EVIDENCE_PROTOCOL.md` § Gate 2 y a `GATE2_REVIEW.md` (v13:87, §8), así que el implementador tendría que inventar la excepción. No afecta a la CLI.

**Corrección mínima:** ampliar la lista de v13:94 a «informes originales, evidencias tipadas citadas en los bloques, los campos `decision` y `review` de `mission.json` (y `owner_acceptance`), `POST-GATE-VALIDATION-*` y citas de hash». Alternativa: sustituir la lista por un criterio, «solo pueden diferir archivos de registro de Gate; cualquier cambio en lo revisado reabre Gate 2».

## Valoraciones solicitadas
- **Autoría, aislamiento y garantía:** siguen separados (v13:31-33). Compartir runtime, usuario SO o workspace no anula A (v13:43). B se declara siempre. GR-41 afecta a la garantía de un control de Gate 2, no al modelo.
- **Nunca autoaprobación:** A es absoluta en PASS/PWR (v13:36) y se mantiene en `validate` para misiones aceptadas, junto con R7 y R8 (v13:71).
- **Proporcionalidad por Gate:** sin cambios. Es razonada, con las salvedades de GR-41 y GR-42.
- **schema_version, hashes normalizados frente a bytes y redundancia:** sin cambios respecto de v12, ya valorados como correctos.
- **Sobrealcance:** ninguno. R02 sigue en GOV-002 (§6). Las adiciones de v13 son documentales.

## Observaciones (no condicionan el dictamen)
El criterio para tratarlas como observaciones es que son mejoras de redacción o completitud: una lectura razonable, apoyada en otra parte del plan, las resuelve sin inventar reglas.
- **OB-18.** El paso 2 (v13:91) compara «el hash citado». En la variante `git:` (v13:90), lo citado es un commit. Conviene escribir «la referencia citada (hash o commit) coincide con la de la instrucción», como proponía la opción (a) de GR-40. Con `git:` lo revisado ya está comiteado, así que la amenaza es menor, aunque un revisor podría citar otro commit.
- **OB-19.** «Sustituyendo las plantillas 04/05» (v13:94) se refiere a `04-GATE2-REVIEW.md` y `05-GATE3-EVIDENCE.md` de GOV-001. En un procedimiento general convendría decir «los informes referenciados por `review.file`».
- **OB-20.** La numeración `GATE2-INPUT-<n>` (v13:88) y `GATE2-INPUT-0N` (v13:75) es la misma convención con dos notaciones. Es editorial.

## Qué NO verifiqué
- El texto literal de la decisión del Owner de 09:53: solo dispongo de la paráfrasis del encargo, redactada por el autor.
- Ninguna implementación v3: no hay prototipo y no medí la estimación de líneas.
- Que exista un registro de lanzamiento utilizable como evidencia `identity` en este runtime, y las propiedades reales de LUNA o Cline. La evidencia de GR-41 procede solo de este runtime (Copilot CLI en Windows); por la definición de I1 (v13:43), lo extrapolo a otros runtimes con el mismo usuario SO, sin haberlo comprobado en ellos.
- No modifiqué `events.jsonl` para demostrar la escritura. Me baso en la ACL y en que escribo este informe en la misma carpeta.
- La existencia de proyectos derivados con manifiestos v2 decididos o con `controls.json` v1.
- La identidad de ningún participante.
- Los pasos de R01 (aprobado, fuera de alcance).
- GR-41 y GR-42 son análisis estáticos de procedimientos documentales. No los reproduje con un escenario en `%TEMP%`.

**Archivos temporales:** ninguno creado en `%TEMP%`. La suite usa `TemporaryDirectory`, que se autoelimina. El repositorio no cambió: 0 líneas de `git status --porcelain --untracked-files=all --ignored` antes y después. Mi única escritura es este informe.

## Limitación de independencia
- Soy un subagente lanzado por el autor (copilot-sdk-main) en el mismo runtime, sesión anfitriona, usuario SO, workspace y credenciales.
- Tengo permiso técnico de escritura sobre el artefacto revisado, el repositorio y el registro de la conversación (GR-41). Me abstuve de usarlo, pero eso no es verificable.
- **Clasificación con el modelo v13:**
  - **A (autoría):** independiente **declarada**. Mi id no figura en ningún rol y no produje ni modifiqué lo revisado.
  - **B (aislamiento):** `I1_CONTEXTO_SEPARADO` declarado: contexto nuevo, sin historial ni memoria del autor. Según la frontera OB-4 (v13:44), declaro que el encargo incluye un resumen del autor sobre la decisión del Owner de 09:53 que **no puede contrastarse** con ninguna fuente escrita. Las demás referencias van con hash y las contrasté. No llego a I2 porque puedo escribir.
  - **C (trazabilidad):** `G0_DECLARADA`. No hay evidencia `identity`/`isolation`/`execution` fijada ni verificación de un tercero.
- Con la matriz propuesta, este informe **no alcanzaría** el mínimo de un Gate 1 formal de GOV-001 (HIGH: I1·G1{identity}). Es un dictamen técnico sobre el plan, no un Gate de `mission.json`.
