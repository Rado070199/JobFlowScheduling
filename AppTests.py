from Zamowienia import Stan_magazynowy, Wymagany_surowiec, Marszruty, Zamowienie_klienta
import unittest

# Testy dla klasy Zamowienie_klienta
class TestZamowienieKlienta(unittest.TestCase):
    
    def test_initialization(self):
        numer_zlecenia = "ZL001"
        ilosc_zlecona = 100
        termin = "2024-09-30"
        operacje = ["Operacja 1", "Operacja 2"]
        surowce = ["Surowiec 1", "Surowiec 2"]
        
        zamowienie = Zamowienie_klienta(numer_zlecenia, ilosc_zlecona, termin, operacje, surowce)
        
        self.assertEqual(zamowienie.numer_zlecenia, numer_zlecenia)
        self.assertEqual(zamowienie.ilosc_zlecona, ilosc_zlecona)
        self.assertEqual(zamowienie.termin, termin)
        self.assertEqual(zamowienie.operacje, operacje)
        self.assertEqual(zamowienie.surowce, surowce)

    def test_default_values(self):
        zamowienie = Zamowienie_klienta("ZL002", 50, "2024-10-01")
        
        self.assertIsNone(zamowienie.operacje)
        self.assertIsNone(zamowienie.surowce)

# Testy dla klasy Marszruty
class TestMarszruty(unittest.TestCase):
    
    def test_initialization(self):
        numer_zlecenia = "ZL123"
        id_operacji = 101
        symbol_gniazda = "GN567"
        czas_miedzyoperacyjny = 30
        tj_robotnika = 10
        tj_maszyny = 15
        ilosc_do_wykonania = 5
        maszyna = "Maszyna A"
        pracownik = "Pracownik B"
        
        marszruta = Marszruty(numer_zlecenia, id_operacji, symbol_gniazda, czas_miedzyoperacyjny, tj_robotnika, tj_maszyny, ilosc_do_wykonania, maszyna, pracownik)
        
        expected_czas_trwania = ((tj_robotnika + tj_maszyny) * ilosc_do_wykonania) + czas_miedzyoperacyjny
        self.assertEqual(marszruta.czas_trwania_operacji, expected_czas_trwania)

    def test_default_values(self):
        marszruta = Marszruty("ZL124", 102, "GN568", 20, 8, 12, 3)
        
        self.assertIsNone(marszruta.maszyna)
        self.assertIsNone(marszruta.pracownik)

# Testy dla klasy Wymagany_surowiec
class TestWymaganySurowiec(unittest.TestCase):
    
    def test_initialization(self):
        numer_zlecenia = "ZL125"
        ilosc = 50
        indeks_czesci = "CZE001"
        
        surowiec = Wymagany_surowiec(numer_zlecenia, ilosc, indeks_czesci)
        
        self.assertEqual(surowiec.numer_zlecenia, numer_zlecenia)
        self.assertEqual(surowiec.ilosc, ilosc)
        self.assertEqual(surowiec.indeks_czesci, indeks_czesci)

    def test_with_dostepna_ilosc(self):
        surowiec = Wymagany_surowiec("ZL126", 25, "CZE002")
        self.assertEqual(surowiec.ilosc, 25)

# Testy dla klasy Stan_magazynowy
class TestStanMagazynowy(unittest.TestCase):
    
    def test_initialization(self):
        indeks_czesci = "CZE003"
        ilosc = 200
        
        stan = Stan_magazynowy(indeks_czesci, ilosc)
        
        self.assertEqual(stan.indeks_czesci, indeks_czesci)
        self.assertEqual(stan.ilosc, ilosc)

# Uruchomienie wszystkich testów
if __name__ == '__main__':
    unittest.main()
