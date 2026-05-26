from sqlalchemy.sql import text
from database import db
from .entities.items import items


class itemsModel():

    @classmethod
    def get_items(cls):
        try:
            items_list = []
            rows = db.execute(text("SELECT * FROM sp_get_items()")).fetchall()

            for row in rows:
                item = items(
                    id_item=row[0], name=row[1], description=row[2],
                    image=row[3], price=row[4], clasification=row[5],
                    category=row[6], status_item=row[7]
                )
                items_list.append(item.to_json())

            return items_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_itembyId(cls, id_item):
        try:
            items_list = []
            rows = db.execute(
                text("SELECT * FROM sp_get_item_by_id(:id_item)"),
                {"id_item": int(id_item)}
            ).fetchall()

            for row in rows:
                item = items(
                    id_item=row[0], name=row[1], description=row[2],
                    image=row[3], price=row[4], clasification=row[5],
                    category=row[6], status_item=row[7]
                )
                items_list.append(item.to_json())

            return items_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_itemsByCategory(cls, category, clasification):
        try:
            items_list = []
            rows = db.execute(
                text("SELECT * FROM sp_get_items_by_category(:category, :clasification)"),
                {"category": int(category), "clasification": int(clasification)}
            ).fetchall()

            for row in rows:
                item = items(
                    id_item=row[0], name=row[1], description=row[2],
                    image=row[3], price=row[4], clasification=row[5],
                    category=row[6], status_item=row[7]
                )
                items_list.append(item.to_json())

            return items_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_item(cls, item):
        try:
            db.execute(
                text("CALL sp_add_item(:name, :description, :image, :price, :clasification, :category)"),
                {
                    "name":          item.name,
                    "description":   item.description,
                    "image":         item.image,
                    "price":         item.price,
                    "clasification": item.clasification,
                    "category":      item.category,
                }
            )
            db.commit()
            return 1
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def update_item(cls, item):
        try:
            db.execute(
                text("CALL sp_update_item(:id_item, :name, :description, :image, :price, :clasification, :category)"),
                {
                    "id_item":       item.id_item,
                    "name":          item.name,
                    "description":   item.description,
                    "image":         item.image,
                    "price":         item.price,
                    "clasification": item.clasification,
                    "category":      item.category,
                }
            )
            db.commit()
            return 1
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def delete_item(cls, item):
        try:
            db.execute(
                text("CALL sp_delete_item(:id_item)"),
                {"id_item": item.id_item}
            )
            db.commit()
            return 1
        except Exception as ex:
            db.rollback()
            raise Exception(ex)