# Portabilidad Cline / DeepSeek: auditoría y propuesta

Estado: propuesta pendiente de Gate 1 independiente; no autoriza implementación ni acredita compatibilidad de extremo a extremo. Alcance: CORE interno, sin piloto de producto.

## Evidencia y límites

- `README.md` exige proporcionar `AGENTS.md` al ejecutor y verificar la disponibilidad de instrucciones y revisión independiente. `docs/CONTEXT-001.md` distingue checkpoints de capacidades nativas de sesión y delegación. Los contratos de `agents/` no instalan agentes.
- `scripts/quality_cli.py` expone `validate`, `status`, `can-implement`, `can-close` y `hash`: son verificaciones formales, no un dictamen técnico ni una autorización. `scripts/new_mission.py` crea registros; `scripts/delivery001.py` prepara/verifica entregas; `scripts/bootstrap001.py` crea proyectos desde una allowlist de Git. No es necesario duplicar estas operaciones en un orquestador nuevo.
- `scripts/met001.py` procesa eventos y estructura de sesión específicos de Codex. No se debe interpretar su resultado como métricas de Cline ni asumir equivalencia de formatos. Mantenerlo como adaptador específico existente hasta disponer de un formato y necesidad comprobados.
- La documentación de Cline describe herramientas, sesiones y equipos de su SDK, pero esto no acredita que estén habilitados en una instalación concreta: https://docs.cline.bot/cline-sdk/sessions. DeepSeek documenta `deepseek-flash` y su API compatible: https://api-docs.deepseek.com/quick_start/agent_integrations/. La combinación local Cline/modelo, carga efectiva de instrucciones y delegación no se ha ejecutado ni verificado.

## Propuesta para revisión independiente

1. Comprobar en la instalación real si Cline carga `AGENTS.md` y si la configuración permite herramientas y revisión por autor diferente. Solo si no carga las instrucciones, añadir una referencia mínima soportada por la versión instalada, con `AGENTS.md` como fuente única. No duplicar reglas.
2. Documentar un procedimiento breve y neutral de preparación: selección del proveedor/modelo en el runner, entrega verificable de instrucciones, capacidades reales de delegación y fallback a revisor humano. No guardar credenciales ni fijar modelo o proveedor en CORE.
3. Mantener CLI y scripts actuales para operaciones deterministas; no introducir capa de orquestación, nuevo Gate, infraestructura ni adaptador de métricas sin evidencia de necesidad.
4. Verificar en ambos entornos disponibles: carga efectiva de instrucciones, comandos de validación y pruebas, límites de permisos y acceso independiente a los artefactos. Registrar versiones, comandos, salidas y limitaciones; no sustituir Gate 2/3 por el resultado de la CLI. No ejecutar piloto de producto.

Gate 1 debe revisar el alcance, archivos propuestos, riesgos, reversión y criterios antes de implementar. No hay aquí dictamen independiente ni aceptación del Owner.
