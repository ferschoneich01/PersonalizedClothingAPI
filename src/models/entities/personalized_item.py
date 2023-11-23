import json

class personalized_item:
    def __init__(self,id_pitem, indications, design, position):
        self.id_pitem=id_pitem
        self.indications=indications
        self.design=design
        self.position=position
        
    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)