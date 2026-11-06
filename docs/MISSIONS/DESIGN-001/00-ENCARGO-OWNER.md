# PROTHEUSAI-CORE · DESIGN-001
## Incorporación del Director Creativo a nuestra empresa de agentes

TERRA, el Owner autoriza implementar DESIGN-001 en PROTHEUSAI-CORE.

**Objetivo:** incorporar un Director Creativo como especialista convocable, capaz de interpretar los requisitos visuales y de experiencia de usuario de un producto, establecer una dirección de diseño coherente y colaborar con los demás agentes durante su desarrollo y evolución.

Esta mejora está aprobada conceptualmente por el Owner. Tu misión es implementarla, integrarla y verificar su funcionamiento.

Trabaja bajo la gobernanza simplificada vigente, utilizando los permisos nativos del runner.

## 1. Visión del Owner

PROTHEUSAI es una empresa de desarrollo de software operada mediante agentes especializados, no simplemente un generador de código.

El equipo debe adaptarse al tipo de producto, su madurez, el valor que busca el cliente y sus riesgos.

Por tanto:

- El Director Creativo forma parte de las competencias disponibles de la empresa.
- TERRA decide cuándo convocarlo según las necesidades de la misión.
- No será obligatorio para proyectos sin interfaz significativa.
- Debe participar preferentemente antes de la implementación visual.
- Puede volver a intervenir durante la evolución de un producto existente.
- No sustituye a Architect, Developer ni Quality.
- No introduce nuevos Gates ni autorizaciones administrativas.

**El Director Creativo debe influir en lo que construimos, no limitarse a decorar lo que Developer ya construyó.**

## 2. Inspección y reutilización

Antes de implementar:

1. Examina la estructura vigente de agentes, skills, Discovery y contratos de CORE.
2. Lee la propuesta existente `docs/DESIGN-001-PROPUESTA.md`.
3. Identifica los mecanismos actuales de convocatoria y delegación del runner.
4. Comprueba qué skills de diseño y frontend existen y cuáles pueden reutilizarse.
5. Identifica los puntos mínimos de integración con el proceso actual.

No reconstruyas capacidades existentes.

No instales una infraestructura externa de diseño ni un nuevo sistema de agentes.

Mantén la implementación portable entre runners siempre que sus capacidades lo permitan.

## 3. Contrato del Director Creativo

Implementa un contrato operativo compacto que defina claramente sus responsabilidades.

### Interpretación creativa

El agente deberá:

- Comprender el propósito del producto.
- Identificar el público objetivo y sus necesidades.
- Interpretar referencias visuales proporcionadas por el cliente.
- Traducir conceptos como minimalista, elegante, industrial, moderno o intuitivo en decisiones de diseño concretas.
- Proponer una dirección visual coherente con el contexto y el alcance autorizado.

No deberá convertir preferencias vagas en requisitos supuestamente aprobados.

### Diseño UX/UI

Deberá poder trabajar sobre:

- Arquitectura de información.
- Flujos de usuario.
- Jerarquía visual.
- Composición y distribución.
- Tipografía y color.
- Componentes y estados de interfaz.
- Diseño responsive y mobile-first.
- Accesibilidad desde la concepción.
- Coherencia visual entre distintas pantallas.

Su profundidad de trabajo debe ajustarse al producto. Una pequeña herramienta interna no necesita el mismo esfuerzo de diseño que una aplicación comercial orientada al consumidor.

### Propuestas visuales

Cuando sea útil y esté disponible la capacidad correspondiente, podrá proponer:

- Referencias visuales.
- Wireframes.
- Mockups.
- Sistemas visuales ligeros.
- Especificaciones de componentes.
- Recomendaciones UX.

No deben generarse estos artefactos obligatoriamente en todas las misiones.

Las imágenes generadas o referencias externas deberán identificarse correctamente. No presentar mockups como capturas de implementaciones reales ni reutilizar materiales sin considerar sus derechos.

### Revisión creativa

Durante la implementación podrá comprobar la correspondencia entre la dirección visual acordada y la interfaz construida.

Debe identificar problemas concretos y proponer correcciones accionables.

