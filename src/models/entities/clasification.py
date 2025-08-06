import json

class clasification:
    def __init__(self,id_clasification, name):
        self.id_clasification=id_clasification
        self.name=name
        

    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return {
            'id_clasification': self.id_clasification,
            'name': self.name
        }