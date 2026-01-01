import PyInstaller.__main__
import customtkinter
import os
import sys

# Get the location of customtkinter to include its assets
ctk_path = os.path.dirname(customtkinter.__file__)

# Determine separator based on OS (Windows uses ;, Unix uses :)
sep = ';' if os.name == 'nt' else ':'

print("Building Replicant.exe...")

PyInstaller.__main__.run([
    'src/main.py',
    '--name=Replicant',
    '--noconfirm',
    '--windowed',  # No console window
    f'--add-data={ctk_path}{sep}customtkinter',
    '--clean',
    # '--onefile', # Uncomment if you want a single .exe (slower startup)
])

print("Build complete. Check the 'dist' folder.")
