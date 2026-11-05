# GOV-001 · Revisión Quality del plan de resolución GOV-R01..R03, ciclo 2

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r2
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) asignó este nombre al lanzar el subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime y no hay firma ni otro mecanismo que acredite la identidad.
**Independencia verificada:** no — la separación es solo contextual. No redacté GOV-001-R-PLAN-v1/v2 ni GOV-R-REVIEW-01 y no implementaré la misión, pero soy un subagente del mismo runtime y sesión que el autor (copilot-sdk-main) y no hay prueba operativa de separación.
**Artefacto revisado:** GOV-001-R-PLAN-v2.md sha256:2a5aaa0262628b76f2845d52c658030aac484142532387042e957e4de3f093ae
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática del plan v2 frente al v1 (`656b67df…38fb`), a `GOV-R-REVIEW-01.md` (`e563c77f…d20e`), a `AGENTS.md`, a `agents/quality.md` y al código en PROTHEUSAI-CORE `6e5e929` (`quality_cli.py`, `tests/test_governance.py`, plantillas, `mission.json` y registros de GOV-001). Hice pruebas propias en `%TEMP%`, ya borradas, con Git 2.55.0.windows.3, OpenSSH de Windows y Python 3.12.0 (`python -B`). Ejecuté la suite actual en modo de solo lectura. No modifiqué el repositorio.

> El dictamen es técnico. Vale solo para la versión identificada arriba y no se transfiere a v3 ni a artefactos posteriores. Las reservas GR-11..GR-14 son **condiciones**: no se pueden ignorar al pasar a la siguiente fase. Ninguna parte de este informe aprueba un Gate formal de `mission.json`.

## Verificación de entradas
- Hash del plan v2 (`Get-FileHash`): `2A5AAA02…F093AE`, coincide con el encargo. También coinciden los hashes del v1 y de `GOV-R-REVIEW-01.md`.
- Estado del repositorio: `HEAD` = `6e5e92980a8e…`, rama `master`. `git status --porcelain --untracked-files=all --ignored` está vacío antes y después.
- Suite actual: `python -B -m unittest discover -s tests -q` → `Ran 19 tests … OK`, exit 0. Sirve como base para comparar en Gate 2/3 de R03.
- Manifiestos: CORE `EXAMPLE-001` y `GOV-001` son v2 con los tres Gates en PENDING. Piloto `protheus-efd`: `APP-001` v1 (PASS/PASS/PASS) y `EXAMPLE-001` v1. La afirmación «no hay ningún v2 con PASS ni PWR» se mantiene.

## Pruebas propias de supuestos técnicos (`%TEMP%`, borradas)
| Supuesto del plan | Prueba | Resultado |
|---|---|---|
| `.gitattributes` con la línea `<ruta> -text` hace que el hash del archivo coincida en cualquier checkout (GR-05) | Repo con `autocrlf=true`, archivo LF con la línea `-text` y un archivo de control sin atributo. Clones con `autocrlf=true`, `false` e `input`. | El archivo con `-text` coincide en los tres. El de control **no** coincide con `autocrlf=true`. **Verificado.** |
| Firma separada verificada pasando el contenido normalizado por stdin (GOV-002) | `ssh-keygen -Y sign -n protheusai-review`; `-Y verify` con stdin. | LF exacto: exit 0. CRLF, contenido alterado, namespace ajeno o principal ajeno: exit ≠ 0. **Verificado.** También confirma que normalizar es imprescindible. |
| Inventario de tests (GR-10) | Lectura de `test_governance.py` en `6e5e929` | 4 subcasos en `:222-225` y 3 en `:231-233` (7 en total). El helper `record()` está en `:68,74` y la plantilla rellenada en `:422`. No hay otros usos de `independence=` ni de la etiqueta. **Exacto.** |
| Citas de GR-07 | `GATE2-REVIEW-02.md:44` («depende de la palabra del revisor») y `:64` («no es reconstruible»); `03-IMPLEMENTATION.md:104` | Las líneas existen y dicen lo citado. **Verificado.** |

