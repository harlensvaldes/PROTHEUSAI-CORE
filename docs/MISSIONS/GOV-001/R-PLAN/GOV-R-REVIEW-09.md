# GOV-001 · Revisión Quality del plan v9 (decisión del Owner sobre GOV-R03/GOV-R02), ciclo 9

**Dictamen:** PASS_WITH_RESERVATIONS
**Revisor:** quality-gov001-r9
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) me asignó este nombre al lanzar el subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento ni hay firma u otro mecanismo que acredite la identidad.
**Independencia verificada:** no — la independencia de autoría es solo declarada (no redacté GOV-001-R-PLAN-v1..v9 ni GOV-R-REVIEW-01..08 ni implementaré la misión); comparto runtime, sesión anfitriona, usuario del sistema, workspace y credenciales con el autor, y el encargo lo redactó el autor. Clasificación v9 al final del informe.
**Artefacto revisado:** GOV-001-R-PLAN-v9.md sha256:4c1f5f7bb03eed2536ff2c7f781a89e8f1889031abcaf21eac02485bab27876e
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v9 frente a v8 (`GOV-001-R-PLAN-v8.md`), la decisión del Owner transcrita en el encargo, `AGENTS.md`, `agents/quality.md`, `OWNER-DECISION-01.md` y el repositorio PROTHEUSAI-CORE `6e5e929` (`scripts/quality_cli.py`, `scripts/new_mission.py`, `tests/test_governance.py`, `quality/controls.json`, `quality/RISK_MATRIX.md`, `docs/templates/GATE{1,2,3}_*.md`, `docs/QUALITY_EVIDENCE_PROTOCOL.md`, `docs/QUALITY_POLICY.md`, `docs/MISSIONS/README.md`, manifiestos de `EXAMPLE-001` y `GOV-001`). Suite y `validate` en solo lectura con `python -B` (Python 3.12.0). No modifiqué el repositorio ni ningún archivo existente; no creé archivos propios en `%TEMP%` (la suite usa `TemporaryDirectory`, que se autoelimina).

