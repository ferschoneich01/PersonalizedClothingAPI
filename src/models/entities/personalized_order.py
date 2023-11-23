import json

class personalized_order:
    def __init__(self,id_porder, id_order, id_pitem):
        self.id_porder=id_porder
        self.id_order=id_order
        self.id_pitem=id_pitem
        
    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)