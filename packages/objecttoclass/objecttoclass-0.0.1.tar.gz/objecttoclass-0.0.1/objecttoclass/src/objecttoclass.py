class ObjectToClass:
    def __init__(self,data:dict):
        for key,value in data.items():
            setattr(self,key,value)
OTC = ObjectToClass


