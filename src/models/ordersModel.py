from sqlalchemy.sql import text
from database import db
from .entities.orders import orders


class ordersModel():

    @classmethod
    def get_orders(cls):
        try:
            orders_list = []
            rows = db.execute(text("SELECT * FROM sp_get_orders()")).fetchall()

            # Fetch additional order details from orders table
            additional_rows = db.execute(text("SELECT id_order, id_canal_de_ventas, pedidoNombre, cedula, pedidoTelefono, orderdate FROM orders")).fetchall()
            order_extra = {
                row[0]: {
                    "id_canal_de_ventas": row[1],
                    "pedidoNombre": row[2],
                    "cedula": row[3],
                    "pedidoTelefono": row[4],
                    "orderdate": str(row[5]) if row[5] else None
                }
                for row in additional_rows
            }

            for i, row in enumerate(rows):
                id_order = row[10]
                extra = order_extra.get(id_order, {})
                ped_nombre = extra.get("pedidoNombre")
                cedula = extra.get("cedula")
                id_canal = extra.get("id_canal_de_ventas", 1)

                name = ped_nombre if ped_nombre else row[0]
                lastname = "" if ped_nombre else row[1]

                orders_list.append({
                    "name":         name,
                    "lastname":     lastname,
                    "address":      row[2],
                    "city":         row[3],
                    "paymethod":    row[4],
                    "subtotal":     row[5],
                    "shippingcost": row[6],
                    "totalAmount":  row[7],
                    "status":       row[8],
                    "id_status":    row[9],
                    "id_order":     id_order,
                    "quantityOrders": i + 1,
                    "id_canal_de_ventas": id_canal,
                    "pedidoNombre": ped_nombre,
                    "cedula":       cedula if cedula else "",
                    "pedidoTelefono": extra.get("pedidoTelefono") if extra.get("pedidoTelefono") else "",
                    "orderdate":    extra.get("orderdate"),
                })

            return orders_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_orderDetails(cls):
        try:
            orders_list = []
            rows = db.execute(text("SELECT * FROM sp_get_order_details()")).fetchall()

            # Fetch additional order details from orders table
            additional_rows = db.execute(text("SELECT id_order, id_canal_de_ventas, pedidoNombre, cedula, pedidoTelefono, orderdate FROM orders")).fetchall()
            order_extra = {
                row[0]: {
                    "id_canal_de_ventas": row[1],
                    "pedidoNombre": row[2],
                    "cedula": row[3],
                    "pedidoTelefono": row[4],
                    "orderdate": str(row[5]) if row[5] else None
                }
                for row in additional_rows
            }

            items_cats = db.execute(text("SELECT i.id_item, c.name FROM items i LEFT JOIN clasification c ON c.id_clasification = i.clasification")).fetchall()
            cats_map = {r[0]: (r[1].capitalize() if r[1] else "General") for r in items_cats}

            for i, row in enumerate(rows):
                id_order = row[12]
                extra = order_extra.get(id_order, {})
                ped_nombre = extra.get("pedidoNombre")
                cedula = extra.get("cedula")
                id_canal = extra.get("id_canal_de_ventas", 1)

                orders_list.append({
                    "id_item":        row[0],
                    "username":       row[1],
                    "name":           row[2],
                    "color":          row[3],
                    "size":           row[4],
                    "paymethod":      row[5],
                    "price":          row[6],
                    "cost":           row[7],
                    "totalAmount":    row[8],
                    "status":         row[9],
                    "image":          row[10],
                    "id_status":      row[11],
                    "id_order":       id_order,
                    "quantityOrders": row[13],
                    "custom_image":   row[14],
                    "paymethod":      row[15] if len(row) > 15 else "Efectivo",
                    "voucher_url":    row[16] if len(row) > 16 else None,
                    "id_canal_de_ventas": id_canal,
                    "pedidoNombre":    ped_nombre,
                    "cedula":          cedula if cedula else "",
                    "pedidoTelefono":  extra.get("pedidoTelefono") if extra.get("pedidoTelefono") else "",
                    "orderdate":       extra.get("orderdate"),
                    "category_name":   cats_map.get(row[0], "General"),
                })

            return orders_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_shipping(cls):
        try:
            orders_list = []
            rows = db.execute(text("SELECT * FROM sp_get_shipping()")).fetchall()

            # Fetch additional order details from orders table
            additional_rows = db.execute(text("SELECT id_order, id_canal_de_ventas, pedidoNombre, cedula, pedidoTelefono FROM orders")).fetchall()
            order_extra = {row[0]: {"id_canal_de_ventas": row[1], "pedidoNombre": row[2], "cedula": row[3], "pedidoTelefono": row[4]} for row in additional_rows}

            for i, row in enumerate(rows):
                id_order = row[12]
                extra = order_extra.get(id_order, {})
                ped_nombre = extra.get("pedidoNombre")
                cedula = extra.get("cedula")
                id_canal = extra.get("id_canal_de_ventas", 1)

                client_name = ped_nombre if ped_nombre else row[15]
                client_lastname = "" if ped_nombre else row[16]
                client_cedula = cedula if cedula else row[17]

                orders_list.append({
                    "address":         row[0],
                    "username":        row[1],
                    "name":            row[2],
                    "color":           row[3],
                    "size":            row[4],
                    "paymethod":       row[5],
                    "price":           row[6],
                    "cost":            row[7],
                    "totalAmount":     row[8],
                    "status":          row[9],
                    "image":           row[10],
                    "id_status":       row[11],
                    "id_order":        id_order,
                    "quantityOrders":  row[13],
                    "custom_image":    row[14],
                    "client_name":     client_name,
                    "client_lastname": client_lastname,
                    "cedula":          client_cedula if client_cedula else "",
                    "city":            row[18],
                    "id_canal_de_ventas": id_canal,
                    "pedidoNombre":    ped_nombre,
                    "pedidoTelefono":  extra.get("pedidoTelefono") if extra.get("pedidoTelefono") else "",
                })

            return orders_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_userbyUsername(cls, username):
        try:
            buys_list = []
            rows = db.execute(
                text("SELECT * FROM sp_get_orders_by_username(:username)"),
                {"username": username}
            ).fetchall()

            # Fetch additional order details from orders table
            additional_rows = db.execute(text("SELECT id_order, id_canal_de_ventas, pedidoNombre, cedula, pedidoTelefono FROM orders")).fetchall()
            order_extra = {row[0]: {"id_canal_de_ventas": row[1], "pedidoNombre": row[2], "cedula": row[3], "pedidoTelefono": row[4]} for row in additional_rows}

            for i, row in enumerate(rows):
                id_order = row[13]
                extra = order_extra.get(id_order, {})
                ped_nombre = extra.get("pedidoNombre")
                cedula = extra.get("cedula")
                id_canal = extra.get("id_canal_de_ventas", 1)

                buys_list.append({
                    "id_item":        row[0],
                    "username":       row[1],
                    "name":           row[2],
                    "color":          row[3],
                    "size":           row[4],
                    "paymethod":      row[5],
                    "price":          row[6],
                    "cost":           row[7],
                    "totalAmount":    row[8],
                    "status":         row[9],
                    "image":          row[10],
                    "address":        row[11],
                    "orderdate":      str(row[12]),
                    "id_order":       id_order,
                    "quantityOrders": row[14],
                    "custom_image":   row[15],
                    "order_paymethod": row[16] if len(row) > 16 else "Efectivo",
                    "voucher_url":     row[17] if len(row) > 17 else None,
                    "id_canal_de_ventas": id_canal,
                    "pedidoNombre":    ped_nombre,
                    "cedula":          cedula if cedula else "",
                    "pedidoTelefono":  extra.get("pedidoTelefono") if extra.get("pedidoTelefono") else "",
                })

            return buys_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_sales_reports_data(cls):
        try:
            # 1. Obtener detalles de pedidos (con fechas, items y categorías mapeadas)
            details = cls.get_orderDetails()

            # 2. Resumen por categoría de producto
            cat_query = text("""
                SELECT COALESCE(c.name, 'General') as category,
                       COUNT(od.id_orderdetail) as items_count,
                       COALESCE(SUM(od.quantity), 0) as total_qty,
                       COALESCE(SUM(i.price * od.quantity), 0) as total_sales
                FROM orderdetails od
                JOIN items i ON i.id_item = od.item
                LEFT JOIN clasification c ON c.id_clasification = i.clasification
                GROUP BY c.name
                ORDER BY total_sales DESC
            """)
            cat_rows = db.execute(cat_query).fetchall()
            categories_summary = [
                {
                    "category": r[0].capitalize() if r[0] else "General",
                    "items_count": int(r[1]),
                    "total_qty": int(r[2]),
                    "total_sales": float(r[3])
                }
                for r in cat_rows
            ]

            # 3. Resumen por canal de ventas
            chan_query = text("""
                SELECT COALESCE(cv.id_canal_de_ventas, 1) as id_canal,
                       COALESCE(cv.nombre, 'Web') as channel_name,
                       COUNT(DISTINCT o.id_order) as orders_count,
                       COALESCE(SUM(od.quantity), 0) as items_count,
                       COALESCE(SUM(i.price * od.quantity), 0) as total_sales
                FROM orders o
                LEFT JOIN canal_de_ventas cv ON cv.id_canal_de_ventas = o.id_canal_de_ventas
                JOIN orderdetails od ON od.id_order = o.id_order
                JOIN items i ON i.id_item = od.item
                GROUP BY cv.id_canal_de_ventas, cv.nombre
                ORDER BY total_sales DESC
            """)
            chan_rows = db.execute(chan_query).fetchall()
            channels_summary = [
                {
                    "id_canal": int(r[0]),
                    "channel_name": r[1],
                    "orders_count": int(r[2]),
                    "items_count": int(r[3]),
                    "total_sales": float(r[4])
                }
                for r in chan_rows
            ]

            # 4. Resumen por estado de pedidos
            status_query = text("""
                SELECT s.status, o.id_status,
                       COUNT(DISTINCT o.id_order) as orders_count,
                       COALESCE(SUM(od.quantity), 0) as items_count,
                       COALESCE(SUM(i.price * od.quantity), 0) as total_sales
                FROM orders o
                JOIN status s ON s.id_status = o.id_status
                JOIN orderdetails od ON od.id_order = o.id_order
                JOIN items i ON i.id_item = od.item
                GROUP BY s.status, o.id_status
                ORDER BY orders_count DESC
            """)
            status_rows = db.execute(status_query).fetchall()
            status_summary = [
                {
                    "status": r[0],
                    "id_status": int(r[1]),
                    "orders_count": int(r[2]),
                    "items_count": int(r[3]),
                    "total_sales": float(r[4])
                }
                for r in status_rows
            ]

            # 5. Top 10 productos más vendidos
            top_query = text("""
                SELECT i.id_item, i.name, i.image, COALESCE(c.name, 'General') as category,
                       COALESCE(SUM(od.quantity), 0) as total_qty,
                       COALESCE(SUM(i.price * od.quantity), 0) as total_sales
                FROM orderdetails od
                JOIN items i ON i.id_item = od.item
                LEFT JOIN clasification c ON c.id_clasification = i.clasification
                GROUP BY i.id_item, i.name, i.image, c.name
                ORDER BY total_qty DESC
                LIMIT 10
            """)
            top_rows = db.execute(top_query).fetchall()
            top_products = [
                {
                    "id_item": int(r[0]),
                    "name": r[1],
                    "image": r[2],
                    "category": r[3].capitalize() if r[3] else "General",
                    "total_qty": int(r[4]),
                    "total_sales": float(r[5])
                }
                for r in top_rows
            ]

            # 6. Historial de ventas mensual
            month_query = text("""
                SELECT TO_CHAR(o.orderdate, 'YYYY-MM') as month,
                       COUNT(DISTINCT o.id_order) as orders_count,
                       COALESCE(SUM(od.quantity), 0) as items_count,
                       COALESCE(SUM(i.price * od.quantity), 0) as total_sales
                FROM orders o
                JOIN orderdetails od ON od.id_order = o.id_order
                JOIN items i ON i.id_item = od.item
                WHERE o.orderdate IS NOT NULL
                GROUP BY TO_CHAR(o.orderdate, 'YYYY-MM')
                ORDER BY month ASC
            """)
            month_rows = db.execute(month_query).fetchall()
            monthly_sales = [
                {
                    "month": r[0],
                    "orders_count": int(r[1]),
                    "items_count": int(r[2]),
                    "total_sales": float(r[3])
                }
                for r in month_rows
            ]

            return {
                "details": details,
                "categories_summary": categories_summary,
                "channels_summary": channels_summary,
                "status_summary": status_summary,
                "top_products": top_products,
                "monthly_sales": monthly_sales
            }
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_order(cls, address, username, carListItems, paymethod='Efectivo', id_canal_de_ventas=1, pedidoNombre=None, cedula=None, pedidoTelefono=None):
        try:
            result = db.execute(
                text("SELECT * FROM sp_create_order(:username, :address, :paymethod)"),
                {"username": username, "address": address, "paymethod": paymethod}
            ).fetchone()
            
            id_order = result[0]

            # Update new order fields before committing details
            db.execute(
                text("UPDATE orders SET id_canal_de_ventas = :id_canal_de_ventas, pedidoNombre = :pedidoNombre, cedula = :cedula, pedidoTelefono = :pedidoTelefono WHERE id_order = :id_order"),
                {
                    "id_canal_de_ventas": id_canal_de_ventas,
                    "pedidoNombre": pedidoNombre,
                    "cedula": cedula,
                    "pedidoTelefono": pedidoTelefono,
                    "id_order": id_order
                }
            )

            for item in carListItems:
                # item frontend sends: [name, price, quantity, size, color, image, cartId, id_item]
                quantity = int(item[2])
                size = str(item[3])
                color = str(item[4])
                custom_image = str(item[5])
                id_item = int(item[7])
                
                db.execute(
                    text("CALL sp_add_order_detail(:id_order, :color, :size, :id_item, :quantity, :custom_image)"),
                    {
                        "id_order": id_order,
                        "color": color,
                        "size": size,
                        "id_item": id_item,
                        "quantity": quantity,
                        "custom_image": custom_image
                    }
                )
                db.commit()
            return id_order
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def changeStatus(cls, id_order, status):
        try:
            db.execute(
                text("CALL sp_change_order_status(:id_order, :status)"),
                {"id_order": int(id_order), "status": str(status)}
            )
            db.commit()
            return 1
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def upload_voucher(cls, id_order, voucher_url):
        try:
            db.execute(
                text("CALL sp_upload_voucher(:id_order, :voucher_url)"),
                {"id_order": int(id_order), "voucher_url": str(voucher_url)}
            )
            db.commit()
            return 1
        except Exception as ex:
            db.rollback()
            raise Exception(ex)
