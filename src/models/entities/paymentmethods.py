import json

class paymentmethods:
    def __init__(self,id_paymentmethod, method):
        self.id_paymentmethod=id_paymentmethod
        self.method=method
        

    def to_json(self):
       
        return {
            'id_paymentmethod': self.id_paymentmethod,
            'method': self.method
        }