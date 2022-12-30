import client_stub as stub
import numpy as np

FAST = "fast"
SLOW = "slow"

N = 10

eyes = [2.25,3.75,5,5,4] 
nose = [3,3,6]
mouth = [2.5,3,3.5, 1.15,1,1.15,8]

target_gene = np.array(eyes + nose + mouth)

class agent():
    def __init__(self, idx, m = 15):
        self.id = idx
        self.m = m
        self.genome = self.create_gene()
        
    def create_gene(self):
        return np.random.rand(self.m) * 10
    
    def set_gene(self, new_gene):
        self.genome = new_gene
    
    def fitness(self):
        error = (target_gene - self.genome)
        return 1 / (1 + np.dot(error, error))


population = {i:agent(i) for i in range(N)}
genomes = []
for i in population:
    genomes.append(population[i].genome)

result = stub.remote_call(genomes, "evolve", FAST)
print(result)

