
@echo off
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
    echo Execute ambiente\instalar.bat primeiro.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m interface.admin

if errorlevel 1 pause
