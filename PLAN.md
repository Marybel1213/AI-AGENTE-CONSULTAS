# PLAN.md

## 1. RESUMEN

Vamos a construir una aplicación web tipo chatbot en español para que los Jefes de área realicen consultas operativas e institucionales de Talento Humano (TH) de manera directa e inmediata. Entra una pregunta en lenguaje natural del Jefe y, como único insumo de MVP, el archivo Excel `Banco de Preguntas y Respuestas RRHH.xlsx` con 10 preguntas frecuentes y sus respuestas. El agente de IA actúa como Asistente Experto en Normativa de TH, analiza la información, redacta la respuesta formal y devuelve un JSON con `respuesta`, `cita_fuente` y `estado_encontrado`. Sale una pantalla de chat con la respuesta y un recuadro de "Fuente / Cita de Referencia".

---

## 2. LO QUE ENCONTRÉ

### En la carpeta CONTEXTO

Archivo: `DOCUMENTO_DE_CONTEXTO_ChatbotTH.docx` (convertido a `Contexto_Mi_App.md`).
Contiene: propósito del app, proceso actual, datos de entrada (ejemplos de archivos PDF/Word/Excel que aún no existen), 4 reglas de negocio (R1-R4), rol del agente de IA, contrato de salida JSON, qué produce la app, quién decide, cifras de control (10/10), casos límite, reglas del sistema (Flask, MVC, `uv`, `.env`, `iniciar_app.bat`, español) y 2 supuestos por confirmar (S1, S2).

### En la carpeta INSUMOS

Archivo: `Banco de Preguntas y Respuestas RRHH.xlsx`.
- 1 hoja: `Banco de Preguntas`
- 15 filas totales × 5 columnas
- Filas 1-2: título y descripción (metadatos)
- Filas 3-4: metadatos del banco (10 preguntas, 1 categoría, población: Supervisores y Jefes de Planta, módulos: Nómina/Desempeño/Vacaciones/SST, estado: Listo para Entrenamiento)
- Fila 5 — encabezados: `ID`, `Categoría`, `Pregunta Frecuente`, `Respuesta Sugerida/Ficticia`, `Palabras Clave / Keywords`
- Filas 6-15: 10 registros (FAQ-001 a FAQ-010) sobre nómina/horas extras, gestión de rendimiento, vacaciones y permisos, seguridad/SST/onboarding.

### ¿Coincide con AGENTS.md?

Sí, AGENTS.md describe exactamente este único archivo de insumos para el MVP y confirma que los manuales PDF/Excel mencionados en el contexto (`Manual de Beneficios 2026.pdf`, `Matriz_Politicas_TH.xlsx`) se agregarán después.

### Qué falta o no cuadra

- Falta `Manual de Beneficios 2026.pdf` (Manuales y Guías) — pendiente post-MVP.
- Falta `Matriz_Politicas_TH.xlsx` (Bases del Centro de Expertis) — pendiente post-MVP.
- S1 y S2 están marcados como supuestos por confirmar en AGENTS.md.

---

## 3. ENTREGAS POR SUBAGENTE

Orden de ejecución: cada entrega debe ser pequeña, verificable en pocos minutos, y la salida de una es la entrada de la siguiente.

