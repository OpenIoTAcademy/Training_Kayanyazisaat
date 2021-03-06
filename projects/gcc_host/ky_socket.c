#include <stdio.h>
#include <string.h>
#ifdef WINNT
#include <winsock2.h>
#include <ws2tcpip.h>
#include <errno.h>
#else
#include <sys/socket.h>
#endif

#include "ky_socket_if.h"

int kySocket_init(void)
{
#ifdef WINNT
    WSADATA wsaData = {0};
    int result = WSAStartup(MAKEWORD(2,2), &wsaData);
    if (0 != result)
    {
        printf("WSAStartup failed with error: %d\n", result);
    }
    return (result);
#else
    return (0);
#endif
}

int kySocket_quit(void)
{
#ifdef WINNT
    int result = WSACleanup();
    if (0 != result)
    {
        printf("WSACleanup failed with error: %d\n", result);
    }
    return (result);
#else
    return (0);
#endif
}


int kySocket_create(tkySocketInfo *connection, const char *addr, const char *port)
{
    int retval;
    struct addrinfo *result = NULL;
    struct addrinfo hints = { 0 };

    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    // Resolve the server address and port
    retval = getaddrinfo(addr, port, &hints, &result);
    if(0 == retval)
    {
        connection->sc = socket(result->ai_family, result->ai_socktype, result->ai_protocol);
        connection->ai_addrlen = result->ai_addrlen;
        memcpy(&connection->ai_addr, result->ai_addr, sizeof(struct sockaddr));
    }
    return (retval);
}

int kySocket_connect(tkySocketInfo *connection)
{
    const int retval = connect(connection->sc, &connection->ai_addr, connection->ai_addrlen);
#ifdef WINNT
    if (0 != retval)
    {
        printf("kySocket_send failed: %d\n", WSAGetLastError());
    }
#endif
    return (retval);
}

int kySocket_disconnect(tkySocketInfo *connection)
{
    const int retval = shutdown(connection->sc, SD_SEND);
#ifdef WINNT
    if (0 != retval)
    {
        printf("kySocket_send failed: %d\n", WSAGetLastError());
    }
#endif
    return (retval);
}

int kySocket_destroy(tkySocketInfo *connection)
{
    return (closesocket(connection->sc));
}

int kySocket_send(const tkySocketInfo *connection, const char *buf, const int len)
{
    int retval = send(connection->sc, buf, len, 0);
    if (len == retval)
    {
        retval = 0;
    }
    return (retval);
}

int kySocket_receive(const tkySocketInfo *connection, char *buf, const int len)
{
    int retval = 0;
    int rx_len = 0;
    do {

        rx_len= recv(connection->sc, buf, len, 0);
        if ( rx_len > 0 )
        {
            retval += rx_len;
        }
        else if ( rx_len != 0 )
        {
            retval = -1;
        }

    } while( rx_len > 0 );

    return (retval);
}
