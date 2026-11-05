# GOV-001 · Revisión Quality del plan de resolución GOV-R01..R03, ciclo 3

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r3
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) asignó este nombre al lanzar el subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime y no hay firma ni otro mecanismo que acredite la identidad.
**Independencia verificada:** no — la separación es solo contextual. No redacté GOV-001-R-PLAN-v1/v2/v3 ni GOV-R-REVIEW-01/02 y no implementaré la misión, pero soy un subagente del mismo runtime y sesión que el autor (copilot-sdk-main) y no hay prueba operativa de separación.
**Artefacto revisado:** GOV-001-R-PLAN-v3.md sha256:53b0ff3a303ee495ba92b7d1e106597d12b2cb751fc79c6ac7f8f772b1d8779e
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática del plan v3 frente al v2 (`git diff --no-index --word-diff`), a `GOV-R-REVIEW-01.md` (`e563c77f…d20e`) y `GOV-R-REVIEW-02.md` (`d20320a7…a9c7`), a `AGENTS.md`, `agents/quality.md` y al código de PROTHEUSAI-CORE `6e5e929` (`scripts/quality_cli.py`, `tests/test_governance.py`, plantillas, workflows, manifiestos y registros de GOV-001). Pruebas propias en `%TEMP%` (borradas) con Python 3.12.0 (`python -B`), Git 2.55.0.windows.3 y OpenSSH_for_Windows_9.5p2. Suite actual y `validate` ejecutados en solo lectura. No modifiqué el repositorio ni archivos existentes.

> Dictamen técnico, válido solo para la versión identificada arriba; no se transfiere a v4 ni posteriores. Según la decisión del Owner, PASS_WITH_RESERVATIONS **no habilita avanzar**: GR-16, GR-17 y GR-19 y el residual de GR-08 son condiciones a corregir en el plan antes de someterlo a decisión del Owner; GR-18 puede cerrarse en el Gate 1 de R03. Ningún punto de este informe aprueba un Gate formal de `mission.json`.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash del plan v3 | `Get-FileHash` | `53B0FF3A…D8779E` = encargo |
| Hashes previos | `Get-FileHash` | v2 `2A5AAA02…93AE`, REVIEW-02 `D20320A7…A9C7`, REVIEW-01 `E563C77F…D20E`: coinciden |
| Repo | `git log`, `git status --porcelain --untracked-files=all --ignored` | HEAD `6e5e929`; salida vacía antes y después (exit 0); no existe `.gitattributes` |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0; 19 `def test_` |
| Validación | `python -B scripts\quality_cli.py validate` | `OK …`, exit 0 |
| Manifiestos | lectura JSON | `GOV-001` y `EXAMPLE-001`: v2, tres Gates y Owner en PENDING |

