import os
import sys
import glob
import shutil
import argparse
from config_loader import load_config

cfg = load_config()
ARTIFACTS_DIR = cfg["paths"]["artifacts_dir"]
DRAFT_EXCEL = os.path.join(ARTIFACTS_DIR, "step1_draft_testcases.xlsx")

def find_custom_excel():
    """현재 폴더에서 사용자가 작성한 TC 엑셀 파일을 자동으로 탐색합니다."""
    if os.path.exists("test_cases.xlsx"):
        return "test_cases.xlsx"

    # 결과 파일 및 엑셀 실행 중 생기는 임시 파일(~$) 제외하고 .xlsx 탐색
    excluded = {"test_results_executed.xlsx"}
    candidates = [
        f for f in sorted(glob.glob("*.xlsx"))
        if not f.startswith("~$") and f not in excluded
    ]
    return candidates[0] if candidates else None

def main():
    parser = argparse.ArgumentParser(description="5-Step Modular QE Multi-Agent Pipeline")
    parser.add_argument(
        "--excel",
        type=str,
        default=None,
        help="직접 작성한 TC 엑셀 파일 경로 (미지정 시 현재 폴더의 엑셀 자동 감지)"
    )
    args = parser.parse_args()

    print("=" * 70)
    print("🏛️ [QE Modular Multi-Agent Pipeline] 5단계 계층형 테스트 엔지니어링 시스템")
    print("=" * 70)

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    # --excel 지정이 없으면 현재 폴더의 사용자 엑셀 파일 자동 감지
    custom_excel = args.excel or find_custom_excel()

    # [Step 1: 사용자 엑셀 자동 적용 또는 기본 TC 설계]
    if custom_excel:
        if not os.path.exists(custom_excel):
            print(f"❌ [오류] 지정한 엑셀 파일을 찾을 수 없습니다: {custom_excel}")
            return
        shutil.copyfile(custom_excel, DRAFT_EXCEL)
        print(f"\n📌 [자동 감지] 사용자 엑셀 '{custom_excel}'을(를) 발견해 Step 1을 대체 적용합니다.")
    else:
        print("\n📌 사용자 엑셀 파일이 없어 [1단계: TC Designer Agent]를 가동합니다.")
        import step1_tc_designer
        step1_tc_designer.generate_draft_testcases()

    # [Step 2: Quality Gate]
    print("\n▶️ [2단계 가동] Step 2: Quality Gate Agent (품질 심사 및 실행 승인)")
    import step2_quality_gate
    approved = step2_quality_gate.evaluate_quality_gate()
    if not approved:
        print("❌ Quality Gate 기준 미달로 파이프라인이 중단되었습니다.")
        print("👉 엑셀의 '대분류' 열(인증, 유효성, 보안) 및 '우선순위'(P0)를 확인해 주세요.")
        return

    # [Step 3: Test Runner]
    print("\n▶️ [3단계 가동] Step 3: Test Runner Agent (Playwright E2E 브라우저 실측)")
    import step3_test_runner
    step3_test_runner.run_approved_tests()

    # [Step 4: Defect Triage]
    print("\n▶️ [4단계 가동] Step 4: Defect Triage Agent (결함 원인 분석 및 트리아지)")
    import step4_defect_triage
    step4_defect_triage.analyze_defects()

    # [Step 5: Release Commander]
    print("\n▶️ [5단계 가동] Step 5: Release Commander Agent (최종 릴리즈 판정 및 브리핑)")
    import step5_release_commander
    step5_release_commander.decide_release()

    print("\n" + "=" * 70)
    print("🎉 [5단계 전 과정 완료] 모든 단계별 중간 보고서 생성이 완료되었습니다!")
    print("=" * 70)

if __name__ == "__main__":
    main()