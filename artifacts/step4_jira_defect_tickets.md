# 🚨 개발팀 공유용 Jira 결함 티켓

## [P1 (High)] TC-001: 정상 계정(standard_user) 로그인 및 인벤토리 진입
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '상품 목록 페이지 헤더 확인' vs 실제값 'Products' 불일치`

## [P1 (High)] TC-002: 잘못된 비밀번호 입력 시 로그인 실패 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '인증 실패 에러 메시지 확인' vs 실제값 'Epic sadface: Username and password do not match any user in this service' 불일치`

## [P1 (High)] TC-003: 아이디 미입력(빈값) 로그인 시도 유효성 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '아이디 필수값 에러 노출 확인' vs 실제값 'Epic sadface: Username is required' 불일치`

## [P1 (High)] TC-004: 비밀번호 미입력(빈값) 로그인 시도 유효성 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '비밀번호 필수값 에러 노출 확인' vs 실제값 'Epic sadface: Password is required' 불일치`

## [P1 (High)] TC-005: 아이디/비밀번호 모두 빈값 상태에서 로그인 시도
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '우선순위에 따른 아이디 필수 에러 노출' vs 실제값 'Epic sadface: Username is required' 불일치`

## [P1 (High)] TC-006: 잠긴 계정(locked_out_user) 로그인 차단 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '계정 잠김 알림 에러 확인' vs 실제값 'Epic sadface: Sorry, this user has been locked out.' 불일치`

## [P1 (High)] TC-007: 존재하지 않는 미등록 계정 로그인 차단 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '미등록 계정 불일치 에러 확인' vs 실제값 'Epic sadface: Username and password do not match any user in this service' 불일치`

## [P1 (High)] TC-008: 아이디 대소문자 구분 및 민감도 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '대소문자 불일치 에러 노출 확인' vs 실제값 'Epic sadface: Username and password do not match any user in this service' 불일치`

## [P2 (Medium)] TC-009: 아이디 앞뒤 공백 포함 시 트림(Trim) 처리 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.wait_for_selector: Timeout 5000ms exceeded.
Call log:
  - waiting for locator("[data-test='error']") to be visible
`

## [P1 (High)] TC-010: 로그인 입력창 SQL Injection 문자열 차단 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '인젝션 차단 및 일반 에러 노출' vs 실제값 'Epic sadface: Username and password do not match any user in this service' 불일치`

## [P1 (High)] TC-011: 로그인 입력창 XSS 스크립트 태그 처리 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '스크립트 미실행 및 안전한 에러 출력' vs 실제값 'Epic sadface: Username and password do not match any user in this service' 불일치`

## [P2 (Medium)] TC-013: 비인증 상태에서 /inventory.html 직접 URL 접근 차단
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.wait_for_selector: Timeout 5000ms exceeded.
Call log:
  - waiting for locator("[data-test='error']") to be visible
`

## [P2 (Medium)] TC-014: 비인증 상태에서 /cart.html 직접 URL 접근 차단
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.wait_for_selector: Timeout 5000ms exceeded.
Call log:
  - waiting for locator("[data-test='error']") to be visible
`

## [P2 (Medium)] TC-015: 비인증 상태에서 /checkout-step-one.html 직접 접근 차단
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.wait_for_selector: Timeout 5000ms exceeded.
Call log:
  - waiting for locator("[data-test='error']") to be visible
`

## [P2 (Medium)] TC-017: 로그아웃 후 브라우저 뒤로가기(Back) 세션 재진입 차단
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.wait_for_selector: Timeout 5000ms exceeded.
Call log:
  - waiting for locator("[data-test='error']") to be visible
`

## [P1 (High)] TC-020: 버그 계정(error_user) 로그인 후 기본 UI 로딩 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '상품 목록 타이틀 정상 렌더링 확인' vs 실제값 'Products' 불일치`

## [P1 (High)] TC-023: 기본 정렬 기본값(A to Z) 설정 상태 확인
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '기본 정렬 활성 옵션 확인' vs 실제값 'Name (A to Z)' 불일치`

## [P1 (High)] TC-024: 상품 이름 내림차순(Name: Z to A) 정렬 동작 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '첫 번째 상품 Z 정렬 확인' vs 실제값 'Sauce Labs Backpack' 불일치`

## [P1 (High)] TC-025: 상품 이름 오름차순(Name: A to Z) 재정렬 동작 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '첫 번째 상품 A 정렬 복귀 확인' vs 실제값 'Sauce Labs Backpack' 불일치`

## [P1 (High)] TC-026: 가격 낮은 순(Price: low to high) 정렬 동작 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '최저가 $7.99 상품 선두 노출 확인' vs 실제값 '$29.99' 불일치`

## [P1 (High)] TC-027: 가격 높은 순(Price: high to low) 정렬 동작 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '최고가 $49.99 상품 선두 노출 확인' vs 실제값 '$29.99' 불일치`