> PASS_WITH_RESERVATIONS **no habilita avanzar**: v9 no puede someterse al Owner como plan aprobado ni citarse en `OWNER-DECISION-02` hasta corregir GR-24..GR-27 y pasar un nuevo ciclo. El dictamen se refiere solo al hash identificado arriba. La dirección del modelo (A/B/C separadas, autoría absoluta, aislamiento graduado, R02 a investigación) es fiel a la decisión del Owner; los defectos son locales y corregibles sin rediseño, por eso no es FAIL.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash de v9 | `Get-FileHash -Algorithm SHA256` | `4C1F5F7B…27876E`: coincide con el encargo. `sha256_lf` = `0f3c69827b470eea224ff1c1489b1f7e7a9a175d4fc1912db0c384da64588468` (11 620 bytes) |
| Base v8 citada | v9:3 | `sha256_lf 0d6bcca0…2a93`: coincide con el valor del encargo y con el registrado en `GOV-R-REVIEW-08.md` |
| Repo | `git log -1 --oneline`; `git status --porcelain --untracked-files=all --ignored` | `6e5e929`; 0 líneas antes y después |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 |
| Validación | `python -B scripts\quality_cli.py validate` | `OK — estructura consistente…`, exit 0 |
| Uso actual de `risk` en la CLI | `Select-String quality_cli.py -Pattern risk` | Solo enumeración (`:286`) e impresión (`:327`): hoy el riesgo **no** influye en ninguna regla |
| Decisión del Owner de 09:53 | búsqueda en `files\` y repo | **No existe registro escrito**; solo la paráfrasis del encargo |

## Fidelidad a la decisión del Owner
| Petición del Owner | v9 | Valoración |
|---|---|---|
| GOV-R01 aprobado | §0:9 sin cambios | Fiel |
| Distinguir autoría / aislamiento / garantía | §1:15-19 | Fiel en estructura; C no respalda lo que dice respaldar (GR-24) |
| Compartir runtime/usuario/workspace no anula autoría | §1:21, I1:25 | Fiel |
| Clasificación mínima y verificable, sin afirmar aislamiento inexistente | I0–I3, G0–G2 | B es solo declarado (lo dice, :18); C se presenta como «acreditada» con contenido que no lo acredita (GR-24) |
| Aislamiento proporcional al riesgo **y al tipo de Gate** | matriz :36-41 | Columnas de Gate idénticas y MEDIUM≡HIGH sin razonar (GR-28) |
| Un agente nunca aprueba su propio trabajo | A absoluta :17, R2, R8 | Fiel como norma; su aplicación sigue limitada a ids declarados (ver tabla siguiente) |
| Revisar necesidad de subir `schema_version` | :67, :98-101 | Justificado para B; falta el tratamiento de v2 con decisiones (GR-27) |
| Distinguir hash normalizado y de bytes | §2 | Mezcla «normalizado vs bytes» con «recalculado vs declarado» (GR-30) |
| Reducir controles documentales redundantes | :90-96 | Mayoritariamente correcto; uno de los eliminados no es redundante (GR-24) y desaparecen mitigaciones de v8 sin decirlo (GR-26) |
| R02: SSH solo investigación, sin dependencia | §4 | Fiel; sin dependencia de claves ni infraestructura |
| No ampliar GOV-001; portable, sencillo | B, sin dependencias | Sin funcionalidades nuevas fuera del encargo; tamaño de B no estimado con método (O-5) |

## Qué comprueba la CLI y qué solo se declara (v9, alternativa B)
| Elemento | Comprobado por la CLI | Solo declarado / no acreditado |
|---|---|---|
| A: revisor ∉ roles | Igualdad canónica de cadenas | Que los roles estén completos y que el id corresponda a una instancia real |
| A: `authorship_independent` | Tipo booleano y valor `true` | Veracidad de la afirmación |
| B: nivel I0–I3 | Enumeración y ≥ mínimo | Todo el contenido del nivel (v9:18 lo dice) |
| C: G1 | Existencia, ruta canónica y `sha256_lf` de ≥1 archivo | Que el archivo trate de aislamiento o identidad, quién lo produjo, su veracidad |
| C: G2 | Presencia y forma de `verification`, `by` ≠ autores/revisor | Que la verificación ocurriera; no cubre el nivel B declarado |
| Riesgo que selecciona la fila de la matriz | Enumeración | Quién lo fijó y si coincide con el evaluado por el revisor (GR-25) |
| Informe fijado | `review.sha256_lf` | Integridad antes de fijarse (mitigación de v8 retirada, GR-26) |

## Hallazgos

### GR-24 · MEDIUM · La garantía C no respalda A ni B: G1 se satisface con cualquier archivo y G2 no cubre el aislamiento
**Evidencia:**
- v9:19 define C como «¿Qué respalda A y B más allá de la palabra del revisor?»; v9:31 da G1 por «≥1 evidencia de aislamiento o identidad … dentro de la misión». La CLI solo puede comprobar existencia y hash (v9:85, :126); no hay tipo ni exclusiones. Con la lista de v9, citar `01-PLAN.md` o `03-IMPLEMENTATION.md` (archivos obligatorios de toda misión, `quality_cli.py:18-19`) da G1. La exclusión de v8 «no es el propio `evidence_file`» (GR-04, v8 § Reglas de la CLI) no se traslada: v9:85 solo hereda «rutas canónicas de v8».
- v9:32: G2 es la verificación de **identidad** del revisor y autores. En CRITICAL, la matriz exige I2 (v9:41) pero ningún nivel de C exige evidencia de que el revisor no pueda escribir: I2 queda siempre en la palabra del revisor.
- v9:95 clasifica R1/R4b (`quality_cli.py:236-244`) como «control redundante». No lo es: es hoy el único elemento atribuido a un tercero, exigido en todo PASS/PWR. Para MEDIUM y HIGH (GOV-001 es HIGH) se sustituye por G1, que, según lo anterior, puede no aportar nada. Es una relajación de fondo, legítima si el Owner la decide, pero presentada como eliminación de redundancia.

**Impacto:** falso PASS de garantía. Un Gate HIGH alcanza el mínimo citando el plan, y el Owner decidiría D2 creyendo que G1 aporta respaldo de aislamiento o identidad.

**Corrección mínima:**
1. Evidencias tipadas `{"kind": "isolation"|"identity", "path", "sha256_lf"}`. Se excluyen el propio informe, `mission.json`, los `MISSION_FILES` y el artefacto revisado.
2. Si `isolation` ≥ I2, G1 exige al menos una evidencia `kind: isolation`.
3. En G2, la verificación del tercero declara qué cubrió (identidad y nivel de aislamiento).
4. Alternativa: renombrar C a «trazabilidad de evidencias» y declarar que B es solo declarado en todos los niveles.
5. Mover R1/R4b de «redundantes» a «relajaciones sometidas a D2», indicando qué pierden MEDIUM y HIGH.

### GR-25 · MEDIUM · El riesgo y la matriz pasan a ser una palanca que el autor puede bajar sin tocar el informe del revisor
**Evidencia:**
- Hoy `risk` no afecta a ninguna regla (`quality_cli.py:286,327`; R1/R4b son universales). v9:34-41 hace que `mission.risk` elija el mínimo de I y G.
- `risk` lo escribe el Orchestrator en `mission.json` (`new_mission.py`) y el bloque del revisor (v9:72-79) no lo contiene. Basta bajar `CRITICAL` a `HIGH` en el manifiesto para pasar de I2·G2 a I1·G1 sin alterar ningún informe fijado.
- Esto contradice el principio que v8 mantenía y v9 no deroga: el autor u Orchestrator «no pueden fijar la independencia del revisor sin alterar su informe» (v8, GR-01/GR-14).
- La matriz vive en `quality/controls.json` «ajustable por el Owner sin tocar código» (v9:34). Ni la CLI ni el plan lo limitan al Owner ni validan el contenido: matriz completa, enumeraciones válidas, monotonía y comportamiento ante una clave ausente (`controls.json` actual tiene `schema_version: 1` y no la contiene).

**Corrección mínima:**
1. Añadir `risk` (y, de paso, `mission`, O-7) al bloque, con igualdad exigida respecto del manifiesto.
2. La CLI falla cerrado si la matriz falta, está incompleta, tiene valores no enumerados o no es monótona.
3. «I0 nunca basta» y la regla A quedan en código, no en datos.
4. Todo cambio de `controls.json` o de `risk` tras el Gate 1 se trata como cambio de política o de alcance: reabre Gate 1 y requiere al Owner (`QUALITY_POLICY.md` § Reapertura).

### GR-26 · MEDIUM · El delta v9 deja partes de v8 en estado indefinido o contradictorio y retira mitigaciones sin declararlo
**Evidencia:**
- v9:7-12 solo trata R01, R02, R03 y el Cierre. No dice qué ocurre con las secciones de v8 «Secuencia», «Detención», «Carácter de los Gates de R01 y R03» y «Decisiones del Owner».
  - «Carácter de los Gates» dice que los subagentes «marcarán `NO_ACREDITADA`» y que los Gates de GOV-001 «siguen en PENDING».
  - «Decisiones del Owner / GOV-R03» pide aprobar el token `ACREDITADA`/`NO_ACREDITADA`, que v9 elimina.
- v9:139 «Se mantiene la opción A de v8». Pero la opción A de v8 difiere el cierre formal a la revalidación con GOV-002, mientras v9:140 permite el cierre formal sin GOV-002, que pasa a ser solo investigación (§4). Ambas cosas no pueden ser ciertas a la vez.
- Como R03 de v8 queda «Sustituida» (v9:11), desaparecen sin justificación mitigaciones ya revisadas:
  - el revisor comunica en su respuesta el `sha256_lf` de su informe (GR-19);
  - el Orchestrator lo cita solo por adición;
  - las entradas append-only `GATE2-INPUT-05…` con `git status` y `sha256_lf`;
  - la comprobación tras el commit y `POST-GATE-VALIDATION-R03.md` (GR-23);
  - la comparación independiente asignada al cierre (O-7).

  En B, `review.sha256_lf` lo escribe el mismo Orchestrator que guarda el informe: sin la cita del revisor, nada detecta una alteración anterior a la fijación.
- v8 exige que `OWNER-DECISION-02` transcriba o cite «el plan aprobado por ruta y hash». Con v8 y v9 contradictorios, no hay un texto coherente que citar.

**Corrección mínima:**
1. Ampliar la tabla §0 a todas las secciones de v8 (conservada / sustituida / obsoleta), con una regla de prelación explícita.
2. Mantener, adaptadas a v3, GR-19, GR-23, O-7 y las entradas `GATE2-INPUT-05…`, o justificar su retirada.
3. Redactar las nuevas líneas de autorización de R03 para `OWNER-DECISION-02`.
4. Resolver la contradicción entre v9:139 y v9:140.

### GR-27 · MEDIUM · Inventario de impacto incompleto y migración de v2 con decisiones sin procedimiento
**Evidencia:**
- B cambia la estructura del manifiesto (v9:81-83), pero el plan no menciona:
  - `scripts/new_mission.py`, que hoy genera `schema_version: 2` con `reviewer`, `reviewed_artifact`, `evidence_file` y `date`. Las misiones nuevas nacerían en un esquema que v9:101 solo tolera en PENDING.
  - `docs/QUALITY_EVIDENCE_PROTOCOL.md` § Identidades, que hoy exige verificación registrada en todo PASS/PWR y las cinco etiquetas, y § Para todo Gate, que pide «prueba operativa de separación». Ambos contradirían a la CLI v3.
  - `docs/MISSIONS/README.md`, que solo tiene el procedimiento v1→v2.
  - `EXAMPLE-001/02-GATE1-REVIEW.md:5` (`**Independencia verificada:**`, que v8 sí incluía).
- El inventario de pruebas (v9:132) solo cita los casos de etiquetas. Rompen o deben cambiar también:
  - `test_malformed_records_fail_without_exceptions`, subcaso `'schema 3'` (`tests/test_governance.py:327`), que exige que v3 sea **inválido**;
  - `test_package_has_all_required_files_and_example_pending` (`:104`, `assertEqual(2, …)`);
  - `test_new_mission_starts_pending…`;
  - los helpers `record()`, `ident()` y `mission()` (`:24-79`), que usan los campos de Gate retirados;
  - `test_identities_need_registered_verification` (`:187-201`), cuyo comportamiento cambia con la matriz.
- v9:101 hace inválido cualquier v2 con decisión distinta de PENDING («migrar a v3»), incluido un FAIL. Sin embargo:
  - la migración exige un bloque JSON en el informe, y los informes históricos son append-only (`docs/MISSIONS/README.md`, § v1);
  - no hay vía equivalente a `mission.v1.json`;
  - un proyecto que use esta base con un v2 decidido vería fallar `validate` y su CI sin forma de cumplir. Los v1 con PASS, en cambio, se toleran como históricos.

**Corrección mínima:**
1. Listar todos los archivos afectados, incluidos `new_mission.py`, el protocolo, el README, `EXAMPLE-001/02` y `controls.json` con su versión.
2. Completar el inventario de tests, incluidos `'schema 3'` y `:104`.
3. Definir el tratamiento de los v2 con decisiones: históricos como v1 (aviso; nunca habilitan `can-*`) o renombrado a `mission.v2.json` con hash registrado. Un FAIL v2 no debe obligar a reescribir informes.

### GR-28 · LOW · La proporcionalidad por tipo de Gate que pidió el Owner no está razonada
**Evidencia:**
- v9:36-41 tiene columnas de Gate idénticas en todas las filas, y MEDIUM es igual a HIGH.
- El razonamiento (v9:43-46) solo trata el riesgo y una variante, D3.
- No explica por qué el aislamiento debe o no variar entre Gate 1 (plan: escribir el artefacto es poco relevante), Gate 2 (diff: un revisor con escritura puede alterar lo revisado, que es justo lo que define I2) y Gate 3 (ejecución: integridad de resultados).
- `quality/RISK_MATRIX.md` distingue MEDIUM de HIGH en profundidad («contrato formal + revisor independiente»).

**Corrección mínima:** justificar por Gate y por la pareja MEDIUM/HIGH la igualdad propuesta, o diferenciarla. Por ejemplo, en HIGH, Gate 2 con G1 de tipo `isolation` o I2. Presentarlo dentro de D2/D3.

### GR-29 · LOW · Las alternativas no son ortogonales y la C no es una opción real
**Evidencia:**
- A arrastra como «consecuencias» decisiones que no dependen del formato:
  - mantener R1/R4b (v9:62, :66), cuando la matriz y G2 son igual de aplicables en A;
  - la subida de esquema (v9:67), cuando v8 defendía lo contrario para un cambio aditivo.
- §6 separa D1 (A/B) de D2 (matriz), pero no define qué significa elegir «A + matriz».
- C (v9:108-109) se presenta como descartada porque no cumple la decisión; no es una alternativa. El Owner pidió «alternativas y consecuencias».

**Corrección mínima:**
1. Separar dos ejes: el formato (etiquetas + espejo / bloque único) y la política (R1/R4b universal / matriz).
2. Definir las combinaciones admitidas.
3. Sustituir C por una opción mínima real que cumpla la decisión, por ejemplo A sin subida de esquema y con matriz, con sus costes.

### GR-30 · LOW · Hashes: el eje relevante (recalculado vs declarado) no coincide con el nombre del campo
**Evidencia:**
- v9:53-56 asocia `sha256_lf` a «la CLI lo recalcula».
- Sin embargo, el bloque admite `artifact.ref: "git:… | sha256_lf:<hex> | sha256:<hex>"` (v9:74). El `artifact.name` es texto libre, sin ruta canónica, así que ese `sha256_lf` no puede recalcularse: un `sha256_lf` declarado quedaría indistinguible de uno verificado.
- El formato de `ref` es ambiguo (¿alternativas o concatenación con `|`?).
- `VERSION_ID` (`quality_cli.py:22`) no admite `sha256_lf:`, y v9 no dice cómo cambia.

**Corrección mínima:**
1. Separar en el bloque `artifact.ref` (declarado: `git:` | `sha256:` | `sha256_lf:`) y `artifact.path` opcional. Si la ruta está dentro de la misión, la CLI recalcula su hash.
2. Decir en §2 que la CLI recalcula **solo** los `sha256_lf` de `review` y `evidence`, y que cualquier otro hash es un identificador declarado, sea normalizado o de bytes.
3. Precisar la gramática de `ref`.

## Valoraciones solicitadas
- **¿Sigue siendo absoluta la regla de autoría?** Sí como norma: v9:17 no admite excepciones por riesgo ni por Gate, y se conservan R2, R8 y la exclusión del Orchestrator. La aplicación automática se limita a ids declarados y a un booleano autodeclarado; v9 lo dice en la columna «Qué comprueba la CLI». No hay retroceso respecto al código actual.
- **¿Hace falta schema v3?** En B, sí: se eliminan campos del manifiesto. En A es discutible (GR-29). En ambos casos lo que falta es el tratamiento de los v2 con decisiones (GR-27).
- **¿Elimina la reducción alguna protección necesaria?** El regex, el análisis de las cinco etiquetas, la detección de plantilla por texto y la duplicación de campos son redundantes una vez fijado el informe por hash. **No lo son** R1/R4b en MEDIUM/HIGH (GR-24) ni las mitigaciones GR-19/GR-23/O-7 de v8 (GR-26).
- **¿Hay sobrealcance?** No se añaden funcionalidades ajenas al encargo. R02 queda como investigación sin dependencias.

## Observaciones (no condicionan el dictamen)
- **O-1.** El ejemplo de I0 (v9:24, «el autor se revisa en el mismo hilo») es una violación de A, no un nivel de B. Mejor: «revisor distinto que recibe el historial o la memoria del autor».
- **O-2.** El nombre `G2_VERIFICADA` choca con C1 de `OWNER-DECISION-01.md` y con `UNQUALIFIED_CLAIM` (`tests/test_governance.py:21`, `:397-415`). Se propone `G2_VERIFICACION_REGISTRADA`, coherente con el vocabulario del protocolo.
- **O-3.** Especificar la delimitación exacta del bloque (cercado ```` ```protheusai-review ````, comportamiento con CRLF y con cercas anidadas). Hacer que el esqueleto de la plantilla falle cerrado y conservar como negativos explícitos «plantilla sin rellenar» (hoy en `:163-165`), «`gate` del bloque distinto de la clave del manifiesto» y «el mismo informe en dos Gates».
- **O-4.** No se dice si A, B y C se aplican a FAIL. Hoy R2 solo rige en PASS/PWR (`quality_cli.py:236`). Conviene decidirlo para no impedir registrar un FAIL de un revisor I0.
- **O-5.** «Balance de líneas cercano a cero» (v9:103) no tiene método. v8 estimaba unas 50 líneas para un cambio menor.
- **O-6.** §5 es autorreferente: el Architect de GOV-001 propone para HIGH el mínimo (I1·G1) que permite cerrar su propia misión sin un tercero, y las evidencias G1 de los subagentes las produciría ese mismo Orchestrator (v9:48). No es autoaprobación (decide el Owner y rige R8), pero D2 debería mostrar este conflicto de forma explícita.
- **O-7.** El bloque no contiene el id de la misión, así que un informe válido podría reutilizarse en otra misión con los mismos ids. Es una carencia previa, no una regresión; se resuelve con GR-25.
- **O-8.** I3 se define pero no se usa en la matriz. Es aceptable como nivel disponible para el Owner.