No debe emitir dictámenes de Quality ni asumir la aceptación final del Owner.

## 4. Integración entre agentes

Define e implementa la colaboración con los roles existentes.

**TERRA**
- Evalúa la necesidad del especialista.
- Lo convoca con un encargo delimitado.
- Coordina sus resultados con los demás agentes.
- Evita convocatorias redundantes.

**Discovery**
- Recoge la intención del cliente.
- Identifica necesidades visuales relevantes.
- Solicita referencias únicamente cuando aporten valor.
- No convierte Discovery en un cuestionario interminable.

**Architect**
- Contrasta la propuesta UX con las restricciones técnicas.
- Mantiene la responsabilidad sobre la arquitectura del software.

**Creative Director**
- Define la experiencia y dirección visual.
- Propone decisiones de diseño que puedan implementarse.
- Mantiene coherencia entre requisitos y resultados.

**Developer**
- Implementa la experiencia acordada.
- Consulta al Director Creativo cuando hay ambigüedades relevantes.
- No necesita esperar una aprobación creativa para cada detalle menor.

**Quality**
- Verifica criterios comprobables de interfaz, requisitos, accesibilidad y funcionamiento.
- Conserva su capacidad de FAIL por defectos reales.
- No confunde preferencias estéticas subjetivas con errores técnicos.

**Owner**
- Define la visión.
- Decide sobre alternativas visuales importantes cuando sea necesario.
- Evalúa el producto y acepta el release.

No añadas otro Gate ni un circuito paralelo de aprobación visual.

## 5. Composición adaptativa del equipo

El Director Creativo debe convocarse por necesidad, no por formalidad.

Implementa criterios sencillos para orientar a TERRA.

Ejemplos:

**Caso A: aplicación comercial con interfaz importante**
Director Creativo recomendado desde Discovery o diseño inicial.

**Caso B: API, biblioteca o herramienta CLI sin interfaz significativa**
No convocarlo por defecto.

**Caso C: evolución visual de un producto existente**
Convocarlo para analizar los cambios y conservar la identidad visual anterior cuando corresponda.

**Caso D: cambio técnico sin impacto UX**
No convocarlo.

Estos criterios son orientaciones operativas, no una matriz burocrática obligatoria.

TERRA debe poder justificar brevemente sus decisiones y adaptarlas al contexto.

## 6. Skills especializados

Integra la capacidad de seleccionar skills de diseño cuando estén disponibles y sean relevantes.

Ámbitos posibles:

- UX research.
- UI design.
- Design systems.
- Frontend visual.
- Responsive design.
- Accesibilidad.
- Prototipado.
- Crítica visual.

Prioriza skills existentes y compatibles.

No desarrolles ahora una biblioteca gigantesca de skills ni instales herramientas sin necesidad.

Los skills deben ampliar las capacidades del Director Creativo, no convertirse en agentes adicionales por defecto.

## 7. Entregables creativos compactos

El resultado habitual del Director Creativo debe ser suficientemente concreto para orientar a Developer.

Propongo un contrato mínimo:

1. Intención de experiencia.
2. Dirección visual.
3. Flujos y componentes relevantes.
4. Comportamiento responsive y accesibilidad.
5. Decisiones confirmadas y supuestos pendientes.
6. Criterios verificables de implementación.
7. Referencias a artefactos, cuando existan.

No impongas extensiones fijas ni produzcas documentación ceremonial.

La información que Developer necesita debe poder consultarse directamente, sin transmitirle la conversación completa del Director Creativo.

Aplica los principios de comunicación compacta de CONTEXT-OPT-001. Conserva el detalle original cuando sea necesario.

## 8. Pruebas de integración

No construyas un MVP completo para probar DESIGN-001.

Realiza comprobaciones pequeñas y representativas.

### Escenario 1 — Producto con interfaz significativa

Entrada: una descripción breve de una aplicación comercial con preferencias visuales.

Verificar que:
- TERRA reconoce la necesidad creativa.
- Convoca correctamente al especialista.
- El Director Creativo produce decisiones UX/UI aplicables.
- Developer puede interpretar esas decisiones.
- Quality conserva sus responsabilidades.

