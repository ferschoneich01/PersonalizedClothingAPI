from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from funciones import *
from sqlalchemy.sql import text
#objeto
from .entities.users import users

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class usersModel():

    @classmethod
    def get_users(self):
        try:
            usersList=[]
            usersDBList = db.execute(
                text("SELECT * FROM users")).fetchall()

            for i in range(len(usersDBList)):
                user = users(id_user=usersDBList[i][0],username=usersDBList[i][1],
                            password=usersDBList[i][2],email=usersDBList[i][3],
                            person=usersDBList[i][4],role=usersDBList[i][5],status_user=usersDBList[i][6])
                
                usersList.append(user.to_json())
                i+=1

            return usersList
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def get_userbyId(self, username):
        try:
            usersList=[]
            usersDBList = db.execute(
                text("SELECT * FROM users where username = '"+str(username)+"'")).fetchall()
            
            for i in range(len(usersDBList)):
                user = users(id_user=usersDBList[i][0],username=usersDBList[i][1],
                            password=usersDBList[i][2],email=usersDBList[i][3],
                            person=usersDBList[i][4],role=usersDBList[i][5],status_user=usersDBList[i][6])
                
                usersList.append(user.to_json())
                i+=1

            return usersList
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_user(self, user, person):
        try:
            # Query database for person
            db.execute(text("INSERT INTO person (cedula,name,lastname,birthday,phone,country,city,sex) VALUES ('"+str(person.cedula)+"','"+str(person.name)+
                       "','"+str(person.lastname)+"','"+str(person.birthday)+"','"+str(person.phone)+"','Nicaragua','"+str(person.city)+"','"+str(person.sex)+"')"))
            db.commit()
            # Query selection id person
            id_person = db.execute(text(
                "SELECT * FROM person WHERE cedula = '"+person.cedula+"'")).fetchall()
            
            db.execute(text("INSERT INTO users (username,password,email,person,role,status_user) VALUES ('" +
                       str(user.username)+"','"+str(user.password)+"','"+str(user.email)+"',"+str(id_person[0][0])+",2,1)"))
            db.commit()

            db.close()

            return 1
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_user(self, user):
        try:
            db.execute(text("UPDATE users set password = '"+str(user.password)+"', role = '"+str(user.role)+"', email = '"+str(user.email)+"', status_user = '"+str(user.status_user)+"'"
                            +"WHERE id_user = '"+str(user.id_user)+"'"))
            
            db.commit()
            db.close()
            return 1
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_user(self, user):
        try:
            db.execute(text("UPDATE users set status_user = 2 WHERE id_user = '"+str(user.id_user)+"'"))
            db.commit()
            return 1
        except Exception as ex:
            raise Exception(ex)