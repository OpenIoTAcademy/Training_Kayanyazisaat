'''
Created on 5 Aug 2020

@author: IBeRyUS
'''
from EmulatorBase import EmulatorBase


class GpioEmulator(EmulatorBase):
    """ Emulator class
    """
    def __init__(self, server, server_port, port_list):
        """ Constructor of the Class
        """
        # initialise local variables
        # self.delay = delay
        super().__init__(emulator_name=__class__.__name__,
                         server_addr=server, port_num=server_port)
        self.commands = self.initialise_commands()
        self.ports = []
        self.port_lkup = {}
        i = 0
        for key in port_list:
            port = self.create_port_instance(port_list[key])
            self.ports.append(port)
            self.port_lkup.update({key: i})
            i += 1

    # enddef __init__

    @classmethod
    def create_port_instance(cls, number_of_pins):

        """ Creates and return list of pin definitions for port instance.
            @param number_of_pins: Number of pins in port instance
        """
        return list({"Direction": 0, "Value": 0, "Pull-up": 0, "Pull-down": 0} for _ in range(number_of_pins))
    # enddef create_port_instance

    @classmethod
    def initialise_commands(cls):
        """ Initialises commands for emulator interface
        """
        return {
            "D": "Direction",
            "V": "Value",
            "U": "Pull-up",
            "P": "Pull-down",
            "R": "Read",
            }
    # enddef initialise_commands

    def process_data(self, received_data):
        """ Overridden process function for received data.
        """
        if received_data[0:4] == "GPIO":
            port = received_data[4]
            pin = received_data[5:7]
            command = received_data[7]
            param = received_data[8]
            print(received_data, "PORT=", port, pin, command, param)
        # request.sendall(received_data.encode("utf-8"))
        # enddef

    def service_actions(self):
        """ Overridden service_actions function.
        """
        # print(self.hede)
    # enddef service_actions

    def gpio_set_value(self, pin_value, set_value):
        pin_value = set_value
        return set_value


    def change_value(self,pin,value,port,command):
        self.gpio_set_value(self.pin,pin)
        self.gpio_set_value(self.value, value)
        self.gpio_set_value(self.port, port)
        self.gpio_set_value(self.command, command)

        return pin,value,port,command