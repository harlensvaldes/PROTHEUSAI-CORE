# GOV-001 · Revisión Quality del plan de resolución GOV-R01..R03, ciclo 8

**Dictamen:** PASS
**Revisor:** quality-gov001-r8
**Verificación de identidad:** solo declarada. El agente principal (copilot-sdk-main) me asignó este nombre al lanzar el subagente en la sesión e5be03ee-40b1-4d52-a967-aab163ad6f3c. No tengo acceso al registro de lanzamiento del runtime y no hay firma ni otro mecanismo que acredite la identidad.
**Independencia verificada:** no — la separación es solo contextual: no redacté GOV-001-R-PLAN-v1..v8 ni GOV-R-REVIEW-01..07 y no implementaré la misión, pero soy un subagente del mismo runtime, sesión y usuario del sistema que el autor (copilot-sdk-main). Con la semántica del plan, este informe sería `NO_ACREDITADA`.
**Artefacto revisado:** GOV-001-R-PLAN-v8.md sha256:c8432b8d146c624cec7b7f50668aaf5354e1b45615656866a5961c1e738fed38
**Autor efectivo:** copilot-sdk-main
**Fecha:** 2026-11-05
**Método:** revisión estática de v8 frente a v7 (`git diff --no-index --word-diff=plain`, exit 1 = hay diferencias), frente a `GOV-R-REVIEW-07.md`, `AGENTS.md`, `agents/quality.md` y el repositorio PROTHEUSAI-CORE `6e5e929`. Pruebas propias en `%TEMP%` (borradas, `cleaned=True`) con Python 3.12.0 y Git 2.55.0.windows.3. Suite y `validate` en solo lectura con `python -B`. No modifiqué el repositorio ni ningún archivo existente.

> PASS técnico del **plan v8**, solo para el hash identificado arriba. No se transfiere a versiones posteriores. No aprueba ningún Gate formal de `mission.json` ni sustituye la autorización del Owner (`OWNER-DECISION-02.md`). Con `NO_ACREDITADA`, este informe no puede servir como `evidence_file` de un Gate formal en PASS. Las observaciones O-10 y O-12..O-14 no condicionan el dictamen; el criterio se explica abajo.

## Verificación de entradas
| Comprobación | Comando / fuente | Resultado |
|---|---|---|
| Hash del plan v8 | `Get-FileHash` | `C8432B8D…FED38`: coincide con el encargo. `sha256_lf` = `0d6bcca043a10066ebe1b2d15bbd9dfa5b271ce077aae5f8378f25f82c9e2a93` |
| Hashes previos | `Get-FileHash` | v7 `07FD2E92…AA498` y REVIEW-07 `A208FC02…3370E`: coinciden |
| Repo | `git rev-parse HEAD`; `git status --porcelain --untracked-files=all --ignored` | HEAD `6e5e92980a8e…`; 0 líneas antes y después |
| Suite base | `python -B -m unittest discover -s tests -q` | `Ran 19 tests … OK`, exit 0 |
| Validación | `python -B scripts\quality_cli.py validate` | exit 0 |
| `core.autocrlf` | `git config --show-origin --get-all core.autocrlf` | `true`, desde el gitconfig de **sistema** (`C:/Program Files/Git/etc/gitconfig`), no del repositorio |
| Dictámenes previos | `Select-String '^\*\*Dictamen:\*\*'` | REVIEW-01 FAIL; 02 a 07 PWR. La cabecera («Corrige el PWR ciclo 7… v1 FAIL; v2 a v6 PWR») es exacta y sigue la convención de v7 |
| Diff v7→v8 | `git diff --no-index --word-diff=plain` | Solo: cabecera; R01 Cambios, punto 6 nuevo (O-11); R01 Verificación, pasos 1 y 3 desglosados más la viñeta «Revisión (GR-23)»; § Gates de R03, una frase; bloque nuevo «Después del commit de R03 (GR-23)»; Opción B, «Gate de cierre (O-7)». No se elimina contenido salvo el texto sustituido a propósito |

## Pruebas propias de supuestos (`%TEMP%`, borradas)
**C. Punto 6 de R01 (copias en `R-PLAN/`).** Clon local de `6e5e929` (hereda `autocrlf=true`). Copio `GOV-001-R-PLAN-v1..v8.md` y `GOV-R-REVIEW-01..07.md` en `docs/MISSIONS/GOV-001/R-PLAN/` y hago un commit desechable.
- `validate` da exit 0 y la suite `Ran 19 tests … OK`, exit 0. La subcarpeta no interfiere: `quality_cli.py:306` solo recorre los hijos directos de `docs/MISSIONS`.
- Al extraer en clones nuevos, `GOV-001-R-PLAN-v8.md` da:

| Clon | SHA-256 crudo | `sha256_lf` | CR |
|---|---|---|---|
| `autocrlf=true` | `c8432b8d…` (= hash citado) | `0d6bcca0…` | 207 |
| `autocrlf=false` | `0d6bcca0…` | `0d6bcca0…` | 0 |

- Los 16 archivos de sesión revisados son CRLF puros: ningún `\r` suelto y ninguna aparición del nombre de usuario del sistema.
- Precedente: los blobs de `PROPOSAL-v1..v8` comiteados son iguales a la normalización LF de los originales de sesión, no a sus bytes.

Base de O-12.

## Estado de los hallazgos previos
| ID | Estado | Evidencia en v8 | Residual |
|---|---|---|---|
| GR-01..22 | Cerrados en ciclos anteriores; sin regresión | El diff v7→v8 no toca esos puntos | GR-09 sigue arrastrado al Gate 1 de GOV-002 |
| GR-23 (b) R03 | **Cerrado** | Bloque «Después del commit de R03 (GR-23)»: el Orchestrator compara el `sha256_lf` de cada archivo de `git diff --name-only <commit previo>..HEAD` con la última entrada revisada. Solo pueden diferir las adiciones permitidas, que enumera (informes originales, citas y validación posterior). Repite tests y `validate` sobre el commit extraído en un clon limpio, registra el resultado por adición en `POST-GATE-VALIDATION-R03.md` y asigna su revisión independiente (A: revalidación con GOV-002; B: Gate de cierre). Equivale a la corrección mínima pedida en REVIEW-07 y al precedente `PROPOSAL-v8` paso 7. | — |
| GR-23 revisión de `POST-GATE-VALIDATION-R01.md` | **Cerrado** | R01, paso 3: «la revisa Quality en el Gate 1 de R03, la siguiente revisión programada. Una discrepancia detiene R03». La Secuencia (3 antes que 4) confirma que ese Gate llega después del commit de R01. La opción B también cubre `POST-GATE-VALIDATION-*`. | — |
| O-7 (editorial «Gate de cierre») | **Cerrado** | La opción B define el Gate de cierre: revisor `ACREDITADA` según la regla de prevalencia, cubre las citas y los `POST-GATE-VALIDATION-*`, e informe firmado con GOV-R02. | — |
| O-8 | **Cerrado en R01**; residual editorial en R03 | R01, paso 1: `git status --porcelain --untracked-files=all`. | En R03: «`git status --porcelain`» sin `--untracked-files=all` (O-14). |
| O-9 | **Cerrado** en lo sustancial | Paso 3: `sha256_lf` por archivo del diff, extracción en un clon nuevo, SHA-256 crudo del archivo extraído y `MATCH`. | No fija `autocrlf` en el clon nuevo. En este equipo hereda `true` del sistema (prueba C); en otro podría no hacerlo. GR-05 se sigue deduciendo de la igualdad de `.gitattributes` con `-04` y del paso 2. Editorial. |
| O-10 | **Sin cambios** (no lo cita v8 como corregido) | «`GATE2-INPUT-05`…, porque la `-04` corresponde a R01». | Editorial, como en REVIEW-07: la secuencia es lineal y se lee como «el siguiente número libre». No condiciona. |
| O-11 | **Cerrado**, con una precisión pendiente (O-12) | Punto 6: copia de v1…vN y de `GOV-R-REVIEW-01..N` en `R-PLAN/`, dentro de las adiciones de R01 y, por tanto, del manifiesto `-04` y de su Gate 2/3. Es proporcionado: hay precedentes (`PROPOSAL-v1..v8`, `GATE1-REVIEW-05..08`). | Ver O-12. |

## Hallazgos nuevos
No hay hallazgos que condicionen el dictamen (no se asigna GR-24).

### Observaciones no bloqueantes
Criterio: no condicionan el dictamen porque no permiten ningún PASS falso (cualquier fallo se manifiesta como una discrepancia, es decir, falla cerrado) y el riesgo ya tiene un control previsto o una limitación documentada. Son mejoras de precisión que el autor puede adoptar o no.

