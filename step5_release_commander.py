import os
import json
from datetime import datetime
from openpyxl import load_workbook
from config_loader import load_config

_cfg = load_config()
ARTIFACTS_DIR = _cfg["paths"]["artifacts_dir"]
APPROVED_EXCEL = os.path.join(ARTIFACTS_DIR, "step2_approved_testcases.xlsx")
LOGS_JSON = os.path.join(ARTIFACTS_DIR, "step3_raw_execution_logs.json")
SIGNOFF_REPORT_MD = os.path.join(ARTIFACTS_DIR, "step5_release_signoff_report.md")
SLACK_JSON = os.path.join(ARTIFACTS_DIR, "step5_slack_broadcast.json")
QA_STATUS_JSON = os.path.join(ARTIFACTS_DIR, "qa_pipeline_status.json")
SENTINEL_CONFIG = os.path.join("sentinel_monitor", "monitor_config.json")

def extract_tested_urls(excel_path: str) -> list:
    urls = []
    if not os.path.exists(excel_path):
        return urls
    wb = load_workbook(excel_path, data_only=True)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or len(row) < 8:
            continue
        action = str(row[5] or "").strip().lower()
        val = str(row[7] or "").strip()
        if action == "goto" and val.startswith("http") and val not in urls:
            urls.append(val)
    return urls

def sync_to_sentinel_monitor(tested_urls: list, decision: str, pass_rate: float, passed: int, total: int):
    qa_status = {
        "decision": decision,
        "pass_rate": round(pass_rate, 1),
        "passed": passed,
        "total": total,
        "tested_urls": tested_urls,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(QA_STATUS_JSON, "w", encoding="utf-8") as f:
        json.dump(qa_status, f, indent=2, ensure_ascii=False)

    if pass_rate >= 90 and os.path.exists(SENTINEL_CONFIG) and tested_urls:
        with open(SENTINEL_CONFIG, "r", encoding="utf-8") as f:
            mon_cfg = json.load(f)
        existing_urls = {t["url"] for t in mon_cfg.get("targets", [])}
        added = 0
        for url in tested_urls:
            if url not in existing_urls:
                mon_cfg.setdefault("targets", []).append({
                    "name": f"[QA승인] Target #{len(mon_cfg['targets']) + 1}",
                    "url": url,
                    "expected_status": 200
                })
                added += 1
        if added > 0:
            with open(SENTINEL_CONFIG, "w", encoding="utf-8") as f:
                json.dump(mon_cfg, f, indent=2, ensure_ascii=False)
            print(f"🔗 [Closed-Loop 연계] QA 승인 URL {added}건을 Sentinel 모니터링에 자동 등록했습니다.")

def decide_release():
    if not os.path.exists(LOGS_JSON):
        print(f"❌ [에러] '{LOGS_JSON}' 파일이 없습니다. 이전 단계들을 먼저 실행해 주세요.")
        return False

    with open(LOGS_JSON, "r", encoding="utf-8") as f:
        logs = json.load(f)

    total = len(logs)
    passed = sum(1 for log in logs if log["status"] == "PASS")
    pass_rate = (passed / total * 100) if total > 0 else 0
    p0_failed = any(log["status"] == "FAIL" and log["priority"] == "P0" for log in logs)

    if pass_rate == 100:
        decision = "🟢 GO (무결점 정식 배포 승인)"
        decision_desc = "모든 P0/P1 핵심 시나리오 및 보안 검증이 100% 통과하여 무결점 릴리즈를 최종 승인합니다."
    elif not p0_failed and pass_rate >= 90:
        decision = "🟡 CONDITIONAL GO (조건부 배포 승인)"
        decision_desc = "P0 크리티컬 결함은 없으나 경미한 이슈가 발견되어 긴급 패치 일정 수립 후 배포를 승인합니다."
    else:
        decision = "🔴 NO-GO (배포 보류 및 롤백)"
        decision_desc = "P0 크리티컬 결함 또는 90% 미만 통과율로 인해 릴리즈를 차단하고 개발팀 재작업을 요청합니다."

    tested_urls = extract_tested_urls(APPROVED_EXCEL)
    sync_to_sentinel_monitor(tested_urls, decision, pass_rate, passed, total)

    with open(SIGNOFF_REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# 📋 [Step 5 최종 보고서] QE 릴리즈 종합 평가 및 최종 배포 승인서\n\n")
        f.write(f"- **최종 판정 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **최종 배포 의사결정**: **{decision}**\n")
        f.write(f"- **테스트 통과율**: **{passed}/{total}건 ({pass_rate:.1f}%)**\n")
        f.write(f"- **QE 총평**: {decision_desc}\n\n")
        f.write("## 1. 5단계 파이프라인 중간 산출물 종합 감사 (Audit Trail)\n\n")
        f.write("| 단계 | 담당 에이전트 | 주요 활동 | 생성 산출물 |\n")
        f.write("| :---: | :--- | :--- | :--- |\n")
        f.write(f"| **Step 1** | TC Designer Agent | 기획서 분석 및 BVA/보안 TC 초안 설계 | `{ARTIFACTS_DIR}/step1_draft_testcases.xlsx` |\n")
        f.write(f"| **Step 2** | Quality Gate Agent | ISTQB 기준 품질 점수 심사 | `{ARTIFACTS_DIR}/step2_approved_testcases.xlsx` |\n")
        f.write(f"| **Step 3** | Test Runner Agent | Playwright 실측 실행 및 요약 엑셀 생성 | `{ARTIFACTS_DIR}/step3_test_results_report.xlsx` |\n")
        f.write(f"| **Step 4** | Defect Triage Agent | 결함 원인 분석(RCA) 및 Jira 티켓 발행 | `{ARTIFACTS_DIR}/step4_triage_report.md` |\n")
        f.write(f"| **Step 5** | Release Commander | 최종 Go/No-Go 판정 및 모니터링 자동 연동 | `{ARTIFACTS_DIR}/step5_release_signoff_report.md` |\n\n")
        if tested_urls:
            f.write("## 2. Sentinel 모니터링 자동 연계 현황\n")
            for u in tested_urls:
                f.write(f"- 감시 대상 동기화: `{u}`\n")

    slack_payload = {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": "🚀 [QE Pipeline] 최종 릴리즈 판정 알림"}},
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*최종 판정:*\n*{decision}*"},
                    {"type": "mrkdwn", "text": f"*테스트 통과율:*\n*{passed}/{total}건 ({pass_rate:.1f}%)*"},
                    {"type": "mrkdwn", "text": f"*P0 장애 여부:*\n{'발생 (차단)' if p0_failed else '정상 (무결함)'}"},
                    {"type": "mrkdwn", "text": f"*사인오프 일시:*\n{datetime.now().strftime('%Y-%m-%d %H:%M')}"}
                ]
            }
        ]
    }
    with open(SLACK_JSON, "w", encoding="utf-8") as f:
        json.dump(slack_payload, f, indent=2, ensure_ascii=False)

    print("=" * 65)
    print("👑 [Step 5: Release Commander Agent] 최종 릴리즈 사인오프 완료")
    print(f"📊 최종 의사결정: {decision}")
    print(f"📄 최종 보고서: {SIGNOFF_REPORT_MD}")
    print(f"🔗 QA 상태 동기화: {QA_STATUS_JSON}")
    print("=" * 65)
    return True

