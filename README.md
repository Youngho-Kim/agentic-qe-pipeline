# 🛡️ Agentic-QE Closed-Loop Platform
[https://github.com/Youngho-Kim/agentic-qe-pipeline/actions/workflows/qe_ci.yml/badge.svg]

> **배포 전 5단계 AI-QE 자동화 파이프라인(엑셀 DDT · Jira 중복방지 연동)과 배포 후 실시간 서비스 헬스체크 대시보드(Sentinel)가 하나로 순환하는 올인원 QE 플랫폼**

---

## 📌 프로젝트 개요 (Overview)

* **해결하고자 한 문제**:
  * 단일 LLM 테스트 생성의 경계값(BVA) 누락 및 블랙박스 자동화의 신뢰성 저하
  * 코드 하드코딩 방식의 유지보수 한계(100+ TC 확장 불가) 및 반복 실행 시 Jira 중복 티켓 생성 문제
  * 배포 전 QA와 배포 후 운영 관제가 단절되어 장애 발생 시 회귀 테스트로 즉시 이어지지 않는 한계
* **구축한 해결책**:
  * **Closed-Loop 순환 구조**: QA가 `GO(배포 승인)`를 내리면 테스트 URL을 Sentinel 모니터링에 자동 등록하고, 운영 중 `CRITICAL` 장애가 감지되면 Playwright E2E 회귀 테스트(`Step 3~4`)를 자동 재가동합니다.
  * **5단계 Human-in-the-Loop**: 설계(`Step 1`) → 품질 심사(`Step 2`) → 브라우저 실행(`Step 3`) → 결함 원인 분석 & Jira 등록(`Step 4`) → 최종 판정(`Step 5`)마다 `artifacts/`에 중간 보고서를 남깁니다.
  * **엑셀 데이터 주도 테스팅(DDT) & 요약 대시보드**: 코드 수정 없이 `test_cases.xlsx`로 100건 이상의 TC를 일괄 실행하고, `테스트_요약` 대시보드 시트가 포함된 `step3_test_results_report.xlsx`를 자동 생성합니다.
  * **Jira Cloud 연동 & 중복 등록 방지**: [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/)로 버그 티켓을 자동 생성하되, 로컬 레지스트리와 실시간 JQL(`statusCategory != Done`) 조회로 동일 결함의 중복 티켓 생성을 차단합니다.

---

## 🏗️ Closed-Loop 아키텍처

```text
[Step 1] step1_tc_designer.py       ──► 초안 엑셀 & 기획 분석 보고서 (또는 test_cases.xlsx 자동 감지)
   │
   ▼
[Step 2] step2_quality_gate.py      ──► ISTQB/BVA 기준 품질 심사 (85점 이상 통과 시 승인)
   │
   ▼
[Step 3] step3_test_runner.py       ──► Playwright 실측 실행 & 요약 대시보드 엑셀(step3_test_results_report.xlsx)
   │
   ▼
[Step 4] step4_defect_triage.py     ──► Flaky vs Bug RCA 분류 & Jira Cloud 중복방지 티켓 발행
   │
   ▼
[Step 5] step5_release_commander.py ──► 최종 Go/No-Go 판정 & Slack JSON 생성
   │
   ├── (GO 승인 시 테스트 URL 자동 동기화) ──► [Sentinel 실시간 서비스 헬스체크 대시보드]
   │                                              │  (단발 순단 오탐 필터링: HEALTHY → SUSPECT → CRITICAL)
   └──◄── (CRITICAL 장애 확정 시 Step 3~4 자동 출동) ──┘
```

---

## ✨ 주요 모듈 및 기능

| 구분 | 파일 / 폴더 | 핵심 기능 |
| :--- | :--- | :--- |
| **통합 런처** | `qe_launcher.py` / `run_all.bat` | 배포 전 5단계 QA, 배포 후 Sentinel 대시보드, 도메인 시연을 통합 실행 |
| **5단계 QA** | `step1` ~ `step5` / `run_modular_qe_pipeline.py` | 역할별 분리 모듈 및 단계별 마크다운 중간 보고서(`artifacts/`) 생성 |
| **엑셀 DDT** | `step3_test_runner.py` | 100+ TC 자동 실행 및 `테스트_요약`(통과율·집계) + `상세_실행결과` 엑셀 산출 |
| **Jira 연동** | `jira_connector.py` | [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/) 버그 티켓 자동 등록 및 2중 중복 방지(JQL + 로컬 캐시) |
| **실시간 관제** | `sentinel_monitor/` | 내장 웹 대시보드(`127.0.0.1:8900`), 오탐 필터링 상태 머신, Slack 알림 연동 |
| **도메인 시연** | `run_fanding_membership_qa.py`, `run_likey_mobile_qa.py` | 멤버십 권한·쿠폰 음수 결제 BVA, `iPhone 14` 모바일 1:1 채팅·코인 결제 검증 |
| **외부 설정** | `config.json` / `config_loader.py` | 경로, 심사 점수, 브라우저 옵션, Jira 설정을 코드에서 분리 관리 |

---

## 🛠️ 기술 스택 (Tech Stack)

* **Language**: [Python](https://www.python.org/) 3.11+
* **E2E & Mobile Automation**: [Playwright](https://playwright.dev/) (Desktop Chromium & `iPhone 14` Viewport Emulation)
* **Excel DDT & Reporting**: [openpyxl](https://openpyxl.readthedocs.io/)
* **Data Validation**: [Pydantic](https://docs.pydantic.dev/) v2
* **Monitoring & API**: Python Standard Library (`ThreadingHTTPServer`, `urllib.request`), [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/), Slack Incoming Webhook
* **Automation Scripts**: Windows Batch (`.bat`), Bash Shell (`.sh`)

---

## 🚀 빠른 시작 (Quickstart)

### 1. 원클릭 환경 설치 (최초 1회)
* **Windows 11**: `setup.bat` 더블 클릭
* **macOS / Linux**:
  ```bash
  bash setup.sh
  ```

### 2. 통합 런처 실행
* **Windows 11**: `run_all.bat` 더블 클릭
* **터미널 직접 실행**:
  ```bash
  python qe_launcher.py
  ```

### 3. Jira 연동 설정 (선택 사항)
`config.json`의 `"jira"` 항목에 본인의 Jira Cloud 도메인, 이메일, API 토큰, 프로젝트 키를 입력하면 Step 4에서 실제 이슈가 등록됩니다. *(보안을 위해 저장소에는 토큰을 비워둔 상태로 유지합니다.)*

---

## 📂 프로젝트 구조 (Directory Structure)

```text
.
├── qe_launcher.py                 # 통합 메뉴 런처 (QA / Sentinel / 도메인 시연)
├── run_all.bat                    # Windows 통합 원클릭 실행기
├── setup.bat / setup.sh           # OS별 원클릭 환경 설치 스크립트
├── requirements.txt               # 의존성 패키지 목록
├── config.json / config_loader.py # 외부 설정 파일 및 로더
├── test_cases.xlsx                # 사용자 작성 100+ TC 엑셀 (자동 감지)
├── run_modular_qe_pipeline.py     # 5단계 QA 파이프라인 마스터 오케스트레이터
├── step1_tc_designer.py           # [Step 1] TC 초안 설계
├── step2_quality_gate.py          # [Step 2] ISTQB/BVA 품질 심사
├── step3_test_runner.py           # [Step 3] Playwright 실행 & 요약 대시보드 엑셀 생성
├── step4_defect_triage.py         # [Step 4] RCA 분석 & Jira 중복방지 티켓 발행
├── step5_release_commander.py     # [Step 5] Go/No-Go 판정 & Sentinel 자동 연계
├── jira_connector.py              # Jira Cloud REST API + JQL 중복 방지 모듈
├── run_fanding_membership_qa.py   # 멤버십 권한 & 결제 BVA 시연
├── run_likey_mobile_qa.py         # 모바일(iPhone 14) 1:1 채팅 & 코인 결제 시연
├── sentinel_monitor/              # 실시간 서비스 헬스체크 웹 대시보드 모듈
│   ├── monitor_config.json        # 감시 대상 URL 및 임계치 설정
│   ├── config_manager.py          # 설정 로드/저장
│   ├── probe_collector.py         # HTTP 응답 및 지연시간 측정
│   ├── noise_filter.py            # 오탐 필터링 상태 머신
│   ├── notifier.py                # Slack 알림 및 상태 보고서 생성
│   ├── dashboard_server.py        # 웹 대시보드 서버 & Closed-Loop QA 트리거
│   ├── sentinel_app.py            # 대시보드 실행 엔트리포인트
│   └── run_monitor.bat            # 모니터링 단독 실행기
└── artifacts/                     # 단계별 보고서, 요약 엑셀, 증빙 스크린샷
```
