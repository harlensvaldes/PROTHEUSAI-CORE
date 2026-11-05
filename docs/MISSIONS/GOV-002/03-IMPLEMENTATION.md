# GOV-002 · Registro de implementación

**Gate 1 formal:** PENDING; no se ha aprobado ni eludido la CLI. Inicio extraordinario autorizado en `OWNER-ARRANQUE-01.md`; revisión técnica de plan en `REVISION-TECNICA-PLAN-02.md` no acredita I1/G1.
**Developer declarado:** TERRA. **Base:** `78374146993c4661dddcf1f9c66edff5eb3cfbfa`, árbol CORE original limpio al comenzar.

## Archivos realmente modificados
| Archivo | Qué cambió | Por qué | Gate 1 sección |
|---|---|---|---|
| `scripts/quality_cli.py`, `scripts/quality_v3.py`, `scripts/quality_v4.py` | Validación estructural y diagnóstico manual de excepción acotada | No registrar PASS ni otorgar autorización autónoma | Contrato v4 |
| `tests/test_governance_v4.py` | Casos positivos y negativos de waiver | Comprobar límites y regresiones | Pruebas |
| `docs/QUALITY_POLICY.md`, `docs/QUALITY_EVIDENCE_PROTOCOL.md`, `docs/MISSIONS/README.md` | Política propuesta, límites y uso | Trazabilidad y comprobación humana | Contrato v4 |

## Diferencias de alcance
La CLI informa `MANUAL_OWNER_VERIFICATION_REQUIRED` con salida no cero para el carril excepcional; se requiere una transición operativa humana no contemplada por el autorizador actual. No se aplica a APP-002 ni cambia su Gate. Quality revisó fragmentos críticos, no se presenta esa revisión como examen íntegro o Gate formal.

## Pruebas locales ejecutadas
| Comando | Entorno/fecha | Exit code | Resultado |
|---|---|---|---|
| `python -m unittest discover -s tests -q` | Python local, 2026-11-05, checkout aislado | 0 | 180 ejecuciones, dos omitidas; incluye fixtures heredadas repetidas. El test nuevo de symlink quedó SKIPPED por WinError 1314 |

## Riesgos y deuda técnica
Identidad y autorización del Owner no autenticadas por CLI; riesgo de omisión o alteración de revocaciones e historia; TOCTOU; consumidores externos NO VERIFICADOS. La copia temporal no prueba custodia duradera. E2E NO EJECUTADO.
