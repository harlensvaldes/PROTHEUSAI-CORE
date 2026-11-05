# GOV-001 · Gate 1 — Revisión independiente, ciclo 8

**Dictamen:** PASS
**Revisor:** quality-gov001-c8
**Verificación de identidad:** solo declarada. Es el nombre que el agente principal asignó al lanzar este subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime, y ni este informe ni la CLI verifican la identidad.
**Independencia verificada:** no — la separación es solo contextual: no redacté v1–v8 ni implementaré la misión, pero soy un subagente del mismo runtime que el autor (copilot-sdk-main) y no existe una prueba operativa de separación.
**Artefacto revisado:** GOV-001-PROPOSAL-v8.md sha256:252C71CA09D26947FCE1F352E708DB2C927C6A8C2A6560EBD4007DB93EFFED7F
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v8 y del diff v7→v8 (`git diff --no-index`), contrastada con GATE1-REVIEW-07, OWNER-DECISION-01 y PROTHEUSAI-CORE `29d741e` (`scripts/quality_cli.py`). Ejecuté además comandos de solo lectura: la CLI actual con `python -B` y `--root` sobre el piloto protheus-efd.

> **Alcance del dictamen.** Este PASS se refiere solo al diseño de v8 (hash indicado). No se transfiere a versiones posteriores. No certifica la implementación (Gates 2/3 pendientes). Tampoco suple la verificación de identidades: según la propia v8, los Gates de `mission.json` v2 siguen PENDING hasta que un tercero registre `verification`. Por la línea `Independencia verificada: no`, este informe no serviría como `evidence_file` de un Gate v2 en PASS (N29).

## Integridad y entorno
- `Get-FileHash`: v8 = `252C71CA…ED7F`, coincide con la instrucción. `GOV-001-PROPOSAL.md` es idéntico a v8. v7 = `22B81C6D…7F92`, GATE1-REVIEW-07 = `DC315471…C12D` y OWNER-DECISION-01 = `7F9103CF…76AE`: los tres coinciden.
- Leí `AGENTS.md` y `agents/quality.md` de PROTHEUSAI-CORE.
- CORE: HEAD = `29d741e`; `git status --short` vacío, antes y después de la revisión. No modifiqué ningún archivo, salvo la creación de este informe.
- Diff v7→v8: 5 líneas cambiadas, todas marcadas [v8]: Estado, fila `GOV-001/`, Secuencia, P7b y N42. Solo hay un cambio sin marca, «propuestas v1–v7» → «v1–v8» en la fila `GOV-001/`, que es editorial y coherente. No encontré ningún cambio en §1–§4, §7 ni §8.

## Evidencia ejecutada (solo lectura)
| Comando | Exit | Resultado |
|---|---|---|
| `python -B CORE\scripts\quality_cli.py validate --root <protheus-efd>` | 0 | OK estructura |
| `python -B CORE\scripts\quality_cli.py can-close --mission APP-001 --root <protheus-efd>` | 1 | BLOCKED (owner/Gates no aprobados) |
| `Get-FileHash APP-001\mission.json` antes/después | — | `D3E1AA17…A39F`, idéntico |
| `git status --porcelain --untracked-files=all` del piloto, antes/después | 0 | vacío, idéntico |
| `git -C CORE status --short` | 0 | vacío |

