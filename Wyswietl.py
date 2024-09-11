import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

class Pokaz:
    def GenerujGantDlaZamowienKlientow(zamowienia_klienta):
        # Przygotowanie danych do wykresu Gantta
        gantt_data = []

        for zamowienie in zamowienia_klienta:

            end_date = zamowienie.termin
            for operacja in zamowienie.operacje:
                # Obliczamy start operacji na podstawie terminu końcowego
                start_date = end_date - pd.Timedelta(seconds=operacja.czas_trwania_operacji)
                
                gantt_data.append({
                    'Zamowienie klienta': zamowienie.numer_zlecenia,  # numer zlecenia na osi Y
                    'Marszruta': f"Operacja {operacja.id_operacji}",
                    'Start': start_date,  # Czas startu operacji
                    'Koniec': end_date,  # Termin zakończenia
                    'Maszyna': str(operacja.maszyna.symbol) if operacja.maszyna.symbol else 'Brak danych',  # Zamiana obiektu na string
                    'Pracownik': str(operacja.pracownik.symbol) if operacja.pracownik.symbol else 'Brak danych',  # Zamiana obiektu na string
                    'Gniazdo': operacja.symbol_gniazda
                })

                # Zaktualizuj koniec dla kolejnej operacji
                end_date = start_date

        # Konwersja do DataFrame
        df_gantt = pd.DataFrame(gantt_data)

        # Tworzenie wykresu Gantta
        fig = px.timeline(
            df_gantt,
            x_start='Start',
            x_end='Koniec',
            y='Zamowienie klienta',  # numer zlecenia na osi Y
            color='Marszruta',  # Kolorowanie według gniazda (maszyny/gniazda)
            labels={'Marszruta': 'Gniazdo'},
            title='Harmonogram zleceń i przypisanych operacji',
            hover_name='Marszruta',
            hover_data={
                'Start': True,
                'Koniec': True,
                'Maszyna': True,
                'Pracownik': True
            }
        )

        # Dostosowanie wyglądu wykresu, aby dodać pasek przewijania
        fig.update_layout(
            title='Harmonogram zleceń i przypisanych operacji',
            xaxis_title='Czas',
            yaxis_title='Numer zlecenia',  # Dodano opis osi Y
            showlegend=True,
            xaxis=dict(type='date'),
            yaxis=dict(
                autorange=False,
                fixedrange=False
            ),
            height=900  # Wysokość wykresu, dostosuj w zależności od liczby zleceń
        )

        # Wyświetlenie wykresu
        fig.show()

    ##### - Wyświetlamy ilość potrzebnych surowców i ilość w magazynie. - #####
    def WyswietlIloscWymaganychSurowcowIStanyMagazynoweKonsola(wymagane_surowce, stan_magazynowy):
        grupy = {}

        for surowiec in wymagane_surowce:
            if surowiec.indeks_czesci not in grupy:
                grupy[surowiec.indeks_czesci] = 0
            grupy[surowiec.indeks_czesci] += surowiec.ilosc

        for indeks_czesci, zapotrzebowanie in grupy.items():
            stan_magazynowy_dla_indeksu = next((czesc for czesc in stan_magazynowy if czesc.indeks_czesci == indeks_czesci), None)
            potrzeba_surowca = stan_magazynowy_dla_indeksu.ilosc - zapotrzebowanie
            print(f'indeks_czesci {indeks_czesci} Zapotrzebowanie(szt): {zapotrzebowanie} Dostępne w magazynie(szt): {stan_magazynowy_dla_indeksu.ilosc}')
            if potrzeba_surowca < 0:
                print(f'UWAGA brakuje {potrzeba_surowca*(-1)} szt surowca [indeks_czesci:{indeks_czesci}]')
    