# GOV-001 · Revisión Quality del plan de resolución GOV-R01..R03, ciclo 4

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r4
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) asignó este nombre al lanzar el subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime y no hay firma ni otro mecanismo que acredite la identidad.
**Independencia verificada:** no — separación solo contextual: no redacté GOV-001-R-PLAN-v1..v4 ni GOV-R-REVIEW-01..03 y no implementaré la misión, pero soy un subagente del mismo runtime, sesión y usuario del sistema que el autor (copilot-sdk-main); con la semántica de v4 este informe sería `NO_ACREDITADA`.
**Artefacto revisado:** GOV-001-R-PLAN-v4.md sha256:891a6ddd9441817d73a870a0351429010a272f58bc8acd2a14af84fbed943774
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v4 frente a v3 (`git diff --no-index --word-diff=plain`, exit 1 = hay diferencias), a `GOV-R-REVIEW-03.md`, a `AGENTS.md`, `agents/quality.md`, `OWNER-DECISION-01.md` y al código de PROTHEUSAI-CORE `6e5e929` (`scripts/quality_cli.py`, `tests/test_governance.py`). Pruebas propias en `%TEMP%` (borradas) con Python 3.12.0 (`python -B`) y Git 2.55.0.windows.3. Suite y `validate` ejecutados en solo lectura. No modifiqué el repositorio ni archivos existentes.

> Dictamen técnico, válido solo para la versión identificada arriba; no se transfiere a v5 ni posteriores. Según la decisión del Owner, PASS_WITH_RESERVATIONS **no habilita avanzar**: GR-20 y GR-21 deben corregirse en el plan antes de someterlo al Owner; el residual de GR-18 puede cerrarse en el Gate 1 de R03. Este informe no aprueba ningún Gate formal de `mission.json`.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash del plan v4 | `Get-FileHash` | `891A6DDD…943774` = encargo |
| Hashes previos | `Get-FileHash` | v3 `53B0FF3A…D8779E`, REVIEW-03 `DE109327…D69C0A`: coinciden |
| Repo | `git log -1`, `git status --porcelain --untracked-files=all --ignored` | HEAD `6e5e929`; salida vacía antes y después (exit 0) |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0; 19 `def test_` |
| Validación | `python -B scripts\quality_cli.py validate` | `OK …`, exit 0 |
| Inventario citado | `Select-String 'Independencia verificada'` en `tests/test_governance.py` | Líneas 74, 222–225, 231–233, 422 (la 68 es la firma de `record()` con el parámetro `independence`); `EXAMPLE-001/02-GATE1-REVIEW.md:5` y `GATE2-REVIEW-01.md:7`/`GATE3-EVIDENCE-01.md:7` (`f0f7392a…4a9b`) coinciden con lo citado |
| Alcance de `validate` | `quality_cli.py:232-251` (`report_text` solo sobre `evidence_file` de Gates no PENDING) | Los informes técnicos no referenciados en `mission.json` no se validan: la vía «dictamen técnico» de v4 no rompe `validate` |

## Pruebas propias de supuestos (`%TEMP%`, borradas)
| Supuesto (v4 § Rutas canónicas) | Prueba | Resultado |
|---|---|---|
| La gramática rechaza `\`, espacios, comas, `/` inicial o final, `//`, `:`, `~` | `re.match`/`re.fullmatch` con `^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*$` | **Verificado.** Admite `.`, `..`, `./a.md`, `a/../b` (por eso v4 los rechaza aparte: correcto). Con `re.match` + `$` acepta `'a.md\n'`; con `fullmatch` no. |
| Resolución por `os.listdir` independiente de plataforma | Carpeta con `Ev-01.md` y `sub/e.md` en Windows | `ev-01.md`, `SUB/e.md`, `Ev-01.md.` (punto final), `CON`, `nul`: rechazados por listado; `is_file()` ingenuo acepta los tres primeros. **Verificado.** |
| «Existe dentro de la misión» | Unión (junction) dentro de la misión hacia la carpeta padre (`mklink /J`, exit 0); el enlace simbólico no se pudo crear (WinError 1314) | La resolución segmento a segmento por `os.listdir` **acepta** `junc/outside.md` (archivo fuera de la misión); `resolve().is_relative_to(misión)` lo rechaza. Ver residual de GR-18. |

