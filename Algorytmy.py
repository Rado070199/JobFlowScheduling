import pandas as pd
from Maszyny import Wykluczenie_maszyny
from Pracownicy import Wykluczenie_pracownika

class AlgorytmyPrzypisujace():
    ############# - Przypisywanie GNIAZD oraz WYKLUCZEŃ dla MASZYN - #############
    def PrzypisywanieGniazdOrazWykluczenDlaMaszyn(maszyny, gniazda, wykluczenia_maszyn):
        for maszyna in maszyny:
            gniazdo = next((gniazdo for gniazdo in gniazda if gniazdo.symbol == maszyna.symbol_gniazda), None)
            wykluczeniaMaszyn = [wykluczenia for wykluczenia in wykluczenia_maszyn if wykluczenia.symbol_maszyny == maszyna.symbol]
            maszyna.gniazdo = gniazdo
            maszyna.wykluczenia = wykluczeniaMaszyn
        return maszyny

    ############# - Przypisywanie KOMPETENCJI oraz WYKLUCZEŃ dla PRACOWNIKÓW - #############
    def PrypisanieKompetencjiOrazWykluczenDlaPracownikow(pracownicy, kompetencje, wykluczenia_pracownikow):
        for pracownik in pracownicy:
            fragmenty_kompetencji = [pracownik.kod_kompetencji[i:i+4] for i in range(0, len(pracownik.kod_kompetencji), 4)] 
            lista_kompetencji = []
            for fragment in fragmenty_kompetencji:
                kod_kompetencji = fragment[:2]
                poziom_kompetencji = fragment[2:]
                nowa_kompetencja = next((kompetencja for kompetencja in kompetencje if kompetencja.symbol == kod_kompetencji), None)
                nowa_kompetencja.poziom = poziom_kompetencji
                lista_kompetencji.append(nowa_kompetencja)     
            pracownik.kompetencje = lista_kompetencji
            wykluczeniaPracownika = [wykluczenia for wykluczenia in wykluczenia_pracownikow if wykluczenia.symbol_pracownika == pracownik.symbol]
            pracownik.wykluczeniaPracownika = wykluczeniaPracownika
        return pracownicy
        
    ############# - Przypisywanie PRACOWNIKÓW oraz MASZYN do MARSZRUT a MARSZRUT do ZAMÓWIENIA KLIENTA - #############    
    def PrzypisywanieMaszynIPracownikowDoOperacji(zamowienia, gniazda, marszruty, maszyny, pracownicy):
        zamowienia = sorted(zamowienia, key=lambda z: z.termin)
        for zamowienie in zamowienia:
            marszruty_dla_zamowienia = [marszruta for marszruta in marszruty if marszruta.numer_zlecenia == zamowienie.numer_zlecenia]
            # Sortowanie operacji po id_operacji rosnąco (od najmniejszego do największego)
            marszruty_dla_zamowienia = sorted(marszruty_dla_zamowienia, key=lambda mdz: mdz.id_operacji, reverse=True)
            for marszruta in marszruty_dla_zamowienia:
                gniazdo = next((gniazdo for gniazdo in gniazda if marszruta.symbol_gniazda == gniazdo.symbol), None)
                maszyny_dla_gniazda = [
                    maszyna for maszyna in maszyny
                    if marszruta.symbol_gniazda == maszyna.symbol_gniazda
                ]   
                pracownicy_dla_kompetencji = [
                    pracownik for pracownik in pracownicy
                    if any(kompetencja.symbol == gniazdo.kompetencja for kompetencja in pracownik.kompetencje)
                ]
                
                data_koncowa = zamowienie.termin
                start_date = data_koncowa - pd.Timedelta(seconds=marszruta.czas_trwania_operacji)
                # wyszukaj z listy maszyn, maszyn które są dostępne w danym terminie.
                maszyny_dostepne = [
                    maszyna for maszyna in maszyny_dla_gniazda
                    if not any(
                        wylaczenie.data_od >= data_koncowa and wylaczenie.data_do <= start_date
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
                    pracownik for pracownik in pracownicy_dla_kompetencji
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
                
            zamowienie.operacje = marszruty_dla_zamowienia   
                
        return zamowienia
    
