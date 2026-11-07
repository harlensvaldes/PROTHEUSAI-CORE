# DET-001 · Gate 1 — Plan

**Estado:** DRAFT / PENDING INDEPENDENT REVIEW
**Architect:** Cline (identidad declarada)
**Orchestrator:** Cline (identidad declarada)
**Fecha:** 2026-11-07
**Riesgo:** MEDIUM — herramienta de verificación usada como evidencia; un resultado erróneo puede inducir una decisión equivocada
**Baseline:** HEAD `784c262071d6c63d3bf6034901bd4cd701f07ec0`; `git status --porcelain --untracked-files=all` sin cambios rastreados y con estas rutas no seguidas preexistentes: `docs/MISSIONS/CONTEXT-OPT-001/BASELINE-A.zip`, `docs/MISSIONS/CONTEXT-OPT-001/CHECKPOINT.md`, `docs/MISSIONS/CONTINUITY-002/06-DECISION.md`, `docs/MISSIONS/CONTINUITY-002/mission.json`, `docs/PORTABILIDAD-CLINE-DEEPSEEK-PLAN.md`. No se modifican. Línea base de pruebas ejecutada el 2026-11-07 en Windows, Python 3.13.12: `python -m unittest discover -s tests -v` → `Ran 270 tests in 59.923s` + `OK (skipped=4)` (sin fallos; 4 omisiones por privilegios de enlace/características del entorno).

## 1. Objetivo y aceptación verificable
Trasladar a `scripts/quality_cli.py` las comprobaciones mecánicas que hoy ejecutan agentes por razonamiento al contrastar expedientes:
(a) verificar manifiestos `*.sha256` con rutas y hashes `sha256_lf` (CRLF→LF), detectando archivos ausentes, hashes divergentes, rutas no canónicas, duplicados y entradas ambiguas;
(b) cruzar los hashes anclados en los manifiestos de una misión con el artefacto revisado y las evidencias registradas, informando discrepancias;
(c) clasificar cada ruta como gobernanza o producto/implementación, solo como dato informativo.

Aceptación verificable:
- `python scripts/quality_cli.py manifest <ruta> --root <raíz>`: 0 si todas las entradas coinciden; 1 si hay discrepancias, incluido un manifiesto legible sin entradas; 2 solo si la ruta falta en la invocación (`parser.error`) o el manifiesto no puede leerse/decodificarse. La salida respeta el orden del manifiesto e incluye conteos por clase.
- `python scripts/quality_cli.py audit --mission <ID> --root <raíz>`: 0 si el registro es coherente con las anclas (los avisos de deriva no bloquean), 1 si hay discrepancias de registro, 2 con error de uso o lectura. La integridad del árbol frente al manifiesto se comprueba con `manifest`, no con `audit`.
- Pruebas nuevas en `tests/test_det001.py` (positivas, negativas y de regresión); la suite completa sigue en verde con el mismo resultado que la línea base.
- `validate`, `status`, `can-implement` y `can-close` no cambian de comportamiento ni de reglas.

## 2. No objetivos y restricciones
- No se implementan M2 ni M3.
- No se modifica qué artefactos forman parte de un Gate, ni `quality/controls.json`, ni la semántica v1–v5.
- No se alteran expedientes históricos ni APP-001; DET-001 es un registro nuevo.
- No se autentican identidades, no se certifica aislamiento y la CLI no emite dictamen de Quality.
- Solo biblioteca estándar; sin dependencias, CI, servicios ni ficheros de configuración nuevos.
- Sin escritura en Git, sin push y sin despliegue; los cambios quedan en el árbol de trabajo.

