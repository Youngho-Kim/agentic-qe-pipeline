# 📱 [LIKEY] 모바일 웹/앱 1:1 채팅 & 코인 결제 QA 종합 리포트

- **검증 일시**: 2026-11-12 13:25:23
- **테스트 환경**: Apple iPhone 14 Viewport (390 x 844, Touch Event)
- **테스트 통과율**: **5/5 건 (100.0%)**
- **최종 판정**: **🟢 GO (릴리즈 승인)**

## 1. 주요 검증 및 협업 요약 (Jira / Slack 대응)
본 테스트는 티피씨 LIKEY의 핵심 기능인 **크리에이터 1:1 채팅 인터랙션**과 **인앱 코인 차감/부족 상태 전이**를 모바일 실측 환경에서 멀티 에이전트 파이프라인으로 검증한 결과입니다.

## 2. 모바일 세부 테스트 실행 결과

| TC ID | 테스트 명세 | 분류 | 상태 | 검증 내용 | 모바일 스크린샷 |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `TC-LIKEY-001` | 모바일 뷰포트 반응형 헤더 및 기본 50코인 노출 확인 | MobileUI | ✅ PASS | iPhone 14 모바일 뷰포트 로드 및 50코인 확인 | [TC-LIKEY-001](likey_screenshots/TC-LIKEY-001_mobile_pass.png) |
| `TC-LIKEY-002` | 빈 메시지 전송 차단 및 경고 배너 검증 | Boundary | ✅ PASS | 공백 전송 차단 에러 배너 정상 노출 | [TC-LIKEY-002](likey_screenshots/TC-LIKEY-002_mobile_pass.png) |
| `TC-LIKEY-003` | 정상 메시지 입력 및 전송 버블 렌더링 확인 | Positive | ✅ PASS | 모바일 1:1 메시지 전송 버블 정상 렌더링 | [TC-LIKEY-003](likey_screenshots/TC-LIKEY-003_mobile_pass.png) |
| `TC-LIKEY-004` | 30코인 잠긴 사진 열람 시 잔액 차감(50 ➔ 20) 검증 | CoinBVA | ✅ PASS | 30코인 콘텐츠 잠금 해제 및 잔액 20코인 차감 검증 성공 | [TC-LIKEY-004](likey_screenshots/TC-LIKEY-004_mobile_pass.png) |
| `TC-LIKEY-005` | 잔여 20코인 상태에서 100코인 영상 클릭 시 코인 부족 차단 | AccessControl | ✅ PASS | 코인 부족 감지 및 충전소 이동 팝업 정상 차단 확인 | [TC-LIKEY-005](likey_screenshots/TC-LIKEY-005_mobile_pass.png) |

## 3. Slack 연동 안내
- 생성된 `likey_slack_notification.json` 파일의 블록 키트 페이로드를 사내 Slack Incoming Webhook에 그대로 전송할 수 있도록 설계되었습니다.
