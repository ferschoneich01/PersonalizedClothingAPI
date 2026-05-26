from sqlalchemy.sql import text
from database import db
from .entities.users import users


class usersModel():

    @classmethod
    def get_users(cls):
        try:
            users_list = []
            rows = db.execute(text("SELECT * FROM sp_get_users()")).fetchall()

            for row in rows:
                user = users(
                    id_user=row[0], username=row[1], password=row[2],
                    email=row[3], person=row[4], role=row[5], status_user=row[6]
                )
                users_list.append(user.to_json())

            return users_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_userbyId(cls, username):
        try:
            users_list = []
            rows = db.execute(
                text("SELECT * FROM sp_get_user_by_username(:username)"),
                {"username": username}
            ).fetchall()

            for row in rows:
                user = users(
                    id_user=row[0], username=row[1], password=row[2],
                    email=row[3], person=row[4], role=row[5], status_user=row[6]
                )
                users_list.append(user.to_json())

            return users_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_user(cls, user, person):
        try:
            db.execute(
                text("CALL sp_add_user(:username, :password, :email, :cedula, :name, :lastname, :birthday, :phone, :city, :sex)"),
                {
                    "username":  user.username,
                    "password":  user.password,
                    "email":     user.email,
                    "cedula":    person.cedula,
                    "name":      person.name,
                    "lastname":  person.lastname,
                    "birthday":  person.birthday,
                    "phone":     person.phone,
                    "city":      person.city,
                    "sex":       person.sex,
                }
            )
            db.commit()
            return 1
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def update_user(cls, user):
        try:
            db.execute(
                text("CALL sp_update_user(:id_user, :password, :role, :email, :status_user)"),
                {
                    "id_user":     user.id_user,
                    "password":    user.password,
                    "role":        user.role,
                    "email":       user.email,
                    "status_user": user.status_user,
                }
            )
            db.commit()
            return 1
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def delete_user(cls, user):
        try:
            db.execute(
                text("CALL sp_delete_user(:id_user)"),
                {"id_user": user.id_user}
            )
            db.commit()
            return 1
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def reset_password(cls, email, new_password):
        try:
            db.execute(
                text("CALL sp_reset_password(:email, :password)"),
                {"email": email, "password": new_password}
            )
            db.commit()
            return 1
        except Exception as ex:
            db.rollback()
            raise Exception(ex)