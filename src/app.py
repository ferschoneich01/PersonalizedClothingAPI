from flask import Flask
from flask_cors import CORS
from routes import users, orders, messages, items
import os
from dotenv import load_dotenv

# Cargar variables de entorno (desde la carpeta src)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

# Configuración de CORS
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://personalizedclothing.fly.dev",
    "https://www.personalizedclothing.fly.dev",
]}})


# Registro de blueprints (fuera del if __main__ para compatibilidad con Gunicorn/Fly.io)
app.register_blueprint(users.main,    url_prefix='/api/users')
app.register_blueprint(orders.main,   url_prefix='/api/orders')
app.register_blueprint(items.main,    url_prefix='/api/items')
app.register_blueprint(messages.main, url_prefix='/api/messages')

from database import db

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()


@app.errorhandler(404)
def page_not_found(error):
    return {"message": "Ruta no encontrada"}, 404


@app.errorhandler(500)
def internal_error(error):
    return {"message": "Error interno del servidor"}, 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
