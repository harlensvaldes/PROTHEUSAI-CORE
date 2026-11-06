# CONTEXT-OPT-001 · Protocolo previo a los experimentos

## Encargo resumido

Reducir el consumo de contexto y coordinación sin perder autonomía, decisiones del Owner, seguridad ni revisión independiente. Priorizar datos históricos, luego mediciones de arranque y comparaciones controladas; implementar solo mejoras respaldadas por evidencia. No construir gestores de sesiones ni modificar el runner. Conservar CONTEXT-001 y sus reservas. No iniciar APP-005 ni DESIGN-001. El encargo íntegro está en `00-ENCARGO-ORIGINAL.md`; este resumen no sustituye sus requisitos.

El Owner añadió: analizar los eventos históricos antes de A/B; estimar el arranque por rol; congelar A; fijar criterios y al menos dos repeticiones por celda para tareas cortas; presupuesto total de **2.000.000 tokens observados** incluida la investigación. Parar antes de una prueba si su coste razonablemente esperado excede el saldo; si ya se alcanza el límite, detener y presentar resultado parcial. MET-001 puede subcontar, por lo que un corte parcial no garantiza permanecer bajo el límite. No equiparar tokens con coste monetario.

## Línea base y restricciones

HEAD `722053b381ad1dbe88c082ddf4109883e3d9ff9d`; A incluye los cambios preexistentes sin commit. `BASELINE-A.zip` conserva sus contenidos, `BASELINE-A.json` sus hashes y el del ZIP; aplicar sobre ese HEAD en una copia aislada tras verificar todos los hashes. El commit por sí solo no reproduce A. No registrar un tag que sugiera lo contrario ni incorporar cambios preexistentes a un commit sin aprobación de su contenido. El ZIP no es sustituto de una copia de seguridad externa.

## Análisis previo

Para DELIVERY-001, extraer de los eventos originales respuestas únicas del hilo principal con el corte histórico; ordenar por tiempo y posición estable. Guardar solo índice, timestamp, identificador de respuesta, entrada, entrada en caché y salida, con procedencia, sin mensajes. Graficar entrada e incluir primera respuesta, cambios de tendencia y posible compactación. Un ajuste lineal y sus residuales son descriptivos: la ordenada incluye instrucciones, tarea y otras cargas iniciales; la pendiente también incluye herramientas, cambios de tarea y compactación. Ni una ni otra identifica causalmente H1 o H3. Identificar discontinuidades y cobertura antes de atribuir causas; no extrapolar desde la media de todos los agentes al hilo principal.

La primera respuesta a «responde OK» en hilos nuevos por rol mide entrada inicial **total observada**, no el tamaño puro de instrucciones; incluye runner, tarea, contrato y metadatos. Registrar modelo, esfuerzo, instrucciones efectivamente inyectadas, caché y configuraciones de lanzamiento. No suponer que `fork_turns=none` elimina instrucciones permanentes. Igualar condiciones y documentar qué rol se ejecuta realmente.

## Prerregistro A/B

No iniciar hasta disponer de Gate 1 independiente aplicable, un procedimiento de medición operable, saldo suficiente y una A recuperable. Tres tareas cortas con mismo input y criterios en ambas variantes: (1) recuperar decisiones y estado con referencia a fuentes; (2) analizar un cambio técnico acotado con riesgos y pruebas; (3) revisar un diff fijado con defectos conocidos. Cada celda se repite al menos dos veces en hilos nuevos; orden AB y BA alternado, ejecución secuencial, modelo y esfuerzo iguales. Fijar por hash las entradas, el diff y la clave de defectos antes de ejecutar. Si se incluye implementación, usar copias aisladas equivalentes y revisar artefactos reales. Anotar caché, lecturas, llamadas, errores, correcciones y duración; MET-001 por sesión con cortes explícitos.

Rúbrica previa por respuesta: decisiones y estado correctos; referencias verificables; detección de todos los defectos críticos predefinidos; identificación de límites y autorización; ausencia de invenciones. Cualquier omisión crítica, decisión inventada o pérdida de control de seguridad implica fallo de calidad, independientemente de tokens. Quality independiente coteja fuentes y artefactos. La mejora por eficiencia requiere que **todas** las repeticiones B cumplan la rúbrica y que la suma de tokens totales de B sea al menos un 10 % menor que A para cada tarea, sin empeorar la detección de defectos ni omitir una decisión relevante. Si no se cumple para cada tarea, no afirmar mejora general. Una ganancia de calidad con sobrecoste requiere defectos adicionales verificables, coste informado y decisión del Owner sobre la compensación. Dos repeticiones son mínimo, no prueba estadística; informar cada resultado y dispersión, ampliar solo si el presupuesto lo permite.

## Gates y verificación

Este protocolo es una propuesta del autor, no dictamen. Quality distinto del autor debe revisar el plan y su versión antes de implementar cambios sujetos a Gate 1, y después revisar diff y resultados conforme a `docs/QUALITY_POLICY.md`. No registrar aceptación del Owner ni convertir dictámenes históricos. E2E no ejecutado debe declararse expresamente. No emprender pruebas que no puedan medirse o verificarse con las capacidades reales.
