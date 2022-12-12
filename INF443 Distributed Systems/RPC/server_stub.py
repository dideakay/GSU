import socket
import pickle
import serverProcess

HOST = '192.168.1.109'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)

while 1:
    messagelist = []
    data = conn.recv(4096)
    if not data: break
    data_arr=""
    data_arr = pickle.loads(data)
    messagelist = data_arr.split(",")
    arg = messagelist[0]
    method = messagelist[1]
    if method== "square":
        result = (serverProcess.square(int(arg)))
    elif method== "cube":
         result = (serverProcess.cube(int(arg)))
    else: break
    print(f'method called: {method}, argument: {arg}, result: {result}')
    result_bytes = pickle.dumps(result)
    conn.send(result_bytes)
print("connection closing... bye!")
conn.close()