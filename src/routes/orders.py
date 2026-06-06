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
        address        = request.json["address"]
        username       = request.json["username"]
        carListItems   = request.json["carListItems"]
        paymethod      = request.json.get("paymethod", "Efectivo")
        id_canal       = request.json.get("id_canal_de_ventas", 1)
        pedidoNombre   = request.json.get("pedidoNombre", None)
        cedula         = request.json.get("cedula", None)
        pedidoTelefono = request.json.get("pedidoTelefono", None)

        id_order = ordersModel.add_order(
            address=address,
            username=username,
            carListItems=carListItems,
            paymethod=paymethod,
            id_canal_de_ventas=id_canal,
            pedidoNombre=pedidoNombre,
            cedula=cedula,
            pedidoTelefono=pedidoTelefono
        )

        if id_order:
            return jsonify({"message": "Orden registrada exitosamente!", "id_order": id_order}), 201
        else:
            return jsonify({'message': "Error al registrar la orden"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/upload-voucher', methods=['PUT'])
def upload_voucher():
    """Guarda la URL del comprobante de depósito para una orden."""
    try:
        id_order    = request.json["id_order"]
        voucher_url = request.json["voucher_url"]

        affected_rows = ordersModel.upload_voucher(id_order, voucher_url)

        if affected_rows == 1:
            return jsonify({"message": "Comprobante guardado correctamente"})
        else:
            return jsonify({'message': "Orden no encontrada"}), 404

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