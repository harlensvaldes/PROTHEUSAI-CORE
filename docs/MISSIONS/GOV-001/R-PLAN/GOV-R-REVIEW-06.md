# GOV-001 · Revisión Quality del plan de resolución GOV-R01..R03, ciclo 6

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r6
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) me asignó este nombre al lanzar el subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime y no hay firma ni otro mecanismo que acredite la identidad.
**Independencia verificada:** no — la separación es solo contextual: no redacté GOV-001-R-PLAN-v1..v6 ni GOV-R-REVIEW-01..05 y no implementaré la misión, pero soy un subagente del mismo runtime, sesión y usuario del sistema que el autor (copilot-sdk-main). Con la semántica del plan, este informe sería `NO_ACREDITADA`.
**Artefacto revisado:** GOV-001-R-PLAN-v6.md sha256:dcc9af80fcb7c8e9c5772be4fbff6a8922f53e87e214926590f77534997a73f9
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v6 frente a v5 (`git diff --no-index --word-diff=plain`, exit 1 = hay diferencias), frente a `GOV-R-REVIEW-05.md`, `AGENTS.md`, `agents/quality.md` y el repositorio PROTHEUSAI-CORE `6e5e929`. Pruebas propias de supuestos en `%TEMP%` (borradas) con Python 3.12.0 (`python -B`) y Git 2.55.0.windows.3. Suite y `validate` ejecutados en solo lectura. No modifiqué el repositorio ni ningún archivo existente.

> Este dictamen técnico vale solo para la versión identificada arriba. Según la decisión del Owner, PASS_WITH_RESERVATIONS **no habilita avanzar**: hay que corregir GR-23 en el plan antes de someterlo al Owner. Las observaciones no bloquean. Este informe no aprueba ningún Gate formal de `mission.json`.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash del plan v6 | `Get-FileHash` | `DCC9AF80…7A73F9`, igual al del encargo |
| Hashes previos | `Get-FileHash` | v5 `04DB987B…FDBFF` y REVIEW-05 `49DD34F4…3EF58`: coinciden |
| Repo | `git log -1`, `git status --porcelain --untracked-files=all --ignored` | HEAD `6e5e92980a8e…`; salida vacía antes y después (exit 0) |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 |
| Validación | `python -B scripts\quality_cli.py validate` | `OK — estructura consistente…`, exit 0 |
| `core.autocrlf` | `git config --get core.autocrlf` | `true` |
| `.gitattributes` | `Test-Path`, `git ls-files` | No existe |
| Finales de línea de los informes de sesión | conteo de bytes `0x0D` | REVIEW-05: 85 CR; REVIEW-04: 71; plan v6: 188. Los informes se escriben en CRLF (relevante para O-1) |
| `POST-GATE-VALIDATION.md` | `Select-String` en `GATE2-INPUT-0*.sha256` y `*.md` de GOV-001 | Ninguna entrada de Gate lo fija por hash. Solo lo citan `GATE1-REVIEW-07/08` y `PROPOSAL-v8` (relevante para O-3) |
| Dictámenes previos | `Select-String '^\*\*Dictamen:\*\*'` | REVIEW-01 FAIL; 02, 03, 04 y 05 PWR. La cabecera de v6 es exacta |
| Diff v5→v6 | `git diff --no-index --word-diff=plain` | Cambios limitados a: cabecera; § Principio (crudo antes de R03, solo por adición sin tocar `03-IMPLEMENTATION.md`, alcance de la comparación); prueba de enlaces (O-4); § Arranque («credenciales»); Secuencia paso 2; «Decisiones del Owner» → Autorización. No se elimina contenido salvo el texto sustituido a propósito (la opción `03-IMPLEMENTATION.md` y «R01 sin condiciones») |

## Pruebas propias de supuestos (`%TEMP%`, borradas; `cleaned=True`)
**A. Efecto de `-text` y dependencia del hash crudo** (repositorio desechable con `core.autocrlf=true`; `rec.sha256` en LF, `rep.md` en CRLF; clones con `autocrlf=true`/`false`):

| Caso | autocrlf=true | autocrlf=false | Lectura |
|---|---|---|---|
| `rec.sha256` LF, sin `.gitattributes` | `7EE5CDA6…` ≠ original `17054D8A…` | `17054D8A…` | Reproduce GR-05 |
| `rec.sha256` con `rec.sha256 -text` **comiteado** | `17054D8A…` | `17054D8A…` | La propiedad de GR-05 se cumple, pero **solo puede comprobarse tras un commit** (GR-23) |
| `rep.md` CRLF: SHA-256 crudo | `452C4C5E…` (= original) | `2E6E399F…` | El crudo depende de `autocrlf` |
| `rep.md` CRLF: `sha256_lf` | `2E6E399F…` | `2E6E399F…` | Estable. El crudo del original (`452C…`) **no coincide** con su `sha256_lf` (`2E6E…`) (O-1) |

