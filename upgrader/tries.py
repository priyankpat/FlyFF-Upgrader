from time import sleep

class TriesRecorder(threading.Thread):
    def __init__(self):
        super().__init__()
        self._running = True

    def run(self):
        while self._running:

            sleep(0.1)

    def stop(self):
        self._running = False