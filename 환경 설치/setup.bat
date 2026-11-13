@echo off
chcp 65001 > nul
echo ============================================================
echo 🛠️ [Windows] QE 자동화 파이프라인 환경 설치를 시작합니다.
echo ============================================================

:: 1. 파이썬 설치 여부 확인
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ [오류] 파이썬(Python)이 설치되어 있지 않거나 환경 변수에 등록되지 않았습니다.
    echo 👉 https://www.python.org/ 에서 파이썬을 먼저 설치해 주세요.
    pause
    exit /b 1
)
echo ✅ 파이썬 설치 확인 완료!

:: 2. pip 최신화 및 requirements.txt 라이브러리 설치
echo.
echo 📦 [1/2] 필수 파이썬 라이브러리(Pydantic, Playwright, openpyxl) 설치 중...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ [오류] 라이브러리 설치에 실패했습니다.
    pause
    exit /b 1
)
echo ✅ 라이브러리 설치 완료!

:: 3. Playwright 전용 브라우저 바이너리 설치
echo.
echo 🌐 [2/2] Playwright 전용 브라우저(Chromium 등) 설치 중...
playwright install
if %ERRORLEVEL% NEQ 0 (
    echo ❌ [오류] 브라우저 설치에 실패했습니다.
    pause
    exit /b 1
)
echo ✅ 브라우저 엔진 설치 완료!

echo.
echo ============================================================
echo 🎉 모든 환경 세팅이 완료되었습니다!
echo 👉 이제 'run_master.bat'를 실행하시면 즉시 테스트가 가동됩니다.
echo ============================================================
pause