# GOV-001 · Revisión Quality del plan de resolución GOV-R01..R03, ciclo 7

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r7
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) me asignó este nombre al lanzar el subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime y no hay firma ni otro mecanismo que acredite la identidad.
**Independencia verificada:** no — la separación es solo contextual: no redacté GOV-001-R-PLAN-v1..v7 ni GOV-R-REVIEW-01..06 y no implementaré la misión, pero soy un subagente del mismo runtime, sesión y usuario del sistema que el autor (copilot-sdk-main). Con la semántica del plan, este informe sería `NO_ACREDITADA`.
**Artefacto revisado:** GOV-001-R-PLAN-v7.md sha256:07fd2e9298ce19f741aaac947e3a3233fb1af04ac581139082a9ec2afd1aa498
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v7 frente a v6 (`git diff --no-index --word-diff=plain`, exit 1 = hay diferencias), frente a `GOV-R-REVIEW-06.md`, `AGENTS.md`, `agents/quality.md`, `GOV-001-PROPOSAL-v8.md` y el repositorio PROTHEUSAI-CORE `6e5e929`. Pruebas propias de supuestos en `%TEMP%` (borradas) con Python 3.12.0 y Git 2.55.0.windows.3, usando los bytes reales de la reconstrucción. Suite y `validate` ejecutados en solo lectura con `python -B`. No modifiqué el repositorio ni ningún archivo existente.

> Este dictamen técnico vale solo para la versión identificada arriba. Según la decisión del Owner, PASS_WITH_RESERVATIONS **no habilita avanzar**: hay que completar GR-23 en el plan antes de someterlo al Owner. Las observaciones no condicionan el dictamen. Este informe no aprueba ningún Gate formal de `mission.json`.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash del plan v7 | `Get-FileHash` | `07FD2E92…1AA498`, igual al del encargo |
| Hashes previos | `Get-FileHash` | v6 `DCC9AF80…7A73F9` y REVIEW-06 `12BF11DB…B966F0`: coinciden |
| Repo | `git rev-parse HEAD`; `git status --porcelain --untracked-files=all --ignored` | HEAD `6e5e92980a8e…`; 0 líneas antes y después |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 |
| Validación | `python -B scripts\quality_cli.py validate` | `OK — estructura consistente…`, exit 0 |
| `core.autocrlf` | `git config --get core.autocrlf` | `true` |
| Numeración de entradas | `git ls-files docs/MISSIONS/GOV-001` | Existen `GATE2-INPUT-02/03.sha256`; no existe `-04`. La asignación de v7 (`-04` a R01) no colisiona |
| Formato precedente | `GATE2-INPUT-03.sha256`, líneas 1–8 | Incluye `# git status --porcelain --untracked-files=all` y su salida (relevante para O-8) |
| Precedente post-commit | `GOV-001-PROPOSAL-v8.md` § Secuencia, paso 7 | «comparar el SHA-256 de cada archivo de `git diff 29d741e..HEAD --name-only` con `GATE2-INPUT.sha256`» |
| Reconstrucción | `files/gov-r01/GATE2-INPUT.sha256.reconstructed` | SHA-256 `F0F7392A…8C4A9B` = `GATE2-REVIEW-01.md:7`; 6442 bytes, 0 CR, 98 LF |
| Dictámenes previos | `Select-String '^\*\*Dictamen:\*\*'` | REVIEW-01 FAIL; 02 a 06 PWR. La cabecera de v7 («v1 FAIL; v2 a v5 PWR», corrige el PWR del ciclo 6) es exacta |
| Diff v6→v7 | `git diff --no-index --word-diff=plain` | Cambios limitados a: cabecera; § R01 Verificación (pasos 1–3); § Principio (comando `sha256_lf` y dependencia del crudo); viñeta nueva «Último Gate de R03 (O-7)»; § Gates de R03 (`-05`); «Decisiones del Owner» → Autorización (transcripción o cita). No se elimina contenido salvo el texto sustituido a propósito |

## Pruebas propias de supuestos (`%TEMP%`, borradas; `cleaned=True`)
**A. Paso 2 de la verificación de R01 con los bytes reales.** Clon local de `6e5e929` con `autocrlf=true`, archivo reconstruido en `docs/MISSIONS/GOV-001/GATE2-INPUT-01.RECONSTRUCTED.sha256`, commit desechable, y extracción en clones con cada valor de `autocrlf`:

| Caso | autocrlf=true | autocrlf=false | Blob `HEAD:<ruta>` |
|---|---|---|---|
| Con `.gitattributes` (`<ruta> -text`) | `F0F7392A` | `F0F7392A` | `F0F7392A` |
| Sin `.gitattributes` (control) | `8D50DF33` | `F0F7392A` | `F0F7392A` |

Lectura: el procedimiento de v7 demuestra el efecto de `-text` antes del commit real (el control falla donde debe). También muestra que el **blob** coincide con o sin `-text`: el `MATCH` contra el blob, por sí solo, no prueba GR-05 (relevante para O-9).

