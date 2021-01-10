# Choi,Jeongmin 20165974

# server_skel.py
import socket
import time
import random
import sys
from threading import Thread
from datetime import datetime

server_ip = "0.0.0.0"  # server ip
server_port = 35974  # server port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create udp socket
sock.bind((server_ip, server_port))  # bind socket


def simulator(data, addr):
    try:
        random.seed(datetime.now())  # random(time seed)
        if random.randint(1, 5) == 1:  # drop 20% packet
            print("Server: drop \"" + data.decode('utf-8') + "\"")
            return
        sec = random.uniform(0.0, 2.0)  # 1~2 secs sleep
        time.sleep(sec)  # sleep
        sock.sendto(data, addr)
        print("Server: reply \"%s\" (%0.0f ms)" % (data.decode('utf-8'), sec*1000))
    except KeyboardInterrupt:
        print("Bye bye~")
        sock.close()
        sys.exit(0)

try:
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # receive data
            print("Server: recv \"" + data.decode('utf-8') + "\"")
            ping = Thread(target=simulator, args=(data, addr))  # create thread to simulate latency
            ping.daemon = False
            ping.start()  # Ping thread start
        except Exception as e:
            pass
except KeyboardInterrupt:
    print("Bye bye~")
    sock.close()
    sys.exit(0)

