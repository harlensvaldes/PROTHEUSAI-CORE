# GOV-001 · Revisión focalizada del plan v8 (v9) — decisiones del Owner del 2026-11-05 09:53

**Estado:** DRAFT v9 — PENDING Quality y Owner. Alcance limitado a esa decisión. Base: `GOV-001-R-PLAN-v8.md` (sha256_lf `0d6bcca0…2a93`).
**Autor (Architect, declarado):** copilot-sdk-main · **Repo:** PROTHEUSAI-CORE `6e5e929`, limpio.

## 0. Efecto sobre el plan v8
| Sección de v8 | Estado en v9 |
|---|---|
| GOV-R01 | **Sin cambios** (APROBADO). Ejecución pendiente de la autorización `OWNER-DECISION-02` según v8. |
| GOV-R02 | **Sustituida por §4.** Pospuesto a GOV-002; firmas SSH solo como línea de investigación. |
| GOV-R03 | **Sustituida por §1–§3.** Cambia el modelo de independencia, los hashes, el esquema y los controles redundantes. |
| Cierre de GOV-001 | Ajustado en §5. |

## 1. Modelo: tres dimensiones separadas
| Dimensión | Pregunta | Quién la aporta | Qué comprueba la CLI |
|---|---|---|---|
| **A. Independencia de autoría** | ¿El revisor produjo o modificó lo revisado? | Roles del manifiesto + declaración del revisor | id del revisor ∉ {orchestrator, architect, developer} (R2 actual, normalizado) **y** `authorship_independent: true` en el bloque del revisor. **Regla absoluta: sin excepción por riesgo ni por Gate.** |
| **B. Aislamiento operativo** | ¿Qué separación de ejecución, permisos y credenciales hay? | Declaración del revisor, con nivel enumerado | Nivel declarado ≥ mínimo exigido. **La CLI no comprueba que sea cierto**. |
| **C. Garantía acreditada** | ¿Qué respalda A y B más allá de la palabra del revisor? | Se **calcula**, no se declara | Las evidencias existen dentro de la misión y su `sha256_lf` coincide; los registros de verificación de identidad existen y cumplen sus reglas. |

Compartir runtime, usuario del sistema operativo o workspace **no** anula A: solo determina el nivel de B. Así, agentes separados de LUNA o Cline en un mismo entorno son válidos si A se cumple y B y C alcanzan el mínimo del riesgo.

**Niveles de aislamiento (B), ordenados:**
- `I0_CONTEXTO_COMPARTIDO`: comparte con algún autor la conversación, la memoria o el contexto de trabajo (por ejemplo, el autor se revisa en el mismo hilo). **Nunca basta para PASS/PWR.**
- `I1_CONTEXTO_SEPARADO`: es otra instancia de agente o persona, sin historial ni memoria del autor; recibe solo referencias. Puede compartir runtime, usuario del sistema, workspace y credenciales. *Es el caso típico de agentes separados de LUNA o Cline.*
- `I2_PERMISOS_SEPARADOS`: I1 y, además, el revisor **no puede modificar** lo revisado (acceso de solo lectura impuesto por el runtime, usuario del sistema o token distinto).
- `I3_ENTORNO_SEPARADO`: otra máquina, organización o entorno bajo custodia distinta.

**Niveles de garantía (C), calculados por la CLI:**
- `G0_DECLARADA`: solo el bloque del revisor, sin evidencias.
- `G1_REGISTRADA`: el bloque cita ≥1 evidencia de aislamiento o identidad (registro de lanzamiento, configuración de permisos, log del runtime…), fijada por `sha256_lf` y ubicada dentro de la misión. Prueba integridad desde que se fijó, **no** veracidad.
- `G2_VERIFICADA`: G1 y además un tercero (`by` ∉ autores del artefacto y ≠ revisor) registró la verificación de la identidad del revisor y de los autores pertinentes. Son los registros `verification` ya existentes (C1).

**Requisitos proporcionales.** Son datos en `quality/controls.json`, ajustables por el Owner sin tocar código. Valores propuestos:

| Riesgo | Gate 1 | Gate 2 | Gate 3 |
|---|---|---|---|
| LOW | I1 · G0 | I1 · G0 | I1 · G0 |
| MEDIUM | I1 · G1 | I1 · G1 | I1 · G1 |
| HIGH | I1 · G1 | I1 · G1 | I1 · G1 |
| CRITICAL | I2 · G2 | I2 · G2 | I2 · G2 |

