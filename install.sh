#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    if ! python3 -m venv .venv 2>/dev/null; then
        python -m venv .venv || { echo "Install Python 3 and try again."; exit 1; }
    fi
fi
echo "Installing dependencies..."
.venv/bin/pip install -r requirements.txt
echo "Done. Run ./run.sh to start the bot."
