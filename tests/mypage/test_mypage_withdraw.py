# tests/test_mypage_06.py
# 마이페이지 > 계정 관리 — 계정 탈퇴 E2E 테스트 — FHC-084 ~ FHC-086
# ※ FHC-086 계정 탈퇴 후 동일 함수 내에서 동일 계정으로 재가입하여 복구

import logging
import pytest
import allure

from pages.mypage.mypage_withdraw_page import MyPage06

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("MyPage"),
    allure.feature("계정 탈퇴"),
    allure.story("계정 탈퇴 해피 케이스"),
]

MAIN_EMAIL    = "test_dummy@naver.com"
MAIN_PASSWORD = "test@1234"
MAIN_NAME     = "포커스 테스트"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def mypage(tools_driver_module):
    """
    MyPage06 fixture (모듈 공유)

    전제: tools_driver_module fixture로 로그인 완료 상태
    단계:
      1. tools_driver_module에서 driver 수신 → MyPage06 반환
    """
    page = MyPage06(tools_driver_module)
    page.login()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.title("[FHC-084~086] 계정 탈퇴 해피 케이스")
@allure.severity(allure.severity_level.CRITICAL)
def test_withdraw_happy_case(mypage):
    """
    [FHC-084~086] 계정 탈퇴 해피 케이스

    전제: 로그인 완료 상태
    단계:
      1. [FHC-084] 마이페이지 > 계정 관리 → 하단 '계정 탈퇴' 영역 이동
      2. [FHC-085] [탈퇴하기] 버튼 클릭 → 2차 확인 문구 표시
      3. [FHC-086] 탈퇴 확인 텍스트 입력 → 탈퇴 완료
      4. [인프라] 탈퇴 후 동일 계정으로 재가입하여 계정 복구
    기대: 로그인 랜딩 페이지로 이동한다 / 재가입 후 헬피 챗 메인 페이지로 접속된다
    """
    with allure.step("[FHC-084] 계정 탈퇴 영역 확인"):
        logger.info("[FHC-084] 계정 탈퇴 영역 확인 시작")
        mypage.navigate_to_account()
        mypage.scroll_to_withdraw_area()
        assert mypage.is_withdraw_area_displayed(), \
            "계정 탈퇴 영역 또는 [탈퇴하기] 버튼이 표시되지 않았습니다"

    with allure.step("[FHC-085] 계정 탈퇴 2차 확인 문구"):
        logger.info("[FHC-085] 계정 탈퇴 2차 확인 문구 시작")
        mypage.click_withdraw_button()
        assert mypage.is_withdraw_confirm_message_displayed(), \
            "탈퇴하기 클릭 후 2차 확인 문구('Delete [이메일]' 입력 안내)가 표시되지 않았습니다"

    with allure.step("[FHC-086] 계정 탈퇴"):
        logger.info("[FHC-086] 계정 탈퇴 시작")
        mypage.enter_withdraw_confirm_text(MAIN_EMAIL)
        mypage.submit_withdraw()
        assert mypage.is_withdrawal_complete(), \
            "계정 탈퇴 후 로그인 랜딩 페이지로 이동하지 못했습니다"

    with allure.step("[인프라] 탈퇴 후 계정 재가입"):
        logger.info("[인프라] 탈퇴 후 계정 재가입 시작")
        mypage.driver.get(mypage.CHAT_URL)
        mypage.signup(MAIN_EMAIL, MAIN_PASSWORD, MAIN_NAME)
        assert mypage.is_signup_success(), \
            f"탈퇴 후 재가입 시 helpy-chat 메인 페이지로 이동하지 못했습니다 (이메일: {MAIN_EMAIL})"

    logger.info("[FHC-084~086] 계정 탈퇴 및 계정 복구 완료")
