/*
 * @brief 	KayanYazi socket interface file
 *
 */
#ifndef KY_SOCKET_IF_H
#define KY_SOCKET_IF_H

#ifdef WINNT
#include <winsock2.h>
#else
typedef int	SOCKET;
#endif

typedef struct {
	SOCKET sc;
	size_t ai_addrlen;
	struct sockaddr ai_addr;
} tkySocketInfo;

int kySocket_init(void);
int kySocket_quit(void);

int kySocket_create(tkySocketInfo *connection, const char *addr, const char *port);
int kySocket_destroy(tkySocketInfo *connection);
int kySocket_send(const tkySocketInfo *connection, const char *buf, const int len);
int kySocket_receive(const tkySocketInfo *connection, char *buf, const int len);



#endif // KY_SOCKET_IF_H
