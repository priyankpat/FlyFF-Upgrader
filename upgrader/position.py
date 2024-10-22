import json
import threading
import keyboard
import pyautogui

from upgrader.types import Position

class PositionsRecorder(threading.Thread):
    def __init__(self):
        super().__init__()
        self._running = True
        self.index = 0
        self.prompts = {
            'inventory_cess_pos': Position('inventory_cess_pos'),
            'inventory_ces_pos': Position('inventory_ces_pos'),
            'start_button_pos': Position('start_button_pos'),
            'stop_button_pos': Position('stop_button_pos'),
            'reset_button_pos': Position('reset_button_pos'),
            'plus_button_pos': Position('plus_button_pos'),
            'minus_button_pos': Position('minus_button_pos'),
            'upgrade_ces_pos': Position('upgrade_ces_pos'),
            'upgrade_cess_pos': Position('upgrade_cess_pos'),
            'upgrade_status_pos': Position('upgrade_status_pos'),
            'update_number_start_pos': Position('update_number_start_pos'),
            'update_number_end_pos': Position('update_number_end_pos'),
            'tries_number_start_pos': Position('tries_number_start_pos'),
            'tries_number_end_pos': Position('tries_number_end_pos'),
        }
        self.positions = {}

    def run(self):
        print('Starting the recorder...')

        for key in self.prompts.keys():
            position = self.prompts[key]
            print(f'Select position for {key} and press ~')

            keyboard.wait('~')
            if keyboard.is_pressed('~'):
                mouse_position = pyautogui.position()
                position.set_position(mouse_position.x, mouse_position.y)
                print(position.key, position.x, position.y)

                self.positions[key] = position

        self.save_settings()
        self.stop()
        return

    def save_settings(self):
        with open("sample.json", "w") as outfile:
            positions_dict = {key: pos.to_dict() for key, pos in self.positions.items()}
            json.dump(positions_dict, outfile, indent=4)

        print('Settings saved.')

    def stop(self):
        self._running = False