## Estado de los hallazgos previos
| ID | Estado | Evidencia en v4 | Residual |
|---|---|---|---|
| GR-01..07, GR-09..15 | Cerrados en ciclos anteriores; sin regresión | Texto sin cambios relevantes (diff v3→v4) | GR-09 sigue arrastrado al Gate 1 de GOV-002 |
| GR-08 (residual LOW) | **Cerrado en lo sustancial; queda una omisión, absorbida por GR-21** | § Secuencia paso 2 (`OWNER-DECISION-02.md`); párrafo «Carácter de los Gates de R01 y R03»: dictámenes técnicos, Gates y `owner_acceptance` siguen en PENDING; § Cierre ya decía «siguen en PENDING» | La autorización no figura en «Decisiones del Owner», como pedía REVIEW-03, y no se declara su condición ni el efecto bloqueante de los dictámenes técnicos (GR-21) |
| GR-16 (LOW) | **Cerrado** | § R01 Hechos, primer punto: «el autor declara…», corroboración parcial de Quality ciclo 3 «sin independencia acreditada», «No consta como hecho verificado». INCIDENT-01 (punto 4) remite a «la misma redacción de GR-13» | Al redactar INCIDENT-01, incluir expresamente este punto (Gate 2 de R01) |
| GR-17 (LOW) | **Cerrado** | `ACREDITADA` exige dos condiciones; «instancia de runtime distinta» definida operativamente (sesión, contexto, credenciales, claves, usuario del SO); subagente o subproceso lanzado desde la sesión del autor no cuenta; regla de prevalencia y «no verificable» → `NO_ACREDITADA`. El caso del ciclo 3 (otra instancia lanzada como proceso separado) queda en `NO_ACREDITADA` al compartir usuario del SO | Ver GR-20 (consecuencia no declarada para revisores humanos) |
| GR-18 (LOW) | **Cerrado en lo esencial; residual LOW para el Gate 1 de R03** | Gramática explícita; rechazo de `.`/`..`, `\`, `./`, espacios, comas, duplicados; comparación exacta contra `os.listdir`; test de mayúsculas también en Windows | (a) La contención «dentro de la misión» no se especifica para enlaces/uniones: la resolución por listado acepta una unión hacia fuera (prueba propia); falta `resolve()` + `is_relative_to` (ya usado en `quality_cli.py:50-51`) y un test con enlace. (b) Exigir `fullmatch` (o `\Z`), no `match` + `$`, y test con `\n` final |
| GR-19 (LOW) | **Cerrado** | § Principio: el revisor comunica `sha256_lf` calculado con `quality_cli.py hash`; el valor es comparable con `evidence_sha256_lf` | Observación no bloqueante: no se dice quién compara ni dónde se cita; y `hash` no existe hasta implementar R03, por lo que los dictámenes técnicos de R01 y del Gate 1 de R03 seguirán usando SHA-256 crudo (aceptable si se declara así) |

## Hallazgos nuevos
| ID | Gravedad | Evidencia | Problema | Corrección mínima |
|---|---|---|---|---|
| GR-20 | LOW (coherencia R03↔R02; consecuencia material no declarada). Condición antes de la decisión del Owner. | § R03 «Semántica…»: «persona distinta **o** instancia de runtime distinta»; «Regla de prevalencia: si se comparte con un autor **alguno de esos elementos** [sesión, contexto, credenciales, claves, usuario del SO]… `NO_ACREDITADA`». § R02 «Arranque»: «Requiere un revisor humano o un agente de otro runtime con un usuario del sistema distinto». | Nuevo en v4. Si la prevalencia rige para todos, un revisor **humano** que trabaje con el mismo usuario del SO bajo el que corre el agente autor (situación actual: los agentes corren con la cuenta del Owner) debe marcar `NO_ACREDITADA`, y la CLI bloqueará el PASS del Gate 1 de GOV-002 que el arranque presenta como resuelto con «un revisor humano». Si la prevalencia solo rige para instancias de runtime, vuelve una lectura ambigua del tipo que GR-17 quiso cerrar. v4 solo declara la consecuencia para «los revisores actuales de GOV-001». | Declarar expresamente si la prevalencia aplica también a personas (recomendado: sí, falla cerrado) y su consecuencia: con la configuración actual, ninguna revisión hecha bajo la cuenta del autor puede ser `ACREDITADA`. Alinear el «Arranque» de R02: «revisor humano o agente que no comparta usuario del SO ni credenciales con ningún autor, o excepción documentada del Owner». |
| GR-21 | LOW (proceso; AGENTS §3). Condición antes de la decisión del Owner. Absorbe el residual de GR-08. | § Secuencia: paso 2 «Autorización expresa del Owner para implementar R01 y R03» **antes** del paso 4 «GOV-R03: Gate 1 → implementación»; párrafo «Carácter»: los Gates de R01/R03 son dictámenes técnicos, no registrados. AGENTS §3: «Un Gate FAIL/BLOCKED prohíbe avanzar». `OWNER-DECISION-01.md` (C2): PWR no autoriza transiciones. | Nuevo en v4. Al sacar los Gates de R01/R03 de `mission.json`, la regla de bloqueo de AGENTS §3 deja de aplicarse por sí sola y el plan no dice que un dictamen técnico FAIL, PENDING o PWR detiene el avance. La autorización del paso 2, previa al Gate 1 de R03, no se declara condicionada a esos dictámenes; leída literalmente, autoriza implementar R03 con independencia del resultado del Gate 1. Además no figura en «Decisiones del Owner» (residual de GR-08). | Una frase en «Carácter» y en «Decisiones del Owner»: `OWNER-DECISION-02` autoriza implementar R01 y R03 **solo** tras dictamen técnico PASS de Quality en cada Gate aplicable (Gate 1 de R03 antes de tocar código; Gate 2/3 antes de cada commit); FAIL, PENDING o PASS_WITH_RESERVATIONS detienen el avance salvo excepción documentada del Owner. |

## Regresiones v3→v4, falsos PASS, alcance y afirmaciones
- **Regresiones:** ninguna en lo validado por la CLI. Se mantienen las comparaciones de Revisor, Dictamen, Artefacto y Autor, la verificación registrada del revisor (`quality_cli.py:252-264`), N42 y el inventario de tests. La frase «ningún Gate formal en PASS sin cumplir sus condiciones» se trasladó al párrafo «Carácter», no se perdió. GR-20 y GR-21 son huecos introducidos por el texto nuevo.
- **Falsos PASS:** ninguno en el diseño de la CLI. La vía de la unión/enlace (residual GR-18) no produce un PASS falso: el contenido queda fijado por `sha256_lf` y el revisor lo cita; solo deja de cumplirse «dentro de la misión». El riesgo de proceso de GR-21 es un avance sin dictamen favorable, no un PASS registrado.
- **Alcance:** sin sobrealcance ni frameworks; el diff v3→v4 se limita a los puntos pedidos (≈+1,4 kB).
- **Afirmaciones:** «Quality ciclo 3 corroboró en parte (historial de VS Code y Papelera), sin independencia acreditada» coincide con REVIEW-03. «En Windows rechaza las mismas variantes de mayúsculas que en Linux y el resultado no depende del sistema operativo» es correcto para mayúsculas, punto final y nombres de dispositivo (prueba propia), pero no cubre uniones de Windows frente a enlaces simbólicos de Linux (residual GR-18). «Los subagentes del mismo runtime marcarán `NO_ACREDITADA`» solo es aplicable tras implementar R03; antes (Gates de R01 y Gate 1 de R03) las plantillas vigentes usan `**Independencia verificada:**`. Imprecisión menor, sin efecto: esos dictámenes no se registran.

## Estado por observación
| Obs. | Clasificación v4 | Estado |
|---|---|---|
| GOV-R01 | Bloqueo | Correcto y mínimo; GR-16 cerrado. Verificación real del script adaptado pendiente para el Gate 2/3 de R01. |
| GOV-R03 | Bloqueo | Diseño correcto; GR-17 y GR-19 cerrados. Condición: GR-20 antes del Owner; residual de GR-18 en el Gate 1 de R03. |
| GOV-R02 | Mejora futura (GOV-002) | Sin cambios salvo la alineación del «Arranque» que pide GR-20. |
| Secuencia/Cierre | — | Condición: GR-21 (incluye el residual de GR-08). |

## Qué NO verifiqué
- `GOV-R01-reconstruct.py` adaptado ni ningún MATCH en este ciclo (el script no existe).
- La implementación de R03 (no existe); lo dicho sobre la CLI futura es análisis del plan más pruebas aisladas de la gramática y de la resolución por `os.listdir`.
- Enlaces simbólicos reales en Windows (sin privilegio, WinError 1314) ni en Linux/CI; solo una unión de directorio en Windows.
- `git fsck` ni nuevas búsquedas de copias del original (me apoyo en REVIEW-03 para GR-16).
- El piloto `protheus-efd`, el origen EPF `5ee75df`, otros consumidores de `quality_cli.py` y las pruebas de firma de R02 (no repetidas).
- Que las marcas de tiempo del sistema de archivos no hayan sido alteradas.

## Limitación de independencia
Soy un subagente del mismo runtime, sesión y usuario del sistema que el autor del plan (copilot-sdk-main) y que los revisores de los ciclos 1 a 3. Mi separación es solo contextual y no está acreditada; con la semántica de v4 este informe declararía `**Independencia:** NO_ACREDITADA`. No puede servir como `evidence_file` de un Gate formal en PASS o PWR. Su valor es técnico: las comprobaciones descritas son reproducibles por un revisor independiente.
