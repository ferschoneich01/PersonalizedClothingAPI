import json

class orders:
    def __init__(self,id_order, orderdate, paymentmethod, id_user, id_status):
        self.id_order=id_order
        self.orderdate=orderdate
        self.paymentmethod=paymentmethod
        self.id_user=id_user
        self.id_status=id_status
     
    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)