# Revisión técnica del plan 02 y su base

Fecha 2026-11-05. Revisor declarado /root/core_quality, agente delegado mediante herramienta de colaboración, distinto del autor declarado /root/architect; no redacté el plan ni implementé la reforma. Acceso de lectura comprobado. Contexto heredado y entorno compartido: no certifico I1 ni identidad G1. Baseline Git indicada 11a6f189fd8dc2459232c438e046f58440070b91. Unidad revisada: PLAN-REFORMA-QUALITY-01.md sha256_lf 4e6c72f329fc8858ad737cb7beb2d8dd2bdd1ac4265000c5cd544285c74b96bd y PLAN-REFORMA-QUALITY-02.md sha256_lf 1540dbc0651c6b2cf265c906fcd9b57535665e952c535077bfd518d156a7462d; ambos hashes recalculados.

**Dictamen técnico: PASS_WITH_RESERVATIONS. Gate 1 formal: PENDING.** Según docs/QUALITY_POLICY.md solo PASS habilita la transición; esta revisión no acredita I1/G1 vigentes ni permite implementar. El FAIL de la versión 01 se conserva. No se ejecutaron pruebas. E2E NO EJECUTADO.

## Resolución de hallazgos anteriores

- Anclaje: plan 02 líneas 11-15 define digest del objeto completo, enlace a documento y declara que restaurar datos puede ocultar cambios. Resuelve la especificación, no autentica historial ni detecta revocaciones.
- Semántica de comandos: líneas 21-30 separan PENDING válido de can-implement/can-close bloqueados y mantienen comportamiento legado.
- Documento: líneas 17-19 fijan formato, campos, duplicados, proyecto y hash; la CLI no autentica autor ni vigencia.
- Bootstrap: línea 34 define vía ordinaria bajo matriz anterior y BLOCKED si no hay vía válida. La autorización extraordinaria alternativa es solo propuesta condicional, no permiso recibido y no convierte el Gate en PASS. Debe comprobarse su compatibilidad con la instrucción Owner de no crear otro mecanismo de waiver; ninguna excepción queda aprobada por este informe.
- Proporcionalidad y sesión: líneas 7-9 reducen cinco banderas a un perfil y declaran sesión cuando esté disponible. Persiste reserva: documento Owner adicional y bloque estructurado por misión, digest por revisión y cotejo manual antes de actuar son carga nueva; el plan no demuestra que no exista opción más sencilla que mantenga las garantías requeridas. El Owner pidió regla sencilla y evitar nuevas capas. Verificar que esta carga sea necesaria y aceptable antes de adoptarla como política.

## Reserva de prueba

Plan 02 línea 38 pide que digest y hash LF fallen ante «cualquier cambio», pero el digest canónico debe permanecer estable ante cambios solo de orden o espacios del JSON de scope y el hash LF del documento no cambia si solo cambia scope. Precisar oráculos por propiedad y archivo, con pruebas de equivalencia canónica y de modificación semántica. No se ha ejecutado ninguna prueba.

Fuente Owner leída directamente: evento user_message línea 800 de rollout-2026-11-05T16-57-50-01a1ac6e-4676-7602-b3b7-51c843e805d6.jsonl; autoriza reforma ordinaria, pide Quality distinto, trazabilidad, no I1/G1 bloqueante para pilotos, evitar nuevas capas, pruebas y propuesta APP-003 separada. Fuentes técnicas contrastadas: AGENTS.md, agents/quality.md, docs/QUALITY_POLICY.md, docs/QUALITY_EVIDENCE_PROTOCOL.md, quality/controls.json, scripts/quality_cli.py y scripts/quality_v3.py. Charter consultado DRAFT. Revisión estática; no se verificaron funcionamiento de v5 inexistente, identidad o integridad externa de registros.