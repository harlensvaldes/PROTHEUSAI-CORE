# CONTEXT-001 + DET-001 · Diagnóstico y evidencia

## Diagnóstico

DELIVERY-001 `../DELIVERY-001/METRICAS-03.md` registra 376 respuestas y 43.966.778 tokens observados, con 43.288.448 de entrada en caché; no atribuye fracción evitable ni facturación. Los mensajes, salidas y herramientas se acumulan en el contexto hasta que el runner lo gestione; el volumen de coordinación y resultados extensos es un indicio, no una atribución causal medida. El runner de esta ejecución informa de compactación automática al agotarse el contexto y de continuación desde resumen; no expone aquí una orden verificable para crear una nueva sesión principal o transferir manejadores. Las herramientas nativas permiten crear, consultar, mensajear y esperar subagentes; `fork_turns=none` no transmite historial, por lo que hay que proporcionar instrucciones y referencias. Comparten workspace y permisos. El estado de trabajos debe verificarse en el runner; los archivos no reanudan procesos.

Documentación oficial consultada: [contexto y compactación](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.3-codex) y [sesiones de Agents API](https://developers.openai.com/api/docs/guides/agents-api/sessions). Esta última describe otro producto y no acredita disponibilidad de sus API en esta ejecución. Escribir un checkpoint no compacta ni elimina el historial.

MET-001 deduplica registros observados, suma uso por respuesta y ofrece agrupación por hilo y ventanas configuradas. Caché está incluida en entrada y razonamiento en salida; no acredita cobertura completa, identidad de facturación, causalidad, ciclos Quality ni coste real. `docs/MET-001.md` describe sus límites. Se reutilizan Git, `quality_cli.py` y MET-001; no se justificó otro script para hashes, estado o agregación.

## Plan del experimento

Para una futura comparación A/B: repetir una misma tarea de recuperación de decisiones y evidencias sobre el mismo repositorio y estado, con iguales criterios y revisores; A con procedimiento habitual y B con checkpoint y recuperación selectiva. Registrar cortes UTC y raíz de cada sesión, MET-001, respuestas y delegaciones, tiempo transcurrido, lecturas repetidas observables, correcciones y dictamen. No mezclar caché con entrada adicional ni estimar gasto sin tarifas aplicables verificadas. Aquí no se ejecutó A/B equivalente: no hay base para calcular ahorro. DELIVERY-001 tiene otro alcance y no constituye control.

## Comprobaciones

- Gate 1: `/root/quality`, revisor independiente mediante herramienta de delegación, PASS técnico sobre `01-PLAN.md`, SHA-256 `846c07a228e7fa9fd2198d8e6d23db1832c93293b197a4cf8ec37f6bb083073b`. Sin identidad ni aislamiento certificados.
- Baseline de esta misión: `python scripts/met001.py --sessions "$env:USERPROFILE/.codex/sessions" --session-id $env:CODEX_SESSION_ID --cutoff 2026-11-06T18:58:11.971Z --output "$env:TEMP/context001-baseline"`; salida 0, estado parcial por dos errores de lectura: 20 respuestas, entrada 708.681, caché 573.952, entrada menos caché 134.729, salida 3.109, total 711.790. No es una medición antes/después equivalente ni coste.
- Segundo corte acumulado: mismo comando, cutoff `2026-11-06T19:01:02.219Z`, output `$env:TEMP/context001-final`; salida 0, parcial por dos errores de lectura. 44 respuestas; entrada 1.833.670, caché 1.667.200, entrada menos caché 166.470, salida 11.016, total 1.844.686. Tiempo entre cortes 170,248 s, transcurrido y no tiempo activo. No mide toda la misión posterior al corte ni compara tratamientos equivalentes. Delegaciones invocadas hasta este corte: Quality y continuidad; corrección observada: incorporar la fuente del Owner. Lecturas repetidas no cuantificadas.
- `python -m unittest discover -s tests -p test_met001.py`: 5 pruebas, salida 0, Python 3.13.12. `git diff --check`: salida 0; los archivos nuevos requieren revisión directa.
- `/root/continuidad`, creado con `fork_turns=none`, recuperó objetivo, límites, pendientes, Git y estado de agentes leyendo checkpoint y fuentes. Comprobó el hash del plan y rechazó el hash de ceros y la referencia inexistente preparados para prueba. Al principio detectó que la fuente original del Owner no estaba accesible; se incorporó una copia exacta en `00-ENCARGO-OWNER.md` y se actualizó la referencia. El agente confirmó hash y coherencia de decisiones con la copia; no pudo cotejarla independientemente con el adjunto original. Esta prueba no crea ni renueva la sesión principal ni demuestra transferencia de manejadores.

E2E NO EJECUTADO: no se verificó una nueva sesión principal. La aceptación corresponde al Owner.
