from flask import request
from models.genero import Genero
from app import app, db

@app.route('/genero', methods=['GET'])
def listar_generos():
    try:
        mensaje = None
        Generos = Genero.objects()
        
    except Exception as e:
        mensaje = str(e)
    return {'mensaje': mensaje, 'generos': Generos}, 200

@app.route('/genero', methods=['POST'])
def add_genero():
    try:
        mensaje = None
        estado = False
        if request.method == 'POST':
            datos = request.get_json(force=True)
            genero = Genero(**datos)
            genero.save()
            estado = True
            mensaje = 'Genero creado correctamente'
        else:
            mensaje = 'Metodo no permitido'
        
    except Exception as e:
        mensaje = str(e)
    return {'estado': estado, 'mensaje': mensaje}, 201