# BOOTSTRAP-001 — crear un proyecto

Desde un commit de CORE que incluya el generador y su lista positiva:

```powershell
python -B scripts/bootstrap001.py --name "Nombre del producto" --id nombre-producto --destination C:\ruta\nueva
```

El padre del destino debe existir; el destino no puede existir, solaparse con CORE ni estar dentro de un repositorio Git. Se rechazan enlaces y puntos de reanálisis en la ruta. El nombre debe ocupar una línea y el ID usa minúsculas ASCII, números y guiones internos. No se aceptan fuentes o lista positiva modificadas frente al commit activo. Se requiere Python y Git instalados.

El proyecto incluye `README.md` propio, `START_HERE.md`, `prompts/00_START_PROJECT.md`, los contratos y herramientas enumerados en `bootstrap/allowlist.json`, y un repositorio Git sin commit ni remoto. `bootstrap-provenance.json` registra commit de CORE, hash de lista y hashes de archivos copiados. La lista es positiva y excluye misiones y paquetes históricos. Revisa el README y realiza Discovery antes de definir el producto.

Si hay un error después de crear el directorio, se informa de la ruta parcial y no se elimina automáticamente. La protección no garantiza seguridad frente a un tercero que modifique concurrentemente los directorios padre. La inicialización aísla las variables Git y evita configuración global y plantillas externas; Git y Python siguen sujetos a los permisos nativos del entorno. La ausencia de información sensible no queda demostrada universalmente por la lista positiva.
