@echo off
title AI Voice Studio V0.5.0 - Mobile Controller
cd /d "%~dp0"
echo Starting mobile controller on port 8001...
echo Open the laptop IPv4 address from your phone:
echo http://LAPTOP-IP:8001/controller.html
python -m http.server 8001 --bind 0.0.0.0
pause
