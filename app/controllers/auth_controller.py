"""
Controlador de autenticación.

Implementa el acceso sencillo a la aplicación usando credenciales leídas
de variables de entorno (APP_USUARIO y APP_CLAVE), sin base de datos.

Reglas de negocio:
    - Ruta /login: muestra formulario y valida credenciales.
    - Ruta /salir: cierra la sesión del usuario.
    - Todas las demás rutas exigen haber iniciado sesión.
    - Si las credenciales son incorrectas, muestra mensaje de error.
"""

from flask import Blueprint, request, redirect, url_for, render_template, session, flash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Muestra el formulario de login (GET) y valida las credenciales (POST).

    Las credenciales válidas se leen de las variables de entorno:
        - APP_USUARIO
        - APP_CLAVE

    Si son correctas, establece la sesión y redirige a la página de inicio.
    Si son incorrectas, muestra mensaje de error.
    """
    # Si ya está autenticado, redirigir al inicio
    if session.get("usuario_autenticado"):
        return redirect(url_for("index"))

    error = None

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        clave = request.form.get("clave", "").strip()

        usuario_valido = __import__("os").getenv("APP_USUARIO", "")
        clave_valida = __import__("os").getenv("APP_CLAVE", "")

        if usuario == usuario_valido and clave == clave_valida:
            session["usuario_autenticado"] = True
            session["usuario_nombre"] = usuario
            return redirect(url_for("index"))
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template("login.html", error=error)


@auth_bp.route("/salir")
def salir():
    """Cierra la sesión del usuario y redirige al login."""
    session.clear()
    return redirect(url_for("auth.login"))
