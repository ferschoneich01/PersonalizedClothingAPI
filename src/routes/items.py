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


@main.route('/category/<int:category>', methods=['GET'])
def get_items_by_category_only(category):
    try:
        items_list = itemsModel.get_items_by_category_only(category)
        return jsonify(items_list)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/clasification/<int:clasification>', methods=['GET'])
def get_items_by_clasification_only(clasification):
    try:
        items_list = itemsModel.get_items_by_clasification_only(clasification)
        return jsonify(items_list)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_item():
    try:
        name          = request.json["name"]
        description   = request.json["description"]
        price         = float(request.json["price"])
        clasification = int(request.json["clasification"])
        category      = int(request.json["category"])
        status_item   = int(request.json.get("status_item", 1))

        # Soporte para múltiples imágenes (hasta 5)
        raw_images = request.json.get("images", [])
        if not raw_images and request.json.get("image"):
            raw_images = [request.json.get("image")]

        images_list = [img.strip() for img in raw_images if isinstance(img, str) and img.strip()][:5]
        primary_image = images_list[0] if images_list else request.json.get("image", "")

        item = items(
            id_item=0, name=name, description=description, image=primary_image,
            price=price, clasification=clasification, category=category,
            status_item=status_item
        )

        affected_rows = itemsModel.add_item(item, images=images_list)

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
        price         = float(request.json["price"])
        clasification = int(request.json["clasification"])
        category      = int(request.json["category"])

        # Soporte para múltiples imágenes (hasta 5)
        raw_images = request.json.get("images", [])
        if not raw_images and request.json.get("image"):
            raw_images = [request.json.get("image")]

        images_list = [img.strip() for img in raw_images if isinstance(img, str) and img.strip()][:5]
        primary_image = images_list[0] if images_list else request.json.get("image", "")

        item_obj = items(
            id_item=id_item, name=name, description=description, image=primary_image,
            price=price, clasification=clasification, category=category,
            status_item=1
        )

        affected_rows = itemsModel.update_item(item_obj, images=images_list)

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


# ─────────────────────────────────────────────────────────────
# Endpoints de Categorías (Clasificación de Prendas)
# ─────────────────────────────────────────────────────────────

@main.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = itemsModel.get_categories()
        return jsonify(categories)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/categories/add', methods=['POST'])
def add_category():
    try:
        data = request.get_json(silent=True) or {}
        name = data.get("name", "").strip()
        if not name:
            return jsonify({'message': 'El nombre de la categoría es obligatorio.'}), 400

        created = itemsModel.add_category(name)
        return jsonify({
            'message': f'Categoría "{name}" agregada con éxito.',
            'category': created
        }), 201
    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/categories/update/<int:id_clasification>', methods=['PUT'])
def update_category(id_clasification):
    try:
        data = request.get_json(silent=True) or {}
        name = data.get("name", "").strip()
        if not name:
            return jsonify({'message': 'El nombre de la categoría es obligatorio.'}), 400

        updated = itemsModel.update_category(id_clasification, name)
        if updated:
            return jsonify({
                'message': 'Categoría actualizada con éxito.',
                'category': updated
            }), 200
        else:
            return jsonify({'message': 'Categoría no encontrada.'}), 404
    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/categories/delete/<int:id_clasification>', methods=['DELETE'])
def delete_category(id_clasification):
    try:
        affected = itemsModel.delete_category(id_clasification)
        if affected == 1:
            return jsonify({
                'message': 'Categoría eliminada con éxito.',
                'id_clasification': id_clasification
            }), 200
        else:
            return jsonify({'message': 'Categoría no encontrada.'}), 404
    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500