Razonamiento:
- Hasta HIGH basta con agentes separados en un mismo entorno y evidencias fijadas, sin intervención del Owner.
- CRITICAL exige que el revisor no pueda escribir y una verificación por un tercero.
- Variante a decidir (D3): Gate 3 de HIGH con I2. Cuesta más, porque re-ejecutar tests exige shell, y a cambio protege los resultados frente a manipulación.

**Implicación honesta.** Los subagentes de GOV-001 serían `I1` (contexto nuevo, aunque los lanzó y les dio instrucciones el autor-Orchestrator). Su garantía sería G0 o G1 según las evidencias que se fijen. Ninguno pasa a ser «verificado».

## 2. Hashes: dos conceptos con nombre propio
| Campo | Definición | Uso | ¿Lo recalcula la CLI? |
|---|---|---|---|
| `sha256_lf` | `sha256(bytes.replace(b'\r\n', b'\n'))` | Fijar informes y evidencias; independiente de `core.autocrlf` | **Sí** |
| `sha256` (bytes originales) | `sha256(bytes)` del archivo tal como está | Citar artefactos históricos o binarios en texto humano; registros anteriores a v9 | No: es un identificador declarado |

- La CLI solo verifica `sha256_lf`. Los `sha256:` históricos (GOV-001 ciclos 1–3, propuestas) siguen siendo hashes de bytes originales y dependen del checkout (G2-13 abierto para ellos).
- Subcomando `quality_cli.py hash <ruta>`: imprime `sha256_lf` y, por separado, `sha256` con su etiqueta.

## 3. Alternativas de implementación de R03
### Alternativa A — Aditiva (schema v2, sin cambio de versión)
- Se añaden al informe las etiquetas de autoría, aislamiento y evidencias, y en el manifiesto su espejo `independence` y `evidence_sha256_lf`. Desaparece la regla del «no».
- Se mantienen R1/R4b (verificación registrada obligatoria) y todas las etiquetas Markdown actuales.
- **Consecuencias:**
  - Aumenta la duplicación: cada dato vive en el informe y en el manifiesto.
  - Se conserva el análisis de etiquetas Markdown.
  - R1/R4b siguen obligando a que alguien, en la práctica el Owner, verifique identidades en cada Gate PASS, en contra de su objetivo.
  - **Exige** cambiar `schema_version`: los requisitos nuevos invalidan cualquier v2 con PASS y cambian la semántica. No subirla sería incoherente.

### Alternativa B — Fuente única en el informe (schema v3) · **recomendada**
- **Informe.** La narrativa es libre y la CLI no la lee. Contiene **un único** bloque `protheusai-review` en JSON (biblioteca estándar):
  ```json
  {"gate": "gate2", "decision": "PASS",
   "reviewer": "quality-x",
   "artifact": {"name": "diff 29d741e..abc1234", "ref": "git:abc1234 | sha256_lf:<hex> | sha256:<hex>"},
   "effective_authors": ["dev-1"],
   "authorship_independent": true,
   "isolation": "I1_CONTEXTO_SEPARADO",
   "evidence": [{"path": "evidence/launch.log", "sha256_lf": "<hex>"}],
   "date": "AAAA-MM-DD"}
  ```
- **Manifiesto v3, por Gate:**
  - `{"decision": ..., "review": null | {"file": <ruta>, "sha256_lf": <hex>}}`.
  - Salen del manifiesto `reviewer`, `reviewed_artifact`, `evidence_file` y `date`: viven solo en el informe fijado.
  - La duplicación se reduce a `decision`, que es el registro del Orchestrator y debe ser igual a la del revisor.
- **CLI.** Valida el bloque de forma estricta: claves exactas, tipos, enumeraciones, rutas canónicas de v8 y `sha256_lf`. Después aplica:
  - A (regla absoluta);
  - B ≥ el mínimo;
  - C calculado ≥ el mínimo;
  - las reglas actuales: autores efectivos ⊆ rol, orden de Gates, FAIL trazable, PWR nunca habilita, R8 (aprobación final no por autores).
