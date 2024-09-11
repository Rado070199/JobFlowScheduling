import pandas as pd
import plotly.express as px

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

class PrintGant:
    
    @staticmethod
    def ShowGant(zamowienia_klienta):
        # Przygotowanie danych do wykresu Gantta
        gantt_data = []

        for zamowienie in zamowienia_klienta:
            # Sortowanie operacji po id_operacji rosnąco (od najmniejszego do największego)
            sorted_operacje = sorted(zamowienie.operacje, key=lambda op: op.id_operacji, reverse=True)

            end_date = zamowienie.termin
            for operacja in sorted_operacje:
                # Obliczamy start operacji na podstawie terminu końcowego
                start_date = end_date - pd.Timedelta(seconds=operacja.czas_trwania_operacji)
                
                gantt_data.append({
                    'Order': zamowienie.numer_zlecenia,  # numer zlecenia na osi Y
                    'Task': f"Operacja {operacja.id_operacji}",
                    'Start': start_date,  # Czas startu operacji
                    'Finish': end_date,  # Termin zakończenia
                    'Machine': str(operacja.maszyna.symbol) if operacja.maszyna.symbol else 'Brak danych',  # Zamiana obiektu na string
                    'Worker': str(operacja.pracownik.symbol) if operacja.pracownik.symbol else 'Brak danych',  # Zamiana obiektu na string
                    'Operation': operacja.symbol_gniazda
                })

                # Zaktualizuj koniec dla kolejnej operacji
                end_date = start_date

        # Konwersja do DataFrame
        df_gantt = pd.DataFrame(gantt_data)

        # Tworzenie wykresu Gantta
        fig = px.timeline(
            df_gantt,
            x_start='Start',
            x_end='Finish',
            y='Order',  # numer zlecenia na osi Y
            color='Operation',  # Kolorowanie według gniazda (maszyny/gniazda)
            labels={'Operation': 'Gniazdo'},
            title='Harmonogram zleceń i przypisanych operacji',
            hover_name='Task',
            hover_data={
                'Start': True,
                'Finish': True,
                'Machine': True,
                'Worker': True
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