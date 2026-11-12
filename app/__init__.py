import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv

from app.controllers.chat_controller import chat_bp
from app.controllers.auth_controller import auth_bp
from app.services.conversation_service import (
    preparar_contexto_ia,
    obtener_historial,
    limpiar_historial,
    obtener_error_lectura,
)

load_dotenv()


def create_app():
    app = Flask(__name__)

    # Clave secreta para sesiones de Flask (requerida por session)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-cambiar-en-produccion")

    # Registrar blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)

    # Middleware: proteger todas las rutas excepto login, salir, health y estáticos
    @app.before_request
    def requerir_autenticacion():
        rutas_publicas = [
            "auth.login",
            "auth.salir",
            "static",
        ]
        # Permitir health sin autenticación (para Render)
        if request.endpoint == "health":
            return None
        if request.endpoint not in rutas_publicas and not session.get("usuario_autenticado"):
            return redirect(url_for("auth.login"))

    @app.route("/")
    def index():
        """Pantalla de inicio con formulario de consulta."""
        session_id = session.get("session_id", "default")
        session["session_id"] = session_id
        historial = obtener_historial(session_id)
        error_lectura = obtener_error_lectura()
        return render_template(
            "inicio.html",
            session_id=session_id,
            historial=historial,
            error_lectura=error_lectura,
            usuario_nombre=session.get("usuario_nombre", "Usuario"),
        )

    @app.route("/resultados")
    def resultados():
        """Pantalla de resultados con respuesta, cita fuente y tabla de registros."""
        session_id = session.get("session_id", "default")
        session["session_id"] = session_id

        # Leer resultado de la sesión (guardado por el controlador de chat)
        respuesta = session.get("ultima_respuesta", "")
        cita_fuente = session.get("ultima_cita_fuente", "")
        estado_encontrado = session.get("ultimo_estado_encontrado", False)

        # Cargar registros del insumo para la tabla
        try:
            from app.services.insumos_service import leer_insumos_excel

            datos = leer_insumos_excel()
            registros = datos["registros"]
            total_registros = datos["total_registros"]
        except Exception:
            registros = []
            total_registros = 0

        historial = obtener_historial(session_id)
        error_lectura = obtener_error_lectura()

        return render_template(
            "resultados.html",
            respuesta=respuesta,
            cita_fuente=cita_fuente,
            estado_encontrado=estado_encontrado,
            registros=registros,
            total_registros=total_registros,
            historial=historial,
            session_id=session_id,
            error_lectura=error_lectura,
            usuario_nombre=session.get("usuario_nombre", "Usuario"),
        )

    @app.route("/nueva-conversacion")
    def nueva_conversacion():
        """Limpia el historial de la sesión y redirige al inicio."""
        session_id = session.get("session_id", "default")
        limpiar_historial(session_id)
        session.pop("session_id", None)
        session.pop("ultima_respuesta", None)
        session.pop("ultima_cita_fuente", None)
        session.pop("ultimo_estado_encontrado", None)
        return redirect(url_for("index"))

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    return app
