# DELIVERY-001 · Decisión del Owner sobre controles de entrega

Fecha: 2026-11-06. Fuente: respuesta directa del Owner a la decisión solicitada en esta conversación; identidad nominal no verificada.

El Owner acepta controles explícitos con reconocimiento de sus límites y exige: allowlist; revisión verificable por archivo con procedencia y justificación; exclusión por defecto de secretos, archivos `.env`, credenciales, bases operativas, logs, cachés y temporales; escaneos conservadores de nombres, contenido y patrones; manifiesto con hashes y resultados; y declaración de que no se garantiza detectar todos los secretos o datos privados. Cualquier secreto confirmado, procedencia desconocida o hallazgo de seguridad sin resolver bloquea su inclusión y, si es necesario para ejecutar el producto, bloquea la entrega. No crear Gate nuevo ni exigir garantías absolutas imposibles. Aplicar controles proporcionales al riesgo.

Esta decisión modifica el contrato del plan anterior; exige reabrir Gate 1 según `AGENTS.md` y `docs/QUALITY_POLICY.md`. No elimina los FAIL históricos ni autoriza declarar la entrega terminada.
