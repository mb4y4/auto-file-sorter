#!/bin/bash
set -e

PROJECT_DIR="/f/Coding/auto-file-sorter"
VENV_DIR="$PROJECT_DIR/venv"

cd "$PROJECT_DIR"

# Create virtual environment if not exists
if [ ! -d "$VENV_DIR" ]; then
    python -m venv "$VENV_DIR"
fi

# Activate venv (Windows Git Bash)
source "$VENV_DIR/Scripts/activate"

# Install dependencies
pip install -r requirements.txt

# Run sorter.py
if [ "$1" = "realtime" ]; then
    python sorter.py --mode realtime
else
    python sorter.py --mode once
fi
