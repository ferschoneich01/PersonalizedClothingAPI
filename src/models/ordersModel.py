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
            additional_rows = db.execute(text("SELECT id_order, id_canal_de_ventas, pedidoNombre, cedula, pedidoTelefono FROM orders")).fetchall()
            order_extra = {row[0]: {"id_canal_de_ventas": row[1], "pedidoNombre": row[2], "cedula": row[3], "pedidoTelefono": row[4]} for row in additional_rows}

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
            additional_rows = db.execute(text("SELECT id_order, id_canal_de_ventas, pedidoNombre, cedula, pedidoTelefono FROM orders")).fetchall()
            order_extra = {row[0]: {"id_canal_de_ventas": row[1], "pedidoNombre": row[2], "cedula": row[3], "pedidoTelefono": row[4]} for row in additional_rows}

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