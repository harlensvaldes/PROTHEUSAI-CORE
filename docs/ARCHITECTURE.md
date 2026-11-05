# Architecture Baseline · [NOMBRE DEL PROYECTO]

**Estado:** DRAFT · **ADR relevantes:** [DECIDIR]

## 1. Contexto del sistema
Usuarios, integraciones, límites de confianza, redes y entornos: [DECIDIR]

## 2. Stack (decisión, no valor por defecto)
| Capa | Tecnología y versión | Motivo | Riesgos |
|---|---|---|---|
| Cliente | [DECIDIR] | | |
| Backend | [DECIDIR] | | |
| Persistencia | [DECIDIR] | | |
| Cola/async | [DECIDIR] | | |
| Despliegue | [DECIDIR] | | |

## 3. Módulos y fronteras
| Dominio | Propietario de estado/datos | API/eventos | No debe hacer |
|---|---|---|---|
| [DECIDIR] | [DECIDIR] | [DECIDIR] | [DECIDIR] |

## 4. Fuentes de verdad e identidad
IDs, concurrencia, versiones, transacciones, conflictos, política de reintentos, idempotencia: [DECIDIR]

## 5. Contratos externos
Esquemas, validación, compatibilidad, errores, límites, timeouts: [DECIDIR]

## 6. Autorización y datos sensibles
Roles, permisos, límites de recursos, secrets, retención, auditoría: [DECIDIR]

## 7. Observabilidad
Logs estructurados, correlación, métricas, alertas, diagnósticos: [DECIDIR]

## 8. Recuperación
Backups, restauración probada, rollbacks, migraciones, disaster recovery: [DECIDIR]

## 9. Decisiones pendientes
- [DECIDIR] -> abrir ADR, revisor independiente y propietario según riesgo.
