from time import sleep
import threading
import json
from PIL import ImageGrab
import cv2
import pytesseract
import numpy as np
from queue import Queue

from upgrader.types import Position

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class StatusRecorder(threading.Thread):
    def __init__(self, comm_queue: Queue):
        super().__init__()
        self._running = True
        self._comm_queue = comm_queue
        self.tries_pos: Position = None

        with open('sample.json') as f:
            d = json.load(f)
            start_pos = d['update_number_start_pos']
            end_pos = d['update_number_end_pos']

            position = Position('status')
            position.set_position(start_pos['x'], start_pos['y'])
            position.set_end_position(end_pos['x'], end_pos['y'])

            self.tries_pos = position

    def run(self):
        while self._running:
            img = ImageGrab.grab(bbox=(self.tries_pos.x, self.tries_pos.y, self.tries_pos.x1, self.tries_pos.y1))
            img.save("status.png")

            gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
            upscaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            cv2.imwrite("status_upscaled_image.png", upscaled)

            custom_config = r'--oem 3 --psm 10 outputbase digits -c tessedit_char_whitelist=0123456789'
            text = pytesseract.image_to_string(upscaled, config=custom_config)

            text = pytesseract.image_to_string(upscaled, config=custom_config)
            # print("[Status] Recognized text:", text.strip())
            self._comm_queue.put({ 'status': text.strip() })

            sleep(0.5)

    def stop(self):
        self._running = False