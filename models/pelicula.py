from mongoengine import *
from models.genero import Genero

class Pelicula(Document):
    codigo       = IntField(required=True, unique=True)
    titulo       = StringField(max_length=80, required=True)
    protagonista = StringField(max_length=50, required=True)
    duracion     = IntField(min_value = 30, max_value = 200, required=True)
    resumen      = StringField(required=True)
    foto         = StringField()
    genero       = ReferenceField(Genero)
    
    def __str__(self):
        return self.titulo