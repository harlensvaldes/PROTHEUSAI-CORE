# Misiones

Una carpeta por misión, creada con:

```bash
python scripts/new_mission.py --id APP-001 --title "Primera función" --risk MEDIUM --orchestrator "orch-01" --architect "arch-01"
```

El script crea `mission.json` (esquema v2) y los formularios Markdown. El registro nace con **todos los Gates en PENDING**, identidades **solo declaradas** y `roles.developer` vacío: el Developer se registra cuando existe implementación real, nunca por defecto. `--author` es un alias obsoleto de `--orchestrator`: emite un aviso y no asigna Developer ni Architect.

Antes de registrar un dictamen, el Orchestrator completa en `mission.json` la `evidence` de cada identidad (método y referencia reproducible). Quien comprueba efectivamente esa evidencia registra `verification` (`by`, método, referencia, fecha). Nadie verifica su propia identidad, y el autor revisado no verifica la identidad de su revisor. La CLI comprueba que estos registros existen y son coherentes; no comprueba identidades. Reglas completas: `docs/QUALITY_EVIDENCE_PROTOCOL.md`.

Un revisor real (distinto de cualquier autor) produce su informe; solo entonces puede registrarse la decisión explícita con evidencia. `PASS_WITH_RESERVATIONS` no habilita transiciones.

### Manifiestos v1 (históricos)
`validate` los acepta con un aviso y sus dictámenes se conservan, pero `can-implement` y `can-close` siempre los bloquean. Para obtener nuevas autorizaciones:
1. Registra el SHA-256 de `mission.json` v1 y renómbralo a `mission.v1.json` sin alterar su contenido. Comprueba que el hash no cambia; la CLI ignora ese archivo.
2. Crea `mission.json` v2 con las identidades reales y su evidencia; nunca las infieras de `author`/`implementation_author`.
3. Cada Gate queda en PENDING salvo que Quality lo revalide con un informe nuevo que cumpla las reglas v2. Los informes históricos no se modifican.

El ejemplo `EXAMPLE-001` demuestra estructura sin fingir que ningún Gate pasó. Validación formal automática: `python scripts/quality_cli.py validate`. No sustituye auditoría técnica.
