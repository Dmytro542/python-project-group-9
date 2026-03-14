#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
else
    echo "Virtual environment not found. Run: python3 -m venv .venv"
    echo "Then: .venv/bin/pip install -r requirements.txt"
    exit 1
fi
exec python main.py
