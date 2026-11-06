# DOC-001 · Plan

Estado: DRAFT, Gate 1 PENDING. Autor y coordinador declarado: TERRA. Baseline CORE `24d95892233d17cb08850f0656582cefe537898c`; árbol limpio, dos commits locales adelantados. Riesgo MEDIUM propuesto: cambio documental reversible sin motor, datos ni permisos, con impacto transversal en la calidad y veracidad de entregas futuras. La matriz contiene ejemplos, no una obligación automática de HIGH; revisar detectabilidad y recuperación.

## Objetivo y alcance

Incorporar un contrato portable y una plantilla adaptable para que cada proyecto de software mantenga un README propio, profesional y fiel al producto y a la evidencia. Se revisa en los Gates existentes sin añadir agentes, Gates, ejecutores ni dependencias. No modificar DISCOVERY-001, APP-003, APP-004, lógica o permisos de agentes, CI ni motor. No crear documentos comerciales o capturas artificiales.

## Cambios previstos

- Crear `docs/README_CONTRACT.md` como única fuente del contrato: README propio durante desarrollo y previo a entrega; estructura recomendada adaptable; afirmaciones basadas en producto y evidencias; resultados con comando, fecha/hora, versión, aprobados/fallidos/omitidos, estado y referencia cuando disponibles; cobertura solo medida; resultados anteriores identificados como históricos, pruebas ausentes Not run. Badges solo verificables y preferentemente CI real si existe, sin suponer proveedor; capturas reales de UI cuando disponibles y autorizadas, sin secretos/datos personales, rutas relativas; licencia únicamente declarada. Responsabilidades TERRA, Developer y Quality, sin agentes nuevos. Documentación extendida solo si solicitada o justificada. Resumen determinista preferible si puede obtenerse de resultados existentes, sin nuevo sistema.
- Crear `docs/templates/README_PRODUCT.md` como guía mínima adaptable, sin datos ficticios ni secciones vacías obligatorias, que remita al contrato y exponga marcadores como no verificados; el README del producto nunca debe copiar el del CORE.
- En `START_HERE.md` añadir referencia al contrato y plantilla para uso en proyectos nuevos; en `prompts/02_IMPLEMENT.md` instruir mantenimiento y referencia; en `prompts/03_GATE2_DIFF_REVIEW.md` y `prompts/04_GATE3_ACCEPTANCE.md` añadir contraste de afirmaciones con código y pruebas en revisión y entrega. Reutilizar el proceso existente, no duplicar reglas exhaustivas en cada punto de entrada. No asumir que ejecutores cargan instrucciones sin haberlas recibido.

## Verificación y límites

Simular con ejemplos pequeños y resultados observados A web con captura real disponible, B CLI sin capturas, C pruebas no ejecutadas, D pasadas/fallidas/omitidas, E cobertura desconocida, F licencia no declarada y G cambios posteriores a pruebas. Indicar qué es fixture hipotético y no atribuirlo a un producto real; evaluar trazabilidad y fechas/horas y commit exacto. Verificar ausencia de PASS/cobertura/licencia inventados y captura no obligatoria CLI. Validar que se distinguen CI, Quality, E2E y aceptación. Ejecutar `python -m unittest discover -s tests -q`, `python scripts/quality_cli.py validate`, `git diff --check`; registrar entorno, fecha, resultado y omisiones. Una revisión textual o simulación no demuestra ejecución automática ni uso real multiplataforma. E2E NO EJECUTADO salvo prueba real.

## Gates y riesgos

Gate 1 independiente sobre hash exacto del plan y fuentes, con decisión de aplicabilidad del Charter; la interpretación anterior de DISCOVERY-001 se limitó expresamente a esa misión. El Charter CORE permanece DRAFT; no fingir su cumplimiento. MEDIUM v3 exige I1/G0 Gates 1 y 2, y I1/G1 evidencia de ejecución Gate 3. Si la política lo permite, emitir dictamen real y mantener aceptación Owner pendiente; la CLI no autentica identidad ni aislamiento. Gate 2 requiere ancla y comparación post-commit; Gate 3 requiere evidencia realmente ejecutada. Reversión futura mediante parche inverso revisado, sin borrar historia ni trabajo preexistente. Riesgos: instrucciones no cargadas, documentación afirmada sin evidencia, resultados históricos ambiguos y exposición de datos en capturas.
