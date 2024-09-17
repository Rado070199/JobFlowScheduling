from graphviz import Digraph

# Diagram UML dla Klasyczny Algorytm Genetyczny (GA - Genetic Algorithm)
uml = Digraph(comment="Klasyczny Algorytm Genetyczny (GA)", format='png')

# Definiowanie klasy "GeneticAlgorithm"
uml.node('GA', 'GeneticAlgorithm\n- population_size\n- generations\n- mutation_rate\n- crossover_rate\n+ initialize_population()\n+ select_parents()\n+ crossover()\n+ mutate()\n+ evaluate_fitness()\n+ run()')

# Definiowanie innych klas wspierających
uml.node('Chromosome', 'Chromosome\n- genes\n+ fitness()\n+ mutate()\n+ crossover()')
uml.node('Population', 'Population\n- chromosomes\n+ evaluate_fitness()\n+ select_parents()\n+ evolve()')

# Relacje pomiędzy klasami
uml.edge('GA', 'Population', label='manages')
uml.edge('Population', 'Chromosome', label='contains')

# Wyświetlenie diagramu UML
uml.render('/mnt/data/genetic_algorithm_uml', view=False)
'/mnt/data/genetic_algorithm_uml.png'
