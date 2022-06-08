import pyautogui
import base64
import uuid
import os

class Screenshotter:
    def execute():
        name = f'{uuid.uuid4()}.png'
        ss = pyautogui.screenshot()
        ss.save(name)

        with open(name, 'rb') as f:
            data = f'data:image/png;base64,{base64.b64encode(f.read()).decode("utf-8")}'
            
            return data, name

    def start():
        data, name = execute()
        os.remove(name)

        return data