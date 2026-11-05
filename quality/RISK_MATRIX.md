# Matriz de riesgos para decidir profundidad de Quality

| Riesgo | Ejemplos | Gate 1 | Gate 2 | Gate 3 |
|---|---|---|---|---|
| LOW | textos, iconos sin lógica, CSS aislado | revisión breve documentada | diff + visual | lint/build + smoke relevante |
| MEDIUM | componentes, navegación sin persistencia, formularios | contratos y riesgos | diff + UX/a11y | pruebas focalizadas + regresión |
| HIGH | guardado, cambios de BD, concurrencia, auth, colas | contrato formal + revisor independiente | diff y casos adversos | integración, fallos, rollback |
| CRITICAL | cálculo resistente, vida/salud, datos irreversibles | ingeniería del dominio, normativa y expertos | review especializado independiente | validación externa, trazabilidad y release separado |

**Política local:** incluso LOW conserva independencia de quien aprobó el trabajo. La longitud del informe es proporcional al riesgo.

Riesgo = impacto x probabilidad razonada + detectabilidad/recuperación. Registrar hipótesis; no fingir un número universal.
