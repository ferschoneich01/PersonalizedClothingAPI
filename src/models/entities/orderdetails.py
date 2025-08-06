import json

class orderdetails:
    def __init__(self,id_orderdetail, color, size, item, quantity, id_order):
        self.id_orderdetail=id_orderdetail
        self.color=color
        self.size=size
        self.item=item
        self.quantity=quantity
        self.id_order=id_order
        
    def to_json(self):
        # Convertir el objeto a un diccionario y luego a una cadena JSON
        return {
            'id_orderdetail': self.id_orderdetail,
            'color': self.color,
            'size': self.size,
            'item': self.item,
            'quantity': self.quantity,
            'id_order': self.id_order
        }