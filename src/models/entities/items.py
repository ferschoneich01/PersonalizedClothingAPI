import json

class items:
    def __init__(self,id_item, name, description, image, price, clasification, category):
        self.id_item=id_item
        self.name=name
        self.description=description
        self.image=image
        self.price=price
        self.clasification=clasification
        self.category=category
        
    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return json.dumps(self.__dict__)