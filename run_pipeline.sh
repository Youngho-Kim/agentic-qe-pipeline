#!/usr/bin/env bash
# 에러 발생 시 즉시 중단 설정
set -e

echo "============================================================"
echo "🏛️ [QE Modular Multi-Agent Pipeline] 5단계 자동화 가동"
echo "============================================================"

# Step 1
echo ""
echo "▶️ [Step 1/5] TC Designer Agent: 기획 분석 및 TC 설계 중..."
python step1_tc_designer.py

# Step 2
echo ""
echo "▶️ [Step 2/5] Quality Gate Agent: 품질 심사 및 실행 승인 중..."
python step2_quality_gate.py

# Step 3
echo ""
echo "▶️ [Step 3/5] Test Runner Agent: Playwright E2E 브라우저 실측 중..."
python step3_test_runner.py

# Step 4
echo ""
echo "▶️ [Step 4/5] Defect Triage Agent: 결함 원인 분석 및 트리아지 중..."
python step4_defect_triage.py

# Step 5
echo ""
echo "▶️ [Step 5/5] Release Commander Agent: 최종 릴리즈 판정 중..."
python step5_release_commander.py

echo ""
echo "============================================================"
echo "🎉 [완료] 5단계 모든 중간 보고서 생성이 성공적으로 끝났습니다!"
echo "📁 산출물 확인: artifacts/ 폴더"
echo "============================================================"