import numpy as np
import socket
import pickle
import evolve_slow_server as server
from threading import Thread

HOST = '192.168.54.64'
PORT = 50008

class Listen(Thread):

        def __init__(self, conn, addr):
            Thread.__init__(self)
            self.conn = conn
            self.addr = addr

        def run(self):
            messagelist = []
            data = self.conn.recv(4096)
            if not data:
                return
            data_arr=""
            data_arr = pickle.loads(data)
            messagelist = data_arr.split("*")
            arg = messagelist[0]
            method = messagelist[1]
            result=""
            if method=="evolve":
                result = (server.evolve(arg))
            #print(f'method called: {method}, argument: {arg}, result: {result}')
            #print(f'method called: {method}')
            result_bytes = pickle.dumps(result)
            self.conn.send(result_bytes)
            #print("connection closing... bye!")
            self.conn.close()


class SocketManager(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            while True:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((HOST, PORT))
                s.listen(1)
                conn, addr = s.accept()
                #print ('Connected by', addr)
                l = Listen(conn, addr)
                l.start()
                l.join()

socket_manager = SocketManager()
socket_manager.start()