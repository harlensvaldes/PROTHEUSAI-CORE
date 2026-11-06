# CONTEXT-OPT-001 · Diagnóstico inicial y límites

## Evidencia histórica disponible

`docs/MISSIONS/DELIVERY-001/METRICAS-03.md` informa 376 respuestas agregadas, 43.859.230 tokens de entrada, incluidos 43.288.448 en caché, y 107.548 de salida. La media agregada de caché es aproximadamente 115.129 tokens por respuesta; no es una medición del prefijo fijo ni de la sesión principal. El informe no ofrece la secuencia por respuesta. `docs/MISSIONS/CONTEXT-001/08-RESULTADO-AB.md` recoge un único contraste: A 153.044 y B 172.210 tokens, 5 y 6 respuestas; B detectó obsolescencia que A pasó por alto. No demuestra ahorro ni permite atribuir diferencias a una causa aislada.

Se intentó reproducir el corte DELIVERY-001 con `python scripts/met001.py --sessions "$env:USERPROFILE/.codex/sessions" --session-id 01a1b13a-3b02-7052-ad60-01e25c0a3fad --cutoff 2026-11-06T15:09:01Z --output "$env:TEMP/context-opt-delivery-probe"`: salida 0, pero estado `partial`, 118 archivos inspeccionados, dos errores de lectura y cero respuestas de la raíz. El archivo raíz histórico referido en `docs/MISSIONS/DELIVERY-001/LECTURA-ANCLA-04.md` no aparece en `sessions/2026/11/06` en este entorno. Por tanto no se dispone aquí de puntos por respuesta, gráfico, pendiente ni separación H1/H3. Salida 0 no significa medición completa. Los errores no prueban por sí mismos la causa de la ausencia.

## Estado de la investigación

Los tamaños por rol, las causas específicas, el efecto de la compactación, los tiempos, costes y ahorro de una optimización siguen sin determinar. `AGENTS.md` vigente contiene 6.729 caracteres en la versión HEAD, no tokens; esto no establece cuánto contexto consume una respuesta ni cuánto se carga automáticamente. Los contratos de Architect y Developer son breves; Quality incorpora obligaciones de lectura y revisión, pero el contexto efectivamente inyectado no se conoce mediante estos documentos. Los tokens cacheados se incluyen en entrada; su precio puede diferir del de entrada no cacheada. No hay coste real ni tarifas verificadas para esta medición.

El árbol previo incluía cambios en AGENTS.md y archivos de CONTEXT-001 sin seguimiento. Se conservaron en `BASELINE-A.zip`, con manifiesto de hashes; no se alteraron expedientes históricos. El servidor de grafo no respondió a la consulta de proyectos dentro de ocho segundos; se usó lectura de documentos y archivos de configuración como alternativa. La revisión independiente, los experimentos por rol y A/B, y la implementación de optimizaciones permanecen pendientes; este documento no es un dictamen Quality.

Recomendación provisional para APP-005: conservar el mecanismo de checkpoint como índice verificado contra originales, sin afirmar que ahorra tokens; no anticipar cambios en gobernanza ni inicio del producto. Recuperar los eventos originales de DELIVERY-001 y habilitar revisión independiente antes de decidir modificaciones operativas.

## Alternativa con datos existentes

El Owner indica que no dispone del JSONL histórico de DELIVERY-001. No se reconstruye su serie a partir de los totales. Como evidencia de otra misión, se contrastaron las 44 referencias de `docs/MISSIONS/CONTEXT-001/05-MET-CORTE-2.json` con los eventos originales accesibles: las 44 se pudieron leer, 24 corresponden al hilo raíz. En orden temporal, la entrada observada de la primera respuesta raíz fue 21.205 tokens y la de la última 66.917; diferencia 45.712 tokens entre esos dos puntos. Este contraste no demuestra una tendencia lineal ni identifica la causa del crecimiento y no permite extrapolar a DELIVERY-001. El corte MET histórico señala dos errores de lectura, por lo que la cobertura total no está acreditada.

En esta misión, un corte MET-001 exclusivo a las 19:33:25.346 UTC del 2026-11-06 observó 1.140.380 tokens totales, incluidos 1.057.664 tokens de entrada en caché; estado parcial por dos errores de lectura. La sesión continuó después y el saldo restante es como máximo 859.620 tokens de los 2.000.000 autorizados, sin garantía de exhaustividad. Antes de cualquier experimento tomar un corte nuevo y estimar su coste.