## Estado de los hallazgos
| ID | Estado | Evidencia |
|---|---|---|
| R-1 (G1-19 resto) | **CERRADO** | La fila `GOV-001/` [v8] registra que `OWNER-DECISION-01.md` ya existe, con su SHA-256 `7F9103CF…76AE` (lo comprobé), la sesión `e5be03ee…` y el timestamp del mensaje del Owner (07:57:02+01:00). Se copia al registro sin alterar bytes y con el hash comprobado. El paso 2 de la Secuencia remite al artefacto «existente y con hash». El archivo se creó el 2026-11-05 a las 08:13:23. No hay ninguna implementación: CORE está limpio en `29d741e`. Que la transcripción sea literal no es verificable por mí; el propio archivo lo declara («pendiente de confirmación del Owner»). |
| R-2 (G1-22 resto) | **CERRADO** | N42 [v8] usa `verificad[oa]` con el calificativo `registrad[oa]` o «no comprobada por la CLI». Las cadenas de mensaje de v8 que contienen `verificad[oa]` son «revisor registrado como verificado por el autor revisado», que lleva el calificativo, y «verificada por la CLI», que solo aparece como texto prohibido en N37. No hay contradicción. |
| R-3 = G1-23 | **CERRADO** | La Secuencia [v8] cubre las cinco correcciones mínimas. (i) Paso 6: las plantillas `04`/`05` se sustituyen por los informes originales byte-idénticos y `06` solo por el Owner, como adición permitida. Así desaparece el bucle de reapertura y la contradicción de plantillas PENDING (`quality_cli.py:38-39`). (ii) Paso 4: `01`/`02` remiten por ruta y SHA-256 a la propuesta y a GATE1-REVIEW-05..08. (iii) Paso 5: `GATE2-INPUT.sha256` contiene la lista `--porcelain --untracked-files=all` con el SHA-256 de cada archivo y `diff --stat` respecto a `29d741e`; incluye los archivos no rastreados. (iv) Paso 6: `POST-GATE-VALIDATION.md`, con comando, fecha y exit. (v) Paso 7: comparación posterior al commit con el manifiesto; solo pueden diferir los archivos permitidos. Se detecta cualquier archivo ausente del manifiesto. Queda una precisión menor, que paso a O-3. |
| O-1 | **CERRADO** | P7b [v8] ejecuta la CLI nueva con `--root` sobre el piloto completo, en solo lectura, con el hash de `APP-001/mission.json` y el `git status` del piloto antes y después. Comprobé que es viable: la CLI actual ya admite `--root` (`quality_cli.py:117`), el piloto cumple `FILES` (`validate` 0) y la ejecución no alteró ni el hash ni el estado git. |
| O-2 | Sin cambio (observación, no requisito de este Gate) | v8 no añade a la viñeta D3 que el Orchestrator solo puede firmar `owner_acceptance` cuando es el Owner. Se puede recoger en la implementación de D3. |

No reabro G1-01..G1-22: no hay evidencia nueva y v8 no altera sus líneas, salvo las cerradas arriba. **No encontré regresiones v7→v8 ni falsos PASS.** El paso 1 exige «Gate 1 ciclo 8 **PASS**», coherente con C2 y R7. La fila Secuencia [v7] mantiene que la autorización del Owner no es un waiver.

## Hallazgos nuevos
Ninguno bloqueante. No abro G1-24.

### Observaciones (sin reserva; no condicionan el PASS)
- **O-3** (paso 5/7, `GATE2-INPUT.sha256`): v8 no fija la ubicación del manifiesto. Si se versiona dentro del árbol, no puede contener su propio hash, y en la comparación del paso 7 aparecería como archivo «no listado». Precisión recomendada en la implementación: (a) excluirlo explícitamente de su propia lista y de la comparación, y (b) hacer que el informe Gate 2 lo identifique en `**Artefacto revisado:**` por su SHA-256, lo que cierra la cadena de custodia. Para los archivos eliminados, registrar `DELETED` en lugar del hash.
- **O-4** (editorial): las etiquetas de las filas `GOV-001/` («[v5/v6/v7]») y Secuencia («[v6/v7]») no incluyen [v8], aunque el contenido nuevo sí lleva la marca. En el paso 4, «GATE1-REVIEW-05..08» debería leerse «05..último ciclo» si hubiera más ciclos.

## Estado D1–D4 / C1–C3
- **D1–D4:** se cumplen, sin cambios respecto a v7.
- **C1:** se cumple; R-2 está cerrada.
- **C2:** se cumple. El paso 1 exige PASS exacto y PWR no habilita.
- **C3:** se cumple en el modelo (R5b) y en la secuencia (manifiesto de entrada y comparación posterior al commit).

## Qué NO verifiqué
- No hay implementación de v8, así que todas las pruebas P/N son NOT_RUN. **E2E NO EJECUTADO** (no aplica a Gate 1).
- No ejecuté `unittest` de CORE en este ciclo: no cambió el código y GATE1-REVIEW-07 lo registra.
- No verifiqué mi identidad, la de copilot-sdk-main ni la autenticidad ni la literalidad de OWNER-DECISION-01 respecto al mensaje del Owner. Tampoco el timestamp 07:57:02, porque no tengo acceso a la transcripción de la sesión.
- No revisé v1–v6 ni los documentos de CORE ajenos a `quality_cli.py`, porque v8 no los toca.
- La comprobación de O-1 la hice con la CLI **actual**, no con la nueva.

## Limitación de independencia
Soy un subagente lanzado por el mismo runtime que el autor (copilot-sdk-main), posiblemente con la misma familia de modelo. La separación es solo de contexto. Según las reglas de v8 (R1, R4b), este informe no puede habilitar un Gate v2 sin que un tercero (por ejemplo, el Owner) registre la verificación de las identidades. El avance a la implementación se apoya en este PASS de diseño y en la autorización expresa del Owner (`OWNER-DECISION-01.md`), que no es un waiver.
