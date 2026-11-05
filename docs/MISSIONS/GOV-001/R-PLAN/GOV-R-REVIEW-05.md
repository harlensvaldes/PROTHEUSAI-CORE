# GOV-001 · Revisión Quality del plan de resolución GOV-R01..R03, ciclo 5

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r5
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) asignó este nombre al lanzar el subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime y no hay firma ni otro mecanismo que acredite la identidad.
**Independencia verificada:** no — separación solo contextual: no redacté GOV-001-R-PLAN-v1..v5 ni GOV-R-REVIEW-01..04 y no implementaré la misión, pero soy un subagente del mismo runtime, sesión y usuario del sistema que el autor (copilot-sdk-main); con la semántica de v5 este informe sería `NO_ACREDITADA`.
**Artefacto revisado:** GOV-001-R-PLAN-v5.md sha256:04db987b81fbda6a9a0d0bd11e190b43667a354c54e1e3e43659a0e38fffdfbff
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v5 frente a v4 (`git diff --no-index --word-diff=plain`, exit 1 = hay diferencias), frente a `GOV-R-REVIEW-04.md`, `AGENTS.md`, `agents/quality.md` y `OWNER-DECISION-01.md`, y frente al repositorio PROTHEUSAI-CORE `6e5e929`. Pruebas propias de supuestos en `%TEMP%` (borradas) con Python 3.12.0 (`python -B`) y Git 2.55.0.windows.3. Suite y `validate` ejecutados en solo lectura. No modifiqué el repositorio ni ningún archivo existente.

> Dictamen técnico, válido solo para la versión identificada arriba; no se transfiere a v6 ni posteriores. Según la decisión del Owner, PASS_WITH_RESERVATIONS **no habilita avanzar**: GR-22 debe corregirse en el plan antes de someterlo al Owner. Las observaciones O-1 a O-5 no bloquean. Este informe no aprueba ningún Gate formal de `mission.json`.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash del plan v5 | `Get-FileHash` | `04DB987B…FDBFF` = encargo |
| Hashes previos | `Get-FileHash` | v4 `891A6DDD…943774` y REVIEW-04 `69C1A1DB…87AFF0`: coinciden |
| Repo | `git log -1`, `git status --porcelain --untracked-files=all --ignored` | HEAD `6e5e92980a8e…`; salida vacía antes y después (exit 0) |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 |
| Validación | `python -B scripts\quality_cli.py validate` | `OK — estructura consistente…`, exit 0 |
| CI | `.github/workflows/quality.yml:8,13`, `.gitea/workflows/quality.yml:9,15` | `ubuntu-latest`, Python 3.12 |
| `03-IMPLEMENTATION.md` | `Get-FileHash` frente a `GATE2-INPUT-03.sha256:66` | `963F1565…549620`: coincide (relevante para O-3) |
| Diff v4→v5 | `git diff --no-index --word-diff=plain` | Cambios limitados a: cabecera, § Principio (quién cita y quién compara), `re.fullmatch`, `resolve()`+`is_relative_to`, dos tests negativos, § Arranque, Secuencia pasos 2 y 4, párrafo «Detención» y línea «Autorización» en «Decisiones del Owner». Sin supresiones de contenido previo. |

## Pruebas propias de supuestos (`%TEMP%`, borradas; `cleaned: True`)
Carpeta `mission` con `Ev-01.md`, `sub/in.md`, unión `junc` → carpeta externa `outside` (con `x.md`) y unión `juncin` → `mission/sub`. Implementé en un script desechable la secuencia de v5: `re.fullmatch` → rechazo de `.`/`..` → resolución por `os.listdir` → `resolve()` + `is_relative_to(mission.resolve())` → `is_file()`.

| Entrada | Resultado | Lectura |
|---|---|---|
| `Ev-01.md` | OK | Positivo |
| `'Ev-01.md\n'` | rechazo (gramática) | `fullmatch` cierra el caso; `re.match('^…$')` lo **acepta** (comprobado: `True`) |
| `ev-01.md`, `Ev-01.md.` | rechazo (listado) | Mayúsculas y punto final en Windows |
| `junc/x.md` | rechazo (`outside`) | La unión hacia fuera, aceptada por el listado, la rechaza `resolve()`+`is_relative_to` |
| `juncin/in.md`, `sub/in.md` | OK | Unión que permanece dentro de la misión: aceptada, contenido fijado por hash |
| `a\b`, `./Ev-01.md` | rechazo | Gramática / segmento `.` |
| `mklink /J` sin privilegios | exit 0 | Las uniones se crean sin privilegio en Windows (ver O-4) |

