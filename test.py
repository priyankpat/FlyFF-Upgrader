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

class TerminateListener(threading.Thread):
    def __init__(self, tries_thread, status_thread, caster_thread):
        super().__init__()
        self._running = True
        self._tries_thread = tries_thread
        self._status_thread = status_thread
        self._caster_thread = caster_thread

    def run(self):
        while self._running:
            if keyboard.is_pressed('ctrl+z'):
                self._tries_thread.stop()
                self._tries_thread.join()
                self._status_thread.stop()
                self._status_thread.join()
                self._caster_thread.stop()
                self._caster_thread.join()

                print('Exiting the upgrader...')
                sys.exit(0)
                return
            sleep(0.1)

    def stop(self):
        self._running = False

def main():
    positions_recorder = PositionsRecorder()

    tries_queue = Queue()
    status_queue = Queue()

    tries_recorder = TriesRecorder(tries_queue)
    status_recorder = StatusRecorder(status_queue)
    caster = Caster(tries_queue, status_queue)

    terminate_listener = TerminateListener(tries_recorder, status_recorder, caster)

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
            # if tries_recorder.is_alive():
            #     tries_recorder.stop()
            #     tries_recorder.join()
            # if status_recorder.is_alive():
            #     status_recorder.stop()
            #     status_recorder.join()
            # if caster.is_alive():
            #     caster.stop()
            #     caster.join()

            sleep(1)
            print('Exiting the upgrader...')
            sys.exit(0)
            break
        elif keyboard.is_pressed('shift+tab'):
            if not terminate_listener.is_alive():
                terminate_listener.start()
            if not tries_recorder.is_alive():
                tries_recorder.start()
            if not status_recorder.is_alive():
                status_recorder.start()
            if not caster.is_alive():
                caster.start()

        sleep(0.1)  # Prevents excessive CPU usage

if __name__ == "__main__":
    main()
