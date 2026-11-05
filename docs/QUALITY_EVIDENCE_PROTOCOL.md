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