## Estado de los hallazgos previos
| ID | Estado | Evidencia en v2 | Residual |
|---|---|---|---|
| GR-01 (BLOCKER) | **Cerrado en estructura** | § GOV-R03 «Principio»: el token lo emite el revisor y el manifiesto lo replica. Hay igualdad exacta y test negativo «informe `true` con manifiesto `false`». | Dos problemas nuevos sobre la **semántica** del token y la garantía declarada: GR-11 y GR-14. |
| GR-02 | **Cerrado** (por eliminación) | Se excluyen las referencias `git:` y no hay dependencia de git ni del clon superficial. | — |
| GR-03 | **Cerrado con residual LOW** | Campo `evidence_sha256_lf`; los `sha256:` humanos no se recalculan. | No se añade un subcomando `hash` ni se dice cómo calcula el Orchestrator `sha256_lf` en Windows. No se declara expresamente que G2-13 sigue abierto para los hashes crudos históricos. La normalización no se define a nivel de bytes (GR-15). |
| GR-04 | **Cerrado con residual LOW** | La evidencia no puede ser el propio `evidence_file`. Hay tabla de tres filas para R03. | No se dice cómo presentará `status` la independencia («declarada, no verificada»), aunque el test `:411-415` limita «verificad[oa]». |
| GR-05 | **Cerrado** | Línea `-text` (comprobada arriba); script por `git show`; reproducción con `autocrlf` `true` y `false`. | — |
| GR-06 | **Cerrado con residual LOW** | `--repo` y `--commit`; borrado en `finally` que incluye archivos de solo lectura. El clon residual `gov-r01-*` ya no está en `%TEMP%`. | No se registra la versión de Git con la que se obtiene el MATCH (`diff --stat`). `git cat-file blob HEAD:<ruta>` debe tolerar que el archivo aún no esté comiteado. |
| GR-07 | **Cerrado** | INCIDENT cita `GATE2-REVIEW-02.md:44,64`; append-only no se impone por la CLI y así se declara. | — |
| GR-08 | **Cerrado** | Una clasificación por observación. Con la opción A, Gates y `owner_acceptance` en PENDING. Arranque de GOV-002 definido. | Precisar que el «PASS de los Gate 2/3» de R01 y R03 son dictámenes técnicos, no Gates formales, coherente con «siguen en PENDING». |
| GR-09 | **Cerrado** (diseño de GOV-002) | Ancla externa, condición de custodia, firmas separadas y vocabulario «atribución» / «separación de claves calculada». Viabilidad de stdin verificada arriba. | Se revisará en el Gate 1 de GOV-002. |
| GR-10 | **Cerrado con residual LOW** | Inventario exacto (verificado). | No se compromete a comparar el recuento de tests y aserciones antes y después (base: 19 tests). |

