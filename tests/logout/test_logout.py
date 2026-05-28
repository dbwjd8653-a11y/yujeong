# tests/logout/test_logout.py
# 로그아웃 E2E 테스트 — FHC-014 ~ FHC-017

import logging
import pytest
import allure
from pages.logout.logout_page import LogoutPage
from config.settings import TEST_USER

logger = logging.getLogger(__name__)

INPUT_PWD_INVALID = "12345678"

pytestmark = [
    allure.epic("Logout"),
    allure.feature("로그아웃"),
    allure.story("로그아웃 URL 검증"),
]


# ── fixtures ───────────────────────────────────────────────────────

@pytest.fixture
def logout_page_ready(login):
    """
    로그아웃 완료 상태 LogoutPage fixture (새드케이스용)

    전제: login fixture로 로그인 완료 상태
    단계:
      1. login에서 (driver, wait) 수신 → LogoutPage 생성
      2. 프로필 버튼 클릭 → 로그아웃 버튼 클릭 → 로그아웃 완료 상태
    """
    driver, wait = login
    page = LogoutPage(driver, wait)
    page.click_profile()
    page.click_logout()
    return page


# ── 해피패스 ──────────────────────────────────────────────────────

@allure.story("로그아웃 URL 검증")
@allure.title("[FHC-014] 로그아웃 완료 URL 검증")
@allure.severity(allure.severity_level.NORMAL)
def test_logout_url(login):
    """
    [FHC-014] 로그아웃 동작 및 완료 URL 검증

    전제: 로그인 완료 상태 (qa5team3-01@elicer.com)
    단계:
      1. 우측 상단 프로필 버튼 클릭
      2. 계정 메뉴에서 로그아웃 버튼 클릭
    기대: URL에 'signin/history'가 포함된 로그아웃 완료 페이지로 이동
    """
    logger.info("[FHC-014] 로그아웃 완료 URL 검증 시작")

    driver, wait = login
    page = LogoutPage(driver, wait)

    with allure.step("[FHC-014] 프로필 클릭 후 로그아웃"):
        page.click_profile()
        page.click_logout()

    with allure.step("[FHC-014] 로그아웃 완료 URL 확인"):
        assert page.is_logout_url(), "로그아웃 완료 URL 미도달 (signin/history 미포함)"

    logger.info("[FHC-014] 로그아웃 완료 URL 검증 완료")


# ── 새드케이스 (해피패스와 독립) ──────────────────────────────────

@allure.story("잘못된 비밀번호 재로그인 오류")
@allure.title("[FHC-015] 잘못된 비밀번호 재로그인 오류")
@allure.severity(allure.severity_level.NORMAL)
def test_wrong_password_error(logout_page_ready):
    """
    [FHC-015] 유효하지 않은 비밀번호로 재로그인 시도 → 오류 메시지 확인

    전제: 로그아웃 완료 상태 (로그인 페이지)
    단계:
      1. 비밀번호 필드에 잘못된 값(12345678) 입력
      2. 로그인 버튼 클릭
    기대: 'Email or password does not match' 오류 메시지 표시
    """
    logger.info("[FHC-015] 잘못된 비밀번호 재로그인 시작")

    with allure.step("[FHC-015] 잘못된 비밀번호 입력 후 로그인 시도"):
        logout_page_ready.enter_password(INPUT_PWD_INVALID)
        logout_page_ready.click_login_btn()

    with allure.step("[FHC-015] 오류 메시지 확인"):
        assert logout_page_ready.is_login_error_displayed(), "오류 메시지 미표시"

    logger.info("[FHC-015] 잘못된 비밀번호 재로그인 완료")


@allure.story("올바른 비밀번호 재로그인")
@allure.title("[FHC-016] 올바른 비밀번호 재로그인")
@allure.severity(allure.severity_level.NORMAL)
def test_correct_password_relogin(logout_page_ready):
    """
    [FHC-016] 올바른 비밀번호로 재로그인

    전제: 로그아웃 완료 상태 (로그인 페이지)
    단계:
      1. 비밀번호 필드에 올바른 비밀번호(qwer1234!) 입력
      2. 로그인 버튼 클릭
    기대: URL에 'ai-helpy-chat'이 포함된 메인 페이지로 이동
    """
    logger.info("[FHC-016] 올바른 비밀번호 재로그인 시작")

    with allure.step("[FHC-016] 올바른 비밀번호 입력 후 로그인 시도"):
        logout_page_ready.enter_password(TEST_USER["pw"])
        logout_page_ready.click_login_btn()

    with allure.step("[FHC-016] 재로그인 성공 확인"):
        assert logout_page_ready.is_login_success(), "재로그인 실패"

    logger.info("[FHC-016] 올바른 비밀번호 재로그인 완료")


@allure.story("다른 계정으로 전환")
@allure.title("[FHC-017] 다른 계정으로 전환")
@allure.severity(allure.severity_level.NORMAL)
def test_switch_account(logout_page_ready):
    """
    [FHC-017] 다른 계정으로 전환 → 로그인 페이지 이동 확인

    전제: 로그아웃 완료 상태 (로그인 페이지)
    단계:
      1. 'Sign in with a different account' 링크 클릭
    기대: 이메일 입력 필드가 있는 로그인 페이지로 이동
    """
    logger.info("[FHC-017] 다른 계정으로 전환 시작")

    with allure.step("[FHC-017] 다른 계정으로 전환 링크 클릭"):
        logout_page_ready.click_switch_account()

    with allure.step("[FHC-017] 로그인 페이지 이동 확인"):
        assert logout_page_ready.is_login_page(), "로그인 페이지 미이동"

    logger.info("[FHC-017] 다른 계정으로 전환 완료")
