import PyInstaller.__main__
import sys

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--name=MultiBloxy',
    '--icon=NONE',
    '--distpath=./dist',
    '--buildpath=./build',
    '--specpath=./build',
])

print("\n✅ MultiBloxy.exe создан в папке 'dist/'")
print("Консоль будет скрыта при запуске!")
