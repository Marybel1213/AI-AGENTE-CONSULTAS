"""
Controlador de chat.

Implementa la regla de negocio R1:
    El sistema debe recibir preguntas en lenguaje natural a través de una
    interfaz de chat web.

Este controlador expone un endpoint POST que recibe una pregunta del usuario,
la envía al agente de IA y devuelve la respuesta en formato JSON.
"""

from flask import Blueprint, request, jsonify, session

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
    Recibe una pregunta en lenguaje natural y devuelve la respuesta del agente de IA en JSON.

    Cuerpo de la petición (JSON):
        {
            "pregunta": "¿Cuántos días de licencia corresponden por matrimonio?",
            "session_id": "sesion_123"
        }

    Respuesta (JSON):
        {
            "respuesta": "...",
            "cita_fuente": "...",
            "estado_encontrado": true/false
        }
    """
    data = request.get_json(silent=True) or {}
    pregunta = data.get("pregunta", "").strip()
    session_id = data.get("session_id", session.get("session_id", "default"))

    if not pregunta:
        return jsonify({"error": "La pregunta no puede estar vacía", "estado": "error"}), 400

    session["session_id"] = session_id

    # Obtener historial previo de la sesión (R3)
    historial = obtener_historial(session_id)

    # Preparar contexto para el agente de IA (R2)
    contexto = preparar_contexto_ia(session_id, pregunta)

    # Llamar al agente de IA y validar contrato
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

    # Guardar en sesión para la página de resultados (si se usa)
    session["ultima_respuesta"] = resultado_ia["respuesta"]
    session["ultima_cita_fuente"] = resultado_ia["cita_fuente"]
    session["ultimo_estado_encontrado"] = resultado_ia["estado_encontrado"]

    # Devolver JSON directamente (no redirigir)
    return jsonify(resultado_ia)
