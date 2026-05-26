from flask import Blueprint, jsonify, request
from models.entities.items import items
from models.itemsModel import itemsModel

main = Blueprint('items_blueprint', __name__)


@main.route('/', methods=['GET'])
def get_items():
    try:
        items_list = itemsModel.get_items()
        return jsonify(items_list)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<int:id_item>', methods=['GET'])
def get_itembyId(id_item):
    try:
        item = itemsModel.get_itembyId(id_item)
        if item:
            return jsonify(item)
        else:
            return jsonify({'message': 'Artículo no encontrado'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/category/<int:category>/<int:clasification>', methods=['GET'])
def get_itemsByCategory(category, clasification):
    try:
        items_list = itemsModel.get_itemsByCategory(category, clasification)
        return jsonify(items_list)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_item():
    try:
        name          = request.json["name"]
        description   = request.json["description"]
        image         = request.json["image"]
        price         = float(request.json["price"])
        clasification = int(request.json["clasification"])
        category      = int(request.json["category"])
        status_item   = int(request.json.get("status_item", 1))

        item = items(
            id_item=0, name=name, description=description, image=image,
            price=price, clasification=clasification, category=category,
            status_item=status_item
        )

        affected_rows = itemsModel.add_item(item)

        if affected_rows == 1:
            return jsonify({"message": "Artículo registrado exitosamente!"}), 201
        else:
            return jsonify({'message': "Error al registrar"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update/<int:item>', methods=['PUT'])
def update_item(item):
    try:
        id_item       = int(request.json["id_item"])
        name          = request.json["name"]
        description   = request.json["description"]
        image         = request.json["image"]
        price         = float(request.json["price"])
        clasification = int(request.json["clasification"])
        category      = int(request.json["category"])

        item_obj = items(
            id_item=id_item, name=name, description=description, image=image,
            price=price, clasification=clasification, category=category,
            status_item=1
        )

        affected_rows = itemsModel.update_item(item_obj)

        if affected_rows == 1:
            return jsonify({"id_item": item_obj.id_item})
        else:
            return jsonify({'message': "Artículo no encontrado"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/delete/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        item = items(id_item=id, name=None, description=None, image=None,
                     price=None, clasification=None, category=None, status_item=None)

        affected_rows = itemsModel.delete_item(item)

        if affected_rows == 1:
            return jsonify({"id_item": id})
        else:
            return jsonify({'message': "Artículo no encontrado"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500