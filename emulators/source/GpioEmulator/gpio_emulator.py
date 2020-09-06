'''
Created on 5 Aug 2020

@author: IBeRyUS
'''
from EmulatorBase import EmulatorBase

class GpioEmulator(EmulatorBase):
    """ Emulator class
    """
    def __init__(self, port_list, server, server_port):
        """ Constructor of the Class
        """
        # initialise local variables
        #self.delay = delay
        self.server_addr = server
        self.server_port = server_port
        super().__init__(emulator_name=__class__.__name__,
                         server=self.server_addr, port_num=self.server_port)
        self.ports = []
        self.port_lkup = {}
        i = 0;
        for key in port_list:
            port = self.create_port_instance(port_list[key])
            self.ports.append(port)
            self.port_lkup.update({key:i})
            i += 1
            
    #enddef __init__

    def create_port_instance(self, number_of_pins):
        port = list( {"Direction" : 0, "Value": 0, "Pull-up": 0, "Pull-down" :0 } for _ in range(number_of_pins) )
        return port
    #enddef create_port_instance

    def initialise_commands(self):
        
        self.commands = {
            "D": "Direction",
            "V": "Value",
            "U": "Pull-up",
            "P": "Pull-down",
            "R": "Read",
            }
    #enddef initialise_commands

    def process_data(self, received_data, request):
        """ Process received data. Should be overridden by class
        """
        if "GPIO"== received_data[0:4]:
            port = received_data[4]
            pin = received_data[5:7]
            command = received_data[7]
            param = received_data[8]
            print(received_data, port, pin, command, param)
        request.sendall(received_data.encode("utf-8"))
        #enddef

    def service_actions(self):
        """ Overridden service_actions function.
        """
#        print(self.hede)
    #enddef service_actions
