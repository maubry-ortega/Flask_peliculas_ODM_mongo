# VolleyDevByMaubry [2/∞] - Configuración completa Flask + MongoEngine + reCAPTCHA inyectado

from flask import Flask, render_template, session
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = MongoEngine()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)
    app.secret_key = os.getenv("SECRET_KEY")

    app.config['MONGODB_SETTINGS'] = {
        'db': os.getenv("DB_NAME"),
        'host': os.getenv("MONGO_URI")
    }
    db.init_app(app)

    # Blueprints
    from app.routes.genero import genero_bp
    from app.routes.pelicula import pelicula_bp
    from app.routes.usuario import usuario_bp
    from app.routes.correo import correo_bp

    app.register_blueprint(genero_bp)
    app.register_blueprint(pelicula_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(correo_bp)

    # Inyectar el site_key globalmente en todas las plantillas
    @app.context_processor
    def inject_site_key():
        return {"site_key": os.getenv("RECAPTCHA_SITE_KEY")}

    @app.route("/")
    def home():
        if "usuario" not in session:
            return render_template("login.html")
        return render_template("home.html")

    return app
