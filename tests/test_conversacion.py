"""
Pruebas del servicio de conversación.

Valida las reglas de negocio R2 y R3:
    R2: Gestionar el flujo de la conversación y enviar consulta + documentos al agente de IA.
    R3: Registrar el historial de interacciones de la sesión.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.services.conversation_service import (
    obtener_historial,
    registrar_interaccion,
    limpiar_historial,
    preparar_contexto_ia,
    obtener_fragmentos_documentos,
)


class TestConversacionR2R3:
    """Pruebas de reglas R2 y R3."""

    def setup_method(self):
        """Limpia el historial antes de cada prueba."""
        limpiar_historial("sesion_prueba_r2r3")

    def test_registrar_y_obtener_historial(self):
        """Debe registrar una interacción y recuperarla del historial."""
        session_id = "sesion_prueba_r2r3"
        registrar_interaccion(
            session_id,
            "¿Cuál es la fecha de corte?",
            "El corte es el día 25.",
            "Banco de Preguntas.xlsx",
            True,
        )
        historial = obtener_historial(session_id)
        assert len(historial) == 1
        assert historial[0]["pregunta"] == "¿Cuál es la fecha de corte?"
        assert historial[0]["respuesta"] == "El corte es el día 25."
        assert historial[0]["cita_fuente"] == "Banco de Preguntas.xlsx"
        assert historial[0]["estado_encontrado"] is True

    def test_historial_mantiene_multiple_interacciones(self):
        """Debe conservar varias interacciones en el historial."""
        session_id = "sesion_prueba_r2r3"
        registrar_interaccion(session_id, "P1", "R1", "F1", True)
        registrar_interaccion(session_id, "P2", "R2", "F2", False)
        historial = obtener_historial(session_id)
        assert len(historial) == 2

    def test_limpiar_historial_nueva_conversacion(self):
        """Debe eliminar el historial al iniciar una nueva conversación."""
        session_id = "sesion_prueba_r2r3"
        registrar_interaccion(session_id, "P1", "R1", "F1", True)
        limpiar_historial(session_id)
        historial = obtener_historial(session_id)
        assert len(historial) == 0

    def test_preparar_contexto_ia_tiene_claves_requeridas(self):
        """El contexto para IA debe tener pregunta, fragmentos_documentos y historial_sesion."""
        session_id = "sesion_prueba_r2r3"
        contexto = preparar_contexto_ia(session_id, "¿Cuántos días de vacaciones?")
        assert "pregunta" in contexto
        assert "fragmentos_documentos" in contexto
        assert "historial_sesion" in contexto
        assert contexto["pregunta"] == "¿Cuántos días de vacaciones?"

    def test_obtener_fragmentos_documentos_retorna_lista(self):
        """Los fragmentos de documentos deben ser una lista (puede estar vacía si no hay archivo)."""
        fragmentos = obtener_fragmentos_documentos()
        assert isinstance(fragmentos, list)
