# AGENTS.md

## Qué es esta app

Aplicación web tipo chatbot inteligente para que los Jefes de área de la organización realicen consultas operativas e institucionales de Talento Humano (TH) de manera directa e inmediata. Resuelve el problema de que actualmente el Consultor de Talento Humano atiende las consultas manualmente, lo que genera cuellos de botella y consume aproximadamente 3 horas diarias. La solución automatiza la atención de dudas recurrentes mediante la lectura acelerada de fuentes oficiales, reduciendo los tiempos de respuesta.

Público objetivo: Jefes de área de la empresa.
Validador final: Consultor de Talento Humano (aprueba el paso a producción tras validar contra el banco de pruebas).

## Datos de entrada

### Archivos de insumos actuales (MVP)

Solo existe un archivo en la carpeta `INSUMOS`:

**`INSUMOS\Banco de Preguntas y Respuestas RRHH.xlsx`**
- 1 hoja: `Banco de Preguntas`
- 15 filas totales × 5 columnas
- Filas 1-2: título y descripción del banco (metadatos, no datos estructurados)
- Filas 3-4: metadatos del banco (Total Preguntas: 10; Categorías Activas: 1; Población Objetivo: Supervisores y Jefes de Planta; Módulos Clave: Nómina, Desempeño, Vacaciones, SST; Estado del Banco: Listo para Entrenamiento)
- Fila 5 — encabezados de datos:
  - `ID`
  - `Categoría`
  - `Pregunta Frecuente`
  - `Respuesta Sugerida/Ficticia`
  - `Palabras Clave / Keywords`
- Filas 6-15: 10 registros (FAQ-001 a FAQ-010) con preguntas sobre nómina/horas extras, gestión de rendimiento, vacaciones y permisos, seguridad/SST/onboarding.

### Entradas del usuario

- Pregunta del Jefe: texto plano en lenguaje natural ingresado por el usuario a través de la interfaz de chat web.
  Ejemplo del contexto: "¿Cuántos días de licencia corresponden por matrimonio?"

### Archivos mencionados en el contexto que NO están todavía en insumos (pendientes de agregar post-MVP)

El contexto menciona como ejemplos de entrada:
- `Manual de Beneficios 2026.pdf` (Manuales y Guías) — no existe en `INSUMOS` todavía.
- `Matriz_Politicas_TH.xlsx` (Bases del Centro de Expertis) — no existe en `INSUMOS` todavía.

El usuario confirmó que por ahora solo el Excel es insumo y que los manuales se agregarán después.

## Reglas de negocio (código, sin IA)

Estas reglas las implementa el código de la aplicación, no el agente de IA:

- R1: El sistema debe recibir preguntas en lenguaje natural a través de una interfaz de chat web.
- R2: El código debe gestionar el flujo de la conversación y enviar la consulta junto con los documentos de referencia al modelo de IA.
- R3: El sistema debe registrar el historial de interacciones de la sesión para mantener el contexto de la conversación.
- R4: Si se detecta un error de archivo ilegible, el código debe interceptar la falla y mostrar la notificación correspondiente sin colapsar.

## Lo que hace el agente de IA

Rol: Asistente Experto en Normativa de Talento Humano.

Entradas recibidas: la pregunta en texto ingresada por el Jefe y los fragmentos de documentos relevantes del repositorio oficial de TH.

Comportamiento: analiza la información, redacta la respuesta formal y extrae la cita exacta del documento fuente.

Regla estricta: el agente NUNCA inventa información. Si la respuesta no figura en los documentos, escribe "no indicado".

### Contrato de salida JSON

| Llave (Key) | Tipo de Dato | Qué significa |
|---|---|---|
| `respuesta` | string | Redacción clara, directa y formal de la solución a la pregunta. |
| `cita_fuente` | string | Nombre del documento, sección o página de donde se obtuvo la respuesta. |
| `estado_encontrado` | boolean | `true` si la respuesta está en los documentos; `false` si no aparece ("no indicado"). |

## Qué produce la app

- Interfaz visual: pantalla principal tipo chatbot limpia y responsiva en español.
- Componentes: caja de texto para ingresar preguntas, botón de "Enviar" y botón de "Nueva conversación".
- Visualización de resultados: burbuja de texto con la respuesta formal redactada y un recuadro destacado de "Fuente / Cita de Referencia".

## Quién decide

- Usuarios finales: los Jefes de área de la empresa utilizan la herramienta de forma cotidiana.
- Validador final: el Consultor de Talento Humano evalúa y valida la herramienta frente al banco de pruebas para otorgar la aprobación final de paso a producción.

## Cifras de control

- Criterio de éxito: 10 de 10 (100%) respuestas correctas y adecuadamente citadas según el banco de prueba del Consultor de Talento Humano para autorizar la salida a producción.

## Casos límite

- Pregunta confusa o en otro idioma: mostrar mensaje formal solicitando al usuario que reformule o detalle su pregunta de forma clara y respetuosa.
- Información no encontrada en manuales: devolver el estado "no indicado" y mostrar en pantalla un mensaje automático derivando la consulta directamente con el Consultor de Talento Humano.
- Archivo borroso o ilegible: mostrar notificación indicando que el archivo de origen no se puede leer o está corrupto.

## Reglas del sistema

- Arquitectura y Lenguaje: desarrollo en Python utilizando el framework Flask.
- Estructura del Proyecto: patrón de diseño MVC (Modelo-Vista-Controlador) gestionado exclusivamente mediante la herramienta `uv`.
- Seguridad de credenciales: la API key del agente debe residir de forma obligatoria en el archivo `.env` y NUNCA estar quemada (hardcoded) en el código.
- Despliegue local: se debe incluir un script ejecutable `iniciar_app.bat` para encender el servidor y la aplicación con un solo clic.
- Interfaz de Usuario: pantallas sencillas, limpias y 100% en español.
- Restricción de Desarrollo: queda estrictamente prohibido inventar reglas de negocio, lógica o campos que no estén explícitamente detallados en este documento.

## Supuestos por confirmar (pendientes)

- S1: Estructura detallada de columnas de las bases en Excel generadas por los centros de expertis.
- S2: Mecanismo de actualización periódica de los manuales en el repositorio del chatbot.