- **Controles redundantes que desaparecen:**
  - el regex de independencia y la regla del «no»;
  - el análisis de cinco etiquetas Markdown (`Revisor`, `Dictamen`, `Artefacto revisado`, `Autor efectivo`, `Independencia verificada`);
  - la detección de plantilla por texto (`**Dictamen:** PENDING` / `[IDENTIDAD REAL]`), sustituida por «bloque válido + hash»;
  - la duplicación de cuatro campos entre informe y manifiesto;
  - R1/R4b como requisito universal: la verificación por terceros solo se exige donde el riesgo pide G2;
  - la clave `identity_verification_record_required`, sustituida por la matriz de requisitos.
- **Se conserva:** las identidades de roles con sus tres niveles (C1), R2, R8, el orden de Gates, el carácter histórico de v1, la normalización `canon()` y la política append-only documental.
- **Versión del esquema:**
  - **sube a 3**;
  - v1: histórico, sin cambios;
  - v2: válido solo si todos sus Gates están en PENDING (el caso de `EXAMPLE-001` y `GOV-001`, que migran mecánicamente a v3 en este incremento); cualquier v2 con decisión distinta de PENDING → «migrar a v3»; `can-*` bloquea siempre v1 y v2.
- **Consecuencias:**
  - Diff mayor que en A, pero con un balance de líneas cercano a cero: se sustituye el análisis de etiquetas por `json.loads` y la validación del bloque.
  - Hay que reescribir las fixtures de informe de los tests.
  - Las plantillas incluyen el bloque JSON como esqueleto, algo menos cómodo de rellenar a mano.
  - Sin dependencias nuevas.

### Alternativa C — Solo eliminar la regla del «no» (descartada)
- Mínimo cambio, pero no distingue autoría, aislamiento y garantía, ni reduce la redundancia. No responde a la decisión del Owner.

## 3b. Pruebas previstas (alternativa B)
- **Positivas:**
  - Agentes con `I1` en el mismo entorno → PASS en LOW, MEDIUM y HIGH con la garantía requerida.
  - La narrativa no afecta a la validación.
  - `sha256_lf` coincide en LF y en CRLF; `hash` muestra ambos valores.
  - v2 con Gates PENDING es válido; v1 conserva su comportamiento.
  - Las plantillas rellenadas pasan la validación.
- **Negativas (cada una con control de mutación):**
  - Revisor que es autor (también Orchestrator-Developer o tras normalizar el id).
  - `authorship_independent` en `false`, ausente o no booleano.
  - `I0` con PASS o PWR.
  - Aislamiento inferior al mínimo de la matriz.
  - Garantía calculada inferior al mínimo: G1 sin evidencias; G2 sin `verification`, con `by` ∈ autores o con `by` = revisor.
  - Bloque ausente, duplicado, con JSON inválido o con claves extra o ausentes.
  - `decision` del bloque distinta de la del manifiesto.
  - `review.sha256_lf` incorrecto (informe alterado) o evidencia alterada.
  - Rutas no canónicas, que salen de la misión o que pasan por una unión de directorio.
  - v2 con PASS → migrar.
  - PWR nunca habilita.
  - R8.
  - Ningún mensaje de la CLI dice «verificado» sin calificar.
- **Inventario.** Se sustituyen los subcasos de etiquetas y prosa (`test_report_must_match_manifest`, `test_filled_templates_satisfy_report_rules` y el helper `record()`). Las demás aserciones se conservan, adaptadas a v3. Se registra el número de tests y subcasos antes y después.

## 4. GOV-R02 → GOV-002 (investigación)
- Las firmas SSH quedan como línea de investigación para atribución e integridad. **No** son un requisito universal ni una dependencia obligatoria de proyectos ordinarios.
- El diseño v9 reserva sitio sin depender de ellas: una firma futura sería un tipo más de evidencia que eleva C, sin cambiar A ni B.

## 5. Cierre de GOV-001
- Se mantiene la opción A de v8, ajustada a la matriz.
- Con HIGH (I1 · G1), GOV-001 podría cerrarse formalmente sin el Owner como verificador: tendría que revalidarse con revisores `I1` y evidencias fijadas, y que el Owner apruebe al final (R8).
- No se marca ningún Gate hasta implementar R03 y cumplir esas condiciones.

## 6. Decisiones solicitadas
- **D1:** Alternativa B (recomendada) o A.
- **D2:** niveles I0–I3 y G0–G2 y la matriz propuesta.
- **D3:** Gate 3 de HIGH en I1 (propuesto) o en I2.
- **D4:** autorizar la ejecución de R01 (`OWNER-DECISION-02`) ahora o junto con R03.
