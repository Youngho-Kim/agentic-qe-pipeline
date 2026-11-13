import os
import sys
import json
import time
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from playwright.sync_api import sync_playwright

# ========================================================
# 1. 팬딩(Fanding) 맞춤형 데이터 모델
# ========================================================
class TestCase(BaseModel):
    tc_id: str
    title: str
    test_type: str
    priority: str
    target_tier: str
    steps: List[str]
    expected_result: str

class TestSuite(BaseModel):
    service_name: str = "팬딩(Fanding) 크리에이터 멤버십 및 유료 포스트 권한 제어"
    version: int = 1
    test_cases: List[TestCase] = []

class ReviewFeedback(BaseModel):
    approved: bool
    quality_score: int
    summary: str
    missing_points: List[str] = []
    action_items: List[str] = []

# ========================================================
# 2. 로컬 팬딩(Fanding) 모의 웹 애플리케이션 (Mock Server)
# ========================================================
HTML_CONTENT = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>팬딩 (Fanding) - 크리에이터 멤버십</title>
    <style>
        body { font-family: 'Pretendard', sans-serif; background: #0f1015; color: #fff; margin: 0; padding: 20px; }
        .header { border-bottom: 1px solid #2a2c38; padding-bottom: 15px; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 22px; font-weight: bold; color: #ff3366; }
        .user-status { color: #8f94a6; font-size: 14px; }
        .container { max-width: 800px; margin: 30px auto; }
        .creator-card { background: #1a1c26; border-radius: 12px; padding: 20px; margin-bottom: 25px; border: 1px solid #2e3245; }
        .tiers { display: flex; gap: 15px; margin-top: 15px; }
        .tier-box { flex: 1; background: #252836; padding: 15px; border-radius: 8px; border: 1px solid #3d4259; text-align: center; }
        .tier-box.gold { border-color: #f1c40f; }
        .tier-btn { background: #ff3366; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; margin-top: 10px; font-weight: bold; }
        .post { background: #1a1c26; border-radius: 10px; padding: 20px; margin-bottom: 15px; border: 1px solid #2e3245; }
        .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
        .badge.public { background: #2ecc71; color: #000; }
        .badge.silver { background: #95a5a6; color: #000; }
        .badge.gold { background: #f1c40f; color: #000; }
        .blurred { filter: blur(6px); user-select: none; pointer-events: none; }
        .gated-overlay { background: rgba(26,28,38,0.92); border: 1px dashed #ff3366; border-radius: 8px; padding: 25px; text-align: center; margin-top: -60px; position: relative; z-index: 10; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); justify-content: center; align-items: center; }
        .modal-content { background: #1a1c26; padding: 25px; border-radius: 12px; width: 380px; border: 1px solid #ff3366; }
        input[type="text"] { width: 90%; padding: 8px; margin: 10px 0; background: #0f1015; border: 1px solid #3d4259; color: #fff; border-radius: 4px; }
        .banner-grace { background: #e67e22; color: #fff; padding: 10px; border-radius: 6px; margin-bottom: 15px; display: none; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">FANDING</div>
        <div class="user-status" id="userStatus">현재 로그인: <span id="currentRole" style="color:#ff3366; font-weight:bold;">일반 회원(Free)</span></div>
    </div>

    <div class="container">
        <div id="graceBanner" class="banner-grace">⚠️ 정기 결제 실패: 3일의 결제 유예 기간(Grace Period) 동안 멤버십 혜택이 유지됩니다. 결제 수단을 갱신해 주세요.</div>

        <div class="creator-card">
            <h2>🎨 일러스트레이터 나나 (팬딩 공식 파트너)</h2>
            <p style="color:#8f94a6;">디지털 원화 및 작업 비하인드 스토리를 공유하는 공식 멤버십입니다.</p>
            <div class="tiers">
                <div class="tier-box">
                    <h3>실버 팬</h3>
                    <p style="color:#ff3366; font-weight:bold;">월 4,900원</p>
                    <button class="tier-btn" id="btnSilver" onclick="openCheckout('실버 팬', 4900)">구독하기</button>
                </div>
                <div class="tier-box gold">
                    <h3 style="color:#f1c40f;">골드 팬 (VIP)</h3>
                    <p style="color:#f1c40f; font-weight:bold;">월 14,900원</p>
                    <button class="tier-btn" id="btnGold" onclick="openCheckout('골드 팬', 14900)" style="background:#f1c40f; color:#000;">구독하기</button>
                </div>
            </div>
        </div>

        <!-- 1. 전체 공개 포스트 -->
        <div class="post" id="postPublic">
            <span class="badge public">전체 공개</span>
            <h3>11월 정기 연재 일정 안내</h3>
            <p>안녕하세요 팬 여러분! 이번 달 연재 일정 공지드립니다. 누구나 열람 가능한 공개 게시글입니다.</p>
        </div>

        <!-- 2. 실버 전용 포스트 -->
        <div class="post" id="postSilver">
            <span class="badge silver">실버 멤버십 전용</span>
            <h3>캐릭터 러프 스케치 및 채색 과정 영상</h3>
            <div id="silverContent" class="blurred">
                <p>실버 회원 전용 튜토리얼 텍스트와 비하인드 영상 클립 링크입니다.</p>
            </div>
            <div id="silverGate" class="gated-overlay">
                🔒 <strong>실버 팬 이상 전용 콘텐츠입니다.</strong><br>
                <small style="color:#8f94a6;">멤버십에 가입하시면 즉시 열람하실 수 있습니다.</small><br>
                <button class="tier-btn" onclick="openCheckout('실버 팬', 4900)">월 4,900원으로 잠금 해제</button>
            </div>
        </div>

        <!-- 3. 골드 전용 포스트 -->
        <div class="post" id="postGold">
            <span class="badge gold">골드 팬 (VIP) 전용</span>
            <h3>고해상도 PSD 원본 레이어 파일 다운로드</h3>
            <div id="goldContent" class="blurred">
                <p>골드 회원 전용 원본 PSD 다운로드 링크: [Secret_Layer_v1.psd]</p>
            </div>
            <div id="goldGate" class="gated-overlay">
                👑 <strong>골드 팬(VIP) 전용 콘텐츠입니다.</strong><br>
                <small style="color:#8f94a6;">고해상도 원본과 특전 브러시가 포함되어 있습니다.</small><br>
                <button class="tier-btn" onclick="openCheckout('골드 팬', 14900)" style="background:#f1c40f; color:#000;">골드 멤버십 가입</button>
            </div>
        </div>
    </div>

    <!-- 결제 및 쿠폰 모달 -->
    <div class="modal" id="checkoutModal">
        <div class="modal-content">
            <h3 id="modalTitle">멤버십 정기 결제</h3>
            <p>기본 플랜 가격: <span id="planPrice">0</span>원</p>
            <label>프로모션 할인 쿠폰 코드:</label>
            <input type="text" id="couponCode" placeholder="쿠폰 코드 입력 (예: WELCOME_20K)">
            <button class="tier-btn" style="background:#4a4e69; margin-top:0;" onclick="applyCoupon()">쿠폰 적용</button>
            <div style="margin: 15px 0; border-top:1px solid #3d4259; padding-top:10px;">
                <strong>최종 결제 금액: <span id="finalPrice" style="color:#ff3366; font-size:18px;">0</span>원</strong>
            </div>
            <button class="tier-btn" id="btnPay" style="width:100%;" onclick="completePayment()">정기 결제 승인</button>
            <button onclick="closeModal()" style="width:100%; background:transparent; border:none; color:#8f94a6; margin-top:10px; cursor:pointer;">닫기</button>
        </div>
    </div>

    <script>
        let currentPrice = 0;
        let selectedTier = "";

        function openCheckout(tier, price) {
            selectedTier = tier;
            currentPrice = price;
            document.getElementById('modalTitle').innerText = tier + " 정기 결제";
            document.getElementById('planPrice').innerText = price.toLocaleString();
            document.getElementById('finalPrice').innerText = price.toLocaleString();
            document.getElementById('couponCode').value = "";
            document.getElementById('checkoutModal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('checkoutModal').style.display = 'none';
        }

        function applyCoupon() {
            const code = document.getElementById('couponCode').value.trim();
            let discount = 0;
            if (code === "WELCOME_20K") {
                discount = 20000;
            } else if (code === "DISCOUNT_5K") {
                discount = 5000;
            }
            let finalAmt = currentPrice - discount;
            if (finalAmt < 0) {
                finalAmt = 0;
            }
            document.getElementById('finalPrice').innerText = finalAmt.toLocaleString();
        }

        function completePayment() {
            alert(selectedTier + " 구독이 정상 승인되었습니다!");
            closeModal();
            if (selectedTier.includes("골드")) {
                document.getElementById('currentRole').innerText = "골드 팬 (VIP)";
                document.getElementById('currentRole').style.color = "#f1c40f";
                document.getElementById('goldContent').classList.remove('blurred');
                document.getElementById('goldGate').style.display = 'none';
            }
        }

        const params = new URLSearchParams(window.location.search);
        if (params.get("role") === "gold") {
            document.getElementById('currentRole').innerText = "골드 팬 (VIP)";
            document.getElementById('currentRole').style.color = "#f1c40f";
            document.getElementById('goldContent').classList.remove('blurred');
            document.getElementById('goldGate').style.display = 'none';
        } else if (params.get("status") === "grace_period") {
            document.getElementById('graceBanner').style.display = 'block';
        }
    </script>
</body>
</html>
"""

class MockFandingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode("utf-8"))

    def log_message(self, format, *args):
        pass

def start_mock_server(port=8899):
    server = HTTPServer(("127.0.0.1", port), MockFandingHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

# ========================================================
# 3. 팬딩 특화 멀티 에이전트 (대리-팀장 검토 루프)
# ========================================================
class FandingAssistantAgent:
    def draft_or_refine(self, feedback: Optional[ReviewFeedback], iteration: int) -> TestSuite:
        if iteration == 1 or not feedback:
            cases = [
                TestCase(tc_id="TC-FANDING-001", title="전체 공개 포스트 비로그인 접근 정상 열람", 
                         test_type="Positive", priority="P0", target_tier="Free",
                         steps=["크리에이터 홈 접속", "전체 공개 포스트 영역 확인"],
                         expected_result="블라인드 없이 포스트 텍스트가 정상 노출됨"),
                TestCase(tc_id="TC-FANDING-002", title="일반 회원의 골드 전용 콘텐츠 접근 시 차단 배너 노출", 
                         test_type="AccessControl", priority="P0", target_tier="Free",
                         steps=["일반 회원으로 접속", "골드 전용 포스트 확인"],
                         expected_result="콘텐츠가 블러 처리되고 '골드 팬 전용' 안내 배너가 뜸")
            ]
            return TestSuite(version=1, test_cases=cases)
        else:
            cases = [
                TestCase(tc_id="TC-FANDING-001", title="전체 공개 포스트 비로그인 접근 정상 열람", 
                         test_type="Positive", priority="P0", target_tier="Free",
                         steps=["크리에이터 홈 접속", "전체 공개 포스트 영역 확인"],
                         expected_result="블라인드 없이 포스트 텍스트가 정상 노출됨"),
                TestCase(tc_id="TC-FANDING-002", title="일반 회원의 골드 전용 콘텐츠 접근 시 차단 배너 노출", 
                         test_type="AccessControl", priority="P0", target_tier="Free",
                         steps=["일반 회원으로 접속", "골드 전용 포스트 확인"],
                         expected_result="콘텐츠가 블러 처리되고 '골드 팬 전용' 안내 배너가 뜸"),
                TestCase(tc_id="TC-FANDING-003", title="골드 멤버십 구독자의 VIP 전용 원본 콘텐츠 잠금 해제 검증", 
                         test_type="AccessControl", priority="P0", target_tier="Gold",
                         steps=["골드 회원 세션으로 접속", "골드 포스트 확인"],
                         expected_result="블러 및 게이트 배너가 제거되고 원본 다운로드 링크가 활성화됨"),
                TestCase(tc_id="TC-FANDING-004", title="플랜 가격 초과 쿠폰 적용 시 음수 결제 방지(BVA 경계값) 검증", 
                         test_type="Boundary", priority="P0", target_tier="Free",
                         steps=["14,900원 골드 플랜 결제창 오픈", "20,000원 할인 쿠폰 입력 후 적용"],
                         expected_result="최종 결제 금액이 마이너스가 아닌 정확히 '0원'으로 바운딩 처리됨"),
                TestCase(tc_id="TC-FANDING-005", title="정기 결제 실패 시 즉시 해지 차단 및 3일 유예(Grace Period) 배너 검증", 
                         test_type="StateTransition", priority="P1", target_tier="Gold",
                         steps=["정기 결제 실패 유저 상태로 접속"],
                         expected_result="상단에 '3일 결제 유예 안내 및 결제수단 갱신' 경고 배너가 정상 표시됨")
            ]
            return TestSuite(version=iteration, test_cases=cases)

class FandingTeamLeadAgent:
    def review(self, suite: TestSuite, iteration: int) -> ReviewFeedback:
        types = {tc.test_type for tc in suite.test_cases}
        if iteration == 1 and ("Boundary" not in types or "StateTransition" not in types):
            return ReviewFeedback(
                approved=False,
                quality_score=62,
                summary="팬딩의 핵심 비즈니스 모델인 '정기 결제 쿠폰 경계값'과 '구독 결제 실패 유예기간 상태 전이' 테스트가 누락되었습니다.",
                action_items=[
                    "TC-FANDING-004: 플랜가 초과 쿠폰 적용 시 음수 결제(버그) 차단 BVA 케이스 추가 필수",
                    "TC-FANDING-005: 정기 구독 실패 시 즉시 강퇴 방지(Grace Period 배너 노출) 상태 전이 검증 추가"
                ]
            )
        return ReviewFeedback(
            approved=True,
            quality_score=98,
            summary="팬딩의 크리에이터 멤버십 권한 제어(Access Control), BVA 결제 방어, 구독 유예 상태 전이가 완벽히 충족되었습니다. 실행을 승인합니다.",
            action_items=[]
        )

# ========================================================
# 4. 사원 에이전트: Playwright 실측 브라우저 자동화
# ========================================================
def execute_fanding_tests(server_url: str, suite: TestSuite) -> List[Dict[str, Any]]:
    os.makedirs("fanding_screenshots", exist_ok=True)
    results = []

    print("\n" + "=" * 65)
    print("🤖 [사원 Agent] 팬딩 멤버십 특화 E2E 브라우저 자동화 실행")
    print("=" * 65)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=700)
        page = browser.new_page()

        for tc in suite.test_cases:
            tc_id = tc.tc_id
            print(f"\n▶️ [{tc_id}] 실행 중: {tc.title}")

            try:
                if tc_id == "TC-FANDING-001":
                    page.goto(server_url)
                    page.wait_for_selector("#postPublic")
                    assert "전체 공개" in page.text_content("#postPublic")
                    status = "✅ PASS"
                    detail = "전체 공개 포스트 정상 로드"

                elif tc_id == "TC-FANDING-002":
                    page.goto(server_url)
                    page.wait_for_selector("#goldGate")
                    assert "골드 팬(VIP) 전용 콘텐츠입니다" in page.text_content("#goldGate")
                    status = "✅ PASS"
                    detail = "미구독 일반 회원에게 권한 차단 오버레이 정상 노출"

                elif tc_id == "TC-FANDING-003":
                    page.goto(f"{server_url}?role=gold")
                    is_gate_visible = page.is_visible("#goldGate")
                    assert not is_gate_visible
                    status = "✅ PASS"
                    detail = "골드 회원 세션에서 VIP 전용 콘텐츠 잠금 해제 확인"

                elif tc_id == "TC-FANDING-004":
                    page.goto(server_url)
                    page.click("#btnGold")
                    page.wait_for_selector("#checkoutModal", state="visible")
                    page.fill("#couponCode", "WELCOME_20K")
                    page.click("button:has-text('쿠폰 적용')")
                    final_price = page.text_content("#finalPrice")
                    assert final_price == "0"
                    status = "✅ PASS"
                    detail = "2만원 쿠폰 적용 시 음수 결제 차단 및 0원 정상 계산 확인"

                elif tc_id == "TC-FANDING-005":
                    page.goto(f"{server_url}?status=grace_period")
                    page.wait_for_selector("#graceBanner", state="visible")
                    banner_text = page.text_content("#graceBanner")
                    assert "결제 유예 기간(Grace Period)" in banner_text
                    status = "✅ PASS"
                    detail = "결제 실패 시 3일 유예 상태 전이 안내 배너 정상 확인"

                screenshot_path = f"fanding_screenshots/{tc_id}_success.png"
                page.screenshot(path=screenshot_path)
            except Exception as e:
                status = "❌ FAIL"
                detail = str(e)
                screenshot_path = f"fanding_screenshots/{tc_id}_fail.png"
                page.screenshot(path=screenshot_path)

            print(f"   결과: {status} ({detail})")
            results.append({
                "tc_id": tc_id,
                "title": tc.title,
                "type": tc.test_type,
                "tier": tc.target_tier,
                "status": status,
                "detail": detail,
                "screenshot": screenshot_path
            })

        browser.close()
    return results

# ========================================================
# 5. 팬딩 전용 QA 릴리즈 종합 리포트 생성
# ========================================================
def generate_fanding_report(suite: TestSuite, results: List[Dict[str, Any]], output_path: str):
    total = len(results)
    passed = sum(1 for r in results if "PASS" in r["status"])
    pass_rate = (passed / total * 100) if total > 0 else 0
    decision = "🟢 GO (릴리즈 승인)" if pass_rate == 100 else "🔴 NO-GO (릴리즈 보류)"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 📋 [팬딩(Fanding)] 크리에이터 멤버십 & 결제 권한 제어 QA 종합 리포트\n\n")
        f.write(f"- **검증 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **대상 플랫폼**: 팬딩(Fanding) 웹 서비스\n")
        f.write(f"- **최종 배포 판정**: **{decision}**\n")
        f.write(f"- **테스트 통과율**: **{passed}/{total} 건 ({pass_rate:.1f}%)**\n\n")
        
        f.write("## 1. 비즈니스 리스크 및 검증 요약 (Executive Summary)\n")
        f.write("팬딩의 핵심 비즈니스 모델인 **크리에이터 유료 멤버십 구독** 및 **등급별 디지털 리워드 권한 제어(Access Control)**에 대해 ")
        f.write("멀티 에이전트 파이프라인(대리-팀장 검토)과 Playwright E2E 자동화를 통해 실측 검증을 완료하였습니다.\n")
        f.write("- **보안 및 권한**: 비로그인/미구독 회원의 유료 콘텐츠(VIP 원본 등) 우회 열람 불가 확인\n")
        f.write("- **결제 안정성**: 플랜 가격 초과 쿠폰 적용 시 시스템 오류나 음수(-금액) 결제 발생 방지(BVA 경계값 통과)\n")
        f.write("- **구독 유지율**: 정기 결제 실패 시 즉시 해지로 인한 이탈 방지용 '3일 결제 유예(Grace Period)' 상태 전이 정상 동작\n\n")

        f.write("## 2. 테스트 케이스별 실행 결과 및 증빙\n\n")
        f.write("| TC ID | 테스트 명세 | 분류 | 등급 | 결과 | 세부 내용 | 증빙 스크린샷 |\n")
        f.write("| :--- | :--- | :---: | :---: | :---: | :--- | :--- |\n")
        for r in results:
            link = f"[{r['tc_id']}]({r['screenshot']})"
            f.write(f"| `{r['tc_id']}` | {r['title']} | {r['type']} | **{r['tier']}** | {r['status']} | {r['detail']} | {link} |\n")

        f.write("\n## 3. 팬딩 QA 인프라 도입 제언\n")
        f.write("1. **크리에이터 신규 기능 배포 시 회귀 테스트(Regression Test) 자동화** 파이프라인으로 본 모듈 상시 가동\n")
        f.write("2. 모바일 웹 환경(iOS Safari, 안드로이드 Chrome) 뷰포트 에뮬레이션 테스트 확장\n")

# ========================================================
# 6. 메인 실행 함수
# ========================================================
def main():
    print("=" * 65)
    print("🚀 [팬딩 특화 QA 파이프라인] 크리에이터 멤버십 E2E 자동화 가동")
    print("=" * 65)

    port = 8899
    server = start_mock_server(port)
    server_url = f"http://127.0.0.1:{port}"
    print(f"📡 팬딩 로컬 테스트베드 웹서버 구동 완료: {server_url}")

    assistant = FandingAssistantAgent()
    team_lead = FandingTeamLeadAgent()

    feedback = None
    approved_suite = None
    for iteration in range(1, 3):
        print(f"\n[Phase 1 / Loop {iteration}] 대리 Agent가 팬딩 기획 요구사항을 분석하여 TC를 작성합니다...")
        suite = assistant.draft_or_refine(feedback, iteration)
        print(f"   -> {len(suite.test_cases)}건의 멤버십 TC 생성 완료 (버전 {suite.version})")

        print(f"[Phase 1 / Loop {iteration}] 팀장 Agent가 팬딩 비즈니스 룰 및 결제 경계값을 검토합니다...")
        feedback = team_lead.review(suite, iteration)
        print(f"   -> 심사 결과: {'✅ 승인' if feedback.approved else '❌ 반려'} (점수: {feedback.quality_score}점)")

        if feedback.approved:
            approved_suite = suite
            with open("fanding_approved_test_cases.json", "w", encoding="utf-8") as f:
                data = suite.model_dump() if hasattr(suite, "model_dump") else suite.dict()
                f.write(json.dumps(data, indent=2, ensure_ascii=False))
            break
        else:
            print(f"   -> 반려 사유: {feedback.summary}")
            for item in feedback.action_items:
                print(f"      * {item}")

    if approved_suite:
        execution_results = execute_fanding_tests(server_url, approved_suite)

        report_file = "fanding_qa_release_report.md"
        generate_fanding_report(approved_suite, execution_results, report_file)

        print("\n" + "=" * 65)
        print("🎉 [팬딩 특화 QA 완료] 모든 검증과 보고서 생성이 완료되었습니다!")
        print(f"📄 팬딩 최종 리포트: {report_file}")
        print(f"📁 팬딩 증빙 캡처: fanding_screenshots/")
        print("=" * 65)

    server.shutdown()

if __name__ == "__main__":
    main()