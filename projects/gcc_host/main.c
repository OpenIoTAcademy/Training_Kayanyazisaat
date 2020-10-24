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

int main(void)
{
// Don't Erase
    setvbuf(stdout, NULL, _IONBF, 0);
    if(kySocket_init() != 0)
    {
        kySocket_quit();
        return 1;
    }
    tGpioDef led_pin1  = { .port = PORT_A, .pin = 2};
    tGpioDef pin2      = { .port = PORT_B, .pin = 9};
    tGpioDef led_pin3  = { .port = PORT_C, .pin = 11};
    tGpioDef pin4      = { .port = PORT_C, .pin = 15};
    //while(1)
    uint_fast8_t value;
    {
// Start of Main
        gpio_init();
//        gpio_getDirection(led_pin1);
        gpio_setDirection(led_pin1, GPIO_DIRECTION_OUTPUT);
        gpio_getDirection(led_pin1, &value);

        //gpio_setDirection(pin2, GPIO_DIRECTION_INPUT);
        //gpio_setDirection(led_pin3, GPIO_DIRECTION_OUTPUT);
        //gpio_setDirection(pin4, GPIO_DIRECTION_INPUT);

// End of Main
        gpio_deInit();
    }
// Don't Erase
    kySocket_quit();
    printf("End Of Main\n");

    return 0;
}
