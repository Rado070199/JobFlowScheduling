import pandas as pd
from Maszyny import Maszyna, Gniazdo, Wykluczenie_maszyny
from Pracownicy import Pracownik, Kompetencja, Wykluczenie_pracownika
from Zamowienia import Stan_magazynowy, Wymagany_surowiec, Marszruty, Zamowienie_klienta

#Klasa inicjalizuje dane wejściowe używane w generowaniu harmonogramu gantta dla produkcji.
class DataDownload():
    def __init__(self, dataFilePath):
        df_gniazda = pd.read_excel(dataFilePath, sheet_name='GNIAZDA')
        self.gniazda_list = zamien_na_liste_gniazd(df_gniazda)    
        df_wykluczenia_maszyn = pd.read_excel(dataFilePath, sheet_name='WYKLUCZENIA_MASZYNY')
        self.wykluczenia_maszyn_list = zamien_na_liste_wykluczen_maszyn(df_wykluczenia_maszyn)      
        df_maszyny = pd.read_excel(dataFilePath, sheet_name='MASZYNY')
        self.maszyny_list =  zamien_na_liste_maszyn(df_maszyny)
        
        df_kompetencje = pd.read_excel(dataFilePath, sheet_name='KOMPETENCJE')
        self.kompetencje_list = zamien_na_liste_kompetencji(df_kompetencje)
        df_wykluczenia_pracownikow = pd.read_excel(dataFilePath, sheet_name='WYKLUCZENIA_PRACOWNICY')
        self.wykluczenia_pracownikow_list = zamien_na_liste_wykluczen_pracownikow(df_wykluczenia_pracownikow)
        df_pracownicy = pd.read_excel(dataFilePath, sheet_name='PRACOWNICY')
        self.pracownicy_list = zamien_na_liste_pracownikow(df_pracownicy)
        
        df_dostepne_surowce = pd.read_excel(dataFilePath, sheet_name='STAN_MAGAZYNOWY')
        self.stan_magazynowy = zamien_na_liste_dostepne_surowce(df_dostepne_surowce)
        df_wymagane_surowce = pd.read_excel(dataFilePath, sheet_name='WYMAGANE_SUROWCE')
        self.wymagane_surowce = zamien_na_liste_wymagane_surowce(df_wymagane_surowce)
        df_marszruty = pd.read_excel(dataFilePath, sheet_name='MARSZRUTY')
        self.marszruty_list = zamien_na_liste_marszruty(df_marszruty)
        df_zamowienia_klientow = pd.read_excel(dataFilePath, sheet_name='ZAMOWIENIA_KLIENTA')
        self.zamowienia_klientow = zamien_na_liste_zamowienia_klienta(df_zamowienia_klientow)
        
        
# Maszyny
def zamien_na_liste_gniazd(df_gniazda):
    gniazda_list = []
    for _, row in df_gniazda.iterrows():
        gniazdo = Gniazdo(row['SYMBOL'], row['KOMPETENCJA'], row['NAZWA'])
        gniazda_list.append(gniazdo)
    return gniazda_list
    
def zamien_na_liste_wykluczen_maszyn(df_wykluczenia_maszyn):
    wykluczenia_maszyn_list = []
    for _, row in df_wykluczenia_maszyn.iterrows():
        wykluczenie = Wykluczenie_maszyny(row['SYMBOL_MASZYNY'], row['DATA_OD'], row['DATA_DO'])
        wykluczenia_maszyn_list.append(wykluczenie)
    return wykluczenia_maszyn_list    
    
def zamien_na_liste_maszyn(df_maszyny):
    maszyny_list = []
    for _, row in df_maszyny.iterrows():
        maszyna = Maszyna(row['SYMBOL'], row['NAZWA'], row['SYMBOL_GNIAZDA'], row['NAZWA'])
        maszyny_list.append(maszyna)
    return maszyny_list
    
# Pracownicy
def zamien_na_liste_kompetencji(df_kompetencje):
    kompetencje_list = []
    for _, row in df_kompetencje.iterrows():
        kompetencja = Kompetencja(row['SYMBOL'], row['NAZWA'])
        kompetencje_list.append(kompetencja)
    return kompetencje_list
    
def zamien_na_liste_wykluczen_pracownikow(df_wykluczenia_pracownikow):
    wykluczenia_pracownikow_list = []
    for _, row in df_wykluczenia_pracownikow.iterrows():
        wykluczenie = Wykluczenie_pracownika(row['SYMBOL_PRACOWNIKA'], row['DATA_OD'], row['DATA_DO'])
        wykluczenia_pracownikow_list.append(wykluczenie)
    return wykluczenia_pracownikow_list    
    
def zamien_na_liste_pracownikow(df_pracownicy):
    pracownicy_list = []
    for _, row in df_pracownicy.iterrows():
        pracownik = Pracownik(row['SYMBOL'], row['IMIE'], row['NAZWISKO'], row['KOD_KOMPETENCJI'])
        pracownicy_list.append(pracownik)
    return pracownicy_list

# Zamowienia 
def zamien_na_liste_dostepne_surowce(df_dostepne_surowce):
    dostepne_surowce_list = []
    for _, row in df_dostepne_surowce.iterrows():
        dostepny_surowiec = Stan_magazynowy(row['INDEKS_CZESCI'], row['ILOSC'])
        dostepne_surowce_list.append(dostepny_surowiec)
    return dostepne_surowce_list
    
def zamien_na_liste_wymagane_surowce(df_wymagane_surowce):
    Wymagane_surowce_list = []
    for _, row in df_wymagane_surowce.iterrows():
        wymagany_surowiec = Wymagany_surowiec(row['NUMER_ZLECENIA'], row['ILOSC'], row['INDEKS_CZESCI'])
        Wymagane_surowce_list.append(wymagany_surowiec)
    return Wymagane_surowce_list    
    
def zamien_na_liste_marszruty(df_marszruty):
    marszruty_list = []
    for _, row in df_marszruty.iterrows():
        marszruta = Marszruty(row['NUMER_ZLECENIA'], row['ID_OPERACJI'], row['SYMBOL_GNIAZDA'], row['CZAS_MIEDZYOPERACYJNY'], row['TJ_ROBOTNIKA'], row['TJ_MASZYNY'], row['ILOSC_DO_WYKONANIA'])
        marszruty_list.append(marszruta)
    return marszruty_list

def zamien_na_liste_zamowienia_klienta(df_zamowienia_klienta):
    kompetencje_list = []
    for _, row in df_zamowienia_klienta.iterrows():
        maszyna = Zamowienie_klienta(row['NUMER_ZLECENIA'], row['ILOSC_ZLECONA'], row['TERMIN'])
        kompetencje_list.append(maszyna)
    return kompetencje_list