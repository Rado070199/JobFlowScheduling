import json

class InitUstawienAplikacji(): 
    def __init__(self):
        with open('appsettings.json', 'r') as file:
            settings = json.load(file)
            self.jsonModel = Json(**settings)
                       
class Json():
    def __init__(self, PathToDataFiles):
        self.PathToDataFiles = PathToDataFiles