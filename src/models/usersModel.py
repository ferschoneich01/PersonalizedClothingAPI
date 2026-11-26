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

    @classmethod
    def get_user_addresses(cls, username):
        try:
            user_row = db.execute(
                text("""
                    SELECT u.person, u.email, p.name, p.lastname, p.phone, p.cedula, p.city
                    FROM users u
                    LEFT JOIN person p ON p.id_person = u.person
                    WHERE u.username = :username
                    LIMIT 1
                """),
                {"username": username}
            ).fetchone()

            if not user_row or not user_row[0]:
                return {"profile": None, "addresses": []}

            person_id = user_row[0]
            profile = {
                "email":    user_row[1] or "",
                "name":     user_row[2] or "",
                "lastname": user_row[3] or "",
                "phone":    user_row[4] or "",
                "cedula":   user_row[5] or "",
                "city":     user_row[6] or "Managua",
            }

            rows = db.execute(
                text("""
                    SELECT id_address_person, address, city
                    FROM addres_persons
                    WHERE person = :person_id
                      AND COALESCE(TRIM(address), '') <> ''
                    ORDER BY id_address_person DESC
                """),
                {"person_id": person_id}
            ).fetchall()

            seen = set()
            addresses = []
            for r in rows:
                raw_addr = (r[1] or "").strip()
                norm_key = " ".join(raw_addr.lower().split())
                if norm_key in seen:
                    continue
                seen.add(norm_key)
                addresses.append({
                    "id_address_person": r[0],
                    "address": raw_addr,
                    "city": (r[2] or "Managua").strip(),
                })

            return {"profile": profile, "addresses": addresses}
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_user_address(cls, username, address, city="Managua"):
        try:
            person_id = db.execute(
                text("SELECT person FROM users WHERE username = :username LIMIT 1"),
                {"username": username}
            ).scalar()

            if not person_id:
                raise ValueError("Usuario no encontrado.")

            clean_address = str(address or "").strip()
            clean_city = str(city or "Managua").strip() or "Managua"
            if not clean_address:
                raise ValueError("La dirección es requerida.")

            # Evitar duplicados exactos para la misma persona
            existing = db.execute(
                text("""
                    SELECT id_address_person, address, city
                    FROM addres_persons
                    WHERE person = :person_id AND LOWER(TRIM(address)) = LOWER(:addr)
                    LIMIT 1
                """),
                {"person_id": person_id, "addr": clean_address}
            ).fetchone()

            if existing:
                return {
                    "id_address_person": existing[0],
                    "address": existing[1],
                    "city": existing[2] or clean_city,
                }

            row = db.execute(
                text("""
                    INSERT INTO addres_persons (address, person, city)
                    VALUES (:address, :person_id, :city)
                    RETURNING id_address_person, address, city
                """),
                {"address": clean_address, "person_id": person_id, "city": clean_city}
            ).fetchone()
            db.commit()

            return {
                "id_address_person": row[0],
                "address": row[1],
                "city": row[2] or clean_city,
            }
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def delete_user_address(cls, username, id_address_person):
        try:
            person_id = db.execute(
                text("SELECT person FROM users WHERE username = :username LIMIT 1"),
                {"username": username}
            ).scalar()

            if not person_id:
                return {"deleted": False, "archived": False}

            # Verificar si está referenciada por un envío histórico para no romper integridad referencial
            in_use = db.execute(
                text("SELECT COUNT(*) FROM shipping WHERE address = :aid"),
                {"aid": int(id_address_person)}
            ).scalar() or 0

            if in_use > 0:
                return {"deleted": False, "archived": True}

            row = db.execute(
                text("""
                    DELETE FROM addres_persons
                    WHERE id_address_person = :aid AND person = :person_id
                    RETURNING id_address_person
                """),
                {"aid": int(id_address_person), "person_id": person_id}
            ).fetchone()
            db.commit()
            return {"deleted": bool(row), "archived": False}
        except Exception as ex:
            db.rollback()
            raise Exception(ex)