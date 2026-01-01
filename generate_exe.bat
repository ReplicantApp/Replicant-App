@echo off
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Starting Build Process...
python build.py
echo.
echo Build finished! Your .exe is in the 'dist' folder.
pause
