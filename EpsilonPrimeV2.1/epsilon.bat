@echo off
:: EPSILON PRIME V2.2 SOVEREIGN LAUNCHER
:: "Stronger Gates, Deeper Memory, Faster Hands"

set PROJECT_ROOT=C:\Users\Media Server\EpsilonPrimeV2.1
cd /d "%PROJECT_ROOT%"

:: 1. TRIGGER SOVEREIGN BOOT SEQUENCE
python boot/BOOT.py

:: 2. ARGUMENT ROUTING
if "%~1"=="--server" (
    :: Server is handled by BOOT.py auto-start, but allow manual foreground launch
    echo [!] MANUAL OVERRIDE: LAUNCHING API BRIDGE IN FOREGROUND...
    python main_server.py
    goto :eof
)

if "%~1"=="--sync" (
    echo [!] TRIGGERING GLOBAL SYNC...
    python tools\maintenance\daily_git_sync.py
    goto :eof
)

if "%~1"=="--backup" (
    echo [!] EXECUTING BACKUP PROTOCOL...
    python tools\maintenance\daily_backup.py
    goto :eof
)

:: 3. DEFAULT: DROP TO SOVEREIGN REPL
if "%~1"=="" (
    echo [Entering REPL Mode...]
    gemini repl
) else (
    :: Passthrough for direct commands
    gemini %*
)