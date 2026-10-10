@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8

rem --- pick an interpreter ---
set "PY="
where py >nul 2>nul
if not errorlevel 1 set "PY=py"
if not defined PY (
    where python >nul 2>nul
    if not errorlevel 1 set "PY=python"
)
if not defined PY (
    echo [!] Python not found. Install Python 3.10+ from python.org and enable "py launcher".
    pause
    exit /b 1
)

rem --- install deps only if missing ---
%PY% -c "import telebot, requests" >nul 2>nul
if errorlevel 1 (
    echo [*] Installing dependencies: pyTelegramBotAPI, requests ...
    %PY% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [!] pip install failed. Run manually: %PY% -m pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo [*] Starting bot... Close this window to stop it.
%PY% main.py

echo.
echo [*] Bot stopped.
pause
