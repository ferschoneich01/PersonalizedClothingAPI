from flask import Flask, render_template, url_for, request, flash, redirect, sessions, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from funciones import *
from sqlalchemy.sql import text
#objeto
from model.users import users

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Datos de ejemplo (lista de tareas)
tasks = [
    {"id": 1, "title": "Tarea 1", "done": False},
    {"id": 2, "title": "Tarea 2", "done": True},
]

usersList = []
# Ruta para obtener todas las tareas (GET)
@app.route('/getUsers', methods=['GET'])
def getUsers():

    usersDBList = db.execute(
            text("SELECT * FROM users limit 100")).fetchall()

    for i in range(len(usersDBList)):
        user = users(id_user=usersDBList[i][0],username=usersDBList[i][1],
                     password=usersDBList[i][2],email=usersDBList[i][3],
                     person=usersDBList[i][4],role=usersDBList[i][5])
        
        usersList.append(user.to_json())
        i+=1

    return jsonify({"users": usersList})

# Ruta para obtener una tarea por su ID (GET)
@app.route('/getUser/<string:username>', methods=['GET'])
def get_user(username):
    print(limpiarString(username))
    user = db.execute(
            text("SELECT * FROM users WHERE username = '"+str(username)+"'")).fetchall()

    user = next((user for u in user if user[0][1] == username), None)
    
    if user is not None:
        return jsonify({"user": user})
    
    return jsonify({"error": "El usuario no existe"}, 404)

# Ruta para crear una nueva tarea (POST)
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if 'title' in data:
        new_task = {
            "id": len(tasks) + 1,
            "title": data['title'],
            "done": False
        }
        tasks.append(new_task)
        return jsonify({"task": new_task}), 201
    return jsonify({"error": "Falta el título de la tarea"}, 400)

# Ruta para actualizar una tarea por su ID (PUT)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is not None and 'title' in data:
        task['title'] = data['title']
        task['done'] = data.get('done', task['done'])
        return jsonify({"task": task})
    return jsonify({"error": "Tarea no encontrada o falta el título de la tarea"}, 404)

# Ruta para eliminar una tarea por su ID (DELETE)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is not None:
        tasks.remove(task)
        return jsonify({"result": True})
    return jsonify({"error": "Tarea no encontrada"}, 404)

if __name__ == '__main__':
    app.run(debug=True)
