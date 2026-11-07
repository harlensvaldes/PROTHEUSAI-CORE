# DET-001 · Implementación y comprobaciones

Fecha: 2026-11-07. Developer declarado: Cline. Gate 1 PASS sobre `01-PLAN.md` (`sha256_lf 320d0520cc936347d08b52c45e06906670e5299d5819055bb5fea5fa1450c9b8`, `02-GATE1-REVIEW.md`). Sin escritura en Git, sin push y sin despliegue.

Gate 2 ciclo 1: `PASS_WITH_RESERVATIONS` sobre `GATE2-INPUT-01.sha256` (`sha256_lf 2914025…`), con H1 (traceback ante registro estructuralmente inválido), H2 (constantes duplicadas de `quality_v3`) y H3 (hash truncado de 63 hex ignorado si había entradas válidas). Las tres se corrigieron antes de renovar la entrada: guardas de tipo en `audit_report` y salida de `print_audit` (H1), reutilización de `quality_v3.HEX` y detección de 63 hex contiguos (H2/H3), más dos pruebas nuevas. La PWR se conserva como historia y no se convierte en PASS.

## Archivos realmente modificados
| Archivo | Qué cambió | Por qué | Gate 1 sección |
|---|---|---|---|
| `scripts/quality_cli.py` | comandos `manifest` y `audit`; `parse_manifest`, `manifest_report`, `classify`, `audit_report`, `print_manifest`, `print_audit`; importación de `canonical_file`/`parse_block`/`RELATIVE_PATH` de `quality_v3` | verificar manifiestos y cruzar anclas con el registro | §4.1–§4.5 |
| `tests/test_det001.py` | 24 pruebas nuevas (positivas, negativas y códigos) | verificar los contratos del plan | §7 |
| `docs/QUALITY_EVIDENCE_PROTOCOL.md` | sección «Deterministic anchor checks» | documentar comandos, ciclos y límites | §5 |
| `README.md` | comandos nuevos en «Verificación determinista de anclas» | mantener la guía de la CLI | §5 |
| `docs/MISSIONS/DET-001/*` | expediente de la misión | trazabilidad | §5 |

Sin cambios en `quality/controls.json`, `quality_v3.py`, `quality_v4.py`, `quality_v5.py`, `validate`, `status`, `can-implement` ni `can-close`. No se tocaron expedientes históricos ni APP-001. Diferencias de alcance: ninguna; no requiere reabrir Gate 1.

## Decisiones de implementación
- **Separación de responsabilidades.** `manifest` verifica el manifiesto contra los bytes actuales del árbol (0/1/2). `audit` no usa el árbol como autoridad: contrasta el hash registrado de cada informe y evidencia con las anclas del expediente; la deriva del árbol se informa como aviso.
- **Base de rutas.** Los manifiestos son relativos a la raíz; `review.file` y las evidencias, relativas a la carpeta de misión. El cruce normaliza `docs/MISSIONS/<ID>/<ruta>`. El argumento `<ruta>` de `manifest` se resuelve desde el directorio de trabajo; `--root` solo resuelve las entradas.
- **Clases.** Error (1): hash divergente, archivo ausente/no regular/fuera de la raíz, ruta no canónica, duplicado, línea ambigua, manifiesto sin entradas, `versión registrada no anclada`. Aviso (0): deriva del árbol, ancla ausente, ciclo anterior. Lectura imposible (2), con precedencia sobre 1.
- **Ciclos append-only.** Ancla efectiva por `(ciclo numérico, original sobre .RECONSTRUCTED, nombre)`; las anteriores no bloquean. Una reconstrucción sin original sigue siendo efectiva.
- **Parser.** Uno o más espacios/tabuladores entre hash y ruta; tokens `git status --porcelain` con `[ MADRCU?!]{1,2}` (incluye `!!`); comentarios `#` ignorados aunque contengan hash; prosa y vallas ignoradas; línea con 64 hexadecimales no interpretable = error.
- **Clasificación.** Heurística de presentación (gobernanza/producto) que solo alimenta conteos; no altera la pertenencia a Gates ni ninguna validación.
- Reutilización: `quality_v3.digest` (`sha256_lf`), `canonical_file` (rutas, enlaces, escapes), `parse_block` (bloque de revisión) y `quality_cli.mission_errors` (registro). No se duplicó su lógica.
- La implementación amplía la deriva a **todas** las anclas efectivas del expediente (no solo a las referenciadas por el registro); sigue siendo aviso y no cambia ningún código de salida.

## Pruebas locales ejecutadas
| Comando | Entorno/fecha | Exit code | Resultado |
|---|---|---|---|
| `python -m unittest tests.test_det001 -v` | Windows, Python 3.13.12, 2026-11-07 | 0 | 26 pruebas, **OK (skipped=1)** en 0,71 s; la omitida es el enlace simbólico (`WinError 1314`) |
| `python -m unittest discover -s tests -v` | Windows, Python 3.13.12, 2026-11-07 | 0 | 296 pruebas, **OK (skipped=5)** en 47,52 s; línea base 270, sin regresiones |
| `python scripts/quality_cli.py validate` | Windows, 2026-11-07 | 0 | estructura consistente; solo avisos históricos v1 |
| `python scripts/quality_cli.py audit --mission DET-001` | Windows, 2026-11-07 | 0 | registro y anclas coherentes |

Casos negativos cubiertos: hash divergente, ausente, duplicado, ruta `..`/absoluta, manifiesto vacío, línea ambigua (64/65 hex), hash truncado de 63 hex, manifiesto ilegible/no UTF-8, `--root` inexistente, registro alterado, evidencia eliminada, versión no anclada, prioridad 2>1, registro estructuralmente inválido, ciclos con reconstrucción y orden numérico. Los 27 manifiestos reales del repositorio se parsean sin errores de formato (comprobación de solo lectura).

Comprobaciones de solo lectura sobre el repositorio: `manifest` → `docs/STRUCTURAL-CONSISTENCY-INPUT.sha256` 7/7 (0); `GATE2-INPUT-04.sha256` de BOOTSTRAP-001 detecta dos hashes divergentes (1); `audit --mission DOC-001` detecta la versión no anclada documentada en el plan (1); `can-implement --mission DET-001` (0) sin cambio de contrato.

## Riesgos y deuda técnica
- La CLI no autentica identidades ni aislamiento, no emite dictamen de Quality y no habilita Gates por sí sola.
- `manifest` verifica el estado actual; los manifiestos históricos ya divergentes (25 de 26) siguen divergiendo y no se reescriben.
- `audit` devolverá 1 en `DOC-001` y `DISCOVERY-001` por discrepancias de trazabilidad preexistentes, documentadas y no corregidas aquí.
- No hay commit ni comparación post-commit: la validación posterior se limita al árbol de trabajo y se declara en `05-GATE3-EVIDENCE.md`.
- Enlaces simbólicos: la prueba se omitió por privilegio del entorno; `canonical_file` ya los rechaza en código, pero esta ejecución no lo acreditó.