if __name__ == "__main__":
    decide_release()import os
import json
from datetime import datetime
from openpyxl import load_workbook
from config_loader import load_config

_cfg = load_config()
ARTIFACTS_DIR = _cfg["paths"]["artifacts_dir"]
APPROVED_EXCEL = os.path.join(ARTIFACTS_DIR, "step2_approved_testcases.xlsx")
LOGS_JSON = os.path.join(ARTIFACTS_DIR, "step3_raw_execution_logs.json")
SIGNOFF_REPORT_MD = os.path.join(ARTIFACTS_DIR, "step5_release_signoff_report.md")
SLACK_JSON = os.path.join(ARTIFACTS_DIR, "step5_slack_broadcast.json")
QA_STATUS_JSON = os.path.join(ARTIFACTS_DIR, "qa_pipeline_status.json")
SENTINEL_CONFIG = os.path.join("sentinel_monitor", "monitor_config.json")

def extract_tested_urls(excel_path: str) -> list:
    urls = []
    if not os.path.exists(excel_path):
        return urls
    wb = load_workbook(excel_path, data_only=True)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or len(row) < 8:
            continue
        action = str(row[5] or "").strip().lower()
        val = str(row[7] or "").strip()
        if action == "goto" and val.startswith("http") and val not in urls:
            urls.append(val)
    return urls

