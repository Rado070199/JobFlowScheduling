import json

class InitAppSettings(): 
    def __init__(self):
        with open('appsettings.json', 'r') as file:
            settings = json.load(file)
            self.jsonModel = JsonModel(**settings)
                       
class JsonModel():
    def __init__(self, PathToDataFiles):
        self.PathToDataFiles = PathToDataFiles