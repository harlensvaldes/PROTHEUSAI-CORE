# GOV-001 · Plan de resolución de la revisión del Owner (GOV-R01..R03)

**Estado:** DRAFT v1 — PENDING Quality y Owner
**Autor (Architect, declarado):** copilot-sdk-main
**Repo:** PROTHEUSAI-CORE `6e5e929` (árbol limpio). Commits y dictámenes existentes intactos.
**Restricciones:** sin frameworks; mínimo alcance; nada se implementa sin aprobación del Owner.

## Clasificación
| Obs. | Clasificación | Resolución propuesta |
|---|---|---|
| GOV-R01 Historial alterado | **Bloqueo** del cierre (integridad de evidencia) | Dentro de GOV-001: solo documentación y evidencia, sin código |
| GOV-R03 Validación estructurada | **Bloqueo** de GOV-001 (heurística defectuosa en código entregado) | Dentro de GOV-001: incremento pequeño; reabre Gate 1 → 2 → 3 |
| GOV-R02 Identidad verificable | **Limitación aceptable** para el código de GOV-001; **bloquea el cierre formal**; **mejora futura** GOV-002 | Diseño aquí; implementación en GOV-002 |

## GOV-R01 — Entrada eliminada de Gate 2, ciclo 1
**Hechos verificados (investigación de solo lectura, 2026-11-05):**
- No hay copia: el archivo nunca se comiteó, no está en la Papelera, no hay historial local de VS Code y `git fsck` no encuentra objetos.
- El archivo es **reconstruible y verificable**. Se generó de forma determinista (comando registrado en la sesión) a partir del estado del árbol, y todas las ediciones posteriores están registradas. El script `gov-r01/reconstruct.py`:
  1. parte del árbol actual y deshace exactamente las ediciones de los ciclos 2 y 3 y la normalización CRLF;
  2. regenera las plantillas 04 y 05 y el `git diff --stat` en un clon temporal;
  3. ensambla el archivo con el mismo formato.
- **Resultado:** SHA-256 `f0f7392a…4a9b` = hash original registrado en `GATE2-REVIEW-01.md:7` y `GATE3-EVIDENCE-01.md:7`, con 38 entradas. Coinciden también los 12 hashes parciales impresos en su día. Un SHA-256 idéntico implica bytes idénticos (resistencia a colisiones).

**Cambios (solo adiciones en `docs/MISSIONS/GOV-001/`; no se modifica ningún archivo comiteado):**
1. `GATE2-INPUT-01.RECONSTRUCTED.sha256`: los bytes reconstruidos. El nombre declara que es una reconstrucción; su contenido no se altera, porque la prueba depende de él.
2. `GOV-R01-reconstruct.py`: el script, ajustado para leer blobs del commit `6e5e929` mediante `git show` en vez del árbol de trabajo. Así es reproducible en cualquier checkout. Imprime `MATCH` o `NO MATCH` y no escribe en el repositorio salvo con `--out`.
3. `INCIDENT-01.md`, según `docs/templates/INCIDENT.md`: qué se borró, cuándo, por quién (copilot-sdk-main) y su impacto. Explica cómo se detectó (lo declaró el autor, G2-10), la reparación (reconstrucción verificada por hash, no original) y cómo reproducirla. Rectifica expresamente la frase de `03-IMPLEMENTATION.md` «No es reconstruible byte a byte», que se conserva sin editar. Prevención: las entradas y evidencias de Gate son append-only y numeradas por ciclo.
4. `docs/QUALITY_EVIDENCE_PROTOCOL.md`: una línea. «Las entradas y evidencias de Gate son append-only; un registro perdido se documenta como incidente y solo puede sustituirse por una reconstrucción declarada, verificada por el hash original registrado.»

**Pruebas:** no hay cambio de código. Quality ejecuta el script de forma independiente sobre `6e5e929` y comprueba `MATCH`.
**Residual:** el original no existe; queda una reconstrucción idéntica en bytes, declarada como tal.

