import json

class person:
    def __init__(self,id_person, cedula, name, lastname, birthday, phone, country, city, sex):
        self.id_person = id_person
        self.cedula=cedula
        self.name=name
        self.lastname=lastname
        self.birthday=birthday
        self.phone=phone
        self.country=country
        self.city=city
        self.sex=sex

    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return {
            'id_person': self.id_person,
            'cedula': self.cedula,
            'name': self.name,
            'lastname': self.lastname,
            'birthday': self.birthday,
            'phone': self.phone,
            'country': self.country,
            'city': self.city,
            'sex': self.sex
        }