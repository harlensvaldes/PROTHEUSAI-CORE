# GOV-001 · Revisión Quality del plan v15 (cierre de GR-43, GR-44, OB-21 y OB-22), ciclo 15

**Dictamen:** PASS
**Revisor:** quality-gov001-r15
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) me asignó este nombre al lanzarme como subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No hay registro de lanzamiento accesible como evidencia, ni firma ni otro mecanismo que lo acredite.
**Independencia verificada:** no — la autoría independiente es solo declarada: no redacté v1–v15 ni GOV-R-REVIEW-01..14 y no implementaré la misión. Comparto runtime, sesión anfitriona, usuario SO, workspace y credenciales con el autor, y el encargo lo redactó el autor. Clasificación con el modelo v15 al final: A declarada · I1 (con resumen no contrastable declarado) · G0.
**Artefacto revisado:** GOV-001-R-PLAN-v15.md sha256:67e3643d6adedba102f956af57729bc4800eba5266b9747dbb7a8633005ce31b
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v15 frente a v14 (`git diff --no-index --word-diff=plain`), v8 y `GOV-R-REVIEW-14.md`; lectura de `AGENTS.md`, `agents/quality.md`, `docs/QUALITY_POLICY.md`, `docs/ROLE_MATRIX.md` y `docs/MISSIONS/GOV-001/06-DECISION.md` de PROTHEUSAI-CORE `6e5e929`. Ejecuté la suite y `validate` en solo lectura con `python -B`. No leí el registro de mensajes de la sesión. No hice prototipo de la CLI v3.

