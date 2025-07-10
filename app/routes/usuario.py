# VolleyDevByMaubry [3/∞]
from flask import Blueprint, request, session, jsonify, redirect
from app.models.usuario import Usuario

usuario_bp = Blueprint("usuario", __name__, url_prefix="/auth")

@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = Usuario.objects(usuario=data["usuario"], password=data["password"]).first()
    if user:
        session["usuario"] = user.usuario
        return jsonify({"mensaje": "OK"}), 200
    return jsonify({"mensaje": "Credenciales inválidas"}), 401

@usuario_bp.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")
