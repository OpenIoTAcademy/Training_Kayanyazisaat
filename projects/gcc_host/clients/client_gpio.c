#include <stdio.h>
#include "ky_socket_if.h"
#include "gpio_if.h"

static tkySocketInfo m_gpio_connection = {0};

void gpio_init(void)
{
    if (kySocket_create(&connection, "localhost", "9999") != 0)
    {
    }
}
