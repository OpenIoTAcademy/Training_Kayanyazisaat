'''
Created on 5 Aug 2020

@author: IBeRyUS
'''
from EmulatorBase import EmulatorBase


class GpioEmulator(EmulatorBase):
    """Gpio Emulator Class."""
    def __init__(self, server, server_port, port_list):
        """Initialises class."""
        # initialise local variables
        # self.delay = delay
        super().__init__(emulator_name=__class__.__name__,
                         server_addr=server, port_num=server_port)
        self._commands = self._initialise_commands()
        self._ports = []
        self._port_lkup = {}
        i = 0
        for key in port_list:
            port = self._create_port_instance(port_list[key])
            self._ports.append(port)
            self._port_lkup.update({key: i})
            i += 1
    # enddef __init__

    @classmethod
    def _create_port_instance(cls, number_of_pins):
        """Creates and return list of pin definitions for port instance.
           @param number_of_pins: Number of pins in port instance
        """
        return list({"Direction": 1, "Value": 0, "Pull-up": 0, "Pull-down": 0} for _ in range(number_of_pins))
    # enddef _create_port_instance

    @classmethod
    def _initialise_commands(cls):
        """Initialises commands for emulator interface."""
        return {
            "D": "Direction",
            "V": "Value",
            "U": "Pull-up",
            "P": "Pull-down",
            "R": "Read",
            }
    # enddef _initialise_commands

    def process_data(self, received_data):
        """Overridden process function for received data.
           This function called by EmulatorBase in try block.
           This prevents any failure on process_data function to cause connection issues.
        """
        received_data = received_data.decode()
        if received_data[0:4] == "GPIO":
            port = received_data[4]
            pin = int(received_data[5:7])
            command = received_data[7]
            if command == "R":
                param = received_data[8]
                self._read_pin_field_values(port, pin, param)
            else:
                param = int(received_data[8])
                self._update_pin_field_values(self._commands[command], port, pin, param)
        # request.sendall(received_data.encode("utf-8"))
        # enddef process_data

    def _update_pin_field_values(self, command, port, pin, param):
        """Updates pin field values."""
        print("Received Command =", command , port, pin, param)
        self._ports[self._port_lkup[port]][pin][command] = param
        # enddef _update_pin_field_values

    def _read_pin_field_values(self, port, pin, param):
        """Reads pin field values and sends back."""
        value = self._ports[self._port_lkup[port]][pin][self._commands[param]]
        print("Read Command. Field = {2} {0} {1} {3}".format(port, pin, param, value))
        new_string = "GPIO{}{:02d}{}{}".format(port, pin, param, value)
        self.send_data(new_string, len(new_string))
        # enddef _read_pin_field_values
