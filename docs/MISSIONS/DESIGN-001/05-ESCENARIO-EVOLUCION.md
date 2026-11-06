# DESIGN-001 · Escenario ficticio 3: evolución de citas

**Naturaleza:** propuesta acotada, no implementación, dictamen Quality ni aceptación. Fuente: encargo de TERRA para el escenario ficticio 3 y contrato `agents/creative_director.md` (SHA-256 `94e6299e488529e9f9365206989548803d9d4c42e7f4a28fc5b1b01436cbeeee`). No se inspeccionó una aplicación real.

## Decisiones vigentes y alcance

El encargo confirma fondo marfil `#FAF7F0`, texto `#1F2933`, acento azul `#2457A6`, sans serif del sistema, lista vertical de tarjetas, navegación inferior, foco visible y botón primario azul. El Owner solicita una vista de citas próximas y el estado cancelada, conservando identidad, marca y flujos existentes. Estas son entradas confirmadas del ejercicio, no evidencia de un producto desplegado.

**Hipótesis no aprobadas:** existe una ubicación adecuada dentro de la navegación actual para acceder a las citas; cada cita dispone de servicio, fecha, hora y estado fiables. La inclusión de canceladas junto a próximas, su periodo de visibilidad, orden, zona horaria y detalle requieren acuerdo con producto y contraste técnico. No se propone una acción nueva de cancelación, recuperación ni cambio de reserva.

## Propuesta puntual

Reutilizar la estructura de pantalla existente: título «Próximas citas» y lista vertical de las tarjetas actuales, manteniendo navegación inferior y su comportamiento. En cada tarjeta mostrar, cuando los datos existan, nombre del servicio y fecha y hora legibles, seguidos del estado comunicado por el sistema. Propuesta de orden cronológico ascendente para citas próximas; no presentar como requisito aprobado.

Para una cita cancelada, conservar el mismo componente y mostrar una etiqueta textual «Cancelada» junto al resto de información. No depender solo de color, tachado o icono ni insinuar que puede usarse. Su ubicación exacta en la vista queda pendiente: mostrarla solo cuando la regla de producto determine que corresponde; no ocultarla ni incluirla universalmente por suposición. Mantener sin alteraciones los enlaces y acciones ya existentes y su semántica.

Estado vacío: mensaje claro cuando la fuente confirme que no hay citas próximas; carga y error deben distinguirse de vacío. Ante un fallo, conservar los patrones y recuperación existentes; no inventar datos, confirmaciones o nuevas acciones. Preservar el botón primario azul donde ya exista, sin añadirlo artificialmente a esta vista.

## Adaptación y accesibilidad

En móvil mantener una columna y espacio suficiente para que la navegación inferior no tape contenido o foco; en ancho mayor conservar la lista y limitar su ancho de lectura según los patrones existentes. Permitir que fecha y texto se ajusten en varias líneas sin recortar el estado. Mantener orden visual y de lectura coherentes.

Cada tarjeta y acción conserva semántica y nombre accesible adecuados; el foco visible recorre controles en orden lógico. El estado «Cancelada» se comunica como texto accesible. Los mensajes de carga, error y cambio de estado deben poder percibirse sin depender solo del color; anunciar cambios dinámicos pertinentes sin interrumpir innecesariamente.

## Criterios propuestos para comprobar

1. Con datos de prueba acordados se muestran las citas próximas según la regla temporal aprobada; una cancelada se identifica textualmente y su presencia sigue la regla acordada. La pantalla no modifica flujos existentes.
2. A 320 píxeles CSS de ancho y al ampliar texto al 200 %, las tarjetas, estado, acciones existentes y navegación siguen visibles y operables sin solapamiento ni desplazamiento horizontal de página.
3. Con teclado se alcanza cada control en orden lógico, el foco permanece visible y no queda oculto por la navegación inferior; con lector de pantalla se identifica el servicio, fecha, hora y estado disponible.
4. Verificar con los estilos reales el contraste de texto y controles, incluidos estados y foco; contrastar como objetivo texto normal ≥4,5:1, texto grande ≥3:1 y límites/foco pertinentes ≥3:1. Las entradas de color no prueban por sí solas la conformidad de todos los estados.
5. En pruebas con carga, vacío y error se distingue cada estado y no se comunica una cita inexistente ni una cancelación inventada. Quality revisa las fuentes y la implementación real.

## Riesgos y próxima acción

La semántica de «próxima» frente a «cancelada», las reglas de disponibilidad de datos y el acceso desde la navegación son desconocidos. La propuesta no cambia identidad ni reinicia Discovery; requiere resolver esas incertidumbres con producto y Architect antes de implementación. No se verificaron dispositivos, contraste real ni accesibilidad implementada. **Bloqueos:** ninguno para la propuesta; falta la definición de reglas para implementarla. **Próxima acción:** TERRA contrasta las reglas pendientes y encarga al Developer adaptar los componentes existentes; Quality verifica independientemente. **E2E NO EJECUTADO.**
