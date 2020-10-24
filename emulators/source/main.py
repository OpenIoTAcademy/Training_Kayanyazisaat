'''
Created on 6 Aug 2020

@author: IBeRyUS
'''
# import python and pip libraries
import signal
import time

# import local libraries
from GpioEmulator import GpioEmulator

IS_RUNNING = True


def signal_handler(sig, frame):
    """ Ctrl+C Interrupt Signal Handler.
        This function prototype needs sig and frame parameters and currently not used.
        Will be disabled temporarily in pylint.
    """
    #pylint: disable=unused-argument,global-statement
    global IS_RUNNING
    IS_RUNNING = False
    print("Interrupt SIGNAL received. Closing application")


def start_emulator(emulator, params):
    """ Creates and starts the selected emulator with the parameters
    """
    i = emulator("localhost", params[0], params[1])
    i.start()
    return i

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print("This is main")

    # Create new threads list to keep track of emulators
    emulators = []
    emulators.append(start_emulator(GpioEmulator, [9999, {"A": 16, "B": 16, "C": 16, "D": 16, "E": 16}]))
    # emulators.append(start_emulator(GpioEmulator, [10000, {"A":2, "B":3}]))

    while IS_RUNNING:
        pass

    for e in emulators:
        time.sleep(0.2)
        e.close()
        e.join()
    print("Exiting Main Thread")
