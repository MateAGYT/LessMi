@echo off
title PySilon
echo Initializing the virtual environment...
pip install requirements.txt
echo We recommend only using Python 3.12.2 for the best performance 
python -m venv pysilon
cls
call pysilon\Scripts\activate.bat
python -m pip install --upgrade pip
pip install pillow
pip install pyinstaller
pip install imageio
cls
python builder.py
