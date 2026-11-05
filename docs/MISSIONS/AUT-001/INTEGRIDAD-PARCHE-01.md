# AUT-001 · Integridad del parche preparado

Fecha: 2026-11-05. `REVISION-TECNICA-PLAN-03.md` registró el SHA-256 de bytes del parche en la copia candidata con saltos LF: `b25ea5b5a7676872e1487dcab5fb46629e30dfe864a3e50c64ebc23f0a28ff65`. Al trasladar el commit a CORE, Git convirtió los finales de línea a CRLF en el árbol de trabajo Windows: el SHA-256 de esos bytes observados fue `92f40381cc4ec706aa9d9dfebdc9fd7e83ad349e7332e3fd6a6637ea863f2a79`. El primer hash identifica el contenido LF, no los bytes CRLF del árbol actual.

`git apply --check --unidiff-zero docs/MISSIONS/AUT-001/PROPUESTA-DIFF.patch` terminó con código 0 también en CORE después del traslado. El parche no se aplicó. Esta comprobación no demuestra comportamiento ni autoriza transición.
