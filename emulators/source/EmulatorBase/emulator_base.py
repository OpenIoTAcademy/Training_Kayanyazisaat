'''
@filename: emulator_base.py
@brief:    Base class for emulators
'''
import threading
import socketserver
from tkinter.constants import ACTIVE

class EmulatorBase(threading.Thread):
    """ Threaded emulator class
    """
    class Handler(socketserver.BaseRequestHandler):
        """ TCP Socket request handler class
        """
        def handle(self):
            """ The request handler class for our server.
            It is instantiated once per connection to the server, and must
            override the handle() method to implement communication to the
            client.
            """
            data = self.request.recv(1024)
            if len(data) > 4 :
                data_len = data[0:4]
                data_len = int.from_bytes(data_len, byteorder='little')
                if len(data) == (data_len + 4):
                    data = data[4:(data_len + 4)]
                    active_thread = threading.current_thread()
                    active_thread.process_data(data.decode(), self.request)
        #enddef handle
        
        def finish(self):
            """ The request handler class for our server.
            It is instantiated once per connection to the server, and must
            override the handle() method to implement communication to the
            client.
            """
            print("Peer {} Port {} Disconnected".format(self.client_address[0],
                                                        self.client_address[1]))
        #enddef finish

    def __init__(self, emulator_name, server, port_num):
        """ Constructor
        """
        # initialise local variables
        # call inherited Thread init function and set inherited variable values
        self.data_count = 0
        super().__init__(name=emulator_name)
        self.server = socketserver.TCPServer((server, port_num),
                                             self.Handler, bind_and_activate=False)
    #enddef __init__

    def service_actions(self):
        """ Overridden service_actions function.
        """
#        print(self.hede)
    #enddef service_actions
    def process_data(self, received_data, request):
        """ Process received data. Should be overridden by class
        """
        #enddef
        
    def run(self):
        """ Thread class overriden run function
        """
        print ("Starting server in " + self.name)
        self.server.server_bind()
        self.server.server_activate()
        self.server.service_actions = self.service_actions
        self.server.serve_forever()
        print("Stopping server in "+ self.name)
    #enddef run

    def close(self):
        """ Close server and let thread to be shut down
        """
        self.server.shutdown()
    #enddef close
