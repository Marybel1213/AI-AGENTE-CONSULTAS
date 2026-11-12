"""
Pruebas del contrato de salida JSON del agente de IA.

Valida que el agente de IA respete el contrato definido en AGENTS.md:
    - respuesta: string
    - cita_fuente: string
    - estado_encontrado: boolean
    - Regla estricta: si no se encuentra, "no indicado"
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.services.ia_service import (
    validar_contrato_ia,
    procesar_pregunta_ia,
    llamar_agente_ia,
)


class TestContratoIA:
    """Pruebas del contrato JSON del agente de IA."""

    def test_respuesta_valida_tiene_tres_llaves(self):
        """El contrato JSON debe tener exactamente respuesta, cita_fuente, estado_encontrado."""
        entrada = {
            "respuesta": "El corte es el día 25 de cada mes.",
            "cita_fuente": "Banco de Preguntas.xlsx",
            "estado_encontrado": True,
        }
        resultado = validar_contrato_ia(entrada)
        assert set(resultado.keys()) == {"respuesta", "cita_fuente", "estado_encontrado"}

    def test_tipos_de_datos_correctos(self):
        """respuesta debe ser string, cita_fuente string, estado_encontrado boolean."""
        entrada = {
            "respuesta": "Texto de respuesta",
            "cita_fuente": "Documento fuente",
            "estado_encontrado": True,
        }
        resultado = validar_contrato_ia(entrada)
        assert isinstance(resultado["respuesta"], str)
        assert isinstance(resultado["cita_fuente"], str)
        assert isinstance(resultado["estado_encontrado"], bool)

    def test_estado_encontrado_falso_para_no_indicado(self):
        """Cuando no se encuentra información, estado_encontrado debe ser False y respuesta 'no indicado'."""
        resultado = procesar_pregunta_ia("sesion_test", "Pregunta fuera de alcance", [], [])
        assert resultado["estado_encontrado"] is False
        assert resultado["respuesta"] == "no indicado"

    def test_validacion_corrompe_tipos_incorrectos(self):
        """Debe corregir tipos incorrectos en la entrada."""
        entrada = {"respuesta": 123, "cita_fuente": None, "estado_encontrado": "no booleano"}
        resultado = validar_contrato_ia(entrada)
        assert resultado["respuesta"] == "no indicado"  # No es string válido
        assert resultado["cita_fuente"] == "no indicado"  # Es None
        assert resultado["estado_encontrado"] is True  # "no booleano" es truthy

    def test_sin_api_key_retorna_no_indicado(self):
        """Sin API key configurada, el agente debe retornar estado_encontrado: False."""
        resultado = llamar_agente_ia("¿Cuál es la fecha de corte?", [], [])
        assert resultado["estado_encontrado"] is False
        assert resultado["respuesta"] == "no indicado"
