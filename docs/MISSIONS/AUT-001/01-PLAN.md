# AUT-001 · Plan de autonomía y consultas al Owner

**Estado:** DRAFT; Gate 1 PENDING. **Orchestrator y autor declarado del plan:** TERRA, con propuesta del agente `/root/aut001_architect`. **Riesgo:** HIGH propuesto de forma conservadora por afectar decisiones transversales de gobernanza; no implica aceptación de riesgo. **Baseline:** CORE `bce0d41aa89a93b30d003dc721a3946f21db43ba`, árbol original limpio al crear copia aislada. El Owner autorizó AUT-001, revisión y Git, no un waiver o PASS artificial; no modificar APP-002 ni derivados.

## Objetivo y alcance

Incorporar en el contrato existente del Orchestrator las reglas Owner para resolver consultas con autonomía y escalar decisiones, y para suministrar contexto trazable a agentes. La única fuente normativa propuesta es `AGENTS.md`: ampliar el punto Orchestrator y su sección de comunicación. En `README.md` añadir una indicación de uso portable que remita a esa fuente sin duplicar la regla. No existe actualmente `agents/orchestrator.md`; no crearlo ni duplicar el contrato en `ROLE_MATRIX.md`. La redacción es neutral respecto a plataformas; eso no demuestra que Codex, Cursor o Claude Code carguen o cumplan automáticamente estas instrucciones.

## Contrato propuesto

Después del punto Orchestrator añadir: «Antes de plantear una cuestión al Owner, el Orchestrator consulta las decisiones previas aplicables, los contratos y requisitos vigentes y la autoridad técnica delegada, con sus fuentes y vigencia. Resuelve dentro de esa autoridad o asigna la cuestión al especialista competente cuando corresponda. Consulta al Owner ante una decisión nueva, ambigüedad material, contradicción, riesgo relevante o duda razonable; no reduce consultas a costa de la supervisión del Owner ni interpreta su silencio como permiso. Al consultar, expone la cuestión, por qué requiere decisión, la recomendación y sus consecuencias. El Owner conserva las decisiones de alcance, riesgos aceptados, excepciones y aceptación. Ninguna delegación sustituye las autorizaciones o Gates exigidos.»

En comunicación añadir: «Antes de delegar, el Orchestrator proporciona el objetivo y alcance, las instrucciones, decisiones, documentos, referencias y versiones necesarias, los criterios de aceptación y el formato de respuesta. Cuando un agente necesite contexto adicional, lo solicita al Orchestrator, que lo recupera de fuentes autorizadas y facilita su contenido con procedencia y versión o hash cuando estén disponibles, identificando límites y datos no verificados. Cuando un rol requiera lectura del código o de fuentes, el Orchestrator garantiza su acceso mediante un medio verificable o declara el bloqueo. El intercambio de contexto no acredita identidad, independencia ni aislamiento técnico. Si falta contexto obligatorio que no puede recuperarse ni entregarse por un medio verificable, declara el bloqueo.»

En README añadir: «Para usar estas instrucciones con cualquier herramienta de agentes, proporciona `AGENTS.md` al Orchestrator y verifica que sus instrucciones estén disponibles en ese entorno; no supongas que todas las herramientas lo cargan automáticamente.» Esto orienta la preparación de APP-003 sin afirmar compatibilidad o ejecución real en herramientas concretas.

Alternativas: crear un archivo de rol separado duplicaría la regla para este cambio; limitar consultas indiscriminadamente reduciría supervisión. No introducir infraestructura, poderes nuevos, aceptación de riesgos ni una excepción automática.

## Escenarios y verificación

Verificar con escenarios documentados: decisión previa inequívoca y vigente; cuestión técnica delegada resuelta o asignada; nueva decisión funcional; ambigüedad material, contradicción, riesgo o duda razonable escalados; consulta sencilla útil permitida; ausencia/silencio no autorizan; fuente obligatoria ausente bloquea; petición de contexto recibe fuente y versión sin afirmar aislamiento; Owner retiene alcance, riesgos, excepciones y aceptación. Cada escenario debe indicar entrada, fuentes, resultado esperado y resultado observado; no confundir comprobaciones estáticas de texto con prueba de conducta real del modelo o de integración con un runtime. Todo NOT_RUN hasta ejecución real.

## Gates, riesgos y reversión

Quality distinto del autor revisará plan y versiones con autoridad de FAIL; Gate 1 se tramitará según política realmente aplicable, sin fabricar I1/G1. Luego se aplicaría el diff mínimo, revisión independiente Gate 2, escenarios y Gate 3, y aceptación Owner según política. El Charter y arquitectura CORE son plantillas DRAFT con `[DECIDIR]`; ADR-0001 está PROPUESTO. `AGENTS.md` exige completar Charter antes de misiones productivas, sin definir expresamente aquí si esta misión de gobernanza lo es: cuestión de aplicabilidad no resuelta, no suplirla por inferencia. Los requisitos de identidad e independencia HIGH no están aún acreditados; la política de excepción recién incorporada no se aplica automáticamente a esta misión.

Reversión futura: inspeccionar cambios posteriores y usar parche inverso revisado, preservando evidencias y trabajo ajeno; no usar reset destructivo. Riesgos: instrucción demasiado restrictiva, delegación sin autoridad, pérdida de supervisión y discrepancias entre plataformas. Una regla textual no garantiza ejecución. E2E NO EJECUTADO.
