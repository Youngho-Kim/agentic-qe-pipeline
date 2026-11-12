@echo off
chcp 65001 > nul
echo ============================================================
echo 🏛️ [QE Modular Multi-Agent Pipeline] 5단계 자동화 가동
echo ============================================================

echo.
echo ▶️ [Step 1/5] TC Designer Agent 가동 중...
python step1_tc_designer.py
if %ERRORLEVEL% NEQ 0 ( echo ❌ Step 1 실패 & pause & exit /b %ERRORLEVEL% )

echo.
echo ▶️ [Step 2/5] Quality Gate Agent 가동 중...
python step2_quality_gate.py
if %ERRORLEVEL% NEQ 0 ( echo ❌ Step 2 심사 탈락 & pause & exit /b %ERRORLEVEL% )

echo.
echo ▶️ [Step 3/5] Test Runner Agent 가동 중...
python step3_test_runner.py
if %ERRORLEVEL% NEQ 0 ( echo ❌ Step 3 실행 실패 & pause & exit /b %ERRORLEVEL% )

echo.
echo ▶️ [Step 4/5] Defect Triage Agent 가동 중...
python step4_defect_triage.py

echo.
echo ▶️ [Step 5/5] Release Commander Agent 가동 중...
python step5_release_commander.py

echo.
echo ============================================================
echo 🎉 [완료] 5단계 모든 보고서가 artifacts/ 폴더에 생성되었습니다!
echo ============================================================
pause