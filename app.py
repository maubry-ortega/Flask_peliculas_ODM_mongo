# VolleyDevByMaubry [1/∞] - El propósito del código es simplificar lo complejo, no al revés.

"""
Archivo: app.py
Autor: Maubry (VolleyDevByMaubry)

Descripción:
    Punto de entrada de la aplicación Flask.
    Inicializa la aplicación llamando a create_app() desde el paquete app.
    Ejecuta el servidor configurando puerto y modo debug según variables de entorno.

Uso:
    python app.py

Notas para desarrolladores:
    - No modificar directamente la lógica de la aplicación aquí. Toda la configuración
      y registros de blueprints están dentro de app/__init__.py.
    - Para entornos de producción, configurar FLASK_DEBUG=false y PORT según sea necesario.
    - Si se requiere modificar rutas o comportamiento global, hacerlo en app/config.py o en los blueprints.

Configuración de entorno recomendada:
    export FLASK_DEBUG=false
    export PORT=5400

Ejemplo de ejecución:
    $ python app.py
"""

from app import create_app
import os

# Crea la instancia de la aplicación Flask utilizando la factoría definida en app/__init__.py
app = create_app()

if __name__ == "__main__":
    # Lee el valor de FLASK_DEBUG desde variables de entorno. Por defecto, false.
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    # Lee el puerto desde PORT o usa 5400 por defecto
    port = int(os.getenv("PORT", 5400))

    # Ejecuta la aplicación
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
