# VolleyDevByMaubry [4/∞] - El código no miente, pero puede confundir si no se documenta.

"""
Archivo: app/routes/pelicula.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Rutas para gestionar películas:
    - Listar, crear, actualizar y eliminar películas (API JSON).
    - Vista HTML protegida por sesión.

Notas:
    - Todas las rutas validan sesión de usuario antes de ejecutarse.
    - Los géneros deben existir previamente para asignarlos a una película.
"""

from flask import Blueprint, request, session, jsonify, render_template, redirect
from bson import ObjectId
from app.models.pelicula import Pelicula
from app.models.genero import Genero

pelicula_bp = Blueprint("pelicula", __name__, url_prefix="/pelicula")

@pelicula_bp.before_request
def proteger_sesion():
    """
    Middleware que valida sesión antes de procesar la ruta.
    Si no hay sesión activa, devuelve 401 o redirige.
    """
    if "usuario" not in session:
        if request.path.endswith(".json") or request.is_json:
            return jsonify({"mensaje": "No autorizado"}), 401
        return redirect("/")

@pelicula_bp.route("/", methods=["GET"])
def list_movies():
    """
    Devuelve un listado de todas las películas con sus datos y género.

    Returns:
        list: Lista de diccionarios con datos de cada película.
    """
    arr = []
    for p in Pelicula.objects():
        arr.append({
            "id": str(p.id),
            "codigo": p.codigo,
            "titulo": p.titulo,
            "protagonista": p.protagonista,
            "duracion": p.duracion,
            "resumen": p.resumen,
            "foto": p.foto,
            "genero": {
                "id": str(p.genero.id),
                "nombre": p.genero.nombre
            } if p.genero else {"id": "", "nombre": "N/A"}
        })
    return jsonify(arr)

@pelicula_bp.route("/", methods=["POST"])
def add_movie():
    """
    Crea una nueva película a partir de datos JSON.

    Returns:
        dict: Mensaje de confirmación o error.
    """
    d = request.get_json()
    genero_id = d.pop("genero", None)
    if not genero_id:
        return jsonify({"mensaje": "Género requerido"}), 400

    g = Genero.objects(id=genero_id).first()
    if not g:
        return jsonify({"mensaje": "Género inválido"}), 404

    try:
        p = Pelicula(
            codigo=int(d.get("codigo", 0)),
            titulo=d.get("titulo", ""),
            protagonista=d.get("protagonista", ""),
            duracion=int(d.get("duracion", 0)),
            resumen=d.get("resumen", ""),
            foto=d.get("foto", ""),
            genero=g
        )
        p.save()
        return jsonify({"mensaje": "Película creada"}), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error al crear: {str(e)}"}), 500

@pelicula_bp.route("/<id>", methods=["PUT"])
def upd_movie(id):
    """
    Actualiza una película existente.

    Args:
        id (str): ID de la película.

    Returns:
        dict: Mensaje de confirmación o error.
    """
    d = request.get_json()
    p = Pelicula.objects(id=ObjectId(id)).first()
    if not p:
        return jsonify({"mensaje": "No existe"}), 404

    g = Genero.objects(id=d.get("genero")).first()
    if not g:
        return jsonify({"mensaje": "Género inválido"}), 404

    try:
        p.codigo = int(d.get("codigo", p.codigo))
        p.titulo = d.get("titulo", p.titulo)
        p.protagonista = d.get("protagonista", p.protagonista)
        p.duracion = int(d.get("duracion", p.duracion))
        p.resumen = d.get("resumen", p.resumen)
        p.foto = d.get("foto", p.foto)
        p.genero = g
        p.save()
        return jsonify({"mensaje": "Película actualizada"})
    except Exception as e:
        return jsonify({"mensaje": f"Error al actualizar: {str(e)}"}), 500

@pelicula_bp.route("/<id>", methods=["DELETE"])
def del_movie(id):
    """
    Elimina una película por ID.

    Args:
        id (str): ID de la película.

    Returns:
        dict: Mensaje de confirmación o error.
    """
    p = Pelicula.objects(id=ObjectId(id)).first()
    if not p:
        return jsonify({"mensaje": "No existe"}), 404
    p.delete()
    return jsonify({"mensaje": "Película eliminada"})

@pelicula_bp.route("/vista", methods=["GET"])
def vista_peliculas():
    """
    Renderiza la vista HTML de gestión de películas.

    Returns:
        str: HTML renderizado.
    """
    return render_template("peliculas.html")
