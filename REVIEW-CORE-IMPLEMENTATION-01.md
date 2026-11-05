# Revisión técnica de implementación CORE · entrada 01

Fecha 2026-11-05. Revisor declarado /root/core_quality; autor productivo declarado /root/developer. Acceso de lectura al código y ejecución de pruebas; no he implementado el diff. Contexto heredado y runtime compartido: identidad real e I1/G1 no acreditados. Baseline indicada 11a6f189fd8dc2459232c438e046f58440070b91. Entrada CORE-REVIEW-INPUT-01.sha256 sha256_lf 168b62e8fe0a1a4210554498b794125b94730cc3ab0e03d42a1326be659cab71; 15 hashes de rutas coinciden antes y después de la revisión. El archivo de entrada e informe no se incluyen recursivamente en esa entrada. Aviso Git: acceso denegado al ignore global; el inventario declarado fue contrastado con status visible.

**Dictamen técnico: FAIL.** Gate 1 formal de la reforma permanece PENDING; este informe no certifica identidad ni autoriza transición o cierre. La autorización Owner de ejecución controlada se documenta en OWNER-EJECUCION-CONTROLADA.md y no convierte Gate 1 en PASS. Corregir el defecto y efectuar nueva revisión de entrada fijada. El FAIL se conserva.

## Hallazgo bloqueante

**Contradicción en políticas sobre los mínimos v5.** docs/QUALITY_EVIDENCE_PROTOCOL.md:5 permite I0/G0 para v5, pero el mismo documento bajo «Every Gate» afirma en línea 13 que I0 nunca es suficiente y en línea 15 presenta la matriz quality/controls.json como aplicable sin salvedad. docs/QUALITY_POLICY.md bajo «Independence minimums and reopening» también presenta esa matriz como vigente en términos generales, mientras su sección v5 posterior permite I0/G0. Esto ofrece instrucciones incompatibles sobre si un Gate de piloto v5 puede pasar; AGENTS.md requiere detener el cambio afectado ante contradicción. Corregir de forma explícita el alcance por versión/perfil de los textos generales, preservando requisitos v1–v4 y control reforzado fuera del perfil. No alterar Gates históricos.

## Evidencia y límites

Inspeccioné el diff rastreado y archivos nuevos scripts/quality_v5.py y tests/test_governance_v5.py, además de los planes 01–03, política y protocolo. El validador define perfil exclusivo no CRITICAL, digest del scope, separación de autoría, secuencia y ancla Gate 2; la CLI no autentica identidades ni elegibilidad real. No observé nuevo mecanismo de waiver v5. Esto es revisión estática y pruebas, no una prueba exhaustiva de seguridad o integridad externa. No modifiqué código ni decisiones de Gates.

Comando ejecutado en checkout temporal, Python local: `python -B -m unittest discover -s tests -v`; exit code 0; 227 pruebas ejecutadas, 2 omitidas, salida OK. Las omitidas no son PASS. E2E NO EJECUTADO. No se ha auditado aplicación real de perfil ni aceptación Owner de una misión v5.