## GOV-R03 — Sustituir la heurística de independencia
**Defecto:** `quality_cli.py` interpreta prosa (`INDEPENDENCE` y la regla de la palabra «no»).
- Rechaza textos legítimos («sí — no comparte runtime»).
- Admite negaciones disfrazadas (homoglifos, «sí — _no», «falso»; G2-15).

**Diseño (mínimo, sin nueva versión de esquema; ningún v2 con PASS existe aún):**
- **Se elimina** la interpretación de texto: el regex `INDEPENDENCE`, la regla del «no» y la obligación de la línea `**Independencia verificada:**`. En las plantillas pasa a ser narrativa: `**Independencia (narrativa):**`. La CLI ya no la lee.
- **Datos estructurados en `mission.json`.** Por cada Gate con PASS o PWR:
  ```json
  "independence": {"conflict": false,
                   "evidence": [{"ref": "<ruta dentro de la misión> | git:<sha>", "sha256": "<64 hex> | null"}]}
  ```
  - `conflict`: booleano estricto. PASS o PWR exigen `false`.
  - `evidence`: lista no vacía de referencias. Una ruta exige `sha256` y la CLI comprueba que coincide. Un `git:<sha>` debe existir en el repositorio (`git cat-file -e`) y su `sha256` es null.
- **Fijación del informe:** `evidence_sha256` por Gate; la CLI comprueba el hash del `evidence_file`.
- **Hash canónico:** la CLI calcula los SHA-256 sobre el contenido con CRLF normalizado a LF, para que no dependan de `core.autocrlf` (resuelve también G2-13 en lo que verifica la CLI).
- **Se mantiene:** la comparación exacta de identificadores entre informe y manifiesto (Revisor, Dictamen, Artefacto revisado, Autor efectivo). Es igualdad canónica de identificadores, no interpretación semántica, y es lo que exige C3.
- **Qué deja de comprobar la CLI:** la coherencia entre la prosa del informe y `conflict`. Pasa a ser responsabilidad de Quality (§ distribución en GOV-R02).

**Impacto en código:**
- `quality_cli.py`: unas 40 líneas. Desaparecen `INDEPENDENCE` y la regla del «no»; se añaden la validación R0 de `independence` y `evidence_sha256`, un `content_sha256()` y la resolución de referencias. `git cat-file` se usa solo para referencias `git:`.
- `new_mission.py`: los Gates nacen con `independence: null` y `evidence_sha256: null`.
- Tres plantillas de Gate, `QUALITY_EVIDENCE_PROTOCOL.md`, `docs/MISSIONS/README.md`.
- `EXAMPLE-001` y `GOV-001/mission.json`: se añaden campos null. Los Gates siguen en PENDING.

**Pruebas:**
- **Positivas:**
  - PASS con `conflict:false` y evidencia resoluble.
  - Un texto narrativo con «no» no afecta.
  - Los hashes se aceptan con LF y con CRLF.
- **Negativas:**
  - `conflict:true` con PASS o PWR.
  - `conflict` no booleano (`"false"`, 0).
  - `evidence` vacía o ausente.
  - Una ruta fuera de la misión o con NUL.
  - `sha256` incorrecto o de 63 caracteres hexadecimales.
  - Un `git:<sha>` inexistente.
  - `evidence_sha256` que no coincide (informe alterado después de registrarse).
  - FAIL no exige `independence`.
  - Claves desconocidas en `independence`.
- **Se sustituyen** los casos de texto de independencia (N29, N30, G2-05, G2-08), sin perder ninguna otra aserción.
- **Control de mutación:** se repite para cada regla nueva.

**Gates:** el cambio de diseño reabre Gate 1. Después vienen Gate 2 y Gate 3 con entradas append-only (`GATE2-INPUT-04`).

## GOV-R02 — Identidad verificable sin intervención rutinaria del Owner
**Probado en `%TEMP%`:** Git 2.55 + OpenSSH verifican firmas SSH de commits con `gpg.ssh.allowedSignersFile`.
- `git log --format=%G?%GS` devuelve `G` y el principal registrado.
- Un commit sin firmar queda `N` y `verify-commit` sale con exit 1.
- No interviene ningún runtime concreto.

