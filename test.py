import threading
from time import sleep
from pynput import mouse
import keyboard
import sys
from queue import Queue

from upgrader.position import PositionsRecorder
from upgrader.status import StatusRecorder
from upgrader.tries import TriesRecorder
from upgrader.caster import Caster

def main():
    positions_recorder = PositionsRecorder()

    comm_queue = Queue()
    tries_recorder = TriesRecorder(comm_queue)
    status_recorder = StatusRecorder(comm_queue)
    caster = Caster(comm_queue)

    while True:
        if keyboard.is_pressed('shift+z'):
            if not positions_recorder.is_alive():
                positions_recorder = PositionsRecorder()
                positions_recorder.start()
                print('Starting the upgrader...')
        elif keyboard.is_pressed('shift+x'):
            if positions_recorder.is_alive():
                positions_recorder.stop()
                positions_recorder.join()
                print('Stopping the upgrader...')
            else:
                print('Upgrader is not running...')
        elif keyboard.is_pressed('ctrl+z'):
            if positions_recorder.is_alive():
                positions_recorder.stop()
                positions_recorder.join()
            print('Exiting the upgrader...')
            sys.exit(0)
            break
        elif keyboard.is_pressed('shift+tab'):
            if not tries_recorder.is_alive():
                tries_recorder.start()
            if not status_recorder.is_alive():
                status_recorder.start()
            if not caster.is_alive():
                caster.start()

        sleep(0.1)  # Prevents excessive CPU usage

if __name__ == "__main__":
    main()
