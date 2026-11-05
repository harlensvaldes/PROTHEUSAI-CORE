# GOV-001 · Plan de resolución de la revisión del Owner (GOV-R01..R03)

**Estado:** DRAFT v3. Corrige el PWR de Quality ciclo 2 (`GOV-R-REVIEW-02.md` sha256 `d20320a7…a9c7`; GR-11..GR-15 y residuales de GR-03, GR-04, GR-06 y GR-10) sobre v2 `2A5AAA02…93AE`. La v1 (`656B67DF…38FB`) tuvo FAIL en el ciclo 1. PENDING Quality y Owner.
**Autor (Architect, declarado):** copilot-sdk-main
**Repo:** PROTHEUSAI-CORE `6e5e929` (árbol limpio). Commits y dictámenes existentes intactos.
**Restricciones:** sin frameworks; mínimo alcance; nada se implementa sin aprobación del Owner.

## Clasificación (una por observación, GR-08)
| Obs. | Clasificación | Consecuencia |
|---|---|---|
| GOV-R01 Historial alterado | **Bloqueo** | Se resuelve en GOV-001 con adiciones documentales y de evidencia; sin cambios en la CLI |
| GOV-R03 Validación estructurada | **Bloqueo** | Se resuelve en GOV-001 con un incremento pequeño de código; reabre Gate 1 → 2 → 3 |
| GOV-R02 Identidad verificable | **Mejora futura (GOV-002)** | El cierre formal de GOV-001 queda diferido (ver «Cierre de GOV-001») |

## GOV-R01 — Entrada eliminada de Gate 2, ciclo 1
**Hechos (GR-13: se separa lo reproducido de lo declarado):**
- No se ha encontrado ninguna copia (Papelera, historial local de VS Code, `git fsck`).
- **Reproducido por el autor y por Quality ciclo 1** (`GOV-R-REVIEW-01.md`, subagente del mismo runtime, **independencia no acreditada**): la reconstrucción determinista da el SHA-256 `f0f7392a…4a9b`, con 38 entradas y el repositorio sin cambios.
- Según el **análisis del código** de Quality, no se identificó ninguna vía de MATCH engañoso. El resultado depende de que `f0f7…` sea el hash revisado en el ciclo 1. Ese valor consta en `GATE2-REVIEW-01.md:7` y `GATE3-EVIDENCE-01.md:7`, comiteados antes de que existiera el script.
- **Declarado por el autor, procedencia no acreditada:** los 12 hashes parciales que el script contrasta. Proceden de salidas de la sesión, sin archivo.

**Cambios (solo adiciones):**
1. `docs/MISSIONS/GOV-001/GATE2-INPUT-01.RECONSTRUCTED.sha256`: los bytes reconstruidos, sin alterar. El nombre declara que es una reconstrucción.
2. `.gitattributes` con **una sola línea**, `docs/MISSIONS/GOV-001/GATE2-INPUT-01.RECONSTRUCTED.sha256 -text`. Así se almacena y se extrae sin conversión de finales de línea y su hash coincide en cualquier checkout (GR-05). No afecta a ningún otro archivo, incluidas las entradas -02/-03 ya comiteadas.
3. `docs/MISSIONS/GOV-001/GOV-R01-reconstruct.py` (GR-06):
   - Argumentos `--repo` (por defecto, el directorio actual) y `--commit` (por defecto `6e5e929`).
   - Lee blobs con `git show <commit>:<ruta>`, sin depender del árbol de trabajo ni de `autocrlf`.
   - Usa un clon temporal que se borra en `finally`, incluidos los archivos de solo lectura.
   - Imprime `MATCH`/`NO MATCH` y la versión de Git usada (GR-06). Si el archivo reconstruido ya está comiteado, compara además con su blob (`git cat-file blob HEAD:<ruta>`); si aún no lo está, lo indica sin fallar.
   - No escribe nada fuera de `%TEMP%` salvo con `--out`.
4. `docs/MISSIONS/GOV-001/INCIDENT-01.md`, con la plantilla `docs/templates/INCIDENT.md`:
   - Qué se borró, cuándo, quién (copilot-sdk-main) y su impacto. Cómo se detectó (declarado por el autor; G2-10).
   - La reparación: reconstrucción declarada, no original, contrastada con el hash registrado de antemano. Se usa la misma redacción de GR-13: lo que se reprodujo, sin independencia acreditada, y lo que solo se declaró.
   - Cómo reproducirla en un clon limpio, con `autocrlf=true` y con `false`.
   - **Rectificaciones expresas, sin editar los originales:** `03-IMPLEMENTATION.md` («No es reconstruible byte a byte») y `GATE2-REVIEW-02.md:44,64` (GR-07).
   - Prevención: entradas y evidencias de Gate append-only y numeradas por ciclo.
