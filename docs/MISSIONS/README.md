# Misiones

Una carpeta por misión, creada con:

```bash
python scripts/new_mission.py --id APP-001 --title "Primera función" --risk MEDIUM --author "dev-01"
```

El script crea `mission.json` y los formularios Markdown. El registro nace con **todos los Gates en PENDING**. Un revisor real (distinto del autor) produce su informe; solo entonces puede registrarse la decisión explícita con evidencia.

El ejemplo `EXAMPLE-001` demuestra estructura sin fingir que ningún Gate pasó. Validación formal automática: `python scripts/quality_cli.py validate`. No sustituye auditoría técnica.
