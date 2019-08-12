from socket import *
import socket
import os
import time
import sys
import cv2
import numpy as np
import face_recognition


# 이미지 파일 저장경로
src = "/home/step112/PE/"


def fileName():
    dte = time.localtime()
    Year = dte.tm_year
    Mon = dte.tm_mon
    Day = dte.tm_mday
    WDay = dte.tm_wday
    Hour = dte.tm_hour
    Min = dte.tm_min
    Sec = dte.tm_sec
    imgFileName = src + str(Year) + '_' + str(Mon) + '_' + str(Day) + '_' + str(Hour) + '_' + str(Min) + '_' + str(Sec)
    return imgFileName


# 서버 소켓 오픈
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 8080))
server_socket.listen(5)


print("TCPServer Waiting for client ")


while True:
    n=0
    print("클라이언트 요청 대기중")
    # 클라이언트 요청 대기중 .
    client_socket, address = server_socket.accept()
    # 연결 요청 성공
    print("연결 요청 성공")
    print("I got a connection from ", address)

    data = None

    # Data 수신
    while True:

        # rec_path = "./"
        # rev_flist = os.listdir(rec_path)
        # print("file_list: {}".format(rec_path))

        # rev_flist.remove(".DS_Store")
        # if (file_recive_cnt > 2):
        #     for fname in rev_flist:
        #         os.system("rm " + fname)
        #     file_recive_cnt = 0



        # 데이터 수신 받는 코드

        try:
            img_data = client_socket.recv(1024)
        except OSError :
            print("Bad file descriptor")

        data = img_data

        if img_data:
            while img_data:
                print("recving Img...")
                img_data = client_socket.recv(1024)
                data += img_data
        else:
            print("데이터 수신 기달")
            break



        # 받은 데이터 저장하는 코드

        img_fileName = fileName()
        print(img_fileName)

        img_fileName = img_fileName + ".mp4"


        img_file = open(img_fileName, "wb")

        print("finish img recv")
        print(sys.getsizeof(data))

        img_file.write(data)
        img_file.close()





        ###########################################################################################################


        # 동영상 처리하는 코드

        count = 0

        descs = {}

        temp_descs = {}

        temp_1 = []

        temp_2 = []

        # 파일 경로
        FilePath = img_fileName

        # Open the File
        movie = cv2.VideoCapture(FilePath)  # 동영상 핸들 얻기

        # Check that the file is opened
        if movie.isOpened() == False:  # 동영상 핸들 확인
            print('Can\'t open the File' + (FilePath))
            exit()

        while (True):

            print("현재 인식된 사람 얼굴의 수 : ", count)
            # print(descs)

            print("descs의 길이 : ", len(descs))

            ret, frame = movie.read()

            try:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            except Exception as e:
                break

            rgb_small_frame = small_frame[:, :, ::-1]

            rects = face_recognition.face_locations(rgb_small_frame)

            descriptors = face_recognition.face_encodings(rgb_small_frame, rects)

            print("프레임에서 인식된 얼굴 수 : ", len(descriptors))

            for i, desc in enumerate(descriptors):

                if i == 0:

                    temp_1.append(desc)
                else:
                    num = 0
                    for j in range(len(temp_1)):

                        num = num + 1

                        dist = np.linalg.norm([desc] - temp_1[j], axis=1)  # 거리 계산

                        if dist < 0.6:
                            break
                        elif num == len(temp_1):
                            temp_2.append(desc)

                temp_1 = temp_1 + temp_2

            if len(descs) != 0:

                for i, desc in enumerate(temp_1):  # 배열의 인자와 해당 값에 대한 포문

                    found = False

                    num = 0

                    for name, saved_desc in descs.items():  # 글로벌 변수로 선언 저장되있는 얼굴 특징값
                        num = num + 1

                        dist = np.linalg.norm([desc] - saved_desc, axis=1)  # 거리 계산

                        print("길이가 0이 아닌 경우의 dist : ", dist)

                        if dist < 0.6:  # 거리가 짧으면 트루

                            print("짧음")

                            break
                        elif num == len(descs):
                            temp_descs[count] = desc

                            count = count + 1

                    descs.update(temp_descs)

            else:
                # num=0

                for i in temp_1:

                    if len(descs) == 0:

                        descs[count] = i

                        count = count + 1
                    else:
                        num = 0
                        for j in descs:
                            num = num + 1

                            dist = np.linalg.norm([i] - j, axis=1)

                            if dist < 0.6:

                                break
                            elif num == len(descs):

                                temp_descs[count] = i

                                print(temp_descs[count])

                                count = count + 1
                        descs.update(temp_descs)

        num=len(descs)

        num=str(num)




        ###########################################################################################################


        # 처리된 결과값 보내는 코드


        client_socket.send(str(num).encode())

        print("Finish ")


    client_socket.close()

print("SOCKET closed... END")


