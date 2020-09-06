'''
Created on 6 Aug 2020

@author: IBeRyUS
'''
# import python and pip libraries
import signal
import time

# import local libraries
from GpioEmulator import GpioEmulator

_is_running = True

def signal_handler(sig, frame):
    global _is_running
    _is_running = False
    print("Interrupt SIGNAL received. Closing application")

def start_emulator(emulators, emulator, params):
    i = emulator(params[0], "localhost", params[1])
    emulators.append(i)
    i.start()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print("This is main")

    # Create new threads list to keep track of emulators
    emulators = []
    start_emulator(emulators, GpioEmulator, [{"A":2, "B":3}, 9999])

    while _is_running:
        pass

    for e in emulators :
        time.sleep(0.2)
        e.close()
        e.join()
    print ("Exiting Main Thread")
