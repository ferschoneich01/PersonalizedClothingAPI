import json

class role:
    def __init__(self,id_role, name):
        self.id_role=id_role
        self.name=name
        
    def to_json(self):
       
        return {
            'id_role': self.id_role,
            'name': self.name
        }