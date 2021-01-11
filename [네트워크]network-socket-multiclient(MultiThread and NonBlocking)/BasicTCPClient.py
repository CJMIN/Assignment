# Choi, Jeong Min 20165974

import datetime
from socket import *
import time
import signal
import sys



def signal_handler(sig, frame):
        CtrlC="CtrlC"
        clientSocket.send(CtrlC.encode())
        print('Bye bye ~')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def isNumber(s):
  try:
    int(s)
    return True
  except ValueError:
    return False


serverName = 'nsl2.cau.ac.kr' #'169.254.47.195'
serverPort = 45974

clientSocket = socket(AF_INET, SOCK_STREAM)  # create ClientSocket

clientSocket.connect((serverName, serverPort))  # connect server

address=clientSocket.recv(2048).decode()        # receive address

print('''<MENU>
1) convert text to UPPER-case
2) get my IP address and port number
3) get server time
4) get server service count
5) exit''')



while True:
    clientSocket.send(address.encode()) # send address to client
    option = input('Input option : ')
    while True:
        if isNumber(option):
            break
        else:option = input('Input option : ')

    if int(option) == 1:

        message = input('Input lowercase sentence: ')

        while True:
            if message.islower():
                break
            else: message = input('Input lowercase sentence: ')

        start = time.perf_counter()
        clientSocket.send(message.encode()) # Encode message and send it to the server name and server port

        modifiedMessage = clientSocket.recv(1024)# Assign modified data
        end = time.perf_counter()

        print('Reply from server:', modifiedMessage.decode()) # print modified data
        print('Response time:', (end - start) / 1000000, "ms") # print Response time in milliseconds



    elif int(option) == 2: #

        message="2"

        start = time.perf_counter()

        clientSocket.send(message.encode())         # Encode message and send it to the server name and server port
        modifiedMessage = clientSocket.recv(2048)
        end = time.perf_counter()

        message=modifiedMessage.decode()

        list = message.split(",")
        list1 = list[0]
        list2 = list[1]

        print('Reply from server: IP =', list1[1:], ", port =", list2[:-1])  # print server IP
        print('Response time:', (end - start) / 1000000, "ms")               # print Response time in milliseconds

    elif int(option) == 3:

        message = "3"

        start = time.perf_counter()

        clientSocket.send(message.encode())                 # Encode message and send it to the server name and server port

        modifiedMessage = clientSocket.recv(2048)          # Assign modified data

        end = time.perf_counter()

        message=modifiedMessage.decode()

        print('Reply from server: time = ', message)
        print('Response time:', (end - start) / 1000000, "ms") # print Response time in milliseconds

    elif int(option) == 4:

        message = "4"

        start = time.perf_counter()

        clientSocket.send(message.encode()) # Encode message and send it to the server name and server port

        modifiedMessage = clientSocket.recv(2048) # Assign modified data
        end = time.perf_counter()

        print("서버에서 응답 : 클라이언트 요청 개수 = ", modifiedMessage.decode()) # print the Number of client requests
        print('Response time:', (end - start) / 1000000, "ms")# print Response time in milliseconds

    elif int(option) == 5:

        message = "5"

        clientSocket.send(message.encode())

        print("Bye bye~")

        exit() # exit the program

        break

clientSocket.close()


