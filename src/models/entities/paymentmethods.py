import json

class paymentmethods:
    def __init__(self,id_paymentmethod, method):
        self.id_paymentmethod=id_paymentmethod
        self.method=method
        

    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)