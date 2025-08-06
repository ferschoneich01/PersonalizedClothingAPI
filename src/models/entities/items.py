import json

class items:
    def __init__(self,id_item, name, description, image, price, clasification, category, status_item):
        self.id_item=id_item
        self.name=name
        self.description=description
        self.image=image
        self.price=price
        self.clasification=clasification
        self.category=category
        self.status_item=status_item
        
    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return {
            'id_item': self.id_item,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'price': self.price,
            'clasification': self.clasification,
            'category': self.category,
            'status_item':self.status_item
        }