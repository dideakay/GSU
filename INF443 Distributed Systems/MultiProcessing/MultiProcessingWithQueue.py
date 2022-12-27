from threading import Thread
from queue import Empty
import random
import sys
from random import choices
from multiprocessing import Process, Queue, Value


class App:
    
    def __init__(self):
        queue = Queue()
        collecter_list = []
        analyser_list = []
        self.sense_counter = Value('i', 0)
        self.no_sense_counter = Value('i', 0)

        for i in range (10):
            c1 = App.Collecter(queue)
            collecter_list.append(c1)
            
        for i in range (3):
            a = App.Analyser(queue, self)
            analyser_list.append(a)

        for i in range (10):
            collecter_list[i].start()
        for i in range (3):
            analyser_list[i].start()

        for i in range (10):
            collecter_list[i].join()
        for i in range (3):
            analyser_list[i].join()
        
        print(self.sense_counter.value)
        print(self.no_sense_counter.value)

    class Collecter(Thread):
        
        def __init__(self, queue):
            Thread.__init__(self)
            self.queue = queue

        def run(self):
            item = (random.choices([0,1],[0.15,0.85]))[0]
            id = random.randint(0,256)
            comment=''
            
            if(item == 1):
                comment='make sense'
            elif(item == 0):
                comment='non sense'

            collecter_tuple = (comment, id)
            self.queue.put(collecter_tuple)
            print(f' tweet collected by {self.name}')
            

    class Analyser(Process):

        def __init__(self, queue, parent):
            Process.__init__(self)
            self.queue = queue
            self.sense_counter=0
            self.no_sense_counter=0
            self.parent = parent

        def run(self):
            while (not self.queue.empty()):
                try:
                    collecter_tuple = self.queue.get(timeout=1)
                    print(f'-Analyser : tweet id {collecter_tuple[1]}')
                    print(f' analysed by {self.name}')
                    print(f' tweet sense: {collecter_tuple[0]}')
                    
                    if(collecter_tuple[0] == 'make sense'):
                        self.parent.sense_counter.value=(self.parent.sense_counter.value+1)
                    elif(collecter_tuple[0] == 'non sense'):
                        self.parent.no_sense_counter.value=(self.parent.no_sense_counter.value+1)
                except Empty:
                    break

            
if __name__ == '__main__':
    a = App()
    print(f'sense_counter: {(a.sense_counter.value)}')
    print(f'non sense_counter: {(a.no_sense_counter.value)}')  
    sys.exit("sayım bitti")
        
