# DELIVERY-001 · Encuadre preliminar para Gate 1

Estado: BORRADOR; Gate 1 PENDING. Autor: terra-root, Orchestrator y Architect declarados. Baseline CORE: 1b14c34ad4a87792a73d4fc9de20d209bfdb4565. APP-004: 0cf56f78c090783f24e93aaedbc2b523d37ba82b, árbol Git limpio; recursos ignorados fuera del commit. Owner autoriza DELIVERY-001 y sus entregables en el mandato de esta sesión; no se infiere adopción del perfil v5 para CORE.

## Alcance y riesgo

Herramienta reutilizable de preparación de una entrega independiente y demostración local ficticia APP-004. No modificar el producto aprobado, no implementar BOOTSTRAP-001 ni DESIGN-001, no despliegue, ni limpieza destructiva. Riesgo provisional HIGH por posible inclusión de secretos o datos privados y consecuencias de una entrega incompleta; la inspección no garantiza ausencia de secretos. Charter general DRAFT: la decisión previa de DISCOVERY-001 afecta aquella misión y no se atribuye automáticamente a esta.

## Diseño candidato, sujeto a revisión

Definir descriptor declarativo por proyecto con identidad, versión aprobada y procedencia, lista explícita de archivos fuente y destino, instrucciones aportadas por el proyecto, y evidencia/limitaciones. Copiar solamente archivos explícitamente autorizados a un destino nuevo; rechazar rutas absolutas en destinos, escapes, enlaces, colisiones, exclusiones sensibles y archivos ausentes. Ningún script debe ejecutar comandos arbitrarios de un descriptor durante la preparación. Generar inventario SHA-256, informe e instrucciones sin referencias al taller; verificación posterior detecta archivos añadidos, eliminados o alterados. El manifiesto excluye su propio hash y explica la frontera. Escaneo de secretos y rutas como control adicional con límites declarados, nunca prueba universal de ausencia. No prometer compatibilidad con otras tecnologías sin prueba.

APP-004 usa Python 3.12, biblioteca estándar y `python -m app.server`; el producto inicializa SQLite en `var/`. Las fotos y metadatos están en `var/images`; la base de trabajo contiene potenciales datos de pedidos. No copiar la base existente sin demostrar que contiene exclusivamente datos ficticios y ausencia de datos privados; preferir crear una semilla ficticia nueva por proceso documentado sin modificar código aprobado. Verificar licencia y procedencia de cada recurso. [Licencia Pexels](https://www.pexels.com/legal-pages/license) y [condiciones](https://help.pexels.com/hc/en-us/articles/900005880463-What-are-the-Terms-and-Conditions): uso en apps admitido con restricciones de distribución aislada; conservar créditos y no interpretar esto como certificación legal.

No instalar dependencias ni ejecutar la aplicación en entorno que pueda acceder al taller para afirmar independencia. Un contenedor o VM debe demostrar que el workspace original no está montado ni accesible y registrar imagen, montajes, versión, comandos y resultados; ejecutar instalación, inicio, API/recursos, persistencia tras reinicio, integridad y análisis de configuración. Smoke no es E2E. Docker daemon no disponible y WSL denegado en comprobación inicial; resolver entorno antes de afirmar éxito. No borrar resultados ni alterar datos originales.

Archivar por copia explícita y hash, sin modificar originales ni incluir credenciales o perfiles de navegador; inventariar candidatos temporales sin borrarlos. MET-001: raíz 01a1b13a-3b02-7052-ad60-01e25c0a3fad, corte inicial exclusivo 2026-11-06T14:19:54Z; datos observados únicamente. Registrar corte final, sin inventar facturación.

## Pruebas previstas y fronteras

Pruebas deterministas: archivo alterado, añadido o ausente; rutas traversal, absolutas y enlaces; colisiones y destino existente; exclusión de secretos, caches, registros y datos privados; errores sin entrega parcial presentada como válida; descriptor mínimo no específico de Python. Comprobar que texto generado y archivos no incorporan rutas absolutas del taller ni credenciales conocidas, con límites de detección. Revisión de diff, pruebas de regresión relevantes, demostración aislada, Gate 2 y Gate 3 independientes y aceptación Owner según política. E2E NO EJECUTADO salvo prueba real.

Archivos concretos, contratos, semilla demostrable y procedimiento de aislamiento aún por precisar antes de un Gate 1 efectivo. Reversión mediante parche inverso revisado y preservación de evidencias; no reset ni limpieza automática. Este documento no autoriza implementación ni representa un dictamen.
