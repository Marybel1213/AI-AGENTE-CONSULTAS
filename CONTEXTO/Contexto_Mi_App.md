DOCUMENTO DE CONTEXTO · ChatbotTH
1. Qué es esta app (para quién y qué problema resuelve)
Propósito: Esta aplicación web es un asistente conversacional (chatbot) inteligente diseñado para que los Jefes de área de la organización realicen consultas operativas e institucionales de manera directa e inmediata.
Problema a resolver: Actualmente, las consultas son atendidas manualmente por el Consultor de Talento Humano, lo que genera cuellos de botella y consume un alto volumen de tiempo operativo. La solución busca automatizar la atención de dudas recurrentes mediante la lectura acelerada de fuentes oficiales, reduciendo significativamente los tiempos de respuesta.
2. El proceso hoy (paso a paso, tiempo que toma, quién lo hace)
Responsable actual: Consultor de Talento Humano.
Tiempo requerido: Aproximadamente 3 horas diarias dedicadas a resolver dudas de los jefes.
Flujo actual paso a paso: 1) El Jefe de área envía una inquietud al Consultor de Talento Humano.
2) El Consultor busca manualmente la norma o procedimiento en archivos y manuales.
3) El Consultor redacta y envía la respuesta por correo o mensaje.
3. Datos de entrada

### Tabla 1

| Archivo / Dato | Formato | Campos / Contenido | Ejemplo |
| --- | --- | --- | --- |
| Manuales y Guías | PDF / Word / Excel | Texto normativo, procedimientos de TH | Manual de Beneficios 2026.pdf |
| Bases del Centro de Expertis | Excel / Tablas | Estructura salarial, procedimientos | Matriz_Politicas_TH.xlsx |
| Pregunta del Jefe | Texto plano | Inquietud en lenguaje natural | ¿Cuántos días de licencia corresponden por matrimonio? |

4. Reglas de negocio para el código
R1: El sistema debe recibir preguntas en lenguaje natural a través de una interfaz de chat web.
R2: El código debe gestionar el flujo de la conversación y enviar la consulta junto con los documentos de referencia al modelo de IA.
R3: El sistema debe registrar el historial de interacciones de la sesión para mantener el contexto de la conversación.
R4: Si se detecta un error de archivo ilegible, el código debe interceptar la falla y mostrar la notificación correspondiente sin colapsar.
5. Lo que hace el agente de IA
Rol del Agente: Asistente Experto en Normativa de Talento Humano.
Entradas recibidas: Recibe la pregunta en texto ingresada por el Jefe y los fragmentos de documentos relevantes del repositorio oficial de TH.
Comportamiento: Analiza la información, redacta la respuesta formal y extrae la cita exacta del documento fuente. REGLA ESTRICTA: El agente NUNCA inventa información. Si la respuesta no figura en los documentos, escribe 'no indicado'.
Contrato de Salida JSON:

### Tabla 2

| Llave (Key) | Tipo de Dato | Qué significa |
| --- | --- | --- |
| respuesta | string | Redacción clara, directa y formal de la solución a la pregunta. |
| cita_fuente | string | Nombre del documento, sección o página de donde se obtuvo la respuesta. |
| estado_encontrado | boolean | True si la respuesta está en los documentos; False si no aparece ('no indicado'). |

6. Qué produce la app
Interfaz visual: Pantalla principal tipo Chatbot limpia y responsiva en español.
Componentes: Caja de texto para ingresar preguntas, botón de 'Enviar' y botón de 'Nueva conversación'.
Visualización de resultados: Burbuja de texto con la respuesta formal redactada y un recuadro destacado de 'Fuente / Cita de Referencia'.
7. Quién decide
Usuarios finales: Los Jefes de área de la empresa utilizan la herramienta de forma cotidiana.
Validador final: El Consultor de Talento Humano evaluará y validará la herramienta frente al banco de pruebas para otorgar la aprobación final de paso a producción.
8. Datos de prueba que hay que generar
Banco de Calibración: Banco de 10 preguntas y respuestas oficiales preparado por el Consultor de TH.
Documento de Referencia: Documento PDF de pruebas que contenga políticas reales de vacaciones, licencias, permisos e incentivos corporativos.
9. Cifras de control
Criterio de éxito: 10 de 10 (100%) respuestas correctas y adecuadamente citadas según el banco de prueba del Consultor de Talento Humano para autorizar la salida a producción.
10. Casos límite
Pregunta confusa o en otro idioma: Mostrar mensaje formal solicitando al usuario que reformule o detalle su pregunta de forma clara y respetuosa.
Información no encontrada en manuales: Devolver el estado 'no indicado' y mostrar en pantalla un mensaje automático derivando la consulta directamente con el Consultor de Talento Humano.
Archivo borroso o ilegible: Mostrar notificación indicando que el archivo de origen no se puede leer o está corrupto.
11. Reglas del sistema
Arquitectura y Lenguaje: Desarrollo en Python utilizando el framework Flask.
Estructura del Proyecto: Patrón de diseño MVC (Modelo-Vista-Controlador) gestionado exclusivamente mediante la herramienta `uv`.
Seguridad de Credenciales: La API key del agente debe residir de forma obligatoria en el archivo `.env` y NUNCA estar quemada (hardcoded) en el código.
Despliegue Local: Se debe incluir un script ejecutable `iniciar_app.bat` para encender el servidor y la aplicación con un solo clic.
Interfaz de Usuario: Pantallas sencillas, limpias y 100% en español.
Restricción de Desarrollo: Queda estrictamente prohibido inventar reglas de negocio, lógica o campos que no estén explícitamente detallados en este documento.
12. Supuestos por confirmar
S1: Estructura detallada de columnas de las bases en Excel generadas por los centros de expertis.
S2: Mecanismo de actualización periódica de los manuales en el repositorio del chatbot.