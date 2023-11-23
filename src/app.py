from flask import Flask
#objeto
from routes import users
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={"*": {"origins": "http://localhost:5000"}})

def page_not_found(error):
    return "<h1>Not found page</h1>", 404

if __name__ == '__main__':   
    app.register_blueprint(users.main, url_prefix='/api/users')
    app.register_error_handler(404, page_not_found)
    app.run()