## [P1 (High)] TC-029: 인벤토리 화면에서 단일 상품 Add to cart 버튼 클릭 시 상태 토글
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '버튼 텍스트 Remove로 변경 확인' vs 실제값 'Remove' 불일치`

## [P2 (Medium)] TC-030: 인벤토리 화면에서 Remove 버튼 클릭 시 취소 및 버튼 원복 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-031: 상품 1개 추가 시 헤더 장바구니 뱃지 숫자 1 표시 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-032: 상품 3개 연속 추가 시 카트 뱃지 숫자 3 누적 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-033: 전체 6개 상품 모두 추가 시 카트 뱃지 숫자 6 표시 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-034: 상품 제거 후 뱃지 수량 감소 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-035: 모든 상품 제거 시 카트 뱃지 엘리먼트 제거 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P1 (High)] TC-039: 정렬 옵션 변경 후 새로고침 시 정렬 상태 지속성/초기화 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '새로고침 시 기본 정렬 복귀 확인' vs 실제값 'Name (A to Z)' 불일치`

## [P1 (High)] TC-040: 헤더 장바구니 아이콘 클릭 시 카트 페이지 이동 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '장바구니 페이지 타이틀 진입 확인' vs 실제값 'Your Cart' 불일치`

## [P1 (High)] TC-041: 상품 상세 화면 구성요소(이름, 상세설명, 가격, 이미지) 일치 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '상품명 일치 확인' vs 실제값 'Sauce Labs Backpack' 불일치`

## [P2 (Medium)] TC-042: 상세 화면에서 Add to cart 클릭 시 카트 뱃지 증가 및 버튼 전환
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-043: 상세 화면에서 Remove 클릭 시 카트 뱃지 제거 및 버튼 복귀
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P1 (High)] TC-044: Back to products 버튼 클릭 시 인벤토리 목록 복귀 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '인벤토리 목록 페이지 복귀 확인' vs 실제값 'Products' 불일치`

## [P2 (Medium)] TC-045: 목록에서 담은 상품의 상세 진입 시 Remove 상태 동기화 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P1 (High)] TC-046: Bike Light(id=0) 상세 정보 및 가격 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '상품명 확인' vs 실제값 'Sauce Labs Bike Light' 불일치`

## [P1 (High)] TC-047: Bolt T-Shirt(id=1) 상세 정보 및 가격 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '상품명 확인' vs 실제값 'Sauce Labs Bolt T-Shirt' 불일치`

## [P1 (High)] TC-048: Fleece Jacket(id=5) 상세 정보 및 최고가 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '상품명 확인' vs 실제값 'Sauce Labs Fleece Jacket' 불일치`

## [P1 (High)] TC-049: Onesie(id=2) 상세 정보 및 최저가 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '상품명 확인' vs 실제값 'Sauce Labs Onesie' 불일치`

## [P1 (High)] TC-050: 존재하지 않는 상품 id 파라미터 URL 예외 처리 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '미존재 상품 에러/안내 노출 검증' vs 실제값 'ITEM NOT FOUND' 불일치`

## [P2 (Medium)] TC-051: 담은 상품이 카트 목록(cart.html)에 정상 표시되는지 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-052: 카트 내에서 Remove 버튼 클릭 시 상품 삭제 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-053: 복수 상품 담긴 카트에서 특정 1개 상품만 선별 삭제 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P1 (High)] TC-054: 빈 장바구니에서 Continue Shopping 클릭 시 인벤토리 복귀
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '인벤토리 복귀 확인' vs 실제값 'Products' 불일치`

## [P2 (Medium)] TC-055: 상품 담긴 상태에서 Continue Shopping 클릭 후 이전 상태 유지 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-056: 카트 내 상품명 클릭 시 해당 상품 상세 화면으로 이동 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-057: 상품이 담긴 상태에서 Checkout 버튼 클릭 시 결제 1단계 진입
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-059: 장바구니 목록 가격과 인벤토리 가격 일치 여부 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-060: 카트 수량 컬럼 기본값 1 고정 표시 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-061: 동일 상품 중복 추가 시 수량 증가 여부(시스템 사양 확인)
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-062: 브라우저 새로고침(F5) 시 장바구니 세션 상태 유지 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P1 (High)] TC-063: 사이드바 All Items 클릭 시 인벤토리 복귀 및 카트 유지
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '상품 목록 복귀 확인' vs 실제값 'Products' 불일치`

## [P2 (Medium)] TC-064: 사이드바 Reset App State 클릭 시 카트 비우기 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P1 (High)] TC-065: 카트 테이블 헤더 QTY 및 Description 라벨 노출 확인
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '수량 라벨 노출' vs 실제값 'QTY' 불일치`

## [P1 (High)] TC-066: 정상 배송 정보 입력 후 결제 2단계(개요) 진입 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '결제 2단계 Overview 진입' vs 실제값 'Checkout: Your Information' 불일치`

## [P1 (High)] TC-067: First Name 빈값 상태에서 Continue 클릭 시 에러 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '이름 필수 입력 에러 노출' vs 실제값 'Error: Last Name is required' 불일치`

