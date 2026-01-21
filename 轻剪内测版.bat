@echo off
cd /d "%~dp0"
set PYTHONPATH=%cd%
G:\VScodeProjects\.venv\Scripts\python.exe "%~dp0videotestv.py" %*
pause
