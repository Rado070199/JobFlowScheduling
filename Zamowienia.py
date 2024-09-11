class Zamowienie_klienta():
    def __init__(self, numer_zlecenia, ilosc_zlecona, termin, operacje = None, surowce = None):
        self.numer_zlecenia = numer_zlecenia
        self.ilosc_zlecona = ilosc_zlecona
        self.termin = termin
        self.operacje = operacje
        self.surowce = surowce
        
class Marszruty():
    def __init__(self, numer_zlecenia, id_operacji, symbol_gniazda, czas_miedzyoperacyjny, tj_robotnika, tj_maszyny, ilosc_do_wykonania, maszyna = None, pracownik = None):
        self.numer_zlecenia = numer_zlecenia
        self.id_operacji = id_operacji
        self.symbol_gniazda = symbol_gniazda
        self.czas_trwania_operacji = ((tj_robotnika + tj_maszyny) * ilosc_do_wykonania) + czas_miedzyoperacyjny
        self.maszyna = maszyna
        self.pracownik = pracownik
        
class Wymagany_surowiec():
    def __init__(self, numer_zlecenia, ilosc, indeks_czesci):
        self.numer_zlecenia = numer_zlecenia
        self.ilosc = ilosc
        self.indeks_czesci = indeks_czesci
        
class Stan_magazynowy():
    def __init__(self, indeks_czesci, ilosc):
        self.indeks_czesci = indeks_czesci
        self.ilosc = ilosc