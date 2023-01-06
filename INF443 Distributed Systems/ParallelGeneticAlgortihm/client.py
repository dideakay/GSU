import client_stub as stub
import numpy as np
from threading import Thread
from queue import Queue
import time

FAST = "fast"
SLOW = "slow"

N = 10

eyes = [2.25,3.75,5,5,4] 
nose = [3,3,6]
mouth = [2.5,3,3.5, 1.15,1,1.15,8]

target_gene = np.array(eyes + nose + mouth)

class agent():
    def __init__(self, idx, genome = [], m = 15):
        self.id = idx
        self.m = m
        self.genome = self.create_gene(genome)
        
    def create_gene(self, genome: np.array):
        if(len(genome)==0):
            return np.random.rand(self.m) * 10
        result = genome
        for i in range(15):
            result[i] = float(genome[i])
        return result
    
    def set_gene(self, new_gene):
        self.genome = new_gene
    
    def fitness(self):
        error = (target_gene - self.genome)
        return 1 / (1 + np.dot(error, error))


class SendReceiveGenomes(Thread):
    def __init__(self, genomes, queue, server):
            Thread.__init__(self)
            self.genomes = genomes
            self.queue = queue
            self.server = server
    
    def run(self):
        result= stub.remote_call(self.genomes, "evolve", self.server)
        self.queue.put(result)
        print(f'{self.server} put to queue')
        return


if __name__ == '__main__':
    population = {i:agent(i) for i in range(N)}
    fast_queue = Queue()
    slow_queue = Queue()

    genomes = []
    for i in population:
        genomes.append(population[i].genome)

    start_time = time.time() 
    for i in range (10):
        fast = SendReceiveGenomes(genomes, fast_queue, FAST)
        slow = SendReceiveGenomes(genomes, slow_queue, SLOW)
        fast.start()
        slow.start()
        result_fast = []
        result_slow = []
        while True:
            if (not fast_queue.empty()): 
                result_fast = fast_queue.get()
                break
        while True:
            if (not slow_queue.empty()): 
                result_slow = slow_queue.get()
                break
        fast.join()
        slow.join()
        result = result_fast + result_slow

        new_population = {}
        for i in range(N*2):
            new_population[i] = agent(i, result[i])
        
        new_population = sorted(new_population.values(), key=lambda x: x.fitness(), reverse=True)

        population = new_population[:10]

        genomes = [agent.genome for agent in population]

        for i in range(10):
            population[i].set_gene(result[i])
    end_time = time.time() 
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print("Elapsed time:", elapsed_time)  # Print elapsed time

