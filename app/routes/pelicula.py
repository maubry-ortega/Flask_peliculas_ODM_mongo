# VolleyDevByMaubry [6/∞]
from flask import Blueprint, request, session, jsonify
from bson import ObjectId
from app.models.pelicula import Pelicula
from app.models.genero import Genero

pelicula_bp = Blueprint("pelicula", __name__, url_prefix="/pelicula")

@pelicula_bp.before_request
def sede():
    if "usuario" not in session:
        return jsonify({"mensaje": "No autorizado"}), 401

@pelicula_bp.route("/", methods=["GET"])
def list_movies():
    arr = []
    for p in Pelicula.objects():
        arr.append({
            "id": str(p.id), "codigo": p.codigo, "titulo": p.titulo,
            "protagonista": p.protagonista, "duracion": p.duracion,
            "resumen": p.resumen, "foto": p.foto,
            "genero": {"id": str(p.genero.id), "nombre": p.genero.nombre} if p.genero else {"id": "", "nombre": "N/A"}
        })
    return jsonify(arr)

@pelicula_bp.route("/", methods=["POST"])
def add_movie():
    d = request.get_json()
    genero_id = d.pop("genero", None)
    if not genero_id:
        return jsonify({"mensaje": "Género requerido"}), 400

    g = Genero.objects(id=genero_id).first()
    if not g:
        return jsonify({"mensaje": "Género inválido"}), 404

    try:
        p = Pelicula(
            codigo=int(d["codigo"]),
            titulo=d["titulo"],
            protagonista=d["protagonista"],
            duracion=int(d["duracion"]),
            resumen=d["resumen"],
            foto=d.get("foto", ""),
            genero=g
        )
        p.save()
        return jsonify({"mensaje": "Película creada"}), 201
    except Exception as e:
        return jsonify({"mensaje": str(e)}), 500

@pelicula_bp.route("/<id>", methods=["PUT"])
def upd_movie(id):
    d = request.get_json()
    p = Pelicula.objects(id=ObjectId(id)).first()
    if not p:
        return jsonify({"mensaje": "No existe"}), 404

    g = Genero.objects(id=d["genero"]).first()
    if not g:
        return jsonify({"mensaje": "Género inválido"}), 404

    try:
        p.codigo = int(d["codigo"])
        p.titulo = d["titulo"]
        p.protagonista = d["protagonista"]
        p.duracion = int(d["duracion"])
        p.resumen = d["resumen"]
        p.foto = d.get("foto", "")
        p.genero = g
        p.save()
        return jsonify({"mensaje": "Película actualizada"})
    except Exception as e:
        return jsonify({"mensaje": str(e)}), 500

@pelicula_bp.route("/<id>", methods=["DELETE"])
def del_movie(id):
    p = Pelicula.objects(id=ObjectId(id)).first()
    if not p:
        return jsonify({"mensaje": "No existe"}), 404
    p.delete()
    return jsonify({"mensaje": "Película eliminada"})
