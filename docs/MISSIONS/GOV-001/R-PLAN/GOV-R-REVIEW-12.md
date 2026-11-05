# GOV-001 · Revisión Quality del plan v12 (GOV-R03 rediseñado, GOV-R02 a GOV-002), ciclo 12

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r12
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) me asignó este nombre al lanzarme como subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento ni hay firma u otro mecanismo que lo acredite.
**Independencia verificada:** no — la autoría independiente es solo declarada: no redacté v1–v12 ni GOV-R-REVIEW-01..11 y no implementaré la misión. Comparto runtime, sesión anfitriona, usuario SO, workspace y credenciales con el autor, y el encargo lo redactó el autor. Clasificación v12 al final: A declarada · I1 (con resumen no contrastable declarado) · G0.
**Artefacto revisado:** GOV-001-R-PLAN-v12.md sha256:ed64eba028be9cde17e1a5fb5e0705890488b3d62e7881f68e21f1b4634af7e8
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v12 contra:
- v11 (diff palabra a palabra con `git diff --no-index --word-diff=plain`), v8 (prelación y GR-19/GR-23/R01) y `GOV-R-REVIEW-11.md`;
- `AGENTS.md` y `agents/quality.md`;
- PROTHEUSAI-CORE `6e5e929`: `scripts/quality_cli.py` (`v2_errors`, `main`), `tests/test_governance.py`, `docs/QUALITY_EVIDENCE_PROTOCOL.md`, `docs/MISSIONS/README.md`, `README.md`, y grep de `can-close`, `GATE2-INPUT` y `POST-GATE` en el repositorio;
- `GOV-001-PROPOSAL-v8.md` (definición de R1–R8).

Ejecuté la suite y `validate` en solo lectura con `python -B`. No hice prototipo de la CLI v3.

