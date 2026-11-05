# Matriz de responsabilidades (RACI simplificada)

| Acción | Owner | Orchestrator | Architect | Developer | Quality independiente | Release |
|---|---|---|---|---|---|---|
| Priorizar requisito | A | I | C | I | I | I |
| Registrar identidades y evidencias de roles | A | R | C | C | verifica | I |
| Diseñar solución | A | I | R | C | C | I |
| Emitir Gate 1 | I/A de decisión | I | C | I | R | I |
| Implementar | I | R solo si registrado como Developer | C | R | I | I |
| Emitir Gate 2 | I | I | C | C | R | I |
| Ejecutar tests | I | I | C | R | verifica evidencia | I |
| Dictamen Gate 3 | A de aceptación | I | C | C | R | I |
| Desplegar | A | I | C | I | I | R |

R = ejecuta; A = autoridad/aprueba; C = consultado; I = informado. El mismo individuo no puede ejercer papel de autor y revisor de un mismo artefacto. El Orchestrator no es autor por defecto; si implementa, figura como Developer y queda excluido de revisar, aprobar o registrar la verificación de identidad del revisor de ese trabajo.

## Registro de herramientas
| Agente/rol | Runtime real | Herramienta de invocación | Lectura repositorio | Autorizado | Verificado |
|---|---|---|---|---|---|
| Orchestrator | [DECIDIR] | [DECIDIR] | [sí/no] | [sí/no] | [fecha/evidencia] |
| Architect | [DECIDIR] | [DECIDIR] | [sí/no] | [sí/no] | [fecha/evidencia] |
| Developer | [DECIDIR] | [DECIDIR] | [sí/no] | [sí/no] | [fecha/evidencia] |
| Quality | [DECIDIR] | [DECIDIR] | [sí/no] | [sí/no] | [fecha/evidencia] |

No rellenar con capacidades hipotéticas.
