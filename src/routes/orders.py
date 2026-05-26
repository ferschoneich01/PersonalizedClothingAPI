from flask import Blueprint, jsonify, request
from models.entities.orders import orders
from models.ordersModel import ordersModel

main = Blueprint('orders_blueprint', __name__)


@main.route('/', methods=['GET'])
def get_orders():
    try:
        orders_list = ordersModel.get_orders()
        return jsonify(orders_list)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/details', methods=['GET'])
def get_orderDetails():
    try:
        orders_list = ordersModel.get_orderDetails()
        return jsonify(orders_list)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/shippings', methods=['GET'])
def get_shipping():
    try:
        orders_list = ordersModel.get_shipping()
        return jsonify(orders_list)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<username>', methods=['GET'])
def get_userbyUsername(username):
    try:
        orders_list = ordersModel.get_userbyUsername(username)
        if orders_list:
            return jsonify(orders_list)
        else:
            return jsonify({'message': 'Sin órdenes para este usuario'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_order():
    try:
        address       = request.json["address"]
        username      = request.json["username"]
        carListItems  = request.json["carListItems"]

        affected_rows = ordersModel.add_order(address, username, carListItems)

        if affected_rows == 1:
            return jsonify({"message": "Orden registrada exitosamente!"}), 201
        else:
            return jsonify({'message': "Error al registrar la orden"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/changeStatus', methods=['PUT'])
def changeStatus():
    try:
        id_order = request.json["id_order"]
        status   = request.json["status"]

        affected_rows = ordersModel.changeStatus(id_order, status)

        if affected_rows == 1:
            return jsonify({"message": "Estado actualizado correctamente"})
        else:
            return jsonify({'message': "Orden no encontrada"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500