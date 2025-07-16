# VolleyDevByMaubry [9/∞] - La identidad del usuario define su acceso.

"""
Archivo: app/models/usuario.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Modelo de datos para usuarios del sistema.
    Incluye credenciales, datos de contacto y nivel de acceso.

Notas:
    - La colección se llama 'usuario'.
    - El campo 'nivel' define si es administrador ('admin') o usuario normal ('user').
    - El campo 'correo' usa validación automática como EmailField.
"""

from mongoengine import Document, StringField, EmailField

class Usuario(Document):
    """
    Modelo de Usuario.

    Campos:
        usuario (str): Nombre de usuario único.
        password (str): Contraseña asociada.
        nombre (str): Nombre completo del usuario.
        correo (str): Correo electrónico validado.
        nivel (str): Nivel de acceso ("admin" o "user"), valor por defecto "user".
    """
    usuario = StringField(required=True, unique=True)
    password = StringField(required=True)
    nombre = StringField(required=True)
    correo = EmailField(required=True)
    nivel = StringField(required=True, choices=["admin", "user"], default="user")

    meta = {
        'collection': 'usuario'
    }
