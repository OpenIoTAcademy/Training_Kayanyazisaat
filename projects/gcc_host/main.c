#include <stdlib.h>
#include <stdio.h>
//#include "gpio_if.h"

#ifdef WINNT
#include <winsock2.h>
#include <ws2tcpip.h>
#include <errno.h>
#else
#include <sys/socket.h>
#endif
#include "ky_socket_if.h"

int main(void)
{
    int iResult;
    setvbuf(stdout, NULL, _IONBF, 0);
    if(kySocket_init() != 0)
    {
        printf("WSAStartup failed with error: %d\n", iResult);
        kySocket_quit();
        return 1;
    }


    const char *text = "GPIOADI";
    char sendbuf[20] = {0};
    char recvbuf[20] = {0};


    int len = strlen(text);
    int *lenptr = (int *)sendbuf;
    char *destptr;
    *lenptr++ = len;
    destptr = (char *)lenptr;
    for (int i = len; i; i--)
    {
    	*destptr++ = *text++;
    }
    len = len + 4;
//    iResult = kySocket_send(&connection, (const char*)sendbuf, len);
//    iResult = kySocket_receive(&connection, recvbuf, len);
//    kySocket_destroy(&connection);
    kySocket_quit();
    printf("End Of Main\n");
    return 0;
}
