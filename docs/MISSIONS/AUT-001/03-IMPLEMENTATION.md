# AUT-001 · Registro de implementación

**Gate 1 formal:** PENDING; no aprobado. Ejecución limitada autorizada por el Owner en `OWNER-ARRANQUE-01.md`; no es waiver ni PASS.
**Developer declarado:** TERRA. **Base commit:** `bff1de00f98bc2caa40e2e7be057c0adc4e7b649`; árbol CORE limpio al inicio.

## Archivos realmente modificados
| Archivo | Qué cambió | Por qué | Gate 1 sección |
|---|---|---|---|
| `AGENTS.md` | Contrato de decisión y entrega de contexto del Orchestrator | Aplicar reglas Owner sin duplicar fuentes normativas | Contrato propuesto |
| `README.md` | Instrucción de suministrar `AGENTS.md` y verificar disponibilidad | Uso portable sin afirmar carga automática | Contrato propuesto |
| `docs/MISSIONS/AUT-001/` | Autorización, roles declarados, escenarios y revisión | Preservar evidencia y límites reales | Gates y verificación |

## Diferencias de alcance
Sin ampliación de alcance identificada. Los Gates formales permanecen PENDING y el Charter CORE continúa DRAFT. No se modificó APP-002 ni se inició APP-003.

## Pruebas locales ejecutadas
| Comando | Entorno/fecha | Exit code | Resultado |
|---|---|---|---|
| `git apply --check --unidiff-zero docs/MISSIONS/AUT-001/PROPUESTA-DIFF.patch` | Copia aislada, 2026-11-05 | 0 | Parche aplicable, no prueba de conducta |
| `python -m unittest discover -s tests -q` | Python local, copia aislada, 2026-11-05 | 0 | 180 ejecuciones, dos omitidas; incluye fixtures heredadas repetidas |
| `python scripts/quality_cli.py validate` | Copia aislada, 2026-11-05 | 0 | Consistencia estructural, no certifica Quality ni identidades |
| `git diff --check` | Copia aislada, 2026-11-05 | 0 | Sin errores de espacios del diff; Git advirtió conversión de finales de línea |

TERRA comparó SHA-256 de bytes del plan `facfafd9baf7fa26d1f8672bb814cc45c98b29fb9d1ddbd90df67c2157966c9e` con la versión indicada por Quality y reconstruyó el parche desde los tres textos literales del plan. Los bytes del parche tras normalizar CRLF→LF coincidieron exactamente con la reconstrucción y con SHA-256 `b25ea5b5a7676872e1487dcab5fb46629e30dfe864a3e50c64ebc23f0a28ff65`. En un primer intento se comparó por error el hash LF del plan con el hash de bytes y falló; se corrigió y se repitió antes de aplicar ningún cambio.

Diez escenarios sintéticos fueron respondidos por un agente distinto y se registran en `ESCENARIOS-01.md`; no son una suite de runtime ni demuestran comportamiento general del modelo. Quality revisó el diff entregado en `REVISION-TECNICA-DIFF-01.md`.

## Riesgos y deuda técnica
No se verificó carga ni obediencia automática en Codex, Cursor o Claude Code; estos contratos requieren entrega y comprobación en cada entorno. Una prueba real de enlaces simbólicos se omitió por privilegios Windows y otra prueba quedó omitida en la suite. El estado y custodia de identidad/aislamiento permanecen no acreditados. E2E NO EJECUTADO.
