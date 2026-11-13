# 📊 [Step 3 보고서] Playwright 실측 실행 요약 보고서

- **실행 일시**: 2026-11-14 01:47:43
- **총 실행 건수**: 102건
- **성공**: 24건 | **실패**: 78건 (통과율: 23.5%)
- **요약 엑셀 보고서**: `artifacts\step3_test_results_report.xlsx`

## 1. 테스트 케이스별 실행 결과표

| TC ID | 테스트명 | 우선순위 | 결과 | 소요시간 | 증빙 스크린샷 |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `TC-001` | 정상 계정(standard_user) 로그인 및 인벤토리 진입 | **P0** | ❌ FAIL | 2.61s | [TC-001 캡처](artifacts/screenshots\TC-001_fail.png) |
| `TC-002` | 잘못된 비밀번호 입력 시 로그인 실패 검증 | **P1** | ❌ FAIL | 2.21s | [TC-002 캡처](artifacts/screenshots\TC-002_fail.png) |
| `TC-003` | 아이디 미입력(빈값) 로그인 시도 유효성 검증 | **P0** | ❌ FAIL | 1.69s | [TC-003 캡처](artifacts/screenshots\TC-003_fail.png) |
| `TC-004` | 비밀번호 미입력(빈값) 로그인 시도 유효성 검증 | **P0** | ❌ FAIL | 1.7s | [TC-004 캡처](artifacts/screenshots\TC-004_fail.png) |
| `TC-005` | 아이디/비밀번호 모두 빈값 상태에서 로그인 시도 | **P1** | ❌ FAIL | 1.15s | [TC-005 캡처](artifacts/screenshots\TC-005_fail.png) |
| `TC-006` | 잠긴 계정(locked_out_user) 로그인 차단 검증 | **P0** | ❌ FAIL | 2.18s | [TC-006 캡처](artifacts/screenshots\TC-006_fail.png) |
| `TC-007` | 존재하지 않는 미등록 계정 로그인 차단 검증 | **P1** | ❌ FAIL | 2.23s | [TC-007 캡처](artifacts/screenshots\TC-007_fail.png) |
| `TC-008` | 아이디 대소문자 구분 및 민감도 검증 | **P2** | ❌ FAIL | 2.2s | [TC-008 캡처](artifacts/screenshots\TC-008_fail.png) |
| `TC-009` | 아이디 앞뒤 공백 포함 시 트림(Trim) 처리 검증 | **P2** | ❌ FAIL | 7.19s | [TC-009 캡처](artifacts/screenshots\TC-009_fail.png) |
| `TC-010` | 로그인 입력창 SQL Injection 문자열 차단 검증 | **P1** | ❌ FAIL | 2.4s | [TC-010 캡처](artifacts/screenshots\TC-010_fail.png) |
| `TC-011` | 로그인 입력창 XSS 스크립트 태그 처리 검증 | **P1** | ❌ FAIL | 2.21s | [TC-011 캡처](artifacts/screenshots\TC-011_fail.png) |
| `TC-012` | 로그인 에러 메시지 닫기(X) 버튼 인터랙션 검증 | **P2** | ✅ PASS | 1.67s | [TC-012 캡처](artifacts/screenshots\TC-012_pass.png) |
| `TC-013` | 비인증 상태에서 /inventory.html 직접 URL 접근 차단 | **P0** | ❌ FAIL | 5.62s | [TC-013 캡처](artifacts/screenshots\TC-013_fail.png) |
| `TC-014` | 비인증 상태에서 /cart.html 직접 URL 접근 차단 | **P0** | ❌ FAIL | 5.64s | [TC-014 캡처](artifacts/screenshots\TC-014_fail.png) |
| `TC-015` | 비인증 상태에서 /checkout-step-one.html 직접 접근 차단 | **P0** | ❌ FAIL | 5.61s | [TC-015 캡처](artifacts/screenshots\TC-015_fail.png) |
| `TC-016` | 사이드바 메뉴를 통한 정상 로그아웃 세션 만료 검증 | **P0** | ✅ PASS | 3.24s | [TC-016 캡처](artifacts/screenshots\TC-016_pass.png) |
| `TC-017` | 로그아웃 후 브라우저 뒤로가기(Back) 세션 재진입 차단 | **P1** | ❌ FAIL | 8.26s | [TC-017 캡처](artifacts/screenshots\TC-017_fail.png) |
| `TC-018` | 비밀번호 입력 필드 마스킹(type=password) 보안 속성 검증 | **P2** | ✅ PASS | 0.56s | [TC-018 캡처](artifacts/screenshots\TC-018_pass.png) |
| `TC-019` | 지연 계정(performance_glitch_user) 명시적 대기 처리 검증 | **P1** | ✅ PASS | 7.17s | [TC-019 캡처](artifacts/screenshots\TC-019_pass.png) |
| `TC-020` | 버그 계정(error_user) 로그인 후 기본 UI 로딩 검증 | **P2** | ❌ FAIL | 2.23s | [TC-020 캡처](artifacts/screenshots\TC-020_fail.png) |
| `TC-021` | 기본 상품 목록 총 6개 아이템 렌더링 수량 검증 | **P0** | ✅ PASS | 0.6s | [TC-021 캡처](artifacts/screenshots\TC-021_pass.png) |
| `TC-022` | 각 상품 카드 필수 구성요소(이미지, 타이틀, 설명, 가격, 버튼) 검증 | **P1** | ✅ PASS | 0.59s | [TC-022 캡처](artifacts/screenshots\TC-022_pass.png) |
| `TC-023` | 기본 정렬 기본값(A to Z) 설정 상태 확인 | **P1** | ❌ FAIL | 0.63s | [TC-023 캡처](artifacts/screenshots\TC-023_fail.png) |
| `TC-024` | 상품 이름 내림차순(Name: Z to A) 정렬 동작 검증 | **P1** | ❌ FAIL | 0.64s | [TC-024 캡처](artifacts/screenshots\TC-024_fail.png) |
| `TC-025` | 상품 이름 오름차순(Name: A to Z) 재정렬 동작 검증 | **P1** | ❌ FAIL | 0.64s | [TC-025 캡처](artifacts/screenshots\TC-025_fail.png) |
| `TC-026` | 가격 낮은 순(Price: low to high) 정렬 동작 검증 | **P0** | ❌ FAIL | 0.65s | [TC-026 캡처](artifacts/screenshots\TC-026_fail.png) |
| `TC-027` | 가격 높은 순(Price: high to low) 정렬 동작 검증 | **P0** | ❌ FAIL | 0.65s | [TC-027 캡처](artifacts/screenshots\TC-027_fail.png) |
| `TC-028` | 상품 카드 가격 통화 기호($) 및 소수점 2자리 포맷 검증 | **P2** | ✅ PASS | 0.6s | [TC-028 캡처](artifacts/screenshots\TC-028_pass.png) |
| `TC-029` | 인벤토리 화면에서 단일 상품 Add to cart 버튼 클릭 시 상태 토글 | **P0** | ❌ FAIL | 1.17s | [TC-029 캡처](artifacts/screenshots\TC-029_fail.png) |
| `TC-030` | 인벤토리 화면에서 Remove 버튼 클릭 시 취소 및 버튼 원복 검증 | **P0** | ❌ FAIL | 31.09s | [TC-030 캡처](artifacts/screenshots\TC-030_fail.png) |
| `TC-031` | 상품 1개 추가 시 헤더 장바구니 뱃지 숫자 1 표시 검증 | **P0** | ❌ FAIL | 31.32s | [TC-031 캡처](artifacts/screenshots\TC-031_fail.png) |
| `TC-032` | 상품 3개 연속 추가 시 카트 뱃지 숫자 3 누적 검증 | **P1** | ❌ FAIL | 31.31s | [TC-032 캡처](artifacts/screenshots\TC-032_fail.png) |
| `TC-033` | 전체 6개 상품 모두 추가 시 카트 뱃지 숫자 6 표시 검증 | **P1** | ❌ FAIL | 31.1s | [TC-033 캡처](artifacts/screenshots\TC-033_fail.png) |
| `TC-034` | 상품 제거 후 뱃지 수량 감소 검증 | **P1** | ❌ FAIL | 31.15s | [TC-034 캡처](artifacts/screenshots\TC-034_fail.png) |
| `TC-035` | 모든 상품 제거 시 카트 뱃지 엘리먼트 제거 검증 | **P1** | ❌ FAIL | 31.12s | [TC-035 캡처](artifacts/screenshots\TC-035_fail.png) |
| `TC-036` | problem_user 로그인 시 상품 이미지 깨짐/동일 이미지 결함 감지 | **P2** | ✅ PASS | 2.21s | [TC-036 캡처](artifacts/screenshots\TC-036_pass.png) |
| `TC-037` | 상품 타이틀 클릭 시 해당 상세 페이지로 라우팅 검증 | **P0** | ✅ PASS | 1.17s | [TC-037 캡처](artifacts/screenshots\TC-037_pass.png) |
| `TC-038` | 상품 썸네일 이미지 클릭 시 상세 페이지로 라우팅 검증 | **P1** | ✅ PASS | 1.15s | [TC-038 캡처](artifacts/screenshots\TC-038_pass.png) |
| `TC-039` | 정렬 옵션 변경 후 새로고침 시 정렬 상태 지속성/초기화 검증 | **P2** | ❌ FAIL | 0.67s | [TC-039 캡처](artifacts/screenshots\TC-039_fail.png) |
| `TC-040` | 헤더 장바구니 아이콘 클릭 시 카트 페이지 이동 검증 | **P0** | ❌ FAIL | 1.18s | [TC-040 캡처](artifacts/screenshots\TC-040_fail.png) |
| `TC-041` | 상품 상세 화면 구성요소(이름, 상세설명, 가격, 이미지) 일치 검증 | **P0** | ❌ FAIL | 0.62s | [TC-041 캡처](artifacts/screenshots\TC-041_fail.png) |
| `TC-042` | 상세 화면에서 Add to cart 클릭 시 카트 뱃지 증가 및 버튼 전환 | **P0** | ❌ FAIL | 31.11s | [TC-042 캡처](artifacts/screenshots\TC-042_fail.png) |
| `TC-043` | 상세 화면에서 Remove 클릭 시 카트 뱃지 제거 및 버튼 복귀 | **P0** | ❌ FAIL | 31.1s | [TC-043 캡처](artifacts/screenshots\TC-043_fail.png) |
| `TC-044` | Back to products 버튼 클릭 시 인벤토리 목록 복귀 검증 | **P0** | ❌ FAIL | 1.21s | [TC-044 캡처](artifacts/screenshots\TC-044_fail.png) |
| `TC-045` | 목록에서 담은 상품의 상세 진입 시 Remove 상태 동기화 검증 | **P1** | ❌ FAIL | 31.11s | [TC-045 캡처](artifacts/screenshots\TC-045_fail.png) |
| `TC-046` | Bike Light(id=0) 상세 정보 및 가격 검증 | **P1** | ❌ FAIL | 0.68s | [TC-046 캡처](artifacts/screenshots\TC-046_fail.png) |
| `TC-047` | Bolt T-Shirt(id=1) 상세 정보 및 가격 검증 | **P1** | ❌ FAIL | 0.65s | [TC-047 캡처](artifacts/screenshots\TC-047_fail.png) |
| `TC-048` | Fleece Jacket(id=5) 상세 정보 및 최고가 검증 | **P1** | ❌ FAIL | 0.64s | [TC-048 캡처](artifacts/screenshots\TC-048_fail.png) |
| `TC-049` | Onesie(id=2) 상세 정보 및 최저가 검증 | **P1** | ❌ FAIL | 0.7s | [TC-049 캡처](artifacts/screenshots\TC-049_fail.png) |
| `TC-050` | 존재하지 않는 상품 id 파라미터 URL 예외 처리 검증 | **P2** | ❌ FAIL | 0.64s | [TC-050 캡처](artifacts/screenshots\TC-050_fail.png) |
| `TC-051` | 담은 상품이 카트 목록(cart.html)에 정상 표시되는지 검증 | **P0** | ❌ FAIL | 31.1s | [TC-051 캡처](artifacts/screenshots\TC-051_fail.png) |
| `TC-052` | 카트 내에서 Remove 버튼 클릭 시 상품 삭제 검증 | **P0** | ❌ FAIL | 31.13s | [TC-052 캡처](artifacts/screenshots\TC-052_fail.png) |
| `TC-053` | 복수 상품 담긴 카트에서 특정 1개 상품만 선별 삭제 검증 | **P1** | ❌ FAIL | 31.12s | [TC-053 캡처](artifacts/screenshots\TC-053_fail.png) |
| `TC-054` | 빈 장바구니에서 Continue Shopping 클릭 시 인벤토리 복귀 | **P0** | ❌ FAIL | 1.19s | [TC-054 캡처](artifacts/screenshots\TC-054_fail.png) |
| `TC-055` | 상품 담긴 상태에서 Continue Shopping 클릭 후 이전 상태 유지 검증 | **P1** | ❌ FAIL | 31.09s | [TC-055 캡처](artifacts/screenshots\TC-055_fail.png) |
| `TC-056` | 카트 내 상품명 클릭 시 해당 상품 상세 화면으로 이동 검증 | **P1** | ❌ FAIL | 31.11s | [TC-056 캡처](artifacts/screenshots\TC-056_fail.png) |
| `TC-057` | 상품이 담긴 상태에서 Checkout 버튼 클릭 시 결제 1단계 진입 | **P0** | ❌ FAIL | 31.31s | [TC-057 캡처](artifacts/screenshots\TC-057_fail.png) |
| `TC-058` | 빈 장바구니에서 Checkout 클릭 시 동작(방어 로직 검증) | **P2** | ✅ PASS | 1.78s | [TC-058 캡처](artifacts/screenshots\TC-058_pass.png) |
| `TC-059` | 장바구니 목록 가격과 인벤토리 가격 일치 여부 검증 | **P1** | ❌ FAIL | 31.09s | [TC-059 캡처](artifacts/screenshots\TC-059_fail.png) |
| `TC-060` | 카트 수량 컬럼 기본값 1 고정 표시 검증 | **P2** | ❌ FAIL | 31.13s | [TC-060 캡처](artifacts/screenshots\TC-060_fail.png) |
| `TC-061` | 동일 상품 중복 추가 시 수량 증가 여부(시스템 사양 확인) | **P2** | ❌ FAIL | 31.31s | [TC-061 캡처](artifacts/screenshots\TC-061_fail.png) |
| `TC-062` | 브라우저 새로고침(F5) 시 장바구니 세션 상태 유지 검증 | **P1** | ❌ FAIL | 31.12s | [TC-062 캡처](artifacts/screenshots\TC-062_fail.png) |
| `TC-063` | 사이드바 All Items 클릭 시 인벤토리 복귀 및 카트 유지 | **P1** | ❌ FAIL | 1.73s | [TC-063 캡처](artifacts/screenshots\TC-063_fail.png) |
| `TC-064` | 사이드바 Reset App State 클릭 시 카트 비우기 검증 | **P0** | ❌ FAIL | 31.15s | [TC-064 캡처](artifacts/screenshots\TC-064_fail.png) |
| `TC-065` | 카트 테이블 헤더 QTY 및 Description 라벨 노출 확인 | **P2** | ❌ FAIL | 0.74s | [TC-065 캡처](artifacts/screenshots\TC-065_fail.png) |
| `TC-066` | 정상 배송 정보 입력 후 결제 2단계(개요) 진입 검증 | **P0** | ❌ FAIL | 2.79s | [TC-066 캡처](artifacts/screenshots\TC-066_fail.png) |
| `TC-067` | First Name 빈값 상태에서 Continue 클릭 시 에러 검증 | **P0** | ❌ FAIL | 2.26s | [TC-067 캡처](artifacts/screenshots\TC-067_fail.png) |
| `TC-068` | Last Name 빈값 상태에서 Continue 클릭 시 에러 검증 | **P0** | ❌ FAIL | 2.27s | [TC-068 캡처](artifacts/screenshots\TC-068_fail.png) |
| `TC-069` | Postal Code 빈값 상태에서 Continue 클릭 시 에러 검증 | **P0** | ❌ FAIL | 2.27s | [TC-069 캡처](artifacts/screenshots\TC-069_fail.png) |
| `TC-070` | 모든 배송 필드 빈값 상태에서 Continue 클릭 시 우선순위 에러 | **P1** | ❌ FAIL | 1.26s | [TC-070 캡처](artifacts/screenshots\TC-070_fail.png) |
| `TC-071` | 결제 1단계에서 Cancel 버튼 클릭 시 카트 페이지 복귀 검증 | **P1** | ❌ FAIL | 1.23s | [TC-071 캡처](artifacts/screenshots\TC-071_fail.png) |
| `TC-072` | 배송 정보에 특수문자 입력 시 정상 수용 검증 | **P2** | ❌ FAIL | 2.78s | [TC-072 캡처](artifacts/screenshots\TC-072_fail.png) |
| `TC-073` | 배송 정보 공백(Space)만 입력 시 유효성 검증 | **P2** | ✅ PASS | 2.76s | [TC-073 캡처](artifacts/screenshots\TC-073_pass.png) |
| `TC-074` | 결제 2단계: 주문 요약 상품 목록 및 수량 일치 검증 | **P0** | ❌ FAIL | 0.66s | [TC-074 캡처](artifacts/screenshots\TC-074_fail.png) |
| `TC-075` | 결제 2단계: Payment Information 카드 정보 표기 확인 | **P1** | ❌ FAIL | 5.6s | [TC-075 캡처](artifacts/screenshots\TC-075_fail.png) |
| `TC-076` | 결제 2단계: Shipping Information 배송 방식 표기 확인 | **P1** | ❌ FAIL | 0.69s | [TC-076 캡처](artifacts/screenshots\TC-076_fail.png) |
| `TC-077` | 결제 2단계: 단일 상품 아이템 소계(Item total) 계산 정확도 검증 | **P0** | ❌ FAIL | 31.14s | [TC-077 캡처](artifacts/screenshots\TC-077_fail.png) |
| `TC-078` | 결제 2단계: 8% 세율(Tax) 자동 계산 정확도 검증 | **P0** | ✅ PASS | 0.59s | [TC-078 캡처](artifacts/screenshots\TC-078_pass.png) |
| `TC-079` | 결제 2단계: 총 결제 금액(Total = Item total + Tax) 합산 검증 | **P0** | ❌ FAIL | 0.63s | [TC-079 캡처](artifacts/screenshots\TC-079_fail.png) |
| `TC-080` | 결제 2단계에서 Cancel 버튼 클릭 시 인벤토리 복귀 검증 | **P1** | ❌ FAIL | 1.19s | [TC-080 캡처](artifacts/screenshots\TC-080_fail.png) |
| `TC-081` | Finish 버튼 클릭 시 최종 주문 완료 페이지 라우팅 검증 | **P0** | ❌ FAIL | 1.18s | [TC-081 캡처](artifacts/screenshots\TC-081_fail.png) |
| `TC-082` | 주문 완료 화면: 감사 메시지(THANK YOU FOR YOUR ORDER) 검증 | **P0** | ❌ FAIL | 0.64s | [TC-082 캡처](artifacts/screenshots\TC-082_fail.png) |
| `TC-083` | 주문 완료 화면: 포니 익스프레스 배송 안내 문구 노출 검증 | **P1** | ❌ FAIL | 0.63s | [TC-083 캡처](artifacts/screenshots\TC-083_fail.png) |
| `TC-084` | 주문 완료 후 Back Home 버튼 클릭 시 인벤토리 이동 검증 | **P0** | ❌ FAIL | 1.2s | [TC-084 캡처](artifacts/screenshots\TC-084_fail.png) |
| `TC-085` | 주문 완료 후 장바구니 뱃지 자동 비워짐(초기화) 검증 | **P0** | ✅ PASS | 0.58s | [TC-085 캡처](artifacts/screenshots\TC-085_pass.png) |
| `TC-086` | 사이드바 메뉴 열기(햄버거 버튼) 인터랙션 검증 | **P1** | ✅ PASS | 1.13s | [TC-086 캡처](artifacts/screenshots\TC-086_pass.png) |
| `TC-087` | 사이드바 닫기(X 버튼) 인터랙션 검증 | **P1** | ✅ PASS | 1.67s | [TC-087 캡처](artifacts/screenshots\TC-087_pass.png) |
| `TC-088` | 사이드바 About 링크 클릭 시 Sauce Labs 공식 사이트 이동 | **P1** | ✅ PASS | 2.31s | [TC-088 캡처](artifacts/screenshots\TC-088_pass.png) |
| `TC-089` | 푸터 트위터(X) SNS 링크 URL 및 새 창 타겟 속성 검증 | **P2** | ✅ PASS | 0.66s | [TC-089 캡처](artifacts/screenshots\TC-089_pass.png) |
| `TC-090` | 푸터 페이스북(Facebook) SNS 링크 URL 및 새 창 검증 | **P2** | ✅ PASS | 0.58s | [TC-090 캡처](artifacts/screenshots\TC-090_pass.png) |
| `TC-091` | 푸터 링크드인(LinkedIn) SNS 링크 URL 및 새 창 검증 | **P2** | ✅ PASS | 0.57s | [TC-091 캡처](artifacts/screenshots\TC-091_pass.png) |
| `TC-092` | 푸터 카피라이트 텍스트 및 현재 연도 표기 검증 | **P2** | ❌ FAIL | 0.64s | [TC-092 캡처](artifacts/screenshots\TC-092_fail.png) |
| `TC-093` | 모바일 해상도(390x844)에서 반응형 UI 레이아웃 검증 | **P1** | ✅ PASS | 0.58s | [TC-093 캡처](artifacts/screenshots\TC-093_pass.png) |
| `TC-094` | 태블릿 해상도(768x1024)에서 네비게이션 및 그리드 검증 | **P2** | ✅ PASS | 0.61s | [TC-094 캡처](artifacts/screenshots\TC-094_pass.png) |
| `TC-095` | problem_user 체크아웃 시 성(Last Name) 입력 필드 잠김 결함 감지 | **P1** | ✅ PASS | 3.83s | [TC-095 캡처](artifacts/screenshots\TC-095_pass.png) |
| `TC-096` | error_user 체크아웃 2단계 진입 시 에러 발생 감지 | **P1** | ✅ PASS | 4.89s | [TC-096 캡처](artifacts/screenshots\TC-096_pass.png) |
| `TC-097` | 지연 계정(performance_glitch) 장바구니 추가 응답성 검증 | **P2** | ❌ FAIL | 37.68s | [TC-097 캡처](artifacts/screenshots\TC-097_fail.png) |
| `TC-098` | 브라우저 다중 탭 환경에서 장바구니 수량 동기화 검증 | **P2** | ❌ FAIL | 31.1s | [TC-098 캡처](artifacts/screenshots\TC-098_fail.png) |
| `TC-099` | 로그아웃 후 브라우저 캐시를 통한 주문 정보 잔존 여부 검증 | **P1** | ❌ FAIL | 2.41s | [TC-099 캡처](artifacts/screenshots\TC-099_fail.png) |
| `TC-100` | End-to-End 전체 풀 시나리오(로그인→검색/정렬→담기→결제→완료) 검증 | **P0** | ❌ FAIL | 5.89s | [TC-100 캡처](artifacts/screenshots\TC-100_fail.png) |
| `TC-API-01` | 공개 API 조회 검증 | **P0** | ❌ FAIL | 0.06s | [TC-API-01 캡처](artifacts/screenshots\TC-API-01_fail.png) |
| `TC-API-02` | 게시글 생성 POST 검증 | **P1** | ❌ FAIL | 0.0s | [TC-API-02 캡처](artifacts/screenshots\TC-API-02_fail.png) |
