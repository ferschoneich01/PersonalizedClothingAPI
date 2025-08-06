from flask import Blueprint,jsonify, request

#entities
from models.entities.orders import orders

#models
from models.ordersModel import ordersModel

main = Blueprint('orders_blueprint', __name__)

@main.route('/', methods=['GET'])
def get_orders():
    try:
        ordersList = ordersModel.get_orders()
        return jsonify(ordersList)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/shippings', methods=['GET'])
def get_shipping():
    try:
        ordersList = ordersModel.get_shipping()
        return jsonify(ordersList)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/<username>')
def get_userbyUsername(username):
    try:
        ordersList = ordersModel.get_userbyUsername(username)
        if ordersList != None:
            return jsonify(ordersList)
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_order():
    try:

        address = request.json["address"]
        username = request.json["username"]
        carListItems = request.json["carListItems"]

        affected_rows = ordersModel.add_order(address,username,carListItems)

        if affected_rows == 1:
            return jsonify({"message":"usuario registrado exitosamente!"})
        else:
            return jsonify({'message': "Error on insert"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

""""
@main.route('/update/<id>', methods=['PUT'])
def update_order(id):
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
        return jsonify({'message': str(ex)}), 500"""


@main.route('/changeStatus', methods=['PUT'])
def changeStatus():
    try:
        affected_rows = ordersModel.changeStatus(request.json["id_order"],request.json["status"])

        if affected_rows == 1:
            return jsonify({"message":"Estado Cambiado"})
        else:
            return jsonify({'message': "No order update"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500