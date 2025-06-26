from flask import request
from models.pelicula import Pelicula
from models.genero import Genero
from app import app, db
from bson import ObjectId

@app.route('/pelicula', methods=['POST'])
def add_pelicula():
    try:
        mensaje = None
        estado = False
        if request.method == 'POST':
            datos = request.get_json(force=True)
            genero = Genero.objects(id=ObjectId(datos['genero'])).first()
            if genero is not None:
                pelicula = Pelicula(**datos)
                pelicula.save()
                estado = True
                mensaje = 'Pelicula creada correctamente'
            else:
                mensaje = 'genero no existe'
        else:
            mensaje = 'Metodo no permitido'
    except Exception as e:
        mensaje = str(e)
        if "duplicate key" in mensaje:
            mensaje = 'Ya existe una pelicula con ese codigo'
        
    return {'estado': estado, 'mensaje': mensaje}, 201

@app.route('/pelicula', methods=['GET'])
def listar_peliculas():
    try:
        
        mensaje = None
        peliculas = Pelicula.objects()
        
    except Exception as e:
        mensaje = str(e)
    return {'mensaje': mensaje, 'peliculas': peliculas}, 200

@app.route('/pelicula', methods=['PUT'])
def update_pelicula():
    try:
        mensaje = None
        estado = False
        if request.method == 'PUT':
            datos = request.get_json(force=True)
            pelicula = Pelicula.objects(id=ObjectId(datos['id'])).first()
            if pelicula is not None:
                pelicula.codigo       = datos['codigo']
                pelicula.titulo       = datos['titulo']
                pelicula.protagonista = datos['protagonista']
                pelicula.duracion     = datos['duracion']
                pelicula.resumen      = datos['resumen']
                pelicula.foto         = datos['foto']
                pelicula.genero       = ObjectId(datos['genero'])
                pelicula.save()
                estado = True
                mensaje = 'Pelicula actualizada correctamente'
            else:
                mensaje = 'Pelicula no existe'
        else:
            mensaje = 'Metodo no permitido'
    except Exception as e:
        mensaje = str(e)
        
    return {'estado': estado, 'mensaje': mensaje}

@app.route('/pelicula/<id>', methods=['DELETE'])
def delete_pelicula(id):
    try:
        mensaje = None
        estado  = False
        pelicula = Pelicula.objects(id=ObjectId(id)).first()
        if pelicula is not None:
            pelicula.delete()
            estado  = True
            mensaje = 'Pelicula eliminada correctamente'
        else:
            mensaje = 'Pelicula no existe'
    except Exception as e:
        mensaje = str(e)
        
    return {'estado': estado, 'mensaje': mensaje}

@app.route('/pelicula/<id>', methods=['GET'])
def get_pelicula(id):
    try:
        mensaje = None
        pelicula = Pelicula.objects(id=ObjectId(id)).first()
        if pelicula is not None:
            mensaje = 'Pelicula encontrada'
        else:
            mensaje = 'Pelicula no existe'
    except Exception as e:
        mensaje = str(e)
        
    return {'mensaje': mensaje, 'pelicula': pelicula}, 200