# PROTHEUSAI-CORE · CONTEXT-001 + DET-001
## Economía de contexto y ejecución determinista

TERRA, el Owner autoriza el segundo incremento de maduración de PROTHEUSAI-CORE.

**Objetivo: reducir el consumo innecesario de contexto, las llamadas redundantes a modelos y las operaciones de coordinación que pueden resolverse mediante herramientas deterministas, conservando la autonomía y la calidad de nuestra empresa de agentes.**

Esta es una misión de implementación, no solamente de investigación.

Trabaja dentro de PROTHEUSAI-CORE bajo la gobernanza simplificada vigente.

## 1. Contexto y evidencias

Hemos observado los siguientes datos en DELIVERY-001:

- 43.966.778 tokens observados.
- 376 respuestas únicas.
- 43.288.448 tokens de entrada en caché.
- 36.115.395 tokens en la sesión principal.
- Varias respuestas superiores a 200.000 tokens durante coordinación, esperas, consultas Git y seguimiento de revisiones.

Estas cifras muestran dónde se acumuló el volumen, pero no demuestran qué proporción era evitable ni su coste monetario real.

MET-001 ya está disponible en CORE y debe utilizarse para medir las mejoras.

**No confundas tokens procesados, tokens nuevos, caché y coste facturado.**

## 2. Principios obligatorios

Aplica estas decisiones del Owner:

1. La inteligencia de PROTHEUSAI debe pertenecer a su metodología y a sus agentes especializados, no a una conversación interminable.
2. El conocimiento duradero debe persistir fuera del contexto temporal de los modelos.
3. Los agentes deben recuperar únicamente la información necesaria para cada tarea.
4. Las herramientas deterministas tienen prioridad cuando pueden resolver una operación de manera fiable.
5. Quality conserva independencia funcional, capacidad de FAIL y acceso a las evidencias originales.
6. PROTHEUSAI utiliza las capacidades nativas del runner: sesiones, permisos, subagentes y herramientas disponibles.
7. No debe duplicar funcionalidades que Codex, Claude Code u otros entornos ya proporcionan.
8. MCP Memory es una integración externa opcional. La elección, instalación y mantenimiento corresponden al Owner o responsable técnico.
9. No se desarrollará un servidor MCP Memory propio.
10. No se crearán nuevos Gates ni requisitos administrativos de identidad o aislamiento.

**El objetivo no es reducir el número de especialistas, sino reducir el coste de coordinarlos y utilizarlos.**

## 3. Primera fase — Diagnóstico técnico acotado

Antes de implementar, investiga las capacidades reales del runner disponible.

Determina:

- Cómo se construye y acumula el contexto de la sesión principal.
- Qué mecanismos nativos existen para compactación, renovación o continuación mediante nuevas sesiones.
- Qué capacidades ofrecen las herramientas de delegación y recuperación de contexto.
- Qué información se transmite realmente a los agentes especializados.
- Qué mecanismos permiten conservar y recuperar el estado de una misión.
- Qué operaciones rutinarias se ejecutan actualmente mediante razonamiento LLM.
- Qué puede observar MET-001 y qué no puede atribuir.

No presupongas que escribir un resumen elimina el contexto ya acumulado.

No atribuyas capacidades al runner sin comprobarlas.

Evita investigaciones extensas de herramientas o proveedores que no utilizaremos en este incremento.

Entrega internamente un diagnóstico compacto y pasa a implementar las mejoras viables.

## 4. CONTEXT-001 — Gestión eficiente del contexto

### 4.1. Estado operativo persistente

Evalúa una bitácora o checkpoint por misión que contenga exclusivamente:

- Identificador y objetivo de la misión.
- Estado vigente.
- Decisiones del Owner aplicables.
- Tareas completadas y pendientes.
- Agentes o trabajos todavía activos.
- Versión Git relevante.
- Referencias a contratos y evidencias.
- Bloqueos y próxima acción.

La bitácora NO debe duplicar informes completos ni convertirse en otra fuente de verdad.

Los documentos, commits, dictámenes y decisiones originales conservan su autoridad.

Si implementas un checkpoint, utiliza inicialmente archivos locales sencillos, legibles y verificables.

No introduzcas bases de datos, embeddings, búsqueda vectorial ni servicios adicionales sin una necesidad demostrada.

### 4.2. Recuperación selectiva

Implementa o ajusta el mecanismo mínimo para que TERRA:

- Consulte primero el estado operativo compacto.
- Recupere archivos originales bajo demanda.
- Utilice rutas, referencias, versiones y hashes cuando sean suficientes.
- Evite transmitir el historial completo a los especialistas.
- Excluya por defecto expedientes históricos ajenos a la misión actual.
- Permita a Quality consultar directamente las fuentes originales.

No ocultes información necesaria para verificar una decisión.

### 4.3. Renovación de sesiones

Comprueba si el runner permite continuar una misión desde un contexto nuevo o compactado, conservando referencias a las operaciones pendientes.

Si resulta viable, implementa el mecanismo más pequeño que permita una transferencia segura del estado.

Nunca abandones una operación activa o un subagente pendiente sin registrar su situación.

Si la renovación no puede automatizarse de forma fiable, no simules que funciona: proporciona un procedimiento de transferencia verificable y documenta la limitación.

