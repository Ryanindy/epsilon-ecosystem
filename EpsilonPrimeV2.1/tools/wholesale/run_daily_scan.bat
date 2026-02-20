@echo off
REM ============================================================================
REM Property Sourcing Agent - Daily Automation Launcher
REM Runs every morning at 6:00 AM
REM ============================================================================

echo ========================================
echo Property Sourcing Agent Starting...
echo Time: %date% %time%
echo ========================================

REM Change to project directory
cd /d "C:\Users\Media Server\Desktop\Wholesale_AI_Project\scripts"

REM Activate virtual environment if you have one
REM call ..\venv\Scripts\activate.bat

REM Run the property sourcing agent
python property_sourcing_agent.py

REM Log completion
echo.
echo ========================================
echo Property Sourcing Completed
echo Time: %date% %time%
echo ========================================

REM Keep window open if run manually (not from scheduler)
if "%1"=="" timeout /t 10

exit
