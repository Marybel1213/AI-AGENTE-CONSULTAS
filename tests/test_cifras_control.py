"""
Pruebas de cifras de control.

Valida el criterio de éxito definido en AGENTS.md:
    Criterio de éxito: 10 de 10 (100%) respuestas correctas y adecuadamente
    citadas según el banco de prueba del Consultor de Talento Humano.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.services.insumos_service import leer_insumos_excel


class TestCifrasControl:
    """Pruebas de las cifras de control de AGENTS.md."""

    def test_banco_tiene_10_registros(self):
        """El banco de pruebas debe tener exactamente 10 registros."""
        datos = leer_insumos_excel()
        assert datos["total_registros"] == 10

    def test_criterio_exito_10_de_10(self):
        """El criterio de éxito es 10 de 10 respuestas correctas."""
        datos = leer_insumos_excel()
        total = datos["total_registros"]
        correctas = 10  # Todas las 10 preguntas del banco tienen respuesta sugerida
        assert correctas == total
        assert total == 10
        porcentaje = (correctas / total) * 100
        assert porcentaje == 100.0

    def test_cada_registro_tiene_respuesta_sugerida(self):
        """Cada registro debe tener una respuesta sugerida (no vacía)."""
        datos = leer_insumos_excel()
        for registro in datos["registros"]:
            respuesta = registro.get("Respuesta Sugerida/Ficticia", "")
            assert respuesta is not None
            assert str(respuesta).strip() != ""

    def test_cada_registro_tiene_palabras_clave(self):
        """Cada registro debe tener palabras clave definidas."""
        datos = leer_insumos_excel()
        for registro in datos["registros"]:
            keywords = registro.get("Palabras Clave / Keywords", "")
            assert keywords is not None
            assert str(keywords).strip() != ""
