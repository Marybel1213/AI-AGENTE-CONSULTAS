"""
Pruebas del servicio de manejo de errores.

Valida la regla de negocio R4:
    Si se detecta un error de archivo ilegible, el código debe interceptar
    la falla y mostrar la notificación correspondiente sin colapsar.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.services.error_service import leer_archivo_seguro, notificar_archivo_ilegrable


class TestErroresR4:
    """Pruebas de la regla R4."""

    def test_archivo_legible_retorna_exito(self):
        """Un archivo existente y legible debe retornar éxito."""
        exito, contenido, error = leer_archivo_seguro("app/__init__.py")
        assert exito is True
        assert contenido is not None
        assert error is None

    def test_archivo_inexistente_no_colapsa(self):
        """Un archivo inexistente debe retornar error sin colapsar."""
        exito, contenido, error = leer_archivo_seguro("INSUMOS/archivo_que_no_existe.pdf")
        assert exito is False
        assert contenido is None
        assert error is not None
        assert "no existe" in error.lower()

    def test_notificacion_estructura_correcta(self):
        """La notificación debe tener las claves: archivo, legible, mensaje, accion_recomendada."""
        notificacion = notificar_archivo_ilegrable("INSUMOS/documento_corrupto.pdf")
        assert "archivo" in notificacion
        assert "legible" in notificacion
        assert "mensaje" in notificacion
        assert "accion_recomendada" in notificacion
        assert notificacion["legible"] is False
        assert notificacion["mensaje"] is not None
        assert notificacion["accion_recomendada"] is not None

    def test_notificacion_archivo_legible(self):
        """Si el archivo es legible, la notificación debe indicarlo."""
        notificacion = notificar_archivo_ilegrable("app/__init__.py")
        assert notificacion["legible"] is True
        assert notificacion["mensaje"] is None