**B. Comando de O-6.** Copiado literalmente del plan y ejecutado en PowerShell 5.1 y en `cmd`: CRLF `a\r\nb\r\n` y LF `a\nb\n` → `911169dd…59a2` en ambos shells, igual al SHA-256 crudo del archivo LF. Con un `\r` suelto (`a\rb\n`) → `367d1c77…`, distinto. Cumple la definición GR-15b.

## Estado de los hallazgos previos
| ID | Estado | Evidencia en v7 | Residual |
|---|---|---|---|
| GR-01..21 | Cerrados en ciclos anteriores; sin regresión | El diff v6→v7 no toca esos puntos | GR-09 sigue arrastrado al Gate 1 de GOV-002 |
| GR-22 (detalle) | **Cerrado** | Autorización: «El registro debe transcribir literalmente estas líneas o citarlas por ruta y hash de este plan». Es lo que pedía el residual de REVIEW-06. | Ver O-11 (opcional). |
| GR-23 (LOW) | **Cerrado en parte (R01); abierto en R03** | **R01, parte (a):** paso 1 (manifiesto `GATE2-INPUT-04.sha256` con `sha256_lf` y crudo del reconstruido) y paso 2 (commit desechable y extracción con ambos `autocrlf`, comprobado en la prueba A). El bloqueo circular desaparece. **R01, parte (b):** paso 3, comparación posterior al commit contra `-04` y `MATCH` repetido, registrada por adición en `POST-GATE-VALIDATION-R01.md`. | **R03, parte (b):** REVIEW-06 («Estado por observación»: «GOV-R03 … Quedan O-6 y la parte (b) de GR-23») pedía que, tras el commit de R03, se compare lo comiteado con lo revisado. v7 no lo hace. La viñeta nueva «Último Gate de R03 (O-7)» solo compara **la cita** del `sha256_lf` del informe de Quality, no los archivos de código comiteados. § Gates de R03 solo dice que habrá entradas `GATE2-INPUT-05…`, y Secuencia paso 4 termina en «Gate 2/3 → commit», sin comprobación posterior. R03 es el único incremento de **código** (unas 50 líneas en `quality_cli.py`, tests, plantillas), así que es donde más importa que el commit sea lo revisado. **Revisión del registro de R01:** REVIEW-06, corrección (3), asignaba a Quality la revisión del registro posterior al commit «en el Gate siguiente». v7 lo asigna para R03 (O-7), pero no para `POST-GATE-VALIDATION-R01.md`, que solo produce el Orchestrator, que es también quien comitea. Ver la corrección mínima abajo. |
| O-6 | **Cerrado** | § Principio: comando de una línea para `sha256_lf` hasta que exista `hash`; «El SHA-256 crudo depende de `core.autocrlf` y se usa solo como referencia secundaria». La comparación con `evidence_sha256_lf` ya es entre valores `sha256_lf`. Prueba B: el comando funciona tal como está escrito. | — |
| O-7 | **Cerrado** | «la comparación independiente queda **asignada a la revalidación de GOV-001 con GOV-002** (opción A) o al Gate de cierre (opción B)». Asigna momento y, por el adjetivo «independiente», a un revisor Quality. | Editorial: la opción B no define ningún «Gate de cierre». Se entiende como el último Gate de la misión ampliada. No condiciona. |

### GR-23: corrección mínima pendiente
Añadir a R03 (por ejemplo, en § Gates o en la viñeta O-7) una frase equivalente al paso 3 de R01 y al precedente `PROPOSAL-v8` paso 7. Tras el commit de R03, el Orchestrator compara cada archivo de `git diff <commit de R01>..HEAD --name-only` con la última entrada `GATE2-INPUT-0N.sha256` de R03. Solo pueden diferir los archivos de registro permitidos. Repite la suite y `validate` y lo registra por adición en `POST-GATE-VALIDATION-R03.md`. Indicar también quién revisa `POST-GATE-VALIDATION-R01.md`: por ejemplo, el revisor del Gate 1 de R03, que es el Gate siguiente, y la revalidación de la opción A para `-R03`.

Criterio de gravedad: LOW. No hay ningún PASS falso registrado ni ningún defecto de diseño. Es el riesgo, ya señalado en REVIEW-06 y no corregido, de que el commit de código de R03 difiera de lo revisado en su Gate 2/3 sin que nada previsto lo detecte (AGENTS §3, Gate 2; §5, trazabilidad). Por eso condiciona el dictamen y no es una observación.

## Hallazgos nuevos
No hay hallazgos nuevos que condicionen el dictamen (GR-24 no se asigna).