No construyas un administrador de sesiones propio si el runner ya dispone de capacidades suficientes.

## 5. DET-001 — Determinismo antes que razonamiento

Identifica las operaciones recurrentes de TERRA que puedan ejecutarse mediante código convencional.

Prioriza casos observados, como:

- Cálculo y comparación de hashes.
- Validación de manifiestos.
- Inventarios de archivos.
- Comparación de versiones y cambios.
- Consulta compacta de estado Git.
- Agregación de métricas.
- Verificación estructural de contratos.
- Preparación de referencias para Quality.
- Comprobación de resultados de herramientas.
- Reducción de consultas repetidas de estado y espera.

Reutiliza los scripts existentes.

Implementa solamente automatizaciones pequeñas que:

1. Resuelvan una necesidad repetida y comprobada.
2. Sean deterministas.
3. Tengan pruebas.
4. Sean más fáciles de mantener que la operación manual.
5. No debiliten la trazabilidad ni las verificaciones técnicas.

**No conviertas DET-001 en un framework de herramientas.**

Si una operación no necesita automatización nueva, utiliza la herramienta existente.

## 6. Experimento de eficiencia

Diseña una comparación pequeña y reproducible.

Compara, cuando sea viable:

**A. Procedimiento actual**
- Sesión continua o mecanismo habitual.
- Contexto y delegación convencionales.

**B. Procedimiento optimizado**
- Estado operativo compacto.
- Recuperación selectiva.
- Renovación de contexto si está soportada.
- Herramientas deterministas.

Utiliza tareas equivalentes, entradas comparables y criterios de calidad idénticos.

No desarrolles otro MVP completo.

Mide con MET-001:

- Tokens totales.
- Entrada en caché.
- Entrada no contabilizada como caché.
- Salida.
- Respuestas y delegaciones.
- Tiempo observado.
- Consultas y lecturas repetidas, si se pueden identificar.
- Correcciones y resultados de Quality.

Calcula costes hipotéticos solamente con tarifas verificadas y aplicables.

No inventes ahorros ni supongas que la reducción de tokens implica una reducción proporcional del coste.

Si no es posible construir una comparación controlada, proporciona una evaluación parcial honesta y conserva las limitaciones.

## 7. Criterios de calidad

Las mejoras deben demostrar que no se pierden:

- Decisiones vigentes del Owner.
- Requisitos técnicos.
- Referencias a evidencias.
- Estado de agentes y operaciones pendientes.
- Capacidad de revisión independiente.
- Reproducibilidad de las comprobaciones.

Una nueva sesión debe poder recuperar el estado correcto de la misión y continuar sin reconstruir toda la conversación.

Quality debe verificar los cambios funcionales y comprobar que la compactación o recuperación no altera decisiones ni referencias críticas.

Las pruebas deben ser proporcionales al alcance.

No conviertas esta intervención en una nueva investigación de I1/G1 o de las anclas históricas.

## 8. Límites

No modificar APP-004 ni otros productos.

No iniciar APP-005.

No implementar DESIGN-001.

No desarrollar un servidor MCP.

No imponer un MCP específico.

No crear un motor de orquestación paralelo al runner.

No introducir nuevos Gates.

No reconstruir la gobernanza histórica.

No realizar limpiezas destructivas.

No instalar servicios o dependencias innecesarias.

No hacer despliegues ni publicaciones.

El Owner autoriza las decisiones técnicas ordinarias dentro de este alcance; respeta los permisos reales del entorno.

## 9. Implementación incremental

Trabaja en incrementos pequeños:

1. Identifica la oportunidad de mayor impacto verificable.
2. Implementa la corrección mínima.
3. Ejecuta pruebas.
4. Solicita revisión técnica de Quality.
5. Corrige los defectos reales.
6. Mide el resultado.
7. Continúa únicamente si existe una segunda mejora claramente justificada.

Evita abrir múltiples frentes.

No prolongues la investigación cuando la evidencia disponible ya permite tomar una decisión técnica.

## 10. Entregables

Al finalizar presenta:

1. Diagnóstico de las causas observables del consumo.
2. Capacidades reales del runner para renovación y recuperación.
3. Mejoras de contexto implementadas.
4. Automatizaciones deterministas incorporadas o reutilizadas.
5. Resultado de la prueba de continuidad entre sesiones, si es viable.
6. Comparación de métricas antes y después, con limitaciones.
7. Dictamen de Quality.
8. Archivos modificados.
9. Pruebas ejecutadas y omitidas.
10. Commits y estado Git.

Mantén la documentación compacta y orientada al uso real.

## Condición de éxito

CONTEXT-001 + DET-001 debe conseguir al menos una mejora de eficiencia implementada y verificada, manteniendo la calidad y la continuidad operativa.

Si la medición no demuestra ahorro, informa el resultado sin maquillarlo.

No declares completada una renovación de contexto que no hayas comprobado.

**El objetivo de PROTHEUSAI es funcionar como una empresa de ingeniería profesional, con especialistas adecuados al encargo y una coordinación eficiente.**

No queremos que TERRA tenga que recordar dos galaxias de conversación para saber qué debe hacer.

Queremos que pueda recuperar el conocimiento necesario, razonar, ejecutar y continuar trabajando.

**El Owner autoriza. TERRA ejecuta. Quality verifica. El Owner acepta.**

Procede.