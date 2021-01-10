# Choi,Jeongmin 20165974

# client_skel.py
import socket
import time
import sys
import getopt
from threading import Thread

IP = "127.0.0.1"  # defualt ip
PORT = 35974   # default port

time_out = 1000  # default time out : 1000ms

message = "Ping"

ping_queue = {}  # dict for ping rtt

send = 0
recv = 0
lost = 0

min = 999999
max = 0
tot = 0

def help():
    print("-w ip\n-p port\n-w tmout(ms)")
    sys.exit(0)

try:
    opts, args = getopt.getopt(sys.argv[1:], "c:p:w:h")
except getopt.GetoptError as e:
    print(str(e))
    help()

for opt, arg in opts:
    if opt == "-c":
        IP = arg
    elif opt == "-w":
        time_out = float(arg)
    elif opt == "-p":
        PORT = arg
    elif opt == "-h":
        help()
    else:
        help()


def report():
    global sock

    print('')
    print('> FINISHED!')
    print('Number of ping sent     : %d' % send)
    print('Number of ping received : %d' % recv)
    print('Number of ping lost     : %d (loss ratio : %d%%)' % (lost, lost*10))
    print("------------------------------")
    if recv == 0:
        print('Minimum RTT : 0 ms')
        print('Maximum RTT : 0 ms')
        print('Average RTT : 0 ms')
    else:
        print('Minimum RTT : %0.0f ms' % min)
        print('Maximum RTT : %0.0f ms' % max)
        print('Average RTT : %0.3f ms' % (float(tot)/float(recv)))

    sock.close()  #close socket
    sys.exit(0)


def receiver(sock, cnt):
    global ping_queue
    global min
    global max
    global tot
    global recv
    global recv
    global lost

    try:
        data, addr = sock.recvfrom(1024)  # receive data
        recv += 1  # plus recv count
        end = time.time()
        duration = (end - ping_queue[data.decode('utf-8')]) * 1000  # calc duration
        print('%s reply received from %s : RTT = %0.0f ms' % (data.decode('utf-8'), IP, duration))

        if duration < min:
            min = duration
        if duration > max:
            max = duration

        tot += duration  # add duration to total duration var
    except socket.timeout as e:
        sock.close()
        print('Ping %d timeout!' % cnt)  # print time out message
        lost += 1  # plus lost count


try:
    while send < 10:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create udp socket
        IP = socket.gethostbyname(IP)  # get host ip

        sock.settimeout(time_out / 1000)  # set time out

        sndMsg = message + " " + str(send)
        sock.sendto(sndMsg.encode('utf-8'), (IP, int(PORT)))  # send ping to server
        print("%s sent" % sndMsg)
        ping_queue[sndMsg] = time.time()  # Set start time for this ping
        rcvThread = Thread(target=receiver, args=(sock, send))  # create thread to wait response
        rcvThread.daemon = False
        rcvThread.start()  # recvThread start
        send += 1  # plus send count
        time.sleep(0.5)  # sleep
except KeyboardInterrupt:
   while True:
        if recv + lost == send:
            break
   sock.close()
   print("Bye bye~")
   exit(0)

while True:
    if recv + lost is 10:
        break

report()