**B. Uniones y enlaces (O-4):** `mklink /J` sin privilegios → exit 0. `Path.resolve()` de `mission/junc/x.md` sale de la misión → `is_relative_to` = `False`. `os.symlink` sin privilegios → `WinError 1314`. Confirma la premisa de v6: en Windows la unión siempre puede crearse y el enlace simbólico no.

## Estado de los hallazgos previos
| ID | Estado | Evidencia en v6 | Residual |
|---|---|---|---|
| GR-01..21 | Cerrados en ciclos anteriores; sin regresión | El diff v5→v6 no toca esos puntos | GR-09 sigue arrastrado al Gate 1 de GOV-002 |
| GR-22 (LOW) | **Cerrado** | «Decisiones del Owner» → Autorización: «R01: implementar las adiciones; commit solo tras PASS técnico en su Gate 2/3»; «R03: implementar solo tras PASS técnico en su Gate 1; commit solo tras PASS técnico en su Gate 2/3»; «En ambos rige la cláusula de detención». Secuencia paso 2: «cada commit queda condicionado a PASS técnico en Gate 2/3». Es la redacción que pidió REVIEW-05 y no contradice § Detención. Ya no queda la expresión «sin condiciones». | Menor, no bloqueante: no se exige expresamente que `OWNER-DECISION-02.md` transcriba o cite literalmente esas líneas. El encabezado «Autorización (`OWNER-DECISION-02.md`)» lo implica. |
| O-1 | **Cerrado en parte** | § Principio: «**Hasta que R03 esté implementada**, ese subcomando no existe y se usa el SHA-256 crudo (O-1)». | No declara que el crudo dependa de `core.autocrlf` (era lo que pedía O-1), y la comparación que prescribe la viñeta siguiente («con `evidence_sha256_lf`») no sirve para valores crudos. Prueba A: un informe CRLF (los de esta sesión lo son) tiene crudo `452C…` y `sha256_lf` `2E6E…`. Daría una falsa alarma, no un PASS falso. Ver O-6. |
| O-2 | **Cerrado en lo principal** | «Esa comparación solo detecta cambios **posteriores** a la cita, no una fabricación anterior (O-2)». | No se aborda la segunda parte: la cita del Gate final no tiene «Gate siguiente» y la «auditoría» sigue sin responsable ni momento. No bloquea; la Opción A (revalidación con GOV-002) sería el lugar natural. |
| O-3 | **Cerrado** | «solo por adición, en `POST-GATE-VALIDATION.md` o en un archivo nuevo, nunca editando `03-IMPLEMENTATION.md`». Comprobado: ninguna entrada de Gate fija `POST-GATE-VALIDATION.md` por hash, así que añadirle texto no invalida ningún registro. | — |
| O-4 | **Cerrado** | «En Windows se usa una unión (`mklink /J`), que no requiere privilegios, así que el test **no** se omite»; solo se omite si no se puede crear ni el enlace ni la unión. Premisa confirmada (prueba B). | — |
| O-5 | **Cerrado** | § Arranque: «sin compartir sesión, contexto, credenciales ni claves». Lo de «un humano con la misma cuenta no basta» no se trasladó a la semántica de R03. Ese caso ya lo cubre literalmente la regla de prevalencia de R03 («si se comparte con un autor alguno de esos elementos», incluido el usuario del sistema operativo, y vale para cualquier revisor). | Editorial; aceptado. |

## Hallazgos nuevos
| ID | Gravedad | Evidencia | Problema | Corrección mínima |
|---|---|---|---|---|
| GR-23 | LOW (proceso y verificación; AGENTS §3 Gate 2/3 y §5; «Toda revisión Quality identifica inequívocamente la versión»). Debe corregirse antes de la decisión del Owner. | § R01 Verificación: «En el Gate 2/3 de R01, Quality ejecuta el script sobre un clon limpio con `autocrlf=true` y con `false`, y comprueba `MATCH` y el hash del archivo extraído». § R01.2: `.gitattributes` hace que «su hash coincida en cualquier checkout (GR-05)». § R01.3: el script, si el archivo «aún no está [comiteado], lo indica sin fallar». Secuencia paso 3 y Autorización (GR-22): «commit solo tras PASS técnico en su Gate 2/3». Prueba A: el efecto de `-text` solo es observable en un clon **después de un commit**. Comparar con `PROPOSAL-v8.md:84`, paso 7 (precedente aprobado: comparación posterior al commit contra el manifiesto). | Antes de v6 ya existía, pero GR-22 hace vinculante el orden «Gate 2/3 → commit». (a) En el Gate 2/3 de R01, ningún clon limpio contiene todavía el archivo reconstruido ni `.gitattributes`. La comprobación del «archivo extraído», que sostiene GR-05, solo es posible si Quality improvisa un commit desechable no previsto en el plan. Si no, el Gate queda en PENDING (bloqueo circular) o aprueba GR-05 sin evidencia. (b) Nada comprueba después del commit que lo comiteado sea lo revisado. Para R01 ni siquiera se prevé un manifiesto de entrada; `GATE2-INPUT-04…` solo se menciona en R03. No hay PASS falso registrado. El riesgo es un PASS técnico sin la evidencia que el plan exige, o que el commit difiera de lo revisado. | Añadir a R01 (y, para el punto 2, a R03): (1) Gate 2/3 sobre un manifiesto append-only `GATE2-INPUT-0N.sha256`, con `git status --porcelain --untracked-files=all` y el hash de cada archivo; (2) Quality comprueba el efecto de `-text` con un commit desechable de esos archivos exactos en `%TEMP%`, clonado con `autocrlf=true` y `false`; (3) tras el commit, el Orchestrator vuelve a ejecutar el script sobre un clon limpio del nuevo HEAD con los dos valores de `autocrlf`, compara los archivos comiteados con el manifiesto y lo registra por adición. Quality lo revisa en el Gate siguiente (en el último, en la revalidación de la Opción A). |

