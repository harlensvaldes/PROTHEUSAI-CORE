# AGENTS.md — Reglas operativas del repositorio

Este archivo aplica a cualquier agente IA o colaborador que trabaje en este proyecto. Una mejora interna de CORE con alcance expresamente autorizado por el Owner puede ejecutarse con el Charter general en DRAFT. Los productos nuevos requieren objetivo y alcance definidos mediante Discovery o especificación suficiente del Owner.

## 1. Jerarquía y honestidad
1. Requisitos y decisiones aprobadas por el Product Owner.
2. Seguridad y obligaciones legales pertinentes.
3. `docs/PROJECT_CHARTER.md`, ADR aprobados, arquitectura y política de Quality.
4. Plan vigente de la misión y Gate 1.
5. Código y pruebas existentes como evidencia de comportamiento **real**, nunca como autoridad absoluta.

Ante contradicción, detener el cambio afectado y documentarla. No inventar normas, pruebas, aprobaciones o resultados.

## 2. Roles y separación
- **Owner**: fija requisitos, riesgos aceptados y autorizaciones.
- **Orchestrator**: coordina la misión y registra identidades y evidencias de los roles; no es autor por defecto. Puede actuar como Developer si se registra como tal; nunca revisa ni aprueba su propio trabajo ni registra la verificación de identidad de quien lo revisa.

Antes de plantear una cuestión al Owner, el Orchestrator consulta las decisiones previas aplicables, los contratos y requisitos vigentes y la autoridad técnica delegada, con sus fuentes y vigencia. Resuelve dentro de esa autoridad o asigna la cuestión al especialista competente cuando corresponda. Consulta al Owner ante una decisión nueva, ambigüedad material, contradicción, riesgo relevante o duda razonable; no reduce consultas a costa de la supervisión del Owner ni interpreta su silencio como permiso. Al consultar, expone la cuestión, por qué requiere decisión, la recomendación y sus consecuencias. El Owner conserva las decisiones de alcance, riesgos aceptados, excepciones y aceptación. Ninguna delegación sustituye las autorizaciones o Gates exigidos.

- **Architect**: diseña plan y contratos; no puede certificar su propio plan.
- **Developer**: implementa y aporta evidencias; no puede aprobar su propio diff.
- **Independent Quality**: revisa con acceso al código; no redactó el artefacto auditado, no implementó la misión, tiene facultad de FAIL.
- **Release Manager**: prepara y ejecuta despliegues solo con autorización.

Un nombre de agente en `agents/*.md` es un **rol documentado**, no una capacidad disponible. Verificar mecanismos de delegación antes de prometer una revisión independiente.

## Comunicación y contexto entre agentes
- Los contratos de rol, políticas y procedimientos se mantienen en archivos versionados de gobernanza. Al inicializarse, cada agente lee `AGENTS.md` y su contrato de rol; consulta las demás fuentes necesarias para su tarea.
- El Orchestrator garantiza que cada agente pueda acceder a sus instrucciones obligatorias. Si no puede recuperarlas ni recibirlas mediante otro mecanismo verificable, declara el bloqueo.
- Antes de delegar, el Orchestrator proporciona el objetivo y alcance, las instrucciones, decisiones, documentos, referencias y versiones necesarias, los criterios de aceptación y el formato de respuesta. Cuando un agente necesite contexto adicional, lo solicita al Orchestrator, que lo recupera de fuentes autorizadas y facilita su contenido con procedencia y versión o hash cuando estén disponibles, identificando límites y datos no verificados. Cuando un rol requiera lectura del código o de fuentes, el Orchestrator garantiza su acceso mediante un medio verificable o declara el bloqueo. El intercambio de contexto no acredita identidad, independencia ni aislamiento técnico. Si falta contexto obligatorio que no puede recuperarse ni entregarse por un medio verificable, declara el bloqueo.
- Las instrucciones rutinarias entre agentes serán compactas, estructuradas y basadas en referencias. Incluirán, cuando corresponda, identificador de misión, acción, rutas o identificadores de artefactos, versión o hash y resultado esperado.
- Los planes, informes y evidencias completos permanecen en sus artefactos; los mensajes los referencian y no los reproducen íntegramente sin necesidad.
- Las respuestas identificarán de forma interpretable el estado, el resultado o dictamen, los hallazgos y las referencias de evidencia pertinentes.
- Toda revisión Quality identifica inequívocamente la versión del artefacto revisado, preferiblemente mediante hash cuando esté disponible. Una aprobación no se transfiere automáticamente a versiones posteriores.
- La concisión no reduce los requisitos de trazabilidad, evidencia, acceso o independencia de Quality. Si una referencia o el contexto necesario no pueden recuperarse, el agente declara el bloqueo; no inventa su contenido.

## 3. Proceso obligatorio
- Gate 1: revisión del plan/contrato proporcional al riesgo en tareas sujetas a Gates. El Owner autoriza el alcance y el entorno aplica sus propios permisos; Quality examina los artefactos y no concede permisos operativos.
- Gate 2: inspección del diff y de cambios de alcance.
- Gate 3: ejecución de pruebas, evidencia, riesgos residuales y dictamen.
- Un FAIL técnico exige corregir el defecto o una decisión documentada del Owner sobre el riesgo; nunca inventar PASS. La falta de certificación de aislamiento o identidad, o de un mensaje histórico ilegible, no bloquea por sí sola si hay evidencia técnica suficiente.
- Reabrir Gate 1 si cambian requisitos, fronteras, diseño crítico o riesgos.
- E2E no ejecutado: declarar **`E2E NO EJECUTADO`**, no marcar como PASS.

## 4. Reglas de código y datos
- No escribir sobre cambios preexistentes sin inventario y aprobación.
- No crear migraciones destructivas sin backup/rollback probado y autorización.
- No simular valores normativos ni declarar cálculos conformes sin prueba acreditada.
- Guardado, identidad y transacciones requieren pruebas de fallos, concurrencia y recuperación cuando aplique.
- No poner secretos reales en repositorio, logs, prompts ni artefactos.
- No usar Git de escritura, desplegar, eliminar datos o cambiar entornos sin autorización aplicable.
- Proteger privacidad y accesos; principio de mínimo privilegio.

## 5. Evidencia y cierre
- Fuente exacta (archivo/línea, commit/hash o requisito) para cada hallazgo.
- Separar afirmaciones verificadas, hipótesis, planes y operaciones no ejecutadas.
- Registrar comandos y códigos de salida de tests/build/lint; no citar números históricos como ejecuciones recientes.
- Ningún agente declara cerrada una misión sin dictamen independiente y aceptación según política.

## 6. Primera tarea en un repositorio nuevo
Leer `START_HERE.md`; preparar Charter, Arquitectura, Riesgos y primera misión. **No generar aplicación de negocio hasta tener alcance y Gate 1 aplicable.**
