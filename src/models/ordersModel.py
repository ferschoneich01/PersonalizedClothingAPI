from sqlalchemy.sql import text
from database import db
from .entities.orders import orders


class ordersModel():

    @classmethod
    def get_orders(cls):
        try:
            orders_list = []
            rows = db.execute(text("SELECT * FROM sp_get_orders()")).fetchall()

            for i, row in enumerate(rows):
                orders_list.append({
                    "name":         row[0],
                    "lastname":     row[1],
                    "address":      row[2],
                    "city":         row[3],
                    "paymethod":    row[4],
                    "subtotal":     row[5],
                    "shippingcost": row[6],
                    "totalAmount":  row[7],
                    "status":       row[8],
                    "id_status":    row[9],
                    "id_order":     row[10],
                    "quantityOrders": i + 1,
                })

            return orders_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_orderDetails(cls):
        try:
            orders_list = []
            rows = db.execute(text("SELECT * FROM sp_get_order_details()")).fetchall()

            for i, row in enumerate(rows):
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
                    "id_order":       row[12],
                    "quantityOrders": row[13],
                    "custom_image":   row[14],
                    "paymethod":      row[15] if len(row) > 15 else "Efectivo",
                    "voucher_url":    row[16] if len(row) > 16 else None,
                })

            return orders_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_shipping(cls):
        try:
            orders_list = []
            rows = db.execute(text("SELECT * FROM sp_get_shipping()")).fetchall()

            for i, row in enumerate(rows):
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
                    "id_order":        row[12],
                    "quantityOrders":  row[13],
                    "custom_image":    row[14],
                    "client_name":     row[15],
                    "client_lastname": row[16],
                    "cedula":          row[17],
                    "city":            row[18]
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

            for i, row in enumerate(rows):
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
                    "id_order":       row[13],
                    "quantityOrders": row[14],
                    "custom_image":   row[15],
                    "order_paymethod": row[16] if len(row) > 16 else "Efectivo",
                    "voucher_url":     row[17] if len(row) > 17 else None,
                })

            return buys_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_order(cls, address, username, carListItems, paymethod='Efectivo'):
        try:
            result = db.execute(
                text("SELECT * FROM sp_create_order(:username, :address, :paymethod)"),
                {"username": username, "address": address, "paymethod": paymethod}
            ).fetchone()
            
            id_order = result[0]

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