| N° | Responsable | Qué debe entregar | Archivos que crea o modifica | Qué recibe de la entrega anterior | Cómo se verifica en pantalla |
|----|-------------|-------------------|------------------------------|-----------------------------------|------------------------------|
| 1 | @backend | Estructura base del proyecto Flask con `uv`: `pyproject.toml`, `app/__init__.py` con `create_app()`, `wsgi.py`, `.env` ejemplo (sin llave real), `iniciar_app.bat` que enciende el servidor y abre el navegador. | `pyproject.toml`, `app/__init__.py`, `wsgi.py`, `.env.example`, `iniciar_app.bat` | AGENTS.md y contexto leídos. | Ejecutar `iniciar_app.bat` y ver que el navegador abre y muestra una página en blanco o de bienvenida de Flask. |
| 2 | @backend | Lectura del insumo Excel: servicio que lea `INSUMOS\Banco de Preguntas y Respuestas RRHH.xlsx`, extraiga encabezados (`ID`, `Categoría`, `Pregunta Frecuente`, `Respuesta Sugerida/Ficticia`, `Palabras Clave / Keywords`) y los 10 registros (FAQ-001 a FAQ-010). | `app/services/insumos_service.py` (nuevo) | Estructura base del backend (entrega 1). | Ejecutar el servicio y ver por consola/print los 10 registros con sus 5 columnas. |
| 3 | @backend | Regla R1: endpoint de chat web que reciba una pregunta en lenguaje natural por POST y devuelva respuesta. | `app/controllers/chat_controller.py` (nuevo), ruta en `app/__init__.py` | Insumos leídos (entrega 2). | Enviar una pregunta por Postman/curl y ver respuesta HTTP 200 con texto. |
| 4 | @backend | Reglas R2 y R3: gestionar flujo de conversación, enviar consulta + fragmentos al agente de IA, registrar historial de sesión. | `app/services/conversation_service.py` (nuevo) | Endpoint R1 (entrega 3). | Enviar 2 preguntas seguidas y ver que el historial se conserva (segunda respuesta referencia la primera). |
| 5 | @backend | Regla R4: interceptar error de archivo ilegible y mostrar notificación sin colapsar. | `app/services/error_service.py` (nuevo) | R2/R3 (entrega 4). | Forzar lectura de archivo inexistente/corrupto y ver mensaje de error controlado, sin que la app se cierre. |
| 6 | @backend | Integración del agente de IA con **Gemini**: leer API key de `.env` (placeholder, se agrega después), enviar consulta al modelo, respetar contrato JSON (`respuesta`, `cita_fuente`, `estado_encontrado`), regla de "no indicado" si no se encuentra. | `app/services/ia_service.py` (nuevo) | R2/R3 y R4 (entregas 4 y 5). | Enviar pregunta cuya respuesta esté en el Excel y ver JSON válido con las 3 llaves; enviar pregunta fuera de alcance y ver `estado_encontrado: false`. |
| 7 | @frontend | Pantalla de inicio: plantilla `base.html` con CSS embebido, caja de texto para preguntas, botón "Enviar", botón "Nueva conversación", 100% en español. | `app/templates/base.html`, `app/templates/inicio.html` | Endpoint de chat (entrega 3). | Abrir `iniciar_app.bat` y ver la pantalla de inicio con los 3 componentes. |
| 8 | @frontend | Pantalla de resultados: burbuja de texto con la respuesta formal, recuadro destacado "Fuente / Cita de Referencia", contadores grandes (cifras de control) y tabla con filtro de los 10 registros del insumo. | `app/templates/resultados.html` | Pantalla de inicio (entrega 7). | Enviar una pregunta y ver la respuesta + cita fuente; ver contadores y tabla filtrando por categoría. |
| 9 | @frontend | Detalle por registro: al hacer clic en una fila de la tabla, mostrar el registro completo (ID, categoría, pregunta, respuesta sugerida, palabras clave). | Modificar `app/templates/resultados.html` (añadir detalle) | Pantalla de resultados (entrega 8). | Clic en una fila y ver el detalle del registro en pantalla. |
| 10 | @tester | Pruebas pytest en `tests/` contra las cifras de control (10/10) y casos límite de AGENTS.md (pregunta confusa, información no encontrada, archivo ilegible). | `tests/test_*.py` (nuevo) | Backend completo + frontend (entregas 1-9). | Ejecutar `pytest` y ver que todas las pruebas pasan. |
| 11 | @tester | `VALIDACION.md` con esperado vs obtenido por cada prueba, reportando diferencias con causa probable. | `VALIDACION.md` (nuevo) | Pruebas ejecutadas (entrega 10). | Leer `VALIDACION.md` y confirmar que cada caso tiene su resultado. |
| 12 | @revisor | Revisión de seguridad: API key en `.env` (no hardcodeada), `.gitignore` con `.env`, `__pycache__/`, `.venv/`, `*.pyc`; revisar que todo esté en AGENTS.md y nada inventado. | Solo entrega informe de texto (no modifica archivos del proyecto) | App completa (entregas 1-11). | Leer el informe de hallazgos del revisor y verificar que no hay llaves expuestas ni archivos sensibles. |

---

## 4. PUNTOS DE CONTROL

| Después de la entrega | Interviene @tester | Qué debe ver usted en pantalla |
|-----------------------|--------------------|--------------------------------|
| 1 (estructura base) | No | Navegador abierto con `iniciar_app.bat`, servidor Flask respondiendo. |
| 6 (agente de IA integrado) | Sí | Pruebas de `ia_service.py`: JSON válido con `respuesta`, `cita_fuente`, `estado_encontrado`; pregunta fuera de alcance devuelve `estado_encontrado: false`. |
| 9 (pantallas completas) | Sí | Pruebas de interfaz: pantalla de inicio, pantalla de resultados con contadores y tabla, detalle por registro funcionando. |
| 11 (VALIDACION.md) | Sí | `VALIDACION.md` muestra esperado vs obtenido para las 10 preguntas del banco y los 3 casos límite; 10 de 10 correctas según AGENTS.md. |

---

## 5. RIESGOS

| Riesgo | Qué hará cada subagente si pasa |
|--------|---------------------------------|
| Datos incompletos en el Excel (columnas vacías o registros faltantes) | @backend valida al leer y devuelve error controlado; @revisor lo reporta en su informe. |
| Archivos escaneados o PDF sin texto (post-MVP, cuando se agreguen manuales) | @backend aplica R4: intercepta el error y muestra notificación sin colapsar. |
| Respuesta del agente de IA que no es JSON válido | @backend valida la estructura del JSON antes de devolverla; si no es válido, devuelve error controlado y @tester registra la diferencia en `VALIDACION.md`. |
| Límite de la llave gratis de la API de IA | @backend lee la llave de `.env` y, si falla por cuota, muestra mensaje amable al usuario; @revisor verifica que la llave nunca esté hardcodeada. |
| Falta de confirmación de S1 o S2 | @arquitecto los deja como pendientes en PLAN.md y no bloquea el MVP. |

---

## 6. PREGUNTAS PARA MÍ

Antes de empezar a construir, necesito que confirme:

1. **API key de IA**: ✅ **Respondido** — se agregará después (`.env.example` como placeholder; no hay llave real todavía).
2. **Modelo de IA específico**: ✅ **Respondido** — **Gemini**.
3. **¿El Excel de insumos es la única fuente de respuestas para el MVP, o el agente de IA también debe consultar documentos externos?** (AGENTS.md dice que el agente recibe "fragmentos de documentos relevantes del repositorio oficial de TH", pero por MVP solo tenemos el Excel). *Asumo: solo el Excel para MVP.*
4. **¿Quiere que las pruebas de @tester usen las 10 preguntas del Excel como banco de calibración, o prepara un banco separado?** *Asumo: las 10 preguntas del Excel como banco de calibración.*

Quedo a la espera de su aprobación de este PLAN.md y de las respuestas a las preguntas 3 y 4 antes de que cada subagente comience a trabajar.
