import datetime as d
import re
import select
import socket
import sys
import threading
import time

address = ('0.0.0.0', 45974)

sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create TCP socket
sSock.bind(address)
sSock.listen(1)
sockList = [sSock] # set socket list

count = 0
clientCount = 0

def status():
    global clientCount
    while True:
        time.sleep(60)
        print('Number of connected clients =', clientCount)

threading._start_new_thread(status, ())

while True:
    inputReady, writeReady, exceptReady = select.select(sockList, [], [])
    for ir in inputReady: # process read list
        if ir == sys.stdin: # monitor stdin
            junk = sys.stdin.readline()
            print(junk, flush = True)
        elif ir == sSock: # process if client connected server
            cSock, address = sSock.accept()
            clientCount += 1
            print(address, 'is connected. Number of connected clients is ', clientCount, flush = True)
            cSock.send(address[0].encode())
            sockList.append(cSock)
        else: # process if server received data from client
            data = ir.recv(1024)
            if data:
                sentence = data.decode()
                result = re.match('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', sentence)
                if sentence == "2":
                    print('Connection requested from', address)
                    print("Command 2")
                    cSock.send(str(address).encode())                               # send Addr to client
                    count = count + 1

                elif sentence == "3":

                    print('Connection requested from', address)
                    print("Command 3")

                    modifiedMessage = d.datetime.today().strftime('%Y-%m-%d %H:%M:%S')      # save date in the variable
                    cSock.send(str(modifiedMessage).encode())                    # send modifiedMessage to client
                    count = count + 1

                elif sentence == "4":

                    print('Connection requested from', address)                                # print the number of connection request
                    print("Command 4")

                    cSock.send(str(count).encode())
                    count = count + 1

                elif result != None:
                    print('Sentence is IPv4')

                else:

                    print('Connection requested from', address)
                    print("Command 1")
                    modifiedMessage = sentence.upper()                                      # change lower string ot upper string
                    cSock.send(str(modifiedMessage).encode())                    # send modifiedMessage to client

                    count = count + 1
            else: # process if client closed socket
                print(ir.getpeername(), 'close', flush = True)
                ir.close()
                sockList.remove(ir) # remove from list
sSock.close()
