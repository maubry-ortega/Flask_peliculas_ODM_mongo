from mongoengine import Document, StringField

class Genero(Document):
    nombre = StringField(required=True, unique=True)
