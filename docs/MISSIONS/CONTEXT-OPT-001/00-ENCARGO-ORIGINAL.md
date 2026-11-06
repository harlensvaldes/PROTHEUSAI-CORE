# PROTHEUSAI-CORE · CONTEXT-OPT-001
## Optimización experimental del consumo de contexto y coordinación

TERRA, el Owner autoriza iniciar una intervención de optimización del consumo de contexto de PROTHEUSAI-CORE.

Tu esfuerzo de razonamiento se ha configurado en HIGH para esta investigación.

**Objetivo principal: reducir el consumo computacional y económico de nuestra empresa de agentes sin sacrificar autonomía, calidad técnica, independencia funcional de Quality ni fidelidad a las decisiones del Owner.**

Esta es una misión de análisis experimental, implementación y verificación. Tienes autorización para realizar tantas pruebas como resulten necesarias para obtener conclusiones fiables, siempre que cada prueba tenga un propósito medible.

No establezcas límites arbitrarios de iteraciones. Tampoco repitas experimentos que ya no aporten información.

## 1. Antecedentes

La auditoría de DELIVERY-001 registró:

- 43.966.778 tokens observados.
- 376 respuestas únicas.
- 43.288.448 tokens de entrada en caché.
- 36.115.395 tokens atribuidos a la sesión principal.
- Respuestas individuales superiores a 200.000 tokens al final de una sesión prolongada.

CONTEXT-001 demostró continuidad mediante checkpoint y recuperación de referencias, pero su primer experimento A/B no demostró ahorro:

- A convencional: 153.044 tokens, 5 respuestas.
- B selectivo: 172.210 tokens, 6 respuestas.
- B detectó información obsoleta que A pasó por alto.
- La renovación de la sesión principal no quedó verificada.

Importante: los aproximadamente 137.000 tokens en caché registrados en cada alternativa del experimento A/B son totales acumulados, NO tamaños acreditados de un prefijo fijo por respuesta.

**No partas de la premisa de que conocemos la causa exacta del consumo. Investígala.**

## 2. Hipótesis principales

Evalúa especialmente estas hipótesis, sin asumir que sean verdaderas:

**H1 — Contexto base excesivo**

TERRA y sus especialistas pueden recibir instrucciones, contratos y documentación que no necesitan mantener en todas sus respuestas.

**H2 — Demasiadas respuestas para operaciones sencillas**

Consultas repetidas de Git, esperas de agentes, revisiones de archivos y pequeñas acciones sucesivas pueden aumentar el número de vueltas del modelo.

**H3 — Acumulación de historial**

Las sesiones prolongadas pueden arrastrar conversaciones y resultados anteriores que ya podrían recuperarse desde fuentes persistentes.

**H4 — Recuperación demasiado costosa**

Un checkpoint puede añadir lecturas y llamadas, incluso cuando la tarea se resolvería más rápidamente mediante el procedimiento convencional.

**H5 — Delegación ineficiente**

Los subagentes pueden recibir demasiado contexto o devolver respuestas excesivamente extensas.

**H6 — Modelo y esfuerzo inadecuados para ciertas tareas**

El modelo más potente no necesariamente aporta valor adicional a todas las operaciones.

## 3. Medición inicial

Antes de modificar el funcionamiento de CORE:

1. Establece el HEAD y el estado Git de referencia.
2. Identifica sesiones y cortes MET-001 cuando existan.
3. Investiga el contexto efectivamente enviado al modelo.
4. Distingue, cuando los registros lo permitan:
   - Instrucciones permanentes del runner.
   - Reglas de CORE.
   - Contexto de misión.
   - Historial acumulado.
   - Resultados de herramientas.
   - Contexto propio de cada agente.
5. Identifica redundancias y relecturas demostrables.
6. Comprueba qué información puede medirse directamente y cuál solo puede estimarse.

**No afirmes que conoces el tamaño exacto del prompt base si el runner no lo expone.**

En ese caso, utiliza mediciones indirectas y declara sus límites.

Incluye el efecto de la caché. Los tokens cacheados no son gratuitos, pero tampoco tienen necesariamente el mismo precio que la entrada ordinaria.

## 4. Primera prioridad — Reducir el contexto permanente

Examina:

- AGENTS.md.
- Contratos operativos.
- Instrucciones de TERRA.
- Instrucciones de Architect, Developer y Quality.
- Documentos cargados automáticamente.
- Referencias duplicadas.
- Información histórica incluida sin necesidad.

Propón y prueba una estructura compacta:

**Instrucciones esenciales siempre disponibles + contratos específicos consultados bajo demanda.**

No elimines reglas necesarias para seguridad, calidad, autoridad del Owner o integridad del proyecto.

No modifiques instrucciones internas del runner ni mecanismos de permisos.

Mantén los textos originales como referencia durante los experimentos.

## 5. Segunda prioridad — Reducir vueltas del modelo

Investiga qué operaciones actualmente requieren varias respuestas y podrían resolverse mediante una única ejecución determinista.

Ejemplos:

- Estado Git y diff.
- Inventarios de archivos.
- Comparación de hashes.
- Validación de referencias.
- Resultados de pruebas.
- Estados de agentes.
- Preparación de información para Quality.

Reutiliza scripts y comandos existentes antes de crear otros.

Agrupa operaciones solamente cuando sea seguro hacerlo y no se pierda capacidad de diagnóstico.

**Menos respuestas no debe significar menos verificación.**

## 6. Experimentos A/B reproducibles

Diseña comparaciones representativas entre:

A. Funcionamiento vigente de CORE.

B. Funcionamiento optimizado.

