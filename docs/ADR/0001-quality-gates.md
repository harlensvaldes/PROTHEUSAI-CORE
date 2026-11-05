# ADR-0001 · Quality Gates independientes

- Estado: PROPUESTO — aprobar en primer proyecto real.
- Fecha: [DECIDIR]
- Contexto: proyectos con implementaciones por humanos y agentes IA necesitan trazabilidad y detección temprana de defectos.
- Decisión propuesta: Gate 1 para plan, Gate 2 para diff, Gate 3 para pruebas; el autor no puede certificar el mismo artefacto; propietario autoriza release.
- Alternativas: solo CI; solo revisión de pares; ausencia de Gates.
- Motivo: CI prueba lo programado; revisión independiente cuestiona las premisas; ambas son complementarias.
- Consecuencias: más coste de preparación, menos defectos introducidos inadvertidamente, necesidad real de segundo revisor.
- Verificación: primera misión completa y auditoría del mecanismo de invocación.
- Aprobador: [PENDIENTE]
