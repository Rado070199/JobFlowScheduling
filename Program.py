import pandas as pd
from Wyswietl import Pokaz as p
from Data import DataDownload as dd
from Inicjalizacja import InitUstawienAplikacji as iua
from Algorytmy import AlgorytmyPrzypisujace as ap

def OperacjeNaDanych(data):
    ############# - Przypisywanie GNIAZD oraz WYKLUCZEŃ dla MASZYN - #############
    data.maszyny_list = ap.PrzypisywanieGniazdOrazWykluczenDlaMaszyn(data.maszyny_list, data.gniazda_list, data.wykluczenia_maszyn_list)        
    ############# - Przypisywanie KOMPETENCJI oraz WYKLUCZEŃ dla PRACOWNIKÓW - #############
    data.pracownicy_list = ap.PrypisanieKompetencjiOrazWykluczenDlaPracownikow(data.pracownicy_list, data.kompetencje_list, data.wykluczenia_pracownikow_list)   
    ############# - Przypisywanie PRACOWNIKÓW oraz MASZYN do MARSZRUT a MARSZRUT do ZAMÓWIENIA KLIENTA - #############
    data.zamowienia_klientow = ap.PrzypisywanieMaszynIPracownikowDoOperacji(data.zamowienia_klientow, data.gniazda_list, data.marszruty_list, data.maszyny_list, data.pracownicy_list)
    
    return data.zamowienia_klientow

################################ - START - ################################
# Ładowanie ustawiń aplikacji
initialize =  iua()
# Pobieranie danych
data = dd(initialize.jsonModel.PathToDataFiles)
# Wyświetlamy ilość potrzebnych surowców i ilość w magazynie
p.WyswietlIloscWymaganychSurowcowIStanyMagazynoweKonsola(data.wymagane_surowce, data.stan_magazynowy)
# Inicjalizacja danych dla harmonogramowania
zamowienia_klientow = OperacjeNaDanych(data)
# Wyświetlenie harmonogramu GANTA
p.GenerujGantDlaZamowienKlientow(zamowienia_klientow)