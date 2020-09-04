#include <stdint.h>
#include <stdio.h>
#include "ky_socket_if.h"
#include "gpio_if.h"

static tkySocketInfo m_gpio_connection = {0};

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
}

void gpio_setDirection(const tGpioDef gpio, uint_fast8_t value )
{

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
