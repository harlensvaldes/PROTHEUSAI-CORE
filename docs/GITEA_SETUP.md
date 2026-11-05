# Configuración de Gitea Actions para esta plantilla

Esta plantilla incluye `.gitea/workflows/quality.yml`. No asume que tu Runner esté ya instalado ni que disponga de etiquetas estándar.

1. Crear repositorio privado en Gitea y establecer responsable.
2. Configurar un Gitea Actions Runner con acceso restringido al repositorio; verificar qué etiqueta soporta (`ubuntu-latest` es solo un ejemplo).
3. Activar Actions y revisar permisos de tokens/secretos.
4. Probar el pipeline en rama de pruebas: debe ejecutar `quality_cli.py validate` y unittest.
5. Añadir comandos de lint, typecheck, tests de backend/frontend, build y seguridad de **tu stack real**.
6. Configurar protección de la rama principal (revisión independiente, checks obligatorios, restricciones de push) en tu versión de Gitea.
7. Probar que un test fallido bloquea el merge según reglas configuradas.
8. Definir política de artefactos, retención de logs, acceso a secrets y permisos de despliegue.

**Limitación deliberada:** CI puede comprobar metadatos, pero no verificar que un agente nombrado realmente efectuó una revisión independiente. Conservar evidencia externa identificable y aprobación humana.
