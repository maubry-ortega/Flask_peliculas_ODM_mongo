# VolleyDevByMaubry [26/∞]
from flask import Blueprint, request, session, jsonify, redirect, url_for
import requests, os
from app.models.usuario import Usuario

usuario_bp = Blueprint("usuario", __name__, url_prefix="/auth")

@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")
    token = data.get("token")

    if not token:
        return jsonify({"mensaje": "reCAPTCHA requerido"}), 400

    # Validar token con Google
    resp = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        "secret": os.getenv("RECAPTCHA_SECRET_KEY"),
        "response": token
    }).json()

    if not resp.get("success"):
        return jsonify({"mensaje": "reCAPTCHA inválido"}), 400

    # Autenticación simple (ajusta a tu modelo real)
    user = Usuario.objects(usuario=usuario, password=password).first()
    if not user:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    session["usuario"] = user.usuario
    return jsonify({"mensaje": "Bienvenido"})

@usuario_bp.route("/logout", methods=["GET"])
def logout():
    session.pop("usuario", None)
    return redirect(url_for("home"))

# Ruta temporal para crear usuarios desde el navegador o cliente HTTP
@usuario_bp.route("/crear", methods=["POST"])
def crear_usuario():
    data = request.get_json()
    try:
        nuevo = Usuario(
            usuario=data.get("usuario"),
            password=data.get("password"),
            nombre=data.get("nombre"),
            correo=data.get("correo")
        )
        nuevo.save()
        return jsonify({"mensaje": "Usuario creado"}), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 400
