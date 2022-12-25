import socket, pickle

HOST = '192.168.1.109' #insert ip
FAST_PORT = 50007
SLOW_PORT = 50008
FAST_SERVER = 'fast'
SLOW_SERVER = 'slow'


s_dict = {}
s_dict[FAST_SERVER] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_dict[SLOW_SERVER] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start_socket(server):
    if server == "fast":
        s_dict[FAST_SERVER].connect((HOST, FAST_PORT))
    if server== "slow":
        s_dict[SLOW_SERVER].connect((HOST, SLOW_PORT))

def stop_socket(server):
    if server == "fast":
        s_dict[FAST_SERVER].close()
    if server== "slow":
        s_dict[SLOW_SERVER].close()

def remote_call(arg, method, server):
    
    
    message = str(str(arg) + "," + method)
    data_string = pickle.dumps(message)
    s_dict[FAST_SERVER].send(data_string)

    data = s_dict[FAST_SERVER].recv(4096)
    result = pickle.loads(data)

    
    return result