> **Alcance del PASS.** Es un dictamen técnico sobre el plan con el hash indicado, no un Gate 1 de `mission.json`. No sustituye las decisiones D1–D4 del Owner ni la autorización de `OWNER-DECISION-02.md`. Con la matriz propuesta, este informe tampoco alcanzaría el mínimo de un Gate 1 formal HIGH (I1·G1{identity}); ver «Limitación de independencia».
>
> **Criterio de dictamen.** Es PASS porque:
> - GR-43, GR-44, OB-21 y OB-22 quedan cerrados;
> - el diff v14→v15 no introduce regresiones;
> - no encuentro ningún defecto que pueda causar un falso PASS, una contradicción normativa o un incumplimiento de la decisión del Owner.
>
> Las tres observaciones nuevas (OB-23..OB-25) no condicionan el dictamen. En cada una, una lectura razonable apoyada en el propio plan resuelve la duda sin inventar reglas, o la cuestión es una consecuencia ya cubierta por el riesgo residual declarado (v15:107). Las incluyo para mejorar la redacción cuando el plan se convierta en protocolo (§8).

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash de v15 | `sha256(bytes)` y `sha256(bytes.replace(b'\r\n',b'\n'))` | `67e3643d…ce31b` y `sha256_lf 1da8ab7b…5f52a` (26 626 bytes). **Coinciden** con el encargo |
| v14, REVIEW-14, v8 | mismo cálculo | sha256_lf: v14 `50c1d66a…8606` ✓; REVIEW-14 `7cb44e12…7c8d` ✓; v8 `0d6bcca0…2a93` ✓. La cabecera de v15 (v15:4-5) cita los mismos valores |
| Repo | `git log -1`; `git status --porcelain --untracked-files=all --ignored` | `6e5e929…f467`; 0 líneas antes y después |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 |
| Validación | `python -B scripts\quality_cli.py validate` | `OK — estructura consistente…`, exit 0 |
| Decisión del Owner de 09:53 | `files\`, repo | Sin registro escrito. Solo dispongo de la paráfrasis del encargo, que v15:8 reconoce |

## Estado de hallazgos previos (REVIEW-14)
| ID | Estado | Evidencia |
|---|---|---|
| GR-43 | **CERRADO** | **Primera laguna.** v15:105 formula la regla sobre la diferencia: «Cualquier diferencia entre lo comiteado y la entrada (archivo modificado, nuevo o eliminado, esté o no listado en la entrada) que no pertenezca a estas categorías reabre Gate 2». Un archivo versionado no listado y modificado o eliminado después aparece en el commit, el paso 2 (v15:92) lo detecta y v15:105 le da consecuencia. **Segunda laguna.** v15:101 añade «el registro de aceptación del Owner (`owner_acceptance` y `06-DECISION.md`)». Con ello la aceptación posterior al commit (v15:93; D4, v15:255) ya no reabre Gate 2. Ambos puntos coinciden con la corrección mínima de REVIEW-14. |
| GR-44 | **CERRADO** (opción a) | v15:94 asigna la lectura del ancla en el registro de mensajes a «quien **no** emite un dictamen sujeto a I1 en la misión: el Owner o Quality en la revisión de aceptación». v15:95 limita al revisor de Gate 3 a examinar la comparación registrada y tratarla «como declaración». Así, el revisor de Gate 3 (I1 en toda la matriz, v15:80-82) ya no está obligado a abrir el registro que contiene el contexto del autor. La opción elegida se declara. El riesgo residual (v15:107) sigue cubriendo la no ejecución de los pasos 2-3. Quedan detalles de redacción y portabilidad en OB-23 y OB-25. |
| OB-21 | CERRADA | v15:59 usa `gates.<gate>.review.reviewer_verification` y v15:215 usa `POST-GATE-VALIDATION-<sufijo>`, coherente con v15:92. `<n>` ya solo aparece en `GATE2-INPUT-<n>` (v15:75, 88 y 215), con el significado definido en v15:88. |
| OB-22 | CERRADA | v15:89: la instrucción incluye «el `sha256_lf` de la entrada o, si lo revisado ya está comiteado, el commit `git:`», coherente con la comparación de v15:92. |

No reabro GR-24..GR-42, O-1..O-8 ni OB-1..OB-20: no hay evidencia nueva y v15 no modifica sus líneas.

## Regresiones v14→v15
El diff solo cambia:
- la versión (v15:1, 3-5, 14 y 255);
- v15:59, 89, 93-95, 97, 101 y 105 en §1–§2;
- v15:215 en §8.

Todo es trazable a GR-43, GR-44, OB-21 y OB-22. No cambian la tabla de §0, el modelo A/B/C, la matriz, §3, §4, §5, §6, §7 ni §9, salvo la referencia a la versión en D4. No hay regresiones ni sobrealcance.

## Hallazgos nuevos
Ninguno que condicione el dictamen (no se abre GR-45).

## Valoraciones solicitadas
- **Autoría, aislamiento y garantía:** siguen separados en tres dimensiones (v15:31-33).
  - Compartir runtime, usuario SO o workspace no anula A (v15:43).
  - B se declara siempre y la CLI nunca acredita aislamiento.
  - El plan no afirma aislamientos inexistentes: el ancla es alterable si se comparte usuario SO (v15:90, 107).
  - v15 reduce además la exposición del revisor I1 de Gate 3 (GR-44).
- **Nunca autoaprobación:**
  - A es absoluta en PASS/PWR (v15:36);
  - R7 y R8 se mantienen en `validate` para misiones aceptadas (v15:71);
  - el conflicto de interés del Architect se declara y se somete a D3 (v15:116).
- **Proporcionalidad por Gate:** la matriz y su razonamiento no cambian. El procedimiento de Gate 2 queda ahora cerrado en su consecuencia (GR-43) y en el reparto de quién lee el ancla (GR-44).
- **schema_version, hashes normalizados frente a bytes y redundancia:** sin cambios desde v12; ya los valoré como correctos.
- **Sobrealcance:** ninguno. R02 sigue en GOV-002 (§6) y los cambios de v15 son documentales.

## Observaciones (no condicionan el dictamen)
Criterio: en cada caso, el texto del plan ya excluye la lectura problemática, o la consecuencia está cubierta por el riesgo residual declarado. Ninguna puede producir por sí sola un PASS falso ni contradice una norma vigente.

- **OB-23 · «Quality en la revisión de aceptación» choca con el vocabulario del repositorio.**
  - En `docs/QUALITY_POLICY.md`, el Gate 3 se titula «Gate 3 · Verification & acceptance». En `docs/ROLE_MATRIX.md:12`, el papel de Quality en la aceptación es el «Dictamen Gate 3». Hoy no existe otra «revisión de aceptación» de Quality.
  - Por tanto, la expresión de v15:94 podría leerse como el revisor de Gate 3, que es I1.
  - La propia frase lo excluye («quien **no** emite un dictamen sujeto a I1»), y v15:95 separa expresamente al revisor de Gate 3. Por eso es una observación.
  - El origen de la expresión es la corrección (a) que propuso REVIEW-14.
  - Además, en v15:94, «quien» sigue gramaticalmente a «Orchestrator» y el sujeto real aparece tras los dos puntos.
  - **Redacción sugerida al pasarlo al protocolo:** «La lee el Owner o un Quality que no emite ningún dictamen de Gate en la misión». Conviene añadir que, si ese Quality interviene después en un Gate reabierto, se declara I0.
- **OB-24 · Encaje con O-7 en GOV-001.** v15:160 asigna «la revisión independiente de esos registros» al Gate de revalidación de §7, cuyos revisores son I1 (fila HIGH).
  - Leída con v15:94-95, la lectura del ancla de R03 corresponde al Owner o a un Quality sin dictamen de Gate. Los revisores de la revalidación examinan la comparación como declaración.
  - Sería más claro decirlo en §5.
- **OB-25 · Consecuencias de la opción (a) no explicitadas.**
  - En la práctica, para cada misión MEDIUM o superior, el lector del ancla será casi siempre el Owner, salvo que se disponga de un Quality adicional sin dictamen de Gate. Esto añade una tarea rutinaria (ligera: comparar un hash) al Owner, cuando §2 justifica la relajación de R1/R4b para que el Owner no sea verificador rutinario de identidades. Son tareas distintas, por lo que no hay contradicción.
  - Tampoco se dice qué ocurre si el lector no tiene acceso al registro de mensajes (runtime que no lo persiste o no lo muestra). El paso 3 es obligatorio antes de la aceptación, así que, si no puede ejecutarse, la aceptación queda sin ese control, que es el caso ya declarado en v15:107.
  - Conviene que la consecuencia y la alternativa (b) consten en el plan o en D3, como pidió el Owner («alternativas y consecuencias»), en lugar de solo por referencia a REVIEW-14.

## Qué NO verifiqué
- El texto literal de la decisión del Owner de 09:53. Solo dispongo de la paráfrasis del encargo, redactada por el autor.
- Ninguna implementación v3: no hay prototipo y no medí la estimación de líneas.
- La existencia, persistencia y accesibilidad de un registro de mensajes, o su visibilidad para el Owner, en LUNA o en Cline.
- El contenido del registro de mensajes de esta sesión (`events.jsonl`). No lo abrí.
- Un registro de lanzamiento utilizable como evidencia `identity`, y la identidad de cualquier participante.
- El procedimiento de Gate 2 de v15. Lo analicé solo de forma estática, sin reproducirlo con un escenario.
- R01, que está aprobado y fuera del alcance de esta revisión.

**Archivos temporales:** no creé ninguno en `%TEMP%`. La suite usa `TemporaryDirectory`, que se elimina sola. El repositorio no cambió: `git status --porcelain --untracked-files=all --ignored` dio 0 líneas antes y después. Mi única escritura es este informe.

## Limitación de independencia
- Soy un subagente lanzado por el autor (copilot-sdk-main), con su mismo runtime, sesión anfitriona, usuario SO, workspace y credenciales.
- Tengo permiso técnico de escritura sobre el artefacto revisado, el repositorio y el registro de la sesión. No lo he usado, pero esa abstención no es verificable.
- **Clasificación con el modelo v15:**
  - **A (autoría):** independiente **declarada**. Mi id no figura en ningún rol y no he producido ni modificado lo revisado.
  - **B (aislamiento):** `I1_CONTEXTO_SEPARADO` declarado. Tengo un contexto nuevo, sin historial ni memoria del autor, y no leí el registro de la sesión.
    - Según OB-4 (v15:44), declaro que el encargo incluye un resumen del autor sobre la decisión de las 09:53 que **no puede contrastarse** con ninguna fuente escrita. Las demás referencias venían con hash y las he contrastado.
    - No alcanzo I2 porque puedo escribir.
  - **C (trazabilidad):** `G0_DECLARADA`. No hay evidencia `identity`, `isolation` ni `execution` fijada, ni verificación de un tercero.
- Con la matriz propuesta, este informe **no alcanzaría** el mínimo de un Gate 1 formal de GOV-001 (HIGH: I1·G1{identity}). Es un dictamen técnico sobre el plan, no un Gate de `mission.json`, y no se transfiere a versiones posteriores.
