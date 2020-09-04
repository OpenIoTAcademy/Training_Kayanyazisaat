'''
Created on 5 Aug 2020

@author: IBeRyUS
'''
import threading
import socketserver

class SocketRequestHandler(socketserver.BaseRequestHandler):
    """ TCP Socket request handler class
    """
    def handle(self):
        """
        The request handler class for our server.

        It is instantiated once per connection to the server, and must
        override the handle() method to implement communication to the
        client.
        """

        # self.request is the TCP socket connected to the client
        active_thread = threading.current_thread()
        
        data = self.request.recv(1024)
        if len(data) > 4 :
            data_len = data[0:4]
            data_len = int.from_bytes(data_len, byteorder='little')
            if data_len < 50:
                data = data[4:(data_len + 4)]
                self.request.sendall(data)
                print("Data = {}".format(data))
#        active_thread.set_value_hede()
        #print("{} wrote:".format(self.client_address[0]))
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())

    def finish(self):
        """
        The request handler class for our server.
        It is instantiated once per connection to the server, and must
        override the handle() method to implement communication to the
        client.
        """
        print("Peer {} Port {} Disconnected".format(self.client_address[0], self.client_address[1]))

class GpioEmulator(threading.Thread):
    """
    Threaded emulator class
    """
    def __init__(self, server, port_num):
        """
        Constructor
        """
        # initialise local variables
        #self.delay = delay
        self.server = server
        self.port_num = port_num
        # call inherited Thread init function and set inherited variable values
        self.data_count = 0
        super().__init__(name=__class__.__name__)
        self.server = socketserver.TCPServer((self.server, self.port_num),
                                             SocketRequestHandler, bind_and_activate=False)
    #enddef __init__

    def service_actions(self):
        """
        Overridden service_actions function.
        """
#        print(self.hede)
    #enddef service_actions

    def run(self):
        print ("Starting server in " + self.name)
        self.server.server_bind()
        self.server.server_activate()
        self.server.service_actions = self.service_actions
        self.server.serve_forever()
        print("Stopping server in "+ self.name)

    #enddef run
    def close(self):
        """
        Close server and let thread to shutdown
        """
        self.server.shutdown()
    #enddef close
