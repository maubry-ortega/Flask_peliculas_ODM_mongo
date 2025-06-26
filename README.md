# Películas Flask Mongo

Este proyecto es una aplicación web desarrollada con Flask y MongoDB para la gestión de películas y géneros.

## Características
- CRUD de películas
- CRUD de géneros
- Interfaz web sencilla
- Uso de MongoDB como base de datos

## Estructura del proyecto
```
app.py                # Archivo principal de la aplicación Flask
models/               # Modelos de datos (película, género)
routes/               # Rutas de la aplicación (película, género)
static/               # Archivos estáticos (CSS, JS, imágenes)
templates/            # Plantillas HTML
```

## Requisitos
- Python 3.10+
- Flask
- flask_mongoengine

## Instalación
1. Clona el repositorio:
   ```sh
   git clone git@github.com:maubry-ortega/Flask_peliculas_ODM_mongo.git
   cd Flask_peliculas_ODM_mongo
   ```
2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
3. Asegúrate de tener MongoDB en ejecución.

## Ejecución
```sh
python app.py
```
La aplicación estará disponible en `http://localhost:5000`.

## Autor
- VolleyDevByMaubry