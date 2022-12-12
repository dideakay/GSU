import socket, pickle

HOST = '192.168.1.109' #insert ip
PORT = 50007

def remote_call(arg, method):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    message = str(str(arg) + "," + method)
    data_string = pickle.dumps(message)
    s.send(data_string)

    data = s.recv(4096)
    result = pickle.loads(data)
    print(f'method called: {method}, argument: {arg}, result: {result}')
    s.close()
    return result


