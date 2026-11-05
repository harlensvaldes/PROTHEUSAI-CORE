# Política de calidad · Engineering Project Foundation

## Objetivo
Evitar errores que comprometan contratos, datos, seguridad y funcionamiento; aportar evidencia verificable y separación real de responsabilidades. Política adaptativa por nivel de riesgo, nunca mero trámite.

## Gate 1 · Design review
**Entrada:** propósito, requisitos, límites, riesgos, contratos, alternativas descartadas, archivos afectados, pruebas previstas, reversión, responsable y baseline de código.

**Revisión:** otro agente/persona que no redactó el plan; examina fuente real, conflictos y escenarios negativos. Puede declarar `PASS`, `PASS_WITH_RESERVATIONS`, `FAIL` o `PENDING` según el protocolo del proyecto. Si política exige PASS explícito, las reservas no lo sustituyen.

**Salida necesaria:** informe con identidad, independencia, hallazgos, evidencia archivo/línea o documentación, fecha, decisión y autorización del propietario cuando proceda. **No implementar con Gate 1 FAIL/PENDING.**

## Gate 2 · Diff review
**Entrada:** Gate 1 vigente, baseline exacta, diff delimitado, pruebas modificadas, migraciones y compatibilidad. Confirmar que no se mezclan modificaciones anteriores no autorizadas.

**Revisión:** code review independiente, riesgos, seguridad, concurrencia, accesibilidad, alcance y pruebas que se eliminan; cambios materiales reabren Gate 1.

## Gate 3 · Verification & acceptance
**Entrada:** código revisado, comandos reales y resultados, pruebas negativas, regresión, build/lint, evidencias de integración/E2E cuando aplique, incidencias y riesgos residuales.

**Regla:** no inventar PASS ni usar números de pruebas de hace semanas. Cada suite: comando, fecha, entorno, código de salida y artefacto cuando exista. `NOT_RUN` no es `PASS`.

## Dictámenes
- `PENDING`: falta revisor, información o evidencia.
- `FAIL`: defecto bloqueante. No avanzar.
- `PASS`: aprobada la etapa correspondiente, después de revisión real.
- `PASS_WITH_RESERVATIONS`: solo reservas explícitas y no bloqueantes; su admisibilidad para avanzar exige política/owner.

## Independencia
- Quien creó el plan no emite Gate 1.
- Quien programó el diff no emite Gate 2.
- Quien ejecutó pruebas puede adjuntar resultados, pero no auto-certifica su interpretación como aceptación independiente.
- Un prompt no instala un subagente. Indicar herramienta real de delegación o revisor humano.

## Reapertura
Reabrir Gate 1 ante cambio de arquitectura, alcance, esquema, reglas de autorización, datos, cálculo crítico o riesgos. Reabrir Gate 2 si cambia código tras revisión. Repetir Gate 3 si cambia binario/imagen después de las pruebas.

## Riesgo adaptativo
Ver `quality/RISK_MATRIX.md`. LOW usa evidencias ligeras y revisión proporcional; HIGH/CRITICAL requieren evidencias rigurosas y escenarios adversos. No confundir cambios visuales con cambios de guardado/permisos.

## Separación del release
Gate 3 PASS **no despliega** ni asegura aptitud legal o validación profesional de un dominio crítico. Seguir `docs/RELEASE_POLICY.md`.
