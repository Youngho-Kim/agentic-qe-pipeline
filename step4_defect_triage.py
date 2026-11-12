import os
import json
from datetime import datetime
from config_loader import load_config

_cfg = load_config()
ARTIFACTS_DIR = _cfg["paths"]["artifacts_dir"]
LOGS_JSON = os.path.join(ARTIFACTS_DIR, "step3_raw_execution_logs.json")
TRIAGE_REPORT_MD = os.path.join(ARTIFACTS_DIR, "step4_triage_report.md")
JIRA_TICKET_MD = os.path.join(ARTIFACTS_DIR, "step4_jira_defect_tickets.md")

def analyze_defects():
    if not os.path.exists(LOGS_JSON):
        print(f"❌ [에러] '{LOGS_JSON}' 파일이 없습니다. 먼저 Step 3을 실행해야 합니다.")
        return False

    with open(LOGS_JSON, "r", encoding="utf-8") as f:
        logs = json.load(f)

    failed_cases = [log for log in logs if log["status"] == "FAIL"]
    total = len(logs)
    
    print("=" * 65)
    print("🔍 [Step 4: Defect Triage Agent] 결함 원인 분석(RCA) 및 트리아지 가동")
    print(f"📋 총 검토 대상: {total}건 | 실패 건수: {len(failed_cases)}건")
    print("=" * 65)

    triaged_defects = []
    for fail in failed_cases:
        err = fail["error_details"]
        if "Timeout" in err:
            classification = "일시적 네트워크/렌더링 지연 (Flaky Issue)"
            action = "재시도(Retry) 로직 추가 및 타임아웃 대기시간 증가 권장"
            severity = "P2 (Medium)"
        elif "불일치" in err:
            classification = "비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)"
            action = "프론트엔드/기획 명세서와 비교 확인 후 버그 티켓 등록"
            severity = "P1 (High)"
        else:
            classification = "UI 셀렉터 변경 또는 요소 미탐색 (DOM Locator Issue)"
            action = "Playwright 셀렉터 유지보수 필요"
            severity = "P2 (Medium)"

        triaged_defects.append({
            "tc_id": fail["tc_id"],
            "title": fail["title"],
            "severity": severity,
            "classification": classification,
            "action": action,
            "error_msg": err,
            "failed_step": fail.get("failed_step"),
            "screenshot": fail["screenshot"]
        })

    with open(TRIAGE_REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# 🔍 [Step 4 보고서] 결함 원인 분석(RCA) 및 트리아지 보고서\n\n")
        f.write(f"- **분석 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **총 실행 건수**: {total}건 | **감지된 결함**: {len(failed_cases)}건\n\n")

        if not failed_cases:
            f.write("## 🟢 결함 미발견 (Clean Run)\n")
            f.write("모든 테스트가 100% 정상 통과하여 시스템 회귀 결함이 발견되지 않았습니다.\n\n")
        else:
            f.write("## 1. 결함 유형별 분류 현황\n\n")
            for d in triaged_defects:
                f.write(f"- **[{d['severity']}] {d['tc_id']}**: {d['classification']} ➔ {d['action']}\n")

    if failed_cases:
        with open(JIRA_TICKET_MD, "w", encoding="utf-8") as f:
            f.write("# 🚨 개발팀 공유용 Jira 결함 티켓\n\n")
            for d in triaged_defects:
                f.write(f"## [{d['severity']}] {d['tc_id']}: {d['title']}\n")
                f.write(f"- **분류**: {d['classification']}\n")
                f.write(f"- **에러 로그**: `{d['error_msg']}`\n\n")

    print(f"📄 QE 트리아지 보고서: {TRIAGE_REPORT_MD}")
    print("=" * 65)
    return True

if __name__ == "__main__":
    analyze_defects()