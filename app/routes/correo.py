import os
from flask import Blueprint, request, session, jsonify
import yagmail
import requests
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

correo_bp = Blueprint("correo", __name__, url_prefix="/correo")

@correo_bp.before_request
def sede():
    if "usuario" not in session:
        return jsonify({"mensaje": "No autorizado"}), 401

@correo_bp.route("/", methods=["POST"])
def enviar():
    token = request.form.get("token")
    if not token:
        return jsonify({"mensaje": "reCAPTCHA requerido"}), 400

    resp = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        "secret": os.getenv("RECAPTCHA_SECRET_KEY"),
        "response": token
    }).json()

    if not resp.get("success"):
        return jsonify({"mensaje": "reCAPTCHA inválido"}), 400

    to = request.form.get("para")
    asunto = request.form.get("asunto")
    mensaje = request.form.get("mensaje")
    archivo = request.files.get("archivo")

    try:
        yag = yagmail.SMTP(
            user=os.getenv("EMAIL"),
            password=os.getenv("EMAIL_PASSWORD"),
            host='smtp.gmail.com'
        )

        adjunto_path = None

        if archivo and archivo.filename:
            filename = secure_filename(archivo.filename)
            temp_path = os.path.join("/tmp", filename)  # Para Render, usa /tmp

            archivo.save(temp_path)
            adjunto_path = temp_path

        yag.send(
            to=to,
            subject=asunto,
            contents=[mensaje],
            attachments=[adjunto_path] if adjunto_path else None
        )

        if adjunto_path:
            os.remove(adjunto_path)

        return jsonify({"mensaje": "Correo enviado con éxito"}), 200

    except Exception as e:
        return jsonify({"mensaje": f"Error al enviar: {str(e)}"}), 500
