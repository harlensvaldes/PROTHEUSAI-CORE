# Política de calidad · Engineering Project Foundation

## Objetivo
Evitar errores que comprometan contratos, datos, seguridad y funcionamiento; aportar evidencia verificable y separación real de responsabilidades. Política adaptativa por nivel de riesgo, nunca mero trámite.

## Gate 1 · Design review
**Entrada:** propósito, requisitos, límites, riesgos, contratos, alternativas descartadas, archivos afectados, pruebas previstas, reversión, responsable y baseline de código.

**Revisión:** otro agente/persona que no redactó el plan, cuando pueda establecerse con los registros disponibles; examina fuente real, conflictos y escenarios negativos. Puede declarar `PASS`, `PASS_WITH_RESERVATIONS`, `FAIL` o `PENDING`. El dictamen informa al Owner; no sustituye la autorización operativa del entorno ni transforma reservas en PASS.

**Salida necesaria:** informe con revisor declarado, separación de autoría cuando sea verificable, hallazgos, evidencia archivo/línea o documentación, fecha y dictamen. El Owner autoriza el alcance y el entorno aplica permisos; Quality no concede permisos operativos. La falta de identidad certificada o aislamiento acreditado no bloquea por sí sola.

## Gate 2 · Diff review
**Entrada:** Gate 1 vigente, baseline exacta, diff delimitado, pruebas modificadas, migraciones y compatibilidad. Confirmar que no se mezclan modificaciones anteriores no autorizadas.

**Revisión:** code review independiente, riesgos, seguridad, concurrencia, accesibilidad, alcance y pruebas que se eliminan; cambios materiales reabren Gate 1.

## Gate 3 · Verification & acceptance
**Entrada:** código revisado, comandos reales y resultados, pruebas negativas, regresión, build/lint, evidencias de integración/E2E cuando aplique, incidencias y riesgos residuales.

**Regla:** no inventar PASS ni usar números de pruebas de hace semanas. Cada suite: comando, fecha, entorno, código de salida y artefacto cuando exista. `NOT_RUN` no es `PASS`.

## Dictámenes
- `PENDING`: falta revisor, información o evidencia.
- `FAIL`: defecto técnico identificado; corregirlo o documentar la decisión del Owner sobre el riesgo. No se convierte en PASS.
- `PASS`: aprobada la etapa correspondiente, después de revisión real.
- `PASS_WITH_RESERVATIONS`: reservas explícitas que no son un PASS. El Owner decide la aceptación de riesgos y el alcance autorizado; no se cambia automáticamente ningún dictamen histórico.

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

## Compatibilidad histórica: waiver v4 de piloto ficticio

Los registros v4 existentes pueden contener una excepción histórica de Gate 1 HIGH para piloto local ficticio. Esa excepción no es PASS, no acredita identidad ni aislamiento y no modifica FAIL históricos. Su lectura conserva alcance, vigencia y revocación; no constituye un requisito nuevo para usar I0/G0.

En el esquema v4, el Gate 1 permanece PENDING y un informe separado conserva su PASS exclusivamente técnico. La CLI valida coherencia declarada y emite `MANUAL_OWNER_VERIFICATION_REQUIRED` con salida no cero cuando el registro está vigente; no autentica al Owner, no certifica I1/G1 ni concede permisos. Si faltan datos, el registro no es válido, la excepción expiró o se registró una revocación, la acción queda BLOCKED. El Owner conserva y coteja la autorización, las revocaciones, evidencias e historial fuera de la mera declaración del agente. Los archivos y hashes editables no garantizan autenticidad ni completitud; si no se pueden verificar, no avanzar. Los lectores externos antiguos y acciones fuera de la CLI no están controlados por esta política automatizada.

## Independence minimums and reopening

For v3/v4 the current risk-by-Gate matrix is quality/controls.json independence_minimums; I0/G0 is permitted for all risks, without requiring identity or isolation evidence. Execution evidence and artifact integrity remain proportional to risk. Declarations are not certifications. Historical verdicts retain their original meaning and never transfer to changed artifacts; future evaluations apply current rules. The Owner accepts the result. The CLI cannot reconstruct historical matrices, authenticate identities, or decide technical sufficiency.

## Perfil ordinario v5 para pilotos locales ficticios

Una nueva misión v5 puede declarar `LOCAL_FICTIONAL_EXPERIMENTAL` únicamente si es experimental, local, usa exclusivamente datos ficticios y no tiene exposición pública ni uso operativo. CRITICAL queda excluido. El Owner mantiene la autoridad sobre su elegibilidad y las autorizaciones de implementación y aceptación. Un cambio real de alcance o revocación conocida detiene la acción y se eleva según AGENTS.md.

Para este perfil, los tres Gates conservan revisión de Quality por autor distinto, declaración de autoría y trazabilidad, pero admiten I0/G0 sin evidencia G1 de identidad. I0 no acredita identidad ni separación de contexto. Se conserva el anclaje Gate 2 MEDIUM/HIGH y el reporte de pruebas reales de Gate 3. La consistencia formal de los registros exige PASS exacto y PWR no lo sustituye; la CLI no concede ni deniega permisos del entorno o del Owner. No autentica personas ni verifica elegibilidad real. El alcance declarado se fija por digest en cada revisión; no prueba que no haya habido cambios y restauración entre comprobaciones.

Este perfil no altera matrices, decisiones ni semántica de v1–v4, y no se adopta automáticamente en proyectos existentes. El Owner conserva la decisión de adopción. Las reservas e historia de misiones anteriores no se convierten en PASS.
