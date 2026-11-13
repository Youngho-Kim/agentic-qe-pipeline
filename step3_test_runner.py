import os
import sys
import json
import time
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from playwright.sync_api import sync_playwright
from config_loader import load_config

_cfg = load_config()
ARTIFACTS_DIR = _cfg["paths"]["artifacts_dir"]
APPROVED_EXCEL = os.path.join(ARTIFACTS_DIR, "step2_approved_testcases.xlsx")
RESULT_EXCEL = os.path.join(ARTIFACTS_DIR, "step3_test_results_report.xlsx")
LOGS_JSON = os.path.join(ARTIFACTS_DIR, "step3_raw_execution_logs.json")
SUMMARY_MD = os.path.join(ARTIFACTS_DIR, "step3_execution_summary.md")
SCREENSHOTS_DIR = _cfg["paths"]["screenshots_dir"]

def build_excel_result_report(approved_excel_path: str, output_excel_path: str, execution_logs: list):
    wb = load_workbook(approved_excel_path)
    detail_ws = wb.active
    detail_ws.title = "상세_실행결과"

    log_map = {log["tc_id"]: log for log in execution_logs}

    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="맑은 고딕", size=11, bold=True, color="FFFFFF")
    sub_header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    bold_font = Font(name="맑은 고딕", size=10, bold=True)
    normal_font = Font(name="맑은 고딕", size=10)

    pass_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    pass_font = Font(name="맑은 고딕", size=10, bold=True, color="006100")
    fail_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    fail_font = Font(name="맑은 고딕", size=10, bold=True, color="9C0006")

    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9")
    )

    # 1. 상세_실행결과 시트에 PASS/FAIL, 소요시간, 메모 열 추가
    for col_idx, text in [(10, "실행결과"), (11, "소요시간(초)"), (12, "실행메모 / 에러사유")]:
        cell = detail_ws.cell(row=1, column=col_idx, value=text)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    detail_ws.column_dimensions["J"].width = 14
    detail_ws.column_dimensions["K"].width = 14
    detail_ws.column_dimensions["L"].width = 40

    for row_idx in range(2, detail_ws.max_row + 1):
        tc_id_val = detail_ws.cell(row=row_idx, column=1).value
        if not tc_id_val:
            continue
        log = log_map.get(str(tc_id_val).strip())
        if not log:
            continue

        status_cell = detail_ws.cell(row=row_idx, column=10)
        time_cell = detail_ws.cell(row=row_idx, column=11)
        memo_cell = detail_ws.cell(row=row_idx, column=12)

        status_cell.value = log["status"]
        status_cell.alignment = Alignment(horizontal="center", vertical="center")
        time_cell.value = log["elapsed_seconds"]
        time_cell.alignment = Alignment(horizontal="center", vertical="center")

        if log["status"] == "PASS":
            status_cell.fill = pass_fill
            status_cell.font = pass_font
            memo_cell.value = "정상 통과"
        else:
            status_cell.fill = fail_fill
            status_cell.font = fail_font
            memo_cell.value = log["error_details"][:100]

    # 2. 맨 앞에 '테스트_요약' 대시보드 시트 생성
    summary_ws = wb.create_sheet(title="테스트_요약", index=0)

    total = len(execution_logs)
    passed = sum(1 for l in execution_logs if l["status"] == "PASS")
    failed = total - passed
    pass_rate = round((passed / total * 100), 1) if total > 0 else 0.0
    total_time = round(sum(l["elapsed_seconds"] for l in execution_logs), 2)
    verdict = "GO (배포 승인)" if failed == 0 else "NO-GO (결함 확인 필요)"

    summary_ws.merge_cells("A1:E1")
    title_cell = summary_ws["A1"]
    title_cell.value = "📊 QE 자동화 테스트 실행 요약 대시보드"
    title_cell.font = Font(name="맑은 고딕", size=14, bold=True, color="FFFFFF")
    title_cell.fill = header_fill
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    summary_ws.row_dimensions[1].height = 32

    kpi_rows = [
        ("실행 일시", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("총 테스트 케이스 수", f"{total} 건"),
        ("성공 (PASS)", f"{passed} 건"),
        ("실패 (FAIL)", f"{failed} 건"),
        ("통과율 (Pass Rate)", f"{pass_rate} %"),
        ("총 실행 소요시간", f"{total_time} 초"),
        ("최종 판정", verdict)
    ]

    summary_ws.cell(row=3, column=1, value="요약 항목").fill = sub_header_fill
    summary_ws.cell(row=3, column=1).font = bold_font
    summary_ws.cell(row=3, column=2, value="측정 결과").fill = sub_header_fill
    summary_ws.cell(row=3, column=2).font = bold_font

    for idx, (label, val) in enumerate(kpi_rows, start=4):
        c1 = summary_ws.cell(row=idx, column=1, value=label)
        c2 = summary_ws.cell(row=idx, column=2, value=val)
        c1.font = bold_font
        c2.font = normal_font
        c1.border = thin_border
        c2.border = thin_border
        if label == "최종 판정":
            c2.fill = pass_fill if failed == 0 else fail_fill
            c2.font = pass_font if failed == 0 else fail_font

    # 대분류(카테고리)별 집계표
    cat_stats = {}
    for log in execution_logs:
        cat = log["category"] or "미분류"
        if cat not in cat_stats:
            cat_stats[cat] = {"total": 0, "pass": 0, "fail": 0}
        cat_stats[cat]["total"] += 1
        if log["status"] == "PASS":
            cat_stats[cat]["pass"] += 1
        else:
            cat_stats[cat]["fail"] += 1

    start_cat_row = 13
    for col_i, h in enumerate(["대분류", "총 건수", "PASS", "FAIL", "통과율(%)"], start=1):
        cell = summary_ws.cell(row=start_cat_row, column=col_i, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for offset, (cat, st) in enumerate(cat_stats.items(), start=1):
        r = start_cat_row + offset
        rate = round((st["pass"] / st["total"] * 100), 1) if st["total"] else 0.0
        for col_i, v in enumerate([cat, st["total"], st["pass"], st["fail"], f"{rate}%"], start=1):
            c = summary_ws.cell(row=r, column=col_i, value=v)
            c.font = normal_font
            c.border = thin_border
            c.alignment = Alignment(horizontal="center" if col_i > 1 else "left", vertical="center")

    for col_letter, width in [("A", 22), ("B", 24), ("C", 14), ("D", 14), ("E", 16)]:
        summary_ws.column_dimensions[col_letter].width = width

    wb.save(output_excel_path)

def run_approved_tests():
    if not os.path.exists(APPROVED_EXCEL):
        print(f"❌ [에러] '{APPROVED_EXCEL}' 파일이 없습니다. 먼저 Step 2를 통과해야 합니다.")
        return False

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    wb = load_workbook(APPROVED_EXCEL, data_only=True)
    ws = wb.active

    test_cases = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        tc_id = str(row[0]).strip()
        if tc_id not in test_cases:
            test_cases[tc_id] = {
                "tc_id": tc_id,
                "category": str(row[1] or "").strip(),
                "title": str(row[2] or "").strip(),
                "priority": str(row[3] or "P1").strip(),
                "steps": []
            }
        test_cases[tc_id]["steps"].append({
            "step_num": row[4],
            "action": str(row[5] or "").strip().lower(),
            "selector": str(row[6] or "").strip(),
            "val": str(row[7] if row[7] is not None else "").strip(),
            "expected": str(row[8] if row[8] is not None else "").strip()
        })

    execution_logs = []
    print("=" * 65)
    print("🚀 [Step 3: Test Runner Agent] Playwright E2E 브라우저 자동 실행")
    print(f"📋 실행 대상 테스트 케이스: {len(test_cases)}건")
    print("=" * 65)

    browser_cfg = _cfg["browser"]
    is_ci = os.getenv("CI", "").lower() == "true"
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True if is_ci else browser_cfg["headless"],
            slow_mo=0 if is_ci else browser_cfg["slow_mo_ms"]
        )   
        page = browser.new_page()

        for tc_id, data in test_cases.items():
            print(f"\n▶️ [{tc_id}] 실행 중: {data['title']}")
            tc_pass = True
            error_msg = ""
            start_t = time.time()
            failed_step = None

            for step in data["steps"]:
                action = step["action"]
                selector = step["selector"]
                val = step["val"]
                expected = step["expected"]

                try:
                    if action == "goto":
                        page.goto(val, timeout=browser_cfg["timeout_ms"])
                    elif action == "fill":
                        page.fill(selector, val)
                    elif action == "click":
                        page.click(selector)
                    elif action == "assert_text":
                        page.wait_for_selector(selector, timeout=5000)
                        txt = page.text_content(selector)
                        assert expected in txt, f"기대값 '{expected}' vs 실제값 '{txt}' 불일치"
                except Exception as e:
                    tc_pass = False
                    error_msg = str(e)
                    failed_step = step
                    break

            elapsed = round(time.time() - start_t, 2)
            screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{tc_id}_{'pass' if tc_pass else 'fail'}.png")
            page.screenshot(path=screenshot_path)

            status = "PASS" if tc_pass else "FAIL"
            print(f"   결과: {'✅' if tc_pass else '❌'} {status} (소요시간: {elapsed}s)")

            execution_logs.append({
                "tc_id": tc_id,
                "title": data["title"],
                "category": data["category"],
                "priority": data["priority"],
                "status": status,
                "elapsed_seconds": elapsed,
                "screenshot": screenshot_path,
                "error_details": error_msg,
                "failed_step": failed_step
            })

        browser.close()

    with open(LOGS_JSON, "w", encoding="utf-8") as f:
        json.dump(execution_logs, f, indent=2, ensure_ascii=False)

    build_excel_result_report(APPROVED_EXCEL, RESULT_EXCEL, execution_logs)

    total = len(execution_logs)
    passed = sum(1 for log in execution_logs if log["status"] == "PASS")
    failed = total - passed

    with open(SUMMARY_MD, "w", encoding="utf-8") as f:
        f.write("# 📊 [Step 3 보고서] Playwright 실측 실행 요약 보고서\n\n")
        f.write(f"- **실행 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **총 실행 건수**: {total}건\n")
        f.write(f"- **성공**: {passed}건 | **실패**: {failed}건 (통과율: {passed/total*100:.1f}%)\n")
        f.write(f"- **요약 엑셀 보고서**: `{RESULT_EXCEL}`\n\n")
        f.write("## 1. 테스트 케이스별 실행 결과표\n\n")
        f.write("| TC ID | 테스트명 | 우선순위 | 결과 | 소요시간 | 증빙 스크린샷 |\n")
        f.write("| :--- | :--- | :---: | :---: | :---: | :--- |\n")
        for log in execution_logs:
            f.write(f"| `{log['tc_id']}` | {log['title']} | **{log['priority']}** | {'✅ PASS' if log['status']=='PASS' else '❌ FAIL'} | {log['elapsed_seconds']}s | [{log['tc_id']} 캡처]({log['screenshot']}) |\n")

    print("=" * 65)
    print("📊 [Step 3: Test Runner Agent] 실행 완료")
    print(f"📊 요약 대시보드 엑셀: {RESULT_EXCEL}")
    print(f"📁 실행 로그: {LOGS_JSON}")
    print(f"📄 중간 요약 보고서: {SUMMARY_MD}")
    print("=" * 65)
    return True

if __name__ == "__main__":
    run_approved_tests()