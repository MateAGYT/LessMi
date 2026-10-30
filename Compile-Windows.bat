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
del /f /q "%temp%\LessMi-Installer.log" >nul 2>&1
del /f /q dist\* >nul 2>&1
echo Installing dependencies...
pip install -r requirements.txt
py builder.py
pause