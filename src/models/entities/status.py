import json

class status:
    def __init__(self,id_status, status):
        self.id_status=id_status
        self.status=status
        
    def to_json(self):
        
        return {
            'id_status': self.id_status,
            'status': self.status
        }