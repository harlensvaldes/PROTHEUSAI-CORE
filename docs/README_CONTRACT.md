# Contrato de README técnico del producto

Cada proyecto de software generado con PROTHEUSAI mantiene un `README.md` propio durante el desarrollo y lo actualiza antes de la entrega. Describe el producto real, no copia la presentación de CORE. Usa una presentación clara y cuidada, adecuada para GitHub, sin convertirla en publicidad. Adapta la estructura al proyecto y omite secciones vacías o irrelevantes; consulta `docs/templates/README_PRODUCT.md` como guía, no como formulario obligatorio.

Considera, cuando corresponda: nombre y logotipo existente; propósito; badges verificables; funcionalidades implementadas; capturas reales; tecnologías y requisitos; instalación, configuración y ejecución; pruebas y última verificación conocida; estructura técnica o referencia a arquitectura; limitaciones; licencia solo si está declarada. No presentes planes o funcionalidades no implementadas como existentes.

## Evidencia de verificación

Publica únicamente resultados de ejecuciones reales y verificables. Para cada resultado conocido, proporciona comando, fecha y hora con zona, commit o versión probada, cantidades de pruebas aprobadas, fallidas y omitidas, estado final y referencia al informe o registro, en la medida en que existan. Identifica explícitamente los datos que falten. Las omitidas no son aprobadas. No inventes cifras, cobertura, compatibilidades, versiones ni resultados PASS; muestra cobertura solo si se midió. Si no hay ejecución, indica `Not run` o equivalente. Si el resultado corresponde a una versión anterior o a un árbol de trabajo distinto, márcalo como histórico y no como estado del commit actual. Distingue los resultados de pruebas y CI de los dictámenes Quality, E2E y aceptación final.

Cuando sea viable, prefiere un resumen determinista derivado de los informes existentes, sin construir un sistema nuevo para generarlo. Usa badges enlazados a fuentes verificables; si existe CI, prefiere su estado real. No uses un badge PASS estático sin evidencia ni supongas GitHub Actions: no crees CI solo para producir badges.

## Capturas y documentación adicional

Para una interfaz visual, incluye capturas de la aplicación realmente ejecutada cuando se puedan obtener mediante herramientas autorizadas. Protege datos personales, credenciales y secretos; usa resolución legible, rutas relativas compatibles con GitHub y evita imágenes redundantes o pesadas. `docs/screenshots/` es una ubicación sugerida. Una CLI, biblioteca o servicio sin interfaz visual no necesita capturas; nunca presentes ilustraciones ficticias como producto terminado.

Un manual extendido, portal, sitio promocional, documentación comercial o tutoriales extensos solo se añaden por solicitud expresa del cliente o necesidad justificada del proyecto. El README no sustituye los contratos y evidencias del proyecto.

## Responsabilidades

TERRA, como Orchestrator, garantiza que la documentación forme parte de la entrega; Developer mantiene el README conforme evoluciona el producto; Quality contrasta sus afirmaciones con el código, los comandos y las evidencias disponibles en las revisiones existentes. Ninguna de estas instrucciones crea un Gate ni sustituye autorizaciones.
