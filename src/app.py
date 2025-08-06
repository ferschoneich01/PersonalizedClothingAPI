from flask import Flask, Blueprint
#objeto
from routes import users, orders, messages, items
from flask_cors import CORS

app = Flask(__name__)

#CORS(app, resources={"*": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


def page_not_found(error):
    return "<h1>Not found page</h1>", 404

if __name__ == '__main__':   
    app.register_error_handler(404, page_not_found)
    app.register_blueprint(users.main, url_prefix='/api/users')
    app.register_blueprint(orders.main, url_prefix='/api/orders')
    app.register_blueprint(items.main, url_prefix='/api/items')
    app.register_blueprint(messages.main, url_prefix='/api/messages')
    app.run(host="0.0.0.0", port=8080, debug=True)