### Observaciones no bloqueantes
Criterio: no condicionan el dictamen porque no producen PASS falsos ni dejan un riesgo sin control previsto. Son mejoras de precisión o de redacción que el autor puede adoptar o no.
- **O-8 (manifiesto sin `git status`).** El paso 1 de R01 no dice que `GATE2-INPUT-04.sha256` incluya `git status --porcelain --untracked-files=all`, como hace `-03` y como pedía REVIEW-06, corrección (1). No bloquea por tres motivos: el Gate 2 obliga a Quality a inspeccionar el diff real y su alcance (`agents/quality.md` § Gate 2); el paso 3 compara «los archivos comiteados» con el manifiesto, lo que detecta archivos de más si se lee como el conjunto del commit; y «la numeración continúa la de GOV-001» sugiere el mismo formato. Conviene decirlo expresamente.
- **O-9 (precisión del paso 3 de R01).** «repite el `MATCH` en un clon nuevo» no fija el valor de `autocrlf` ni si «compara los archivos comiteados» se refiere a blobs o a archivos extraídos. La prueba A muestra que el `MATCH` contra el blob se da también sin `-text`. Aun así, la propiedad GR-05 tras el commit real se deduce de forma determinista de dos hechos: el `.gitattributes` comiteado es igual al del manifiesto, y el paso 2 ya demostró su efecto con esos bytes. Basta con añadir «con `autocrlf=true`, comprobando el SHA-256 crudo del archivo extraído».
- **O-10 (numeración).** «`GATE2-INPUT-05`…, porque la `-04` corresponde a R01» supone que R01 tendrá un solo ciclo de Gate 2/3. R01.4 exige numerar por ciclo. Si R01 necesita repetir el Gate, usaría `-05`. La secuencia es lineal (R01 se comitea antes que R03), así que no hay colisión real si se lee como «el siguiente número libre». Es editorial.
- **O-11 (cita del plan en `OWNER-DECISION-02.md`).** Los planes `GOV-001-R-PLAN-v*` solo están en la carpeta de sesión, no en el repositorio. Si el Owner elige citar por ruta y hash, conviene copiar el plan, sin alterar sus bytes, al registro de la misión (como `PROPOSAL-v1..v8`) para que la referencia pueda recuperarse. Hay una alternativa segura (la transcripción literal) y un precedente (`OWNER-DECISION-01`), así que es opcional.

## Regresiones v6→v7, falsos PASS, alcance y afirmaciones
- **Regresiones:** ninguna. Se mantienen la clasificación, R01.1–5, el diseño y las reglas de R03, la tabla de responsabilidades, el inventario de tests (19 tests; suite en verde), R02, el cierre, § Detención y «Carácter». La única renumeración (`-04` → `-05` en R03) es coherente con la nueva entrada de R01.
- **Falsos PASS:** ninguno. El paso 2 de R01 ya no permite aprobar GR-05 sin evidencia (prueba A). El residual de GR-23 en R03 es un riesgo de divergencia tras el commit, no una aceptación indebida.
- **Alcance:** sin sobrealcance ni frameworks. El texto crece unos 1,4 kB, limitados a lo pedido. Los nuevos archivos `POST-GATE-VALIDATION-R01/R03.md` encajan en la opción «o en un archivo nuevo» (O-3).
- **Afirmaciones:**
  - «demuestra el efecto de `-text` antes del commit real»: confirmado (prueba A, con los bytes reales).
  - Comando de una línea `sha256_lf`: confirmado (prueba B).
  - «El SHA-256 crudo depende de `core.autocrlf`»: coherente con la prueba A de REVIEW-06 y con el control sin `-text` de la prueba A.
  - Hashes abreviados de la cabecera (`12BF11DB…66F0`, `DCC9AF80…73F9`): coinciden.

## Estado por observación
| Obs. | Clasificación v7 | Estado |
|---|---|---|
| GOV-R01 | Bloqueo | Diseño y verificación correctos; GR-23 cerrado para R01, salvo la asignación de quién revisa `POST-GATE-VALIDATION-R01.md`. |
| GOV-R03 | Bloqueo | Diseño correcto; O-6 y O-7 cerrados. Falta la comparación posterior al commit (GR-23 b). |
| GOV-R02 | Mejora futura (GOV-002) | Sin cambios. |
| Secuencia/Decisiones | — | GR-22 cerrado. |

## Qué NO verifiqué
- `GOV-R01-reconstruct.py` adaptado ni un `MATCH` real del script. No existe en el repositorio y no ejecuté `files/gov-r01/reconstruct.py`. Usé su salida ya existente (`GATE2-INPUT.sha256.reconstructed`), cuyo hash comprobé.
- La implementación de R03, que no existe.
- Linux/CI y otros shells (bash) para el comando de O-6; solo lo probé en PowerShell 5.1 y en `cmd` en Windows.
- Que `OWNER-DECISION-02.md`, que aún no existe, vaya a transcribir o citar la Autorización.
- `git fsck`, la búsqueda de copias del original (GR-16) y las pruebas de firma de R02 (no las repetí).
- El piloto `protheus-efd`, el origen EPF `5ee75df` y otros consumidores de `quality_cli.py`.
- Que el contenido o las marcas de tiempo de la carpeta de sesión no se alteraran fuera de los hashes comprobados.

## Limitación de independencia
Soy un subagente del mismo runtime, sesión y usuario del sistema que el autor del plan (copilot-sdk-main) y que los revisores de los ciclos 1 a 6. Mi separación es solo contextual y no está acreditada. Con la semántica del plan, este informe declararía `NO_ACREDITADA` y no puede servir como `evidence_file` de un Gate formal en PASS o PWR. Su valor es técnico: un revisor independiente puede reproducir las comprobaciones descritas.
