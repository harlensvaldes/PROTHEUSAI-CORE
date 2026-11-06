# DESIGN-001 · Escenario ficticio 1: reserva móvil

**Naturaleza:** propuesta creativa para el ejercicio, no producto implementado ni decisión aprobada. Entrada facilitada por TERRA: aplicación comercial de reservas de servicios para usuarios móviles; intención «moderna, elegante y sencilla». No se proporcionaron marca, tipografía, colores ni funcionalidades aprobadas. Fuente del mandato: `agents/creative_director.md` (SHA-256 `94e6299e488529e9f9365206989548803d9d4c42e7f4a28fc5b1b01436cbeeee`).

## Intención y decisiones

La experiencia debe ayudar a encontrar una opción y entender qué se solicita antes de confirmar. «Sencilla» se traduce en una decisión principal por etapa; «elegante», en jerarquía y espacio consistente; «moderna», en controles claros y adaptativos, sin exigir efectos decorativos.

**Confirmado para el ejercicio:** contexto móvil, reservas de servicios y los tres adjetivos anteriores. No consta aprobación de ninguna solución visual o funcional.

**Hipótesis para contrastar:** existen servicios, horarios disponibles y datos de contacto mínimos; puede mostrarse el precio antes de confirmar; la reserva necesita confirmación explícita. No asumir pago, cuenta, ubicación, duración, cancelación o disponibilidad en tiempo real como funcionalidades autorizadas. Discovery debe validar público, necesidades, condiciones y datos; Architect evaluará factibilidad. El Owner decide dirección visual y alcance del producto.

## Flujo propuesto

1. **Elegir servicio:** lista de servicios con nombre, descripción breve y, si se conoce, duración y precio; una acción identificable para seleccionar. Sin resultados: explicar que no hay opciones disponibles y ofrecer volver o reintentar cuando corresponda.
2. **Elegir fecha y hora:** presentar fecha y horarios disponibles con etiquetas completas; mantener visible el servicio elegido. Sin disponibilidad: informar sin prometer alternativas inexistentes y permitir cambiar fecha o volver.
3. **Revisar solicitud:** mostrar servicio, fecha, hora, precio y condiciones únicamente si se conocen, junto a datos de contacto solo si se justifican. Permitir editar cada elección antes de una acción explícita «Solicitar reserva».
4. **Resultado:** mostrar confirmación solo tras respuesta positiva del sistema, con los datos recibidos. En espera, indicar progreso; ante error, explicar el problema y conservar los datos cuando sea seguro. Un resultado incierto no debe afirmar que la reserva se creó ni invitar a duplicarla sin comprobar el estado.

La navegación hacia atrás conserva las elecciones válidas; si dejan de ser válidas, se comunica y se solicita una nueva selección. Etiquetas, contenido y comportamiento dependen de los contratos de producto y sistema por validar.

## Dirección visual y componentes

Propuesta provisional: fondo claro neutro, texto oscuro y un único color de acento para acciones; no fijar códigos de marca sin decisión. Tipografía sans serif del sistema como punto de partida, con títulos claramente diferenciados y texto legible sin depender de tamaños absolutos. Composición de una columna en móvil, cabecera con título de etapa, contenido prioritario y acción principal coherente. En pantallas amplias limitar el ancho de lectura y, si ayuda, mostrar un resumen lateral sin cambiar el orden lógico.

Componentes: lista de servicios, selector de fecha y hora, resumen editable, campos etiquetados, botones y mensajes de estado. Cada uno contempla reposo, foco visible, selección, deshabilitado cuando proceda, carga y error; nunca usar solo color para comunicar estado. Mantener denominaciones, espaciado y tratamiento de acciones coherentes entre etapas. Los importes y condiciones ausentes se identifican como pendientes, no se inventan.

## Criterios verificables propuestos

- A 320 px de ancho y con ampliación de texto al 200 %, contenido y controles siguen disponibles sin solaparse ni exigir desplazamiento horizontal de la página.
- Todo el flujo se opera con teclado; el foco es visible, sigue el orden de lectura y llega a mensajes y acciones relevantes. Los controles tienen nombre accesible; errores se asocian al campo y se anuncian cuando aparecen.
- Texto normal alcanza contraste de al menos 4,5:1 y texto grande 3:1; controles y foco pertinentes alcanzan 3:1 frente a su entorno. Verificar con los colores reales seleccionados, no inferir conformidad de esta propuesta.
- Las acciones táctiles apuntan a al menos 44 × 44 píxeles CSS cuando sea viable; si no, documentar alternativa y comprobación de uso. Las etiquetas y estados no dependen exclusivamente de color o iconos.
- Con datos de prueba aprobados, Quality puede recorrer selección, revisión, corrección, éxito, ausencia de disponibilidad, fallo y respuesta incierta; comprueba que no se presenta éxito antes de recibirlo. No hay prueba ni conformidad acreditada en este ejercicio.

## Riesgos, incertidumbres y siguiente acción

La viabilidad de precio, inventario y confirmación es desconocida; la respuesta incierta requiere un contrato de recuperación antes de implementación. Falta validar marca, público, idioma, dispositivos, privacidad y reglas comerciales. Los criterios requieren diseño e implementación reales y revisión independiente. No se conoce una identidad previa para este escenario ficticio; no se ha consultado investigación de usuarios ni se han generado imágenes o prototipos.

**Bloqueos:** ninguno para entregar esta propuesta; faltan decisiones de producto y factibilidad para convertirla en especificación de implementación. **Próxima acción:** TERRA contrasta las hipótesis con Discovery y Architect y eleva al Owner las decisiones de alcance y dirección visual que correspondan. No se emite dictamen Quality ni aceptación del Owner. **E2E NO EJECUTADO.**
