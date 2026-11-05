# GOV-001 · Revisión Quality del plan v14 (cierre de GR-41, GR-42 y OB-18..OB-20), ciclo 14

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r14
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) me asignó este nombre al lanzarme como subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No hay registro de lanzamiento accesible como evidencia, ni firma ni otro mecanismo que lo acredite.
**Independencia verificada:** no — la autoría independiente es solo declarada: no redacté v1–v14 ni GOV-R-REVIEW-01..13 y no implementaré la misión. Comparto runtime, sesión anfitriona, usuario SO (`fayat\cvaldes`), workspace y credenciales con el autor, y el encargo lo redactó el autor. Clasificación con el modelo v14 al final: A declarada · I1 (con resumen no contrastable declarado) · G0.
**Artefacto revisado:** GOV-001-R-PLAN-v14.md sha256:b759b345f0fbfcb22e5897d9cdf44c1688539ac43f4d897b85104693ed5350d2
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v14 frente a v13 (`git diff --no-index --word-diff=plain`), v8 y `GOV-R-REVIEW-13.md`; lectura de `AGENTS.md` y `agents/quality.md` de PROTHEUSAI-CORE `6e5e929`; lectura de `docs/MISSIONS/GOV-001/GATE2-INPUT-03.sha256` y `POST-GATE-VALIDATION.md` como precedente. Inspección de solo lectura del registro de la sesión: ACL con `Get-Acl`, recuento con `Select-String` y recuento de eventos por campo `type`, sin leer su contenido. Ejecuté la suite y `validate` en solo lectura con `python -B`. No hice prototipo de la CLI v3.

