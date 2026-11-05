# Matriz de responsabilidades (RACI simplificada)

| Acción | Owner | Architect | Developer | Quality independiente | Release |
|---|---|---|---|---|---|
| Priorizar requisito | A | C | I | I | I |
| Diseñar solución | A | R | C | C | I |
| Emitir Gate 1 | I/A de decisión | C | I | R | I |
| Implementar | I | C | R | I | I |
| Emitir Gate 2 | I | C | C | R | I |
| Ejecutar tests | I | C | R | verifica evidencia | I |
| Dictamen Gate 3 | A de aceptación | C | C | R | I |
| Desplegar | A | C | I | I | R |

R = ejecuta; A = autoridad/aprueba; C = consultado; I = informado. El mismo individuo no puede ejercer papel de autor y revisor de un mismo artefacto.

## Registro de herramientas
| Agente/rol | Runtime real | Herramienta de invocación | Lectura repositorio | Autorizado | Verificado |
|---|---|---|---|---|---|
| Architect | [DECIDIR] | [DECIDIR] | [sí/no] | [sí/no] | [fecha/evidencia] |
| Developer | [DECIDIR] | [DECIDIR] | [sí/no] | [sí/no] | [fecha/evidencia] |
| Quality | [DECIDIR] | [DECIDIR] | [sí/no] | [sí/no] | [fecha/evidencia] |

No rellenar con capacidades hipotéticas.
