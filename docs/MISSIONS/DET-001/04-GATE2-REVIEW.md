# DET-001 · Gate 2 · revisión independiente del diff

Fecha: 2026-11-07. Revisor `/root/quality`, distinto del Developer declarado (Cline), invocado mediante `spawn_agent`; contexto compartido I0, sin certificación de identidad ni aislamiento. Revisión estática del diff con ejecuciones de solo lectura y pruebas reales.

## Historial de ciclos

| Ciclo | Entrada (`sha256_lf`) | Dictamen | Hallazgos |
|---|---|---|---|
| 01 | `GATE2-INPUT-01.sha256` · `2914025…` | PASS_WITH_RESERVATIONS | H1 traceback ante registro estructuralmente inválido; H2 constantes duplicadas de `quality_v3`; H3 hash truncado de 63 hex ignorado con entradas válidas |
| 02 | `GATE2-INPUT-02.sha256` · `cf4253c…` | **PASS** | H1–H3 cerradas; sin defecto material nuevo |

La PWR del ciclo 01 se conserva como historia y no se convierte en PASS.

## Verificación del dictamen final

- **Alcance:** diff limitado a `README.md`, `docs/QUALITY_EVIDENCE_PROTOCOL.md`, `scripts/quality_cli.py`, `tests/test_det001.py` y el expediente DET-001; sin cambios en `quality/controls.json`, `quality_v3/4/5.py`, expedientes históricos ni APP-001. Las cinco rutas no seguidas preexistentes conservan sus fechas y no se tocaron.
- **H1 cerrada:** guardas `isinstance` sobre `gates`/`record`/`review`/`evidence` y `.get` en `print_audit`; probeta con `mission.json = {}` → exit 1, `FAIL (discrepancias documentales)`, sin traza. JSON inválido o de tipo no objeto → 2.
- **H2 cerrada:** `HEX` importado de `quality_v3` (`HEX_TOKEN=HEX`); `canonical_file` sigue siendo la única autoridad de rutas y `digest`/`parse_block`/`mission_errors` se reutilizan.
- **H3 cerrada:** `TRUNCATED_HEX` detecta 63 hex contiguos; prueba dedicada. Los 28 manifiestos reales (26 preexistentes + 2 de DET-001) se parsean sin errores de formato.
- **Códigos y clases:** errores 1 (`versión registrada no anclada`, formato inválido, hash divergente), avisos 0 (deriva del árbol, ancla ausente, ciclo anterior), lectura imposible 2 con precedencia sobre 1.
- **Sin regresión:** `validate`, `status`, `can-implement` y `can-close` conservan stdout y códigos frente a `HEAD`; la clasificación solo alimenta contadores.

## Ejecuciones del revisor

| Comando | Exit |
|---|---|
| `python -m unittest tests.test_det001 -v` | 0 — 26 pruebas, OK (skipped=1) |
| `python scripts/quality_cli.py manifest docs/MISSIONS/DET-001/GATE2-INPUT-02.sha256` | 0 — 8/8 |
| `python scripts/quality_cli.py validate` | 0 — 3 avisos v1 históricos |
| `python scripts/quality_cli.py audit --mission DET-001` | 0 |
| `audit` sobre las 13 misiones reales | sin trazas; 1 solo en DOC-001 y DISCOVERY-001 por discrepancias reales documentadas |
| Regresión por módulos (governance, v3, v4, v5, mutations, bootstrap, met, reconstructed, delivery) | 0 en todos |

## Observaciones menores (no bloqueantes)

- `03-IMPLEMENTATION.md` cita «27 manifiestos reales»; el recuento del árbol es 26 preexistentes (28 con los dos de DET-001). Se rectifica en `05-GATE3-EVIDENCE.md` sin reescribir el informe revisado.
- No hay prueba directa del `continue` defensivo para evidencias con elementos no-dict; el comportamiento no produce falso OK y queda como deuda de cobertura menor.
- `audit` devuelve 1 en DOC-001 y DISCOVERY-001 por discrepancias de trazabilidad reales, no por deriva del árbol; el código de salida no es un dictamen de Quality.
- E2E: no aplica a este cambio de herramienta; `E2E NO EJECUTADO` en sentido estricto (no hay producto desplegable).

```protheusai-review
{
  "mission": "DET-001",
  "gate": "gate2",
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
  "evidence": [],
  "date": "2026-11-07"
}
```

