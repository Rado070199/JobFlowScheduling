import pandas as pd
import numpy as np
import time
import copy

class GeneticAlgorithms():
    '''
    ==============================================================
    Rozwiązywanie problemu opóźnienia całkowitego ważonego w systemie jednego stanowiska. 
    Funkcja celu polega na minimalizacji całkowitego ważonego opóźnienia.
    ==============================================================
    '''
    def AlgorithmForSingleMachineScheduling(populationSize, crossoverCoefficient, mutationRate, selectionToMutationRatio, numberOfIterations):
        ''' ================= ustawienia inicjalizacyjne ======================'''
        # Wczytanie danych z pliku Excel
        file_path = 'algorithmForOnePosition.xlsx'  # Ścieżka do pliku Excel
        df = pd.read_excel(file_path)

        '''
        Czas trwania zadań (p)
        Jednostka: Czas trwania zadań (np. godziny, minuty, dni, sekundy).
        Znaczenie: Czas potrzebny na wykonanie każdego zadania. W praktyce może to być np. liczba godzin, dni roboczych lub minut potrzebnych do ukończenia zadania.
        '''
        #p = [10, 10, 13, 4, 9, 4, 8, 15, 7, 1, 9, 3, 15, 9, 11, 6, 5, 14, 18, 3]
        p = df['Czas trwania'].tolist()
        '''
        Terminy (d)
        Jednostka: Termin do którego zadanie musi być ukończone (np. godziny, dni, jednostki czasu).
        Znaczenie: Maksymalny czas (od początku planowania) do którego każde zadanie musi być zakończone, aby uniknąć opóźnienia. W praktyce może to być liczba godzin od startu projektu lub dni roboczych do zakończenia zadania.
        '''
        #d = [50, 38, 49, 12, 20, 105, 73, 45, 6, 64, 15, 6, 92, 43, 78, 21, 15, 50, 150, 99]
        d = df['Termin'].tolist()
        '''
        Wagi (w)
        Jednostka: Waga opóźnienia (bez jednostki lub jednostki względne).
        Znaczenie: Określa, jak ważne jest opóźnienie dla danego zadania. Wyższe wagi oznaczają, że opóźnienie dla danego zadania jest bardziej kosztowne lub bardziej niepożądane. W praktyce może to być liczba punktów ważności lub skala oceny opóźnienia.
        '''
        #w = [10, 5, 1, 5, 10, 1, 5, 10, 5, 1, 5, 10, 10, 5, 1, 10, 5, 5, 1, 5]
        w = df['Waga'].tolist()

        num_job = len(p)  # liczba zadań

        # wprowadzenie danych
        '''
        Opis: Rozmiar populacji w algorytmie genetycznym odnosi się do liczby "osobników" (rozwiązań), które są brane pod uwagę w każdej iteracji algorytmu.
        Przykład: Jeśli rozmiar populacji wynosi 30, oznacza to, że algorytm będzie pracował z 30 różnymi rozwiązaniami w jednej iteracji.
        W kontekście problemu: Liczba różnych możliwych sekwencji zadań, które są oceniane i krzyżowane. Każdy osobnik reprezentuje jedną możliwą sekwencję realizacji zadań.
        '''
        population_size = int(populationSize or 30)  # domyślna wartość to 30
        
        '''
        Opis: Współczynnik krzyżowania określa, jak często nastąpi wymiana genów (elementów sekwencji) pomiędzy dwoma "rodzicami" (rozwiązaniami), aby stworzyć nowe "dzieci" (rozwiązania).
        Przykład: Jeśli współczynnik krzyżowania wynosi 0.8, oznacza to, że 80% osobników będzie podlegać krzyżowaniu, co generuje nowe rozwiązania.
        W kontekście problemu: Pomaga w tworzeniu nowych sekwencji zadań na podstawie istniejących rozwiązań. Nie chodzi tu o fizyczne krzyżowanie ludzi, ale o wymianę informacji między rozwiązaniami.
        '''
        crossover_rate = float(crossoverCoefficient or 0.8)  # domyślna wartość to 0.8
        
        '''
        Opis: Współczynnik mutacji określa, jak często nastąpi losowa zmiana w rozwiązaniu.
        Przykład: Jeśli współczynnik mutacji wynosi 0.1, oznacza to, że 10% genów w każdym osobniku może zostać zmienionych.
        W kontekście problemu: Pomaga w unikaniu lokalnych ekstremów i wprowadza różnorodność w populacji rozwiązań poprzez losowe zmiany w sekwencjach zadań.
        '''
        mutation_rate = float(mutationRate or 0.1)  # domyślna wartość to 0.1
        
        '''
        Opis: Współczynnik wyboru do mutacji określa procent elementów (zadań) w osobnikach, które zostaną wybrane do mutacji.
        Przykład: Jeśli współczynnik wynosi 0.5, oznacza to, że 50% zadań w każdym osobniku będzie podlegać mutacji.
        W kontekście problemu: Wskazuje, ile zadań w sekwencji ma zostać zmienionych w wyniku mutacji.
        '''
        mutation_selection_rate = float(selectionToMutationRatio or 0.5)
        
        '''
        Opis: Liczba zadań, które zostaną poddane mutacji. Jest to obliczane na podstawie liczby zadań (num_job) i współczynnika wyboru do mutacji.
        Przykład: Jeśli liczba zadań wynosi 20, a współczynnik wyboru do mutacji to 0.5, wtedy num_mutation_jobs wynosi 10 (20 * 0.5).
        W kontekście problemu: Określa, ile zadań będzie zmienionych w wyniku mutacji w każdej iteracji.
        '''
        num_mutation_jobs = round(num_job * mutation_selection_rate)
        
        '''
        Opis: Liczba iteracji określa, ile razy algorytm genetyczny będzie wykonywał swoje operacje (krzyżowanie, mutacja i selekcja) w celu optymalizacji rozwiązania.
        Przykład: Jeśli liczba iteracji wynosi 2000, algorytm przeprowadzi 2000 cykli przetwarzania, aby znaleźć najlepsze rozwiązanie.
        W kontekście problemu: Pomaga w ustaleniu, jak długo algorytm ma pracować nad znalezieniem optymalnego rozwiązania.
        '''
        num_iteration = int(numberOfIterations or 2000)  # domyślna wartość to 2000

        start_time = time.time()

        '''==================== główny kod ==============================='''
        '''----- generowanie początkowej populacji -----'''
        Tbest = 999999999999999
        best_list, best_obj = [], []
        population_list = []
        for i in range(population_size):
            random_num = list(np.random.permutation(num_job))  # generowanie losowej permutacji od 0 do num_job-1
            population_list.append(random_num)  # dodanie do listy populacji
                
        for n in range(num_iteration):
            Tbest_now = 99999999999           
            '''-------- krzyżowanie --------'''
            parent_list = copy.deepcopy(population_list)
            offspring_list = copy.deepcopy(population_list)
            S = list(np.random.permutation(population_size))  # generowanie losowej sekwencji do wyboru chromosomów rodziców do krzyżowania
            
            for m in range(int(population_size / 2)):
                crossover_prob = np.random.rand()
                if crossover_rate >= crossover_prob:
                    parent_1 = population_list[S[2 * m]][:]
                    parent_2 = population_list[S[2 * m + 1]][:]
                    child_1 = ['na' for i in range(num_job)]
                    child_2 = ['na' for i in range(num_job)]
                    fix_num = round(num_job / 2)
                    g_fix = list(np.random.choice(num_job, fix_num, replace=False))
                    
                    for g in range(fix_num):
                        child_1[g_fix[g]] = parent_2[g_fix[g]]
                        child_2[g_fix[g]] = parent_1[g_fix[g]]
                    c1 = [parent_1[i] for i in range(num_job) if parent_1[i] not in child_1]
                    c2 = [parent_2[i] for i in range(num_job) if parent_2[i] not in child_2]
                    
                    for i in range(num_job - fix_num):
                        child_1[child_1.index('na')] = c1[i]
                        child_2[child_2.index('na')] = c2[i]
                    offspring_list[S[2 * m]] = child_1[:]
                    offspring_list[S[2 * m + 1]] = child_2[:]
                
            '''--------mutacja--------'''   
            for m in range(len(offspring_list)):
                mutation_prob = np.random.rand()
                if mutation_rate >= mutation_prob:
                    m_chg = list(np.random.choice(num_job, num_mutation_jobs, replace=False))  # wybór pozycji do mutacji
                    t_value_last = offspring_list[m][m_chg[0]]  # zapisanie wartości na pierwszej pozycji do mutacji
                    for i in range(num_mutation_jobs - 1):
                        offspring_list[m][m_chg[i]] = offspring_list[m][m_chg[i + 1]]  # przesunięcie wartości
                    
                    offspring_list[m][m_chg[num_mutation_jobs - 1]] = t_value_last  # przeniesienie wartości pierwszej pozycji do ostatniej pozycji mutacji
            
            '''--------wartość dopasowania (obliczanie opóźnienia)-------------'''
            total_chromosome = copy.deepcopy(parent_list) + copy.deepcopy(offspring_list)  # kombinacja chromosomów rodziców i potomków
            chrom_fitness, chrom_fit = [], []
            total_fitness = 0
            for i in range(population_size * 2):
                ptime = 0
                tardiness = 0
                for j in range(num_job):
                    ptime = ptime + p[total_chromosome[i][j]]
                    tardiness = tardiness + w[total_chromosome[i][j]] * max(ptime - d[total_chromosome[i][j]], 0)
                chrom_fitness.append(1 / tardiness)
                chrom_fit.append(tardiness)
                total_fitness = total_fitness + chrom_fitness[i]
            
            '''----------selekcja----------'''
            pk, qk = [], []
            
            for i in range(population_size * 2):
                pk.append(chrom_fitness[i] / total_fitness)
            for i in range(population_size * 2):
                cumulative = 0
                for j in range(0, i + 1):
                    cumulative = cumulative + pk[j]
                qk.append(cumulative)
            
            selection_rand = [np.random.rand() for i in range(population_size)]
            
            for i in range(population_size):
                if selection_rand[i] <= qk[0]:
                    population_list[i] = copy.deepcopy(total_chromosome[0])
                else:
                    for j in range(0, population_size * 2 - 1):
                        if selection_rand[i] > qk[j] and selection_rand[i] <= qk[j + 1]:
                            population_list[i] = copy.deepcopy(total_chromosome[j + 1])
                            break
            '''----------porównanie----------'''
            for i in range(population_size * 2):
                if chrom_fit[i] < Tbest_now:
                    Tbest_now = chrom_fit[i]
                    sequence_now = copy.deepcopy(total_chromosome[i])
            
            if Tbest_now <= Tbest:
                Tbest = Tbest_now
                sequence_best = copy.deepcopy(sequence_now)
            
            job_sequence_ptime = 0
            num_tardy = 0
            for k in range(num_job):
                job_sequence_ptime = job_sequence_ptime + p[sequence_best[k]]
                if job_sequence_ptime > d[sequence_best[k]]:
                    num_tardy = num_tardy + 1
                    
        '''----------WYNIKI----------'''

        '''
        Optymalna Sekwencja Zadań (Sequence Best):
        Opis: To sekwencja zadań, która została uznana za najlepszą po wszystkich iteracjach algorytmu. Jest to permutacja zadań, która minimalizuje całkowite ważone opóźnienie.
        Znaczenie: Pokazuje, w jakiej kolejności powinny być wykonywane zadania, aby osiągnąć minimalne opóźnienia zgodnie z funkcją celu algorytmu. Na przykład, jeśli sekwencja to [2, 0, 1, 3], oznacza to, że zadanie 2 powinno być wykonane jako pierwsze, zadanie 0 jako drugie, itd.
        '''
        #print("optymalna sekwencja", sequence_best)
        ###########################################

        '''
        Optymalna Wartość (Tbest):
        Opis: Jest to minimalna wartość całkowitego ważonego opóźnienia uzyskana przez algorytm. To suma wszystkich ważonych opóźnień dla najlepszej sekwencji.
        Znaczenie: Wskazuje na jakość najlepszego rozwiązania. Im niższa wartość, tym lepsze rozwiązanie, ponieważ oznacza mniejsze opóźnienia i mniejsze koszty związane z opóźnieniami.
        '''
        #print("optymalna wartość: %f" % Tbest)
        ##########################################

        '''
        Średnie Opóźnienie (Average Tardiness):
        Opis: Obliczane jako Tbest / num_job, gdzie Tbest to optymalna wartość całkowitego ważonego opóźnienia, a num_job to liczba zadań.
        Znaczenie: Umożliwia oszacowanie przeciętnego opóźnienia na zadanie. Pomaga zrozumieć, jak dobrze udało się zminimalizować opóźnienia w kontekście średniego przypadku.
        '''
        #print("średnie opóźnienie: %f" % (Tbest / num_job))
        ###########################################

        '''
        Liczba Opóźnionych Zadań (Number of Tardy Jobs):
        Opis: Liczba zadań, które zostały zakończone po ich terminie w najlepszej sekwencji.
        Znaczenie: Wskazuje, ile zadań miało opóźnienia w stosunku do ich terminów. Pomaga ocenić, jak wiele zadań zostało wykonanych z opóźnieniem i w jakim stopniu harmonogram był skuteczny w minimalizowaniu opóźnień.
        '''
        #print("liczba opóźnionych: %d" % num_tardy)
        ############################################

        '''
        Czas Wykonania (Execution Time):
        Opis: Czas, jaki algorytm potrzebował na zakończenie wszystkich iteracji i znalezienie rozwiązania.
        Znaczenie: Informuje o efektywności czasowej algorytmu. Pomaga zrozumieć, jak długo trwało znalezienie rozwiązania i czy czas wykonania jest akceptowalny w kontekście wymagań aplikacji.
        '''
        #print('czas wykonania: %s' % (time.time() - start_time))
        #############################################
        return [sequence_best, Tbest, (Tbest / num_job), num_tardy, (time.time() - start_time)]

    '''
    ==============================================================
    Rozwiązanie problemu harmonogramowania przepływu za pomocą algorytmu genetycznego w Pythonie

    Dane wejściowe:
    Masz macierz czasów przetwarzania, gdzie wiersze odpowiadają poszczególnym zadaniom (Job 1, Job 2, ..., Job 9),
    a kolumny odpowiadają maszynom (Machine 1, Machine 2, ..., Machine 5).
    Każda komórka macierzy zawiera czas przetwarzania danego zadania na określonej maszynie.

    Inicjalizacja:

    Odczytanie danych: Algorytm wczytuje dane z pliku Excel, które są odpowiednikiem macierzy przedstawionej powyżej. Wartości te reprezentują czas przetwarzania każdego zadania na każdej maszynie.
    Parametry: Ustalane są wartości początkowe parametrów, takich jak rozmiar populacji, współczynnik krzyżowania, współczynnik mutacji, oraz liczba iteracji.
    Generowanie początkowej populacji:

    Tworzenie losowych sekwencji zadań. Każda sekwencja reprezentuje pewien sposób przypisania zadań do maszyn, np. Job 3 -> Job 1 -> Job 2 -> ... -> Job 9.
    Iteracyjna optymalizacja:

    Krzyżowanie: Dla każdego pokolenia tworzone są nowe sekwencje (potomstwo) poprzez mieszanie sekwencji rodzicielskich. Na przykład, jeśli mamy dwie sekwencje Job 1 -> Job 3 -> Job 2 oraz Job 2 -> Job 3 -> Job 1, algorytm może wygenerować nowe sekwencje Job 1 -> Job 3 -> Job 2 oraz Job 2 -> Job 3 -> Job 1.
    Mutacja: Niektóre sekwencje są modyfikowane poprzez losowe zamiany miejscami zadań, np. Job 1 -> Job 3 -> Job 2 może zostać zmienione na Job 3 -> Job 1 -> Job 2.
    Ocena dopasowania: Każda sekwencja jest oceniana pod kątem czasu wykonania wszystkich zadań na wszystkich maszynach. Algorytm symuluje przetwarzanie wszystkich zadań w danej sekwencji na maszynach i oblicza całkowity czas przetwarzania.
    Selekcja: Najlepsze sekwencje (te, które dają najkrótszy czas przetwarzania) są wybierane do następnej iteracji.
    Porównanie wyników i uaktualnienie najlepszego rozwiązania:

    Algorytm porównuje najlepszą sekwencję znalezioną dotychczas z nowo wygenerowanymi sekwencjami. Jeśli nowa sekwencja jest lepsza (krótszy czas przetwarzania), zostaje ona zapisana jako nowe najlepsze rozwiązanie.
    Wynik końcowy:

    Po zakończeniu iteracji algorytm zwraca najlepszą znalezioną sekwencję zadań oraz odpowiadający jej czas przetwarzania (makespan), co pozwala na zidentyfikowanie optymalnego harmonogramu pracy maszyn dla zadanych danych.
    ==============================================================
    '''
    def AlgorithmGeneticFlowShopScheduler(populationSize, crossoverCoefficient, mutationRate, mutationSelectionCoefficient, numberOfIterations):
        ''' ================= ustawienia inicjalizacji ======================'''
        #pt_tmp = pd.read_excel("20x5_flowshop.xlsx", sheet_name="S1", index_col=[0])
        pt_tmp = pd.read_excel("9x5_flowshop.xlsx", sheet_name="S1", index_col=[0])
        pt = pt_tmp.values.tolist()
        num_m = pt_tmp.shape[1]
        num_job = len(pt)

        #Podaj rozmiar populacji: 
        rozmiar_populacji = int(populationSize or 30)
        #Podaj współczynnik krzyżowania: 
        crossover_rate = float(crossoverCoefficient or 0.8)
        #Podaj współczynnik mutacji:
        mutation_rate = float(mutationRate or 0.2)
        #Podaj współczynnik selekcji mutacji:
        mutation_selection_rate = float(mutationSelectionCoefficient or 0.2)
        num_mutation_jobs = round(num_job * mutation_selection_rate)
        # Podaj liczbę iteracji: 
        num_iteration = int(numberOfIterations or 2000)

        start_time = time.time()

        '''==================== główny kod ==============================='''
        '''----- generowanie początkowej populacji -----'''
        Tbest = 999999999999999
        best_list, best_obj = [], []
        population_list = []
        for i in range(rozmiar_populacji):
            random_num = list(np.random.permutation(num_job)) # generowanie losowej permutacji od 0 do num_job-1
            population_list.append(random_num) # dodawanie do listy populacji

        for n in range(num_iteration):
            Tbest_now = 99999999999
            '''-------- krzyżowanie --------'''
            parent_list = copy.deepcopy(population_list)
            offspring_list = copy.deepcopy(population_list)
            S = list(np.random.permutation(rozmiar_populacji)) # generowanie losowej sekwencji do wyboru rodzica do krzyżowania

            for m in range(int(rozmiar_populacji / 2)):
                crossover_prob = np.random.rand()
                if crossover_rate >= crossover_prob:
                    parent_1 = population_list[S[2 * m]][:]
                    parent_2 = population_list[S[2 * m + 1]][:]
                    child_1 = ['na' for i in range(num_job)]
                    child_2 = ['na' for i in range(num_job)]
                    fix_num = round(num_job / 2)
                    g_fix = list(np.random.choice(num_job, fix_num, replace=False))

                    for g in range(fix_num):
                        child_1[g_fix[g]] = parent_2[g_fix[g]]
                        child_2[g_fix[g]] = parent_1[g_fix[g]]
                    c1 = [parent_1[i] for i in range(num_job) if parent_1[i] not in child_1]
                    c2 = [parent_2[i] for i in range(num_job) if parent_2[i] not in child_2]

                    for i in range(num_job - fix_num):
                        child_1[child_1.index('na')] = c1[i]
                        child_2[child_2.index('na')] = c2[i]
                    offspring_list[S[2 * m]] = child_1[:]
                    offspring_list[S[2 * m + 1]] = child_2[:]

            '''-------- mutacja --------'''
            for m in range(len(offspring_list)):
                mutation_prob = np.random.rand()
                if mutation_rate >= mutation_prob:
                    m_chg = list(np.random.choice(num_job, num_mutation_jobs, replace=False)) # wybór pozycji do mutacji
                    t_value_last = offspring_list[m][m_chg[0]] # zapisanie wartości z pierwszej pozycji mutacji
                    for i in range(num_mutation_jobs - 1):
                        offspring_list[m][m_chg[i]] = offspring_list[m][m_chg[i + 1]] # przesunięcie

                    offspring_list[m][m_chg[num_mutation_jobs - 1]] = t_value_last # przeniesienie wartości z pierwszej pozycji mutacji na ostatnią pozycję mutacji

            '''-------- wartość dopasowania (obliczanie czasu bezczynności) -------------'''

            total_chromosome = copy.deepcopy(parent_list) + copy.deepcopy(offspring_list) # połączenie chromosomów rodziców i potomków
            chrom_fitness, chrom_fit = [], []
            total_fitness = 0
            s, d, D = {}, {}, {}
            v = [0 for c in range(rozmiar_populacji * 2)]

            for c in range(rozmiar_populacji * 2):
                for i in range(num_m):
                    s[c, i] = pt[total_chromosome[c][0]][i]
                    d[c, i] = v[c]
                    D[c, i, total_chromosome[c][0]] = v[c]
                    v[c] = v[c] + pt[total_chromosome[c][0]][i]

                for j in range(num_job):
                    D[c, 0, j] = 0

                for j in range(1, num_job):
                    for i in range(0, num_m - 1):
                        s[c, i] = s[c, i] + pt[total_chromosome[c][j]][i]
                        D[c, i + 1, j] = max(0, s[c, i] + d[c, i] - s[c, i + 1] - d[c, i + 1])
                        d[c, i + 1] = d[c, i + 1] + D[c, i + 1, j]

                    s[c, num_m - 1] = s[c, num_m - 1] + pt[total_chromosome[c][j]][i + 1]

                v[c] = 0
                for i in range(num_m):
                    v[c] = v[c] + d[c, i]

                chrom_fitness.append(1 / v[c])
                chrom_fit.append(v[c])
                total_fitness = total_fitness + chrom_fitness[c]

            '''---------- selekcja ----------'''
            pk, qk = [], []

            for i in range(rozmiar_populacji * 2):
                pk.append(chrom_fitness[i] / total_fitness)
            for i in range(rozmiar_populacji * 2):
                cumulative = 0
                for j in range(0, i + 1):
                    cumulative = cumulative + pk[j]
                qk.append(cumulative)

            selection_rand = [np.random.rand() for i in range(rozmiar_populacji)]

            for i in range(rozmiar_populacji):
                if selection_rand[i] <= qk[0]:
                    population_list[i] = copy.deepcopy(total_chromosome[0])
                else:
                    for j in range(0, rozmiar_populacji * 2 - 1):
                        if selection_rand[i] > qk[j] and selection_rand[i] <= qk[j + 1]:
                            population_list[i] = copy.deepcopy(total_chromosome[j + 1])
                            break

            '''---------- porównanie ----------'''
            for i in range(rozmiar_populacji * 2):
                if chrom_fit[i] < Tbest_now:
                    Tbest_now = chrom_fit[i]
                    sequence_now = copy.deepcopy(total_chromosome[i])

            if Tbest_now <= Tbest:
                Tbest = Tbest_now
                sequence_best = copy.deepcopy(sequence_now)

        '''---------- wynik ----------'''
        #print("optymalna sekwencja", sequence_best)
        #print("optymalna wartość:%f" % Tbest)
        #print('czas trwania:%s' % (time.time() - start_time))
        return [sequence_best, Tbest, (time.time() - start_time)]

 