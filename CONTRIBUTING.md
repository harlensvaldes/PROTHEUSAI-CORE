# Cómo contribuir

1. Crear una misión identificada (`python scripts/new_mission.py ...`).
2. Redactar alcance, no objetivos, dependencias, riesgos, tests, evidencia y decisiones.
3. Solicitar revisor distinto del autor: Gate 1.
4. Implementar solo el plan aprobado en rama de trabajo y diff acotado.
5. Solicitar Gate 2 al revisor, con lectura de diff real y de pruebas afectadas.
6. Ejecutar Gate 3: CI, pruebas específicas, escenarios negativos y E2E si autorizados; registrar evidencia literal.
7. Obtener autorización de merge/release independiente cuando aplique.

**Cambios de alcance:** actualizar plan, revisar impacto y reabrir Gate 1 si afectan contrato/arquitectura. Un reporte automático nunca sustituye la revisión humana.

**Formato de nombres de misiones:** `AREA-001` o `PROYECTO-MOD-001`; uppercase, números y guiones.

**Definición de terminado:** controles aplicables en verde, evidencia trazable, decisiones aprobadas, documentación actualizada y riesgos residuales aceptados.
