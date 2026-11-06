# Primera hora de un proyecto nuevo

## 1. Define el problema antes del stack
Comienza el descubrimiento con `prompts/00_START_PROJECT.md`: aclara la finalidad y acuerda con el cliente un MVP antes de comprometer su implementación. Después utiliza ese acuerdo para rellenar `docs/PROJECT_CHARTER.md`: usuarios, procesos, alcance, límites, riesgos y responsables. Si no sabes cuál es el daño máximo de un bug, todavía no has terminado esta fase.

## 2. Fija las fronteras
Completa `docs/ARCHITECTURE.md`: dominios, fuentes de verdad, persistencia, contratos, identidad, transacciones, permisos y operaciones asíncronas. Las decisiones irreversibles requieren un ADR.

## 3. Decide el nivel de riesgo
Consulta `quality/RISK_MATRIX.md`. No clasifiques una tarea de navegación como meramente visual si toca guardado, estado o autorización.

## 4. Comprueba las herramientas REALES
- ¿Quién implementa?
- ¿Quién revisa independientemente?
- ¿Qué herramienta de delegación se puede invocar realmente?
- ¿Cómo se obtiene código en lectura para el revisor?
- ¿Qué CI corre los tests y quién puede aprobar merges?

Nunca confundas tener un prompt con haber instalado/invocado un agente.

## 5. Abre la misión inicial
Usa `scripts/new_mission.py`. Redacta el plan y criterios medibles. Identifica los tests antes de escribir código productivo.

## 6. Pasa Gate 1
Revisión independiente del plan, con evidencias y dictamen. Fallo bloqueante = no se implementa.

## 7. Programa en incrementos
Mantén el diff mínimo; preserva trabajo previo no commiteado, datos y migraciones.

## 8. Pasa Gates 2 y 3
Gate 2 examina el diff; Gate 3 exige pruebas realmente ejecutadas. E2E no ejecutado = indicarlo explícitamente. Un test verde no demuestra por sí solo que el software cumple todo el dominio.

## 9. Autoriza el release separadamente
Aprobación de Gate 3 no despliega nada por sí sola. Sigue `docs/RELEASE_POLICY.md`.

## Orden recomendado de lectura
`AGENTS.md` → `docs/PROJECT_CHARTER.md` → `docs/ARCHITECTURE.md` → `docs/QUALITY_POLICY.md` → `docs/TEST_STRATEGY.md`.