## 3. Arquitectura actual acreditada
- `scripts/quality_cli.py` (377 líneas): comandos `validate`, `status`, `can-implement`, `can-close`, `hash`; entre otras funciones, `read_json`, `canon`, `ident_errors`, `structure_errors`, `mission_errors`, `project_report`, `print_status` y `main`; convención de códigos ERROR=2, FAIL=1, OK=0.
- `scripts/quality_v3.py`: `digest()` calcula SHA-256 tras normalizar CRLF→LF; `canonical_file()` rechaza rutas no canónicas, `..`, enlaces y escapes de la raíz; `parse_block()` lee el bloque `protheusai-review`; `gate_errors()` ya recalcula `review.sha256_lf`, hashes de evidencias y `artifact.path` cuando la referencia es `sha256_lf:`.
- Vacío actual: ningún comando interpreta manifiestos `*.sha256`; nadie comprueba sus entradas ni las cruza con el registro. Manifiestos reales en este repositorio que hoy solo se verifican a mano: `docs/MISSIONS/BOOTSTRAP-001/GATE2-INPUT-04.sha256` (5 entradas), `docs/STRUCTURAL-CONSISTENCY-INPUT.sha256` y `CORE-REVIEW-INPUT-01.sha256`. La referencia del Owner es la retrospectiva de APP-001 en el repositorio externo CLINE-LAB-001 (no presente aquí): `docs/MISSIONS/APP-001/POST-ACEPTACION-02.md` §1 registra «18/18 coinciden» contra `GATE2-INPUT-09` y `POST-GATE-VALIDATION-04.md` repite la comparación post-commit; `EVIDENCE-INDEX-01.sha256` (también externo a este repositorio) documenta el índice de evidencias. Es una referencia de motivación, no una fuente de este repositorio.
- Restricción de reutilización: `quality_v3.digest` y `quality_v3.canonical_file` son la única implementación de hash LF y de canonización de rutas; `parse_block` es el único lector del bloque de revisión; las nuevas funciones deben usarlas, no reimplementarlas.
- Deriva histórica conocida y aceptada: en la línea base, 25 de los 26 manifiestos reales del repositorio ya no coinciden con los bytes actuales por evolución posterior del árbol (p. ej. `GOV-001/GATE2-INPUT-03.sha256`, `DELIVERY-001/GATE2-INPUT-01.sha256`, `BOOTSTRAP-001/GATE2-INPUT-01..03.sha256`); el diseño lo absorbe porque la deriva es aviso en `audit`. `CORE-REVIEW-INPUT-01.sha256` y `CORE-REVIEW-INPUT-02.sha256` anclan `docs/MISSIONS/README.md` y `docs/QUALITY_EVIDENCE_PROTOCOL.md`; ambos ya divergen en la línea base y DET-001 modifica además `docs/QUALITY_EVIDENCE_PROTOCOL.md`, de modo que `manifest` sobre esas anclas devolverá 1. No se reescriben ni se crea un ciclo nuevo para ellas, porque su función era identificar una revisión anterior. La misión nueva usa su propio `GATE2-INPUT-01.sha256`.
- Discrepancia histórica de trazabilidad ya presente (no se corrige en esta misión): `DOC-001` registra `04-GATE2-REVIEW.md` con `252a90af…`, que es el hash actual del archivo, mientras `GATE2-INPUT-01.sha256:30` ancló `536764bc…`; `DISCOVERY-001` registra `04-GATE2-REVIEW.md` y `05-GATE3-EVIDENCE.md` con `278c1a19…`/`7f819d43…` y sus anclas son `33abb8c0…`/`559bdafd…`. Son casos «registro == árbol ≠ ancla»: `audit` los reportará como discrepancia (ver §4.3) y no se modifican sus expedientes.

## 4. Diseño propuesto

### 4.1 Superficie de la CLI (solo `scripts/quality_cli.py`)
```text
python scripts/quality_cli.py manifest <ruta> [--root RAÍZ]
python scripts/quality_cli.py audit --mission ID [--root RAÍZ]
```
No se añaden módulos, dependencias ni comandos ajenos; las funciones nuevas viven en `quality_cli.py` y reutilizan `quality_v3.digest`, `quality_v3.canonical_file`, `quality_v3.parse_block` y `quality_cli.mission_errors`.

