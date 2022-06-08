rm -rf out
rm -rf build
rm -rf dist

mkdir out

pip install -r requirements.txt

icon="$PWD/firefox.ico"
main="$PWD/axis.py"

pyinstaller --noconfirm --onefile --windowed --icon "$ICON" --name "Firefox" "$MAIN"

mv dist/Firefox.exe out

rm -rf build
rm -rf dist
rm -rf Firefox.spec
