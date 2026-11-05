# Procedencia de PROTHEUSAI CORE

Plantilla maestra de ingeniería. No contiene código de negocio ni artefactos de
proyectos piloto.

## Origen

| Campo | Valor |
|---|---|
| Repositorio origen | `protheus-efd` — proyecto piloto EPF Appointments |
| Remoto origen | `https://github.com/harlensvaldes/protheus-efd.git` |
| Commit base | `5ee75df9a725698546d6a40e788553fccdb4afb3` |
| Mensaje del commit base | `docs: definir comunicación entre agentes` |
| Fecha del commit base | 2026-11-04 20:03:35 +0100 |
| Tree SHA del commit base | `b9c8ba9bf2da7a18019b81f31bc1ac88ed6fc271` |
| Método de extracción | `git archive --format=tar <commit>` y extracción del archivo tar |
| Fecha de extracción | 2026-11-05 |
| Independencia | `.git` propio, sin remotos, sin historial heredado |

El commit base contiene la gobernanza EPF v1.0 y la política de comunicación
compacta entre agentes de `AGENTS.md`.

## Fidelidad verificada

El primer commit de este repositorio (`baseline: PROTHEUSAI CORE reconstruido
desde EPF 5ee75df`) tiene el mismo tree SHA que el commit base del proyecto
origen:

```bash
git -C PROTHEUSAI-CORE rev-parse "HEAD^{tree}"           # b9c8ba9bf2da7a18019b81f31bc1ac88ed6fc271
git -C protheus-efd rev-parse "5ee75df^{tree}"           # b9c8ba9bf2da7a18019b81f31bc1ac88ed6fc271
git -C PROTHEUSAI-CORE ls-tree -r HEAD                   # idéntico a ls-tree -r 5ee75df
```

La igualdad del tree SHA es una comprobación criptográfica: mismos blobs, mismas
rutas y mismos modos. 53 archivos, todos modo `100644`. Se exportó el commit
versionado, **no** el árbol de trabajo del proyecto origen.

## Exclusiones deliberadas

No forman parte de esta plantilla:

- Código de negocio del piloto (`src/appointments/`, `requirements-app.txt`).
- Misión `APP-001` (`docs/MISSIONS/APP-001/`): plan, Gates, revisiones, decisiones,
  registro de experimentos y evidencias visuales.
- Historial Git del piloto: los commits posteriores al base no se heredan y este
  repositorio no comparte base de objetos con el origen.
- Entornos locales y archivos no versionados (`.venv/`, caches, secretos).

`docs/MISSIONS/EXAMPLE-001/` es el ejemplo demostrativo de la plantilla EPF v1.0,
con todos los Gates en `PENDING`; no es evidencia de ningún proyecto real.

## Alcance de esta versión

Contenido = EPF v1.0 + política de comunicación entre agentes, sin cambios
funcionales de gobernanza y sin skills. Respecto al commit base no se modifica
ningún script, política, plantilla ni control de calidad; este documento y el
índice son las únicas adiciones.

## Estado del proyecto piloto

La aceptación del Owner sobre `APP-001` permanece `PENDING` en el repositorio de
origen. Este documento no declara aceptación, cierre ni aprobación alguna sobre
ese proyecto y no autoriza despliegues.

## Referencias

- `FILE_INDEX.md` — inventario de archivos de la plantilla.
- `README.md` — uso de la plantilla EPF v1.0.
- `docs/QUALITY_POLICY.md` y `quality/controls.json` — controles de calidad.
