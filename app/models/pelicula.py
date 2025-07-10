from mongoengine import Document, IntField, StringField, ReferenceField
from app.models.genero import Genero

class Pelicula(Document):
    codigo = IntField(required=True, unique=True)
    titulo = StringField(required=True)
    protagonista = StringField(required=True)
    duracion = IntField(required=True, min_value=30, max_value=200)
    resumen = StringField(required=True)
    foto = StringField()
    genero = ReferenceField(Genero)
