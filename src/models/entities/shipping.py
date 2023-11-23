import json

class shipping:
    def __init__(self,id_shipping, shipdate, cost, id_order, address):
        self.id_shipping=id_shipping
        self.shipdate=shipdate
        self.cost=cost
        self.id_order=id_order
        self.address=address
        
    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)