def sync_to_sentinel_monitor(tested_urls: list, decision: str, pass_rate: float, passed: int, total: int):
    qa_status = {
        "decision": decision,
        "pass_rate": round(pass_rate, 1),
        "passed": passed,
        "total": total,
        "tested_urls": tested_urls,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(QA_STATUS_JSON, "w", encoding="utf-8") as f:
        json.dump(qa_status, f, indent=2, ensure_ascii=False)

    if pass_rate >= 90 and os.path.exists(SENTINEL_CONFIG) and tested_urls:
        with open(SENTINEL_CONFIG, "r", encoding="utf-8") as f:
            mon_cfg = json.load(f)
        existing_urls = {t["url"] for t in mon_cfg.get("targets", [])}
        added = 0
        for url in tested_urls:
            if url not in existing_urls:
                mon_cfg.setdefault("targets", []).append({
                    "name": f"[QA승인] Target #{len(mon_cfg['targets']) + 1}",
                    "url": url,
                    "expected_status": 200
                })
                added += 1
        if added > 0:
            with open(SENTINEL_CONFIG, "w", encoding="utf-8") as f:
                json.dump(mon_cfg, f, indent=2, ensure_ascii=False)
            print(f"🔗 [Closed-Loop 연계] QA 승인 URL {added}건을 Sentinel 모니터링에 자동 등록했습니다.")

def decide_release():
    if not os.path.exists(LOGS_JSON):
        print(f"❌ [에러] '{LOGS_JSON}' 파일이 없습니다. 이전 단계들을 먼저 실행해 주세요.")
        return False

    with open(LOGS_JSON, "r", encoding="utf-8") as f:
        logs = json.load(f)

    total = len(logs)
    passed = sum(1 for log in logs if log["status"] == "PASS")
    pass_rate = (passed / total * 100) if total > 0 else 0
    p0_failed = any(log["status"] == "FAIL" and log["priority"] == "P0" for log in logs)

    if pass_rate == 100:
        decision = "🟢 GO (무결점 정식 배포 승인)"
        decision_desc = "모든 P0/P1 핵심 시나리오 및 보안 검증이 100% 통과하여 무결점 릴리즈를 최종 승인합니다."
    elif not p0_failed and pass_rate >= 90:
        decision = "🟡 CONDITIONAL GO (조건부 배포 승인)"
        decision_desc = "P0 크리티컬 결함은 없으나 경미한 이슈가 발견되어 긴급 패치 일정 수립 후 배포를 승인합니다."
    else:
        decision = "🔴 NO-GO (배포 보류 및 롤백)"
        decision_desc = "P0 크리티컬 결함 또는 90% 미만 통과율로 인해 릴리즈를 차단하고 개발팀 재작업을 요청합니다."

    tested_urls = extract_tested_urls(APPROVED_EXCEL)
    sync_to_sentinel_monitor(tested_urls, decision, pass_rate, passed, total)

    with open(SIGNOFF_REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# 📋 [Step 5 최종 보고서] QE 릴리즈 종합 평가 및 최종 배포 승인서\n\n")
        f.write(f"- **최종 판정 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **최종 배포 의사결정**: **{decision}**\n")
        f.write(f"- **테스트 통과율**: **{passed}/{total}건 ({pass_rate:.1f}%)**\n")
        f.write(f"- **QE 총평**: {decision_desc}\n\n")
        f.write("## 1. 5단계 파이프라인 중간 산출물 종합 감사 (Audit Trail)\n\n")
        f.write("| 단계 | 담당 에이전트 | 주요 활동 | 생성 산출물 |\n")
        f.write("| :---: | :--- | :--- | :--- |\n")
        f.write(f"| **Step 1** | TC Designer Agent | 기획서 분석 및 BVA/보안 TC 초안 설계 | `{ARTIFACTS_DIR}/step1_draft_testcases.xlsx` |\n")
        f.write(f"| **Step 2** | Quality Gate Agent | ISTQB 기준 품질 점수 심사 | `{ARTIFACTS_DIR}/step2_approved_testcases.xlsx` |\n")
        f.write(f"| **Step 3** | Test Runner Agent | Playwright 실측 실행 및 요약 엑셀 생성 | `{ARTIFACTS_DIR}/step3_test_results_report.xlsx` |\n")
        f.write(f"| **Step 4** | Defect Triage Agent | 결함 원인 분석(RCA) 및 Jira 티켓 발행 | `{ARTIFACTS_DIR}/step4_triage_report.md` |\n")
        f.write(f"| **Step 5** | Release Commander | 최종 Go/No-Go 판정 및 모니터링 자동 연동 | `{ARTIFACTS_DIR}/step5_release_signoff_report.md` |\n\n")
        if tested_urls:
            f.write("## 2. Sentinel 모니터링 자동 연계 현황\n")
            for u in tested_urls:
                f.write(f"- 감시 대상 동기화: `{u}`\n")

    slack_payload = {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": "🚀 [QE Pipeline] 최종 릴리즈 판정 알림"}},
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*최종 판정:*\n*{decision}*"},
                    {"type": "mrkdwn", "text": f"*테스트 통과율:*\n*{passed}/{total}건 ({pass_rate:.1f}%)*"},
                    {"type": "mrkdwn", "text": f"*P0 장애 여부:*\n{'발생 (차단)' if p0_failed else '정상 (무결함)'}"},
                    {"type": "mrkdwn", "text": f"*사인오프 일시:*\n{datetime.now().strftime('%Y-%m-%d %H:%M')}"}
                ]
            }
        ]
    }
    with open(SLACK_JSON, "w", encoding="utf-8") as f:
        json.dump(slack_payload, f, indent=2, ensure_ascii=False)

    print("=" * 65)
    print("👑 [Step 5: Release Commander Agent] 최종 릴리즈 사인오프 완료")
    print(f"📊 최종 의사결정: {decision}")
    print(f"📄 최종 보고서: {SIGNOFF_REPORT_MD}")
    print(f"🔗 QA 상태 동기화: {QA_STATUS_JSON}")
    print("=" * 65)
    return True

if __name__ == "__main__":
    decide_release()