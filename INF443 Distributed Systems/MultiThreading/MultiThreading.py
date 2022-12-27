from threading import Thread
from queue import Queue
import time
import random
import sys
from random import choices


class App:
    sense_counter = 0
    no_sense_counter = 0

    def __init__(self):
        queue = Queue()
        collecter_list = []
        analyser_list = []

        for i in range (5):
            c1 = App.Collecter(queue)
            collecter_list.append(c1)
            c2 = App.Collecter(queue)
            collecter_list.append(c2)
            a = App.Analyser(queue)
            analyser_list.append(a)

        for i in range (10):
            collecter_list[i].start()
        for i in range (5):
            analyser_list[i].start()

        for i in range (10):
            collecter_list[i].join()
        for i in range (5):
            analyser_list[i].join()

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
            time.sleep(1)

    class Analyser(Thread):

        def __init__(self, queue):
            Thread.__init__(self)
            self.queue = queue

        def run(self):
            while (not self.queue.empty()):
                collecter_tuple = self.queue.get()
                print(f'-Analyser : tweet id {collecter_tuple[1]}')
                print(f' analysed by {self.name}')
                print(f' tweet sense: {collecter_tuple[0]}')
                time.sleep(2)
                if(collecter_tuple[0] == 'make sense'):
                    App.sense_counter+=1
                elif(collecter_tuple[0] == 'non sense'):
                    App.no_sense_counter+=1
                self.queue.task_done()
            
if __name__ == '__main__':
    
    a = App()
    print(f'sense_counter: {(App.sense_counter)}')
    print(f'non sense_counter: {(App.no_sense_counter)}')  
    sys.exit("sayım bitti")
        
