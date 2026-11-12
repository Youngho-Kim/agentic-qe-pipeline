## QE가 단계마다 중간 보고서(Artifacts)를 직접 검토하고 통제할 수 있는 '5단계 독립 모듈형 아키텍처'로 프로젝트를 전면 리팩토링했습니다!

> 이제 5개의 에이전트가 각자의 명확한 역할과 책임을 가지며, 단계마다 엑셀 파일과 1페이지 마크다운 중간 보고서를 artifacts/ 폴더에 남기게 됩니다.


### 리팩토링된 5단계 모듈 아키텍처 및 보고 체계

qa-agent-project/
├── step1_tc_designer.py        # [모듈 1] 기획 분석 및 TC 설계자 (Draft 생성)
├── step2_quality_gate.py       # [모듈 2] ISTQB/BVA 품질 심사관 (QE 검토/승인 게이트)
├── step3_test_runner.py        # [모듈 3] Playwright 브라우저 실측 실행자 (E2E 실행)
├── step4_defect_triage.py      # [모듈 4] 결함 원인 분석가 (RCA 분석 및 Jira 티켓 생성)
├── step5_release_commander.py  # [모듈 5] 최종 릴리즈 총괄관 (Go/No-Go 판정 및 슬랙 브리핑)
└── run_modular_qe_pipeline.py  # [통합] 5단계 전 과정을 순차 연결하는 마스터 오케스트레이터


#### step1_tc_designer.py (설계 에이전트)
> 역할: 기획서를 분석해 TC 초안 엑셀(step1_draft_testcases.xlsx)과 기획 분석 요약서(step1_design_report.md)를 작성합니다.

#### step2_quality_gate.py (심사 에이전트)
> 역할: Step 1 엑셀을 심사하여 점수를 매기고, 통과 시 실행용 엑셀(step2_approved_testcases.xlsx)과 심사 보고서(step2_quality_gate_report.md)를 발행합니다.

#### step3_test_runner.py (실행 에이전트)
> 역할: 승인된 엑셀을 읽어 브라우저를 가동하고, 원시 로그(step3_raw_execution_logs.json)와 스크린샷, 실행 요약서(step3_execution_summary.md)를 산출합니다.

#### step4_defect_triage.py (결함 분석 에이전트)
> 역할: 로그를 분석해 Flaky 지연인지 실제 버그인지 판별하고, 트리아지 보고서(step4_triage_report.md)와 개발팀용 Jira 티켓을 작성합니다.

#### step5_release_commander.py (총괄 에이전트)
> 역할: 종합 감사 및 최종 릴리즈 승인서(step5_release_signoff_report.md)와 슬랙 알림 파일(step5_slack_broadcast.json)을 생성합니다.

#### run_modular_qe_pipeline.py (마스터 오케스트레이터)
> 역할: 5개 모듈을 순차적으로 연결해 가동하며, 단계마다 중간 보고서가 만들어지는 과정을 보여줍니다.


#### 실행 방법
> 터미널에서 마스터 스크립트를 실행합니다:

```bash
python run_modular_qe_pipeline.py
```
> 또는 단계별로 따로 실행하여 각 단계의 보고서를 중간중간 확인하실 수도 있습니다:


```bash
python step1_tc_designer.py      # 1단계만 실행 -> artifacts/step1_design_report.md 확인
python step2_quality_gate.py     # 2단계 심사 -> artifacts/step2_quality_gate_report.md 확인
python step3_test_runner.py      # 3단계 브라우저 실행 -> artifacts/step3_execution_summary.md 확인
python step4_defect_triage.py    # 4단계 결함 분석 -> artifacts/step4_triage_report.md 확인
python step5_release_commander.py# 5단계 릴리즈 승인 -> artifacts/step5_release_signoff_report.md 확인
```
> 실행해 보시면 artifacts/ 폴더 안에 각 단계별 엑셀 파일과 마크다운 중간 보고서들이 질서정연하게 쌓이는 것을 보실 수 있습니다