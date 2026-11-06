# DELIVERY-001 · Consulta Quality sobre trazabilidad

Fecha: 2026-11-06. Consulta estática de `codex /root/quality_trace`, instancia delegada con acceso de lectura y contexto heredado compartido (I0 declarado); identidad y aislamiento no certificados. No escribí ni implementé los artefactos históricos consultados. Esta consulta no es un nuevo Gate ni modifica dictámenes, reglas o aceptación. No ejecuté pruebas ni inspeccioné de nuevo el registro runtime.

## Resultado: BLOQUEADO bajo la política vigente

El protocolo `docs/QUALITY_EVIDENCE_PROTOCOL.md:29-33` exige transmitir la referencia antes de encargar la revisión, cotejar instrucción e informe y leer el ancla directamente del registro runtime antes de la aceptación, por el Owner o Quality que no emita una decisión I1 de Gate en la misión. `POST-GATE-VALIDATION-01.md` y `LECTURA-ANCLA-04-TERCERA.md` registran que el mensaje accesible es opaco. No se acredita su contenido ni se concluye que la transmisión no ocurrió; la coincidencia de hashes no demuestra el contenido transmitido.

Una actuación prospectiva posible sería transmitir a un revisor independiente una instrucción legible con la referencia y hash de la versión actual, registrar el mensaje y el recibo, y cotejar independientemente instrucción, bytes e informe. Acreditaría solamente lo observado en esa transmisión y revisión nuevas, con las limitaciones del registro y permisos compartidos; no demostraría la instrucción histórica, autenticidad ni aislamiento. Es una posible medida compensatoria, no una equivalencia prevista por la política. No se ha ejecutado.

La lectura histórica exigida sigue sin acreditarse aunque la actuación prospectiva resulte satisfactoria. `docs/QUALITY_POLICY.md:27` dispone que una reserva no habilita transiciones y requiere política de excepciones explícita aprobada y autorización humana documentada. La excepción existente se limita a Gate 1 v4 y no cubre este caso. Además, `docs/QUALITY_POLICY.md:52` exige reabrir Gate 1 y decisión del Owner si cambia la regla aplicable a una misión v3/v4 aún no aceptada. No se puede prometer que una excepción resuelva el bloqueo sin atender esa exigencia.

Una única decisión que podría plantearse al Owner es autorizar el diseño y revisión de una excepción puntual y documentada para el requisito histórico, condicionada a comprobación prospectiva y conservando todos los dictámenes históricos. Sería preciso resolver expresamente la reapertura exigida por la política; no implica aceptación, certificación retrospectiva ni autorización de despliegue.

## Fuentes y versión

SHA-256 de bytes exactos, recalculados en la consulta:

- `docs/QUALITY_EVIDENCE_PROTOCOL.md`: `c8cffb9b3627378f3f69f59b4e3531f1a56eb01a8853b210a195ca45381edfb3`.
- `docs/QUALITY_POLICY.md`: `512c5c1b0deb65b538c918c4ffeb224e312aa48aee5cd8be0e3bb5a3762fbb7f`.
- `POST-GATE-VALIDATION-01.md`: `6141b777c1778b890cee7360c3b6165666dced322bd776f52ede78fb3bd3a848`.
- `LECTURA-ANCLA-04-TERCERA.md`: `46f3aa524f3d4f31c53b7b177ff8892dfeb4544322c14d8260d82391cbe0b70b`.

La consulta se limita a estas fuentes accesibles y a `AGENTS.md`, `agents/quality.md` y `mission.json`; no autentica su historia ni demuestra exhaustividad de fuentes. E2E NO EJECUTADO.
