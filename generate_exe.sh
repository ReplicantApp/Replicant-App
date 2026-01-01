#!/bin/bash
echo "Installing requirements..."
pip install -r requirements.txt
echo
echo "Starting Build Process..."
python build.py
echo
echo "Build finished! Your executable is in the 'dist' folder."
read -p "Press enter to continue"
