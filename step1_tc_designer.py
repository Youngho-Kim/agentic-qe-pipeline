import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from config_loader import load_config

_cfg = load_config()
ARTIFACTS_DIR = _cfg["paths"]["artifacts_dir"]
DRAFT_EXCEL = os.path.join(ARTIFACTS_DIR, "step1_draft_testcases.xlsx")
REPORT_MD = os.path.join(ARTIFACTS_DIR, "step1_design_report.md")

def generate_draft_testcases():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "TC_설계_초안"

    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="맑은 고딕", size=11, bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

    headers = ["TC_ID", "대분류", "테스트명", "우선순위", "스텝순서", "액션타입", "타겟셀렉터", "입력값", "기대결과값"]
    ws.append(headers)

    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align

    test_steps = [
        # TC-001 (Positive)
        ["TC-001", "인증", "정상 계정 로그인 및 대시보드 진입", "P0", 1, "goto", "", "https://www.saucedemo.com/", "로그인 페이지 접속"],
        ["TC-001", "인증", "정상 계정 로그인 및 대시보드 진입", "P0", 2, "fill", "[data-test='username']", "standard_user", "정상 아이디 입력"],
        ["TC-001", "인증", "정상 계정 로그인 및 대시보드 진입", "P0", 3, "fill", "[data-test='password']", "secret_sauce", "정상 비밀번호 입력"],
        ["TC-001", "인증", "정상 계정 로그인 및 대시보드 진입", "P0", 4, "click", "[data-test='login-button']", "", "로그인 클릭"],
        ["TC-001", "인증", "정상 계정 로그인 및 대시보드 진입", "P0", 5, "assert_text", ".title", "Products", "대시보드 정상 진입 확인"],
        
        # TC-002 (Negative)
        ["TC-002", "인증", "잘못된 비밀번호 에러 처리 검증", "P1", 1, "goto", "", "https://www.saucedemo.com/", "로그인 페이지 접속"],
        ["TC-002", "인증", "잘못된 비밀번호 에러 처리 검증", "P1", 2, "fill", "[data-test='username']", "standard_user", "아이디 입력"],
        ["TC-002", "인증", "잘못된 비밀번호 에러 처리 검증", "P1", 3, "fill", "[data-test='password']", "wrong_pass_999", "틀린 비밀번호 입력"],
        ["TC-002", "인증", "잘못된 비밀번호 에러 처리 검증", "P1", 4, "click", "[data-test='login-button']", "", "로그인 클릭"],
        ["TC-002", "인증", "잘못된 비밀번호 에러 처리 검증", "P1", 5, "assert_text", "[data-test='error']", "Username and password do not match", "불일치 에러 배너 확인"],

        # TC-003 (Boundary / BVA)
        ["TC-003", "유효성", "필수값 빈칸 전송 방지 유효성 검증", "P0", 1, "goto", "", "https://www.saucedemo.com/", "로그인 페이지 접속"],
        ["TC-003", "유효성", "필수값 빈칸 전송 방지 유효성 검증", "P0", 2, "click", "[data-test='login-button']", "", "빈칸 상태로 로그인 클릭"],
        ["TC-003", "유효성", "필수값 빈칸 전송 방지 유효성 검증", "P0", 3, "assert_text", "[data-test='error']", "Username is required", "필수값 경고 배너 확인"],

        # TC-004 (Security)
        ["TC-004", "보안", "잠긴 계정 접근 차단 상태 전이 검증", "P1", 1, "goto", "", "https://www.saucedemo.com/", "로그인 페이지 접속"],
        ["TC-004", "보안", "잠긴 계정 접근 차단 상태 전이 검증", "P1", 2, "fill", "[data-test='username']", "locked_out_user", "잠긴 계정 아이디 입력"],
        ["TC-004", "보안", "잠긴 계정 접근 차단 상태 전이 검증", "P1", 3, "fill", "[data-test='password']", "secret_sauce", "비밀번호 입력"],
        ["TC-004", "보안", "잠긴 계정 접근 차단 상태 전이 검증", "P1", 4, "click", "[data-test='login-button']", "", "로그인 클릭"],
        ["TC-004", "보안", "잠긴 계정 접근 차단 상태 전이 검증", "P1", 5, "assert_text", "[data-test='error']", "Sorry, this user has been locked out", "잠금 상태 에러 확인"]
    ]

    for row in test_steps:
        ws.append(row)

    col_widths = {"A": 12, "B": 12, "C": 35, "D": 10, "E": 10, "F": 15, "G": 28, "H": 28, "I": 35}
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    wb.save(DRAFT_EXCEL)

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# 📋 [Step 1 보고서] 기획서 분석 및 테스트 케이스 설계 요약서\n\n")
        f.write(f"- **분석 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **도출된 총 테스트 케이스**: 4건 (총 18개 세부 자동화 스텝)\n")
        f.write(f"- **생성된 엑셀 산출물**: `{DRAFT_EXCEL}`\n\n")
        f.write("## 1. 기획 요구사항 매핑 현황\n\n")
        f.write("| TC ID | 카테고리 | 우선순위 | 케이스명 | 검증 핵심 목표 |\n")
        f.write("| :--- | :---: | :---: | :--- | :--- |\n")
        f.write("| `TC-001` | 인증 | **P0** | 정상 계정 로그인 및 대시보드 진입 | 세션 생성 및 메인 이동 (Happy Path) |\n")
        f.write("| `TC-002` | 인증 | **P1** | 잘못된 비밀번호 에러 처리 검증 | 비정상 인증 차단 및 인라인 피드백 |\n")
        f.write("| `TC-003` | 유효성 | **P0** | 필수값 빈칸 전송 방지 유효성 검증 | Boundary BVA 빈칸 필터링 |\n")
        f.write("| `TC-004` | 보안 | **P1** | 잠긴 계정 접근 차단 상태 전이 검증 | 보안 계정 잠금 정책 준수 확인 |\n\n")
        f.write("## 2. QE 중간 확인 및 개입 안내 (Human-in-the-Loop)\n")
        f.write("- QE는 생성된 `step1_draft_testcases.xlsx` 파일을 직접 열어 케이스를 추가하거나 셀렉터를 수정할 수 있습니다.\n")
        f.write("- 확인이 완료되면 **Step 2 (Quality Gate 심사)** 단계로 진행해 승인 절차를 밟으십시오.\n")

    print("=" * 65)
    print("🎯 [Step 1: TC Designer Agent] 기획 분석 및 TC 설계 완료")
    print(f"📁 엑셀 초안 산출물: {DRAFT_EXCEL}")
    print(f"📄 QE 중간 요약 보고서: {REPORT_MD}")
    print("=" * 65)

if __name__ == "__main__":
    generate_draft_testcases()