- **O-12 (hash citable de las copias `R-PLAN/`).**
  - **Hecho:** punto 6 dice «se copian sin alterar bytes» y que así el Owner «puede citar el plan aprobado por ruta y hash dentro del repositorio». La prueba C muestra que, con el `autocrlf=true` del sistema, Git almacena el blob normalizado a LF. El hash crudo citado en los informes (`c8432b8d…` para v8) solo se reproduce en una extracción con `autocrlf=true`. Con `false`, tanto el crudo como el `sha256_lf` dan `0d6bcca0…`. Ningún cálculo sobre la copia extraída con `false` reproduce el valor citado.
  - **Por qué no condiciona:**
    - falla cerrado;
    - § Principio ya declara que el SHA-256 crudo depende de `core.autocrlf` y es secundario;
    - G2-13 documenta la misma limitación para propuestas y entradas, y el precedente `PROPOSAL-v*` se comporta igual;
    - en la configuración actual el hash crudo se reproduce.
  - **Mejora sugerida:** en el punto 6 y en la Autorización, indicar que la cita incluya el `sha256_lf` del plan (para v8: `0d6bcca0…2a93`) además del hash crudo, y que G2-13 alcanza también a `R-PLAN/`. Otra opción, sustituir «sin alterar bytes» por «sin alterar su contenido; Git normaliza los finales de línea, como en `PROPOSAL-v*`». No recomiendo añadir `-text` a `R-PLAN/`: contradice la regla de «una sola línea» de `.gitattributes`.
  - **Privacidad, verificada hoy:** ningún archivo que se copiaría contiene el usuario del sistema. Conviene repetir esa comprobación al copiar los informes posteriores, incluido este.
- **O-13 (asimetría entre R01 y R03 tras el commit).**
  - **Hecho:** R03 enumera las diferencias permitidas frente a la última entrada. El paso 3 de R01 compara «cada archivo» del diff con `-04` sin esa lista.
  - **Consecuencia:** si los informes del Gate 2/3 de R01 o `POST-GATE-VALIDATION-R01.md` entran en el rango del diff, aparecerían como discrepancias.
  - **Por qué no condiciona:** falla cerrado, y el precedente (`POST-GATE-VALIDATION.md`) documenta esas adiciones permitidas. Conviene añadir la misma frase a R01.
- **O-14 (`git status` en las entradas de R03).**
  - **Hecho:** § Gates de R03 dice «`git status --porcelain`», sin `--untracked-files=all`. En el modo por defecto, una carpeta nueva no rastreada aparece como una sola línea (`?? …/R-PLAN/`), sin sus archivos.
  - **Por qué no condiciona:** la presencia de archivos no rastreados sigue siendo visible, y Quality inspecciona el diff real en Gate 2. Se recomienda igualarlo a R01.

## Regresiones v7→v8, falsos PASS, alcance y afirmaciones
- **Regresiones:** ninguna. Se mantienen la clasificación, R01.1–5, el paso 2 de R01 (prueba A de REVIEW-07), el diseño y las reglas de R03, el inventario de tests, R02, el cierre, la detención y «Carácter».
- **Falsos PASS:** ninguno. Los Gates siguen en PENDING. Los añadidos son controles posteriores al commit que detienen el avance ante una discrepancia.
- **Alcance:** sin sobrealcance ni frameworks. El texto crece unos 1,6 kB. El punto 6 añade archivos documentales a R01, cubiertos por la Autorización «R01: implementar las adiciones». La sección «Decisiones del Owner · GOV-R01» no lo menciona de forma expresa (editorial).
- **Afirmaciones:**
  - Cabecera (hashes abreviados y ciclos): correcta.
  - «v8 corrige O-8 y O-11»: correcto, con O-14 y O-12 como precisiones.
  - «sin alterar bytes»: inexacto a nivel de blob (O-12).
  - «la siguiente revisión programada» (Gate 1 de R03): coherente con la Secuencia.

## Qué NO verifiqué
- `GOV-R01-reconstruct.py` ni un `MATCH` real del script: no existe. No repetí la prueba A de REVIEW-07.
- La implementación de R03, que no existe, ni los futuros `POST-GATE-VALIDATION-R01/R03.md` y `OWNER-DECISION-02.md`.
- Linux/CI ni otros shells; solo Windows con PowerShell 5.1.
- `git fsck`, la búsqueda de copias del original (GR-16) y las pruebas de firma de R02.
- El piloto `protheus-efd`, el origen EPF `5ee75df` ni otros consumidores de `quality_cli.py`.
- Que la carpeta de sesión no se alterara fuera de los hashes comprobados. Que los informes de sesión no contengan otros datos sensibles distintos del nombre de usuario buscado.

## Limitación de independencia
Soy un subagente del mismo runtime, sesión y usuario del sistema que el autor del plan (copilot-sdk-main) y que los revisores de los ciclos 1 a 7. Mi separación es solo contextual y no está acreditada. Con la semántica del plan, este informe declararía `NO_ACREDITADA`. Su PASS es técnico: no habilita Gates formales y deja la decisión al Owner. Las comprobaciones descritas son reproducibles por un revisor independiente.
