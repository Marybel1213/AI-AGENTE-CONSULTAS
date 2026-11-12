"""
Configuración de pruebas pytest.

Provee fixtures para la aplicación Flask y el cliente de pruebas.
"""

import sys
import os

# Configurar pythonpath para importar la aplicación
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import create_app


@pytest.fixture
def app():
    """Fixture que crea la aplicación Flask para pruebas."""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Fixture que devuelve el cliente de pruebas de Flask."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Fixture que devuelve el runner de CLI de Flask."""
    return app.test_cli_runner()
