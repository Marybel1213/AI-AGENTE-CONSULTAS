"""
Pruebas de casos límite definidos en AGENTS.md:

1. Pregunta confusa o en otro idioma: mostrar mensaje formal solicitando reformulación.
2. Información no encontrada en manuales: devolver "no indicado" y derivar con el Consultor de TH.
3. Archivo borroso o ilegible: mostrar notificación de archivo no legible.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.services.ia_service import procesar_pregunta_ia, validar_contrato_ia
from app.services.error_service import leer_archivo_seguro, notificar_archivo_ilegrable


class TestCasosLimite:
    """Pruebas de los 3 casos límite de AGENTS.md."""

    def test_pregunta_confusa_o_en_otro_idioma(self):
        """
        Caso límite 1: Pregunta confusa o en otro idioma.
        El agente debe responder de forma formal (no colapsar).
        """
        # Pregunta en otro idioma (inglés)
        resultado = procesar_pregunta_ia("sesion_limite_1", "What is the vacation policy?", [], [])
        assert resultado is not None
        assert "respuesta" in resultado
        assert "estado_encontrado" in resultado

        # Pregunta confusa (sin sentido)
        resultado2 = procesar_pregunta_ia("sesion_limite_1", "asdfghjkl qwerty 12345", [], [])
        assert resultado2 is not None
        assert resultado2["estado_encontrado"] is False

    def test_informacion_no_encontrada_en_manuales(self):
        """
        Caso límite 2: Información no encontrada en manuales.
        Debe devolver estado 'no indicado' y derivada al Consultor de TH.
        """
        resultado = procesar_pregunta_ia(
            "sesion_limite_2",
            "¿Cuántos días de licencia por matrimonio en el año 2099?",
            [],
            [],
        )
        assert resultado["estado_encontrado"] is False
        assert resultado["respuesta"] == "no indicado"

        # Validar contrato completo
        contrato = validar_contrato_ia(resultado)
        assert isinstance(contrato["respuesta"], str)
        assert isinstance(contrato["cita_fuente"], str)
        assert isinstance(contrato["estado_encontrado"], bool)

    def test_archivo_borroso_o_ilegible(self):
        """
        Caso límite 3: Archivo borroso o ilegible.
        Debe mostrar notificación sin colapsar la aplicación.
        """
        # Archivo que no existe (simula archivo ilegible/corrupto)
        exito, contenido, error = leer_archivo_seguro("INSUMOS/archivo_corrupto.pdf")
        assert exito is False
        assert contenido is None
        assert error is not None

        # Notificación estructurada
        notificacion = notificar_archivo_ilegrable("INSUMOS/archivo_corrupto.pdf")
        assert notificacion["legible"] is False
        assert notificacion["mensaje"] is not None
        assert notificacion["accion_recomendada"] is not None

    def test_app_no_colapsa_con_casos_limite(self):
        """La aplicación no debe colapsar ante cualquiera de los 3 casos límite."""
        # Caso 1: pregunta en otro idioma
        r1 = procesar_pregunta_ia("s1", "Hello world", [], [])
        assert r1 is not None

        # Caso 2: info no encontrada
        r2 = procesar_pregunta_ia("s2", "Pregunta inexistente", [], [])
        assert r2 is not None

        # Caso 3: archivo ilegible
        r3 = notificar_archivo_ilegrable("INSUMOS/inexistente.docx")
        assert r3 is not None
