#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include "ky_socket_if.h"
#include "gpio_if.h"

static tkySocketInfo m_gpio_connection = {0};
const char *PREFIX = "GPIO";

//Doxygen Format

/*
 * @brief Initialises gpio subsytem
 * @params None
 */
void gpio_init(void)
{
    if (kySocket_create(&m_gpio_connection, "localhost", "9999") != 0)
    {
    }
    //kySocket_destroy(&connection);
}



void gpio_setDirection(const tGpioDef gpio, uint_fast8_t value )
{
    char sendbuf[20] = {0};

    char port_char = 'A' + gpio.port;
    char value_char = value ? '1': '0';
    uint32_t *intptr = (uint32_t *)sendbuf;
    uint32_t length;
    length = snprintf(&sendbuf[4], 16, "GPIO%c%02dD%c", port_char, gpio.pin, value_char);
    *intptr = length;
    //memcpy(&sendbuf[4], tmpbuf, length);
    kySocket_send(&m_gpio_connection, sendbuf, length + sizeof(length));
}
void gpio_setPullUp(const tGpioDef gpio,uint_fast8_t value)
{
    char value_char = value ? '1' : '0';
}
void gpio_setPullDown(const tGpioDef gpio,uint_fast8_t value)
{

    char value_char = value ? '1' : '0';

}

