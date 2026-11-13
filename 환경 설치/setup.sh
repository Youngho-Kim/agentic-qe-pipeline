#!/usr/bin/env bash
# 에러 발생 시 즉시 중단
set -e

echo "============================================================"
echo "🛠️ [macOS/Linux] QE 자동화 파이프라인 환경 설치를 시작합니다."
echo "============================================================"

# 1. 파이썬 설치 확인 (python3 명령어 체크)
if ! command -v python3 &> /dev/null; then
    echo "❌ [오류] python3 명령어를 찾을 수 없습니다."
    echo "👉 Homebrew나 python.org를 통해 파이썬을 먼저 설치해 주세요."
    exit 1
fi

echo "✅ 파이썬 설치 확인 완료: $(python3 --version)"

# 2. pip 최신화 및 requirements.txt 라이브러리 설치
echo ""
echo "📦 [1/2] 필수 파이썬 라이브러리(Pydantic, Playwright, openpyxl) 설치 중..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# 3. Playwright 브라우저 엔진 설치
echo ""
echo "🌐 [2/2] Playwright 전용 브라우저(Chromium) 설치 중..."
python3 -m playwright install

echo ""
echo "============================================================"
echo "🎉 모든 환경 세팅이 완료되었습니다!"
echo "👉 이제 'bash run_master.sh'를 실행하시면 즉시 테스트가 가동됩니다."
echo "============================================================"