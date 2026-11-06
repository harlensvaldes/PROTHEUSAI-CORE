# DESIGN-001 · Lectura Developer del escenario UI

Fecha: 2026-11-06. Lector: `codex /root/bootstrap`, Developer delegado, distinto del autor creativo declarado en la delegación. Lectura de `agents/developer.md` y `03-ESCENARIO-UI.md`; identidad y aislamiento no certificados. No se implementa producto ni se emite Gate.

## Resultado

La propuesta permite preparar un plan de implementación y pruebas observables, pero no iniciar un producto como especificación aprobada. Solo están confirmados contexto móvil, reservas y tres adjetivos; ninguna solución visual o funcional consta aprobada (`03-ESCENARIO-UI.md:9-11`). `agents/developer.md:3,5` exige plan y Gate 1 aplicables, implementar la dirección acordada y consultar ambigüedades relevantes. La propuesta es una hipótesis para revisión, no una autorización.

## Acciones concretas tras decisiones y Gates aplicables

1. Modelar el flujo propuesto de selección de servicio, fecha y hora, revisión editable y resultado (`03-ESCENARIO-UI.md:15-18`) con datos y contratos acordados; conservar elecciones válidas y mostrar estados vacíos, carga, fallo y resultado incierto.
2. Construir componentes accesibles de selección, campos etiquetados, botones y mensajes de estado; usar estructura adaptable de una columna en móvil y los tokens visuales solo cuando se hayan decidido.
3. Integrar confirmación únicamente tras una respuesta positiva y una estrategia acordada de recuperación ante respuesta incierta; no inferir creación ni provocar solicitudes duplicadas. Presentar cambios y evidencia a Quality independiente.

## Pruebas UI propuestas, todavía no ejecutadas

- A 320 px y texto al 200 %, comprobar controles y contenido disponibles sin solapamiento ni desplazamiento horizontal de página. Recorrer el flujo con teclado, foco visible, nombres accesibles y errores asociados y anunciados (`03-ESCENARIO-UI.md:30-31`).
- Medir contraste sobre colores efectivamente seleccionados: 4,5:1 texto normal, 3:1 texto grande y controles/foco pertinentes; comprobar objetivos táctiles de 44 × 44 px CSS cuando sea viable y documentar alternativas (`03-ESCENARIO-UI.md:32-33`).
- Con datos de prueba aprobados recorrer selección, edición, éxito, ausencia de disponibilidad, fallo y respuesta incierta; comprobar que no se muestra éxito antes de la respuesta positiva (`03-ESCENARIO-UI.md:34`).

## Bloqueos, riesgos y siguiente acción

Faltan alcance autorizado, público, marca y selección visual; reglas de reserva, disponibilidad, precio y datos de contacto son hipótesis (`03-ESCENARIO-UI.md:11`). Architect debe resolver factibilidad y contrato de recuperación de respuesta incierta; Discovery y Owner deben aclarar alcance y decisiones visuales importantes. No asumir pago, cuenta, ubicación, duración, cancelación ni tiempo real. La medición de accesibilidad requiere una implementación y valores reales; los criterios aún son propuestos, no resultados.

**Siguiente acción:** TERRA contrasta las hipótesis con Discovery y Architect y eleva al Owner las decisiones correspondientes; consultar al Director Creativo las ambigüedades visuales relevantes. No se han ejecutado pruebas de producto. **E2E NO EJECUTADO.**
