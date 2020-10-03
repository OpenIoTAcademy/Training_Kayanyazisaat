'''
@filename: emulator_base.py
@brief:    Base class for emulators
'''
import threading
import socket
import selectors
if hasattr(selectors, 'PollSelector'):
    _ServerSelector = selectors.PollSelector
else:
    _ServerSelector = selectors.SelectSelector

class EmulatorBase(threading.Thread):
    """ Threaded emulator class
    """
    def __init__(self, emulator_name, server_addr, port_num):
        """ Constructor
        """
        # initialise local variables
        # call inherited Thread init function and set inherited variable values
        super().__init__(name=emulator_name)
        self.server_addr = server_addr
        self.server_port = port_num
        self.__is_shut_down = threading.Event()
        self.server_active = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #enddef __init__

    #enddef service_actions
    def process_data(self, received_data):
        """ Process received data. Should be overridden by class
        """
        #enddef

    def run(self):
        """ Thread class overriden run function
        """
        print ("Starting server in " + self.name)
        request_queue_size = 5
        self.server_socket.bind((self.server_addr, self.server_port))
        self.server_socket.listen(request_queue_size)
        self.serve_forever()
        print("Stopping server in "+ self.name)
    #enddef run
    
    def serve_forever(self, poll_interval=0.5):
        self.__is_shut_down.clear()
        try:
            with _ServerSelector() as selector:
                selector.register(self, selectors.EVENT_READ)
                while self.server_active:
                    ready = selector.select(poll_interval)
                    if not self.server_active:
                        break
                    if ready:
                        self._handle_request_noblock()
        finally:
            self.__is_shut_down.set()
    #enddef serve_forever

    def _handle_request_noblock(self):
        self.cl_ac, cl_addr = self.server_socket.accept()
        while self.cl_ac is not None:
            try:
                data = self.cl_ac.recv(4)
                if len(data) == 4 :
                    data_len = data[0:4]
                    data_len = int.from_bytes(data_len, byteorder='little')
                    data = self.cl_ac.recv(data_len)
#                    active_thread = threading.current_thread()
#                    active_thread.process_data(data.decode())
                    self.process_data(data.decode())
                elif len(data) == 0:
                    self.cl_ac = None
            except:
                self.cl_ac = None
    #enddef _handle_request_noblock

    def fileno(self):
        """Return socket file number.
        Interface required by selector.
        """
        return self.server_socket.fileno()
    #enddef fileno

    def close(self):
        """ Close server and let thread to be shut down
        """
        self.server_active = False
        if hasattr(self, 'cl_ac') and self.cl_ac is not None:
            self.cl_ac.shutdown(socket.SHUT_RDWR)
            self.cl_ac.close()
        self.__is_shut_down.wait()
    #enddef close
