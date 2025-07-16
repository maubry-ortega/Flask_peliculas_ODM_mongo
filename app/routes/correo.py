# VolleyDevByMaubry [10/∞] - La comunicación abre la puerta a nuevos usuarios.

"""
Archivo: app/routes/correo.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Rutas para envío de correos electrónicos con adjuntos mediante Yagmail.
    Incluye:
        - Envío normal protegido por sesión.
        - Solicitud de creación de usuario sin sesión.

Notas:
    - Validación de reCAPTCHA incluida.
    - Manejo seguro de archivos temporales.
    - Variables EMAIL, EMAIL_PASSWORD y ADMIN_EMAIL en el entorno.
"""

import os
import requests
import yagmail
from flask import Blueprint, request, session, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

correo_bp = Blueprint("correo", __name__, url_prefix="/correo")

@correo_bp.before_request
def proteger_sesion():
    """
    Middleware que protege las rutas excepto solicitud_usuario.
    """
    if request.endpoint == "correo.solicitud_usuario":
        return  # Libre acceso
    if "usuario" not in session:
        return jsonify({"mensaje": "No autorizado"}), 401

@correo_bp.route("/", methods=["POST"])
def enviar():
    """
    Ruta para enviar correo normal con posible adjunto.
    Solo accesible con sesión activa.
    """
    token = request.form.get("token")
    if not token:
        return jsonify({"mensaje": "reCAPTCHA requerido"}), 400

    # Validar reCAPTCHA
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
        yag = yagmail.SMTP(user=os.getenv("EMAIL"), password=os.getenv("EMAIL_PASSWORD"))

        adjunto_path = None
        if archivo and archivo.filename:
            filename = secure_filename(archivo.filename)
            temp_path = os.path.join("/tmp", filename)
            archivo.save(temp_path)
            adjunto_path = temp_path

        yag.send(to=to, subject=asunto, contents=[mensaje], attachments=[adjunto_path] if adjunto_path else None)

        if adjunto_path:
            os.remove(adjunto_path)

        return jsonify({"mensaje": "Correo enviado con éxito"}), 200

    except Exception as e:
        return jsonify({"mensaje": f"Error al enviar: {str(e)}"}), 500

@correo_bp.route("/solicitud", methods=["POST"])
def solicitud_usuario():
    """
    Ruta para recibir solicitudes de nuevo usuario.
    Accesible sin sesión.
    """
    data = request.get_json()
    if not data:
        return jsonify({"mensaje": "Datos incompletos"}), 400

    nombre = data.get("nombre")
    usuario = data.get("usuario")
    correo = data.get("correo")
    comentario = data.get("comentario")

    if not nombre or not usuario or not correo:
        return jsonify({"mensaje": "Faltan datos obligatorios"}), 400

    try:
        yag = yagmail.SMTP(user=os.getenv("EMAIL"), password=os.getenv("EMAIL_PASSWORD"))
        contenido = f"""Nueva solicitud de usuario:\n\nNombre: {nombre}\nUsuario deseado: {usuario}\nCorreo de contacto: {correo}\nComentario: {comentario or 'Sin comentarios'}\n"""
        yag.send(to=os.getenv("ADMIN_EMAIL"), subject="Solicitud de nuevo usuario", contents=[contenido])
        return jsonify({"mensaje": "Solicitud enviada correctamente"}), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al enviar: {str(e)}"}), 500