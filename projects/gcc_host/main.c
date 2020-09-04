#include <stdint.h>
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
#include "gpio_if.h"

typedef struct
{
	char port ;
	int  pin;


}tkyGpioDef ;

int main(void)
{
// Don't Erase
	int iResult;
	setvbuf(stdout, NULL, _IONBF, 0);
    if(kySocket_init() != 0)
    {
        printf("WSAStartup failed with error: %d\n", iResult);
        kySocket_quit();
        return 1;
    }
// Start of Main
	static tkySocketInfo connection = {0};



    const char *text = "GPIOA10D0";

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

    kySocket_create(&connection, "localhost", "9999");

    iResult = kySocket_send(&connection, (const char*)sendbuf, len);
    iResult = kySocket_receive(&connection, recvbuf, len);

    kySocket_destroy(&connection);

// End of Main

// Don't Erase
    kySocket_quit();
    printf("End Of Main\n");

    return 0;
}
