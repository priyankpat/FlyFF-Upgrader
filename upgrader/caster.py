import threading
from queue import Queue
from time import sleep, time
import json
from PIL import ImageGrab
import cv2
import pytesseract
import numpy as np
import os

import pyautogui
from upgrader.types import Position

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# os.environ['TESSDATA_PREFIX'] = r'C:\Users\shank\Documents\Upgrader'

class Caster(threading.Thread):
    def __init__(self, tries_queue: Queue, status_queue: Queue):
        super().__init__()
        self._running = True
        self._tries_queue = tries_queue
        self._status_queue = status_queue
        self._success_color = (25, 115, 222)

        self.current_item_index = 0
        self.items_pos = []
        self.inv_cess_pos = None
        self.inv_ces_pos = None
        self.btn_start_pos = None
        self.btn_stop_pos = None
        self.btn_reset_pos = None
        self.btn_plus_pos = None
        self.btn_minus_pos = None
        self.upg_ces_pos = None
        self.upg_cess_pos = None
        self.upg_status_pos = None

        self.tries_pos = None
        self.tries_pos_v2 = None
        self.status_pos = None

        self.load_settings()

    def load_settings(self):
        def get_config(dict, key):
            pos = d[key]
            return [pos['x'], pos['y']]

        with open('sample.json') as f:
            d = json.load(f)

            self.items_pos.append(get_config(d, 'item_1_pos'))
            self.items_pos.append(get_config(d, 'item_2_pos'))
            self.items_pos.append(get_config(d, 'item_3_pos'))
            self.items_pos.append(get_config(d, 'item_4_pos'))

            self.inv_cess_pos = get_config(d, 'inventory_cess_pos')
            self.inv_ces_pos = get_config(d, 'inventory_ces_pos')

            self.btn_start_pos = get_config(d, 'start_button_pos')
            self.btn_stop_pos = get_config(d, 'stop_button_pos')
            self.btn_reset_pos = get_config(d, 'reset_button_pos')
            self.btn_plus_pos = get_config(d, 'plus_button_pos')
            self.btn_minus_pos = get_config(d, 'minus_button_pos')

            self.upg_ces_pos = get_config(d, 'upgrade_ces_pos')
            self.upg_cess_pos = get_config(d, 'upgrade_cess_pos')
            self.upg_status_pos = get_config(d, 'upgrade_status_pos')

            tries_start_pos = d['tries_number_start_pos']
            tries_end_pos = d['tries_number_end_pos']

            tries_position = Position('tries')
            tries_position.set_position(tries_start_pos['x'], tries_start_pos['y'])
            tries_position.set_end_position(tries_end_pos['x'], tries_end_pos['y'])
            self.tries_pos = tries_position

            tries_position_v2 = Position('tries')
            tries_position_v2.set_position(tries_start_pos['x'] + 300, tries_start_pos['y'])
            tries_position_v2.set_end_position(tries_end_pos['x'], tries_end_pos['y'])
            self.tries_pos_v2 = tries_position_v2

            status_start_pos = d['update_number_start_pos']
            status_end_pos = d['update_number_end_pos']

            status_position = Position('status')
            status_position.set_position(status_start_pos['x'], status_start_pos['y'])
            status_position.set_end_position(status_end_pos['x'], status_end_pos['y'])
            self.status_pos = status_position

    def get_tries(self, position):
        print(position)
        img = ImageGrab.grab(bbox=position)
        img.save("tries.png")

        gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
        upscaled = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite("tries_upscaled_image.png", upscaled)
        cv2.imwrite("tries_threshold.png", thresh)

        custom_config = r'--oem 3 --psm 10 outputbase digits -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(upscaled, config=custom_config)
        return text.replace('Tries:', '').strip()

    def get_status(self):
        img = ImageGrab.grab(bbox=(self.status_pos.x, self.status_pos.y, self.status_pos.x1, self.status_pos.y1))
        img.save("status.png")

        gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        upscaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite("status_upscaled_image.png", upscaled)

        custom_config = r'--oem 3 --psm 10 outputbase digits -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(upscaled, config=custom_config)
        return text.strip()

    def wait_for_success(self, position, duration = 2):
        start_time = time()
        while True:
            tries = 0
            tries_raw = self.get_tries((self.tries_pos.x, self.tries_pos.y, self.tries_pos.x1, self.tries_pos.y1))
            tries = int(tries_raw) if tries_raw != '' and tries_raw != None else None

            print(f'Tries: {tries}')
            if tries != None and tries >= 150:
                self.reset()
                break

            print(f"Color: {pyautogui.pixel(*position)}")
            # if pyautogui.pixel(*position) == self._success_color:
            if pyautogui.pixelMatchesColor(position[0], position[1], self._success_color, tolerance=10):
                if time() - start_time >= duration:
                    break
            else:
                start_time = time()
            sleep(0.1)

    def go_to_max(self):
        for i in range(20):
            pyautogui.click(self.btn_plus_pos[0], self.btn_plus_pos[1])

    def go_to_min(self, num):
        for i in range(num):
            pyautogui.click(self.btn_minus_pos[0], self.btn_minus_pos[1])

    def single_click(self, position, wait = 1.3):
        pyautogui.click(position[0], position[1])
        sleep(wait)

    def double_click(self, position, wait = 2):
        pyautogui.doubleClick(position[0], position[1])
        sleep(wait)

    def reset(self):
        pyautogui.click(self.btn_stop_pos[0], self.btn_stop_pos[1])
        # pyautogui.click(self.btn_start_pos[0], self.btn_start_pos[1])

    def run(self):
        print("Starting caster...")
        while self._running:
            status_raw = self.get_status()

            try:
                status = int(status_raw) if status_raw != '' and status_raw != None else None
                print(f"Status: {status}")

                if status == 20 or status == None:
                    print('Item is +20')
                    sleep(2)
                    self.double_click(self.upg_ces_pos)
                    self.double_click(self.upg_cess_pos)
                    sleep(2)
                    self.current_item_index = (self.current_item_index + 1) % len(self.items_pos)
                    x,y = self.items_pos[self.current_item_index]
                    self.double_click([x,y])
                    self.double_click(self.inv_ces_pos)
                elif status in [0, 1, 2, 3, 5, 9, 13, 'g', 'e']:
                    print('Item is +4 --')
                    self.go_to_max()
                    self.double_click(self.upg_cess_pos)
                    self.single_click(self.btn_start_pos)
                    self.single_click(self.btn_stop_pos)
                elif status in [6, 7, 10, 11, 14, 15, 17, 18, 19]:
                    print('Item is +6 --')
                    self.go_to_max()
                    self.double_click(self.inv_cess_pos)
                    self.single_click(self.btn_start_pos)
                    self.single_click(self.btn_stop_pos, 0)
                elif status in [4]:
                    print('Item is +4')
                    self.double_click(self.upg_cess_pos)
                    self.go_to_max()
                    self.go_to_min(14)
                    self.single_click(self.btn_start_pos)
                    self.wait_for_success(self.upg_status_pos, 2)
                    # self.single_click(self.btn_stop_pos)
                elif status in [8]:
                    print('Item is +8')
                    self.double_click(self.upg_cess_pos)
                    self.go_to_max()
                    self.go_to_min(10)
                    self.single_click(self.btn_start_pos)
                    self.wait_for_success(self.upg_status_pos, 2)
                    # self.single_click(self.btn_stop_pos)
                elif status in [12]:
                    print('Item is +12')
                    self.double_click(self.upg_cess_pos)
                    self.go_to_max()
                    self.go_to_min(6)
                    self.single_click(self.btn_start_pos)
                    self.wait_for_success(self.upg_status_pos, 2)
                    # self.single_click(self.btn_stop_pos)
                elif status in [16]:
                    print('Item is +16')
                    self.double_click(self.upg_cess_pos)
                    self.go_to_max()
                    self.go_to_min(2)
                    self.single_click(self.btn_start_pos)
                    self.wait_for_success(self.upg_status_pos, 2)
                    # self.single_click(self.btn_stop_pos)
                elif status in [20]:
                    print('Item is +20')
                    self.double_click(self.upg_cess_pos)
                    self.go_to_max()
                    self.go_to_min(2)
                    self.single_click(self.btn_start_pos)
                    self.single_click(self.btn_stop_pos, 0)
            except ValueError:
                print(f'Failed to recognize status. Status: {self.status}')

            sleep(0.1)

    def stop(self):
        self._running = False