# Choi, Jeong Min 20165974

from socket import *
import time
import datetime as d

serverPort = 7722
serverSocket = socket(AF_INET, SOCK_DGRAM) # create SeverSocket
serverSocket.bind(('', serverPort)) # bind serverPort to socket

print("The server is ready to receive on port", serverPort)

count = 0 # for command 4 the number of connection request

while True:

    message, clientAddress = serverSocket.recvfrom(2048) # Assign data and client address from client to each variable
    if message.decode() == "2":
        serverSocket.sendto(str(clientAddress).encode(), clientAddress) # send clientAddress to client
        print('Connection requested from', clientAddress)
        print("Command 2")

        count = count + 1

    elif message.decode() == "3":

        print('Connection requested from', clientAddress)
        print("Command 3")

        modifiedMessage = d.datetime.today().strftime('%Y-%m-%d %H:%M:%S')  # save date in the variable

        serverSocket.sendto(str(modifiedMessage).encode(), clientAddress) # send modifiedMessage to client

        count = count + 1

    elif message.decode() == "4":

        print('Connection requested from', clientAddress) # print the number of connection request
        print("Command 4")

        serverSocket.sendto(str(count).encode(), clientAddress) # send count to clientAddress

        count = count + 1
    else:
        print('Connection requested from', clientAddress)
        print("Command 1")

        modifiedMessage = message.decode().upper() # change lower string ot upper string
        serverSocket.sendto(str(modifiedMessage).encode(), clientAddress) # send modifiedMessage to clientAddress

        count=count+1



