from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from funciones import *
from sqlalchemy.sql import text
#objeto
from .entities.items import items

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class itemsModel():

    @classmethod
    def get_items(self):
        try:
            itemsList=[]
            itemsDBList = db.execute(
                text("SELECT * FROM items")).fetchall()

            for i in range(len(itemsDBList)):
                item = items(id_item=itemsDBList[i][0],name=itemsDBList[i][1],
                            description=itemsDBList[i][2],image=itemsDBList[i][3],
                            price=itemsDBList[i][4],clasification=itemsDBList[i][5],category=itemsDBList[i][6], status_item=itemsDBList[i][7])
                
                itemsList.append(item.to_json())
                i+=1

            return itemsList
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def get_itembyId(self, id_item):
        try:
            itemsList=[]
            itemsDBList = db.execute(
                text("SELECT * FROM items where id_item = "+str(id_item))).fetchall()
            
            for i in range(len(itemsDBList)):
                item = items(id_item=itemsDBList[i][0],name=itemsDBList[i][1],
                            description=itemsDBList[i][2],image=itemsDBList[i][3],
                            price=itemsDBList[i][4],clasification=itemsDBList[i][5],category=itemsDBList[i][6],status_item=itemsDBList[i][7])
                
                itemsList.append(item.to_json())
                i+=1

            return itemsList
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_itemsByCategory(self, category, clasification):
        try:
            itemsList=[]
            itemsDBList = db.execute(
                text("SELECT * FROM items where id_category="+str(category)+" and id_clasification="+str(clasification))).fetchall()

            for i in range(len(itemsDBList)):
                item = items(id_item=itemsDBList[i][0],name=itemsDBList[i][1],
                            description=itemsDBList[i][2],image=itemsDBList[i][3],
                            price=itemsDBList[i][4],classification=itemsDBList[i][5],category=itemsDBList[i][6])
                
                itemsList.append(item.to_json())
                i+=1

            return itemsList
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def add_item(self, item):
        try:
            # Query database for person
            db.execute(text("INSERT INTO items (name,description,image,price,clasification,category,status_item) VALUES ('"+str(item.name)+"','"+str(item.description)+
                       "','"+str(item.image)+"',"+str(item.price)+","+str(item.clasification)+","+str(item.category)+","+str(item.status_item)+")"))
            db.commit()
            
            db.close()

            return 1
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_item(self, item):
        try:
            db.execute(text("UPDATE items set name = '"+str(item.name)+"', description = '"+str(item.description)+"', image = '"+str(item.image)+"', price = "+str(item.price)+"," +
                            + "clasification = "+str(item.clasification)+","+ "category = "+str(item.category)+""
                            +"WHERE id_item = "+str(item.id_item)))
            
            db.commit()
            db.close()
            return 1
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_item(self, item):
        try:
            db.execute(text("UPDATE items set status_item = 2 WHERE id_item = '"+str(item.id_item)+"'"))
            db.commit()
            return 1
        except Exception as ex:
            raise Exception(ex)