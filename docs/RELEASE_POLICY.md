# Release / Deploy Policy

1. Gate 1 aprobado para el diseño implementado.
2. Gate 2 aprobado para el diff/commit/artefacto que realmente se va a desplegar.
3. Gate 3 con evidencia ejecutada sobre esa revisión, sin BLOCKERS abiertos.
4. Plan de despliegue aprobado: entorno, ventana, migraciones, backups, feature flags y rollback.
5. Autorización expresa del Owner/Release Manager definido en Charter.
6. Verificación post-deploy: health, logs, métricas, funciones críticas y anomalías.
7. Registrar versión, artefacto/hash, operador, fecha, resultado y reversión si ocurrió.

**Importante:** los PASS de Gates no implican autorización implícita de deploy. Un informe de agente no equivale a prueba ejecutada.
