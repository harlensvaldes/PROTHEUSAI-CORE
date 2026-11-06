# DOC-001 · Escenarios sintéticos A–G

2026-11-06. Ejecutados como razonamiento por `/root/doc001_scenarios` sobre el contrato y la plantilla, no como ejecución de producto. Todos los comandos, rutas, fechas, versiones, pruebas y capturas de este archivo son fixtures hipotéticos, no evidencias de CORE. No acreditan Quality, CI, aceptación o E2E.

- A · Web: `![Vista principal](docs/screenshots/vista.png)` solo en un fixture cuya captura proviene de la aplicación realmente ejecutada, está autorizada, es legible y no contiene datos sensibles. No se afirma que exista esa captura aquí.
- B · CLI: README con propósito, instalación, uso y verificación; se omite captura por no existir interfaz visual.
- C · Sin pruebas: `## Verificación` seguido de `Not run`, sin badge PASS.
- D · Resultado parcial ficticio: `pytest tests/unit -q`; 2026-01-10 10:00 UTC; `fixture-D-v1`; 8 aprobadas, 2 fallidas, 3 omitidas; estado FALLÓ; referencia hipotética `fixtures/D/report.txt`. Las omitidas no son aprobadas ni se confunde con CI o Quality.
- E · Cobertura desconocida: `Cobertura: no medida`; no se publica porcentaje.
- F · Sin licencia declarada: se omite la sección de licencia; no se inventa MIT ni otra.
- G · Resultado ficticio de `fixture-G-v1`: `pytest -q`, 2026-01-10 11:00 UTC, 5 aprobadas, 0 fallidas, 1 omitida, estado finalizado con omitida y referencia hipotética `fixtures/G/report.txt`; se rotula HISTÓRICO para `fixture-G-v2`, cuya verificación figura Not run/no verificada.

Ejemplo mínimo de README CLI ficticio:

```markdown
# Herramienta de ejemplo

CLI de ejemplo para procesar entradas locales.

## Uso
`ejemplo --help`

## Verificación
Not run.
```

El ejemplo es ilustrativo: nombre, capacidad y comando no corresponden a un proyecto ejecutado. Los escenarios muestran cómo aplicar las instrucciones, no garantizan que un ejecutor futuro las cumpla o que haya carga automática en sus herramientas. E2E NO EJECUTADO.
