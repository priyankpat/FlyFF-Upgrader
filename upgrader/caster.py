import threading
from queue import Queue
from time import sleep

class Caster(threading.Thread):
    def __init__(self, comm_queue: Queue):
        super().__init__()
        self._running = True
        self._comm_queue = comm_queue

    def run(self):
        while self._running:
            data = self._comm_queue.get()
            print(data)

            sleep(0.1)

    def stop(self):
        self._running = False