> PASS_WITH_RESERVATIONS **no habilita avanzar**. v14 no puede citarse como plan aprobado en `OWNER-DECISION-02` ni someterse a D1–D4 como cerrado mientras no se corrijan GR-43 y GR-44 (ambos LOW) y se pase un nuevo ciclo.
>
> **Criterio de dictamen.** No es FAIL por cuatro razones:
> - GR-41 queda cerrado en lo que señalaba: v14 ya no sitúa la garantía «fuera del workspace» y declara que el registro de mensajes es escribible.
> - El núcleo de GR-42 está corregido: las evidencias tipadas y los registros de Gate ya no reabren Gate 2.
> - OB-18..OB-20 están cerrados.
> - El modelo A/B/C, la matriz, `schema_version`, los hashes y §6 no cambian, y no hay sobrealcance.
>
> No es PASS porque quedan dos defectos reales. Cada uno se corrige con una o dos líneas:
> - **GR-43 (regresión v13→v14).** La nueva regla de reapertura deja fuera los cambios en archivos versionados que no figuran en la entrada. Además, como el plan no la exceptúa, la propia aceptación del Owner reabriría Gate 2.
> - **GR-44.** El paso 3 nuevo obliga a leer el registro de mensajes del runtime sin dar alternativa. Si lo hace el revisor de Gate 3, que es I1, ese registro le expone el historial del autor, lo que contradice la definición de I1 (v14:43).
>
> Lo editorial figura en Observaciones y no condiciona el dictamen. El dictamen se limita al hash indicado.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash de v14 | `sha256(bytes)` y `sha256(bytes.replace(b'\r\n',b'\n'))` | `b759b345…50d2` y `sha256_lf 50c1d66a…f728606` (26 232 bytes). **Coinciden** con el encargo |
| v13, REVIEW-13, v8 | mismo cálculo | sha256_lf: v13 `324b669d…02f1` ✓; REVIEW-13 `d2ffd695…3e62` ✓; v8 `0d6bcca0…2a93` ✓. La cabecera de v14 (v14:4-5) cita los mismos valores |
| Repo | `git log -1`; `git status --porcelain --untracked-files=all --ignored` | `6e5e929…f467`; 0 líneas antes y después |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 |
| Validación | `python -B scripts\quality_cli.py validate` | `OK — estructura consistente…`, exit 0 |
| Decisión del Owner de 09:53 | `files\`, repo | Sin registro escrito. Solo dispongo de la paráfrasis del encargo, que v14:8 reconoce |

## Estado de hallazgos previos (REVIEW-13)
| ID | Estado | Evidencia |
|---|---|---|
| GR-41 | **CERRADO en lo señalado → GR-44** | **Frontera.** v14:89 sustituye «fuera del workspace» por «fuera del árbol revisado», que es exacto. v14:90 declara que el registro «no es inalterable» y que puede ser escribible si se comparte usuario SO, con el ejemplo de `events.jsonl`. **Riesgo residual.** v14:104 incluye el registro entre lo que el revisor puede alterar y mantiene la «condición necesaria, no suficiente». Con ello deja de sobrestimar el aislamiento. **Fuente del ancla.** v14:93 declara de dónde se toma en el paso 3. Así se cierra la segunda laguna, pero la fuente elegida origina GR-44. v14 combina las opciones (a) y (b) de REVIEW-13 y elige como fuente el registro persistido del runtime, en lugar de la copia viva del Orchestrator. Como el riesgo residual declara que ese registro es alterable, la elección es coherente. |
| GR-42 | **CERRADO en su núcleo → GR-43** | v14:95-100 amplía las adiciones permitidas. Incluye las evidencias tipadas de los Gates en curso y `decision` y `review` de `mission.json`; este último cubre `reviewer_verification`. También fija el periodo: «después de fijar la entrada». Las evidencias y registros de Gate que señalaba GR-42 ya no reabren Gate 2. **Sin cubrir:** falta `owner_acceptance`, que figuraba en la corrección propuesta. Además, la frase final nueva (v14:102) acota la reapertura de forma más estrecha que v13. Ambos puntos se tratan en GR-43. |
| OB-18 | CERRADA | v14:92: «la referencia del bloque del revisor coincide con la de la instrucción: el hash de la entrada o, en su caso, el `git:`». Queda un detalle editorial (OB-22). |
| OB-19 | CERRADA | v14:96: «los informes de revisión referenciados por `review.file` (en GOV-001, sustituyendo las plantillas 04/05)». |
| OB-20 | CERRADA en su alcance | v14:75 y v14:88 usan `GATE2-INPUT-<n>`, y v14:88 define `<n>` como dos dígitos. Ya no queda `0N` (búsqueda en v14). Al definir `<n>` aparece un efecto colateral editorial en otras líneas (OB-21). |

No reabro GR-24..GR-40, O-1..O-8 ni OB-1..OB-17: no hay evidencia nueva y v14 no modifica sus líneas.

## Regresiones v13→v14
El diff solo contiene cambios de versión (v14:1, 3-5, 14, 252) y las líneas 75, 88-104 y 106 de §2. Todo es trazable a GR-41, GR-42 y OB-18..OB-20. No cambian §1, §3, §4, §5, §6, §7 ni §8. La única regresión es la acotación de v14:102 (GR-43).

## Hallazgos nuevos

### GR-43 · LOW · La regla de reapertura de v14 deja sin consecuencia los cambios en archivos versionados no listados y reabre Gate 2 con la aceptación del Owner
**Evidencia:**
- v13 decía: «Cualquier otro cambio reabre Gate 2». v14:102 dice: «Cualquier otro cambio **en un archivo listado en la entrada**, o **un archivo nuevo** fuera de estas categorías, reabre Gate 2.»
- Primera laguna:
  - La entrada solo lista los archivos «modificado[s] o nuevo[s]» en el momento de fijarla (v14:88).
  - Si después se modifica o elimina un archivo versionado que **no** estaba en la entrada, ese archivo no está listado ni es nuevo, así que la regla no reabre Gate 2. Por ejemplo, `scripts/quality_cli.py` en una misión cuyo diff revisado solo tocaba documentación.
  - El paso 2 (v14:92) detectaría la discrepancia al comparar «cada archivo comiteado con la entrada», pero solo la «registra». La consecuencia la define únicamente v14:102.
  - Introducir código no revisado después de la revisión es el riesgo central de Gate 2 (v14:87).
- Segunda laguna:
  - El paso 3 ocurre «antes de la aceptación del Owner» (v14:93), así que la aceptación es posterior a fijar la entrada y al commit.
  - En el precedente `GOV-001/GATE2-INPUT-03.sha256`, la entrada lista `docs/MISSIONS/GOV-001/mission.json` y `06-DECISION.md`. Esto es lo esperable, porque D4 solo permite el commit después de Gate 2/3 (v14:252).
  - La aceptación del Owner escribe `owner_acceptance` en `mission.json` y la decisión en `06-DECISION.md`. Las adiciones permitidas solo cubren `decision` y `review` de cada Gate (v14:98).
  - Por tanto, si se lee literalmente, aceptar la misión reabre Gate 2, y §7 (v14:163-169) no podría completarse sin reabrirlo.
  - REVIEW-13 ya incluía `owner_acceptance` en la corrección mínima de GR-42.

**Impacto:** la regla pasa a `QUALITY_EVIDENCE_PROTOCOL.md` § Gate 2 y a `GATE2_REVIEW.md` (v14:87 y §8). Si el implementador la copia literalmente, el protocolo deja sin reapertura cambios no revisados y, a la vez, hace que la aceptación del Owner reabra Gate 2. No afecta a la CLI.

**Corrección mínima (una línea):** formular la regla sobre la diferencia con la entrada, no sobre el tipo de archivo:
- «Cualquier diferencia entre lo comiteado y la entrada (archivo modificado, nuevo o eliminado) que no pertenezca a estas categorías reabre Gate 2.»
- Añadir a la lista «el registro de aceptación del Owner (`owner_acceptance` y `06-DECISION.md`)».

### GR-44 · LOW · El paso 3 impone como única fuente el registro de mensajes del runtime: si lo usa el revisor I1 de Gate 3, ese registro le expone el historial del autor, y el plan no prevé alternativa
**Evidencia:**
- v14:93: el paso 3 se revisa «tomando el valor del ancla **directamente del registro de mensajes del runtime**, no de la copia del Orchestrator». Lo hace «el revisor de Gate 3 si el commit es anterior a Gate 3».
- v14:42-43: I0 es el revisor que «recibe el historial, la memoria o el contexto de trabajo del autor». I1 es una instancia «sin historial ni memoria del autor». La matriz exige I1 en Gate 3 en LOW, MEDIUM y HIGH (v14:80-82).
- Evidencia nueva de solo lectura en este runtime:
  - El registro de mensajes es `…\session-state\e5be03ee-…\events.jsonl`: 21 228 081 bytes y 7 229 eventos, de los que 572 son `assistant.message` y 795 `tool.execution_start` del autor/Orchestrator. Lo he contado solo por el campo `type`, sin leer el contenido.
  - Contiene 11 líneas con el `sha256_lf` de v14 (`Select-String -SimpleMatch`). Por tanto, localizar el ancla implica abrir el mismo registro que guarda el contexto de trabajo del autor.
- El plan no indica:
  - cómo extraer solo el mensaje de la instrucción;
  - qué hacer si quien revisa no tiene acceso a ese registro, por ejemplo un Quality humano, otro runtime o un registro que el runtime no persiste. Las propiedades de LUNA y Cline no están acreditadas (v14:248).

**Impacto:**
- Si se cumple literalmente, el revisor I1 de Gate 3 accede al contexto del autor antes o durante su dictamen. Su declaración I1 queda en entredicho y, por la frontera OB-4 (v14:44), debería declararlo.
- Si no tiene acceso al registro, el paso 3 no puede ejecutarse y no hay alternativa, cuando el Owner pidió un procedimiento portable y verificable.
- Esto no rebaja la garantía declarada: el riesgo residual sigue siendo correcto.

**Corrección mínima (elegir una y declararla):**
- **(a) Recomendada.** Asignar la lectura del registro a quien no emite un dictamen I1 de la misión: el Owner o Quality en la revisión de aceptación. El revisor de Gate 3 revisa la comparación registrada por el Orchestrator y la trata como declaración.
- **(b)** Permitir que el revisor de Gate 3 la haga, pero solo **después** de emitir su dictamen y extrayendo únicamente el mensaje de la instrucción. Si no tiene acceso, declara que el valor procede del Orchestrator.

## Valoraciones solicitadas
- **Autoría, aislamiento y garantía:** siguen separados (v14:31-33). Compartir runtime, usuario SO o workspace no anula A (v14:43). B se declara siempre. Desde v14, el plan ya no afirma que el ancla esté fuera del alcance de un I1 con el mismo usuario SO (v14:90 y 104).
- **Nunca autoaprobación:** A es absoluta en PASS/PWR (v14:36). R7 y R8 se mantienen en `validate` para misiones aceptadas (v14:71).
- **Proporcionalidad por Gate:** no cambia. Queda condicionada a GR-43 y GR-44, que afectan al procedimiento de Gate 2, no a la matriz.
- **schema_version, hashes normalizados frente a bytes y redundancia:** sin cambios desde v12; ya los valoré como correctos.
- **Sobrealcance:** ninguno. R02 sigue en GOV-002 (§6) y los cambios de v14 son documentales.

## Observaciones (no condicionan el dictamen)
Las trato como observaciones porque una lectura razonable, apoyada en otra parte del plan, las resuelve sin inventar reglas.
- **OB-21.** Al definir `<n>` como «dos dígitos» (v14:88), la notación queda ambigua:
  - v14:212 escribe `POST-GATE-VALIDATION-<n>`, mientras que v14:92 usa `<sufijo>` = `R01`/`R03`;
  - v14:59 usa `gates.<n>` para la clave de Gate.
  
  Conviene usar `<sufijo>` en :212 y `<gate>` en :59.
- **OB-22.** En la variante `git:`, v14:92 compara con «el `git:`» de la instrucción, pero v14:89 solo dice que la instrucción incluye el `sha256_lf` de la entrada. Falta decir que, en esa variante, la instrucción incluye el commit.

## Qué NO verifiqué
- El texto literal de la decisión del Owner de 09:53. Solo dispongo de la paráfrasis del encargo, redactada por el autor.
- Ninguna implementación v3: no hay prototipo y no medí la estimación de líneas.
- La existencia, persistencia y accesibilidad de un registro de mensajes en LUNA o en Cline. La evidencia de GR-44 procede solo de este runtime (Copilot CLI en Windows).
- El contenido de `events.jsonl`: solo conté eventos por `type` y coincidencias del hash, sin mostrar líneas. No comprobé si un filtrado permitiría extraer solo la instrucción.
- Un registro de lanzamiento utilizable como evidencia `identity`, y la identidad de cualquier participante.
- GR-43 y GR-44 son análisis estáticos de procedimientos documentales: no los reproduje con un escenario.
- R01, que está aprobado y fuera del alcance de esta revisión.

**Archivos temporales:** no creé ninguno en `%TEMP%`. La suite usa `TemporaryDirectory`, que se elimina sola. El repositorio no cambió: `git status --porcelain --untracked-files=all --ignored` dio 0 líneas antes y después. Mi única escritura es este informe.

## Limitación de independencia
- Soy un subagente lanzado por el autor (copilot-sdk-main), con su mismo runtime, sesión anfitriona, usuario SO, workspace y credenciales.
- Tengo permiso técnico de escritura sobre el artefacto revisado, el repositorio y el registro de la sesión (ACL: `FAYAT\cvaldes FullControl` sobre `events.jsonl`). No lo he usado, pero esa abstención no es verificable.
- **Clasificación con el modelo v14:**
  - **A (autoría):** independiente **declarada**. Mi id no figura en ningún rol y no he producido ni modificado lo revisado.
  - **B (aislamiento):** `I1_CONTEXTO_SEPARADO` declarado. Tengo un contexto nuevo, sin historial ni memoria del autor; del registro de la sesión no leí el contenido, solo recuentos. Según OB-4 (v14:44), declaro que el encargo incluye un resumen del autor sobre la decisión de las 09:53 que **no puede contrastarse** con ninguna fuente escrita. Las demás referencias venían con hash y las he contrastado. No alcanzo I2 porque puedo escribir.
  - **C (trazabilidad):** `G0_DECLARADA`. No hay evidencia `identity`, `isolation` ni `execution` fijada, ni verificación de un tercero.
- Con la matriz propuesta, este informe **no alcanzaría** el mínimo de un Gate 1 formal de GOV-001 (HIGH: I1·G1{identity}). Es un dictamen técnico sobre el plan, no un Gate de `mission.json`.
