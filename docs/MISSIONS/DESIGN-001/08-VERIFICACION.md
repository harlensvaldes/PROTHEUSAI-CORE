# DESIGN-001 · Evidencia de implementación

Fecha: 2026-11-06. Developer declarado: `codex /root` y `codex /root/bootstrap` en los archivos indicados. Implementación y pruebas no son dictamen de Quality.

`python -B -m unittest discover -s tests -p test_bootstrap001.py -v`, ejecutado en Windows por el Developer de bootstrap: salida **0**, 13 pruebas, una omitida por falta del privilegio de Windows para crear enlaces simbólicos (WinError 1314). `TEST-BOOTSTRAP-02.log` conserva la salida completa; SHA-256 de bytes `a50b94a54d82f748c3f60ad29dfdd8638b52aeb5c2e6b0bc3b51bd7b4fb09ea1`. La prueba genera un proyecto desde un commit sintético, comprueba bytes y procedencia del rol, continuidad, MET y exclusión de expedientes, y ejecuta pruebas MET en el generado con comprobación de al menos una prueba descubierta. El número de pruebas MET no se registró individualmente en el log del test padre. No acredita aún ejecución de bootstrap desde el commit real de CORE.

Las delegaciones reales, la decisión de no convocar por defecto en CLI y sus límites constan en `07-ESCENARIOS.md` y los cuatro informes de escenario. No se implementó ni ejecutó un producto ficticio. La accesibilidad descrita es una propuesta comprobable, no una certificación. **E2E NO EJECUTADO**.

El contrato `agents/creative_director.md` es documentación operativa portable; no instala un agente. La disponibilidad real de skills y delegación depende del runner. Las skills de la sesión que podrían utilizarse condicionalmente son `imagegen`, `computer-use`, `visualize` y `sites`; `frontend-design` no figura en el catálogo disponible. No se instaló infraestructura ni se ejecutó una skill de diseño para los escenarios.