## Pruebas propias de supuestos (`%TEMP%`, borradas)
| Supuesto | Prueba | Resultado |
|---|---|---|
| `sha256_lf = sha256(b.replace(b'\r\n', b'\n'))` (GR-15b) | LF vs CRLF; `\r` suelto | Igual LF/CRLF; distinto con `\r` suelto. **Verificado.** |
| La etiqueta nueva no colisiona con la narrativa ni con la antigua | `quality_cli.labels(text,'Independencia')` sobre `**Independencia:**`, `**Independencia (narrativa):**`, `**Independencia verificada:**` | Solo devuelve `['ACREDITADA']`. **Verificado.** |
| Rutas canónicas comparadas «exactamente» (GR-15a) | Archivo `GATE1-REVIEW-09.md` en carpeta temporal; `Path.is_file()` con `gate1-review-09.md`, `./GATE1-REVIEW-09.md`; `sub\x` | En Windows, la ruta con mayúsculas distintas **existe** (`is_file` True, no figura en `os.listdir`); `./` también; `\` actúa como separador. CI usa `ubuntu-latest` (`.github/workflows/quality.yml:8`, `.gitea/workflows/quality.yml:9`), donde no. Ver GR-18. |
| «No se ha encontrado ninguna copia» | Búsqueda de solo lectura de `GATE2-INPUT` en `entries.json` del historial local de VS Code y VS Code Insiders, y en la Papelera del usuario actual | 0 coincidencias. Corrobora parcialmente (mismo usuario/máquina, sin independencia). `git fsck` no ejecutado. Ver GR-16. |
| Anterioridad del hash objetivo | `git log` (commit `6e5e929` 08:46:24) vs creación de `gov-r01\reconstruct.py` (08:54:40); `git show 6e5e929:…GATE2-REVIEW-01.md` y `GATE3-EVIDENCE-01.md` línea 7 | Coherente con el plan y con REVIEW-01:23. **Verificado** (marcas de tiempo del sistema de archivos: evidencia débil). |

## Estado de los hallazgos previos
| ID | Estado | Evidencia en v3 | Residual |
|---|---|---|---|
| GR-01..GR-02, GR-05, GR-07, GR-09 | Cerrados en ciclo 2; sin regresión | Texto sin cambios relevantes en v3 | GR-09 sigue arrastrado al Gate 1 de GOV-002 |
| GR-03 (residual LOW) | **Cerrado** | Subcomando `hash <ruta>`; «G2-13 sigue abierto» para hashes crudos; definición a nivel de bytes | Ver GR-19 (la mitigación de GR-14 no usa esta definición) |
| GR-04 (residual LOW) | **Cerrado** | `status` muestra «declarada por el revisor; no comprobada por la CLI»; se mantiene N42 (`tests/test_governance.py:21,411-415`, regex `verificad[oa]`) | — |
| GR-06 (residual LOW) | **Cerrado** | Imprime la versión de Git; tolera que el archivo no esté comiteado | El script depende de `git diff --stat` (`gov-r01\reconstruct.py:213-224`); INCIDENT-01 debería registrar la versión con la que se obtuvo el MATCH (no bloqueante) |
| GR-08 | **Cerrado; residual LOW sigue abierto** (no abordado en v3; el encargo y la cabecera de v3 lo omiten) | «Tras el PASS de los Gate 2/3 de R01 y R03…» (§ Cierre) | Ver «Residual GR-08» abajo |
| GR-10 (residual LOW) | **Cerrado** | Base 19 tests/exit 0 (verificada); recuento antes/después y justificación de diferencias; inventario `:68,74`, `:222-225`, `:231-233`, `:422` (verificado) | — |
| GR-11 (MEDIUM) | **Cerrado en lo esencial; ambigüedad nueva** | Token `ACREDITADA`/`NO_ACREDITADA` con semántica que falla cerrado; regla «mismo runtime o sesión no excluido → NO_ACREDITADA»; test de plantilla con `NO_ACREDITADA` en PASS | Ver GR-17 |
| GR-12 (MEDIUM) | **Cerrado** | `<ruta> sha256_lf:<64 hex>` en informe; `evidence:[{"path","sha256_lf"}]`; recálculo; test «evidencia editada» | — |
| GR-13 (MEDIUM) | **Cerrado en lo pedido; residual** | Separación «reproducido (independencia no acreditada)» / «análisis del código» / «declarado por el autor» para los 12 hashes | Ver GR-16 (otra afirmación del autor sin atribuir) |
| GR-14 (MEDIUM) | **Cerrado** | «no pueden fijarla sin alterar el informe»; autoría e integridad previas a la fijación en «No acreditado»; mitigación declarativa | Ver GR-19 |
| GR-15 (LOW) | **(b) y (c) cerrados; (a) parcial** | (b) definición en bytes (verificada); (c) `EXAMPLE-001/02-GATE1-REVIEW.md:5` incluido (línea verificada); (a) POSIX, sin casefold, sin espacios/comas/`..`, sin duplicados, separador `, ` | Ver GR-18 |

### Residual GR-08 (LOW, no abordado)
REVIEW-02 pidió precisar que los «PASS de los Gate 2/3» de R01 y R03 son dictámenes técnicos y no Gates formales. v3 lo mantiene implícito. Con la semántica de GR-11, v3 afirma además que los revisores actuales marcarán `NO_ACREDITADA` y que la CLI bloqueará PASS/PWR: el «Gate 1 de R03» tampoco podrá ser formal y `can-implement` seguirá en BLOCKED. El plan no dice expresamente que la implementación de R03 procederá por autorización documentada del Owner (precedente: `OWNER-DECISION-01.md`, «Queda autorizada la implementación incremental»; condición C2 sobre waivers), ni lo incluye en «Decisiones del Owner». **Corrección:** una frase en «Cierre» y «Secuencia»: los Gates 1/2/3 de R01/R03 son dictámenes técnicos no registrados en `mission.json`; la implementación de R03 requiere autorización expresa del Owner, que se añade a «Decisiones del Owner».

## Hallazgos nuevos
| ID | Gravedad | Evidencia | Problema | Corrección mínima |
|---|---|---|---|---|
| GR-16 | LOW (honestidad, GOV-R01; misma clase que GR-13). Condición antes de redactar INCIDENT-01. | Plan v3 § R01 «Hechos (GR-13: se separa lo reproducido de lo declarado)», primer punto: «No se ha encontrado ninguna copia (Papelera, historial local de VS Code, `git fsck`)». `GOV-R-REVIEW-01.md:57`: «Que el original no exista en la Papelera, en el historial de VS Code ni en ningún otro sitio. No lo comprobé.» | Bajo un encabezado que promete separar lo reproducido de lo declarado, esta afirmación del autor aparece sin atribuir. Mi búsqueda (0 coincidencias en historial de VS Code/Insiders y Papelera) solo la corrobora parcialmente y sin independencia; `git fsck` no lo ejecutó ningún revisor. | «Declarado por el autor: no encontró copia (Papelera, historial local de VS Code, `git fsck`). Corroboración parcial sin independencia: GOV-R-REVIEW-03 (historial VS Code y Papelera).» Misma redacción en INCIDENT-01. |
| GR-17 | LOW (especificación del núcleo de GR-11; posible lectura laxa). Condición antes de la decisión del Owner. | § GOV-R03 «Diseño»: `ACREDITADA` si la separación queda demostrada por la evidencia «(persona, **proceso** o runtime distintos)»; siguiente punto: «mismo runtime o sesión que el autor no excluido» → `NO_ACREDITADA`. | La disyunción admite `ACREDITADA` con solo un proceso distinto, y la regla siguiente lo prohíbe si el runtime es el mismo. No se fija la precedencia ni qué es «runtime» (producto o instancia). Caso real: el Orchestrator lanza otra instancia del mismo agente como proceso separado; un revisor puede leer «proceso distinto» y marcar `ACREDITADA`. Es el mismo tipo de hueco interpretativo que cerró GR-11. Mitigan que la CLI exige además verificación registrada del revisor y de los roles (`quality_cli.py:252-266`), por eso LOW. | Declarar que toda condición de `NO_ACREDITADA` prevalece. Sustituir «proceso» por un criterio operativo, p. ej. «persona distinta, o agente no lanzado ni controlado por un autor, en un runtime distinto» (o declarar expresamente «lanzado por un autor» como `NO_ACREDITADA`). Reflejarlo en protocolo y plantillas. |
| GR-18 | LOW (especificación; resultado dependiente de plataforma). Puede cerrarse en el Gate 1 de R03. | § GOV-R03 «Rutas canónicas (GR-15a)». Prueba propia: en Windows `is_file()` acepta mayúsculas distintas y `./`; `\` es separador. CI en `ubuntu-latest`. `report_text` usa `resolve()`+`is_relative_to` (`quality_cli.py:50-51`). | La definición no excluye `\`, segmentos `.` o vacíos, ni exige que la ruta coincida en mayúsculas con la entrada real del directorio. `validate` local (Windows) podría aceptar lo que CI rechaza. No abre un falso PASS: el hash fija el contenido, y una autocita del `evidence_file` es imposible porque su hash debería contenerse a sí mismo (por eso la regla GR-04 queda redundante, no incorrecta). | Gramática explícita, p. ej. `^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*$` sin segmentos `.`/`..`; comprobar mayúsculas contra `os.listdir` de cada nivel; `resolve()` + `is_relative_to` (sigue enlaces). Tests: `\`, `./`, mayúsculas distintas en sistema de archivos insensible. |
| GR-19 | LOW (coherencia con la definición única del hash, GR-03/GR-14). Condición antes de la decisión del Owner. | § GOV-R03 «Principio»: «el revisor comunica en su respuesta el **SHA-256** de su informe y el Orchestrator lo cita»; § «Definición única del hash»: la CLI solo calcula `sha256_lf`. | El revisor (p. ej., con `Get-FileHash`) comunicará el SHA-256 crudo y el manifiesto guardará `evidence_sha256_lf`. Si el informe tiene CRLF o el checkout los introduce (`core.autocrlf=true`, sin `.gitattributes`), los dos valores difieren y la mitigación no es comparable de forma directa; reabre la ambigüedad de G2-13. | El revisor comunica `sha256_lf` obtenido con `quality_cli.py hash <informe>` (opcionalmente también el crudo, etiquetado) y el Orchestrator verifica igualdad con `evidence_sha256_lf`. |

## Regresiones v2→v3, falsos PASS, alcance y afirmaciones
- **Regresiones:** ninguna. Se mantienen las comparaciones de Revisor, Dictamen, Artefacto y Autor, la exigencia de verificación registrada del revisor por alguien distinto del autor pertinente (`quality_cli.py:252-259`) y N42. El test de plantillas se adapta sin perder aserciones (inventario verificado).
- **Falsos PASS:** la vía Orchestrator (GR-01) y la de evidencias mutables (GR-12) quedan cerradas en diseño. Queda una lectura laxa de la semántica (GR-17). Los informes históricos con `**Independencia verificada:** no` dejarán de ser leídos, pero fallan cerrado por ausencia del token nuevo; sin regresión.
- **Alcance:** sin sobrealcance ni frameworks. El aumento (≈50 líneas frente a ≈40) responde a residuales pedidos (subcomando `hash`, rutas canónicas). R02 sigue siendo diseño para GOV-002.
- **Afirmaciones:** las pruebas de R02 citadas («autor y Quality», Git 2.55, OpenSSH 9.5p2) están respaldadas por REVIEW-01:41 y REVIEW-02; la versión de OpenSSH coincide con `ssh -V`. «No hay ningún v2 con PASS ni PWR» es correcta en CORE (verificado) y en el piloto según REVIEW-02. Sin afirmación no acreditada salvo GR-16.
- **Conservación:** commits y dictámenes intactos; la reconstrucción se declara siempre como tal; append-only declarado como documental.

## Estado por observación
| Obs. | Clasificación v3 | Estado |
|---|---|---|
| GOV-R01 | Bloqueo | Correcto y mínimo. Condición: GR-16 (redacción). Verificación real del script adaptado pendiente para Gate 2/3 de R01. |
| GOV-R03 | Bloqueo | Diseño correcto; GR-11..GR-15 cerrados o casi. Condiciones: GR-17 y GR-19 antes de la decisión del Owner; GR-18 en Gate 1 de R03. |
| GOV-R02 | Mejora futura (GOV-002) | Sin cambios; una clasificación. Residual GR-08 a precisar en «Cierre». |

## Qué NO verifiqué
- `GOV-R01-reconstruct.py` adaptado (no existe); no ejecuté ningún MATCH en este ciclo.
- La implementación de R03 (no existe); todo lo dicho sobre la CLI futura es análisis del plan.
- `git fsck` ni búsqueda de copias fuera del historial de VS Code y de la Papelera del usuario actual.
- La estabilidad de `git diff --stat` entre versiones de Git.
- El piloto `protheus-efd` (me apoyo en REVIEW-02), el origen EPF `5ee75df` y otros consumidores de `quality_cli.py`.
- Custodia de claves, firmas SSH (no repetí las pruebas de R02 de ciclos anteriores).
- Que las marcas de tiempo del sistema de archivos no hayan sido alteradas.

## Limitación de independencia
Soy un subagente del mismo runtime y sesión que el autor del plan (copilot-sdk-main) y que los revisores de los ciclos 1 y 2. Mi separación es solo contextual y no está acreditada; con la semántica de v3 este informe declararía `**Independencia:** NO_ACREDITADA`. No puede servir como `evidence_file` de un Gate formal en PASS o PWR. Su valor es técnico: las comprobaciones descritas son reproducibles por un revisor independiente.
