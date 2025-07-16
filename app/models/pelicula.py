# VolleyDevByMaubry [8/∞] - Los detalles importan tanto como la estructura.

"""
Archivo: app/models/pelicula.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Modelo de datos para películas utilizando MongoEngine.
    Incluye referencia al género relacionado.

Notas:
    - La colección se llama 'pelicula'.
    - 'codigo' es único y obligatorio.
    - 'duracion' tiene validación de rango.
    - 'genero' es una referencia al modelo Genero.
"""

from mongoengine import Document, IntField, StringField, ReferenceField
from app.models.genero import Genero

class Pelicula(Document):
    """
    Modelo de Película.

    Campos:
        codigo (int): Código único de la película.
        titulo (str): Título de la película.
        protagonista (str): Nombre del protagonista principal.
        duracion (int): Duración en minutos (entre 30 y 200).
        resumen (str): Resumen o sinopsis de la película.
        foto (str): URL o ruta de la imagen de la película.
        genero (Genero): Referencia al género asociado.
    """
    codigo = IntField(required=True, unique=True)
    titulo = StringField(required=True)
    protagonista = StringField(required=True)
    duracion = IntField(required=True, min_value=30, max_value=200)
    resumen = StringField(required=True)
    foto = StringField()
    genero = ReferenceField(Genero)

    meta = {
        'collection': 'pelicula'
    }
