# VolleyDevByMaubry [7/∞] - La base de todo está en los modelos.

"""
Archivo: app/models/genero.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Modelo de datos para géneros cinematográficos.
    Utiliza MongoEngine para la definición del documento en MongoDB.

Notas:
    - La colección se llama 'genero'.
    - El campo 'nombre' es único y obligatorio.
"""

from mongoengine import Document, StringField

class Genero(Document):
    """
    Modelo de Género para películas.

    Campos:
        nombre (str): Nombre del género (único y obligatorio).
    """
    nombre = StringField(required=True, unique=True)

    meta = {
        'collection': 'genero'
    }
