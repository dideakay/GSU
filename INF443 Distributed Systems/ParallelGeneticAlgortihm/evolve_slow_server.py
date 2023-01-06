import numpy as np

import numpy as np


eyes = [2.25,3.75,5,5,4] 
nose = [3,3,6]
mouth = [2.5,3,3.5, 1.15,1,1.15,8]

target_gene = np.array(eyes + nose + mouth) #15 elements

N = 10

class agent():
    def __init__(self, idx, genome: np.array, m = 15):
        self.id = idx
        self.m = m
        self.genome = self.create_gene(genome)
        self.N = 10
        
    def create_gene(self, genome: np.array):
        result = genome
        for i in range(15):
            result[i] = float(genome[i])
        return result
    
    def set_gene(self, new_gene):
        self.genome = new_gene
    
    def fitness(self):
        error = (target_gene - self.genome)
        return 1 / (1 + np.dot(error, error))
    
class evolution():
    def __init__(self, N, population: list[agent]): 
        self.m = 15
        self.N = N
        self.population: agent = {i: population[i] for i in range(N)}
        self.update_probabilities()

    def update_probabilities(self):
        self.success = {i: self.population[i].fitness() for i in range(self.N)}
        total_success = sum(self.success.values())
        
        self.reproduction_probability = {i: self.success[i]/total_success for i in range(self.N)}

    def selection(self):
        pr = [self.reproduction_probability[i] for i in range(self.N)]
        select = np.random.choice(self.N, 2, replace= False, p=pr)
        return select
    
    def crossover(self, selectedParents):
        parent0 = self.population[selectedParents[0]].genome
        parent1 = self.population[selectedParents[1]].genome

        cut = np.random.randint(self.m)
        child_gene = np.hstack((parent0[:cut],parent1[cut:]))
        return child_gene
    
    def mutation(self, child_gene, p = 0.1):
        mutation_point = np.random.randint(len(child_gene))
        if np.random.rand() < p:
            child_gene[mutation_point] = np.random.rand() * 10
        return child_gene
    
    def create_offspring(self):
        parents = self.selection()
        child_gene = self.crossover(parents)
        child_gene = self.mutation(child_gene)
        return child_gene
    
    def create_new_population(self):
        sorted_by_success = sorted(self.success.items(), key=lambda kv: kv[1])
        self.best_agent = self.population[sorted_by_success[-1][0]]
        
        for i in range(self.N-1):
            child_gene = self.create_offspring()
            agent_id = sorted_by_success[i][0]
            self.population[agent_id].set_gene(child_gene)
        
        self.update_probabilities()
    
    def evolve(self, G = 10):
        for i in range(G):
            self.create_new_population()
        return self.best_agent

def evolve(genome: str):
    temp = genome.replace('array', '').replace('[([', '').replace('])]', '').replace('(', '' ).replace(')', '').replace('],', '').replace('\n','').replace(' ', '').replace(']]', ']').replace('\'', '')
    temp_splitted = temp.split('[')
    genome_list = []
    for i in range(N):
        genome_list.append(temp_splitted[i].split(','))
    
    population = {}
    for i in range(N):
        population[i] = agent(i, genome_list[i])
    world = evolution(10, population)
   
    best = world.evolve(G = 50)
    print(f'best: {best.fitness()}')

    new_population = world.population
    new_genome_list = []

    
    for i in range(N):
        new_genome_list.append(new_population[i].genome)

    return new_genome_list