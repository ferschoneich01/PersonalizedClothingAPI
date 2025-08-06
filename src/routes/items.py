from flask import Blueprint,jsonify, request
#entities

from models.entities.items import items

from models.entities.person import person

#models
from models.itemsModel import itemsModel

main = Blueprint('items_blueprint', __name__)

@main.route('/', methods=['GET'])
def get_items():
    try:
        items_list = itemsModel.get_items()
        return jsonify(items_list)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/<id_item>')
def get_itembyId(item):
    try:
        i = itemsModel.get_itembyId(item)
        if i != None:
            return jsonify(i)
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_item():
    try:

        id_item = request.json["id_item"]
        name = request.json["name"]
        description = request.json["description"]
        image = request.json["image"]
        price = float(request.json["price"])
        clasification = int(request.json["clasification"])
        category = int(request.json["category"])
        status_item = int(request.json["status_item"])
                                   

        #set data
        item = items(id_item=0,name=name, description=description,image=image,price=price,clasification=clasification,category=category,status_item=1)
       
        affected_rows = itemsModel.add_user(item)

        if affected_rows == 1:
            return jsonify({"message":"articulo registrado exitosamente!"})
        else:
            return jsonify({'message': "Error al registrar"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update/<item>', methods=['PUT'])
def update_item(item):
    try:
        #userdata
        id_item = int(request.json["id_item"])
        name = request.json["name"]
        description = request.json["description"]
        image = request.json["image"]
        price = float(request.json["price"])
        clasification = int(request.json["clasification"])
        category = int(request.json["category"])

        item = items(id_item=id_item,name=name, description=description,image=image,price=price,clasification=clasification,category=category,status_item=1)
       
        affected_rows = itemsModel.update_user(item)

        if affected_rows == 1:
            return jsonify(item.id_item)
        else:
            return jsonify({'message': "No item updated"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/delete/<id>', methods=['DELETE'])
def delete_item(id):
    try:
        item = items(id_item=id)

        affected_rows = itemsModel.delete_item(item)

        if affected_rows == 1:
            return jsonify(item.id_item)
        else:
            return jsonify({'message': "No item deleted"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500