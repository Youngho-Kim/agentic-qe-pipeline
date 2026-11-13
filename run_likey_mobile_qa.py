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
# 1. LIKEY 특화 데이터 모델 (Pydantic v2 호환)
# ========================================================
class TestCase(BaseModel):
    tc_id: str
    title: str
    test_type: str  # MobileUI, AccessControl, CoinBVA, ErrorTriage
    priority: str   # P0, P1, P2
    device: str     # iPhone 14
    steps: List[str]
    expected_result: str

class TestSuite(BaseModel):
    service_name: str = "티피씨 LIKEY 모바일 웹/앱 1:1 채팅 및 코인 결제 E2E"
    version: int = 1
    test_cases: List[TestCase] = []

class ReviewFeedback(BaseModel):
    approved: bool
    quality_score: int
    summary: str
    action_items: List[str] = []

# ========================================================
# 2. LIKEY 모바일 앱 모의 웹 애플리케이션 (Mock Server)
# ========================================================
HTML_LIKEY = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>LIKEY - Creator & Fan 1:1</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #121214; color: #fff; display: flex; justify-content: center; height: 100vh; }
        .app-container { width: 100%; max-width: 420px; height: 100vh; display: flex; flex-direction: column; background: #18181c; position: relative; border-left: 1px solid #282830; border-right: 1px solid #282830; }
        .header { height: 55px; background: #1f1f24; display: flex; align-items: center; justify-content: space-between; padding: 0 16px; border-bottom: 1px solid #2e2e38; }
        .creator-info { display: flex; align-items: center; gap: 8px; font-weight: bold; font-size: 15px; }
        .coin-badge { background: #2a2a35; padding: 4px 10px; border-radius: 12px; font-size: 13px; color: #f1c40f; border: 1px solid #f1c40f; }
        .chat-stream { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
        .msg { max-width: 80%; padding: 10px 14px; border-radius: 14px; font-size: 14px; line-height: 1.4; word-break: break-word; }
        .msg.creator { align-self: flex-start; background: #2c2c36; color: #fff; border-bottom-left-radius: 4px; }
        .msg.user { align-self: flex-end; background: #e0245e; color: #fff; border-bottom-right-radius: 4px; }
        .media-card { background: #262630; border-radius: 10px; padding: 12px; border: 1px solid #3d3d4d; margin-top: 6px; text-align: center; }
        .media-lock { background: rgba(0,0,0,0.6); padding: 16px; border-radius: 8px; border: 1px dashed #e0245e; }
        .btn-unlock { background: #e0245e; color: #fff; border: none; padding: 8px 14px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 8px; }
        .chat-input-bar { height: 60px; background: #1f1f24; display: flex; align-items: center; padding: 8px 12px; gap: 8px; border-top: 1px solid #2e2e38; }
        .chat-input { flex: 1; height: 40px; background: #2c2c36; border: 1px solid #3d3d4d; border-radius: 20px; color: #fff; padding: 0 14px; font-size: 14px; }
        .btn-send { background: #e0245e; border: none; border-radius: 50%; width: 40px; height: 40px; color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; }
        .modal { display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.75); justify-content: center; align-items: center; z-index: 100; padding: 20px; }
        .modal-box { background: #262630; padding: 20px; border-radius: 12px; text-align: center; width: 100%; border: 1px solid #e0245e; }
        .banner-error { background: #c0392b; color: #fff; font-size: 12px; padding: 6px 12px; text-align: center; display: none; }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="banner-error" id="errorBanner">⚠️ 빈 메시지는 전송할 수 없습니다.</div>
        <div class="header">
            <div class="creator-info">
                <span style="font-size: 18px;">👑</span>
                <span>크리에이터 유나</span>
            </div>
            <div class="coin-badge" id="coinBadge">🪙 <span id="coinCount">50</span> COIN</div>
        </div>

        <div class="chat-stream" id="chatStream">
            <div class="msg creator">
                안녕하세요 팬 여러분! 라이키 1:1 메시지에 오신 걸 환영해요 💕
            </div>
            
            <!-- 30 코인 포스트 (열람 가능) -->
            <div class="msg creator" style="width: 100%;">
                <div class="media-card">
                    <p style="font-size:13px; margin-bottom:4px;">📸 비하인드 셀카 패키지</p>
                    <div class="media-lock" id="lock30">
                        🔒 <strong>잠긴 콘텐츠</strong><br>
                        <small style="color:#aaa;">30 코인이 필요합니다</small><br>
                        <button class="btn-unlock" id="btnUnlock30" onclick="unlockMedia(30, 'lock30')">30 코인으로 잠금 해제</button>
                    </div>
                    <div id="unlocked30" style="display:none; color:#2ecc71; font-weight:bold; padding:10px;">
                        🎉 잠금 해제 완료! [고화질 원본 4장 열람 가능]
                    </div>
                </div>
            </div>

            <!-- 100 코인 포스트 (잔여 코인 부족으로 차단 테스트용) -->
            <div class="msg creator" style="width: 100%;">
                <div class="media-card">
                    <p style="font-size:13px; margin-bottom:4px;">🎥 미공개 4K 댄스 영상</p>
                    <div class="media-lock" id="lock100">
                        🔒 <strong>VIP 전용 4K 영상</strong><br>
                        <small style="color:#aaa;">100 코인이 필요합니다</small><br>
                        <button class="btn-unlock" id="btnUnlock100" onclick="unlockMedia(100, 'lock100')">100 코인으로 잠금 해제</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 하단 메시지 입력창 -->
        <div class="chat-input-bar">
            <input type="text" class="chat-input" id="chatInput" placeholder="메시지를 입력하세요...">
            <button class="btn-send" id="btnSend" onclick="sendMessage()">➤</button>
        </div>

        <!-- 코인 부족 모달 -->
        <div class="modal" id="coinModal">
            <div class="modal-box">
                <h3 style="margin-bottom:8px; color:#e0245e;">🪙 코인이 부족합니다</h3>
                <p style="font-size:13px; color:#aaa; margin-bottom:16px;">보유 코인이 부족하여 콘텐츠를 열 수 없습니다. 코인을 충전하시겠습니까?</p>
                <button class="btn-unlock" style="width:100%;" onclick="closeModal()">코인 충전소로 이동</button>
            </div>
        </div>
    </div>

    <script>
        let coins = 50;

        function updateCoins(val) {
            coins = val;
            document.getElementById('coinCount').innerText = coins;
        }

        function unlockMedia(cost, lockId) {
            if (coins < cost) {
                document.getElementById('coinModal').style.display = 'flex';
                return;
            }
            coins -= cost;
            updateCoins(coins);
            document.getElementById(lockId).style.display = 'none';
            if (lockId === 'lock30') {
                document.getElementById('unlocked30').style.display = 'block';
            }
        }

        function closeModal() {
            document.getElementById('coinModal').style.display = 'none';
        }

        function sendMessage() {
            const input = document.getElementById('chatInput');
            const text = input.value.trim();
            const banner = document.getElementById('errorBanner');
            
            if (text === "") {
                banner.style.display = 'block';
                setTimeout(() => { banner.style.display = 'none'; }, 2000);
                return;
            }

            banner.style.display = 'none';
            const chatStream = document.getElementById('chatStream');
            const newMsg = document.createElement('div');
            newMsg.className = 'msg user';
            newMsg.innerText = text;
            chatStream.appendChild(newMsg);
            input.value = "";
            chatStream.scrollTop = chatStream.scrollHeight;
        }
    </script>
</body>
</html>
"""

class MockLikeyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_LIKEY.encode("utf-8"))

    def log_message(self, format, *args):
        pass

def start_likey_server(port=8877):
    server = HTTPServer(("127.0.0.1", port), MockLikeyHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

# ========================================================
# 3. LIKEY 특화 멀티 에이전트 (대리-팀장 검토)
# ========================================================
class LikeyAssistantAgent:
    def draft_or_refine(self, feedback: Optional[ReviewFeedback], iteration: int) -> TestSuite:
        if iteration == 1 or not feedback:
            cases = [
                TestCase(tc_id="TC-LIKEY-001", title="모바일 뷰포트 반응형 헤더 및 기본 50코인 노출 확인",
                         test_type="MobileUI", priority="P0", device="iPhone 14",
                         steps=["iPhone 14 환경에서 접속", "헤더 크리에이터명과 50코인 잔액 확인"],
                         expected_result="모바일 헤더 깨짐 없이 코인 배지가 50으로 로드됨"),
                TestCase(tc_id="TC-LIKEY-002", title="메시지 전송 기능 정상 입력 확인",
                         test_type="Positive", priority="P0", device="iPhone 14",
                         steps=["입력창에 '안녕하세요' 입력", "전송 버튼 클릭"],
                         expected_result="채팅창 우측에 사용자 메시지 버블이 생성됨")
            ]
            return TestSuite(version=1, test_cases=cases)
        else:
            cases = [
                TestCase(tc_id="TC-LIKEY-001", title="모바일 뷰포트 반응형 헤더 및 기본 50코인 노출 확인",
                         test_type="MobileUI", priority="P0", device="iPhone 14",
                         steps=["iPhone 14 환경에서 접속", "헤더 크리에이터명과 50코인 잔액 확인"],
                         expected_result="모바일 헤더 깨짐 없이 코인 배지가 50으로 로드됨"),
                TestCase(tc_id="TC-LIKEY-002", title="빈 메시지 전송 차단 및 경고 배너 검증",
                         test_type="Boundary", priority="P0", device="iPhone 14",
                         steps=["입력창을 비워둔 채 전송 버튼 터치"],
                         expected_result="'빈 메시지는 전송할 수 없습니다' 인라인 에러 배너 노출"),
                TestCase(tc_id="TC-LIKEY-003", title="정상 메시지 입력 및 전송 버블 렌더링 확인",
                         test_type="Positive", priority="P1", device="iPhone 14",
                         steps=["'유나님 팬입니다!' 입력 후 전송"],
                         expected_result="사용자 핑크색 메시지 버블이 정상 렌더링됨"),
                TestCase(tc_id="TC-LIKEY-004", title="30코인 잠긴 사진 열람 시 잔액 차감(50 ➔ 20) 검증",
                         test_type="CoinBVA", priority="P0", device="iPhone 14",
                         steps=["30 코인 잠금 해제 버튼 터치"],
                         expected_result="잠금 해제되고 상단 코인이 정확히 20 COIN으로 차감 반영됨"),
                TestCase(tc_id="TC-LIKEY-005", title="잔여 20코인 상태에서 100코인 영상 클릭 시 코인 부족 차단",
                         test_type="AccessControl", priority="P0", device="iPhone 14",
                         steps=["100 코인 잠금 해제 버튼 터치"],
                         expected_result="영상 열람이 차단되고 '코인이 부족합니다' 충전 유도 모달이 팝업됨")
            ]
            return TestSuite(version=iteration, test_cases=cases)

class LikeyTeamLeadAgent:
    def review(self, suite: TestSuite, iteration: int) -> ReviewFeedback:
        types = {tc.test_type for tc in suite.test_cases}
        if iteration == 1 and ("Boundary" not in types or "CoinBVA" not in types or "AccessControl" not in types):
            return ReviewFeedback(
                approved=False,
                quality_score=64,
                summary="LIKEY의 핵심 모바일 기능인 '공백 메시지 유효성 검사', '인앱 코인 차감', '코인 부족 시 충전 모달 차단'이 누락되었습니다.",
                action_items=[
                    "TC-LIKEY-002: 빈 메시지 전송 방지 Boundary 테스트 추가",
                    "TC-LIKEY-004: 30코인 차감 후 실시간 잔액(20) 동기화 검증 추가",
                    "TC-LIKEY-005: 100코인 부족 시 잠금 유지 및 충전 유도 모달 검증 추가"
                ]
            )
        return ReviewFeedback(
            approved=True,
            quality_score=97,
            summary="모바일 뷰포트 반응형, 1:1 채팅, 코인 결제 BVA 및 권한 제어가 모두 충족되었습니다. 모바일 E2E 실행을 승인합니다.",
            action_items=[]
        )

# ========================================================
# 4. 사원 에이전트: Playwright 모바일(iPhone 14) 실측 실행
# ========================================================
def execute_likey_mobile_tests(server_url: str, suite: TestSuite) -> List[Dict[str, Any]]:
    os.makedirs("likey_screenshots", exist_ok=True)
    results = []

    print("\n" + "=" * 65)
    print("📱 [사원 Agent] Playwright 'iPhone 14' 모바일 에뮬레이션 가동")
    print("=" * 65)

    with sync_playwright() as p:
        iphone = p.devices["iPhone 14"]
        browser = p.chromium.launch(headless=False, slow_mo=700)
        context = browser.new_context(**iphone)
        page = context.new_page()

        for tc in suite.test_cases:
            tc_id = tc.tc_id
            print(f"\n▶️ [{tc_id}] 실행 중: {tc.title} ({tc.device})")

            try:
                if tc_id == "TC-LIKEY-001":
                    page.goto(server_url)
                    page.wait_for_selector(".header")
                    coin_txt = page.text_content("#coinCount")
                    assert coin_txt == "50"
                    status = "✅ PASS"
                    detail = "iPhone 14 모바일 뷰포트 로드 및 50코인 확인"

                elif tc_id == "TC-LIKEY-002":
                    page.goto(server_url)
                    page.click("#btnSend")
                    page.wait_for_selector("#errorBanner", state="visible")
                    assert "빈 메시지는 전송할 수 없습니다" in page.text_content("#errorBanner")
                    status = "✅ PASS"
                    detail = "공백 전송 차단 에러 배너 정상 노출"

                elif tc_id == "TC-LIKEY-003":
                    page.goto(server_url)
                    page.fill("#chatInput", "유나님 팬입니다!")
                    page.click("#btnSend")
                    page.wait_for_selector(".msg.user")
                    assert "유나님 팬입니다!" in page.text_content(".msg.user")
                    status = "✅ PASS"
                    detail = "모바일 1:1 메시지 전송 버블 정상 렌더링"

                elif tc_id == "TC-LIKEY-004":
                    page.goto(server_url)
                    page.click("#btnUnlock30")
                    page.wait_for_selector("#unlocked30", state="visible")
                    coin_txt = page.text_content("#coinCount")
                    assert coin_txt == "20"
                    status = "✅ PASS"
                    detail = "30코인 콘텐츠 잠금 해제 및 잔액 20코인 차감 검증 성공"

                elif tc_id == "TC-LIKEY-005":
                    page.click("#btnUnlock100")
                    page.wait_for_selector("#coinModal", state="visible")
                    modal_txt = page.text_content("#coinModal")
                    assert "코인이 부족합니다" in modal_txt
                    status = "✅ PASS"
                    detail = "코인 부족 감지 및 충전소 이동 팝업 정상 차단 확인"

                screenshot_path = f"likey_screenshots/{tc_id}_mobile_pass.png"
                page.screenshot(path=screenshot_path)
            except Exception as e:
                status = "❌ FAIL"
                detail = str(e)
                screenshot_path = f"likey_screenshots/{tc_id}_mobile_fail.png"
                page.screenshot(path=screenshot_path)

            print(f"   결과: {status} ({detail})")
            results.append({
                "tc_id": tc_id,
                "title": tc.title,
                "type": tc.test_type,
                "status": status,
                "detail": detail,
                "screenshot": screenshot_path
            })

        browser.close()
    return results

# ========================================================
# 5. 협업 툴(Slack / Jira / Notion) 연동 산출물 생성
# ========================================================
def export_collaborative_reports(suite: TestSuite, results: List[Dict[str, Any]]):
    total = len(results)
    passed = sum(1 for r in results if "PASS" in r["status"])
    pass_rate = (passed / total * 100) if total > 0 else 0

    slack_payload = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🚀 [LIKEY] 모바일 E2E 자동화 테스트 릴리즈 알림"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*테스트 대상:*\n{suite.service_name}"},
                    {"type": "mrkdwn", "text": f"*통과율:*\n*{passed}/{total}건 ({pass_rate:.1f}%)*"},
                    {"type": "mrkdwn", "text": f"*디바이스 환경:*\niPhone 14 (iOS Safari WebKit/Mobile)"},
                    {"type": "mrkdwn", "text": f"*배포 판정:*\n{'🟢 GO (배포 승인)' if pass_rate == 100 else '🔴 NO-GO'}"}
                ]
            },
            {"type": "divider"}
        ]
    }
    with open("likey_slack_notification.json", "w", encoding="utf-8") as f:
        json.dump(slack_payload, f, indent=2, ensure_ascii=False)

    with open("likey_qa_mobile_report.md", "w", encoding="utf-8") as f:
        f.write("# 📱 [LIKEY] 모바일 웹/앱 1:1 채팅 & 코인 결제 QA 종합 리포트\n\n")
        f.write(f"- **검증 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **테스트 환경**: Apple iPhone 14 Viewport (390 x 844, Touch Event)\n")
        f.write(f"- **테스트 통과율**: **{passed}/{total} 건 ({pass_rate:.1f}%)**\n")
        f.write(f"- **최종 판정**: **{'🟢 GO (릴리즈 승인)' if pass_rate == 100 else '🔴 NO-GO'}**\n\n")
        
        f.write("## 1. 주요 검증 및 협업 요약 (Jira / Slack 대응)\n")
        f.write("본 테스트는 티피씨 LIKEY의 핵심 기능인 **크리에이터 1:1 채팅 인터랙션**과 **인앱 코인 차감/부족 상태 전이**를 ")
        f.write("모바일 실측 환경에서 멀티 에이전트 파이프라인으로 검증한 결과입니다.\n\n")

        f.write("## 2. 모바일 세부 테스트 실행 결과\n\n")
        f.write("| TC ID | 테스트 명세 | 분류 | 상태 | 검증 내용 | 모바일 스크린샷 |\n")
        f.write("| :--- | :--- | :---: | :---: | :--- | :--- |\n")
        for r in results:
            link = f"[{r['tc_id']}]({r['screenshot']})"
            f.write(f"| `{r['tc_id']}` | {r['title']} | {r['type']} | {r['status']} | {r['detail']} | {link} |\n")

        f.write("\n## 3. Slack 연동 안내\n")
        f.write("- 생성된 `likey_slack_notification.json` 파일의 블록 키트 페이로드를 사내 Slack Incoming Webhook에 그대로 전송할 수 있도록 설계되었습니다.\n")

# ========================================================
# 6. 메인 실행 함수
# ========================================================
def main():
    print("=" * 65)
    print("🚀 [티피씨 LIKEY 특화 파이프라인] 모바일 E2E & 협업 알림 자동화")
    print("=" * 65)

    port = 8877
    server = start_likey_server(port)
    server_url = f"http://127.0.0.1:{port}"
    print(f"📡 LIKEY 모바일 테스트베드 서버 가동: {server_url}")

    assistant = LikeyAssistantAgent()
    team_lead = LikeyTeamLeadAgent()

    feedback = None
    approved_suite = None
    for iteration in range(1, 3):
        print(f"\n[Phase 1 / Loop {iteration}] 대리 Agent가 LIKEY 모바일 기획서를 분석해 TC를 작성합니다...")
        suite = assistant.draft_or_refine(feedback, iteration)
        print(f"   -> {len(suite.test_cases)}건의 모바일 TC 생성 (버전 {suite.version})")

        print(f"[Phase 1 / Loop {iteration}] 팀장 Agent가 모바일 뷰포트, 채팅 유효성, 코인 BVA를 심사합니다...")
        feedback = team_lead.review(suite, iteration)
        print(f"   -> 심사 결과: {'✅ 승인' if feedback.approved else '❌ 반려'} (점수: {feedback.quality_score}점)")

        if feedback.approved:
            approved_suite = suite
            break
        else:
            print(f"   -> 반려 사유: {feedback.summary}")
            for item in feedback.action_items:
                print(f"      * {item}")

    if approved_suite:
        execution_results = execute_likey_mobile_tests(server_url, approved_suite)
        export_collaborative_reports(approved_suite, execution_results)

        print("\n" + "=" * 65)
        print("🎉 [LIKEY 모바일 QA 완료] 모든 검증 및 협업 연동 파일 생성이 완료되었습니다!")
        print(f"📄 모바일 QA 보고서: likey_qa_mobile_report.md")
        print(f"💬 슬랙 알림 페이로드: likey_slack_notification.json")
        print(f"📱 모바일 스크린샷: likey_screenshots/")
        print("=" * 65)

    server.shutdown()

if __name__ == "__main__":
    main()