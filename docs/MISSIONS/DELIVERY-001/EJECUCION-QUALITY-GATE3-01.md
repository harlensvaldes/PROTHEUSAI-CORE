# Ejecuci?n independiente Quality Gate 3

2026-11-06, Windows PowerShell, workspace compartido, Python del entorno. Candidata `dist/delivery001-app004-v4/delivery`; manifiesto SHA-256 de bytes exactos `3899099595637eedf75a13486b1a3d421afa89592acb95d6aa5372eacf2065cc`.

- `python -m unittest discover -s tests -p test_delivery001.py`: salida 0, 7 pruebas, 1 omitida por disponibilidad de enlaces.
- `python docs/MISSIONS/DELIVERY-001/COPY-FAIL-CHECK.py`: salida 0; error de escritura sint?tico propagado, salida final ausente, origen intacto, staging retenido.
- `python scripts/delivery001.py verify --directory dist/delivery001-app004-v4/delivery`: salida 0.
- `python -m unittest discover -s tests`: salida 0, 239 pruebas, 3 omitidas; mensajes BLOCKED son salidas de escenarios de gobernanza.
- `git diff --check`: sin salida, salida global 0 en secuencia; los archivos no rastreados no quedan cubiertos por este diff.
- Intento `wsl -d Ubuntu -- bash -lc 'cd /mnt/c/0.-REPOSITORIOS-DESARROLLO/0003.\ EN\ DESARROLLO/PROTHEUSAI-CORE && bash docs/MISSIONS/DELIVERY-001/isolated_smoke.sh dist/delivery001-app004-v4/delivery docs/MISSIONS/DELIVERY-001/isolated_smoke.py'`: salida 1, `Wsl/Service/E_ACCESSDENIED`; no se ejecut? el ensayo. No se ha eludido la restricci?n.
- Comparaci?n SHA-256 LF de las entradas del ancla Gate 2: coinciden todas salvo `mission.json`, cuyo cambio de decisiones se admite en el protocolo; no constituye cotejo post-commit.

No repet? el ensayo aislado del Developer; `ISOLATED-EXECUTION-04.txt` es evidencia aportada, no observaci?n propia. No se ejecut? navegador ni E2E. E2E NO EJECUTADO. Esc?ner y manifiesto no autentican contenido ni garantizan privacidad completa.
