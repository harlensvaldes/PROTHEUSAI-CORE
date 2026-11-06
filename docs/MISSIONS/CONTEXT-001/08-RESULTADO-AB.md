# CONTEXT-001 · Resultado de validación A/B

## Condiciones y alcance

Protocolo anterior a los lanzamientos: `05-EXPERIMENTO.md`. Raíz MET-001 `01a1b237-0edf-7182-b1cd-c120f4816af0`, inicio de observación anterior a ambos 2026-11-06T19:13:01Z, corte exclusivo común 2026-11-06T19:14:49.791Z. A `01a1b247-ae68-7b92-9c81-0c880f3455a7`; B `01a1b247-c6b6-7fd0-93e8-581d85a46e1b`, identificados por `session_meta.payload.source.subagent.thread_spawn`. `turn_context` declara `gpt-6.1-terra`, esfuerzo `high`, en ambos. Cada hilo era nuevo, con igual pregunta, permisos y fuentes accesibles; el tratamiento A prescribió cuatro documentos completos y B checkpoint con fuentes bajo demanda. Se ejecutaron en paralelo sobre el mismo árbol, pero no son condiciones perfectamente aisladas: arranques diferentes, caché, instrucciones y conducta de lectura, y el checkpoint estaba obsoleto. Una sola tarea no acredita un efecto general.

Las respuestas finales originales del registro del runner se conservan como eventos JSON `05-RESPUESTA-A.json` y `05-RESPUESTA-B.json`. `05-MET-AB.json` conserva salida íntegra MET-001, sin mensajes; sus registros originales JSONL permanecen en el directorio local de sesiones y se identifican en su campo `provenance`. El corte y la atribución por hilo son observados, no garantía de exhaustividad: MET-001 notificó dos errores de lectura de archivos, sin acreditar aquí si afectaron a estos hilos.

| Medida observada | A convencional | B selectivo |
|---|---:|---:|
| Entrada | 150.664 | 169.856 |
| Caché incluida en entrada | 136.960 | 137.088 |
| Entrada menos caché | 13.704 | 32.768 |
| Salida | 2.380 | 2.354 |
| Total | 153.044 | 172.210 |
| Respuestas | 5 | 6 |
| Tiempo transcurrido entre eventos task_started y task_complete | 58,901 s | 63,816 s |

Tiempos: A 19:13:25.357–19:14:24.258 UTC; B 19:13:31.722–19:14:35.538 UTC. Son duraciones de tarea observadas, no tiempo activo y no eliminan efectos de ejecución paralela. No son importes ni facturación.

A declaró nueve operaciones agrupadas, incluyendo una búsqueda fallida y un intento de archivo inexistente; B declaró nueve llamadas de comandos y una consulta al runner. Las agrupaciones son distintas, no permiten comparar cuantitativamente las consultas adicionales de forma fiable. B leyó el checkpoint y consultó además el encargo, plan, evidencia, continuidad, dictamen y protocolo; por tanto la prueba no demuestra una reducción del contexto efectivamente procesado. A no detectó el experimento en curso; B sí lo identificó y detectó que el checkpoint seguía refiriendo un informe ya terminado. Ambas conservaron decisiones centrales, Gate 3 PASS_WITH_RESERVATIONS, límites y aceptación del Owner; B omitió explicitar que MCP Memory es opcional y externo. Ver contraste independiente, referencias y demás límites en `07-VERIFICACION.md`. Se encontraron omisiones, no decisiones inventadas ni referencias citadas inexistentes.

## Cortes previos y recomendación

`05-MET-CORTE-1.json` y `05-MET-CORTE-2.json` son los dos resultados originales acumulados de la misma raíz y misión, a 18:58:11.971Z y 19:01:02.219Z. El primero abarca 20 respuestas, entrada 708.681, caché 573.952, entrada menos caché 134.729, salida 3.109 y total 711.790. El segundo abarca 44 respuestas, entrada 1.833.670, caché 1.667.200, entrada menos caché 166.470, salida 11.016 y total 1.844.686. Ambos son parciales con dos errores de lectura; el segundo incluye registros anteriores y no se suma al primero. No son tratamientos A/B ni miden toda la misión posterior al corte.

Recomendación al Owner: conservar el mecanismo con reservas como índice operativo y fuente de recuperación, condicionado a comprobar vigencia y originales; no afirmar eficiencia demostrada ni aceptación final. En esta muestra B procesó más tokens y tardó más, y su detección de obsolescencia fue útil; no demuestra reducción de contexto ni ahorro económico. No se comprobó una nueva sesión principal ni transferencia de manejadores; **E2E NO EJECUTADO**. Gate 3 histórico sigue siendo PASS_WITH_RESERVATIONS y la aceptación permanece pendiente del Owner. No se han cambiado mecanismos de gobernanza ni registrado APPROVED.
