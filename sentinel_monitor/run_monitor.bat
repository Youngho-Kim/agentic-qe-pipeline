@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ============================================================
echo [Sentinel-QE] Starting Service Health Monitoring Dashboard...
echo ============================================================

python sentinel_app.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to start Sentinel Monitor.
    pause
    exit /b %ERRORLEVEL%
)
pause