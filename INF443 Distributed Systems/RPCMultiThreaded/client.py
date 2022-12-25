import client_stub as stub

FAST = "fast"
SLOW = "slow"

stub.start_socket(FAST)

method = "square"
arg = 3
result = stub.remote_call(arg, method, FAST)

print(f'method called: {method}, argument: {arg}, result: {result}')
