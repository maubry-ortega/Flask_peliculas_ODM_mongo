# VolleyDevByMaubry [6/∞]
from flask import Blueprint, request, session, jsonify
import yagmail, os

correo_bp = Blueprint("correo", __name__, url_prefix="/correo")

@correo_bp.before_request
def sede():
    if "usuario" not in session:
        return jsonify({"mensaje":"No autorizado"}),401

@correo_bp.route("/enviar", methods=["POST"])
def send():
    d = request.get_json()
    try:
        yag = yagmail.SMTP(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))
        yag.send(d["destino"], d["asunto"], d["contenido"], attachments=d.get("archivo"))
        return jsonify({"mensaje":"Correo enviado"})
    except Exception as e:
        return jsonify({"mensaje":str(e)}), 500
