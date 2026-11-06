# DESIGN-001 · Plan de integración

Autor: codex `/root`, Orchestrator y Developer. Fecha: 2026-11-06. Baseline Git `1162d89`; cambios preexistentes sin seguimiento de CONTEXT-OPT-001 inventariados por `git status` y fuera de alcance. El Owner autoriza la implementación interna descrita en su encargo de esta sesión; no acepta anticipadamente el resultado. No se crean Gates nuevos; se aplican Gate 1, 2 y 3 existentes con Quality independiente.

## Diseño y límites

Crear `agents/creative_director.md` como contrato portátil de rol convocable, no como capacidad instalada o permiso nuevo. TERRA determina necesidad según interfaz significativa, evolución visual y cambios sin UX, transmite alcance, fuentes, versiones, criterios y restricciones; usa delegación nativa cuando exista y declara limitación cuando no. Interpretar intención y referencias, producir dirección concreta y proporcional, distinguir decisiones del Owner y supuestos, y cuidar flujo, jerarquía, componentes y estados, responsive y accesibilidad. Resultado de siete elementos definido por el Owner y comunicación compacta; los artefactos visuales son opcionales, identificados y respetan derechos. El rol propone, no sustituye a Architect, Developer o Quality ni acepta por Owner.

Integrar la convocatoria en `AGENTS.md` y `prompts/00_START_PROJECT.md` con Discovery conversacional, y las colaboraciones en `agents/architect.md`, `agents/developer.md` y `agents/quality.md`; ninguna añade aprobaciones visuales o criterios estéticos subjetivos como fallos. Skills: seleccionar solo entre disponibles y pertinentes; no declarar `frontend-design` disponible si no figura; `imagegen`, `computer-use`, `visualize` y `sites` son capacidades condicionales, no agentes adicionales ni instalaciones. No modificar permisos, runner, productos, memoria, misiones históricas ni despliegues.

Actualizar `bootstrap/allowlist.json` con el único archivo nuevo de rol; ampliar `tests/test_bootstrap001.py` para comprobar contenido y procedencia del rol y excluir expedientes de misión. Bootstrap opera sobre commit limpio y no se rediseña. Evitar tocar archivos previos del usuario. Las reglas se guían por necesidad, no una matriz obligatoria; conservar decisiones anteriores para evolución visual.

## Verificación

Tras Gate 1 independiente, implementar el diff y ejecutar pruebas del bootstrap. Escenarios ficticios acotados mediante mecanismos de delegación reales disponibles: (1) TERRA decide convocar para producto con UI significativa, delega con contrato, obtiene decisiones UX/UI y Developer comprueba aplicabilidad; Quality retiene el control; (2) TERRA decide no convocar para CLI sin UX significativa y documenta que el flujo no depende del rol; (3) TERRA delega una evolución visual incluyendo identidad y decisiones previas, y comprueba coherencia sin rehacer Discovery. Registrar instrucciones, fuente de decisiones y resultados reales; distinguir comportamiento observado y no observado. No generar un producto real ni confundir un ejercicio con E2E completo.

Quality distinto del autor revisa plan, diff, escenarios y evidencia, con facultad FAIL. Gate 2 ancla estado y hashes antes de la revisión proporcional al riesgo; comparar archivos comprometidos con ancla. Gate 3 registra comandos, salidas y límites. Mantener original de errores accesible; no inventar éxito. Documentar reversión mediante `git revert` del commit del incremento; no crear migraciones ni tocar datos. **E2E NO EJECUTADO** si no se acredita un flujo completo real.

## Medición

MET-001 registra inicio observado 2026-11-06T20:40:41.660Z, raíz `01a1b268-8005-7972-9954-92b25bac03cf`, corte inicial en `MET-INICIAL.json` y configuración de fase `MET-FASES.json`. Los cortes acumulados no se suman y la fase puede no identificar por sí sola la ventana de consumo: filtrar por eventos y documentar errores o atribuciones desconocidas. Registrar entrada, caché, salida, respuestas, delegaciones, duración, tamaño de informes, esperas, correcciones y recuperaciones en la medida observable; no inferir causas ni comparar causalmente tareas distintas ni facturación. Medición secundaria no bloquea implementación. No hay A/B.