## Hallazgos nuevos
| ID | Gravedad | Evidencia | Problema | Corrección mínima |
|---|---|---|---|---|
| GR-11 | **MEDIUM** (GOV-R03; posible falso PASS). **Condición antes del Gate 1 de R03.** | § GOV-R03 «Diseño»: `**Conflicto de independencia:** false\|true` sin definición. La tabla asigna a Quality vigilar que «la narrativa no contradiga el token». Hoy `quality_cli.py:213-218` bloquea si el revisor escribe `no`. | El token pasa de una afirmación positiva («independencia verificada: sí — evidencia») a la ausencia de una negativa («sin conflicto»), y no define qué es un conflicto. Un revisor honesto en la situación actual (no es autor, pero es subagente del mismo runtime) puede escribir `false` con razón aparente y la narrativa «no verificada». La CLI lo aceptaría, cuando hoy lo bloquea: es una regresión de la misma clase que GR-01, pero por interpretación del revisor. Además, nadie revisa la coherencia narrativa↔token de un informe Quality: ese informe es la última revisión del Gate. *(Nota: el nombre del token salió de la corrección propuesta en GR-01. El defecto de definición es también de esa propuesta.)* | Definirlo en el protocolo y en las plantillas, fallando cerrado: `false` solo si el revisor no redactó ni implementó lo revisado **y** puede afirmar la separación con la evidencia citada. En cualquier otro caso, `true`, incluido «mismo runtime o sesión no excluido» o «no verificable». Pasar la coherencia narrativa↔token a la fila «No acreditado». Test: plantilla rellenada con `true` en PASS → error. |
| GR-12 | **MEDIUM** (GOV-R03; regresión v1→v2). **Condición antes del Gate 1 de R03.** | v1: `evidence:[{"ref","sha256"}]` y la CLI comprueba el hash. v2: `evidence:["<ruta>"]`, solo existencia. GR-03 de REVIEW-01 daba por supuesto `evidence[].sha256`. | Las evidencias de independencia se pueden sustituir o editar después de la revisión sin que la CLI lo detecte. El informe está fijado, pero lo que cita no. La regla append-only es solo documental (GR-07). El Owner pidió «evidencias referenciadas»: una referencia sin fijar no prueba qué se vio. | En el informe, `<ruta> sha256_lf:<64hex>` por evidencia. En el manifiesto, `evidence:[{"path","sha256_lf"}]`. La CLI recalcula e iguala. Test negativo: evidencia editada después del registro. Si se descarta, declararlo como limitación en la fila «No acreditado». |
| GR-13 | **MEDIUM** (honestidad, GOV-R01). Corregir antes de redactar INCIDENT-01. | Plan v2 § R01 «Hechos verificados»: «Quality lo verificó **de forma independiente** … y **sin posibilidad** de un MATCH engañoso» y «coinciden los 12 hashes parciales». REVIEW-01: «Independencia verificada: no»; «No, **según el análisis del código**»; «Límites»; y «procedencia de los 12 hashes … no encontré la salida». | Presenta una reproducción por un subagente del mismo runtime como verificación independiente, convierte un análisis con límites en una imposibilidad y da por verificados unos hashes parciales de procedencia no acreditada. Es justo lo que GOV-001 intenta evitar (AGENTS.md §5: separar lo verificado de lo declarado). | Reescribir: «Reproducido por Quality ciclo 1 (independencia no acreditada); según análisis del código no se identificó vía de MATCH engañoso; depende de que `f0f7…` sea el hash revisado en el ciclo 1». Pasar los 12 hashes parciales a «declarado por el autor». Aplicar la misma redacción en INCIDENT-01. |
| GR-14 | **MEDIUM** (honestidad, GOV-R03). Condición antes del Gate 1 de R03. | § GOV-R03 «Principio»: «El Orchestrator o el autor no pueden fijar la independencia del revisor: solo pueden copiarla». En GOV-001 el Orchestrator es el autor (`mission.json` roles) y es quien copia los informes al repositorio y calcularía `evidence_sha256_lf`. | Sin firma, el Orchestrator puede escribir o alterar el informe **antes** de fijarlo. La igualdad informe↔manifiesto solo impide la incoherencia, no la fabricación. La frase sobrestima la garantía, y la fila «No acreditado» no recoge la integridad del informe antes de fijarse. | Cambiar a: «no pueden fijarla sin alterar el informe; la autoría e integridad del informe antes de fijarse no se acreditan hasta GOV-002». Añadirlo a «No acreditado». Como mitigación sin código: el revisor comunica en su respuesta el SHA-256 de su informe y el Orchestrator lo cita (sigue siendo declarativo). |
| GR-15 | LOW (especificación) | § GOV-R03; `docs/MISSIONS/EXAMPLE-001/02-GATE1-REVIEW.md:5` contiene `**Independencia verificada:** [sí/no + evidencia]`; `quality_cli.py:55` lee con `read_text` (newlines universales). | (a) No se define el «conjunto canónico de rutas»: separador, mayúsculas (¿`canon()` aplica casefold a rutas?), rutas con comas, duplicados. (b) `sha256_lf` no se define a nivel de bytes: solo `\r\n`→`\n`, ¿y `\r` suelto? Con newlines universales sería otra cosa. (c) El informe de EXAMPLE-001 conserva la etiqueta eliminada y no figura en la lista de cambios. | (a) Comparar rutas POSIX exactas, sin casefold, separadas por `, `, sin comas en la ruta y sin duplicados. (b) `sha256(bytes.replace(b'\r\n', b'\n'))`. (c) Añadir `EXAMPLE-001/02-GATE1-REVIEW.md` a la lista o justificar por qué se excluye. |

