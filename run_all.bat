@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ============================================================
echo [All-in-One QE Platform] Starting Unified Launcher...
echo ============================================================

python qe_launcher.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Launcher exited with an error.
    pause
    exit /b %ERRORLEVEL%
)
pause