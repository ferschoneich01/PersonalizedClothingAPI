from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models.entities.users import users
from models.entities.person import person
from models.usersModel import usersModel
import smtplib
from email.mime.text import MIMEText
import random
import string

main = Blueprint('users_blueprint', __name__)


@main.route('/', methods=['GET'])
def get_users():
    try:
        users_list = usersModel.get_users()
        return jsonify(users_list)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<username>', methods=['GET'])
def get_userbyId(username):
    try:
        user = usersModel.get_userbyId(username)
        if user:
            return jsonify(user)
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        user_list = usersModel.get_userbyId(username)
        if user_list and len(user_list) > 0:
            user = user_list[0]
            # Compare the hash
            if check_password_hash(user['password'], password):
                # Remove password hash before sending to frontend
                user_copy = dict(user)
                del user_copy['password']
                return jsonify({'message': 'Login exitoso', 'user': user_copy}), 200
            else:
                return jsonify({'message': 'Contraseña incorrecta'}), 401
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/recover_password', methods=['POST'])
def recover_password():
    try:
        email = request.json.get('email')
        
        # We need to verify if a user has this email. 
        # In a real app we'd query by email, but for now we fetch all and filter or just let SP handle it.
        # But we need to send the email with the new password.
        users_list = usersModel.get_users()
        user_exists = next((u for u in users_list if u['email'] == email), None)
        
        if not user_exists:
            return jsonify({'message': 'No hay ninguna cuenta asociada a este correo.'}), 404
            
        # Generate random password
        chars = string.ascii_letters + string.digits
        new_password = ''.join(random.choice(chars) for _ in range(8))
        hashed_password = generate_password_hash(new_password)
        
        # Update in database
        usersModel.reset_password(email, hashed_password)
        
        # Send email
        try:
            import os
            # Obtiene las credenciales del archivo .env
            smtp_server = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
            smtp_port = int(os.environ.get("MAIL_PORT", 587))
            sender_email = os.environ.get("MAIL_USERNAME", "tu-correo@gmail.com")
            sender_password = os.environ.get("MAIL_PASSWORD", "tu-contraseña-de-aplicacion")
            
            msg = MIMEText(f"Hola,\n\nTu nueva contraseña temporal es: {new_password}\n\nPor favor, inicia sesión y cámbiala lo antes posible.")
            msg['Subject'] = 'Recuperación de Contraseña - Personalized Clothing'
            msg['From'] = sender_email
            msg['To'] = email
            
            # Intenta enviar el correo si están configuradas las credenciales
            if sender_email != "tu-correo@gmail.com":
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, msg.as_string())
                server.quit()
                print(f"Correo enviado exitosamente a {email}")
            else:
                print(f"FALTA CONFIGURAR CREDENCIALES - MOCK EMAIL A {email}: Tu nueva clave es {new_password}")
            
            return jsonify({'message': 'Se ha enviado una nueva contraseña a tu correo.'}), 200
        except Exception as mail_ex:
            print("Mail Error:", mail_ex)
            return jsonify({'message': 'La contraseña se reseteó pero falló el envío del correo. Revisa la consola.'}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_user():
    try:
        username  = request.json["username"]
        password  = generate_password_hash(request.json["password"])
        email     = request.json["email"]
        cedula    = request.json["cedula"]
        name      = request.json["name"]
        lastname  = request.json["lastname"]
        birthday  = request.json["birthday"]
        phone     = request.json["phone"]
        city      = request.json["city"]
        sex       = request.json["sex"]

        user_obj = users(
            id_user=0, username=username, password=password,
            email=email, person=None, role=2, status_user=1
        )
        person_obj = person(
            id_person=0, cedula=cedula, name=name, lastname=lastname,
            birthday=birthday, phone=phone, country='Nicaragua', city=city, sex=sex
        )

        affected_rows = usersModel.add_user(user_obj, person_obj)

        if affected_rows == 1:
            return jsonify({"message": "Usuario registrado exitosamente!"}), 201
        else:
            return jsonify({'message': "Error al registrar"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        password    = request.json['password']
        role        = int(request.json['role'])
        email       = request.json['email']
        status_user = request.json['status_user']

        # Corrección: id_user=id  (antes decía is_user=id — typo)
        user = users(id_user=id, password=password, role=role,
                     email=email, status_user=status_user)

        affected_rows = usersModel.update_user(user)

        if affected_rows == 1:
            return jsonify({"id_user": user.id_user})
        else:
            return jsonify({'message': "Usuario no encontrado"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = users(id_user=id)

        affected_rows = usersModel.delete_user(user)

        if affected_rows == 1:
            return jsonify({"id_user": id})
        else:
            return jsonify({'message': "Usuario no encontrado"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500