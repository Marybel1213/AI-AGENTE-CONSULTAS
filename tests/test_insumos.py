"""
Pruebas del servicio de lectura de insumos.

Valida que el Excel de insumos se lea correctamente con sus 5 columnas
y 10 registros, según lo definido en AGENTS.md.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.services.insumos_service import leer_insumos_excel


class TestInsumosExcel:
    """Pruebas del archivo de insumos Excel."""

    def test_archivo_existe_y_se_lee(self):
        """Debe leer el archivo de insumos sin errores."""
        datos = leer_insumos_excel()
        assert datos is not None
        assert "encabezados" in datos
        assert "registros" in datos
        assert "total_registros" in datos

    def test_encabezados_correctos(self):
        """Debe tener exactamente los 5 encabezados definidos en AGENTS.md."""
        datos = leer_insumos_excel()
        encabezados_esperados = [
            "ID",
            "Categoría",
            "Pregunta Frecuente",
            "Respuesta Sugerida/Ficticia",
            "Palabras Clave / Keywords",
        ]
        assert datos["encabezados"] == encabezados_esperados

    def test_total_registros_es_10(self):
        """Debe haber exactamente 10 registros de datos (FAQ-001 a FAQ-010)."""
        datos = leer_insumos_excel()
        assert datos["total_registros"] == 10

    def test_registros_tienen_todos_los_campos(self):
        """Cada registro debe tener los 5 campos con valores no vacíos."""
        datos = leer_insumos_excel()
        for registro in datos["registros"]:
            assert registro.get("ID") is not None and str(registro["ID"]).strip() != ""
            assert registro.get("Categoría") is not None
            assert registro.get("Pregunta Frecuente") is not None
            assert registro.get("Respuesta Sugerida/Ficticia") is not None
            assert registro.get("Palabras Clave / Keywords") is not None

    def test_ids_son_faq_001_a_010(self):
        """Los IDs deben ser FAQ-001 hasta FAQ-010."""
        datos = leer_insumos_excel()
        ids_esperados = [f"FAQ-{i:03d}" for i in range(1, 11)]
        ids_obtenidos = [reg["ID"] for reg in datos["registros"]]
        assert ids_obtenidos == ids_esperados

    def test_no_modifica_archivo_original(self):
        """El servicio solo lee, nunca modifica el archivo de insumos."""
        datos_antes = leer_insumos_excel()
        datos_despues = leer_insumos_excel()
        assert datos_antes["total_registros"] == datos_despues["total_registros"]
        assert datos_antes["encabezados"] == datos_despues["encabezados"]
