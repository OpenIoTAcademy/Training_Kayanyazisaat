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
        kySocket_destroy(&m_gpio_connection);
    }
    kySocket_connect(&m_gpio_connection);
}

void gpio_deInit(void)
{
    kySocket_disconnect(&m_gpio_connection);
    kySocket_destroy(&m_gpio_connection);
}

void gpio_setDirection(const tGpioDef gpio, uint_fast8_t newVal)
{
    char sendbuf[20] = {0};

    char port_char = 'A' + gpio.port;
    char value_char = newVal ? '1': '0';
    uint32_t *intptr = (uint32_t *)sendbuf;
    uint32_t length;
    length = snprintf(&sendbuf[4], 16, "GPIO%c%02dD%c", port_char, gpio.pin, value_char);
    *intptr = length;
    //memcpy(&sendbuf[4], tmpbuf, length);
    kySocket_send(&m_gpio_connection, sendbuf, length + sizeof(length));
}

void gpio_getDirection(const tGpioDef gpio, uint_fast8_t *const outVal)
{
    char sendbuf[20] = {0};
    char recvbuf[20] = {0};

    char port_char = 'A' + gpio.port;
    uint32_t *intptr = (uint32_t *)sendbuf;
    uint32_t length;
    length = snprintf(&sendbuf[4], 16, "GPIO%c%02dRD", port_char, gpio.pin);
    *intptr = length;
    kySocket_send(&m_gpio_connection, sendbuf, length + sizeof(length));
    kySocket_receive(&m_gpio_connection, recvbuf, sizeof(recvbuf));
    printf("%s\n", recvbuf);
    *outVal = 1;
}

/*
 * Fonksiyonlar ya void olacaklar ya da int olarak durum donecekler
 * Parametreler sende
 * typedef ile tkyGpioDef structure
 *        Port  No
 *        Pin   No
 * gpio_deInit()
 * gpio_setDirection(tGpioDef, value)
 * gpio_getDirection(tGpioDef, &retVal)
 * gpio_setPinLevel
 * gpio_getPinLevel
 * gpio_setPullUp
 * gpio_getPullUp
 * gpio_setPullDown
 * gpio_getPullDown
 *
Baslik    GPIO
Port No    A/B/C....
Pin No     00/15
Komut      D/S/U/P/R
Parametre  1/0

Komutlar
D -> Direction Giris/Cikis
V -> Values    1/0
U -> Pull-up   1/0
P -> Pull-Down 1/0
R -> Read      D/V/U/P
 *
 */
