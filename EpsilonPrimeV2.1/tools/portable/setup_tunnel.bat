@echo off
:: Epsilon Portable Secure Tunnel Setup
:: Establishes a reverse SSH tunnel back to the Mainframe
:: Usage: setup_tunnel.bat [REMOTE_HOST] [REMOTE_USER] [REMOTE_PORT]

set REMOTE_HOST=%1
set REMOTE_USER=%2
set REMOTE_PORT=%3

if "%REMOTE_HOST%"=="" set REMOTE_HOST=192.168.1.100
if "%REMOTE_USER%"=="" set REMOTE_USER=epsilon
if "%REMOTE_PORT%"=="" set REMOTE_PORT=22

echo [EPSILON] Initializing Secure Tunnel Protocol...
echo [EPSILON] Target: %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PORT%

:: Check for SSH
where ssh >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] SSH client not found. Install OpenSSH or Git Bash.
    pause
    exit /b 1
)

:: Create Reverse Tunnel (R:8080 -> Local:5000)
:: Allows Mainframe to access Portable API running on port 5000
echo [EPSILON] Opening Reverse Tunnel (Remote:8080 -> Local:5000)...
ssh -N -R 8080:localhost:5000 %REMOTE_USER%@%REMOTE_HOST% -p %REMOTE_PORT%

if %errorlevel% neq 0 (
    echo [ERROR] Tunnel collapse. Check credentials or network.
    pause
)