5. `docs/QUALITY_EVIDENCE_PROTOCOL.md`, una línea: «Las entradas y evidencias de Gate son append-only. Un registro perdido se documenta como incidente y solo puede sustituirse por una reconstrucción declarada, verificada contra un hash registrado antes de la pérdida.» La CLI **no** impone la regla append-only: es una limitación declarada; su automatización queda como mejora futura (GR-07).

**Verificación:** sin cambio de código. En el Gate 2/3 de R01, Quality ejecuta el script sobre un clon limpio con `autocrlf=true` y con `false`, y comprueba `MATCH` y el hash del archivo extraído.
**Residual:** el original no existe; queda una reconstrucción idéntica en bytes, declarada como tal.

## GOV-R03 — Sustituir la heurística de independencia
**Defecto actual:** `quality_cli.py` interpreta prosa (el regex `INDEPENDENCE` y la regla de la palabra «no»). Rechaza textos legítimos y admite negaciones disfrazadas (G2-15).

**Principio (GR-01, GR-14):** el dato de independencia lo emite **el revisor, en su informe**, como token enumerado. El manifiesto lo replica y la CLI exige igualdad exacta, igual que con `Dictamen`. Así, el Orchestrator o el autor **no pueden fijar la independencia del revisor sin alterar su informe**. Hasta GOV-002 no se acreditan ni la autoría ni la integridad del informe **antes** de fijarse: quien lo copia al repositorio podría fabricarlo o alterarlo. Mitigación declarativa: el revisor comunica en su respuesta el SHA-256 de su informe y el Orchestrator lo cita.

**Diseño:**
- **Se eliminan** el regex `INDEPENDENCE`, la regla del «no» y la etiqueta `**Independencia verificada:**`. En las plantillas pasa a ser `**Independencia (narrativa):**`, que la CLI no lee.
- **Informe del revisor**: dos etiquetas nuevas de valor estructurado, cada una exactamente una vez:
  - `**Independencia:** ACREDITADA` o `NO_ACREDITADA`, en ASCII exacto. Cualquier otro valor o una duplicación → error.
    - **Semántica que falla cerrado (GR-11)**, definida en el protocolo y en las plantillas: `ACREDITADA` solo si el revisor **no** redactó ni implementó lo revisado **y** la separación respecto de los autores queda demostrada por la evidencia citada (persona, proceso o runtime distintos).
    - En cualquier otro caso, `NO_ACREDITADA`: incluidos «mismo runtime o sesión que el autor no excluido» y «no verificable».
    - Con esta definición, los revisores actuales de GOV-001 deben marcar `NO_ACREDITADA`. La CLI bloquea entonces PASS y PWR, igual que hoy.
  - `**Evidencia de independencia:** <ruta> sha256_lf:<64 hex>, <ruta> sha256_lf:<64 hex>…`
    - Las evidencias quedan fijadas por hash (GR-12).
    - **Rutas canónicas (GR-15a):** POSIX, relativas a la carpeta de la misión, comparadas exactamente (sin `casefold`), sin espacios, comas ni `..`, y sin duplicados. El separador entre evidencias es `, `.
- **`mission.json`, por Gate.** El Orchestrator lo transcribe desde el informe:
  ```json
  "independence": {"status": "ACREDITADA",
                   "evidence": [{"path": "<ruta>", "sha256_lf": "<64 hex>"}]},
  "evidence_sha256_lf": "<64 hex>"
  ```
- **Reglas de la CLI:**
  - **PASS/PWR:**
    - `independence.status` es exactamente `ACREDITADA`.
    - El token del informe es igual a `status`; los pares ruta/hash del informe son iguales a `evidence`.
    - `evidence` no está vacía; cada ruta existe dentro de la misión, es un archivo regular legible y **no es el propio `evidence_file`** (GR-04); su `sha256_lf` coincide con el recalculado (GR-12).
    - `evidence_sha256_lf` es igual al hash del `evidence_file`, de modo que el informe queda fijado.
  - **FAIL:** `independence` es opcional y, si existe, debe ser coherente con el informe.
  - **PENDING:** sin exigencias.
- **Definición a nivel de bytes (GR-15b):** `sha256_lf = sha256(bytes.replace(b'\r\n', b'\n'))`. Un `\r` suelto no se toca y el archivo se lee siempre en binario.
- **Herramienta:** nuevo subcomando `quality_cli.py hash <ruta>`, que imprime `sha256_lf` para que revisor y Orchestrator calculen igual en cualquier sistema (residual de GR-03).
- **Solo referencias a archivos dentro de la misión**: se descartan las referencias `git:` en este incremento (GR-02). No hay dependencia de git ni del clon superficial de CI. Las referencias firmadas son materia de GOV-002.
- **Definición única del hash (GR-03):** la CLI solo calcula `sha256_lf` y el nombre del campo lo dice. Los tokens `sha256:` de `reviewed_artifact` siguen siendo identificadores registrados por personas, que la CLI no recalcula. **G2-13 sigue abierto** para los hashes crudos históricos (entradas de Gate y propuestas): esos hashes dependen de `core.autocrlf` y así se documenta.
- **`status` (residual de GR-04):** muestra `independencia: <status> (declarada por el revisor; no comprobada por la CLI)`.
- **Distribución de responsabilidades tras R03 (GR-04, GR-11, GR-14):**