> PASS_WITH_RESERVATIONS **no habilita avanzar**. v12 no puede citarse como plan aprobado en `OWNER-DECISION-02` ni someterse a D1–D4 como cerrado mientras no se corrija GR-40 (LOW) y se pase un nuevo ciclo.
>
> **Criterio de dictamen.** No es FAIL: GR-37..GR-39 y OB-7..OB-12 están cerrados, el modelo A/B/C sigue siendo fiel a la decisión del Owner y no hay regresiones. No es PASS por GR-40: la mitigación general de Gate 2, que es lo que justifica I1 hasta HIGH, no vincula la entrada que fija el Orchestrator con la que cita el revisor. Además, el riesgo residual declarado da a entender que, si se ejecutan los pasos, la alteración se detecta, y eso no es cierto frente a un revisor I1 con escritura. Es una garantía no acreditada en el punto que el Owner pidió no sobrestimar, no una cuestión de redacción. Se corrige con una o dos líneas, sin rediseño. Lo editorial u opcional figura en Observaciones y no condiciona el dictamen. El dictamen se limita al hash indicado.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash de v12 | `hashlib.sha256(bytes)` y `sha256(bytes.replace(b'\r\n',b'\n'))` | `ed64eba0…af7e8` y `sha256_lf 5e59a4c9…e1e255` (23 790 bytes, CRLF). **Coinciden** con el encargo |
| v11, REVIEW-11, v8 | mismo cálculo | sha256_lf de v11 `66cc6a26…efe968` ✓; REVIEW-11 `c33f835b…0d62` ✓; v8 `0d6bcca0…2a93` ✓ |
| Repo | `git log -1`; `git status --porcelain --untracked-files=all --ignored` | `6e5e929`; 0 líneas antes y después |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 (Python 3.12.0) |
| Validación | `python -B scripts\quality_cli.py validate` | `OK — estructura consistente…`, exit 0 |
| Decisión del Owner de 09:53 | `files\`, repo | Sin registro escrito. Solo existe la paráfrasis del encargo (v12:8 lo reconoce) |

## Estado de hallazgos previos (REVIEW-11)
| ID | Estado | Evidencia |
|---|---|---|
| GR-37 | **CERRADO en lo señalado → GR-40** | Combina las opciones (a), (b) y (c) de REVIEW-11. **(a)** El procedimiento ya es general para MEDIUM y superiores (v12:84-87) y se incorpora al protocolo § Gate 2 y a `GATE2_REVIEW.md` (v12:191, 195). Hoy no existe: el grep de `GATE2-INPUT\|POST-GATE` en `docs/QUALITY_EVIDENCE_PROTOCOL.md`, `docs/templates`, `docs/MISSIONS/README.md` y `quality/` da 0 coincidencias. **(b)** El riesgo residual se declara (v12:89). **(c)** La variante I2 en Gate 2 HIGH pasa a D3 (v12:230). Queda una laguna en el vínculo entre la entrada fijada y la citada, y en la exactitud del riesgo residual (GR-40). |
| GR-38 | **CERRADO** | `reviewer_verification` `{id, by, method, ref, date}` con `canon(id)` = `reviewer` (v12:59). Las claves exactas de `review` quedan en F2 (v12:159). Se añaden las negativas «de otro revisor» y «claves extra» (v12:221). Si se sustituye un informe por el de otro revisor, falla `id` ≠ `reviewer`. |
| GR-39 | **CERRADO** (opción propia, coherente) | v12:67-70: las transiciones aplican siempre la matriz vigente; `validate` aplica los mínimos solo a misiones no aceptadas y, para las aceptadas, emite un AVISO. Es coherente con el código real: `can-close` exige `owner_acceptance` APPROVED (`quality_cli.py:389-390`), así que reevaluar en `can-close` impide obtener el cierre por debajo de la matriz. La prueba está en v12:222. Hay matices de redacción en OB-13 y OB-14. |
| OB-7 | CERRADA | v12:176 («se pierden todas…, entre ellas… orden de Gates, owner APPROVED sin tres PASS y R8 de v2»). |
| OB-8 | CERRADA | v12:220. |
| OB-9 | CERRADA | v12:127. |
| OB-10 | CERRADA | v12:150. |
| OB-11 | CERRADA | v12:64. |
| OB-12 | CERRADA | v12:197. |

No reabro GR-24..GR-36 ni O-1..O-8: no hay evidencia nueva y v12 no modifica sus líneas.

## Regresiones v11→v12
El diff solo contiene adiciones o sustituciones trazables a GR-37..39 y OB-7..12, además de los cambios de versión (v12:1, 3-5, 14, 233). No encontré regresiones funcionales ni contradicciones bloqueantes. La única fricción de redacción entre la nueva v12:67-70 y la v12:66 previa figura en OB-13.

## Hallazgos nuevos

### GR-40 · LOW · El procedimiento general de Gate 2 no vincula la entrada fijada por el Orchestrator con la que cita el revisor, y el riesgo residual sobrestima la detección
**Evidencia:**
- v12:84 identifica la amenaza: «el riesgo es que el revisor altere lo revisado». Con I1, el revisor puede escribir en el árbol **y** en la carpeta de la misión (v12:43, «Puede compartir runtime, usuario del sistema, workspace y credenciales»).
- v12:85 (paso 1): el Orchestrator fija `GATE2-INPUT-<n>.sha256` **en la misión** y «el revisor la cita en `artifact`». El Orchestrator no registra el `sha256_lf` de la entrada fuera del alcance del revisor, y nadie compara ese valor con `artifact.ref`.
- v12:86 (paso 2): se compara el commit «con la entrada», es decir, con el archivo presente en la misión en ese momento.
- La CLI recalcula `artifact` contra el `sha256_lf` **que cita el propio revisor** (v12:72, 126). La regla append-only es documental y la CLI no la impone (`v8:37`).
- La línea de protocolo de R01, ya aprobada (`v8:37`), presupone «un hash registrado antes de la pérdida» para las entradas. El procedimiento general no dice dónde ni cuándo se registra ese hash.
- Con `git:` (v12:73, 85), lo citado es declarado (v12:127) y el procedimiento tampoco exige comprobar que coincide con lo fijado.
- v12:89: «Si no se ejecutan [los pasos 2 y 3], una modificación hecha por un revisor I1… no se detecta». La frase da a entender lo contrario si se ejecutan.

**Impacto:** un revisor I1 que modifique un archivo y regenere o edite de forma coherente `GATE2-INPUT-<n>` (y cite su nuevo hash) supera la CLI, el paso 2 (commit = entrada alterada) y el paso 3 (la comparación es coherente). El procedimiento solo detecta alteraciones **no coordinadas** con la entrada, como un error accidental. Ese es precisamente el caso adversarial que justifica distinguir I1 de I2 en Gate 2 (v12:84, 89, 230). El plan presenta como condición suficiente de I1 hasta HIGH un control que no cubre la amenaza declarada. Afecta a D2 y D3.

**Corrección mínima (elegir una y declararla):**
- **(a) Anclar.** Paso 1: el Orchestrator comunica el `sha256_lf` de la entrada en el encargo al revisor (como ya pide `AGENTS.md` § Comunicación) y lo registra por adición. Paso 3: quien revisa la comparación comprueba que el `artifact.ref` del informe de Gate 2 es igual a ese valor (o que `git:` coincide con el commit fijado), y el paso 2 compara contra la entrada con ese hash. Riesgo residual: con I1, el registro dentro de la misión también es escribible, así que la referencia fiable es la del encargo o mensaje, no la del repositorio.
- **(b) Solo declarar.** Reescribir v12:89: con I1, el procedimiento solo detecta alteraciones no coordinadas con la entrada. Una alteración coherente de árbol y entrada solo la excluye I2. Someterlo así al Owner en D2/D3.

La opción (a) es una línea más en el paso 1 y otra en el paso 3, sin código nuevo.

## Valoraciones solicitadas
- **Autoría, aislamiento y garantía:** siguen bien separadas (v12:31-33). Compartir runtime, usuario SO o workspace no anula A (v12:43). B siempre se declara.
- **Nunca autoaprobación:** A es absoluta en PASS/PWR (v12:36) y se mantiene también para misiones aceptadas en `validate` (v12:69). R8 se conserva.
- **Proporcionalidad:** Gate 1 y Gate 3 están razonados. Gate 2 ya es general, con la salvedad de GR-40.
- **schema_version, hashes normalizados frente a bytes y redundancia:** sin cambios respecto de v11, que ya fueron valorados como correctos. `git:` queda ahora clasificado como declarado (v12:127).
- **Sobrealcance:** no lo hay. GOV-R02 queda como investigación (§6) y GOV-001 no se amplía. Generalizar el procedimiento de Gate 2 es documental y respondía a una de las correcciones que planteaba GR-37.

## Observaciones (no condicionan el dictamen)
Son mejoras de redacción o completitud. Un implementador no tendría que inventar reglas, porque otra parte del plan o del código vigente las resuelve.
- **OB-13.** v12:66 («cambiar `independence_minimums`… después de su Gate 1 reabre Gate 1») no se restringe a misiones no aceptadas, mientras que v12:67-70 dice que las aceptadas no se reescriben. Prevalece la regla específica de v12:67-70, pero conviene añadir «de una misión no aceptada» en v12:66. Además, el AVISO de v12:69 («ya no cumplen») no distingue entre «ya no cumple» y «nunca cumplió», salvo que se registre la matriz aplicada (opción (b) de REVIEW-11).
- **OB-14.** La lista de v12:69 para misiones aceptadas («hashes, igualdades, A, R8») omite R7 (orden de Gates y «owner APPROVED exige tres PASS», `GOV-001-PROPOSAL-v8.md:64`; hoy `quality_cli.py:270-272`). No condiciona porque v12:186 conserva el orden de Gates y la prueba vigente `test_governance.py:297-299` («owner APPROVED sin tres Gates PASS») no está entre las que se sustituyen. Conviene escribir «todas las reglas salvo los mínimos B/C y de artefacto fijado».
- **OB-15.** En v12:86, «compara cada archivo comiteado con la entrada» no recoge la excepción de `v8:139` («solo pueden diferir las adiciones permitidas tras los Gates: informes, citas y validación posterior»). Leído literalmente, siempre habría diferencias. Los sufijos `<n>` de `POST-GATE-VALIDATION-<n>` frente a `-R01`/`-R03` y `GATE2-INPUT-<n>` frente a `-0N` (v12:72) son editoriales. `docs/MISSIONS/README.md` podría remitir al procedimiento de Gate 2, aunque basta con el protocolo.
- **OB-16.** D3 (v12:230) ofrece la variante I2 en Gate 2 desde HIGH, pero no indica su consecuencia, que REVIEW-11 sí señalaba: hoy no hay acreditados permisos de solo lectura en LUNA ni en Cline. Por eso, un revisor I1 no podría declarar I2 con veracidad, y el cierre de GOV-001 (§7) quedaría pendiente de disponer de ese revisor. Se deduce de v12:45 y no altera la implementación.
- **OB-17.** Con v12:67-70, endurecer la matriz hace que `can-close` devuelva 1 de forma permanente en misiones ya cerradas, salvo que se revaliden. Hoy solo lo consume la documentación (`README.md:67`), así que no tiene efecto práctico. Convendría declararlo como consecuencia en D3.

## Qué NO verifiqué
- El texto literal de la decisión del Owner de 09:53: solo dispongo de la paráfrasis del encargo, redactada por el autor.
- Ninguna implementación v3: no hay prototipo y no medí la estimación de líneas (v12:188).
- Que exista un registro de lanzamiento utilizable como evidencia `identity` en este runtime, y las propiedades reales de LUNA o Cline.
- La existencia de proyectos derivados con manifiestos v2 decididos o con `controls.json` v1.
- La identidad de ningún participante.
- Los pasos de R01 (aprobado, fuera de alcance).
- GR-40 es un análisis estático del procedimiento. No lo reproduje con un escenario en `%TEMP%`, porque es un control procedimental, no código.

**Archivos temporales:** ninguno creado por mí en `%TEMP%`. La suite usa `TemporaryDirectory`, que se autoelimina. El repositorio no cambió: 0 líneas de `git status --porcelain --untracked-files=all --ignored` antes y después. Mi única escritura es este informe.

## Limitación de independencia
- Soy un subagente lanzado por el autor (copilot-sdk-main) en el mismo runtime, sesión anfitriona, usuario SO, workspace y credenciales. Tengo permiso técnico de escritura sobre el artefacto revisado y sobre el repositorio. Me abstuve de usarlo, pero eso no es verificable. Esa misma capacidad es la que describe GR-40.
- **Clasificación con el modelo v12:**
  - **A (autoría):** independiente **declarada**. Mi id no figura en ningún rol y no produje ni modifiqué lo revisado.
  - **B (aislamiento):** `I1_CONTEXTO_SEPARADO` declarado: contexto nuevo, sin historial ni memoria del autor. Según la frontera OB-4 (v12:44), declaro que el encargo incluye un resumen del autor sobre la decisión del Owner de 09:53 que **no puede contrastarse** con ninguna fuente escrita. Las demás referencias van con hash y las contrasté. No llego a I2 porque puedo escribir.
  - **C (trazabilidad):** `G0_DECLARADA`. No hay evidencia `identity`/`isolation`/`execution` fijada ni verificación de un tercero.
- Con la matriz propuesta, este informe **no alcanzaría** el mínimo de un Gate 1 formal de GOV-001 (HIGH: I1·G1{identity}). Es un dictamen técnico sobre el plan, no un Gate de `mission.json`.
