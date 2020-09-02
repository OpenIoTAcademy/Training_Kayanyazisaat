'''
Created on 6 Aug 2020

@author: IBeRyUS
'''
# import python and pip libraries
import sys
import signal
import time
sys.path.append("gpio/")

# import local libraries
from gpio_emulator import GpioEmulator

_is_running = True

def signal_handler(sig, frame):
    global _is_running
    _is_running = False
    print("Interrupt SIGNAL received. Closing application")

def start_emulator(emulators, emulator, port):
    i = emulator("localhost", port)
    emulators.append(i)
    i.start()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print("This is main")

    # Create new threads list to keep track of emulators
    emulators = []
    start_emulator(emulators, GpioEmulator, 9999)

    while _is_running:
        pass

    for e in emulators :
        time.sleep(0.2)
        e.close()
        e.join()
    print ("Exiting Main Thread")
