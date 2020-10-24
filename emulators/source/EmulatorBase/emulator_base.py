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
        self._server_active = True
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # enddef __init__

    def process_data(self, received_data):
        """Processes received data. Should be overridden by child class."""
        # enddef process_data

    def send_data(self, data, data_len):
        """Sends data to the client socket."""
        to_send = bytes()
        if isinstance(data, str):
            to_send = data_len.to_bytes(2, byteorder='little') + data.encode("utf8")
        self._cl_ac.sendall(to_send)
        #enddef send_data

    def run(self):
        """Thread class overriden run function. Runs server until main script is stopped."""
        print("Starting server in " + self.name)
        request_queue_size = 5
        self._server_socket.bind((self.server_addr, self.server_port))
        self._server_socket.listen(request_queue_size)
        self._serve_forever()
        print("Stopping server in " + self.name)
    # enddef run

    def fileno(self):
        """Return socket file number.Interface required by selector."""
        return self._server_socket.fileno()
    # enddef fileno

    def close(self):
        """Closes server and ends thread."""
        self._server_active = False
        if hasattr(self, '_cl_ac'):
            if isinstance(self._cl_ac, socket.socket):
                self._cl_ac.shutdown(socket.SHUT_RDWR)
                self._cl_ac.close()
        self.__is_shut_down.wait()
    # enddef close

    def _serve_forever(self, poll_interval=0.5):
        """Serves forever."""
        self.__is_shut_down.clear()
        try:
            with _ServerSelector() as selector:
                selector.register(self, selectors.EVENT_READ)
                while self._server_active:
                    ready = selector.select(poll_interval)
                    if not self._server_active:
                        break
                    if ready:
                        self._handle_request()
        finally:
            self.__is_shut_down.set()
    # enddef _serve_forever

    def _handle_request(self):
        """Handles accepted socket connection."""
        self._cl_ac, cl_addr = self._server_socket.accept() # pylint: disable=unused-variable,attribute-defined-outside-init
        while hasattr(self, '_cl_ac'):
            try:
                data = self._cl_ac.recv(2)
                if len(data) == 2:
                    data_len = int.from_bytes(data, byteorder='little')
                    data = self._cl_ac.recv(data_len)
                    try :
                        self.process_data(data)
                    except Exception as exp: # pylint: disable=broad-except
                        self._print_traceback(exp)
                elif len(data) == 0:
                    del self._cl_ac
            except Exception as exp: # pylint: disable=broad-except
                del self._cl_ac
                self._print_traceback(exp)
    # enddef _handle_request

    @classmethod
    def _print_traceback(cls, exp):
        """Extracts and prints traceback information from Exception."""
        trace = []
        trace_back = exp.__traceback__
        while trace_back is not None:
            trace.append({
                    "filename": trace_back.tb_frame.f_code.co_filename,
                    "name": trace_back.tb_frame.f_code.co_name,
                    "lineno": trace_back.tb_lineno
                })
            trace_back = trace_back.tb_next
        print(str({
                'type': type(exp).__name__,
                'message': str(exp),
                'trace': trace
            }))
    # enddef _print_traceback
