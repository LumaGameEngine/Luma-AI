#!/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "Setting up Luma AI coordinator..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
echo "Done. Run './scripts/start.sh' to start the coordinator."
