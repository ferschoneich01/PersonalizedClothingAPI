import json

class status:
    def __init__(self,id_status, status):
        self.id_status=id_status
        self.status=status
        
    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)