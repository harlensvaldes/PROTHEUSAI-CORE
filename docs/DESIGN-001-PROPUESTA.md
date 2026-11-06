# DESIGN-001 — Propuesta de integración del Director Creativo

Decisión del Owner: incorporar esta capacidad. Este documento propone su integración; no la implementa ni crea un Gate.

## Contrato y convocatoria

TERRA convoca al Director Creativo cuando una interfaz significativa necesita dirección visual, preferentemente durante Discovery y antes de su implementación, o para una iteración visual posterior. No es obligatorio en misiones sin interfaz relevante. Su mandato es traducir la intención del cliente en una experiencia coherente: dirección de arte, UX/UI, jerarquía, tipografía, componentes, responsive, accesibilidad desde el diseño y crítica visual. No sustituye al Owner, al Architect, al Developer ni a Quality.

## Entradas, salidas y colaboración

Entradas: objetivos del Owner, usuarios, contexto de uso, referencias autorizadas, restricciones de contenido, plataformas, accesibilidad y presupuesto. El Director identifica incertidumbres y las comunica a TERRA; las decisiones visuales importantes corresponden al Owner.

Salidas proporcionadas a la misión: dirección visual breve, referencias y procedencia, jerarquía y flujos, comportamiento móvil y escritorio, especificaciones implementables de componentes y estados, criterios verificables y, cuando aporten valor, wireframes o mockups. Architect contrasta viabilidad y fronteras técnicas; Developer implementa; Quality revisa el resultado con acceso a la versión y evidencia correspondiente. La aceptación visual del Owner se registra separada de las verificaciones técnicas.

En Discovery las salidas informan los requisitos y el plan; los controles de plan, diff y evidencia siguen los Gates existentes cuando sean aplicables. Las iteraciones respetan las decisiones vigentes y escalan cambios materiales. No existe aprobación automática del diseño ni obligación de convocar al rol en todos los proyectos.

## Skills y selección

TERRA selecciona por necesidad real y disponibilidad: `frontend-design` para dirección de interfaces; `imagegen` solo para imágenes generadas o edición autorizada; `computer-use` para inspección visual y de interacción en una aplicación real; herramientas de prototipado existentes cuando faciliten la comunicación. Las referencias y fotografías externas requieren fuentes y derechos adecuados. Una skill no reemplaza al rol ni a la revisión independiente.

## Ejemplo

En una futura tienda móvil, el rol propone una composición, tipografía, ficha de producto y estados de carrito; documenta referencias y criterios de contraste y responsive. Architect valida restricciones, Developer implementa, Quality verifica estados y teclado, y el Owner evalúa la dirección visual. No se atribuyen al Owner pruebas técnicas que no realizó.

## Incremento mínimo sugerido

1. Añadir un contrato breve en `agents/` y documentar convocatoria opcional en Discovery, reutilizando la estructura existente.
2. Probarlo en una misión de interfaz con entradas y salidas reales; verificar que el Developer pueda implementar y Quality evaluar sin inventar criterios.
3. Revisar fricción, trazabilidad y coste antes de extenderlo.

Esfuerzo preliminar: pequeño para el contrato y una prueba piloto; depende de herramientas y contexto. Riesgos: referencias sin derechos, especificaciones visuales ambiguas, accesibilidad insuficiente y confundir una aprobación estética con pruebas funcionales. Mitigación: procedencia, criterios concretos y separación de evidencias.
