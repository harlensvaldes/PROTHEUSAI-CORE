# DISCOVERY-001 · Plan propuesto

Estado: DRAFT; Gate 1 PENDING. Baseline CORE: 461bcfaf5cf82cc860534038f4226f1e1c023564. Autor: Orchestrator actual. Riesgo MEDIUM: cambio documental reversible, sin motor, permisos ni datos; impacto potencial sobre requisitos de futuros proyectos y detectabilidad dependiente de la revisión y escenarios. La matriz ofrece ejemplos y no obliga HIGH; decisión Owner de evaluar MEDIUM en OWNER-DECISION-01.md. No se declara elegibilidad de perfiles o excepciones.

## Objetivo y límites

Incorporar descubrimiento conversacional de producto antes del mandato de desarrollo: comprender finalidad y usuarios, aclarar incertidumbres materiales, registrar necesidades, hipótesis y decisiones por separado, proponer y contrastar un MVP funcional estable, con objetivo, experiencia, funciones esenciales, exclusiones y aceptación verificable. El acuerdo del cliente fundamenta el Charter y la primera misión. No implementar mientras la finalidad esencial o el acuerdo del MVP estén pendientes. El MVP es la primera entrega; Tier 1 y siguientes designan posibles evoluciones funcionales, no riesgos. No implementar su mecanismo. Excluidos APP-003, APP-004, motor, nuevos agentes y Gates.

## Diseño propuesto

- `prompts/00_START_PROJECT.md`: sustituir su instrucción breve por una secuencia conversacional ligera: recoger lo ya expresado, preguntas progresivas según incertidumbres materiales sin repetir respuestas, solicitar referencias cuando aporten evidencia, distinguir hechos del cliente, hipótesis y decisiones confirmadas, devolver propuesta MVP, corregirla con el cliente y registrar el acuerdo explícito con referencia trazable antes del mandato. Identificar futuras peticiones como posibles Tiers funcionales distintos del riesgo, sin construir su mecanismo. Evitar listas obligatorias y presuposiciones técnicas. Mantener pendiente el inicio de implementación si finalidad esencial o acuerdo faltan. Tras acuerdo, completar Charter, arquitectura y primera misión según reglas existentes.
- `START_HERE.md`: añadir al comienzo una referencia al prompt y al acuerdo del MVP antes de arquitectura y desarrollo; mantener los Gates actuales.
- `README.md`: ajustar el inicio rápido para que el prompt sea descubrible en un proyecto nuevo y recordar que debe suministrarse a la herramienta si no lo carga automáticamente. No afirmar compatibilidad runtime probada.
- Reutilizar `docs/PROJECT_CHARTER.md`, `AGENTS.md` y contratos existentes sin duplicar AUT-001. Alternativa descartada: motor nuevo, cuestionario fijo o rol permanente; añadirían infraestructura o rigidez sin necesidad.

## Validación prevista

Ejecutar escenarios documentados con entrada, respuesta observada y comparación con expectativa: idea ambigua pregunta finalidad/usuario relevantes; dato ya respondido no se repite; propuesta técnica aparece como hipótesis; respuestas alimentan objetivo, experiencia, esenciales, exclusiones y aceptación MVP; finalidad esencial sin aclarar impide implementar. Incluir corrección del cliente, ausencia de acuerdo, registro del acuerdo explícito y distinción entre Tier funcional y riesgo. Distinguir revisión textual de interacción real y de ejecución en Codex, Cursor y Claude Code. Ejecutar regresión de gobernanza disponible y `git diff --check`; registrar comandos, salida y entorno. E2E NO EJECUTADO salvo evidencia real.

## Proceso, riesgos y reversión

Gate 1 independiente sobre versión exacta del plan y contratos; únicamente PASS formal habilita implementación conforme a política. Gate 2 revisa diff anclado y Gate 3 evidencia ejecutada y aceptación. El Charter CORE sigue DRAFT con campos [DECIDIR]. El Owner determinó que esta mejora metodológica interna no es desarrollo de una aplicación cliente y que el plan y su decisión definen el alcance; no se declara completado el Charter. Para MEDIUM Gate 1 y 2 requieren I1/G0 y Gate 3 I1/G1 con evidencia de ejecución según `quality/controls.json`; no inferir aislamiento o identidad del nombre de un agente. Riesgos: incoherencia entre entradas, instrucciones que no se cargan en cada runtime, hipótesis tratadas como decisiones, aprobación implícita y pruebas textuales sobreinterpretadas. Reversión mediante parche inverso revisado sobre los archivos afectados, preservando trabajo y registros; no reset destructivo.
