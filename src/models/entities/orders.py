import json

class orders:
    def __init__(self,id_order, orderdate=None, paymentmethod=None, id_user=None, id_status=None):
        self.id_order=id_order
        self.orderdate=orderdate
        self.paymentmethod=paymentmethod
        self.id_user=id_user
        self.id_status=id_status
     
    def to_json(self):
        
        return {
            'id_order': self.id_order,
            'orderdate': self.orderdate,
            'paymentmethod': self.paymentmethod, 
            'id_user': self.id_user,
            'id_status': self.id_status
        }