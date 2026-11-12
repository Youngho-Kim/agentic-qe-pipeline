# 📑 QE / Technical QA 포트폴리오 목차 초안 (Notion · PDF 제출용)

> **작성 전략**: GitHub 프로필 전체 대신 **문제 해결 스토리와 실제 실행 증빙(스크린샷·보고서·엑셀 결과)**을 3~4페이지 분량으로 압축해 보여주고, 마지막에 해당 프로젝트 저장소 직링크를 배치합니다.

---

## 1. 표지 및 핵심 요약 (Cover & Executive Summary)
* **제목**: 5단계 모듈형 AI-QE 자동화 파이프라인 및 데이터 주도 테스트(DDT) 프레임워크
* **한 줄 요약**: 기획 분석부터 품질 게이트 심사, 브라우저 실측, 결함 트리아지, 릴리즈 판정까지 QE의 중간 통제권을 보장하는 E2E 자동화 시스템
* **핵심 지표 / 성과 배지**:
  * 코드 수정 **0줄**로 **100건 이상** 엑셀 TC 일괄 자동 실행 및 결과 마킹
  * **5단계 중간 보고서(Audit Trail)** 기반 Human-in-the-Loop 품질 통제
  * Windows / macOS **원클릭 환경 구축(`setup.bat` / `setup.sh`)** 및 오프라인 독립 시연 지원
* **관련 링크**: GitHub 프로젝트 저장소 직링크 (`https://github.com/<아이디>/<저장소명>`)

---

## 2. 문제 정의 및 설계 의도 (Why I Built This)
* **기존 QA/AI 자동화의 3가지 한계**:
  1. **AI 환각 및 누락**: 단일 프롬프트로 TC를 생성하면 정상 시나리오 위주만 나와 경계값(BVA)·보안 예외가 빠짐
  2. **하드코딩 유지보수 한계**: 파이썬 코드에 TC를 직접 작성하면 100개 이상으로 확장 시 비개발 동료와 협업 불가능
  3. **블랙박스 자동화의 불신**: 중간 확인 없이 결과만 뱉는 구조는 실무 QE가 배포 승인(Sign-off) 책임을 지기 어려움
* **해결 방향**: 역할별 5개 독립 에이전트 모듈 분리 + 엑셀 DDT 엔진 결합

---

## 3. 시스템 아키텍처 (5-Step Modular Architecture)
* **시각 자료**: `Step 1 (설계) → Step 2 (품질 심사) → Step 3 (실행) → Step 4 (결함 분석) → Step 5 (릴리즈 판정)` 흐름도 이미지
* **단계별 QE 개입 및 산출물 표**:
  * Step 1: `step1_draft_testcases.xlsx` & 기획 분석 요약서 (QE 수동 보완 가능 지점)
  * Step 2: `step2_quality_gate_report.md` (85점 이상 통과 기준, BVA/보안 누락 시 반려)
  * Step 3: [Playwright](https://playwright.dev/) 실측 로그 및 스크린샷
  * Step 4: Flaky(지연) vs Functional Bug(기능 결함) 자동 분류 및 Jira 티켓 초안
  * Step 5: Go / No-Go 최종 사인오프 및 Slack Block Kit JSON 알림

---

## 4. 핵심 구현 1: 100+ TC 엑셀 데이터 주도 테스팅 (DDT)
* **시각 자료**: `test_cases.xlsx` 입력 시트 캡처 vs `test_results_executed.xlsx` 자동 마킹 결과 캡처 나란히 배치
* **강조할 포인트**:
  * [openpyxl](https://openpyxl.readthedocs.io/) 파서를 통해 `goto`, `fill`, `click`, `assert_text` 액션을 해석
  * 100개 이상의 TC를 코드 수정 없이 실행하고, 실패 발생 행(Row)에 빨간색 서식과 원시 에러 메모를 자동 기록해 비개발 직군과의 협업 효율 극대화

---

## 5. 핵심 구현 2: 도메인 특화 검증 (크리에이터 · 모바일 · 결제)
* **시나리오 A — 멤버십 권한 제어 & 결제 경계값(BVA)**:
  * 비구독/일반 회원의 VIP 콘텐츠 블라인드 차단 vs 골드 회원 잠금 해제 검증
  * 플랜 금액(14,900원) 초과 할인 쿠폰(20,000원) 적용 시 음수 결제 차단 및 **0원 바운딩** 검증
  * 정기 결제 실패 시 즉시 해지 차단 및 **3일 유예 기간(Grace Period)** 배너 상태 전이 확인
* **시나리오 B — 모바일(iPhone 14) 1:1 채팅 & 코인 결제**:
  * [Playwright](https://playwright.dev/) `iPhone 14` 디바이스 뷰포트(`390x844`) 에뮬레이션 적용
  * 공백 메시지 전송 차단, 30코인 차감 실시간 잔액 동기화(50 → 20), 잔액 부족 시 충전 모달 팝업 검증
* **시각 자료**: `fanding_screenshots/`, `likey_screenshots/` 내 주요 캡처 이미지 2~3장 첨부

---

## 6. 협업 자동화 및 이식성 (Collaboration & Portability)
* **협업 산출물 예시**: 실제 생성된 `step4_jira_defect_tickets.md`, `step5_release_signoff_report.md`, `likey_slack_notification.json` 일부 발췌
* **크로스 플랫폼 환경**: 어느 PC에서도 즉시 실행 가능한 `setup.bat` / `setup.sh` 및 로컬 내장 Mock 웹서버(면접장 오프라인 Live Demo 대응)

---

## 7. 트러블슈팅 및 회고 (Troubleshooting & Takeaways)
* **트러블슈팅 사례**: [Pydantic](https://docs.pydantic.dev/) v1/v2 업그레이드 과정에서 발생한 `suite.json(ensure_ascii=False)` `TypeError`를 `model_dump()` 호환 분기 처리로 해결한 경험
* **향후 고도화 계획**: GitHub Actions CI/CD 워크플로우 연동으로 PR 단위 자동 회귀 테스트 및 Slack 실시간 웹훅 발송 연결
