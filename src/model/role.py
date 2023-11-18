import json

class role:
    def __init__(self,id_role, name):
        self.id_role=id_role
        self.name=name
        
    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)