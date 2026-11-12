@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ============================================================
echo [QE Modular Multi-Agent Pipeline] Starting Master Script...
echo ============================================================

python run_modular_qe_pipeline.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Pipeline failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [SUCCESS] All 5 steps completed! Check the artifacts/ folder.
pause