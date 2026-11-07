# Engineering Project Foundation (EPF)

**Plantilla reutilizable de gobernanza, arquitectura, agentes y Quality Gates para proyectos de software.**

No impone FastAPI, React, PostgreSQL ni otro stack. La estructura inicial contiene **documentación y herramientas de calidad**, no una aplicación de negocio ni una certificación de calidad automática.

## Inicio rápido (Windows / Linux / macOS)

1. Descomprime el ZIP y renombra la carpeta con el nombre del nuevo proyecto.
2. Lee `START_HERE.md` y `AGENTS.md`.
   Para usar estas instrucciones con cualquier herramienta de agentes, proporciona `AGENTS.md` al Orchestrator y verifica que sus instrucciones estén disponibles en ese entorno; no supongas que todas las herramientas lo cargan automáticamente.

3. Inicia el descubrimiento con `prompts/00_START_PROJECT.md` y acuerda el MVP con el cliente. Proporciona el prompt al ejecutor y verifica que esté disponible; no supongas que se carga automáticamente. Usa el acuerdo para completar `docs/PROJECT_CHARTER.md`, `docs/ARCHITECTURE.md` y `docs/QUALITY_POLICY.md` **antes de desarrollar**.
4. Decide tu stack y sustituye los marcadores `[DECIDIR]`.
5. Confirma **de verdad** cómo se invoca un revisor independiente en tus herramientas. Un archivo `agents/quality.md` **no crea automáticamente** un subagente.
6. Ejecuta el chequeo de la plantilla:

   ```bash
   python scripts/quality_cli.py validate
   python -m unittest discover -s tests -v
   ```

7. Abre la primera misión:

   ```bash
   python scripts/new_mission.py --id INIT-001 --title "Definir arquitectura inicial" --risk MEDIUM --orchestrator "orchestrator-01" --architect "architect-01"
   python scripts/quality_cli.py status --mission INIT-001
   ```

8. Somete el plan a **Gate 1 independiente**. No uses la aprobación del mismo agente que redactó el plan.

## Arquitectura del proceso

```text
PRODUCT OWNER define alcance + riesgo
         |
ARCHITECT prepara plan/contratos
         |
GATE 1 -> revisor independiente -> PASS / FAIL
         |
DEVELOPER implementa + pruebas locales
         |
GATE 2 -> revisión independiente del diff
         |
GATE 3 -> evidencia ejecutada, regresiones, aceptación
         |
PRODUCT OWNER autoriza integración/despliegue
```

Los Gates son **controles humanos/organizativos**, no magia de IA. `quality_cli.py` comprueba coherencia de metadatos y archivos; **no otorga PASS** ni reemplaza auditoría técnica o pruebas.

## Carpetas principales

- `docs/`: charter, arquitectura, seguridad, estrategia de pruebas, releases y decisiones (ADR).
- `docs/templates/`: formularios Markdown de misión, Gates, hallazgos, evidencias.
- `docs/MISSIONS/`: plan y registros por misión.
- `agents/`: instrucciones portables para arquitecto, desarrollador, Quality y release manager.
- `quality/`: política de riesgos y controles verificables.
- `scripts/`: utilidades offline, solo biblioteca estándar de Python.
- `tests/`: pruebas de la propia gobernanza.
- `.gitea/workflows/`: CI de partida para Gitea Actions (adaptar runner a tu instalación).
- `src/`: marcador vacío del producto; añade aquí el stack que elijas.

## Comandos de gates

```bash
python scripts/quality_cli.py status --mission INIT-001
python scripts/quality_cli.py can-implement --mission INIT-001
python scripts/quality_cli.py can-close --mission INIT-001
```

`can-implement` solo comprueba registro formal de Gate 1 PASS y revisor distinto del autor; **no verifica** la competencia del revisor ni la validez técnica del informe. La evidencia siempre debe ser contrastada por un responsable autorizado.

### Verificación determinista de anclas

```bash
python scripts/quality_cli.py manifest docs/MISSIONS/INIT-001/GATE2-INPUT-01.sha256
python scripts/quality_cli.py audit --mission INIT-001
```

`manifest` recalcula `sha256_lf` de cada entrada contra el árbol actual (0 todas coinciden, 1 discrepancias, 2 lectura imposible). `audit` contrasta el registro de la misión con los hashes anclados en sus manifiestos: los errores señalan discrepancias de registro y la deriva del árbol se informa como aviso; un manifiesto histórico puede ya no coincidir con el árbol. La clasificación gobernanza/producto es informativa y no altera qué artefactos forman parte de un Gate. Ninguno de los dos comandos emite dictamen de Quality ni comprueba identidades.

## Notas de uso

- Pensado para iniciar proyectos nuevos y para introducir Quality progresivamente en productos existentes.
- Ramas protegidas, secrets, runners, migraciones y despliegues deben configurarse según infraestructura real.
- El proyecto `docs/MISSIONS/EXAMPLE-001` es un **ejemplo pendiente**, nunca un PASS fabricado.
- Derechos de uso: plantilla preparada para reutilización privada o interna. Añade la licencia del producto final según corresponda.
