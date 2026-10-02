@echo off
title PySilon
echo Initializing the virtual environment...
python -m venv pysilon
cls
call pysilon\Scripts\activate.bat
python -m pip install --upgrade pip
pip install pillow
pip install pyinstaller
pip install imageio
cls
python builder.py