| Ámbito | Qué cubre |
|---|---|
| Automático (CLI) | Presencia y forma; igualdad informe↔manifiesto de independencia, evidencias, revisor, dictamen, artefacto y autor efectivo; existencia de las evidencias dentro de la misión y su hash; informe fijado por `sha256_lf`. |
| Revisado por Quality y auditores | Que la evidencia citada respalde la independencia (revisable en Gates posteriores y auditorías); la exactitud de la transcripción del Orchestrator más allá de la igualdad. |
| No acreditado | La identidad del revisor (pendiente de GOV-002). La autoría e integridad del informe antes de fijarse. La coherencia entre la narrativa y el token en el informe Quality final, que nadie revisa después. La veracidad del contenido de la evidencia. |

**Impacto en código:**
- `quality_cli.py`: unas 50 líneas. Se borran `INDEPENDENCE` y la regla del «no»; se añaden `content_sha256_lf()`, el subcomando `hash`, la validación R0 de `independence` (claves exactas, tipos, enumeración) y de `evidence_sha256_lf`, el análisis de rutas canónicas y los cruces con el informe.
- `new_mission.py`: los Gates nacen con `independence: null` y `evidence_sha256_lf: null`.
- Tres plantillas de Gate, `QUALITY_EVIDENCE_PROTOCOL.md` (semántica de `ACREDITADA`) y `docs/MISSIONS/README.md`.
- `EXAMPLE-001/02-GATE1-REVIEW.md:5`: la etiqueta eliminada pasa a la narrativa (GR-15c).
- `EXAMPLE-001` y `GOV-001/mission.json`: se añaden los campos null; los Gates siguen en PENDING.
- **Compatibilidad:** no se sube `schema_version`, porque no hay ningún v2 con PASS ni PWR publicado. Un v2 con PASS sin los campos nuevos pasa a ser inválido, y así se documenta.

**Pruebas (GR-10, inventario de `tests/test_governance.py` a 6e5e929; base: 19 tests, exit 0):**
- Antes y después se registran el número de tests y el de subcasos, y se justifica cada diferencia (residual de GR-10).
- **Se sustituyen** los casos de texto de `test_report_must_match_manifest`, líneas 222–225 y 231–233 (7 subcasos). Desaparece la línea `**Independencia verificada:**` del helper `record()` (`:68,74`) y de `test_filled_templates_satisfy_report_rules` (`:422`). No se pierde ninguna otra aserción.
- **Positivas:**
  - PASS con `ACREDITADA` y evidencia fijada y coherente.
  - Una narrativa que contiene «no» o «sí — no comparte runtime» no afecta al resultado.
  - `sha256_lf` igual para el mismo contenido en LF y en CRLF; distinto si hay un `\r` suelto.
  - `hash <ruta>` coincide con `content_sha256_lf`.
  - Las plantillas rellenadas siguen pasando (P6).
- **Negativas (cada una con control de mutación):**
  - Informe `NO_ACREDITADA` con manifiesto `ACREDITADA` (GR-01).
  - `NO_ACREDITADA` con PASS o PWR (GR-11).
  - Plantilla rellenada con `NO_ACREDITADA` en PASS.
  - `status` no enumerado (`acreditada`, `true`, `null`).
  - Token del informe ausente o duplicado.
  - `evidence` vacía o ausente; pares del informe distintos del manifiesto.
  - Evidencia editada después del registro: `sha256_lf` distinto (GR-12).
  - Rutas con mayúsculas distintas (sin `casefold`), duplicadas, con espacios o comas, fuera de la misión, con `..`, con NUL, inexistentes o que son un directorio.
  - Una evidencia que es el propio `evidence_file`.
  - `evidence_sha256_lf` distinto (informe alterado) o de 63 caracteres hexadecimales.
  - Claves desconocidas en `independence`.
  - FAIL con `independence` incoherente.
  - `status` no contiene «verificad[oa]» sin calificar (se mantiene N42).

**Gates:** el cambio de diseño reabre Gate 1. Gate 2/3 usarán entradas append-only (`GATE2-INPUT-04`…).

