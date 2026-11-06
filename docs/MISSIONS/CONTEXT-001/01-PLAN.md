# CONTEXT-001 + DET-001 · Plan

Baseline: `722053b381ad1dbe88c082ddf4109883e3d9ff9d`, árbol limpio al inicio. Owner autorizó mejora interna; TERRA actúa como Orchestrator y Developer. Quality revisa de forma independiente. Alcance: continuidad y recuperación selectiva de misiones CORE; sin productos, despliegue, servidor MCP, Gates nuevos ni gestor de sesiones.

## Diseño y contratos

Crear guía y plantilla Markdown de checkpoint local: misión y objetivo, estado, decisiones aplicables con fuentes, completado/pendiente, agentes y operaciones activas con identificadores y estado, Git, referencias/versiones/hashes, bloqueos y próxima acción. Es índice operativo editable, no fuente de verdad; consultar originales si hay discrepancia. Antes de transferir, comprobar trabajos reales y registrar los que sigan activos; no afirmar que puedan adjuntarse desde otra sesión. Recuperar checkpoint primero, después instrucciones obligatorias y fuentes necesarias, excluyendo históricos ajenos. Quality conserva acceso directo a originales. Incorporar referencia breve en AGENTS.md para que el procedimiento se descubra. No resumir elimina contexto: la compactación y sesión nueva dependen del runner.

Usar herramientas existentes `git status --short`, `git rev-parse`, `quality_cli.py` y `met001.py`; no crear automatización nueva si no existe necesidad repetida demostrada. Evaluar continuidad con un agente nuevo sin historial, que lea únicamente el checkpoint y fuentes necesarias, y compare decisiones, referencias, pendientes y operaciones. Esto prueba recuperación por un subagente, no renovación de sesión principal. Diseñar comparación reproducible y reportar solo medición parcial si no hay A/B equivalentes.

## Riesgos y validación

Estado obsoleto o referencias incompletas pueden inducir errores: cotejar Git, fuentes y trabajos activos al transferir, anotar incertidumbre y conflictos; no confiar en el checkpoint como autorización. Evitar secretos y datos sensibles. Probar recuperación independiente, referencias inexistentes o cambiadas y trabajo activo; verificar diff y comandos, MET-001 y situación Git. No afirmar ahorro o coste sin datos comparables. Quality revisará plan, diff y evidencia con acceso original. E2E se declara no ejecutado si no existe prueba de sesión real nueva.

Archivos previstos: `AGENTS.md`, `docs/CONTEXT-001.md`, `docs/templates/CHECKPOINT.md`, `docs/MISSIONS/CONTEXT-001/` para plan, estado y evidencias. Reversión: parche inverso revisado de archivos propios, preservando trabajo posterior y evidencias; no reset destructivo. Alternativas descartadas: base de datos/embeddings, MCP propio, administración paralela del runner y duplicar scripts existentes: complejidad sin necesidad demostrada.
