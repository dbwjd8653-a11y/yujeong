# tests/test_mypage_05.py
# 마이페이지 > 계정 관리 — 기본 정보 E2E 테스트 — FHC-080 ~ FHC-083

import pytest
import allure

from pages.mypage.mypage_account_page import MyPage05

pytestmark = [
    allure.epic("MyPage"),
    allure.feature("계정 관리"),
]

MAIN_EMAIL    = "test_dummy@naver.com"
MAIN_PASSWORD = "test@1234"
NEW_PASSWORD  = "test@4321"
NEW_NAME      = "포커스 테스트"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def mypage(tools_driver_module):
    """
    MyPage05 fixture (모듈 공유)

    전제: tools_driver_module fixture로 로그인 완료 상태
    단계:
      1. tools_driver_module에서 driver 수신 → MyPage05 반환
    """
    page = MyPage05(tools_driver_module)
    page.login()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("이름 변경")
@allure.title("[FHC-080] 이름 변경")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_080_change_name(mypage):
    """
    [FHC-080] 이름 변경

    전제: 로그인 상태
    단계:
      1. '계정 관리' 영역 클릭
      2. '이름' 옆 수정 버튼 클릭
      3. 새 이름 입력 후 저장
    기대: '저장되었습니다' 메시지 출력 후 이름 변경 적용됨
    """
    mypage.navigate_to_account()
    mypage.click_name_edit()
    mypage.enter_name(NEW_NAME)
    mypage.save_name()
    assert mypage.is_save_success_toast_displayed(), \
        "이름 변경 후 '저장되었습니다' 메시지가 표시되지 않았습니다"


@allure.story("비밀번호 변경")
@allure.title("[FHC-081] 비밀번호 변경")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_081_change_password(mypage):
    """
    [FHC-081] 비밀번호 변경

    전제: 로그인 상태
    단계:
      1. '계정 관리' 영역 클릭
      2. '비밀번호' 옆 수정 버튼 클릭
      3. 새 비밀번호 입력 후 저장
      4. 검증 후 원래 비밀번호로 복구
    기대: '저장되었습니다' 메시지 출력 후 비밀번호 변경 적용됨
    """
    mypage.navigate_to_account()
    mypage.click_password_edit()
    mypage.change_password(MAIN_PASSWORD, NEW_PASSWORD)
    assert mypage.is_save_success_toast_displayed(), \
        "비밀번호 변경 후 '저장되었습니다' 메시지가 표시되지 않았습니다"
    mypage.navigate_to_account()
    mypage.click_password_edit()
    mypage.change_password(NEW_PASSWORD, MAIN_PASSWORD)


@allure.story("프로모션 알림 설정 변경")
@allure.title("[FHC-082] 프로모션 알림 설정 변경")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_082_toggle_promotion(mypage):
    """
    [FHC-082] 프로모션 알림 설정 변경

    전제: 로그인 상태
    단계:
      1. '프로모션 알림' 영역 이동
      2. '프로모션 알림 받기' 클릭
    기대: 프로모션 알림 토글 시 'Saved successfully' 메시지 출력 및 상태 변경됨
    """
    mypage.navigate_to_account()
    before = mypage.get_promotion_state()
    mypage.toggle_promotion()
    assert mypage.is_saved_successfully_displayed(), \
        "프로모션 알림 토글 후 'Saved successfully' 메시지가 표시되지 않았습니다"
    after = mypage.get_promotion_state()
    assert before != after, \
        f"프로모션 알림 상태가 변경되지 않았습니다 (전: {before}, 후: {after})"


@allure.story("선호 언어 설정 변경")
@allure.title("[FHC-083] 선호 언어 설정 변경")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_083_change_language(mypage):
    """
    [FHC-083] 선호 언어 설정 변경

    전제: 로그인 상태
    단계:
      1. '선호 언어' 영역 이동
      2. 한국어(ko-KR) 선택
    기대: 언어 변경 및 'Saved successfully' 메시지 출력
    """
    mypage.navigate_to_account()
    mypage.change_language("ko-KR")
    assert mypage.is_saved_successfully_displayed(), \
        "언어 변경 후 'Saved successfully' 메시지가 표시되지 않았습니다"
