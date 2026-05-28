# tests/settings/test_settings_member.py
# 설정 > 구성원 관리 탭 E2E 테스트 — FHC-073 ~ FHC-074

import pytest
import logging
import allure
from pages.settings.settings_member_page import SettingsMemberPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Settings"),
    allure.feature("구성원 관리"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def settings_member(login_module):
    """
    설정 > 구성원 관리 페이지 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → SettingsMemberPage 반환
      2. 설정 페이지 이동
      3. 구성원 관리 탭 이동
    """
    driver, wait = login_module
    page = SettingsMemberPage(driver, wait)
    page.navigate_to_settings()
    page.navigate_to_member_tab()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("토큰 한도 토글 비활성화")
@allure.title("[FHC-073] 토큰 한도 토글 비활성화 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_token_limit_disable(settings_member):
    """
    [FHC-073] 토큰 한도 토글 비활성화 테스트

    전제: 헬피챗 접속, 로그인 완료 (관리자 계정), 오른쪽 상단 톱니바퀴 '설정' 클릭 > '설정' 클릭,
          '구성원 관리' 탭 클릭, '토큰 한도' 토글 활성화
    단계:
      1. '구성원 토큰 관리'에서 '토큰 한도' 토글 비활성화
      2. 왼쪽 하단에 '저장' 버튼 클릭
    기대: '토큰 한도가 저장되었습니다.' 알림창 활성화됨
    """
    logger.info("[FHC-073] 토큰 한도 토글 비활성화 시작")
    settings_member.set_token_limit_toggle(activate=True)
    settings_member.set_token_limit_toggle(activate=False)
    toggle = settings_member.get_toggle()
    assert not settings_member.is_toggle_checked(toggle), "토큰 한도 토글 비활성화 실패"
    settings_member.save_and_verify_toast()
    logger.info("[FHC-073] 토큰 한도 토글 비활성화 완료")


@allure.story("토큰 한도 토글 활성화")
@allure.title("[FHC-074] 토큰 한도 토글 활성화 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_token_limit_enable(settings_member):
    """
    [FHC-074] 토큰 한도 토글 활성화 테스트

    전제: 헬피챗 접속, 로그인 완료 (관리자 계정), 오른쪽 상단 톱니바퀴 '설정' 클릭 > '설정' 클릭,
          '구성원 관리' 탭 클릭, '토큰 한도' 토글 비활성화
    단계:
      1. '구성원 토큰 관리'에서 '토큰 한도' 토글 활성화
      2. 왼쪽 하단에 '저장' 버튼 클릭
    기대: '토큰 한도가 저장되었습니다.' 알림창 활성화됨
    """
    logger.info("[FHC-074] 토큰 한도 토글 활성화 시작")
    settings_member.set_token_limit_toggle(activate=False)
    settings_member.set_token_limit_toggle(activate=True)
    toggle = settings_member.get_toggle()
    assert settings_member.is_toggle_checked(toggle), "토큰 한도 토글 활성화 실패"
    settings_member.save_and_verify_toast()
    logger.info("[FHC-074] 토큰 한도 토글 활성화 완료")
