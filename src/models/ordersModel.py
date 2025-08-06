from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from funciones import *
from sqlalchemy.sql import text
#objeto
from .entities.orders import orders

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class ordersModel():

    @classmethod
    def get_orders(self):
        try:
            ordersList = []
            ordersDBList = db.execute(text(
                "Select p.name,p.lastname,ap.address,ap.city,pm.method,sum(i.price),sum(sh.cost),sum(i.price+sh.cost),s.status,s.id_status,o.id_order "+
                +"FROM items i INNER JOIN orderdetails od ON od.item = i.id_item INNER JOIN orders o ON o.id_order = od.id_order INNER JOIN status s on "+
                +"s.id_status = o.id_status INNER JOIN users u on u.id_user = o.id_user INNER JOIN shipping sh on sh.id_order = o.id_order INNER JOIN "+
                +"addres_persons ap on ap.id_address_person = sh.address INNER JOIN paymentmethohds pm on  pm.id_paymentmethod = o.paymentmethod INNER JOIN"+
                +" person p on p.id_person = u.person WHERE s.status = 'En proceso' GROUP BY o.id_order,i.name,pm.method,s.status,s.id_status,p.name,p.lastname,ap.address,ap.city")).fetchall()

            i = 0
            for i in range(len(ordersDBList)):
                order = {
                    "name":ordersDBList[i][0],
                    "lastname":ordersDBList[i][1],
                    "address":ordersDBList[i][2], 
                    "city":ordersDBList[i][3], 
                    "paymethod":ordersDBList[i][4],
                    "subtotal":ordersDBList[i][5], 
                    "shippingcost":ordersDBList[i][6], 
                    "totalAmount":ordersDBList[i][7],
                    "totalAmount":ordersDBList[i][8], 
                    "status":ordersDBList[i][9],
                    "quantityOrders":(i+1),
                    "id_status":ordersDBList[i][10],
                    "id_order":ordersDBList[i][11]
                    }
                
                ordersList.append(order)
                i+=1
            return ordersList
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_orderDetails(self):
        try:
            ordersList = []
            ordersDBList = db.execute(text(
                "Select i.id_item,u.username,i.name,od.color,od.size,p.method,i.price,sh.cost,(i.price+sh.cost),s.status,i.image,s.id_status,o.id_order FROM items i INNER JOIN orderdetails od ON od.item = i.id_item INNER JOIN orders o ON o.id_order = od.id_order INNER JOIN status s on s.id_status = o.id_status INNER JOIN users u on u.id_user = o.id_user INNER JOIN shipping sh on sh.id_order = o.id_order INNER JOIN addres_persons ap on ap.id_address_person = sh.address INNER JOIN paymentmethohds p on  p.id_paymentmethod = o.paymentmethod WHERE s.status = 'En proceso'")).fetchall()

            i = 0
            for i in range(len(ordersDBList)):
                order = {
                    "id_item":ordersDBList[i][0],
                    "username":ordersDBList[i][1],
                    "name":ordersDBList[i][2], 
                    "color":ordersDBList[i][3], 
                    "size":ordersDBList[i][4],
                    "paymethod":ordersDBList[i][5], 
                    "price":ordersDBList[i][6], 
                    "cost":ordersDBList[i][7],
                    "totalAmount":ordersDBList[i][8], 
                    "status":ordersDBList[i][9], 
                    "image":ordersDBList[i][10], 
                    "quantityOrders":(i+1),
                    "id_status":ordersDBList[i][11],
                    "id_order":ordersDBList[i][12]
                    }
                
                ordersList.append(order)
                i+=1
            return ordersList
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_shipping(self):
        try:
            ordersList = []
            ordersDBList = db.execute(text(
                "Select ap.address,u.username,i.name,od.color,od.size,p.method,i.price,sh.cost,(i.price+sh.cost),s.status,i.image,s.id_status,o.id_order FROM items i INNER JOIN orderdetails od ON od.item = i.id_item INNER JOIN orders o ON o.id_order = od.id_order INNER JOIN status s on s.id_status = o.id_status INNER JOIN users u on u.id_user = o.id_user INNER JOIN shipping sh on sh.id_order = o.id_order INNER JOIN addres_persons ap on ap.id_address_person = sh.address INNER JOIN paymentmethohds p on  p.id_paymentmethod = o.paymentmethod WHERE s.status = 'Terminado' or s.status = 'Enviado'")).fetchall()

            i = 0
            for i in range(len(ordersDBList)):
                order = {
                    "address":ordersDBList[i][0],
                    "username":ordersDBList[i][1],
                    "name":ordersDBList[i][2], 
                    "color":ordersDBList[i][3], 
                    "size":ordersDBList[i][4],
                    "paymethod":ordersDBList[i][5], 
                    "price":ordersDBList[i][6], 
                    "cost":ordersDBList[i][7],
                    "totalAmount":ordersDBList[i][8], 
                    "status":ordersDBList[i][9], 
                    "image":ordersDBList[i][10], 
                    "quantityOrders":(i+1),
                    "id_status":ordersDBList[i][11],
                    "id_order":ordersDBList[i][12]
                    }
                
                ordersList.append(order)
                i+=1
            return ordersList
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def get_userbyUsername(self, username):
        try:
            buysList = []
            ordersDBList = db.execute(text(
                "Select i.id_item,u.username,i.name,od.color,od.size,p.method,i.price,sh.cost,(i.price+sh.cost),s.status,i.image,ap.address,o.orderdate FROM items i INNER JOIN orderdetails od ON od.item = i.id_item INNER JOIN orders o ON o.id_order = od.id_order INNER JOIN status s on s.id_status = o.id_status INNER JOIN users u on u.id_user = o.id_user INNER JOIN shipping sh on sh.id_order = o.id_order INNER JOIN addres_persons ap on ap.id_address_person = sh.address INNER JOIN paymentmethohds p on  p.id_paymentmethod = o.paymentmethod WHERE u.username = '"+str(username)+"'")).fetchall()

            i = 0
            for o in ordersDBList:
                order = {
                    "id_item":ordersDBList[i][0],
                    "username":ordersDBList[i][1],
                    "name":ordersDBList[i][2], 
                    "color":ordersDBList[i][3], 
                    "size":ordersDBList[i][4],
                    "paymethod":ordersDBList[i][5], 
                    "price":ordersDBList[i][6], 
                    "cost":ordersDBList[i][7],
                    "totalAmount":ordersDBList[i][8], 
                    "status":ordersDBList[i][9], 
                    "image":ordersDBList[i][10], 
                    "addres":ordersDBList[i][11],
                    "orderdate":ordersDBList[i][12],
                    "quantityOrders":(i+1)
                    }
                
                buysList.append(order)
                i += 1

            return buysList
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_order(self, address, username, carListItems):
        try:
            id_user = db.execute(text(
                "SELECT * FROM users WHERE username = '"+username+"'")).fetchall()
            # crear una nueva orden
            db.execute("INSERT INTO orders(orderdate,paymentmethod,id_user,id_status) VALUES (current_timestamp,1," +
                       str(id_user[0][0])+",1)")
            db.commit()

            # obtener el id de la orden que acabamos de insertar
            id_order = db.execute(
                "select id_order from orders o where id_user = "+str(id_user[0][0])+" order by orderdate desc limit 1 ").fetchall()

            # insertar cada uno de los items comprados
            for i in carListItems:
                db.execute("INSERT INTO orderdetails(color,size,item,quantity,id_order) VALUES ('" +
                           str(i[4])+"','"+str(i[3])+"',"+str(i[7])+","+str(int(i[2]))+","+str(int(id_order[0][0]))+")")
                db.commit()
            # obtener el id de la dirección a enviar el producto
            id_address = db.execute(
                "select id_address_person from addres_persons where address = '"+str(address)+"'limit 1").fetchall()

            # insertamos un nuevo registro de envio
            db.execute("INSERT INTO shipping(shipdate,cost,id_order,address) VALUES (current_date,70.00," +
                       str(id_order[0][0])+","+str(id_address[0][0])+")")
            db.commit()

            db.close()
            return 1
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_user(self, user):
        try:
            db.execute(text("UPDATE users set password = '"+str(user.password)+"', role = '"+str(user.role)+"', email = '"+str(user.email)+"', status_user = '"+str(user.status_user)+"'"
                            +"WHERE id_(user = '"+str(user.id_user)+"'"))
            
            db.commit()
            db.close()
            return 1
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def changeStatus(self, id_order,status):
        try:
            id_status = db.execute(text(
                "select id_status from status where status = '"+str(status)+"'")).fetchall()
            
            db.execute(text("UPDATE orders set id_status = "+str(id_status[0][0])+" WHERE id_order = '"+str(id_order)+"'"))
            db.commit()
            return 1
        except Exception as ex:
            raise Exception(ex)