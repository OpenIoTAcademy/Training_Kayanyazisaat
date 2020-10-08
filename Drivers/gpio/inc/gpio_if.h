#ifndef GPIO_IF_H
#define GPIO_IF_H

#define GPIO_DIRECTION_OUTPUT    (0)
#define GPIO_DIRECTION_INPUT     (1)
#define GPIO_PULL_UP_ENABLED     (0)
#define GPIO_PULL_UP_ACTIVATED   (1)
#define GPIO_PULL_DOWN_ENABLED   (0)
#define GPIO_PULL_DOWN_ACTIVATED (1)
typedef enum
{
    PORT_A = 0, //0
    PORT_B, //1
    PORT_C,
    PORT_D,
    PORT_E,
    NUM_OF_PORTS
} tGpioPorts;

typedef struct
{
    tGpioPorts port;
    uint8_t pin;
    uint8_t pullup;
    uint8_t pulldown;
} tGpioDef ;

void gpio_init(void);
void gpio_setDirection(const tGpioDef gpio, uint_fast8_t value );
void gpio_setPullUp(const tGpioDef gpio,uint_fast8_t value);
void gpio_setPullDown(const tGpioDef gpio,uint_fast8_t value);
#endif  /* GPIO_IF_H */
