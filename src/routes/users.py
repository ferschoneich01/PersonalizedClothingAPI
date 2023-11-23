from flask import Blueprint,jsonify, request
from werkzeug.security import generate_password_hash

#entities

from models.entities.users import users

from models.entities.person import person

#models
from models.usersModel import usersModel

main = Blueprint('users_blueprint', __name__)

@main.route('/', methods=['GET'])
def get_users():
    try:
        users = usersModel.get_users()
        return jsonify(users)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/<username>')
def get_userbyId(username):
    try:
        user = usersModel.get_userbyId(username)
        if user != None:
            return jsonify(user)
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_user():
    try:
        username = request.json["username"]
        password = generate_password_hash(request.json["password"])
        email = request.json["email"]
        cedula = request.json["cedula"]
        name = request.json["name"]
        lastname = request.json["lastname"]
        birthday = request.json["birthday"]
        phone = request.json["phone"]
        city = request.json["city"]
        sex = request.json["sex"]

        #set data
        user = users(id_user=0,username=username, password=password,email=email,person=None, role=2,status_user= 1)
       
        persondata = person(id_person=0, cedula=cedula,name=name,lastname=lastname,birthday=birthday,phone=phone,country='Nicaragua',city=city,sex=sex)

        affected_rows = usersModel.add_user(user,persondata)

        if affected_rows == 1:
            return jsonify({"message":"usuario registrado exitosamente!"})
        else:
            return jsonify({'message': "Error on insert"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update/<id>', methods=['PUT'])
def update_user(id):
    try:
        #userdata
        password = request.json['password']
        role = int(request.json['role'])
        email = request.json['email']
        status_user = request.json['status_user']

        user = users(is_user=id, password=password, role=role, email=email, status_user=status_user)

        affected_rows = usersModel.update_user(user)

        if affected_rows == 1:
            return jsonify(user.id_user)
        else:
            return jsonify({'message': "No user updated"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = users(id)

        affected_rows = usersModel.delete_user(user)

        if affected_rows == 1:
            return jsonify(user.id_user)
        else:
            return jsonify({'message': "No user deleted"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500