**Modelo (GOV-002, independiente de LUNA o Cline):**
- **Registro de claves:** `quality/allowed_signers` en formato OpenSSH; el principal es el id de la identidad.
  - Cada rol o runtime tiene su propia clave. El Owner la incorpora **una vez** al darla de alta, no en cada Gate.
  - Un cambio en el registro solo es válido si lo firma una clave de Owner. La huella de esa clave de arranque se publica en el Charter y se confía fuera de banda.
- **Funcionamiento:** cada agente comitea sus artefactos firmados con su clave. Basta con que el runtime pueda ejecutar `git commit -S` con una clave asignada (LUNA, Cline, un humano o cualquier otro).
- **Nuevo método de evidencia** `git-ssh-signature`, cuya referencia es el sha del commit.

**Distribución de responsabilidades:**

| Ámbito | Qué cubre |
|---|---|
| **Verificable automáticamente (CLI)** | El commit que introduce el informe tiene firma `G` de un principal cuyo canónico es igual a `reviewer.id`. Los commits que tocan el artefacto revisado entre la base y la referencia están firmados por principales de los roles autores. Ningún commit de autoría está firmado por la clave del revisor (independencia calculada, no declarada). El registro de claves está firmado por el Owner. |
| **Revisado por Quality** | El contenido de la revisión; que el conjunto de commits corresponde a la versión revisada; la custodia declarada de cada clave (runtime, máquina, persona) en `ROLE_MATRIX.md`; anomalías como rotaciones o claves compartidas. |
| **Sigue sin acreditarse** | Que dos claves distintas las custodien procesos o personas realmente independientes: un mismo operador podría tener todas. Que el modelo o agente sea el declarado. El compromiso de una clave. La veracidad de las evidencias propias del runtime (handles, ids de tarea) sin firma: solo llegan a «con evidencia». |

**Por qué fuera de GOV-001:**
- Exige dar de alta claves por runtime, que es una decisión operativa del Owner.
- Cambia el flujo de trabajo: los informes deben comitearse firmados antes de registrarse.
- Añade dependencia de `git` y `ssh-keygen` en los tests.

**Impacto estimado en GOV-002:**
- `quality_cli.py`: unas 80 líneas con `subprocess` sobre git.
- `quality/allowed_signers` (vacío) y documentación.
- Tests con un repositorio temporal y claves efímeras generadas con `ssh-keygen`. Positivos: firma válida. Negativos: sin firma, principal ajeno, revisor que firmó un commit de autoría, registro no firmado por el Owner, clave revocada.

**Consecuencia para el cierre de GOV-001:**
- Los informes Quality actuales declaran «independencia no verificada»: son subagentes del mismo runtime. Ningún Gate formal de GOV-001 puede pasar honestamente a PASS solo con ellos.
- Opciones:
  - **(A, recomendada):** aceptar GOV-001 como «implementado y validado técnicamente; cierre formal diferido», con la limitación documentada en `06-DECISION.md` por el Owner. Su revalidación formal sería el primer caso de uso de GOV-002, con revisión firmada desde un runtime o una persona distinta.
  - **(B):** incluir GOV-R02 en GOV-001, lo que amplía su alcance y reabre Gate 1.

## Secuencia propuesta (tras aprobación)
1. Quality revisa este plan.
2. GOV-R01: adiciones documentales, Gate 2/3 de esas adiciones y commit.
3. GOV-R03: Gate 1 (plan) → implementación → pruebas → Gate 2/3 → commit.
4. Decisión del Owner sobre el cierre (A o B) en `06-DECISION.md`.
5. GOV-002 como misión separada si el Owner elige A.

Durante todo el proceso: commits y dictámenes previos intactos, ningún Gate formal en PASS sin cumplir sus condiciones y entradas de Gate append-only.

## Decisiones del Owner
- **GOV-R01:** aprobar la reconstrucción declarada y la regla append-only.
- **GOV-R03:** aprobar la sustitución estructurada (`independence`, `evidence_sha256`, hash con LF normalizado).
- **GOV-R02:** opción A o B; si A, aprobar el modelo de firma Git como base de GOV-002.
