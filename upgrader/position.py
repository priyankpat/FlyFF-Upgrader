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
            'item_1_pos': Position('item_1_pos', 'Item Position 1'),
            'item_2_pos': Position('item_2_pos', 'Item Position 2'),
            'item_3_pos': Position('item_3_pos', 'Item Position 3'),
            'item_4_pos': Position('item_4_pos', 'Item Position 4'),
            'inventory_cess_pos': Position('inventory_cess_pos', 'Inventory Cess Position'),
            'inventory_ces_pos': Position('inventory_ces_pos', 'Inventory Cess Position'),
            'start_button_pos': Position('start_button_pos', 'Start Button Position'),
            'stop_button_pos': Position('stop_button_pos', 'Stop Button Position'),
            'reset_button_pos': Position('reset_button_pos', 'Reset Button Position'),
            'plus_button_pos': Position('plus_button_pos', 'Plus Button Position'),
            'minus_button_pos': Position('minus_button_pos', 'Minus Button Position'),
            'upgrade_ces_pos': Position('upgrade_ces_pos', 'Upgrade Ces Position'),
            'upgrade_cess_pos': Position('upgrade_cess_pos', 'Upgrade Cess Position'),
            'upgrade_status_pos': Position('upgrade_status_pos', 'Upgrade Status Position'),
            'update_number_start_pos': Position('update_number_start_pos', 'Update Number Start Position'),
            'update_number_end_pos': Position('update_number_end_pos', 'Update Number End Position'),
            'tries_number_start_pos': Position('tries_number_start_pos', 'Tries Number Start Position'),
            'tries_number_end_pos': Position('tries_number_end_pos', 'Tries Number End Position'),
        }
        self.positions = {}

    def run(self):
        print('Starting the recorder...')

        for key in self.prompts.keys():
            position = self.prompts[key]
            print(f'Select position for {position.description} and press ~')

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