## [P1 (High)] TC-068: Last Name 빈값 상태에서 Continue 클릭 시 에러 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '성 필수 입력 에러 노출' vs 실제값 'Error: Last Name is required' 불일치`

## [P1 (High)] TC-069: Postal Code 빈값 상태에서 Continue 클릭 시 에러 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '우편번호 필수 입력 에러 노출' vs 실제값 'Error: Last Name is required' 불일치`

## [P1 (High)] TC-070: 모든 배송 필드 빈값 상태에서 Continue 클릭 시 우선순위 에러
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '첫 번째 필드인 이름 에러 최우선 노출' vs 실제값 'Error: First Name is required' 불일치`

## [P1 (High)] TC-071: 결제 1단계에서 Cancel 버튼 클릭 시 카트 페이지 복귀 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '카트 페이지 복귀 확인' vs 실제값 'Your Cart' 불일치`

## [P1 (High)] TC-072: 배송 정보에 특수문자 입력 시 정상 수용 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '특수문자 정상 처리 및 다음 단계 이동' vs 실제값 'Checkout: Your Information' 불일치`

## [P1 (High)] TC-074: 결제 2단계: 주문 요약 상품 목록 및 수량 일치 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '결제 정보 라벨 확인' vs 실제값 'Payment Information:' 불일치`

## [P2 (Medium)] TC-075: 결제 2단계: Payment Information 카드 정보 표기 확인
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.wait_for_selector: Timeout 5000ms exceeded.
Call log:
  - waiting for locator(".summary_value_label:nth-of-type(1)") to be visible
`

## [P1 (High)] TC-076: 결제 2단계: Shipping Information 배송 방식 표기 확인
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '배송 옵션 표기 일치' vs 실제값 'SauceCard #31337' 불일치`

## [P2 (Medium)] TC-077: 결제 2단계: 단일 상품 아이템 소계(Item total) 계산 정확도 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P1 (High)] TC-079: 결제 2단계: 총 결제 금액(Total = Item total + Tax) 합산 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '소계+세금($29.99+$2.40=$32.39) 총액 일치' vs 실제값 'Total: $64.78' 불일치`

## [P1 (High)] TC-080: 결제 2단계에서 Cancel 버튼 클릭 시 인벤토리 복귀 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '인벤토리 목록 페이지 복귀 확인' vs 실제값 'Products' 불일치`

## [P1 (High)] TC-081: Finish 버튼 클릭 시 최종 주문 완료 페이지 라우팅 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '주문 완료 화면 타이틀 확인' vs 실제값 'Checkout: Complete!' 불일치`

## [P1 (High)] TC-082: 주문 완료 화면: 감사 메시지(THANK YOU FOR YOUR ORDER) 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '최종 성공 완료 헤더 텍스트 확인' vs 실제값 'Thank you for your order!' 불일치`

## [P1 (High)] TC-083: 주문 완료 화면: 포니 익스프레스 배송 안내 문구 노출 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '배송 출고 안내 문구 확인' vs 실제값 'Your order has been dispatched, and will arrive just as fast as the pony can get there!' 불일치`

## [P1 (High)] TC-084: 주문 완료 후 Back Home 버튼 클릭 시 인벤토리 이동 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '상품 목록 페이지 복귀 확인' vs 실제값 'Products' 불일치`

## [P1 (High)] TC-092: 푸터 카피라이트 텍스트 및 현재 연도 표기 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '카피라이트 문구 검증' vs 실제값 '© 2026 Sauce Labs. All Rights Reserved. Terms of Service | Privacy Policy' 불일치`

## [P2 (Medium)] TC-097: 지연 계정(performance_glitch) 장바구니 추가 응답성 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P2 (Medium)] TC-098: 브라우저 다중 탭 환경에서 장바구니 수량 동기화 검증
- **분류**: 일시적 네트워크/렌더링 지연 (Flaky Issue)
- **에러 로그**: `Page.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("[data-test='add-to-cart-sauce-labs-backpack']")
`

## [P1 (High)] TC-099: 로그아웃 후 브라우저 캐시를 통한 주문 정보 잔존 여부 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '개인정보 화면 접근 차단 확인' vs 실제값 'Epic sadface: You can only access '/checkout-step-two.html' when you are logged in.' 불일치`

## [P1 (High)] TC-100: End-to-End 전체 풀 시나리오(로그인→검색/정렬→담기→결제→완료) 검증
- **분류**: 비즈니스 기획 불일치 또는 UI 문구 결함 (Functional Bug)
- **에러 로그**: `기대값 '주문 금액 검증' vs 실제값 'Item total: $37.98' 불일치`

## [P2 (Medium)] TC-API-01: 공개 API 조회 검증
- **분류**: UI 셀렉터 변경 또는 요소 미탐색 (DOM Locator Issue)
- **에러 로그**: `<urlopen error unknown url type: [https>`

## [P2 (Medium)] TC-API-02: 게시글 생성 POST 검증
- **분류**: UI 셀렉터 변경 또는 요소 미탐색 (DOM Locator Issue)
- **에러 로그**: `<urlopen error unknown url type: [https>`

