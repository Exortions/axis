import pyautogui
import base64
import uuid
import os

class Screenshotter:
    def execute(self):
        name = f'{uuid.uuid4()}.png'
        ss = pyautogui.screenshot()
        ss.save(name)

        with open(name, 'rb') as f:
            data = f'data:image/png;base64,{base64.b64encode(f.read()).decode("utf-8")}'
            
            return data, name

    def start(self):
        data, name = self.execute()
        os.remove(name)

        return data
