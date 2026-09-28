@echo off
cd /d "%~dp0"
py -c "import flask" >nul 2>&1
if errorlevel 1 py -m pip install -r requirements.txt
py backend\app.py
pause
