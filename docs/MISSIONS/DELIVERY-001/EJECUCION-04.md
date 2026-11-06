# DELIVERY-001 · Cuarta ejecución

Se conserva `GATE2-REVIEW-03.md` con FAIL: se reprodujo una ruta Windows escapada en metadatos JSON que eludía el escaneo. La prueba sintética correspondiente falló antes de la corrección; el escáner ahora examina cadenas JSON decodificadas además de bytes y detecta la reproducción. La cobertura sigue siendo limitada y no garantiza la detección universal de secretos o datos privados.

`python docs/MISSIONS/DELIVERY-001/prepare_case.py --app ..\protheus-app-004 --workspace dist\delivery001-app004-v4` salida 0; `python scripts/delivery001.py verify --directory dist/delivery001-app004-v4/delivery` salida 0. Su manifiesto SHA-256 `3899099595637eedf75a13486b1a3d421afa89592acb95d6aa5372eacf2065cc` coincide exactamente con v3; los archivos listados también verifican mediante sus hashes. La revisión de archivos y generados `APP004-REVISION.json` y `APP004-REVISION-GENERADOS.md` corresponde a esos mismos bytes, sin transferir una aprobación de Gate.

La prueba aislada de esta candidata exacta terminó con salida 0; log completo `ISOLATED-EXECUTION-04.txt`. Procedimiento y límites: `isolated_smoke.sh`, `isolated_smoke.py` y `EJECUCION-03.md`. Se verificó integridad previa, montaje tmpfs sin taller, ausencia de variable de clave, semilla ficticia, tres imágenes, pedido ficticio y persistencia. No es prueba de navegador ni certificación de identidad o seguridad. **E2E NO EJECUTADO**.

`python -m unittest discover -s tests` salida 0: 239 pruebas ejecutadas, 3 omitidas. La suite focalizada en Ubuntu mediante WSL terminó con salida 0: 7 ejecutadas, ninguna omitida. Las líneas BLOCKED de la suite general proceden de escenarios de gobernanza. Falta nueva revisión independiente de Gate 2.
