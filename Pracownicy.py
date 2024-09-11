class Pracownik():
    def __init__(self, symbol, imie, nazwisko, kod_kompetencji, kompetencje = None, wykluczeniePracownika = None):
        self.symbol = symbol
        self.imie = imie
        self.nazwisko = nazwisko
        self.kod_kompetencji = kod_kompetencji
        self.kompetencje = kompetencje
        self.wykluczeniaPracownika = wykluczeniePracownika
             
class Kompetencja():
    def __init__(self, symbol, nazwa, poziom = None):
        self.symbol = symbol
        self.nazwa = nazwa
        self.poziom = poziom
        
class Wykluczenie_pracownika():
    def __init__(self, symbol_pracownika, data_od, data_do):
        self.symbol_pracownika = symbol_pracownika
        self.data_od = data_od
        self.data_do = data_do