### 4.2 Parser de manifiestos
- Formato admitido: `hash  ruta` con **uno o más** espacios o tabuladores entre hash y ruta, opcionalmente precedido por **cualquier token de estado de `git status --porcelain=v1`** (` M `, `M `, `A `, `D `, `R `, `C `, `U `, `??`, `!!`; el token se acepta con uno o dos caracteres del conjunto `[ MADRCU?!]`). El separador puede ser un único espacio, como en `CORE-REVIEW-INPUT-01.sha256`. Caso real con `!!`: `docs/MISSIONS/DESIGN-001/GATE2-INPUT-01.sha256:36`. Las líneas vacías y las que empiezan por `#` se **ignoran siempre, aunque contengan un token de 64 hexadecimales** (caso real: `GOV-001/GATE2-INPUT-04.sha256:76` y `GATE2-INPUT-05.sha256:86`, comentarios `# sha256 raw reconstructed …`). Las líneas sin token de 64 hexadecimales (prosa, encabezados `HEAD …`, vallas ```` ``` ````) también se ignoran sin aviso, porque los expedientes reales contienen documentos con prosa (p. ej. `docs/MISSIONS/DELIVERY-001/GATE2-INPUT-04.sha256`).
- Ambigüedad: fuera de comentarios, si una línea contiene un token de 64 hexadecimales que no casa con la gramática de entrada (por ejemplo 65 hexadecimales o texto pegado), es error; no se adivina la intención.
- Se normaliza CRLF→LF con `digest()`; la comparación de hashes es case-insensitive; la ruta declarada debe ser relativa a `--root`, canónica y resoluble, sin `..`, sin unidades o rutas absolutas y sin enlaces; la comprobación la realiza `canonical_file`, no una copia.
- Errores bloqueantes: hash divergente, archivo ausente/no regular/fuera de la raíz, ruta duplicada en el manifiesto, línea ambigua, manifiesto sin entradas.
- Resolución de rutas: el argumento `<ruta>` del manifiesto se resuelve contra el directorio de trabajo actual (como `hash`); `--root` solo es la base para resolver las rutas **de las entradas**. Un `--root` inexistente no impide leer el manifiesto: cada entrada resulta no resoluble y produce error 1. Si el manifiesto no existe, no se puede leer o no es UTF-8 válido, el código es 2.
- La lectura del manifiesto usa `utf-8` y una sola pasada; cualquier `OSError`/`UnicodeError` termina con código 2 e informe de la ruta.
- Alcance temporal: `manifest` contrasta el manifiesto contra los bytes actuales de `--root`, por lo que **un manifiesto histórico puede dejar de coincidir** cuando el árbol evoluciona; `manifest` verifica el estado actual y no reconstruye historia. `audit` no usa el árbol como autoridad (ver §4.3).

### 4.3 `audit` (cruce registro ↔ manifiestos)
1. Carga `mission.json` y ejecuta `mission_errors` (comportamiento existente reutilizado: estructura, hashes de informes, evidencias, rutas, política). Sus errores se informan como discrepancias del registro.
2. Lee con el mismo parser todos los `*.sha256` de la carpeta de la misión sin verificarlos contra el árbol. Las rutas de los manifiestos son **relativas a la raíz del repositorio** (`docs/MISSIONS/BOOTSTRAP-001/GATE2-INPUT-04.sha256` → `scripts/bootstrap001.py`), mientras que `gate.review.file` y las evidencias del bloque son **relativas a la carpeta de misión** (`quality_v3.canonical_file(folder, name)`). El cruce normaliza ambas bases: `ruta_registro → docs/MISSIONS/<ID>/<ruta_registro>`.
3. Separación de responsabilidades (corrige el riesgo de deriva):
   - **Autoridad del registro**: `gate.review.file` y cada evidencia se comparan con las anclas. Si su hash registrado no coincide con **ninguna** ancla de esa ruta → discrepancia (error). Si coincide con un ciclo anterior pero no con el efectivo → aviso de versión no vigente. Si la ruta no figura en ningún manifiesto → aviso explícito de que no es requisito de Gate.
   - **Caso «registro == árbol ≠ ancla»**: el hash registrado coincide con los bytes actuales (por tanto `mission_errors` lo acepta) pero no con ninguna ancla. Es una **discrepancia de trazabilidad** (error con mensaje propio: `versión registrada no anclada`), porque el artefacto revisado no está identificado por ningún manifiesto del expediente. No se degrada a aviso: es exactamente la clase de deriva que la misión debe detectar. Casos reales ya presentes: `DOC-001` y `DISCOVERY-001` (ver §3); `audit` devolverá 1 en ellos y no se modifican sus expedientes.
   - **Deriva del árbol**: si el ancla efectiva no coincide con los bytes actuales pero el registro sí coincide con un ancla, es un **aviso** (`deriva del árbol respecto al ancla efectiva`), nunca un error. La comprobación de integridad completa contra el árbol es responsabilidad explícita de `manifest`.
   - **Ancla efectiva** (solo para ordenar avisos de vigencia): clave de ciclo = entero `nn` de `-<nn>` en `*-<nn>[.RECONSTRUCTED].sha256`, comparado numéricamente (9 < 10); si no hay sufijo, 0. Desempate: primero el original sobre la reconstrucción (`GATE2-INPUT-01.RECONSTRUCTED.sha256` pierde frente a `GATE2-INPUT-01.sha256` si ambos existen) y después el nombre. Una reconstrucción sin original sigue siendo el ancla efectiva de su ciclo.
   - Si el bloque `protheusai-review` no es interpretable, aviso y se omite el cruce de evidencias (el defecto del bloque ya lo reporta `mission_errors`).
   - No se emite error por anclar rutas de otro expediente (`docs/MISSIONS/<otra>/…`): es un uso legítimo observado en `GOV-001/GATE2-INPUT-10.sha256`, que ancla registros de `EXAMPLE-001`.
4. Los avisos no cambian el código de salida (0); cualquier discrepancia de registro lo fija en 1. Un `mission.json` ausente o ilegible devuelve 2. Una misión sin manifiestos se informa y no falla por ausencia de anclas. En los `*.sha256` de la misión, un manifiesto ilegible o no UTF-8 devuelve 2 (no puede verificarse), mientras que un formato inválido (línea ambigua, sin entradas) es una discrepancia del expediente y devuelve 1, identificando el archivo. Si coexisten una lectura imposible (2) y discrepancias de registro (1), prevalece 2: no se emite un diagnóstico parcial como si la verificación hubiera terminado.

### 4.4 Clasificación producto/gobernanza
Función pura `classify(path)` con reglas explícitas: `gobernanza` para `docs/`, `quality/`, `agents/`; para los archivos raíz `AGENTS.md`, `START_HERE.md`, `CONTRIBUTING.md`, `FILE_INDEX.md`, `README.md`; y para los registros sueltos de raíz que casan `^(PLAN|REVIEW|OWNER|CORE)-.*\.(md|sha256)$`. Todo lo demás (`scripts/`, `tests/`, `src/`, `app/`…) es `producto/implementación`. Es una heurística de presentación: solo alimenta los conteos de la salida y no altera la verificación ni la pertenencia de un artefacto a un Gate. La salida lo declara literalmente.

### 4.5 Salida, códigos y despacho
Formato estable y en español, con una línea de resumen y un ` - ` por discrepancia, respetando el vocabulario existente (`OK — …`, `FAIL (…)`, `ERROR: …`). Sin PASS de Quality. Los comandos son de solo lectura: no escriben manifiestos ni artefactos derivados. El despacho de `manifest` ocurre antes de exigir `--mission`, para no romper la invocación sin misión; `audit` reutiliza la validación de ID y la ruta de misión ya existentes.

### 4.6 Alternativas descartadas
- Integrar la verificación de manifiestos en `validate`: obligaría a interpretar manifiestos históricos y podría convertir discrepancias preexistentes en fallos globales; cambia el contrato de `validate`.
- Añadir un ejecutable propio o CI: duplica infraestructura y contradice el alcance.
- Reimplementar hash/canonización: duplicaría `digest`/`canonical_file` y crearía dos definiciones de `sha256_lf`.

## 5. Matriz de impacto
| Archivo | Acción | Riesgo | Compatibilidad |
|---|---|---|---|
| `scripts/quality_cli.py` | añadir parser de manifiestos, clasificación, `manifest`, `audit`, salida y ayuda | MEDIO: resultados erróneos podrían inducir decisiones; se mitiga con pruebas negativas y sin PASS | Aditivo: comandos y funciones nuevas; los existentes no cambian |
| `tests/test_det001.py` | nuevo: positivas, negativas y regresión de la CLI | Bajo | No altera pruebas existentes |
| `docs/QUALITY_EVIDENCE_PROTOCOL.md` | documentar los dos comandos, la precedencia de ciclos y sus límites | Bajo | Solo texto; no cambia reglas |
| `README.md` | añadir los dos comandos a la sección de comandos de la CLI | Bajo | Solo texto; no cambia reglas |
| `docs/MISSIONS/DET-001/*` | expediente de esta misión (plan, informes, evidencias, decisión) | Bajo | Registro nuevo; no toca expedientes históricos |
| `quality/controls.json`, `quality_v3.py`, `quality_v4.py`, `quality_v5.py` | sin cambios | — | Semántica de Gates intacta |

## 6. Escenarios negativos
- Hash declarado distinto del real; archivo borrado; archivo convertido en directorio; ruta con `..`, absoluta o con separadores de Windows.
- Manifiesto inexistente, ilegible o sin entradas; línea con 63 caracteres hexadecimales o con texto añadido; ruta duplicada.
- Manifiesto con CRLF en el archivo de destino: el hash LF debe coincidir (normalización, no cambio de bytes).
- Misión sin manifiestos: `audit` informa y no falla por ausencia de anclas.
- Varios ciclos `GATE2-INPUT-01..09` con hashes distintos para la misma ruta, incluida una reconstrucción: el ancla efectiva se elige por ciclo numérico y, a igual ciclo, el original prevalece sobre `.RECONSTRUCTED`; el histórico no produce 1.
- Deriva del árbol: un ancla efectiva que ya no coincide con los bytes actuales produce aviso, no error; un registro cuyo hash no casa con ninguna ancla sí es error.
- Registro con ruta relativa a la misión pero manifiesto relativo a la raíz: el cruce debe casar tras normalizar `docs/MISSIONS/<ID>/<ruta>`. Anclar registros de otro expediente es legítimo y no es error.
- Caso «registro == árbol ≠ ancla»: es discrepancia (1) con mensaje `versión registrada no anclada`; no se confunde con deriva del árbol. La prueba lo distingue del caso en que el registro coincide con un ancla y el árbol ha derivado (aviso, 0).
- Misión sin manifiestos: 0 con mensaje informativo. Manifiesto de misión ilegible/no UTF-8: 2. Manifiesto de misión con formato inválido: 1. Si coexisten ilegibilidad y discrepancias, prevalece 2. `<ruta>` del manifiesto se resuelve desde el directorio de trabajo, no desde `--root`.
- Manifiestos reales con prosa, vallas, separador de un solo espacio o comentarios `#` que contienen un hash de 64 hexadecimales: se interpretan solo las líneas con gramática de entrada; los comentarios se ignoran aunque incluyan hash.
- Registro incoherente (informe alterado, evidencia ausente, bloque inválido): `audit` falla por la vía de `mission_errors` y añade aviso si no puede cruzar evidencias.
- Enlace simbólico o junction: `canonical_file` los rechaza. La prueba de enlace se omite con `skip` si el entorno Windows no concede el privilegio, igual que la suite existente; se declara como limitación de la evidencia, no como PASS.
- Fallo de recuperación/rollback: los comandos son de solo lectura; revertir el cambio es restaurar los dos archivos de código/pruebas y el texto documental, sin migraciones ni datos afectados.

## 7. Matriz de pruebas
| Contrato | Prueba (nueva, `tests/test_det001.py`) | Estado | Evidencia |
|---|---|---|---|
| Manifiesto válido con CRLF, prefijo de estado y comentarios | `test_manifest_valid_crlf_status_and_classification` | NOT_RUN | código de salida 0 y conteos gobernanza/producto |
| Hash divergente, ausente, duplicado, ruta no canónica | `test_manifest_reports_mismatch_missing_duplicate_and_unsafe_paths` | NOT_RUN | código 1 y mensajes por ruta |
| Manifiesto inexistente, ilegible o con bytes no UTF-8 | `test_manifest_unreadable_returns_two` | NOT_RUN | código 2 |
| Líneas ambiguas y manifiesto vacío | `test_manifest_ambiguous_and_empty` | NOT_RUN | error 1 para línea ambigua y para manifiesto vacío |
| Prosa, vallas, separador de un solo espacio y comentarios `#` con hash | `test_manifest_prose_and_single_space` | NOT_RUN | solo se interpretan las líneas válidas; comentario con 64 hex ignorado |
| Tokens de `git status --porcelain` incluido `!!` | `test_manifest_porcelain_tokens` | NOT_RUN | código 0 con ` M `, `??` y `!!` |
| Hex en mayúsculas y CRLF | `test_manifest_hash_is_case_insensitive` | NOT_RUN | código 0 |
| `--root` inexistente o entrada fuera de la raíz | `test_manifest_root_missing_or_outside` | NOT_RUN | manifiesto legible; código 1 por ruta no resoluble |
| Enlace/reparse point rechazado | `test_manifest_rejects_symlink` (skip si el entorno no concede privilegio) | NOT_RUN | error de ruta o skip declarado |
| `audit` con anclas correctas | `test_audit_anchored_consistency_passes` | NOT_RUN | código 0 |
| `audit` detecta divergencia registro↔ancla | `test_audit_detects_record_divergence` | NOT_RUN | código 1 |
| `audit` con varios ciclos, reconstrucción y orden numérico | `test_audit_multi_cycle_precedence` | NOT_RUN | histórico no bloquea; ancla efectiva correcta |
| `audit` informa deriva del árbol como aviso | `test_audit_tree_drift_is_warning` | NOT_RUN | registro coincide con ancla; árbol derivado → 0 + AVISO |
| `audit` detecta «registro == árbol ≠ ancla» | `test_audit_record_not_anchored` | NOT_RUN | código 1 con `versión registrada no anclada` |
| `audit` distingue formato inválido (1) de manifiesto ilegible/no UTF-8 (2) | `test_audit_invalid_vs_unreadable_manifest` | NOT_RUN | códigos 1 y 2 respectivos |
| `audit` prioriza 2 sobre 1 cuando un manifiesto es ilegible y hay discrepancias | `test_audit_unreadable_takes_precedence` | NOT_RUN | código 2 |
| `audit` sin manifiestos informa sin fallar | `test_audit_mission_without_manifests` | NOT_RUN | código 0 + mensaje |
| `audit` no falla por anclar otro expediente | `test_audit_foreign_mission_anchor_is_not_error` | NOT_RUN | código 0 |
| `<ruta>` del manifiesto se resuelve desde el directorio de trabajo | `test_manifest_path_resolved_from_cwd` | NOT_RUN | manifiesto en tempfile fuera de `--root`, entradas resolubles dentro de `--root`: código 0 |
| `audit` casa rutas relativas a misión contra manifiesto relativo a raíz | `test_audit_maps_mission_relative_to_repo_relative` | NOT_RUN | código 0 con `docs/MISSIONS/<ID>/<ruta>` |
| `audit` avisa de ancla ausente sin fallar | `test_audit_missing_anchor_is_warning_only` | NOT_RUN | código 0 + AVISO |
| `audit` reutiliza comprobaciones del registro | `test_audit_reuses_mission_record_checks` | NOT_RUN | código 1 tras alterar informe |
| Misión/ID inválidos | `test_audit_invalid_mission_returns_two` | NOT_RUN | código 2 |
| Regresión de la CLI existente | suite completa | NOT_RUN | 270 pruebas base + nuevas, salida 0 |

## 8. Riesgos y mitigaciones
- Falso OK por normalización o ruta mal resuelta: se usa la única implementación existente (`digest`, `canonical_file`) y se prueban CRLF, `..`, rutas absolutas, enlaces (con skip declarado si el entorno no lo permite) y el mapeo misión→raíz.
- Falsa alarma sobre manifiestos históricos: la prosa y los comentarios se ignoran; la deriva del árbol es aviso; los ciclos anteriores no bloquean. La única clase que produce 1 sin defecto del registro es «versión registrada no anclada», que es una discrepancia de trazabilidad real ya presente en `DOC-001` y `DISCOVERY-001`; se documenta y no se reescribe historia.
- Confusión entre ausencia de evidencia y evidencia válida: los avisos se imprimen con prefijo `AVISO:` y nunca cambian el código de salida; las discrepancias usan ` - ` y código 1.
- Interpretación de los avisos como autorización: la salida repite que no hay dictamen de Quality ni comprobación de identidades, y los avisos nunca habilitan un Gate.
- Cambio de reglas por la puerta trasera: `audit` no se invoca desde `validate`/`can-*` y no modifica `controls.json`; la clasificación es informativa.
- Deriva de mantenimiento: nuevas pruebas fijan los códigos de salida, el formato, la precedencia de ciclos y el mapeo de rutas.

## 9. Decisiones del propietario pendientes
- Aceptación final de DET-001 tras los tres Gates; hasta entonces `owner_acceptance` permanece `PENDING`.
- Autorización explícita e independiente para commit/push o despliegue: no solicitada y no ejecutada en esta misión.
- Alcance de M2/M3: fuera de esta autorización; no se implementan.

## 10. Condiciones de Gate 1
El revisor independiente debe comprobar: que el diseño no duplica `digest`/`canonical_file` ni la validación existente; que `validate` y `can-*` conservan su contrato; que los códigos de salida y los escenarios negativos son verificables; que la clasificación no altera la pertenencia a Gates; que no se tocan expedientes históricos, `controls.json` ni APP-001; y que el plan no promete identidad, aislamiento ni dictamen automático.
