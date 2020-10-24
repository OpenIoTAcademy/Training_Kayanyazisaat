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
        printf("kySocket_init failed. WSA Error=: %d\n", result);
    }
    return (result);
#else
    return (0);
#endif
}

int kySocket_quit(void)
{
#ifdef WINNT
    const int result = WSACleanup();
    if (SOCKET_ERROR  == result)
    {
        printf("kySocket_quit failed. WSA Error= %d\n", WSAGetLastError());
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
    if (SOCKET_ERROR == retval)
    {
        printf("kySocket_connect failed. WSA Error= %d\n", WSAGetLastError());
    }
#endif
    return (retval);
}

int kySocket_disconnect(tkySocketInfo *connection)
{
    const int retval = shutdown(connection->sc, SD_SEND);
#ifdef WINNT
    if (SOCKET_ERROR == retval)
    {
        printf("kySocket_disconnect failed. WSA Error= %d\n", WSAGetLastError());
    }
#endif
    return (retval);
}

int kySocket_destroy(tkySocketInfo *connection)
{
    const int retval = closesocket(connection->sc);
#ifdef WINNT
    if (SOCKET_ERROR == retval)
    {
        printf("kySocket_destroy failed. WSA Error= %d\n", WSAGetLastError());
    }
#endif
    return (retval);
}

int kySocket_send(const tkySocketInfo *connection, const char *buf, const int len)
{
    int retval = send(connection->sc, buf, len, 0);
    if (len == retval)
    {
        retval = 0;
    }
    else if (SOCKET_ERROR == retval)
    {
#ifdef WINNT
        printf("kySocket_send failed. WSA Error= %d\n", WSAGetLastError());
#endif
    }
    return (retval);
}

int kySocket_receive(const tkySocketInfo *connection, char *buf, const int length_max)
{
    int rx_len;
    int retval  = recv(connection->sc, (char*)&rx_len, 4, 0);
    if ( retval == 4 && rx_len < length_max )
    {
        retval = recv(connection->sc, buf, rx_len, 0);
    }
    else
    {
        retval = -1;
#ifdef WINNT
        printf("kySocket_receive failed. WSA Error= %d\n", WSAGetLastError());
#endif
    }

    return (retval);
}
