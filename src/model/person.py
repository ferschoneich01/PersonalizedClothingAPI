import json

class person:
    def __init__(self,id_person, cedula, name, lastname, birthday, phone, country, city, sex):
        self.id_person = id_person
        self.cedula=cedula
        self.name=name
        self.lastname=lastname
        self.birthday=birthday
        self.phone=phone
        self.country
        self.city
        self.sex=sex

    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)