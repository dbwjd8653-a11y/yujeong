# tests/test_logout_01.py
# 로그아웃 E2E 테스트 — FHC-014 ~ FHC-017

import logging
import pytest
from pages.logout_page import LogoutPage
from config.config import TEST_USER

logger = logging.getLogger(__name__)

INPUT_PWD_INVALID = "12345678"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def logout_page(login_module):
    """
    로그아웃 페이지 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태 (qa5team3-01@elicer.com)
    단계:
      1. login_module에서 (driver, wait) 수신 → LogoutPage 반환
    """
    driver, wait = login_module
    return LogoutPage(driver, wait)


# ── 테스트 케이스 ──────────────────────────────────────────────────

def test_FHC_014_logout_masked_email(logout_page):
    """
    [FHC-014] 로그아웃 동작 및 마스킹 이메일 검증

    전제: 로그인 완료 상태 (qa5team3-01@elicer.com)
    단계:
      1. 우측 상단 프로필 버튼 클릭
      2. 계정 메뉴에서 로그아웃 버튼 클릭
      3. 마스킹된 이메일의 앞 2자리 + @이후 도메인 검증
    기대: 마스킹된 이메일(qa****@elicer.com)이 원본 계정 앞 2자리와 도메인 일치
    """
    logger.info("[FHC-014] 로그아웃 마스킹 이메일 검증 시작")
    logout_page.click_profile()
    logout_page.click_logout()
    assert logout_page.is_masked_email_valid(TEST_USER["id"]), "마스킹 이메일 불일치"
    logger.info("[FHC-014] 로그아웃 마스킹 이메일 검증 완료")


def test_FHC_015_wrong_password_error(logout_page):
    """
    [FHC-015] 유효하지 않은 비밀번호로 재로그인 시도 → 오류 메시지 확인

    전제: test_FHC_014 이어서 로그아웃 후 로그인 페이지 상태
    단계:
      1. 비밀번호 필드에 잘못된 값(12345678) 입력
      2. 로그인 버튼 클릭
    기대: 'Email or password does not match' 오류 메시지 표시
    """
    logger.info("[FHC-015] 잘못된 비밀번호 재로그인 시작")
    logout_page.enter_password(INPUT_PWD_INVALID)
    logout_page.click_login_btn()
    assert logout_page.is_login_error_displayed(), "오류 메시지 미표시"
    logger.info("[FHC-015] 잘못된 비밀번호 재로그인 완료")


def test_FHC_016_correct_password_relogin(logout_page):
    """
    [FHC-016] 올바른 비밀번호로 재로그인

    전제: test_FHC_015 이어서 로그인 페이지 상태
    단계:
      1. 비밀번호 필드에 올바른 비밀번호(qwer1234!) 입력
      2. 로그인 버튼 클릭
    기대: URL에 'ai-helpy-chat'이 포함된 메인 페이지로 이동
    """
    logger.info("[FHC-016] 올바른 비밀번호 재로그인 시작")
    logout_page.enter_password(TEST_USER["pw"])
    logout_page.click_login_btn()
    assert logout_page.is_login_success(), "재로그인 실패"
    logger.info("[FHC-016] 올바른 비밀번호 재로그인 완료")


def test_FHC_017_switch_account(logout_page):
    """
    [FHC-017] 다른 계정으로 전환 → 로그인 페이지 이동 확인

    전제: test_FHC_016 이어서 로그인 완료 상태
    단계:
      1. 우측 상단 프로필 버튼 클릭
      2. 계정 메뉴에서 로그아웃 버튼 클릭
      3. 'Sign in with a different account' 링크 클릭
    기대: 이메일 입력 필드가 있는 로그인 페이지로 이동
    """
    logger.info("[FHC-017] 다른 계정으로 전환 시작")
    logout_page.click_profile()
    logout_page.click_logout()
    logout_page.click_switch_account()
    assert logout_page.is_login_page(), "로그인 페이지 미이동"
    logger.info("[FHC-017] 다른 계정으로 전환 완료")
