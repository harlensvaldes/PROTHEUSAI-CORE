# DET-001 · Gate 3 · verificación y aceptación

Fecha: 2026-11-07. Revisor `/root/quality`, distinto del Developer declarado (Cline), invocado mediante `spawn_agent`; contexto compartido I0, sin certificación de identidad ni aislamiento. Revisión con ejecuciones reales y acceso a las evidencias.

## Ciclos

| Ciclo | Artefacto identificado | Dictamen | Reservas |
|---|---|---|---|
| 01 | `GATE2-INPUT-02.sha256` · `cf4253c…` | PASS_WITH_RESERVATIONS | R1 registro formal pendiente; R2 informe de Gate 2 sin anclar; R3 recuento 27/28 sin rectificar en evidencia; R4 cobertura no automatizada de sondas; R5 enlaces simbólicos no ejecutados |
| 02 | `EVIDENCE-INDEX-01.sha256` + `GATE2-INPUT-02.sha256` | **PASS** | R1–R3 cerradas; R4–R5 declaradas como límites no bloqueantes del entorno |

## Evidencia ejecutada (2026-11-07, Windows, Python 3.13.12)

| Evidencia | Comando | Exit | `sha256_lf` |
|---|---|---|---|
| `evidence/gate3-tests.txt` | `python -m unittest discover -s tests -v` | 0 | `ecdadb0dad0b291871dac4339fad85eecdde9f63e3b2ae380ffe3b6fe7a16834` |
| `evidence/gate3-targeted.txt` | `python -m unittest tests.test_det001 -v` | 0 | `6988fbcb4c65d756428c0cb549e6cfd353d0e9aec39846bc2fc5acecede7dbf0` |
| `evidence/gate3-cli.txt` | `validate`, `manifest`, `audit`, `status`, `can-implement`, `can-close` y sondas reales | 0/0/0/0/0/1/0/1/1 | `8903e32176a5f0e65077684c4681c900752132231a614b68f5a5aee02278cc57` |

Resultados: suite completa **296 pruebas, OK (skipped=5)**, exit 0; DET-001 **26 pruebas, OK (skipped=1)**, exit 0. `manifest` de `GATE2-INPUT-02` da 8/8 antes de registrar Gate 2 y, después del registro, solo deriva `mission.json` (adición de gobernanza). `can-close` devuelve 1 con Gate 3 pendiente en el momento de la captura; no es un fallo.

## Verificación del revisor

- Recalculó los tres `sha256_lf` y coinciden; reejecutó la suite completa (296, OK, skipped=5, exit 0) y DET-001 (26, OK, skipped=1, exit 0), además de lotes por módulo, todos con exit 0.
- Confirmó que solo `mission.json` deriva de `GATE2-INPUT-02` tras registrar Gate 2; código, pruebas y documentos conservan sus hashes (`scripts/quality_cli.py 38cb53d0…`, `tests/test_det001.py fcb4abf3…`).
- Sondas propias: entrada que es directorio, hash pegado a texto, `sub\y.py`, `./x.py`, `../x.py`, duplicado, manifiesto vacío y comentario `#` con 64 hex; todas con el código esperado y sin falso OK.
- No emite PASS de Quality desde la CLI; `E2E NO EJECUTADO` declarado (cambio de herramienta, sin producto desplegable).

## Rectificación documental

`03-IMPLEMENTATION.md` cita «27 manifiestos reales»; el recuento del árbol es **26 preexistentes** (28 con los dos de DET-001). Se rectifica aquí sin reescribir el informe revisado. La verificación posterior a Gate 2 queda limitada al árbol de trabajo: no hay commit ni comparación post-commit.

## Ciclo 02 · confirmación de cierre

El revisor verificó en la segunda vuelta: que `mission.json` registra Gate 3 con el hash `318b5d61…` del ciclo 01; que el bloque estructurado es coherente (misión, gate, riesgo MEDIUM, reviewer, artifact, authors, evidencias y fecha); que `EVIDENCE-INDEX-01` ancla `02-GATE1-REVIEW.md` (`3ae758a9…`) y `04-GATE2-REVIEW.md` (`440edabc…`) con sus hashes actuales, y que `audit` ya no emite el aviso de ancla ausente para el informe de Gate 2; que la rectificación 26/28 está en la evidencia sin reescribir `03-IMPLEMENTATION.md` (`74c5730f…`); y que código y pruebas conservan los hashes de Gate 2 (`quality_cli.py 38cb53d0…`, `tests/test_det001.py fcb4abf3…`). R4 y R5 quedaron como límites declarados del entorno, sin falso OK demostrado. **Dictamen: PASS.**

El índice de evidencias se renueva en ciclo 03 tras registrar este PASS (incluye el `mission.json` final), de modo que el ancla efectiva deje de ser la obsoleta de `GATE2-INPUT-02`.

## Límites

- Enlaces simbólicos: 5 omisiones en la suite y 1 en DET-001 por `[WinError 1314]`; el rechazo consta en `canonical_file` pero no se acreditó por ejecución en este entorno.
- Cobertura no automatizada: entrada-directorio, separadores Windows y texto pegado tras el hash se acreditaron con sondas del revisor, no con pruebas del repositorio.
- `audit` devuelve 1 en DOC-001 y DISCOVERY-001 por discrepancias históricas reales, ajenas a esta misión.
- La CLI no autentica identidad ni aislamiento y no sustituye el dictamen de Quality.

```protheusai-review
{
  "mission": "DET-001",
  "gate": "gate3",
  "risk": "MEDIUM",
  "decision": "PASS",
  "reviewer": "/root/quality",
  "artifact": {
    "name": "Entrada Gate 2 ciclo 02",
    "ref": "sha256_lf:cf4253ccce414b9e14f8a742b80a122938e1af4c9a228800f48004386bbd0ebf",
    "path": "GATE2-INPUT-02.sha256"
  },
  "effective_authors": ["Cline"],
  "authorship_independent": true,
  "isolation": "I0_CONTEXTO_COMPARTIDO",
  "evidence": [
    {"kind": "execution", "path": "evidence/gate3-tests.txt", "sha256_lf": "ecdadb0dad0b291871dac4339fad85eecdde9f63e3b2ae380ffe3b6fe7a16834"},
    {"kind": "execution", "path": "evidence/gate3-targeted.txt", "sha256_lf": "6988fbcb4c65d756428c0cb549e6cfd353d0e9aec39846bc2fc5acecede7dbf0"},
    {"kind": "execution", "path": "evidence/gate3-cli.txt", "sha256_lf": "8903e32176a5f0e65077684c4681c900752132231a614b68f5a5aee02278cc57"}
  ],
  "date": "2026-11-07"
}
```

