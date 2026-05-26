# tests/test_mypage_06.py
# 마이페이지 > 계정 관리 — 계정 탈퇴 E2E 테스트 — FHC-084 ~ FHC-086
# ※ FHC-086 계정 탈퇴 후 test_recreate_account_after_withdraw에서 동일 계정으로 재가입하여 복구

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
    기대: 로그인 랜딩 페이지로 이동한다
    """
    with allure.step("[FHC-084] 계정 탈퇴 영역 확인"):
        logger.info("[FHC-084] 계정 탈퇴 영역 확인 시작")
        with allure.step("r: 로그인 완료 상태"):
            pass
        with allure.step("g: 계정 관리 → 탈퇴 영역 스크롤 → 탈퇴 버튼 표시 확인"):
            mypage.navigate_to_account()
            mypage.scroll_to_withdraw_area()
            assert mypage.is_withdraw_area_displayed(), \
                "계정 탈퇴 영역 또는 [탈퇴하기] 버튼이 표시되지 않았습니다"

    with allure.step("[FHC-085] 계정 탈퇴 2차 확인 문구"):
        logger.info("[FHC-085] 계정 탈퇴 2차 확인 문구 시작")
        with allure.step("r: 계정 탈퇴 영역 확인 완료 상태"):
            pass
        with allure.step("g: 탈퇴하기 클릭 → 2차 확인 문구 표시 확인"):
            mypage.click_withdraw_button()
            assert mypage.is_withdraw_confirm_message_displayed(), \
                "탈퇴하기 클릭 후 2차 확인 문구('Delete [이메일]' 입력 안내)가 표시되지 않았습니다"

    with allure.step("[FHC-086] 계정 탈퇴"):
        logger.info("[FHC-086] 계정 탈퇴 시작")
        with allure.step("r: 2차 확인 문구 표시 상태"):
            pass
        with allure.step("g: 탈퇴 확인 텍스트 입력 → 탈퇴 완료 → 로그인 페이지 이동 확인"):
            mypage.enter_withdraw_confirm_text(MAIN_EMAIL)
            mypage.submit_withdraw()
            assert mypage.is_withdrawal_complete(), \
                "계정 탈퇴 후 로그인 랜딩 페이지로 이동하지 못했습니다"

    logger.info("[FHC-084~086] 계정 탈퇴 해피 케이스 완료")


@allure.title("[인프라] 계정 탈퇴 후 재가입")
@allure.story("탈퇴 후 재가입")
@allure.severity(allure.severity_level.MINOR)
def test_recreate_account_after_withdraw(mypage):
    """
    [인프라] 계정 생성 (탈퇴 후 재가입)

    전제: FHC-086 계정 탈퇴 후 → 로그인 페이지 상태
    단계:
      1. 회원가입 클릭
      2. 이메일로 가입하기
      3. 이메일/비밀번호/이름 기입
      4. 전체 동의 버튼 클릭
      5. 회원가입 버튼 클릭
    기대: 회원가입 후 헬피 챗 메인 페이지로 접속된다
    """
    with allure.step("r: 계정 탈퇴 완료 → 로그인 페이지 상태"):
        mypage.driver.get(mypage.CHAT_URL)
    with allure.step("g: 재가입 진행 → 헬피 챗 메인 페이지 이동 확인"):
        mypage.signup(MAIN_EMAIL, MAIN_PASSWORD, MAIN_NAME)
        assert mypage.is_signup_success(), \
            f"탈퇴 후 재가입 시 helpy-chat 메인 페이지로 이동하지 못했습니다 (이메일: {MAIN_EMAIL})"
