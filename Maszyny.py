class Maszyna():
    def __init__(self, symbol, nazwa, symbol_gniazda, gniazdo = None, wykluczeniaMaszyny = None):
        self.symbol = symbol
        self.nazwa = nazwa
        self.symbol_gniazda = symbol_gniazda
        self.gniazdo = gniazdo
        self.wykluczeniaMaszyny = wykluczeniaMaszyny      
        
class Gniazdo():
    def __init__(self, symbol, kompetencja, nazwa):
        self.symbol = symbol
        self.kompetencja = kompetencja
        self.nazwa = nazwa
        
class Wykluczenie_maszyny():
    def __init__(self, symbol_maszyny, data_od, data_do):
        self.symbol_maszyny = symbol_maszyny
        self.data_od = data_od
        self.data_do = data_do
        
