"""
Controlador de chat.

Implementa la regla de negocio R1:
    El sistema debe recibir preguntas en lenguaje natural a través de una
    interfaz de chat web.

Este controlador expone un endpoint POST que recibe una pregunta del usuario,
la envía al agente de IA y redirige a la página de resultados HTML.
"""

from flask import Blueprint, request, redirect, url_for, session, jsonify

from app.services.ia_service import procesar_pregunta_ia
from app.services.conversation_service import (
    preparar_contexto_ia,
    registrar_interaccion,
    obtener_historial,
)

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Recibe una pregunta en lenguaje natural, la procesa con el agente de IA
    y redirige a la página de resultados.

    Cuerpo de la petición (JSON o form):
        {
            "pregunta": "¿Cuántos días de licencia corresponden por matrimonio?",
            "session_id": "sesion_123"
        }

    Respuesta: Redirección HTTP 302 a /resultados con los datos en la sesión.
    """
    data = request.get_json(silent=True) or {}
    pregunta = data.get("pregunta", "").strip()
    session_id = data.get("session_id", session.get("session_id", "default"))

    if not pregunta:
        # Si es una petición AJAX, devolver JSON de error
        if request.is_json or request.headers.get("Content-Type") == "application/json":
            return jsonify({"error": "La pregunta no puede estar vacía", "estado": "error"}), 400
        # Si es un formulario, redirigir con mensaje de error
        session["error_msg"] = "La pregunta no puede estar vacía"
        return redirect(url_for("index"))

    session["session_id"] = session_id

    # Obtener historial previo de la sesión (R3)
    historial = obtener_historial(session_id)

    # Preparar contexto para el agente de IA (R2)
    contexto = preparar_contexto_ia(session_id, pregunta)

    # Llamar al agente de IA y validar contrato (entrega 6)
    resultado_ia = procesar_pregunta_ia(
        session_id=session_id,
        pregunta=pregunta,
        fragmentos_documentos=contexto["fragmentos_documentos"],
        historial=contexto["historial_sesion"],
    )

    # Registrar la interacción en el historial (R3)
    registrar_interaccion(
        session_id=session_id,
        pregunta=pregunta,
        respuesta=resultado_ia["respuesta"],
        cita_fuente=resultado_ia["cita_fuente"],
        estado_encontrado=resultado_ia["estado_encontrado"],
    )

    # Guardar el resultado en la sesión para mostrarlo en la página de resultados
    session["ultima_respuesta"] = resultado_ia["respuesta"]
    session["ultima_cita_fuente"] = resultado_ia["cita_fuente"]
    session["ultimo_estado_encontrado"] = resultado_ia["estado_encontrado"]

    # Redirigir a la página de resultados HTML
    return redirect(url_for("resultados"))
