from sqlalchemy.sql import text
from database import db
from .entities.items import items


class itemsModel():

    @classmethod
    def _build_items_response(cls, rows):
        if not rows:
            return []
        try:
            img_rows = db.execute(text("""
                SELECT id_item, image_url, position, is_primary 
                FROM item_images 
                ORDER BY id_item, position ASC
            """)).fetchall()
            images_by_item = {}
            for ir in img_rows:
                item_id = ir[0]
                url = ir[1]
                if item_id not in images_by_item:
                    images_by_item[item_id] = []
                images_by_item[item_id].append(url)
        except Exception:
            images_by_item = {}

        items_list = []
        for row in rows:
            item = items(
                id_item=row[0], name=row[1], description=row[2],
                image=row[3], price=row[4], clasification=row[5],
                category=row[6], status_item=row[7]
            )
            item_dict = item.to_json()
            item_imgs = images_by_item.get(item.id_item, [])
            if not item_imgs and item.image:
                item_imgs = [item.image]
            item_dict["images"] = item_imgs
            if item_imgs:
                item_dict["image"] = item_imgs[0]
            items_list.append(item_dict)

        return items_list

    @classmethod
    def get_items(cls):
        try:
            rows = db.execute(text("SELECT * FROM sp_get_items()")).fetchall()
            return cls._build_items_response(rows)
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_itembyId(cls, id_item):
        try:
            rows = db.execute(
                text("SELECT * FROM sp_get_item_by_id(:id_item)"),
                {"id_item": int(id_item)}
            ).fetchall()
            return cls._build_items_response(rows)
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_itemsByCategory(cls, category, clasification):
        try:
            cat_int = int(category)
            clas_int = int(clasification)

            # En la BD: category = Género (1: Hombre, 2: Mujer)
            #           clasification = Prenda (1: Camisetas, 2: Sudadera, 3: Croptop, 4: Sueter, etc.)
            # Si cat_int > 2 y clas_int <= 2, vinieron invertidos (prenda primero, género después)
            if cat_int > 2 and clas_int <= 2:
                p_cat, p_clas = clas_int, cat_int
            else:
                p_cat, p_clas = cat_int, clas_int

            rows = db.execute(
                text("SELECT * FROM sp_get_items_by_category(:category, :clasification)"),
                {"category": p_cat, "clasification": p_clas}
            ).fetchall()

            # Si no devolvió nada y los parámetros son distintos, intentar en orden alterno
            if not rows and p_cat != p_clas:
                alt_rows = db.execute(
                    text("SELECT * FROM sp_get_items_by_category(:category, :clasification)"),
                    {"category": p_clas, "clasification": p_cat}
                ).fetchall()
                if alt_rows:
                    rows = alt_rows

            return cls._build_items_response(rows)
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_items_by_category_only(cls, category):
        try:
            rows = db.execute(
                text("SELECT id_item, name, description, image, price, clasification, category, status_item FROM items WHERE category = :category ORDER BY id_item DESC"),
                {"category": int(category)}
            ).fetchall()
            return cls._build_items_response(rows)
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_items_by_clasification_only(cls, clasification):
        try:
            rows = db.execute(
                text("SELECT id_item, name, description, image, price, clasification, category, status_item FROM items WHERE clasification = :clasification ORDER BY id_item DESC"),
                {"clasification": int(clasification)}
            ).fetchall()
            return cls._build_items_response(rows)
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_item(cls, item, images=None):
        try:
            clean_images = []
            if images and isinstance(images, list):
                clean_images = [img.strip() for img in images if isinstance(img, str) and img.strip()][:5]

            # La primera imagen es la imagen principal
            primary_image = clean_images[0] if clean_images else item.image

            db.execute(
                text("CALL sp_add_item(:name, :description, :image, :price, :clasification, :category)"),
                {
                    "name":          item.name,
                    "description":   item.description,
                    "image":         primary_image,
                    "price":         item.price,
                    "clasification": item.clasification,
                    "category":      item.category,
                }
            )

            # Obtener el id_item recién insertado
            new_id = db.execute(text("SELECT max(id_item) FROM items")).scalar()

            # Insertar en item_images (máximo 5)
            if new_id:
                if not clean_images and primary_image:
                    clean_images = [primary_image]

                for idx, img_url in enumerate(clean_images[:5]):
                    db.execute(
                        text("""
                            INSERT INTO item_images (id_item, image_url, position, is_primary)
                            VALUES (:id_item, :image_url, :pos, :is_prim)
                        """),
                        {
                            "id_item": new_id,
                            "image_url": img_url,
                            "pos": idx + 1,
                            "is_prim": (idx == 0)
                        }
                    )

            db.commit()
            return 1
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def update_item(cls, item, images=None):
        try:
            clean_images = []
            if images and isinstance(images, list):
                clean_images = [img.strip() for img in images if isinstance(img, str) and img.strip()][:5]

            # La primera imagen es la imagen principal
            primary_image = clean_images[0] if clean_images else item.image

            db.execute(
                text("CALL sp_update_item(:id_item, :name, :description, :image, :price, :clasification, :category)"),
                {
                    "id_item":       item.id_item,
                    "name":          item.name,
                    "description":   item.description,
                    "image":         primary_image,
                    "price":         item.price,
                    "clasification": item.clasification,
                    "category":      item.category,
                }
            )

            # Actualizar tabla item_images si se enviaron imágenes
            if clean_images or images is not None:
                db.execute(text("DELETE FROM item_images WHERE id_item = :id"), {"id": item.id_item})
                if not clean_images and primary_image:
                    clean_images = [primary_image]

                for idx, img_url in enumerate(clean_images[:5]):
                    db.execute(
                        text("""
                            INSERT INTO item_images (id_item, image_url, position, is_primary)
                            VALUES (:id_item, :image_url, :pos, :is_prim)
                        """),
                        {
                            "id_item": item.id_item,
                            "image_url": img_url,
                            "pos": idx + 1,
                            "is_prim": (idx == 0)
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

    @classmethod
    def get_categories(cls):
        try:
            rows = db.execute(text("""
                SELECT 
                    c.id_clasification,
                    c.name,
                    COUNT(i.id_item) AS items_count
                FROM clasification c
                LEFT JOIN items i ON i.clasification = c.id_clasification
                GROUP BY c.id_clasification, c.name
                ORDER BY c.id_clasification ASC
            """)).fetchall()

            categories_list = []
            for row in rows:
                categories_list.append({
                    "id_clasification": row[0],
                    "name": row[1],
                    "items_count": int(row[2])
                })

            return categories_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_category(cls, name):
        try:
            clean_name = str(name).strip()
            if not clean_name:
                raise ValueError("El nombre de la categoría es requerido.")

            row = db.execute(
                text("INSERT INTO clasification (name) VALUES (:name) RETURNING id_clasification, name"),
                {"name": clean_name}
            ).fetchone()
            db.commit()

            return {
                "id_clasification": row[0],
                "name": row[1],
                "items_count": 0
            }
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def update_category(cls, id_clasification, name):
        try:
            clean_name = str(name).strip()
            if not clean_name:
                raise ValueError("El nombre de la categoría es requerido.")

            row = db.execute(
                text("UPDATE clasification SET name = :name WHERE id_clasification = :id RETURNING id_clasification, name"),
                {"name": clean_name, "id": int(id_clasification)}
            ).fetchone()
            db.commit()

            if row:
                count = db.execute(
                    text("SELECT COUNT(*) FROM items WHERE clasification = :id"),
                    {"id": int(id_clasification)}
                ).scalar() or 0
                return {
                    "id_clasification": row[0],
                    "name": row[1],
                    "items_count": int(count)
                }
            return None
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def delete_category(cls, id_clasification):
        try:
            # Validar si tiene artículos asociados para no romper integridad referencial
            count = db.execute(
                text("SELECT COUNT(*) FROM items WHERE clasification = :id"),
                {"id": int(id_clasification)}
            ).scalar() or 0

            if count > 0:
                raise ValueError(f"No se puede eliminar la categoría porque tiene {count} artículo(s) asociado(s). Reasigna o elimina los artículos antes de borrarla.")

            row = db.execute(
                text("DELETE FROM clasification WHERE id_clasification = :id RETURNING id_clasification"),
                {"id": int(id_clasification)}
            ).fetchone()
            db.commit()

            return 1 if row else 0
        except Exception as ex:
            db.rollback()
            raise Exception(ex)