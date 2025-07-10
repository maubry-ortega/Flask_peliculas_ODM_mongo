# VolleyDevByMaubry [13/∞] - Validación reCAPTCHA
from flask import Blueprint, request, session, jsonify
import yagmail, os, requests
from dotenv import load_dotenv

load_dotenv()
correo_bp = Blueprint("correo", __name__, url_prefix="/correo")

@correo_bp.before_request
def sede():
    if "usuario" not in session:
        return jsonify({"mensaje": "No autorizado"}), 401

@correo_bp.route("/", methods=["POST"])
def enviar():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"mensaje": "reCAPTCHA requerido"}), 400

    resp = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        "secret": os.getenv("RECAPTCHA_SECRET_KEY"),
        "response": token
    }).json()

    if not resp.get("success"):
        return jsonify({"mensaje": "reCAPTCHA inválido"}), 400

    # Email
    to = data.get("para")
    asunto = data.get("asunto")
    mensaje = data.get("mensaje")

    try:
        yag = yagmail.SMTP(
            user=os.getenv("EMAIL"),
            password=os.getenv("EMAIL_PASSWORD"),
            host='smtp.gmail.com'
        )
        yag.send(to=to, subject=asunto, contents=mensaje)
        return jsonify({"mensaje": "Correo enviado con éxito"}), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al enviar: {str(e)}"}), 500
