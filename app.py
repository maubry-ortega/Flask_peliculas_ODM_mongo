from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './static/img'
app.config['MONGODB_SETTINGS'] = {
    'db' : 'peliculas',
    'host': os.environ.get('URI'),
    #'port': 27017
    }

db = MongoEngine(app)

if __name__ == '__main__':
    from routes.genero import *
    from routes.pelicula import *
    app.run(debug=True, port='5400', host='0.0.0.0')