## Estado de los hallazgos previos
| ID | Estado | Evidencia en v5 | Residual |
|---|---|---|---|
| GR-01..07, GR-09..17 | Cerrados en ciclos anteriores; sin regresión | Texto sin cambios en esos puntos (diff v4→v5) | GR-09 sigue arrastrado al Gate 1 de GOV-002 |
| GR-08 | Cerrado (su omisión se trató en GR-21) | «Decisiones del Owner» incluye ahora la autorización `OWNER-DECISION-02.md` | Ver GR-22 |
| GR-18 (residual LOW) | **Cerrado** | § Rutas canónicas: «con `re.fullmatch`…se rechaza también un salto de línea final»; «Además, aplica `Path.resolve()` + `is_relative_to(carpeta de la misión resuelta)`»; § Pruebas: salto de línea final y «enlace simbólico o unión… que apunta fuera». Supuestos confirmados por prueba propia. `is_relative_to` ya se usa en `quality_cli.py:50-51` (Python 3.12 en CI) | O-4 (omisión del test en Windows) |
| GR-19 (observación) | **Cerrado en lo pedido; parte (b) sin declarar** | § Principio: el Orchestrator cita el valor en `03-IMPLEMENTATION.md` o `POST-GATE-VALIDATION.md`; Quality lo compara en el Gate siguiente o en la auditoría con `evidence_sha256_lf` y el informe fijado | O-1 (`hash` aún no existe), O-2 (alcance de la comparación), O-3 (dónde se cita) |
| GR-20 (LOW) | **Cerrado** | § Arranque: «debe poder marcar `ACREDITADA` según la regla de prevalencia»; «otro usuario del sistema operativo o en otra máquina»; «Un humano que use la misma cuenta del sistema que el autor **no** basta»; excepción del Owner «que no se registra como PASS». Coherente con la prevalencia de § R03, que ya aplica literalmente a cualquier revisor («si se comparte con un autor alguno de esos elementos») | O-5 (editorial) |
| GR-21 (LOW) | **Cerrado en el cuerpo del plan; residual en el texto de autorización → GR-22** | Secuencia paso 2 (R03 condicionada al PASS técnico de su Gate 1), paso 4 «(solo con PASS técnico)», párrafo «Detención» (FAIL, PENDING o PWR en cualquier Gate de R01 o R03 detiene el avance; excepción solo por decisión documentada del Owner, nunca registrada como PASS) | La línea «Autorización» de «Decisiones del Owner» no recoge la condición de Gate 2/3 antes de cada commit y dice «R01 sin condiciones» |

## Hallazgos nuevos
| ID | Gravedad | Evidencia | Problema | Corrección mínima |
|---|---|---|---|---|
| GR-22 | LOW (proceso; jerarquía AGENTS §1). Condición antes de la decisión del Owner. | v5 «Decisiones del Owner»: «**Autorización (`OWNER-DECISION-02.md`):** R01 sin condiciones; R03 condicionada al PASS técnico de su Gate 1.» Frente a § «Detención»: «un dictamen técnico FAIL, PENDING o PASS_WITH_RESERVATIONS en cualquier Gate de R01 o R03 **detiene** el avance». AGENTS.md §1: las decisiones del Owner (nivel 1) prevalecen sobre el plan (nivel 4). REVIEW-04 GR-21, corrección mínima: «Gate 2/3 antes de cada commit». | Introducido en v5 al cerrar GR-21. El texto que el Owner aprobará y transcribirá en `OWNER-DECISION-02.md` autoriza R01 «sin condiciones» y solo condiciona R03 a su Gate 1. Como la decisión del Owner prevalece sobre el plan, leída literalmente autoriza el commit de R01, y el de R03 tras su Gate 1, aunque Gate 2/3 den FAIL, PENDING o PWR. Eso anula la cláusula «Detención» justo donde debe regir. No hay PASS falso registrado; el riesgo es que se avance sin dictamen favorable, el mismo de GR-21. | Redactar la línea así: «R01: implementar las adiciones sin condición previa; commit solo tras PASS técnico de su Gate 2/3. R03: implementar solo tras PASS técnico de su Gate 1; commit solo tras PASS técnico de su Gate 2/3. Se aplica la cláusula Detención.» Exigir que `OWNER-DECISION-02.md` la incluya literalmente o la cite. |

