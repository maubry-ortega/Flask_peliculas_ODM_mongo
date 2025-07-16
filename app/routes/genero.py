# VolleyDevByMaubry [3/∞] - Código claro, intención clara.

"""
Archivo: app/routes/genero.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Rutas para gestionar géneros de películas:
    - Listar, crear, actualizar y eliminar géneros (API JSON).
    - Vista HTML protegida con sesión.
    - Middleware para proteger todas las rutas del blueprint.
    
Notas:
    - Si la sesión expira o no existe, se redirige a la página de login o devuelve JSON 401.
    - Se recomienda configurar permanent_session_lifetime en create_app().
"""

from flask import Blueprint, request, session, jsonify, render_template, redirect
from app.models.genero import Genero

genero_bp = Blueprint("genero", __name__, url_prefix="/genero")

@genero_bp.before_request
def proteger_sesion():
    """
    Middleware que valida si hay sesión antes de procesar la ruta.
    Devuelve 401 o redirige según sea API o vista.
    """
    if "usuario" not in session:
        if request.path.endswith(".json") or request.is_json:
            return jsonify({"mensaje": "No autorizado"}), 401
        return redirect("/")

@genero_bp.route("/", methods=["GET"])
def list_gen():
    """
    Devuelve un listado de géneros en formato JSON.

    Returns:
        list: Lista de diccionarios con id y nombre de cada género.
    """
    return jsonify([{"id": str(g.id), "nombre": g.nombre} for g in Genero.objects()])

@genero_bp.route("/", methods=["POST"])
def add_gen():
    """
    Crea un nuevo género a partir de datos JSON recibidos.

    Returns:
        dict: Mensaje de confirmación.
    """
    data = request.get_json()
    nuevo = Genero(nombre=data.get("nombre"))
    nuevo.save()
    return jsonify({"mensaje": "Género creado"}), 201

@genero_bp.route("/<id>", methods=["PUT"])
def upd_gen(id):
    """
    Actualiza el nombre de un género existente.

    Args:
        id (str): ID del género.

    Returns:
        dict: Mensaje de actualización o error.
    """
    gen = Genero.objects(id=id).first()
    if not gen:
        return jsonify({"mensaje": "No existe"}), 404
    gen.update(nombre=request.get_json().get("nombre"))
    return jsonify({"mensaje": "Género actualizado"})

@genero_bp.route("/<id>", methods=["DELETE"])
def del_gen(id):
    """
    Elimina un género existente por su ID.

    Args:
        id (str): ID del género.

    Returns:
        dict: Mensaje de eliminación o error.
    """
    gen = Genero.objects(id=id).first()
    if not gen:
        return jsonify({"mensaje": "No existe"}), 404
    gen.delete()
    return jsonify({"mensaje": "Género eliminado"})

@genero_bp.route("/vista", methods=["GET"])
def vista_generos():
    """
    Renderiza la vista HTML de gestión de géneros.

    Returns:
        str: HTML renderizado.
    """
    return render_template("generos.html")
