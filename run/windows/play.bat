@echo off
setlocal enabledelayedexpansion

:: Get the current directory
set "CURRENT_DIR=%cd%"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    :: Python is installed
    for /f "tokens=2 delims= " %%i in ('python --version') do set pyversion=%%i
    
    :: Check Python version
    if "!pyversion!" geq "3.12.4" (
        echo =^> Python !pyversion! is already installed.
    ) else (
        echo =^> Updating Python to version 3.12.4... This can take a little time!
        :: Download and install Python 3.12.4
        powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe', 'python-3.12.4-amd64.exe')"
        python-3.12.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
        del python-3.12.4-amd64.exe
        
        :: Remove old path and add new one
        setx PATH "%PATH:Python;=%"
        setx PATH "%PATH%;C:\Program Files\Python312"
    )
) else (
    :: Python is not installed
    echo =^> Installing Python 3.12.4... This can take a little time!
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe', 'python-3.12.4-amd64.exe')"
    python-3.12.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-3.12.4-amd64.exe
)

:: Move up two levels in the folder structure
cd /d "%CURRENT_DIR%\..\..\"

:: Check pip version
for /f "tokens=2 delims= " %%v in ('python -m pip --version') do set pipversion=%%v

:: Update pip if necessary
python -m pip install --upgrade pip

:: Install pygame if not already installed
python -c "import pygame" 2>nul
if %errorlevel% neq 0 (
    echo =^> Installing pygame...
    python -m pip install pygame
)

:: Add Python to the PATH for the current session
set "PATH=C:\Program Files\Python312;%PATH%"

:: Run the Python file in PowerShell
echo =^> Launching Python file...
powershell -Command "python main.py"

endlocal

cmd /k
