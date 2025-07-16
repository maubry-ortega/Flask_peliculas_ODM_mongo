# VolleyDevByMaubry [5/∞] - No hay control sin niveles, ni seguridad sin roles.

"""
Archivo: app/routes/usuario.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Rutas para gestionar autenticación y usuarios:
    - Login con validación reCAPTCHA.
    - Logout y cierre de sesión.
    - Creación de usuarios.
    - Validación de nivel de usuario (admin o estándar).

Notas:
    - El modelo Usuario debe incluir el campo 'nivel': "admin" o "user".
    - session['usuario'] guarda un diccionario: {usuario, nivel}.
"""

from flask import Blueprint, request, session, jsonify, redirect, url_for, render_template
import requests
import os
from app.models.usuario import Usuario

usuario_bp = Blueprint("usuario", __name__, url_prefix="/auth")


@usuario_bp.route("/login", methods=["POST"])
def login():
    """
    Procesa el login validando usuario, password y reCAPTCHA.

    Returns:
        dict: Mensaje de confirmación o error.
    """
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")
    token = data.get("token")

    if not token:
        return jsonify({"mensaje": "reCAPTCHA requerido"}), 400

    resp = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        "secret": os.getenv("RECAPTCHA_SECRET_KEY"),
        "response": token
    }).json()

    if not resp.get("success"):
        return jsonify({"mensaje": "reCAPTCHA inválido"}), 400

    user = Usuario.objects(usuario=usuario, password=password).first()
    if not user:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    session.permanent = True
    session["usuario"] = {
        "usuario": user.usuario,
        "nivel": user.nivel
    }

    return jsonify({"mensaje": "Bienvenido", "nivel": user.nivel})


@usuario_bp.route("/logout", methods=["GET"])
def logout():
    """
    Cierra la sesión actual.
    """
    session.pop("usuario", None)
    return redirect(url_for("home"))


@usuario_bp.route("/crear", methods=["POST"])
def crear_usuario():
    """
    Crea un nuevo usuario con nivel especificado.

    Returns:
        dict: Mensaje de confirmación o error.
    """
    data = request.get_json()
    try:
        nuevo = Usuario(
            usuario=data.get("usuario"),
            password=data.get("password"),
            nombre=data.get("nombre"),
            correo=data.get("correo"),
            nivel=data.get("nivel", "user")  # Por defecto 'user'
        )
        nuevo.save()
        return jsonify({"mensaje": "Usuario creado"}), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 400


@usuario_bp.route("/vista_admin", methods=["GET"])
def vista_admin():
    """
    Renderiza una vista solo accesible por administradores.

    Returns:
        str: HTML renderizado o redirección.
    """
    usuario_data = session.get("usuario")
    if not usuario_data or usuario_data.get("nivel") != "admin":
        return redirect(url_for("home"))

    return render_template("admin.html")
