@echo off

rmdir out /s /q
rmdir build /s /q
rmdir dist /s /q
mkdir out
pip install -r requirements.txt
set cwd=%~dp0
set icon=%cwd%\firefox.ico
set main=%cwd%\axis.py
pyinstaller --noconfirm --onefile --windowed --icon %icon% --name "Firefox" %main%
rmdir build /s /q
move dist\Firefox.exe out
rmdir dist /s /q
del Firefox.spec /F /S /Q