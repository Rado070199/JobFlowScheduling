import pandas as pd
import random
from datetime import datetime, timedelta
from Gant import PrintGant as pg
from Data import DataDownload as dd
from datetime import datetime, timedelta
from Initialize import InitAppSettings as ias
from Algorithms import GeneticAlgorithms as ga
from Algorytmy import AlgorytmyPrzypisujacy as ap

def MainApp():
    data = dd(initialize.jsonModel.PathToDataFiles)

    ############# - Przypisywanie GNIAZD oraz WYKLUCZEŃ dla MASZYN - #############
    for maszyna in data.maszyny_list:
        gniazdo = next((gniazdo for gniazdo in data.gniazda_list if gniazdo.symbol == maszyna.symbol_gniazda), None)
        wykluczeniaMaszyn = [wykluczenia for wykluczenia in data.wykluczenia_maszyn_list if wykluczenia.symbol_maszyny == maszyna.symbol]
        maszyna.gniazdo = gniazdo
        maszyna.wykluczenia = wykluczeniaMaszyn
         
    ############# - Przypisywanie KOMPETENCJI oraz WYKLUCZEŃ dla PRACOWNIKÓW - #############
    for pracownik in data.pracownicy_list:
        fragmenty_kompetencji = [pracownik.kod_kompetencji[i:i+4] for i in range(0, len(pracownik.kod_kompetencji), 4)] 
        lista_kompetencji = []
        for fragment in fragmenty_kompetencji:
            kod_kompetencji = fragment[:2]
            poziom_kompetencji = fragment[2:]
            nowa_kompetencja = next((kompetencja for kompetencja in data.kompetencje_list if kompetencja.symbol == kod_kompetencji), None)
            nowa_kompetencja.poziom = poziom_kompetencji
            lista_kompetencji.append(nowa_kompetencja)

        pracownik.kompetencje = lista_kompetencji
        wykluczeniaPracownika = [wykluczenia for wykluczenia in data.wykluczenia_pracownikow_list if wykluczenia.symbol_pracownika == pracownik.symbol]
        pracownik.wykluczeniaPracownika = wykluczeniaPracownika
    
    ############# - Przypisanie MASZYN i pracowników do MARSZRUT a marszrut do ZAMOWIEN_KLIENTA  - #############
    #algorithmsGenetic = ga.AlgorithmGeneticFlowShopScheduler(30, 0.8, 0.2, 0.2, 2000)
    #for element in algorithmsGenetic:
    #    print(element)
    
    # Sortowanie listy po dacie zamówienia rosnąco
    data.zamowienia_klientow = sorted(data.zamowienia_klientow, key=lambda z: z.termin)
    for zamowienie in data.zamowienia_klientow:
        marszruty_dla_zamowienia = [marszruta for marszruta in data.marszruty_list if marszruta.numer_zlecenia == zamowienie.numer_zlecenia]
        # Sortowanie operacji po id_operacji rosnąco (od najmniejszego do największego)
        marszruty_dla_zamowienia = sorted(marszruty_dla_zamowienia, key=lambda mdz: mdz.id_operacji, reverse=True)
            
        zamowienie = ap.PrzypisywanieMaszynIPracownikowDoOperacji(zamowienie, data.gniazda_list, marszruty_dla_zamowienia, data.maszyny_list, data.pracownicy_list)
        '''    
        for marszruta in marszruty_dla_zamowienia:
            gniazdo = next((gniazdo for gniazdo in data.gniazda_list if marszruta.symbol_gniazda == gniazdo.symbol), None)
            lista_pracownik_dla_zadania = next((pracownik for pracownik in data.pracownicy_list if any(kompetencja.symbol == gniazdo.kompetencja for kompetencja in pracownik.kompetencje)),None)
            lista_maszyna_dla_zadania = next(maszyna for maszyna in data.maszyny_list if marszruta.symbol_gniazda == maszyna.symbol_gniazda)
            marszruta.pracownik = lista_pracownik_dla_zadania
            marszruta.maszyna = lista_maszyna_dla_zadania
        zamowienie.operacje = marszruty_dla_zamowienia   
        '''
    ##### - Wyświetlamy ilość potrzebnych surowców i ilość w magazynie. - #####
    grupy = {}

    for surowiec in data.wymagane_surowce:
        if surowiec.indeks_czesci not in grupy:
            grupy[surowiec.indeks_czesci] = 0
        grupy[surowiec.indeks_czesci] += surowiec.ilosc

    for indeks_czesci, zapotrzebowanie in grupy.items():
        stan_magazynowy_dla_indeksu = next((czesc for czesc in data.stan_magazynowy if czesc.indeks_czesci == indeks_czesci), None)
        potrzeba_surowca = stan_magazynowy_dla_indeksu.ilosc - zapotrzebowanie
        print(f'indeks_czesci {indeks_czesci} Zapotrzebowanie(szt): {zapotrzebowanie} Dostępne w magazynie(szt): {stan_magazynowy_dla_indeksu.ilosc}')
        if potrzeba_surowca < 0:
            print(f'UWAGA brakuje {potrzeba_surowca*(-1)} szt surowca [indeks_czesci:{indeks_czesci}]')
    
    return data.zamowienia_klientow

################################-START-################################
# Ładowanie ustawiń aplikacji
initialize =  ias()
# Inicjalizacja danych dla harmonogramowania
orders = MainApp()
# Wyświetlenie harmonogramu GANTA
pg.ShowGant(orders)