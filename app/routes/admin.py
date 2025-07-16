# VolleyDevByMaubry [6/∞] - La claridad estructural evita el caos en el código.

"""
Archivo: app/routes/admin.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Rutas específicas para administración de usuarios:
    - Vista de gestión de usuarios.
    - CRUD de usuarios accesible solo por administradores.

Notas:
    - Protege todas las rutas con verificación de nivel "admin".
"""

from flask import Blueprint, request, session, jsonify, redirect, url_for, render_template
from app.models.usuario import Usuario
from bson import ObjectId

admin_bp = Blueprint("admin", __name__, url_prefix="/admin/usuarios")


@admin_bp.before_request
def proteger_admin():
    if "usuario" not in session or session["usuario"]["nivel"] != "admin":
        return redirect(url_for("home"))


@admin_bp.route("/", methods=["GET"])
def vista_admin():
    return render_template("admin/usuarios.html")


@admin_bp.route("/api", methods=["GET"])
def obtener_usuarios():
    usuarios = Usuario.objects().only("id", "usuario", "nombre", "correo", "nivel")
    data = []
    for u in usuarios:
        data.append({
            "id": str(u.id),
            "usuario": u.usuario,
            "nombre": u.nombre,
            "correo": u.correo,
            "nivel": u.nivel
        })
    return jsonify(data), 200


@admin_bp.route("/api", methods=["POST"])
def crear_usuario_admin():
    data = request.get_json()
    try:
        nuevo = Usuario(
            usuario=data.get("usuario"),
            password=data.get("password"),
            nombre=data.get("nombre"),
            correo=data.get("correo"),
            nivel=data.get("nivel", "user")
        )
        nuevo.save()
        return jsonify({"mensaje": "Usuario creado"}), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 400


@admin_bp.route("/api/<id_usuario>", methods=["PUT"])
def actualizar_usuario_admin(id_usuario):
    data = request.get_json()
    try:
        Usuario.objects(id=ObjectId(id_usuario)).update_one(
            set__usuario=data.get("usuario"),
            set__password=data.get("password"),
            set__nombre=data.get("nombre"),
            set__correo=data.get("correo"),
            set__nivel=data.get("nivel")
        )
        return jsonify({"mensaje": "Usuario actualizado"}), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 400


@admin_bp.route("/api/<id_usuario>", methods=["DELETE"])
def eliminar_usuario_admin(id_usuario):
    try:
        Usuario.objects(id=ObjectId(id_usuario)).delete()
        return jsonify({"mensaje": "Usuario eliminado"}), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error: {str(e)}"}), 400
