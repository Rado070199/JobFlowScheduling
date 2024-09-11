import pandas as pd
from Maszyny import Wykluczenie_maszyny
from Pracownicy import Wykluczenie_pracownika

class AlgorytmyPrzypisujacy():
    def PrzypisywanieMaszynIPracownikowDoOperacji(zamowienie, gniazda, marszruty, maszyny, pracownicy):
        for marszruta in marszruty:
            gniazdo = next((gniazdo for gniazdo in gniazda if marszruta.symbol_gniazda == gniazdo.symbol), None)
            maszyny_dla_g = [
                maszyna for maszyna in maszyny
                if marszruta.symbol_gniazda == maszyna.symbol_gniazda
            ]   
            pracownicy_dla_k = [
                pracownik for pracownik in pracownicy
                if any(kompetencja.symbol == gniazdo.kompetencja for kompetencja in pracownik.kompetencje)
            ]
            
            data_koncowa = zamowienie.termin
            start_date = data_koncowa - pd.Timedelta(seconds=marszruta.czas_trwania_operacji)
            # wyszukaj z listy maszyn, maszyn które są dostępne w danym terminie.
            maszyny_dostepne = [
                maszyna for maszyna in maszyny_dla_g
                if not any(
                    wylaczenie.data_od <= data_koncowa and wylaczenie.data_do >= start_date
                    for wylaczenie in (maszyna.wykluczeniaMaszyny or [])
                )
            ]
            # Wybierz jedną maszynę.
            maszyna_wybrana = next((maszyna for maszyna in maszyny_dostepne), None)
            
            if maszyna_wybrana:
                if maszyna_wybrana.wykluczeniaMaszyny is None:
                    maszyna_wybrana.wykluczeniaMaszyny = []
            
            # Tworzymy nowe wykluczenie dla maszyny
            nowe_wykluczenie_maszyny = Wykluczenie_maszyny(
                symbol_maszyny=maszyna_wybrana.symbol,
                data_od=start_date,
                data_do=data_koncowa
            )
            maszyna_wybrana.wykluczeniaMaszyny.append(nowe_wykluczenie_maszyny)
            
            # wyszukaj z listy pracowników, pracowników którzy są dostępne w danym terminie.
            pracownicy_dostepni = [
                pracownik for pracownik in pracownicy_dla_k
                if not any(
                    wylaczenie.data_od <= data_koncowa and wylaczenie.data_do >= start_date
                    for wylaczenie in (pracownik.wykluczeniaPracownika or [])
                )
            ]
            # Wybierz jednego pracownika.
            pracownik_wybrany = next((prcownik for prcownik in pracownicy_dostepni), None)
            
            if pracownik_wybrany:
                if pracownik_wybrany.wykluczeniaPracownika is None:
                    pracownik_wybrany.wykluczeniaPracownika = []
            
            # Tworzymy nowe wykluczenie dla maszyny
            nowe_wykluczenie_pracownika = Wykluczenie_pracownika(
                symbol_pracownika=pracownik_wybrany.symbol,
                data_od=start_date,
                data_do=data_koncowa
            )
            pracownik_wybrany.wykluczeniaPracownika.append(nowe_wykluczenie_pracownika)

            marszruta.maszyna = maszyna_wybrana
            marszruta.pracownik = pracownik_wybrany
            
        zamowienie.operacje = marszruty   
            
        return zamowienie