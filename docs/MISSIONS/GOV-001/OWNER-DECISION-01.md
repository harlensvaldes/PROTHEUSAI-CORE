# GOV-001 · Decisión del Owner 01

**Origen:** mensaje del Owner en la sesión `e5be03ee-40b1-4d52-a967-aab163ad6f3c`, recibido 2026-11-05T07:57:02+01:00 (segundo mensaje de usuario de la sesión).
**Transcrito por:** Orchestrator `copilot-sdk-main`, sin modificaciones, antes de iniciar la implementación. Pendiente de confirmación del Owner; no es evidencia de identidad del Owner.
**Propuesta aprobada:** GOV-001-PROPOSAL-v4.md sha256:09D2451FBE865F8E5179C87FEB0F89851FF191D84F24CEBC3A234D8BA7B9CF10

---

# PROTHEUSAI CORE — GOV-001 · Decisión del Owner
**Apruebo la propuesta arquitectónica v4 de GOV-001, condicionada a las siguientes precisiones.**

## Decisiones

- **D1:** aprobado el manifiesto v2. Los manifiestos v1 con PASS no podrán utilizarse para obtener nuevas autorizaciones sin migración o revalidación explícita. Conservar los dictámenes históricos intactos.
- **D2:** mantener `--author` como alias obsoleto, exclusivamente para la autoría inicial que corresponda. Nunca copiarlo automáticamente a `implementation_author`. Emitir advertencia de obsolescencia.
- **D3:** autorizadas las modificaciones mínimas de `AGENTS.md` y `ROLE_MATRIX.md` para definir el rol Orchestrator.
- **D4:** Orchestrator puede desempeñar también Developer si se registra su identidad efectiva. Nunca podrá revisar ni aprobar su propio trabajo.

## Condiciones adicionales obligatorias
**C1 — Identidad:** distinguir identidad declarada, evidencia de identidad y verificación efectiva. La CLI no debe afirmar que ha comprobado una identidad externa cuando solo ha validado campos declarados.

**C2 — Dictámenes:** `PASS_WITH_RESERVATIONS` no equivale a PASS formal ni autoriza transiciones. Cualquier excepción deberá seguir la política explícita de waivers y autorización humana.

**C3 — Trazabilidad:** cada revisión debe identificar inequívocamente el artefacto, su versión/hash, el autor efectivo, el revisor y las evidencias correspondientes.

## Autorización
Queda autorizada la implementación incremental de GOV-001 conforme al diseño aprobado y estas condiciones.

Antes de modificar archivos, incorpora las precisiones al plan y somete cualquier cambio material de diseño a Quality.

Después:

1. Implementa los cambios mínimos.
2. Ejecuta las pruebas positivas y negativas previstas.
3. Verifica compatibilidad con manifiestos históricos según la política aprobada.
4. Solicita revisión independiente de Quality.
5. Conserva los FAIL y versiones anteriores.
6. Registra los cambios mediante commits trazables, respetando los Gates aplicables.
No incorpores todavía skills, frameworks multiagente ni otras funcionalidades de PROTHEUSAI v1.1.

Mantén las comunicaciones compactas y basadas en referencias.

**Detente cuando GOV-001 esté validado y presenta los resultados para mi revisión.**
