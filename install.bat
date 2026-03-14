@echo off
cd /d "%~dp0"
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed. Install Python or use: py -3 -m venv .venv
        pause
        exit /b 1
    )
)
echo Installing dependencies...
.venv\Scripts\pip install -r requirements.txt
if errorlevel 1 (
    pause
    exit /b 1
)
echo Done. Run run.bat to start the bot.
pause
