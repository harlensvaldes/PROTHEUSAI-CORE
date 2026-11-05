# OWNER-DECISION-02

## Owner decision 2026-11-05 09:53:41 +01:00

Source: session e5be03ee-40b1-4d52-a967-aab163ad6f3c, event 24ba3f60-0a70-46df-b135-02a0993bdc73, data.content UTF-8 SHA-256 73b48e8b396ff6d0295c0e2927f2f42e6d95ad7201858dd6d55ebf5e35a61f70. Original text follows verbatim.

# PROTHEUSAI — GOV-001 · Decisión del Owner sobre plan v8
He revisado la propuesta GOV-R01–R03.

**GOV-R01: APROBADO.**

Acepto la reconstrucción expresamente identificada, la comprobación contra el hash histórico, la conservación del incidente y la política documental append-only.

**GOV-R03: APROBACIÓN PENDIENTE DE AJUSTE ARQUITECTÓNICO.**

La sustitución de validaciones basadas en prosa por datos estructurados es correcta.

Sin embargo, no apruebo que compartir runtime, usuario del sistema operativo o workspace implique automáticamente ausencia de independencia de autoría.

Necesitamos distinguir:

1. Independencia de autoría: el revisor no produjo ni modificó el trabajo examinado.
2. Aislamiento operativo: separación de ejecución, permisos y credenciales.
3. Nivel de garantía acreditado por las evidencias disponibles.
Propón una clasificación mínima y verificable que permita utilizar PROTHEUSAI con agentes separados de LUNA o Cline dentro de un mismo entorno, sin afirmar garantías de aislamiento inexistentes.

Los requisitos de aislamiento deben ser proporcionales al riesgo y al tipo de Gate.

Conserva el principio de que un agente nunca puede aprobar su propio trabajo.

Revisa también:

- La necesidad de actualizar `schema_version` si introduces incompatibilidades.
- La distinción entre hashes de contenido normalizado y hashes de bytes originales.
- La reducción de controles documentales redundantes.
**GOV-R02: POSPUESTO A GOV-002.**

Acepto las firmas SSH como línea de investigación para atribución e integridad de evidencias, no como requisito universal aprobado.

No debe introducirse una dependencia obligatoria de claves o de infraestructuras externas para proyectos ordinarios.

## Instrucciones
Prepara una revisión focalizada del plan v8, limitada a estas decisiones.

No implementes todavía GOV-R03.

No amplíes GOV-001 con nuevas funcionalidades.

Prioriza una solución portable, sencilla, verificable y proporcional al riesgo.

Presenta las alternativas y sus consecuencias antes de solicitar autorización de implementación.

## Current Owner authorization, recorded by the Orchestrator

The Owner approved architecture v15 with F2+P2, dimensions A/B/C and the proportional matrix provisionally, classifying GOV-001 HIGH; G0, G1 and G2 require explicit verifiable criteria. Governance mechanisms cannot be formally certified solely by their own new controls; a separate review of the author's team is required for closure. Sharing runtime does not automatically defeat independent authorship and declarations are not technical guarantees.

The Owner authorized R01 reconstruction, incident preservation and append-only documentation, and R03 implementation, schema v3, tests and historical compatibility without extending previous approvals. Technical PASS is not formal PASS or a waiver, and CLI blocks must not be bypassed. Commits only after technical verification. R02 and SSH remain GOV-002 research, without mandatory strong isolation. Stop after technical validation; final acceptance is not granted.

Per approved plan R-PLAN/GOV-001-R-PLAN-v15.md and v8 section Sequence: R01 additions, Gate 2/3 technical PASS, then commit; R03 Gate 1 technical PASS, implementation, Gate 2/3 technical PASS, then commit. FAIL, PENDING or PASS_WITH_RESERVATIONS stops progress; no invented PASS.

## Owner authorization in this conversation, transcribed

# PROTHEUSAI CORE — GOV-001 · Decisión del Owner sobre plan v15

**Apruebo la arquitectura revisada y autorizo avanzar con las siguientes condiciones.**

### D1 — APROBADA: F2+P2

Adoptar el informe Quality con un único bloque JSON estructurado y el manifiesto con referencias al dictamen.

Evitar duplicaciones innecesarias.

### D2 — APROBADA

Adoptar las tres dimensiones independientes:

- A: independencia de autoría.
- B: aislamiento operativo.
- C: trazabilidad de evidencias.

Compartir runtime no anula automáticamente la separación de autoría.

No presentar datos declarados como garantías técnicas verificadas.

### D3 — APROBADA CON CONDICIÓN

Adoptar provisionalmente la matriz proporcional propuesta.

Clasificar GOV-001 como HIGH.

Definir G0, G1 y G2 mediante criterios explícitos y verificables.

La modificación de los mecanismos de gobernanza no podrá considerarse formalmente certificada únicamente mediante sus propios controles recién implementados.

Para el cierre de GOV-001 exigiré una revisión adicional separada del equipo autor, con las limitaciones de independencia documentadas.

### D4 — IMPLEMENTACIÓN AUTORIZADA

GOV-R01:

- Recuperar la evidencia mediante reconstrucción declarada.
- Conservar el incidente y su historial.
- Incorporar la regla documental append-only.

GOV-R03:

- Implementar el formato estructurado F2+P2.
- Incorporar los niveles de garantía.
- Actualizar el manifiesto a schema_version 3.
- Añadir las comprobaciones y pruebas previstas.
- Mantener compatibilidad histórica sin extender aprobaciones anteriores.

Ejecuta las revisiones técnicas Gate 1, Gate 2 y Gate 3 sobre las versiones correspondientes.

Los PASS técnicos no sustituyen los PASS formales cuando sus condiciones de independencia todavía no se cumplen. Conserva ese estado explícito y no utilices los dictámenes técnicos para eludir bloqueos de la CLI.

Se autoriza el trabajo técnico dentro de este alcance; esta autorización no equivale a un waiver ni a la aceptación final.

Realiza commits únicamente después de las verificaciones técnicas previstas, preservando el historial existente.

### GOV-002

Permanece como investigación futura. No incorporar firmas SSH ni aislamiento fuerte obligatorio en GOV-001.

### Control de alcance

No añadas nuevas funcionalidades.

No introduzcas más políticas ni esquemas salvo que sean indispensables para las decisiones aprobadas.

Si Quality encuentra un defecto verificable, corrígelo. Si plantea una mejora opcional, regístrala para otra misión sin bloquear innecesariamente el trabajo actual.

### Entrega

Presenta:

- Commits realizados.
- Cambios de código.
- Resultado de pruebas positivas y negativas.
- Dictámenes técnicos y estados formales.
- Riesgos residuales.
- Elementos pendientes para mi aceptación.

**Ejecuta GOV-R01 y GOV-R03 y detente al completar su validación técnica.**
