import subprocess

class TerminalCommands:
    def start(self, command):
        try:
            return subprocess.check_output(command, shell=True).decode('utf-8')
        except:
            return None