import json

class addres_person:
    def __init__(self,id_addres_person, addres, person, city):
        self.id_addres_person=id_addres_person
        self.addres=addres
        self.person=person
        self.city=city
        
    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)