### Escenario 2 — Proyecto sin interfaz

Entrada: una biblioteca técnica o herramienta CLI.

Verificar que:
- TERRA no convoca innecesariamente al Director Creativo.
- La ausencia del especialista no bloquea el proyecto.

### Escenario 3 — Evolución visual

Entrada: una modificación visual solicitada sobre un producto ya existente.

Verificar que:
- El Director Creativo considera el diseño y las decisiones anteriores.
- Propone una evolución coherente.
- No exige reconstruir el producto ni repetir Discovery desde cero.

Usa datos y proyectos ficticios mínimos.

Comprueba la integración real con los mecanismos de delegación disponibles; no te limites a verificar que los archivos de instrucciones existen.

Si alguna capacidad del runner impide demostrar una convocatoria, declara la limitación.

## 9. Calidad y autonomía

Quality debe revisar:

- Integridad del contrato del nuevo rol.
- Ausencia de conflictos de responsabilidad.
- Convocatoria correcta y omisión correcta según el tipo de proyecto.
- Utilidad y verificabilidad de las salidas.
- No regresión de contratos existentes.
- Conservación del flujo de autorización del Owner.

Corrige defectos técnicos encontrados.

No exijas I1/G1 como certificaciones obligatorias.

No abras nuevos Gates.

Las decisiones técnicas ordinarias están autorizadas dentro de este mandato.

## 10. Economía y métricas

Esta será nuestra primera misión funcional desarrollada con las mejoras de comunicación de CONTEXT-OPT-001.

Utiliza MET-001 desde el inicio cuando sea posible.

Observa:
- Tokens de entrada y caché.
- Tokens de salida.
- Respuestas y delegaciones.
- Tamaño de los informes de especialistas.
- Saltos de contexto asociados a herramientas y esperas.
- Tiempo.
- Correcciones.
- Recuperaciones de informes completos.

Utiliza como referencia histórica los resultados de CONTEXT-001, sin afirmar causalidad entre tareas distintas.

No conviertas DESIGN-001 en un nuevo laboratorio A/B.

La función principal de esta misión es incorporar el Director Creativo. La medición es secundaria y no debe bloquear la implementación si los registros no permiten una atribución fiable.

## 11. Límites

- No modificar APP-004 ni otros productos.
- No iniciar APP-005.
- No implementar otro sistema de memoria.
- No imponer MCP Memory.
- No desarrollar un nuevo orquestador.
- No duplicar permisos del runner.
- No crear nuevos Gates.
- No reabrir misiones históricas.
- No añadir roles que el Owner no haya solicitado.
- No publicar ni desplegar aplicaciones.
- No realizar cambios destructivos fuera del alcance.

Conserva la gobernanza simplificada y los mecanismos de Quality vigentes.

## 12. Entrega final

Al finalizar presenta:

1. Director Creativo integrado en CORE.
2. Contrato del agente y archivos modificados.
3. Condiciones de convocatoria.
4. Integración con Discovery, Architect, Developer y Quality.
5. Skills disponibles o recomendados.
6. Resultados de los tres escenarios de prueba.
7. Dictamen técnico de Quality.
8. Limitaciones demostradas.
9. Métricas de consumo disponibles.
10. Commits y estado Git.

Verifica que BOOTSTRAP-001 conserve los componentes necesarios para que un nuevo proyecto pueda utilizar el Director Creativo. Actualiza su lista positiva si corresponde y comprueba que el cambio no arrastra expedientes históricos.

No declares aceptación del Owner antes de recibirla.

## Criterio de éxito

**PROTHEUSAI dispone de un Director Creativo que participa cuando aporta valor, ayuda a definir una experiencia coherente antes de programarla y facilita su implementación sin añadir burocracia ni coordinación innecesaria.**

El objetivo no es producir documentos bonitos.

El objetivo es que nuestros futuros productos nazcan mejor concebidos, visualmente coherentes y orientados a las personas que los utilizarán.

**El Owner define la visión. TERRA organiza la empresa. El Director Creativo diseña la experiencia. Developer implementa. Quality verifica. El Owner acepta.**

Implementa DESIGN-001 con autonomía dentro de este alcance.