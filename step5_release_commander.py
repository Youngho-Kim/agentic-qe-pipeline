import os
import json
from datetime import datetime
from config_loader import load_config

_cfg = load_config()
ARTIFACTS_DIR = _cfg["paths"]["artifacts_dir"]
LOGS_JSON = os.path.join(ARTIFACTS_DIR, "step3_raw_execution_logs.json")
SIGNOFF_REPORT_MD = os.path.join(ARTIFACTS_DIR, "step5_release_signoff_report.md")
SLACK_JSON = os.path.join(ARTIFACTS_DIR, "step5_slack_broadcast.json")

def decide_release():
    if not os.path.exists(LOGS_JSON):
        print(f"❌ [에러] '{LOGS_JSON}' 파일이 없습니다. 이전 단계들을 먼저 실행해 주세요.")
        return False

    with open(LOGS_JSON, "r", encoding="utf-8") as f:
        logs = json.load(f)

    total = len(logs)
    passed = sum(1 for log in logs if log["status"] == "PASS")
    pass_rate = (passed / total * 100) if total > 0 else 0

    if pass_rate == 100:
        decision = "🟢 GO (무결점 정식 배포 승인)"
        decision_desc = "모든 P0/P1 핵심 시나리오 및 보안 검증이 100% 통과하여 무결점 릴리즈를 승인합니다."
    else:
        decision = "🔴 NO-GO (배포 보류)"
        decision_desc = "결함이 발견되어 개발팀 핫픽스 후 재테스트가 필요합니다."

    with open(SIGNOFF_REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# 📋 [Step 5 최종 보고서] QE 릴리즈 종합 평가 및 배포 승인서\n\n")
        f.write(f"- **최종 판정 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **최종 배포 의사결정**: **{decision}**\n")
        f.write(f"- **테스트 통과율**: **{passed}/{total}건 ({pass_rate:.1f}%)**\n\n")
        f.write("## 1. 5단계 파이프라인 감사 추적 (Audit Trail)\n\n")
        f.write("| 단계 | 에이전트 | 산출물 파일 |\n")
        f.write("| :---: | :--- | :--- |\n")
        f.write("| Step 1 | TC Designer | `artifacts/step1_draft_testcases.xlsx` |\n")
        f.write("| Step 2 | Quality Gate | `artifacts/step2_approved_testcases.xlsx` |\n")
        f.write("| Step 3 | Test Runner | `artifacts/step3_raw_execution_logs.json` |\n")
        f.write("| Step 4 | Defect Triage | `artifacts/step4_triage_report.md` |\n")
        f.write("| Step 5 | Release Commander | `artifacts/step5_release_signoff_report.md` |\n")

    slack_payload = {
        "text": f"🚀 [릴리즈 판정] {decision} - 통과율 {pass_rate:.1f}% ({passed}/{total}건)"
    }
    with open(SLACK_JSON, "w", encoding="utf-8") as f:
        json.dump(slack_payload, f, indent=2, ensure_ascii=False)

    print("=" * 65)
    print("👑 [Step 5: Release Commander Agent] 최종 릴리즈 사인오프 완료")
    print(f"📊 최종 의사결정: {decision}")
    print(f"📄 최종 보고서: {SIGNOFF_REPORT_MD}")
    print(f"💬 슬랙 알림: {SLACK_JSON}")
    print("=" * 65)
    return True

if __name__ == "__main__":
    decide_release()