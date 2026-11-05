# Estrategia de pruebas

## Pirámide orientativa
- Unitarias: contratos puros, casos frontera, errores y valores inválidos.
- Integración: persistencia, APIs, identidad, permisos, migraciones, concurrencia y colas.
- UI: estados, teclado, foco, mensajes, rutas, no pérdida de ediciones.
- E2E: recorridos críticos con servicios reales y autorización explícita.
- No funcionales: rendimiento, seguridad, recuperabilidad, observabilidad, accesibilidad según riesgo.

## Matriz de requisitos
| Req ID | Riesgo | Evidencia de prueba | Estado (NOT_RUN/PASS/FAIL) | Fuente |
|---|---|---|---|---|
| [DECIDIR] | [DECIDIR] | [DECIDIR] | NOT_RUN | |

## Reglas de evidencia
- Registrar comando exacto, versión, fecha, entorno, salida/return code y artefactos.
- Mantener tests que acreditan módulos compartidos; no borrar test solo porque su pantalla se retira.
- Evitar tests que prueban detalles incidentales mientras omiten contratos de datos.
- Pruebas antiguas pueden codificar bugs: nunca conservar un error solo para mantener la suite verde.
- Un Gate de diseño no convierte escenarios no ejecutados en resultados verificables.

## Línea base inicial
Tests existentes: [POR MEDIR], fallos conocidos: [POR MEDIR].