## Qué NO verifiqué
- El texto literal de la decisión del Owner de 2026-11-05 09:53: no hay registro escrito y me basé en la paráfrasis del encargo, redactada por el autor.
- Ninguna implementación de B: no hay prototipo ni medición de líneas. La revisión es solo estática.
- Las propiedades reales de LUNA o Cline (contexto, permisos, credenciales), y si los subagentes de GOV-001 cumplen I1.
- La existencia de proyectos derivados con manifiestos v2 que tengan decisiones (impacto de GR-27 fuera de este repo).
- La identidad de ningún participante.

## Limitación de independencia
- Soy un subagente lanzado por el autor (copilot-sdk-main) en el mismo runtime, sesión anfitriona, usuario del sistema operativo, workspace y credenciales. Tengo permiso técnico de escritura sobre el artefacto revisado; me abstuve de usarlo, pero eso no es verificable. El encargo lo redactó el autor e incluye su resumen de la decisión del Owner, además de referencias.
- **Clasificación con el modelo v9:**
  - **Autoría (A):** independiente **declarada**. No produje ni modifiqué v1–v9 y mi id no figura en ningún rol.
  - **Aislamiento (B):** `I1_CONTEXTO_SEPARADO` declarado, en el límite: contexto nuevo sin el historial del autor, pero con un encargo que contiene un resumen suyo y no solo referencias. No llega a I2 porque puedo escribir.
  - **Garantía (C):** `G0_DECLARADA`. No hay evidencia de lanzamiento fijada ni verificación de un tercero.
- Con la matriz propuesta, este informe **no alcanzaría** el mínimo de un Gate formal de GOV-001 (HIGH: I1·G1). Es un dictamen técnico sobre el plan, no un Gate de `mission.json`.
