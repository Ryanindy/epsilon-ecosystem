@echo off
:: EPSILON PRIME V3.0 SOVEREIGN LAUNCHER
:: Orchestrates the hardened boot sequence via PowerShell.

set PROJECT_ROOT=%~dp0
cd /d "%PROJECT_ROOT%"

:: Launch the hardened PowerShell boot sequence
:: ExecutionPolicy Bypass is required to run unsigned local scripts.
powershell -ExecutionPolicy Bypass -File epsilon_start.ps1 %*
