#ifndef GPIO_IF_H
#define GPIO_IF_H

typedef enum
{
	PORT_A,
	PORT_B,
	PORT_C,
	PORT_D,
	PORT_E,
	NUM_OF_PORTS
} tGpioPorts;

typedef struct
{
	tGpioPorts port;
	uint8_t pin;
} tGpioDef ;

void gpio_init(void);
void gpio_setDirection(const tGpioDef gpio, uint_fast8_t value );

#endif  /* GPIO_IF_H */
