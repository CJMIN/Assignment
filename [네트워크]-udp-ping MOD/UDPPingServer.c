// Choi,Jeongmin 20165974

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>

#define BUFSIZE 1024         //buffer size

int port = 35974;	//hardcoding
int sFd;	//main socket

void* handler(void* param);

typedef struct {  //Structure for thread
int recvLen;
struct sockaddr_in cAddr;
char buf[BUFSIZE];
} Param;

void* handler(void* param) {
	//copy arg values
	Param* parm = param;
	char buf[BUFSIZE];
	struct sockaddr_in cAddr = parm->cAddr;
	int recvLen = parm->recvLen;
	strcpy(buf, parm->buf);

	srand((int)pthread_self()); //thread id

	int timeout = rand() % 2000001; //delay value (0~2sec)
	int drop = rand() % 5;

	if (drop == 0) { //packet drop (20%)
		printf("Server: drop %s\n", buf);
		return (void*)0;
	}

	usleep(timeout); //sleep

	if (sendto(sFd, buf, recvLen, 0, (struct sockaddr*) &cAddr,
		sizeof(cAddr)) != recvLen) {
		printf("sendto() error...\n");
		exit(1);
	}

	printf("Server: reply %s (%d ms latency) \n", buf, timeout/1000);
}

void* Byebye() { //ctrl+c
	printf("\n=====================================\n");
	printf("Bye bye~\n");
	close(sFd); //Close socket
	exit(0);
}

int main(int argc, char* argv[]) {
	signal(SIGINT, (void*)Byebye);
	struct sockaddr_in sAddr; /*structure to hold server's address */
	struct sockaddr_in cAddr; /*structure to hold client's address */

	int parm = 1;
	int cAddrSize;	//client address length

	char buffer[BUFSIZE];

	printf("\nServer on (port:%d)\n", port);
	printf("=====================================\n");

	if ((sFd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) { //UDP socket
		printf("sock() error...\n");
		return 1;
	}
	else
		printf("socket() success...\n");

	sAddr.sin_family = AF_INET;
	sAddr.sin_addr.s_addr = htonl(INADDR_ANY);	//set ip any
	sAddr.sin_port = htons(port);	//set port

	//time out option
	if (setsockopt(sFd, SOL_SOCKET, SO_REUSEADDR, &parm, sizeof(parm)) == -1) { 
		printf("setsockopt() error..\n");
		return 1;
	}
	else
		printf("setsockopt() success...\n");

	//bind
	if (bind(sFd, (struct sockaddr*) & sAddr, sizeof(sAddr)) == -1) { 
		printf("bind() error...\n"); // debugging
		return 1;
	}
	else
		printf("bind() success...\n");

	while (1) {
		Param param; //Arguments for thread
		pthread_t pingThread; //Thread for each ping
		int recvLen = 0;

		cAddrSize = sizeof(cAddr);

		memset(buffer, 0x00, sizeof(buffer));
		if ((recvLen = recvfrom(sFd, buffer, BUFSIZE - 1, 0, (struct sockaddr*) &cAddr, &cAddrSize)) == -1) {
			printf("recvfrom() error...\n");
			return 1;
		}
		else {
			//param for thread's arg
			strcpy(param.buf, buffer);
			param.recvLen = recvLen;
			param.cAddr = cAddr;
		}

		printf("Server: recv %s\n", buffer);

		pthread_create(&pingThread, NULL, (void*)handler, (void*)&param); //create ping handler thread
		pthread_detach(&pingThread);
	}
}
