import socket, pickle

HOST = '192.168.54.64' #insert ip
FAST_PORT = 50007
SLOW_PORT = 50008

FAST_SERVER = 'fast'
SLOW_SERVER = 'slow'

PORT = {"fast" : FAST_PORT, "slow": SLOW_PORT}



def remote_call(arg, method, server):
    s_dict = {}
    s_dict[FAST_SERVER] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_dict[SLOW_SERVER] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    s_dict[server].connect((HOST, PORT[server]))

    message = str(str(arg) + "*" + method)

    data_string = pickle.dumps(message)
    s_dict[server].send(data_string)

    data = s_dict[server].recv(4096)
    result = pickle.loads(data)

    s_dict[server].close()
    
    return result
