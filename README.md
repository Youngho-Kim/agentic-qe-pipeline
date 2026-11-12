# 🛡️ 5-Step Modular AI-QE Automation Pipeline

> **블랙박스 자동화를 배제하고, 단계별 품질 게이트(Quality Gate)와 데이터 주도 테스팅(DDT)을 결합한 실무형 QE 멀티 에이전트 E2E 자동화 프레임워크**

---

## 📌 프로젝트 개요 (Overview)

* **문제 배경**:
  * 단일 LLM으로 테스트 케이스(TC)를 생성하면 정상 흐름 위주로만 작성되어 경계값(BVA) 및 보안 예외가 누락되는 문제가 발생합니다.
  * 코드에 TC를 하드코딩하면 케이스가 수백 개로 늘어날 때 유지보수가 어려워집니다.
  * 결과만 출력되는 원클릭 블랙박스 자동화는 실무 QE가 중간 의사결정 근거를 검증하기 어렵습니다.
* **해결 방안**:
  * **5단계 역할 분리 아키텍처**: 설계(`step1`) → 품질 심사(`step2`) → 브라우저 실행(`step3`) → 결함 원인 분석(`step4`) → 릴리즈 판정(`step5`)으로 모듈을 분리하고, 단계마다 `artifacts/`에 중간 보고서를 남겨 **QE가 직접 검토·통제(Human-in-the-Loop)**할 수 있도록 구현했습니다.
  * **엑셀 데이터 주도 테스팅(DDT)**: 비개발 직군도 엑셀 시트(`test_cases.xlsx`)에 행만 추가하면 코드 수정 없이 **100건 이상의 TC를 일괄 자동 실행**하고 결과(PASS/FAIL)를 엑셀에 자동 마킹합니다.
  * **도메인 특화 & 크로스 플랫폼**: 멤버십 등급별 권한 제어, 쿠폰 음수 결제 방어(BVA), 모바일 뷰포트(`iPhone 14`) 에뮬레이션 검증과 Windows/macOS 원클릭 설치·실행 스크립트를 제공합니다.

---

## 🏗️ 5단계 모듈 아키텍처 (Architecture)

```text
[기획서 / 요구사항]
       │
       ▼
[Step 1] step1_tc_designer.py       ──► artifacts/step1_draft_testcases.xlsx & step1_design_report.md
       │  (QE 중간 검토 및 엑셀 수정 가능)
       ▼
[Step 2] step2_quality_gate.py      ──► artifacts/step2_approved_testcases.xlsx & step2_quality_gate_report.md
       │  (ISTQB/BVA 기준 85점 이상 통과 시 승인)
       ▼
[Step 3] step3_test_runner.py       ──► artifacts/step3_raw_execution_logs.json & screenshots/
       │  (Playwright 실측 브라우저 E2E 실행)
       ▼
[Step 4] step4_defect_triage.py     ──► artifacts/step4_triage_report.md & step4_jira_defect_tickets.md
       │  (Flaky 지연 vs 기능 결함 1차 RCA 분류)
       ▼
[Step 5] step5_release_commander.py ──► artifacts/step5_release_signoff_report.md & step5_slack_broadcast.json
          (최종 Go / No-Go 판정 및 협업 브리핑)
```

---

## ✨ 주요 기능 및 실행 모듈

| 모듈 / 파일 | 역할 및 주요 검증 내용 | 산출물 |
| :--- | :--- | :--- |
| **`run_modular_qe_pipeline.py`** | 5단계 모듈을 순차 연결하는 마스터 오케스트레이터 | `artifacts/` 전체 보고서 |
| **`excel_test_runner.py`** | [openpyxl](https://openpyxl.readthedocs.io/) 기반 엑셀 DDT 엔진 (100+ TC 코드 수정 없이 실행) | `test_results_executed.xlsx` |
| **`run_fanding_membership_qa.py`** | 크리에이터 멤버십 등급별 접근 권한(Access Control), 초과 쿠폰 0원 바운딩(BVA), 결제 실패 3일 유예 배너 검증 | `fanding_qa_release_report.md` |
| **`run_likey_mobile_qa.py`** | iPhone 14 모바일 뷰포트 에뮬레이션 기반 1:1 채팅 유효성, 코인 차감/부족 모달 차단, Slack Block Kit 알림 생성 | `likey_qa_mobile_report.md`, `likey_slack_notification.json` |

---

## 🛠️ 기술 스택 (Tech Stack)

* **Language**: [Python](https://www.python.org/) 3.11+
* **Browser Automation**: [Playwright](https://playwright.dev/) (Desktop Chromium & iPhone 14 Mobile Emulation)
* **Data Validation**: [Pydantic](https://docs.pydantic.dev/) v2
* **Data-Driven Testing**: [openpyxl](https://openpyxl.readthedocs.io/)
* **Automation Scripts**: Windows Batch (`.bat`), Bash Shell (`.sh`)

---

## 🚀 빠른 시작 (Quickstart)

### 1. 원클릭 환경 설치 (최초 1회)
* **Windows 11**: `setup.bat` 더블 클릭 (또는 터미널에서 `setup.bat`)
* **macOS / Linux**:
  ```bash
  bash setup.sh
  ```

### 2. 5단계 QE 파이프라인 실행
* **Windows 11**: `run_master.bat` 더블 클릭 (또는 터미널에서 `run_master.bat`)
* **macOS / Linux**:
  ```bash
  bash run_master.sh
  ```

### 3. 개별 시나리오 단독 실행
```bash
# 엑셀 기반 100+ TC 데이터 주도 테스트 실행
python excel_test_runner.py

# 크리에이터 멤버십 & 결제 BVA 특화 테스트
python run_fanding_membership_qa.py

# 모바일(iPhone 14) 1:1 채팅 & 코인 결제 특화 테스트
python run_likey_mobile_qa.py
```

---

## 📂 폴더 구조 (Directory Structure)

```text
.
├── step1_tc_designer.py           # [Step 1] TC 설계 초안 및 기획 분석 보고서 생성
├── step2_quality_gate.py          # [Step 2] ISTQB/BVA 기준 품질 심사 게이트
├── step3_test_runner.py           # [Step 3] Playwright 브라우저 실측 실행
├── step4_defect_triage.py         # [Step 4] 결함 원인 분류(RCA) 및 Jira 티켓 생성
├── step5_release_commander.py     # [Step 5] 최종 Go/No-Go 판정 및 Slack JSON 생성
├── run_modular_qe_pipeline.py     # 5단계 마스터 오케스트레이터
├── excel_test_runner.py           # 엑셀 기반 대량 TC 데이터 주도 실행 엔진
├── run_fanding_membership_qa.py   # 멤버십 권한 및 결제 BVA 특화 파이프라인
├── run_likey_mobile_qa.py         # 모바일(iPhone 14) 채팅/코인 특화 파이프라인
├── setup.bat / setup.sh           # OS별 원클릭 환경 설치 스크립트
├── run_master.bat / run_master.sh # OS별 마스터 실행 스크립트
├── requirements.txt               # Python 의존성 패키지 목록
└── artifacts/                     # 단계별 중간 산출물, 보고서, 증빙 스크린샷
```
