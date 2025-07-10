# VolleyDevByMaubry [4/∞]
from flask import Blueprint, request, session, jsonify
from app.models.genero import Genero

genero_bp = Blueprint("genero", __name__, url_prefix="/genero")

@genero_bp.before_request
def sede():
    if "usuario" not in session:
        return jsonify({"mensaje": "No autorizado"}), 401

@genero_bp.route("/", methods=["GET"])
def list_gen():
    return jsonify([{"id": str(g.id), "nombre": g.nombre} for g in Genero.objects()])

@genero_bp.route("/", methods=["POST"])
def add_gen():
    data = request.get_json()
    nuevo = Genero(nombre=data["nombre"])
    nuevo.save()
    return jsonify({"mensaje": "Género creado"}), 201

@genero_bp.route("/<id>", methods=["PUT"])
def upd_gen(id):
    gen = Genero.objects(id=id).first()
    if not gen: return jsonify({"mensaje":"No existe"}), 404
    gen.update(nombre=request.get_json()["nombre"])
    return jsonify({"mensaje": "Género actualizado"})

@genero_bp.route("/<id>", methods=["DELETE"])
def del_gen(id):
    gen = Genero.objects(id=id).first()
    if not gen: return jsonify({"mensaje":"No existe"}), 404
    gen.delete()
    return jsonify({"mensaje": "Género eliminado"})