## Regresiones v1→v2, falsos PASS y alcance
- **Regresiones:** GR-12, por omisión del hash de las evidencias. No encontré otras: se mantienen la comparación de Revisor, Dictamen, Artefacto y Autor, la exigencia de verificación del revisor por alguien distinto del autor (`quality_cli.py:253-259`) y la exclusión de autoaprobación.
- **Vías de falso PASS:** GR-01 queda cerrada en la vía Orchestrator. Queda abierta una vía por interpretación del token (GR-11). Con GR-11 corregido, un subagente del mismo runtime debe declarar `true` y no puede producir PASS ni PWR. Eso es coherente con la opción A, en la que los Gates quedan en PENDING.
- **Alcance:** sin sobrealcance. Las adiciones de v2 (una línea de `.gitattributes`, dos etiquetas y un campo de hash) responden a GR-01..GR-10. El diseño de GOV-R02 es solo documental y queda fuera de GOV-001. No hay frameworks: solo `subprocess` y `ssh-keygen`, previstos para GOV-002.
- **Conservación:** el plan no edita commits ni dictámenes y rectifica mediante INCIDENT. La reconstrucción se declara siempre como tal, salvo la redacción de GR-13 sobre quién la verificó.

## Estado por observación
| Obs. | Clasificación v2 | Valoración | Estado |
|---|---|---|---|
| GOV-R01 | Bloqueo | Correcta y de alcance mínimo. GR-05, GR-06 y GR-07 corregidos. | Puede avanzar. Condición: GR-13 en INCIDENT-01. Residual LOW: registrar la versión de Git. Verificación real del script adaptado en Gate 2/3 de R01. |
| GOV-R03 | Bloqueo | El diseño estructurado es correcto y cierra GR-01..GR-04 y GR-10. | Condiciones antes del Gate 1 de R03: GR-11, GR-12 y GR-14. GR-15 y los residuales LOW pueden resolverse en el Gate 1 de R03. |
| GOV-R02 | Mejora futura (GOV-002) | Una sola clasificación, con cierre formal diferido y arranque definido. | Sin condiciones aquí. GR-09 se arrastra al Gate 1 de GOV-002. |

## Qué NO verifiqué
- El script adaptado `GOV-R01-reconstruct.py`: no existe. No he ejecutado ningún MATCH en este ciclo (REVIEW-01 ejecutó el original).
- La implementación de R03: no existe. Las afirmaciones sobre la CLI futura son análisis del plan.
- La estabilidad de `git diff --stat` entre versiones de Git.
- El origen EPF `5ee75df` ni otros consumidores de `quality_cli.py` fuera de CORE y del piloto.
- La custodia de claves por usuarios distintos del sistema, ni claves FIDO.
- Que no existan copias del original borrado en otros lugares.

## Limitación de independencia
Soy un subagente del mismo runtime y sesión que el autor del plan (copilot-sdk-main), y del mismo runtime que el revisor del ciclo 1. Mi independencia es solo contextual y no está acreditada. Con la definición propuesta en GR-11, este informe declararía `Conflicto de independencia: true`. No puede servir como `evidence_file` de un Gate formal en PASS o PWR. Su valor es técnico: las pruebas descritas son reproducibles por un revisor independiente.
