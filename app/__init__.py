# VolleyDevByMaubry [2/∞] - La simplicidad es el mayor nivel de sofisticación.

"""
Archivo: app/__init__.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Configuración principal de la aplicación Flask, incluyendo:
    - Conexión a MongoDB mediante MongoEngine.
    - Configuración de CORS.
    - Registro de Blueprints.
    - Inyección de variables globales (como reCAPTCHA).
    - Configuración de expiración automática de sesión.

Notas:
    - La duración de la sesión se define con permanent_session_lifetime.
    - session.permanent = True debe establecerse en la ruta de login.
"""

import os
from datetime import timedelta
from flask import Flask, render_template, session
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from dotenv import load_dotenv

# Instancia global de la base de datos
db = MongoEngine()

def create_app():
    """
    Crea y configura la instancia de la aplicación Flask.

    Returns:
        Flask: Aplicación Flask configurada.
    """
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    app.secret_key = os.getenv("SECRET_KEY")

    app.config['MONGODB_SETTINGS'] = {
        'db': os.getenv("DB_NAME"),
        'host': os.getenv("MONGO_URI")
    }

    db.init_app(app)

    # Configuración de duración de la sesión
    app.permanent_session_lifetime = timedelta(minutes=30)

    # Registro de blueprints
    from app.routes.genero import genero_bp
    from app.routes.pelicula import pelicula_bp
    from app.routes.usuario import usuario_bp
    from app.routes.correo import correo_bp

    app.register_blueprint(genero_bp)
    app.register_blueprint(pelicula_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(correo_bp)

    @app.context_processor
    def inject_site_key():
        """
        Inyecta la variable site_key en el contexto de todas las plantillas.

        Returns:
            dict: Diccionario con la clave 'site_key' para reCAPTCHA.
        """
        return {"site_key": os.getenv("RECAPTCHA_SITE_KEY")}

    @app.route("/")
    def home():
        """
        Ruta base. Redirige a login si el usuario no está autenticado.

        Returns:
            str: HTML renderizado.
        """
        if "usuario" not in session:
            return render_template("login.html")
        return render_template("home.html")

    return app

app = create_app()