## GOV-R02 — Identidad verificable (diseño base para GOV-002)
**Probado por el autor y por Quality en `%TEMP%`** (Git 2.55, OpenSSH 9.5p2):

| Prueba | Resultado |
|---|---|
| Firma de commit SSH con `allowedSignersFile`, firmada | `%G?=G` y el principal |
| Commit sin firmar | `N`; `verify-commit` exit 1 |
| Clave fuera del registro | `U`; exit 1 |
| Firma separada `ssh-keygen -Y sign`/`-Y verify` | Válida: exit 0. Principal ajeno o archivo alterado: exit ≠ 0 |

**Modelo propuesto para GOV-002 (independiente de LUNA y Cline; solo OpenSSH):**
- **Firmas separadas sobre los informes (GR-09c):**
  - El revisor firma el contenido de su informe normalizado a LF con `ssh-keygen -Y sign -n protheusai-review`, lo que produce `<informe>.sig`.
  - No necesita escribir en Git, la firma sobrevive a squash o rebase y queda ligada a los bytes exactos.
  - La CLI verifica con `ssh-keygen -Y verify`, pasando por stdin el contenido normalizado.
  - Los autores pueden firmar del mismo modo sus artefactos (plan, informe de implementación).
- **Registro** `quality/allowed_signers`: el principal es el id de la identidad. El Owner da de alta cada clave **una vez**, no en cada Gate.
- **Ancla de confianza fuera del árbol verificado (GR-09a):** la huella de la clave del Owner que firma el registro llega por argumento de la CLI o por una variable de CI, nunca desde el propio repositorio.
- **Vocabulario honesto (GR-09b,d):**
  - Lo automático es la **atribución a una clave registrada** y la **separación de claves calculada**: la clave del revisor ≠ la clave de los autores.
  - Solo se habla de «identidad verificada» si se cumple una condición mínima de custodia declarada y revisable: claves en usuarios del sistema o máquinas distintas. Si no, el nivel es «atribución a clave».

| Ámbito | Qué cubre |
|---|---|
| Automático | Firma válida de un principal registrado sobre el informe exacto; separación de claves; registro firmado por el ancla externa. |
| Revisado por Quality | Declaraciones de custodia de cada clave (`ROLE_MATRIX.md`); rotaciones; contenido de la revisión. |
| No acreditado | Que procesos o personas distintos custodien realmente claves distintas cuando comparten usuario del sistema; que el modelo o agente sea el declarado; el compromiso de una clave. |

- **Arranque (GR-08d):** el Gate 1 de GOV-002 no puede apoyarse en el mecanismo que crea. Requiere un revisor humano o un agente de otro runtime con un usuario del sistema distinto, o bien una excepción documentada del Owner. Es una intervención única, no rutinaria.
- **Impacto estimado:**
  - Unas 80 líneas en `quality_cli.py` (`subprocess` sobre `ssh-keygen`; falla cerrado si no está disponible).
  - `quality/allowed_signers` vacío y documentación.
  - Tests con claves efímeras: firma válida; sin firma; principal ajeno; informe alterado; el revisor firmando un artefacto de autoría; registro no firmado por el ancla; `ssh-keygen` ausente.

## Cierre de GOV-001 (GR-08)
- **Opción A (recomendada):**
  - Tras el PASS de los Gate 2/3 de R01 y R03, citados por hash, GOV-001 queda «implementado y validado técnicamente».
  - En `mission.json`, los Gates y `owner_acceptance` **siguen en PENDING**.
  - El Owner registra en `06-DECISION.md` la aceptación técnica y el cierre formal diferido a la revalidación con GOV-002.
- **Opción B:** incluir GOV-R02 en GOV-001. Amplía su alcance, reabre Gate 1 y exige el mismo arranque.

## Secuencia (tras aprobación)
1. Quality revisa este plan.
2. GOV-R01: adiciones → Gate 2/3 → commit.
3. GOV-R03: Gate 1 → implementación → pruebas y mutación → Gate 2/3 → commit.
4. Decisión del Owner (A o B) en `06-DECISION.md`.
5. GOV-002, si se elige A.

Durante todo el proceso: commits y dictámenes previos intactos, ningún Gate formal en PASS sin cumplir sus condiciones y entradas de Gate append-only.

## Decisiones del Owner
- **GOV-R01:** aprobar la reconstrucción declarada, la línea de `.gitattributes` y la regla append-only (documental).
- **GOV-R03:** aprobar el token del revisor (`ACREDITADA`/`NO_ACREDITADA`, con semántica que falla cerrado), `independence` con evidencias fijadas por `sha256_lf`, `evidence_sha256_lf`, el subcomando `hash` y la exclusión de referencias `git:` en este incremento.
- **GOV-R02:** opción A o B; aprobar el modelo de firmas separadas como base de GOV-002 y la vía de arranque.
