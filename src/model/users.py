import json

class users:
    def __init__(self,id_user,username,password,email,person,role):
        self.id_user=id_user
        self.username=username
        self.password=password
        self.email=email
        self.person=person
        self.role=role

    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)