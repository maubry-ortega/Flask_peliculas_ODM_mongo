# VolleyDevByMaubry [6/∞] - Comunicar es tan importante como construir.

"""
Archivo: app/routes/correo.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Rutas para envío de correos electrónicos con adjuntos mediante Yagmail:
    - Protegidas por sesión de usuario.
    - Validación de reCAPTCHA incluida.
    - Manejo seguro de archivos temporales.

Notas:
    - El envío solo se realiza si el reCAPTCHA es válido.
    - Los archivos adjuntos se guardan temporalmente en /tmp.
    - Utiliza las variables EMAIL y EMAIL_PASSWORD del entorno.
"""

import os
from flask import Blueprint, request, session, jsonify
import yagmail
import requests
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

correo_bp = Blueprint("correo", __name__, url_prefix="/correo")


@correo_bp.before_request
def proteger_sesion():
    """
    Middleware que verifica si hay sesión activa.
    """
    if "usuario" not in session:
        return jsonify({"mensaje": "No autorizado"}), 401


@correo_bp.route("/", methods=["POST"])
def enviar():
    """
    Envía un correo electrónico con posible archivo adjunto.

    Datos esperados en request.form:
        - token: Token de reCAPTCHA (obligatorio).
        - para: Correo de destino.
        - asunto: Asunto del correo.
        - mensaje: Cuerpo del mensaje.
        - archivo: Archivo adjunto opcional (request.files).

    Returns:
        dict: Mensaje de éxito o error.
    """
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

    if not to or not asunto or not mensaje:
        return jsonify({"mensaje": "Faltan datos obligatorios"}), 400

    try:
        yag = yagmail.SMTP(
            user=os.getenv("EMAIL"),
            password=os.getenv("EMAIL_PASSWORD"),
            host='smtp.gmail.com'
        )

        adjunto_path = None
        if archivo and archivo.filename:
            filename = secure_filename(archivo.filename)
            temp_path = os.path.join("/tmp", filename)
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
