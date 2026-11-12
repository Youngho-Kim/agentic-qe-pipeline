import os
import shutil
from datetime import datetime
from openpyxl import load_workbook
from config_loader import load_config

_cfg = load_config()
ARTIFACTS_DIR = _cfg["paths"]["artifacts_dir"]
DRAFT_EXCEL = os.path.join(ARTIFACTS_DIR, "step1_draft_testcases.xlsx")
APPROVED_EXCEL = os.path.join(ARTIFACTS_DIR, "step2_approved_testcases.xlsx")
GATE_REPORT_MD = os.path.join(ARTIFACTS_DIR, "step2_quality_gate_report.md")

def evaluate_quality_gate():
    if not os.path.exists(DRAFT_EXCEL):
        print(f"❌ [에러] '{DRAFT_EXCEL}' 파일이 없습니다. 먼저 Step 1을 실행해 주세요.")
        return False

    wb = load_workbook(DRAFT_EXCEL, data_only=True)
    ws = wb.active

    categories = set()
    priorities = set()
    total_steps = 0
    tc_ids = set()

    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        tc_ids.add(str(row[0]).strip())
        categories.add(str(row[1]).strip())
        priorities.add(str(row[3]).strip())
        total_steps += 1

    has_positive = any("인증" in c for c in categories)
    has_bva = any("유효성" in c for c in categories)
    has_security = any("보안" in c for c in categories)
    has_p0 = "P0" in priorities

    score = 100
    deductions = []
    if not has_positive:
        score -= 30
        deductions.append("기본 정상 흐름(Happy Path) 인증 누락 (-30점)")
    if not has_bva:
        score -= 25
        deductions.append("경계값(BVA) 및 빈값 유효성 검사 누락 (-25점)")
    if not has_security:
        score -= 25
        deductions.append("보안 계정 잠금 및 인젝션 예외 케이스 누락 (-25점)")
    if not has_p0:
        score -= 20
        deductions.append("최우선순위(P0) 핵심 경로 미지정 (-20점)")

    is_passed = score >= 85
    gate_status = "🟢 PASSED (실행 단계 승인)" if is_passed else "🔴 REJECTED (반려 및 보완 필요)"

    if is_passed:
        shutil.copyfile(DRAFT_EXCEL, APPROVED_EXCEL)

    with open(GATE_REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# 🛡️ [Step 2 보고서] Quality Gate 품질 심사 및 실행 승인서\n\n")
        f.write(f"- **심사 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **심사 결과**: **{gate_status}**\n")
        f.write(f"- **품질 종합 점수**: **{score}점 / 100점**\n")
        f.write(f"- **심사 대상**: 총 {len(tc_ids)}개 TC (총 {total_steps}개 스텝)\n\n")
        f.write("## 1. ISTQB 및 비즈니스 기준 평가표\n\n")
        f.write("| 심사 항목 | 기준 | 결과 | 배점 |\n")
        f.write("| :--- | :--- | :---: | :---: |\n")
        f.write(f"| 정상 기능(Happy Path) 검증 | 필수 포함 | {'✅ 통과' if has_positive else '❌ 누락'} | 30점 |\n")
        f.write(f"| 경계값 분석(BVA) 유효성 검증 | 필수 포함 | {'✅ 통과' if has_bva else '❌ 누락'} | 25점 |\n")
        f.write(f"| 보안 및 예외 상태 전이 검증 | 필수 포함 | {'✅ 통과' if has_security else '❌ 누락'} | 25점 |\n")
        f.write(f"| 우선순위(P0/P1) 분류 적합성 | P0 1건 이상 | {'✅ 통과' if has_p0 else '❌ 누락'} | 20점 |\n\n")

    print("=" * 65)
    print("🛡️ [Step 2: Quality Gate Agent] 품질 심사 완료")
    print(f"📊 판정 결과: {gate_status} (품질 점수: {score}점)")
    print(f"📁 승인된 엑셀: {APPROVED_EXCEL}")
    print(f"📄 QE 심사 보고서: {GATE_REPORT_MD}")
    print("=" * 65)
    return is_passed

if __name__ == "__main__":
    evaluate_quality_gate()