### Observaciones no bloqueantes
- **O-6 (residual de O-1).** El SHA-256 crudo de un informe CRLF no es comparable con `evidence_sha256_lf` y depende de `autocrlf` en el checkout (prueba A). La solución más simple no necesita esperar a R03: `sha256_lf` está definido a nivel de bytes, así que el revisor puede calcularlo desde ahora con `python -B -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read().replace(b'\r\n',b'\n')).hexdigest())" <informe>`. Así se evita el periodo con hash crudo. Si se mantiene el crudo, hay que declarar su dependencia de `autocrlf` y que solo se compara con el crudo de un checkout `autocrlf=true` en Windows.
- **O-7 (residual de O-2).** Igual que en la tabla: hay que asignar quién compara la cita del Gate final y cuándo (por ejemplo, el revisor de la revalidación de GOV-002).

## Regresiones v5→v6, falsos PASS, alcance y afirmaciones
- **Regresiones:** ninguna. Solo se sustituyó el texto que pedía REVIEW-05: la cita en `03-IMPLEMENTATION.md` y «R01 sin condiciones». Se mantienen la clasificación, R01, el diseño y las reglas de R03, la tabla de responsabilidades, el inventario de tests (19 tests; suite en verde), § Detención y «Carácter».
- **Falsos PASS:** ninguno en el diseño de la CLI ni en la secuencia. GR-23 es el riesgo de un PASS técnico sin la evidencia prevista, no un PASS registrado. O-6 produce falsas alarmas, no aceptaciones.
- **Alcance:** sin sobrealcance ni frameworks. El texto crece unos 0,8 kB, limitados a lo pedido.
- **Afirmaciones:**
  - «`mklink /J` no requiere privilegios»: confirmado (prueba B).
  - «solo por adición… nunca editando `03-IMPLEMENTATION.md`»: coherente con R01.4, que rectifica sin editar.
  - «Ciclos previos: v1 FAIL; v2, v3 y v4 PWR»: exacto.
  - «Los subagentes del mismo runtime marcarán `NO_ACREDITADA`» sigue siendo prospectivo (solo tras R03), sin efecto, como ya señaló REVIEW-04.

## Estado por observación
| Obs. | Clasificación v6 | Estado |
|---|---|---|
| GOV-R01 | Bloqueo | Diseño correcto; queda condicionado a GR-23 (verificación de `-text` y comprobación posterior al commit). |
| GOV-R03 | Bloqueo | Diseño correcto; O-1..O-5 atendidas. Quedan O-6 y la parte (b) de GR-23. |
| GOV-R02 | Mejora futura (GOV-002) | Sin cambios; cerrado lo pedido. |
| Secuencia/Decisiones | — | GR-22 cerrado; GR-23 abierto. |

## Qué NO verifiqué
- `GOV-R01-reconstruct.py` adaptado ni ningún MATCH real: el script no existe en el repositorio y no ejecuté `files/gov-r01/reconstruct.py`. La prueba A usa archivos sintéticos, no la reconstrucción `f0f7392a…`.
- La implementación de R03, que no existe.
- Enlaces simbólicos en Linux/CI: solo comprobé que en Windows fallan sin privilegio (1314).
- Que `OWNER-DECISION-02.md`, que aún no existe, vaya a transcribir la Autorización.
- `git fsck`, las búsquedas de copias del original de GR-16 y las pruebas de firma de R02 (no las repetí).
- El piloto `protheus-efd`, el origen EPF `5ee75df` y otros consumidores de `quality_cli.py`.
- Que el contenido o las marcas de tiempo de la carpeta de sesión no se alteraran fuera de los hashes comprobados.

## Limitación de independencia
Soy un subagente del mismo runtime, sesión y usuario del sistema que el autor del plan (copilot-sdk-main) y que los revisores de los ciclos 1 a 5. Mi separación es solo contextual y no está acreditada. Con la semántica del plan, este informe declararía `NO_ACREDITADA` y no puede servir como `evidence_file` de un Gate formal en PASS o PWR. Su valor es técnico: un revisor independiente puede reproducir las comprobaciones descritas.
