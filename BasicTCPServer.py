# Choi, Jeong Min 20165974

from socket import *
import time
import datetime as d

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM) # create SeverSocket
#serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1) # listen TCP connection request

print("The server is ready to receive on port", serverPort)

count = 0 # for command 4 the number of connection request

while True:
    (connectionSocket, addr) = serverSocket.accept() # Assign connectionSocket and addr from client to each variable
    sentence = connectionSocket.recv(1024).decode() # store string in sentence

    if sentence == "2":
        print('Connection requested from', addr)
        print("Command 2")
        connectionSocket.send(str(addr).encode())# send Addr to client
        count = count + 1

    elif sentence == "3":

        print('Connection requested from', addr)
        print("Command 3")

        modifiedMessage = d.datetime.today().strftime('%Y-%m-%d %H:%M:%S') # save date in the variable
        connectionSocket.send(str(modifiedMessage).encode()) # send modifiedMessage to client
        count = count + 1

    elif sentence == "4":

        print('Connection requested from', addr) # print the number of connection request
        print("Command 4")

        connectionSocket.send(str(count).encode())
        count = count + 1

    else:

        print('Connection requested from', addr)
        print("Command 1")
        modifiedMessage = sentence.upper()        # change lower string ot upper string
        connectionSocket.send(str(modifiedMessage).encode())# send modifiedMessage to client

        count = count + 1
    connectionSocket.close()

