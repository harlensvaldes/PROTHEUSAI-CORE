# Protocolo de evidencia de Quality

## Para todo Gate
- ID y versión exacta de misión.
- Autor y revisor identificados, con prueba operativa de separación.
- Árbol del repositorio, hash base y modificaciones previas no relacionadas.
- Fuentes consultadas; distinguir archivo local de HEAD confirmado.
- Hallazgos con gravedad, riesgo y evidencia verificable.
- Decisión específica; BLOCKER implica FAIL, no PASS condicional.

## Gate 1
Contratos, escenarios adversos, dependencia de módulos, cambios de identidad, migraciones, rollback y matriz de tests previstos. **No se ejecuta código por el hecho de pasar Gate 1**.

## Gate 2
Diff real revisado, nuevos consumidores, eliminaciones, regresiones y tests modificados. Reabrir Gate 1 ante cambio de contrato.

## Gate 3
Para cada prueba: comando, commit/artefacto exacto, entorno, versión runtime, fecha, código de salida, resultado, archivo de evidencia. `E2E NO EJECUTADO` cuando corresponda.

## Manipulación de registros
`mission.json` registra el dictamen externo; el script solo valida algunos campos y jamás puede certificar la veracidad del revisor, la validez de una prueba o la seguridad del producto. Un campo PASS sin informe real es una violación de la política aunque la CLI aceptase su forma.

## Identidades (manifiesto v2)
- `roles.orchestrator`, `roles.architect` y `roles.developer` son listas de identidades; `gates.<n>.reviewer` identifica a Quality en cada Gate. Ningún rol se rellena por defecto: el Developer se registra cuando existe implementación real.
- Cada identidad tiene tres niveles distintos: **declarada** (`id`), **con evidencia** (`evidence`: método y referencia reproducible) y **verificación registrada** (`verification`: quién comprobó efectivamente la evidencia, método, referencia y fecha). Nadie registra su propia verificación.
- La CLI comprueba presencia y coherencia de estos registros, **no** comprueba identidades externas. Su salida lo declara.
- Un Gate PASS o PASS_WITH_RESERVATIONS exige verificación registrada del revisor y de los autores pertinentes. El revisor no puede figurar en ningún rol de autoría, y su verificación no puede registrarla el autor revisado.
- Toda revisión registrada (PASS, PASS_WITH_RESERVATIONS o FAIL) identifica en su informe, con una única línea por etiqueta: `**Dictamen:**`, `**Revisor:**`, `**Artefacto revisado:**` (nombre + `sha256:` o `git:`) y `**Autor efectivo:**`. Los valores coinciden con `mission.json`. PASS y PASS_WITH_RESERVATIONS exigen además `**Independencia verificada:** sí — <evidencia>`.
- Manifiestos v1: históricos. Se validan con sus reglas, sus dictámenes no se modifican y nunca habilitan `can-implement` ni `can-close`. Para obtener nuevas autorizaciones hay que migrarlos o revalidarlos (`docs/MISSIONS/README.md`).

Las entradas y evidencias de Gate son append-only. Un registro perdido se documenta como incidente y solo puede sustituirse por una reconstrucción declarada, verificada contra un hash registrado antes de la pérdida. La CLI no impone esta regla.
