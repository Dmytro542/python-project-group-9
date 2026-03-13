@echo off
chcp 65001 >nul 2>&1

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

pip install -r requirements.txt --quiet 2>nul

cls
python address_book.py

pause
