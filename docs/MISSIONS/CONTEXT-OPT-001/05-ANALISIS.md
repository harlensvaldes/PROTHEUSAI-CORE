# CONTEXT-OPT-001 · Análisis determinista de registros disponibles

## Datos y procedimiento

Se utiliza el corte histórico `docs/MISSIONS/CONTEXT-001/05-MET-CORTE-2.json`, con 44 respuestas de cuatro hilos y dos errores de lectura. De las 44 referencias se recuperaron y comprobaron los 44 eventos referenciados; 24 pertenecen a la raíz `01a1b237-0edf-7182-b1cd-c120f4816af0`. El corte es parcial: recuperar las referencias no prueba que no falten respuestas. El script `analisis_eventos.py` verifica identificadores, fecha e hilo, ordena por fecha y posición, y genera `05-CONTEXT-SERIE.csv`, `05-CONTEXT-RESULTADOS.json` y `05-CONTEXT-GRAFICA.svg`; no exporta mensajes. Ejecución `python docs/MISSIONS/CONTEXT-OPT-001/analisis_eventos.py`: salida 0. Las entradas y caché son tokens por respuesta; la caché está incluida en la entrada.

## Evolución observada

- Entrada de la respuesta 1: 21.205; respuesta 24: 66.917; diferencia 45.712. Los 23 incrementos consecutivos son positivos. Suma: 1.218.852 de entrada y 1.146.496 de caché (94,06 % de la entrada).
- El ajuste lineal descriptivo con índice 1–24 da pendiente aproximada de 2.106 tokens por respuesta, intercepto en índice 0 de 24.457 y R² 0,851. El intercepto es una extrapolación matemática y no mide el prompt base; la pendiente no aísla causalmente el historial.
- Incrementos mayores en respuestas 7 (+9.187), 9 (+8.319), 10 (+6.550), 4 (+4.434) y 8 (+4.414). Son discontinuidades observadas, sin atribución causal validada. El incremento menor fue +53 en la respuesta 6.
- La caché por respuesta pasó de 7.168 a 66.304, pero cayó en los índices 4 y 6; esas caídas no indican por sí mismas pérdida de contexto ni compactación. La entrada no cacheada por respuesta tuvo mínimo 146, mediana 585,5 y máximo 15.273.
- No hay reducciones de entrada total entre respuestas observadas ni eventos cuyo tipo o subtipo contenga `compact` en el tramo del JSONL examinado. Esto no demuestra ausencia de compactación: puede haber formatos no detectados, eventos fuera del corte o respuestas faltantes.

**Hipótesis:** el crecimiento repetido de entrada y los saltos sugieren que reducir el volumen retenido y el número de respuestas podría ser una oportunidad, pero las fuentes no separan instrucciones, historial y resultados de herramientas. El alto porcentaje de caché no permite estimar ahorro monetario sin tarifas apropiadas. La muestra no permite extrapolación a DELIVERY-001, cuyo JSONL el Owner declara no disponible.

## Entrada inicial por función observable

Las siguientes cifras son la **primera respuesta observada en el corte**, no una medición controlada del prompt base ni prueba de ser el primer evento de cada hilo. Incluyen instrucciones, tarea, runner, herramientas y cualquier contexto heredado; las condiciones no fueron iguales.

| Hilo identificado en metadatos | Entrada | Caché incluida |
|---|---:|---:|
| Raíz CONTEXT-001 | 21.205 | 7.168 |
| `/root/quality` | 21.080 | 13.184 |
| `/root/continuidad` | 20.843 | 17.664 |
| `/root/experimento_a` | 20.882 | 20.480 |
| `/root/experimento_b` | 20.861 | 13.184 |
| `/root/verificador` | 20.835 | 20.480 |

Existe además un hilo sin función identificada con 14.800 tokens de entrada; no se le asigna un rol por inferencia. No hay una medición identificable y comparable de Architect o Developer. Las identidades operativas no acreditan independencia ni aislamiento.

## Oportunidad y viabilidad de prueba

La oportunidad prioritaria a investigar es la **acumulación de entrada entre respuestas**, seguida de reducir vueltas que no aporten evidencia. Es una prioridad experimental, no un ahorro demostrado; la observación no justifica editar AGENTS.md ni debilitar la revisión. Conservar A y la rúbrica prerregistrada.

El diseño prerregistrado mínimo tiene tres tareas × dos variantes × dos repeticiones = 12 ejecuciones. Usando solo como orden de magnitud los resultados anteriores A = 153.044 y B = 172.210 por ejecución, seis de cada una supondrían aproximadamente **1.951.524 tokens**, antes de coordinación y revisión. Es una estimación incierta: las otras tareas podrían costar distinto, la caché y el número de respuestas varían, y no es facturación. El corte de inicio de esta continuación deja como máximo 661.445 tokens observados; el saldo real puede ser menor. La comparación mínima previamente acordada no cabe razonablemente. No se propone relajar el criterio, ampliar el presupuesto ni ejecutar un A/B de utilidad insuficiente.

## Verificaciones y límites

`python -m py_compile docs/MISSIONS/CONTEXT-OPT-001/analisis_eventos.py`: salida 0. `git diff --check`: salida 0 para cambios rastreados; no inspecciona archivos sin seguimiento. El gráfico es descriptivo y no certifica causalidad ni cobertura completa. No se invocaron agentes ni se cambiaron las instrucciones operativas. Quality independiente y Gate 1 permanecen pendientes. **E2E NO EJECUTADO**; no hay aceptación final del Owner.
