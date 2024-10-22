import threading
from time import sleep
from pynput import mouse
import keyboard
import sys

from upgrader.position import PositionsRecorder
from upgrader.tries import TriesRecorder


def main():
    positions_recorder = PositionsRecorder()
    tries_recorder = TriesRecorder()

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
                tries_recorder = TriesRecorder()
                tries_recorder.start()

        sleep(0.1)  # Prevents excessive CPU usage

if __name__ == "__main__":
    main()
