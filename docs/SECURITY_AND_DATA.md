# Seguridad, privacidad e integridad de datos

## Clasificación y amenaza
Datos personales, confidenciales, normativos o empresariales: [DECIDIR].
Actores, fronteras de confianza, privilegios, superficie expuesta: [DECIDIR].

## Controles mínimos a diseñar
- Autenticación y autorización acordes al despliegue; denegar por defecto.
- Validación de entradas, protección contra inyección, CSRF/XSS según arquitectura.
- Secretos fuera del repositorio; rotación y control de acceso.
- Datos personales: minimización, retención, acceso y eliminación documentados.
- Concurrencia: idempotencia, revisiones, conflictos y no pérdida de escrituras.
- Logs auditables sin volcar contraseñas/tokens/datos sensibles.
- Backups y restauración comprobada antes de migraciones destructivas.
- Escaneo de dependencias y plan de respuesta a vulnerabilidades.

## Gate adicional en sistemas críticos
La revisión de código no sustituye auditorías de seguridad dedicadas, validación profesional sectorial ni cumplimiento normativo.
