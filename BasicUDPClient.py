# Choi, Jeong Min 20165974

from socket import *
import time


serverName = 'nsl2.cau.ac.kr'
serverPort = 7722

clientSocket = socket(AF_INET, SOCK_DGRAM)  # create ClientSocket


print('''<MENU>
1) convert text to UPPER-case
2) get my IP address and port number
3) get server time
4) get server service count
5) exit''')

option = input('Input option : ') # input option number

while True:
    if int(option) == 1:

        message = input('Input lowercase sentence: ')

        start=time.perf_counter_ns() # Check start time in nanoseconds

        clientSocket.sendto(message.encode(), (serverName, serverPort))  # Encode message and send it to the server name and server port
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)     # Assign modified data and server address from server to each variable

        end = time.perf_counter_ns() ## Check end time in nanoseconds


        print('Reply from server:', modifiedMessage.decode()) # print modified data
        print('Response time:', (end-start)/1000000,"ms")     # print Response time in milliseconds

        break

    elif int(option) == 2:

        message="2"

        start = time.perf_counter_ns() # Check start time in nanoseconds


        clientSocket.sendto(message.encode(), (serverName, serverPort)) # Encode message and send it to the server name and server port
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)    # Assign modified data and server address from server to each variable

        end = time.perf_counter_ns() # Check end time in nanoseconds


        message=modifiedMessage.decode()

        list=message.split(",")
        list1=list[0]
        list2=list[1]

        print('Reply from server: IP =', list1[1:], ", port =", list2[:-1]) # print server IP
        print('Response time:', (end - start) / 1000000, "ms")# print Response time in milliseconds

        break

    elif int(option) == 3:

        message = "3"

        start = time.perf_counter_ns() # Check start time in nanoseconds


        clientSocket.sendto(message.encode(), (serverName, serverPort))  # Encode message and send it to the server name and server port
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)     # Assign modified data and server address from server to each variable

        end = time.perf_counter_ns() # Check end time in nanoseconds

        message = modifiedMessage.decode()

        print('Reply from server: time = ', message)
        print('Response time:', (end - start) / 1000000, "ms")# print Response time in milliseconds

        break

    elif int(option) == 4:

        message = "4"

        start = time.perf_counter_ns()

        clientSocket.sendto(message.encode(), (serverName, serverPort))  # Encode message and send it to the server name and server port
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)     # Assign modified data and server address from server to each variable

        end = time.perf_counter_ns()

        message = modifiedMessage.decode()

        print("서버에서 응답 : 클라이언트 요청 개수 = ",message) # print the Number of client requests
        print('Response time:', (end - start) / 1000000, "ms")# print Response time in milliseconds

        break

    elif int(option) == 5:

        print("Bye bye~")

        exit() # exit the program

        break

    else:

        option = input('Input option : ')



clientSocket.close()
