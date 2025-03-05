#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python word_start.py
read -p "Press Enter to exit..."