Utiliza inicialmente entre tres y cinco tareas diferentes que representen actividades reales de nuestra empresa:

- Comprensión de requisitos.
- Análisis o diseño técnico.
- Implementación de un cambio pequeño.
- Revisión de Quality.
- Recuperación de decisiones y estado de misión.

Amplía o repite las pruebas si la variabilidad o los resultados contradictorios lo justifican.

Requisitos experimentales:

- Misma entrada y criterios de éxito.
- Estado inicial equivalente.
- Mismo modelo y esfuerzo al comparar estrategias de contexto.
- Ejecución secuencial cuando sea necesaria para evitar contaminación.
- Control o registro de los efectos de caché.
- Alternancia del orden de variantes cuando corresponda.
- Separación de resultados por sesión.
- Verificación de calidad sobre artefactos reales.
- Registro de errores y correcciones.

No mezcles cambios de modelo, esfuerzo de razonamiento y estrategia de contexto en una comparación que pretenda aislar una sola variable.

Si posteriormente evalúas Medium frente a High, hazlo como un experimento separado.

## 7. Métricas obligatorias

Utiliza MET-001 para recoger:

- Tokens de entrada.
- Tokens de entrada en caché.
- Tokens de entrada no contabilizados como caché.
- Tokens de salida.
- Respuestas.
- Sesiones y agentes identificables.
- Tiempo transcurrido.
- Número de llamadas a herramientas.
- Errores y correcciones.
- Calidad de los resultados.

Añade costes API equivalentes solo cuando existan tarifas verificables para los modelos y modalidades utilizadas.

No confundas costes hipotéticos con facturación real ni con la suscripción del Owner.

Cuando sea posible, calcula las diferencias absolutas y relativas entre A y B, sin ocultar la dispersión entre pruebas.

**Una mejora será válida si consigue resultados iguales o mejores con menos recursos, o si demuestra una ganancia de calidad que justifique su sobrecoste.**

## 8. Checkpoints y sesiones

Conserva el mecanismo ligero de CONTEXT-001 como herramienta de continuidad.

Evalúa:

- Si el checkpoint está actualizado.
- Cuándo merece consultarlo.
- Cuándo conviene acceder directamente al documento original.
- Si un agente sin historial puede continuar correctamente.
- Si el runner permite realmente renovar una sesión principal.
- Si hay beneficios frente a sus costes de recuperación.

No implementes un motor propio de sesiones.

No impongas MCP Memory.

Si existe un MCP Memory configurado, úsalo únicamente cuando corresponda y dentro de sus capacidades demostradas.

La elección y mantenimiento de proveedores MCP pertenecen al Owner o responsable del entorno.

## 9. Implementación

Después de los experimentos iniciales, incorpora a CORE únicamente las mejoras respaldadas por evidencia suficiente.

Prioriza:

1. Simplificación de instrucciones permanentes.
2. Recuperación de contratos bajo demanda.
3. Reducción de llamadas redundantes.
4. Reutilización de verificaciones deterministas.
5. Delegaciones compactas entre agentes.

Haz cambios pequeños y reversibles.

Verifica cada incremento antes de incorporar otro.

Quality debe comprobar que la optimización no elimina requisitos, decisiones ni controles técnicos relevantes.

**No conviertas esta misión en el desarrollo de un framework de memoria, un nuevo orquestador o una segunda CLI de gobernanza.**

## 10. Autonomía

El Owner autoriza realizar experimentos repetidos, ajustes técnicos, ejecución de pruebas y commits dentro de este alcance.

No solicites permiso para cada prueba.

Detente y consulta únicamente ante cambios materiales de alcance, riesgos relevantes u operaciones fuera del mandato.

Respeta los permisos nativos del runner.

No modifiques los expedientes históricos ni conviertas antiguos PENDING en PASS.

No inicies APP-005 ni DESIGN-001.

## 11. Criterios para detener los experimentos

No existe un número fijo de pruebas.

Continúa mientras:

- Los resultados sean contradictorios.
- La variabilidad impida una conclusión razonable.
- Exista una hipótesis concreta pendiente de comprobar.
- Una corrección técnica pueda cambiar materialmente el resultado.

Detén una línea experimental cuando los resultados sean suficientemente consistentes para decidir, cuando la siguiente prueba no aporte valor razonable o cuando la mejora no justifique su coste de implementación.

No optimices los resultados únicamente para hacer ganar a B.

Los resultados negativos también son evidencia válida.

## 12. Entregables

Presenta un informe final que incluya:

1. Diagnóstico del consumo y sus causas demostradas.
2. Tamaño del contexto inicial por rol, si es observable.
3. Experimentos realizados y metodología.
4. Comparaciones A/B con métricas.
5. Mejoras implementadas y descartadas.
6. Impacto medido en calidad, tiempo y tokens.
7. Coste hipotético, cuando pueda calcularse.
8. Limitaciones.
9. Dictamen de Quality.
10. Commits y estado Git.
11. Recomendaciones para el funcionamiento de APP-005.

Conserva los datos brutos necesarios para reproducir los cálculos.

Presenta las conclusiones de forma compacta. No necesitamos un documento por cada prueba.

No registres aceptación final del Owner sin su decisión expresa.

## Principio final

**PROTHEUSAI debe ser una empresa completa en competencias, selectiva en el uso de especialistas y eficiente en consumo de contexto.**

No buscamos reducir artificialmente los agentes, los tests o la calidad.

Buscamos eliminar procesamiento innecesario y utilizar el modelo adecuado, con el contexto adecuado, para la tarea adecuada.

Investiga, experimenta, corrige, vuelve a medir e implementa únicamente lo que realmente mejore CORE.

Procede con autonomía.