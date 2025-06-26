from mongoengine import *

class Genero(Document):
    nombre = StringField(max_length = 50 ,required=True, unique=True)
    
    def __str__(self):
        return self.nombre
    