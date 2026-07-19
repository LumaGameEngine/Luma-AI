#!/bin/bash
echo "Termux worker setup for Luma AI"
pkg update && pkg upgrade -y
pkg install python cmake make clang git wget -y
pip install requests fastapi uvicorn
echo "Worker ready!"