### Observaciones no bloqueantes
- **O-1 (residual de GR-19 b, de REVIEW-04).** El subcomando `hash` no existe hasta implementar R03. Los dictámenes técnicos de los Gates de R01 y del Gate 1 de R03 seguirán identificando informes con SHA-256 crudo, dependiente de `core.autocrlf`, que es `true` en este equipo. v5 no lo declara. Basta una frase en § Principio o en «Carácter».
- **O-2 (alcance de la mitigación de GR-19).** Tal como queda especificada, Quality compara dos valores escritos por el Orchestrator: la cita y `evidence_sha256_lf`. Así se detecta una alteración posterior a la cita, pero no un informe fabricado o alterado antes, porque la respuesta original del revisor no se conserva por un canal ajeno al Orchestrator. La tabla «No acreditado» («autoría e integridad del informe antes de fijarse») ya lo cubre y v5 la llama «mitigación declarativa», así que no hay afirmación falsa. Convendría decir expresamente que la comparación solo protege contra cambios posteriores a la cita. Además, la cita del Gate final no tiene «Gate siguiente» y queda a una auditoría que nadie ha programado.
- **O-3 (dónde se cita).** `03-IMPLEMENTATION.md` está fijado en las entradas de Gate (`GATE2-INPUT-02:63` `800e4a…`, `GATE2-INPUT-03:66` `963f15…`, que es el valor actual). Añadirle citas cambia su hash frente a la última entrada. Va en línea con la práctica histórica de añadir un bloque por ciclo, pero debe hacerse **solo por adición**, sin tocar el texto que INCIDENT-01 rectifica (§ R01, punto 4). Precisarlo en el Gate 1 de R03 o al redactar INCIDENT-01.
- **O-4 (test de enlaces, residual de GR-18).** «Si el sistema no permite crearlos, el test se omite» es demasiado laxo en Windows: las uniones de directorio se crean sin privilegio (`mklink /J`, exit 0, prueba propia). Solo debería poder omitirse el enlace simbólico. En CI (`ubuntu-latest`) los enlaces simbólicos sí se pueden crear. Concretarlo en el Gate 1 de R03. Los enlaces duros a archivos externos no se detectan con `resolve()`; no producen PASS falso porque el contenido queda fijado por `sha256_lf`.
- **O-5 (editorial, GR-20).** El § Arranque enumera «sesión, contexto ni claves» y omite «credenciales». La remisión expresa a la regla de prevalencia lo cubre. La aclaración de que un humano con la misma cuenta del SO no basta solo figura en R02. Conviene trasladarla a la semántica que irá a `QUALITY_EVIDENCE_PROTOCOL.md` (Gate 1 de R03), para que el protocolo no dependa del texto de GOV-002.

## Regresiones v4→v5, falsos PASS, alcance y afirmaciones
- **Regresiones:** ninguna. El diff solo añade o precisa contenido. Se mantienen la clasificación, R01, la tabla de responsabilidades, el inventario de tests (19 tests; suite en verde) y el párrafo «Carácter». GR-22 es un hueco introducido por el texto nuevo, no una pérdida.
- **Falsos PASS:** ninguno en el diseño de la CLI. La vía de la unión hacia fuera queda cerrada (prueba propia). El párrafo «Detención» y la excepción del Owner «que no se registra como PASS» evitan PASS inventados. GR-22 es un riesgo de avance sin dictamen favorable, no de PASS registrado.
- **Alcance:** sin sobrealcance ni frameworks. Los cambios se limitan a lo pedido en REVIEW-04 (+≈1,5 kB).
- **Afirmaciones:** «en Windows rechaza las mismas variantes de mayúsculas que en Linux» y «se rechazan los enlaces simbólicos y las uniones de directorio que salen de la misión» quedan confirmadas para uniones en Windows por prueba propia; los enlaces simbólicos no se probaron (ver «Qué NO verifiqué»). «Los subagentes del mismo runtime marcarán `NO_ACREDITADA`» sigue siendo aplicable solo tras implementar R03; es la misma imprecisión menor, sin efecto, que señaló REVIEW-04.

## Estado por observación
| Obs. | Clasificación v5 | Estado |
|---|---|---|
| GOV-R01 | Bloqueo | Sin cambios respecto a v4. Correcto y mínimo. La verificación real del script sigue pendiente para el Gate 2/3 de R01. |
| GOV-R03 | Bloqueo | Diseño correcto; GR-18 y GR-19 cerrados en lo pedido. O-1 a O-5 se pueden concretar en el Gate 1 de R03. |
| GOV-R02 | Mejora futura (GOV-002) | GR-20 cerrado. |
| Secuencia/Decisiones | — | Condición: GR-22. |

## Qué NO verifiqué
- `GOV-R01-reconstruct.py` adaptado ni ningún MATCH (el script no existe en el repositorio). No ejecuté `files/gov-r01/reconstruct.py`.
- La implementación de R03, que no existe. Lo dicho sobre la CLI futura se basa en el análisis del plan y en una simulación desechable de la secuencia de validación de rutas.
- Enlaces simbólicos reales: ni en Windows (no lo intenté; REVIEW-04 obtuvo WinError 1314) ni en Linux/CI. Solo probé uniones de directorio en Windows.
- `git fsck`, búsquedas de copias del original de GR-16 y pruebas de firma de R02 (no repetidas).
- El piloto `protheus-efd`, el origen EPF `5ee75df` y otros consumidores de `quality_cli.py`.
- Que la respuesta del revisor de ciclos futuros se conserve fuera del control del Orchestrator (O-2).
- Que las marcas de tiempo o el contenido de la carpeta de sesión no se hayan alterado fuera de los hashes comprobados.

## Limitación de independencia
Soy un subagente del mismo runtime, sesión y usuario del sistema que el autor del plan (copilot-sdk-main) y que los revisores de los ciclos 1 a 4. Mi separación es solo contextual y no está acreditada. Con la semántica de v5 este informe declararía `**Independencia:** NO_ACREDITADA` y no puede servir como `evidence_file` de un Gate formal en PASS o PWR. Su valor es técnico: las comprobaciones descritas las puede reproducir un revisor independiente.
