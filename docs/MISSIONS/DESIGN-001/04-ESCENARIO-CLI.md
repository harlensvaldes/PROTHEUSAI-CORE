# DESIGN-001 · Escenario 2: biblioteca CLI ficticia

Fecha: 2026-11-06. Participante: `codex /root/bootstrap`, Developer delegado. Análisis ficticio solicitado por TERRA; no es un Gate ni una aprobación.

## Resultado y decisión

Se puede continuar sin convocar al Director Creativo para la entrada planteada: biblioteca CLI con argumentos, validación, mensajes y salida de error, sin interfaz gráfica ni rediseño UX significativo. `AGENTS.md:67` indica que TERRA no convoca por defecto para una CLI sin impacto UX y debe justificar la decisión; `agents/creative_director.md:3` confirma que el rol no es obligatorio en ese caso. Esta evaluación no significa que toda CLI carezca de impacto UX. Una interacción compleja o una ambigüedad relevante justificaría reevaluar la necesidad (`agents/developer.md:5`).

La decisión de TERRA se comunica en la delegación de este escenario y se apoya en el alcance ficticio descrito; no he convocado al especialista. `docs/MISSIONS/DESIGN-001/01-PLAN.md:15` prevé este escenario como ejercicio acotado. El comportamiento observado es esta lectura y análisis de un Developer delegado, no una ejecución completa de producto.

## Mini plan implementable

1. Concretar el contrato de argumentos, entradas válidas, códigos de salida y mensajes antes de programar; mantener abiertos los detalles que el supuesto no define.
2. Implementar análisis y validación, separar la salida útil de los diagnósticos y evitar que entradas inválidas provoquen trazas no controladas. Mantener el alcance y los Gates aplicables (`agents/developer.md:3`).
3. Probar cada argumento y límite acordado, errores y códigos de salida con ejemplos reproducibles; entregar resultados y fuentes a Quality. Si aparecen decisiones de interacción relevantes, registrar la incertidumbre y pedir a TERRA que reevalúe la convocatoria.

**Criterio verificable propuesto:** para cada caso acordado de entrada válida e inválida, una prueba automatizada comprueba código de salida, canal y mensaje esperado; ningún caso inválido presenta una traza no controlada. Este criterio requiere acordar los casos y mensajes concretos antes de implementación.

## Riesgos, incertidumbres y límites

Los argumentos, semántica, público y mensajes no se han especificado; no se inventan como requisitos. Los mensajes son una interacción y podrían exigir dirección adicional si su complejidad lo justifica. No se construyó ni ejecutó una CLI, no se ejecutaron pruebas del producto y no se auditó un diff de producto. **E2E NO EJECUTADO.** Quality conserva su competencia independiente y este análisis no constituye dictamen.
