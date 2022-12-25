import socket
import pickle
import server
from threading import Thread

HOST = "localhost"
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

class Listen(Thread):

        def __init__(self, conn, addr):
            Thread.__init__(self)
            self.conn = conn
            self.addr = addr

        def run(self):
            messagelist = []
            data = self.conn.recv(4096)
            if not data: return
            data_arr=""
            data_arr = pickle.loads(data)
            messagelist = data_arr.split(",")
            arg = messagelist[0]
            method = messagelist[1]

            if method== "square":
                result = (server.square(int(arg)))
            elif method== "cube":
                result = (server.cube(int(arg)))

            print(f'method called: {method}, argument: {arg}, result: {result}')
            result_bytes = pickle.dumps(result)
            self.conn.send(result_bytes)
            print("connection closing... bye!")
            self.conn.close()

class SocketManager(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            while True:
                conn, addr = s.accept()
                print ('Connected by', addr)
                l = Listen(conn, addr)
                l.start()

socket_manager = SocketManager()
socket_manager.start()