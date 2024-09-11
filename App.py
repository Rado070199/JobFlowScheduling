import pandas as pd
import random
from datetime import datetime, timedelta
from Gant import PrintGant as pg
from Data import DataDownload as dd
from datetime import datetime, timedelta
from Initialize import InitAppSettings as ias
from Algorithms import GeneticAlgorithms as ga

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
        
        
    ##### - Wyświetlamy ilość potrzebnych surowców i ilość w magazynie. - #####
    grupy = {}

    # Grupowanie i sumowanie
    for surowiec in data.wymagane_surowce:
        if surowiec.indeks_czesci not in grupy:
            grupy[surowiec.indeks_czesci] = 0
        grupy[surowiec.indeks_czesci] += surowiec.ilosc

    # Wypisywanie wyników
    for indeks_czesci, zapotrzebowanie in grupy.items():
        stan_magazynowy_dla_indeksu = next((czesc for czesc in data.stan_magazynowy if czesc.indeks_czesci == indeks_czesci), None)
        potrzeba_surowca = stan_magazynowy_dla_indeksu.ilosc - zapotrzebowanie
        print(f'indeks_czesci {indeks_czesci} Zapotrzebowanie(szt): {zapotrzebowanie} Dostępne w magazynie(szt): {stan_magazynowy_dla_indeksu.ilosc}')
        if potrzeba_surowca < 0:
            print(f'UWAGA brakuje {potrzeba_surowca*(-1)} szt surowca [indeks_czesci:{indeks_czesci}]')
    
    ############# - Przypisanie MASZYN i pracowników do MARSZRUT a marszrut do ZAMOWIEN_KLIENTA  - #############
    #algorithmsGenetic = ga.AlgorithmGeneticFlowShopScheduler(30, 0.8, 0.2, 0.2, 2000)
    #for element in algorithmsGenetic:
    #    print(element)
    for zamowienie in data.zamowienia_klientow:
        marszruty_dla_zamowienia = [marszruta for marszruta in data.marszruty_list if marszruta.numer_zlecenia == zamowienie.numer_zlecenia]
        for marszruta in marszruty_dla_zamowienia:
            gniazdo = next((gniazdo for gniazdo in data.gniazda_list if marszruta.symbol_gniazda == gniazdo.symbol), None)
            marszruta.pracownik = next((pracownik for pracownik in data.pracownicy_list if any(kompetencja.symbol == gniazdo.kompetencja for kompetencja in pracownik.kompetencje)),None)
            marszruta.maszyna = next(maszyna for maszyna in data.maszyny_list if marszruta.symbol_gniazda == maszyna.symbol_gniazda)
        zamowienie.operacje = marszruty_dla_zamowienia
    
    return data.zamowienia_klientow
'''
def generate_sample_data(machine_df, orders_df, marszruty_df, employees_df):
    # Obliczanie liczby zadań dla każdego zlecenia
    task_counts = marszruty_df.groupby('NUMER_ZLECENIA').size()
    
    # Pobranie unikalnych zleceń
    orders = orders_df['NUMER_ZLECENIA'].unique()
    machines = machine_df['KOD'].tolist()
    machine_types = machine_df.set_index('KOD')['RODZAJ'].to_dict()  # Mapowanie maszyn na typy
    
    # Tworzenie listy pracowników
    employees = employees_df['KOD'].tolist()
    employee_names = employees_df.set_index('KOD').apply(lambda x: f"{x['IMIE']} {x['NAZWISKO']}", axis=1).to_dict()

    # Przechowywanie końcowego czasu pracy pracownika
    worker_end_time = {worker: datetime.min for worker in employees}

    tasks = []
    
    for order_id in orders:
        # Pobranie i przetłumaczenie terminu z orders_df
        order_due_date_str = orders_df.loc[orders_df['NUMER_ZLECENIA'] == order_id, 'TERMIN'].values[0]
        order_due_date_str = translate_date(order_due_date_str)  # Translacja miesiąca
        order_due_date = pd.to_datetime(order_due_date_str, format='%d-%b-%y')  # Konwersja na datetime
        
        # Ustalenie czasu rozpoczęcia zlecenia na kilka dni przed terminem
        order_start = order_due_date - timedelta(days=10)
        
        if order_id in task_counts:
            num_tasks_per_order = task_counts[order_id]
        else:
            num_tasks_per_order = 0
            print(f"Zlecenie {order_id} nie ma przypisanych zadań.")
        
        for task_id in range(1, num_tasks_per_order + 1):
            machine = random.choice(machines)
            machine_type = machine_types[machine]
            
            # Wybór pracownika, który będzie dostępny najwcześniej
            available_worker = min(worker_end_time, key=worker_end_time.get)
            worker_name = employee_names[available_worker]
            
            # Ustalenie czasu rozpoczęcia na podstawie dostępności pracownika
            start_date = max(order_start + timedelta(days=random.randint(0, 5)), worker_end_time[available_worker])
            end_date = start_date + timedelta(days=random.randint(1, 3))  # Czas trwania zadania
            
            # Aktualizacja końcowego czasu pracy pracownika
            worker_end_time[available_worker] = end_date
            
            task = {
                'Order': order_id,
                'Task': f"Zadanie_{task_id}",
                'Machine': machine,
                'Machine_Type': machine_type,
                'Worker': worker_name,
                'Start': start_date,
                'Finish': end_date
            }
            tasks.append(task)
    
    df_tasks = pd.DataFrame(tasks)
    return df_tasks
'''
################################-START-################################
# Ładowanie ustawiń aplikacji
initialize =  ias()
# Inicjalizacja danych dla harmonogramowania

# Przygotowanie danych do harmonogramowania
orders = MainApp()
pg.ShowGant(orders)