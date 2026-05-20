# tests/test_mypage_01.py
# 마이페이지 프로필 E2E 테스트 — FHC-076 ~ FHC-079

import logging
import pytest
from pages.mypage.mypage_profile_page import MyPage

logger = logging.getLogger(__name__)


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture
def mypage(login):
    """
    마이페이지 프로필 fixture

    전제: login fixture로 로그인 완료 상태
    단계:
      1. login에서 (driver, wait) 수신 → MyPage 반환
    """
    driver, wait = login
    return MyPage(driver)


# ── 테스트 케이스 ──────────────────────────────────────────────────

def test_FHC_076_profile_dropdown_menu(mypage):
    """
    [FHC-076] 프로필 드롭다운 메뉴 항목 확인

    전제: 로그인 완료 상태
    단계:
      1. 우측 상단 프로필 버튼 클릭
    기대: 드롭다운에 '계정 관리', '결제 내역', '언어 설정', '고객 센터', '로그아웃' 메뉴 표시
    """
    logger.info("[FHC-076] 프로필 드롭다운 메뉴 항목 확인 시작")
    mypage.click_profile_button()
    assert mypage.get_account_management_menu().is_displayed(), "계정 관리 메뉴 미표시"
    assert mypage.get_payment_history_menu().is_displayed(), "결제 내역 메뉴 미표시"
    assert mypage.get_language_setting_menu().is_displayed(), "언어 설정 메뉴 미표시"
    assert mypage.get_customer_center_menu().is_displayed(), "고객 센터 메뉴 미표시"
    assert mypage.get_logout_menu().is_displayed(), "로그아웃 메뉴 미표시"
    logger.info("[FHC-076] 프로필 드롭다운 메뉴 항목 확인 완료")


def test_FHC_077_navigate_to_account_management(mypage):
    """
    [FHC-077] 계정 관리 페이지 이동 확인

    전제: 로그인 완료 상태
    단계:
      1. 우측 상단 프로필 버튼 클릭
      2. '계정 관리' 메뉴 클릭
    기대: 계정 관리 페이지에 '이름', '이메일' 항목 표시
    """
    logger.info("[FHC-077] 계정 관리 페이지 이동 확인 시작")
    mypage.move_to_account_management()
    assert mypage.get_name_label().is_displayed(), "이름 항목 미표시"
    assert mypage.get_email_label().is_displayed(), "이메일 항목 미표시"
    logger.info("[FHC-077] 계정 관리 페이지 이동 확인 완료")
