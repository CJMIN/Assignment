# Choi, Jeong Min 20165974

from socket import *
import time
import datetime as d
import signal
import sys
import threading

#count = 0  # for command 4 the number of connection request

clientCount = 0  # Number of clients

dic = {}

idx = 0


def signal_handler(sig, frame):                     # For Ctrl + C
    print('Bye bye ~')
    sys.exit(0)


def one_minute():
    threading.Timer(60.0, one_minute).start()
    print("The number of clients : ", clientCount)  # For 1 minute alarm


one_minute()


def threaded(connectionSocket):                     # thread function
    global clientCount
    count=0
    connectionSocket.send(str(addr).encode())       # send address to client
    while True:
        address = connectionSocket.recv(1024).decode() # receive address to use the address value of the client to apply to the following codes
        sentence = connectionSocket.recv(1024).decode()
        if sentence == "2":
            print('Connection requested from', address)
            print("Command 2")
            connectionSocket.send(str(address).encode())  # send address to client
            count = count + 1

        elif sentence == "3":

            print('Connection requested from', address)
            print("Command 3")

            modifiedMessage = d.datetime.today().strftime('%Y-%m-%d %H:%M:%S')  # save date in the variable
            connectionSocket.send(str(modifiedMessage).encode())  # send modifiedMessage to client
            count = count + 1

        elif sentence == "4":

            print('Connection requested from', address)  # print the number of connection request
            print("Command 4")
            count = count + 1
            connectionSocket.send(str(count).encode())


        elif sentence == "5":
            clientCount -= 1
            print('Client ', dic[address], 'is disconnected. Number of connected clients =', clientCount)
            del dic[address]
            break

        elif sentence.islower():

            print('Connection requested from', address)
            print("Command 1")
            modifiedMessage = sentence.upper()  # change lower string ot upper string
            connectionSocket.send(str(modifiedMessage).encode())  # send modifiedMessage to client

            count = count + 1
        elif sentence == "CtrlC":
            clientCount -= 1
            print('Client ', dic[address], 'is disconnected. Number of connected clients =', clientCount)
            del dic[address]
            break

    connectionSocket.close()


signal.signal(signal.SIGINT, signal_handler)

serverPort = 45974

serverSocket = socket(AF_INET, SOCK_STREAM)  # create SeverSocket
# serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

serverSocket.bind(('', serverPort))
serverSocket.listen(5)  # listen TCP connection request

print("The server is ready to receive on port", serverPort)

while True:
    (connectionSocket, addr) = serverSocket.accept()  # Assign connectionSocket and addr from client to each variable
    clientCount += 1
    idx += 1         # The unique number assigned to the client
    addr=str(addr)   # Code to prevent key error
    dic[addr] = idx  # The key of dictionary is the address of the client and the value of dictionary  is a unique number

    print('Client ', dic[addr], 'is connected. Number of connected clients =', clientCount)
    threading._start_new_thread(threaded, (connectionSocket,)) # Code for threads
