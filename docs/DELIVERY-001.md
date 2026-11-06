# DELIVERY-001 · Entregas independientes

El mecanismo copia una selección explícita y genera instrucciones, informe y manifiesto. Se ejecuta desde CORE; el directorio resultante no requiere CORE. Es obligatorio revisar el descriptor y cada archivo seleccionado, especialmente binarios y datos: los nombres excluidos y el escáner heurístico no garantizan ausencia de secretos ni datos privados. Una referencia de aprobación es una declaración, no autenticación. Un manifiesto editable proporciona integridad, no autenticidad.

```powershell
python scripts/delivery001.py prepare --descriptor <descriptor.json> --source <directorio-fuente> --output <directorio-nuevo>
python scripts/delivery001.py verify --directory <directorio-nuevo>
```

El descriptor JSON `delivery-001/v1` exige `product`, `version`, `mission`, `approval`, `known_roots` y `files` (lista positiva de objetos con `source`, `destination`, `sha256`, `provenance`, `justification`, `reviewer`, `review`, `review_date` y `findings`). Cada revisión debe ser real y trazable: `review` es `approved`, `findings` es una lista vacía y el hash corresponde a los bytes revisados. El programa valida las declaraciones, pero no certifica identidad ni que una persona haya realizado la revisión. Una procedencia desconocida o un hallazgo no resuelto bloquea la inclusión; si el archivo es necesario, bloquea la entrega. `known_roots` contiene las raíces del taller a detectar y no se incluye en el paquete. También son obligatorias las listas no vacías `prerequisites`, `install_steps`, `start_steps`, `configuration`, `verification_steps`, `evidence`, `limitations`. Las instrucciones se incorporan literalmente a `INSTALL.md` y no se ejecutan; quien prepara la entrega es responsable de su corrección y de probarlas. `MANIFEST.json` excluye únicamente a sí mismo y conserva resultados de controles y revisión declarada. Verificar antes del primer arranque o con copia inmutable: la aplicación puede modificar sus propios datos.

Se rechazan todos los `.env` y rutas y archivos sensibles conocidos, enlaces, colisiones y destino existente. El escaneo de nombres, patrones de contenido, firmas SQLite y rutas conocidas reduce riesgos pero no garantiza detección de todos los secretos o datos privados. Un fallo puede dejar un directorio temporal hermano para inspección; no hay limpieza automática. El control de cambios concurrentes es limitado y el proceso debe operar en una fuente estable bajo control del responsable. No se ha probado independencia para otros stacks o proyectos.

Para el caso APP-004, con Python 3.12 y Git disponibles:

```powershell
python docs/MISSIONS/DELIVERY-001/prepare_case.py --app <ruta-APP-004> --workspace <directorio-nuevo>
python scripts/delivery001.py verify --directory <directorio-nuevo>/delivery
```

La receta obtiene código del commit fijado y copia tres imágenes y sus metadatos seleccionados. No copia la base del taller; el destinatario crea la semilla ficticia siguiendo `INSTALL.md`. Las fotos están sujetas a las condiciones del proveedor y sus créditos se conservan en `IMAGE_SOURCES.md` y metadatos. El piloto no está autorizado para publicación ni uso real. El procedimiento de ensayo aislado, resultados y límites figuran en la misión; un arranque no constituye E2E.

Para archivar evidencias, preparar otro descriptor con lista explícita de archivos ya revisados y un destino nuevo; el mismo mecanismo copia y genera hashes sin alterar originales. No seleccionar perfiles de navegador, secretos ni bases no auditadas. Para preparar el siguiente encargo, inventariar por separado temporales, respaldos y evidencias y decidir su conservación; este incremento no borra ni marca automáticamente como prescindible ningún archivo.
