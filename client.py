from socket  import *
from constCS import * #-

comando = input(f"DIGITE UM COMANDO\n")
s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT)) # connect to server (block until accepted)
s.send(str.encode(comando))  # send some data
data = s.recv(1024)     # receive the response
print (bytes.decode(data))            # print the result
s.close()               # close the connection
