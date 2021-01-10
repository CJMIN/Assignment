// Choi,Jeongmin 20165974

#include <stdio.h>

#include <string.h>

#include <unistd.h>

#include <time.h>

#include <stdlib.h>

#include <sys/socket.h>

#include <sys/types.h>

#include <netinet/in.h>

#include <netdb.h>

#include <arpa/inet.h>

#include <sys/time.h>

#include <ctype.h>

#include <signal.h>


 

static char* server_ip = "127.0.0.1"; //Server ip (default 127.0.0.1)

static int server_port = 35974; //Server port (default 35974)


 

static int si_sendCount = 0; //send ping

static int si_recvCount = 0; //recv ping

static int si_lostCount = 0; //time out ping


 

static double sd_tot = 0; //tot rtt

static double sd_min = 999999; //min rtt

static double sd_max = 0; //max rtt


 

static struct timeval st_begin;

static struct timeval st_finish;


 

static int si_timeout = 1000; //defualt timeout


 

void* Byebye() { //ctrl+c

        printf("\n=====================================\n");

        printf("Bye bye~\n");

        exit(0);

}


 

void* ping(void* param);


 

typedef struct {

        int sock;

        int seq;

} Param;


 

void* ping(void*);


 

void help() //usage function

{

        printf("USAGE : \n-c ipaddress\n-p port\n-w time-out(ms)\n");

}


 

int main(int argc, char* argv[]) {

        signal(SIGINT, (void*) Byebye);

        int sockfd;

        int i = 0;

        int opt;

        int continue_flag = 1;

        struct timeval tv;


 

        //Parsing argumnets

        while ((opt = getopt(argc, argv, "c:p:w:h")) != -1) {

               switch (opt) {

               case 'h':

                       continue_flag = 0;

                       break;

               case 'c':

                       server_ip = optarg;

                       continue_flag = 1;

                       break;

               case 'w':

                       si_timeout = atoi(optarg);

                       continue_flag = 1;

                       break;

               case 'p':

                       server_port = atoi(optarg);

                       continue_flag = 1;

                       break;

               case '?':

                       continue_flag = 0;

                       break;

               }

        }

        if (continue_flag != 1) {

               help();

               return 0;

        }


 

        tv.tv_sec = si_timeout / 1000;

        tv.tv_usec = si_timeout % 1000 * 1000; //1000us = 1ms (timeout : ms)


 

        // get host ip

        if (isalpha(server_ip[0]) != 0) {

               struct hostent* he;

               he = gethostbyname(server_ip);

               if (!he) {

                       printf("gethostbyname() error...\n");

                       return 1;

               }

               server_ip = inet_ntoa(*(struct in_addr*) he->h_addr_list[0]);

        }


 

        gettimeofday(&st_begin, NULL); //Get start time


 

        for (i = 0; i < 10; i++) {

               if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) { //udp socket

                       perror("socket() error...\n");

                       return 1;

               }


 

               if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv)) < 0) { //Set TIMEOUT option for this socket

                       printf("setsockopt() error...\n");

                       exit(1);

               }


 

               // copy values for thread argument

               Param param;

               pthread_t pingThread; //ping thread

               param.sock = sockfd;

               param.seq = i;

               pthread_create(&pingThread, NULL, (void*) ping, (void*) &param); //Create threads for each ping

               usleep(500000); //sleep 500ms

        }


 

        while (si_recvCount + si_lostCount != 10)

               ;


 

        //print result

        float total_time;

        gettimeofday(&st_finish, NULL); //Get end time

        total_time = (st_finish.tv_sec * 1000 - st_begin.tv_sec * 1000)

                       + (st_finish.tv_usec / 1000 - st_begin.tv_usec / 1000); //run time

        printf("\n===========================================\n");

        printf("DURATION : %0.1f ms\n", total_time);

        printf("TOTAL    : %d packets\n", si_sendCount);

        printf("RECEIVED : %d packets\n", si_recvCount);

        printf("TIME-OUT : %d packets (%0.0f%% loss)\n", si_lostCount,

                       (float) (si_lostCount) / si_sendCount * 100);

        if (si_recvCount == 0) {

               printf("Minimum RTT : 0 ms\n");

               printf("Maximum RTT : 0 ms\n");

               printf("Average RTT : 0 ms\n");

        } else {

               printf("Minimum RTT : %0.0f ms\n", sd_min);

               printf("Maximum RTT : %0.0f ms\n", sd_max);

               printf("Average RTT : %0.3f ms\n", sd_tot / si_recvCount);

        }

        return 0;

}


 

void* ping(void* param) {

        struct sockaddr_in servAddr;

        char sendBuffer[1024], recvBuffer[1024];

        struct timeval stime, etime;

        int servLen;

        int recvLen;

        float duration = 0;


 

        Param* parm = param;

        int sockfd = parm->sock; // copy sock

        int seq = parm->seq; // copy seq value


 

        struct timeval to;

        to.tv_sec = si_timeout / 1000;

        to.tv_usec = si_timeout % 1000 * 1000; //1000us = 1ms (timeout : ms)


 

        memset(sendBuffer, 0x00, sizeof(sendBuffer));


 

        if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &to, sizeof(to)) < 0) { //Set TIMEOUT option for this socket

               perror("setsockopt() error...\n");

               exit(1);

        }


 

        memset(&servAddr, 0, sizeof(servAddr));

        servAddr.sin_family = AF_INET;

        servAddr.sin_addr.s_addr = inet_addr(server_ip); //ip setting

        servAddr.sin_port = htons(server_port); //port setting


 

        //send ping

        sprintf(sendBuffer, "Ping %d", seq); //make send msg

        if (sendto(sockfd, sendBuffer, strlen(sendBuffer), 0,

                       (struct sockaddr*) &servAddr, sizeof(servAddr))

                       != strlen(sendBuffer)) {

               perror("sendto() error...\n");

               return 0;

        }

        printf("%s sent\n", sendBuffer);

        si_sendCount += 1; //Plus send count


 

        gettimeofday(&stime, NULL); //Start time value for rtt

        servLen = sizeof(servAddr); //get servAddr size


 

        //receive ping

        recvLen = recvfrom(sockfd, recvBuffer, 1024 - 1, 0,

                       (struct sockaddr*) &servAddr, &servLen);

        if (recvLen == -1) { //time-out

               printf("%s timeout!\n", sendBuffer);

               si_lostCount += 1; //plus lost count

               return 0;

        } else if (recvLen != strlen(sendBuffer)) { //error

               perror("recvfrom() error...\n");

               return 0;

        } else

               si_recvCount += 1; //plus recv count

        gettimeofday(&etime, NULL); //end time

        duration = (etime.tv_sec * 1000 - stime.tv_sec * 1000)

                       + (etime.tv_usec / 1000 - stime.tv_usec / 1000); //duration time

        if (duration < sd_min)

               sd_min = duration;

        if (duration > sd_max)

               sd_max = duration;


 

        sd_tot += duration; //plus tot duration time


 

        printf("%s reply received from %s : RTT = %0.0f ms\n", recvBuffer,

                       server_ip, duration);

        close(sockfd); //socket close

}