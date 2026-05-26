# tests/settings/test_settings_useage.py
# 설정 > 이용 내역 탭 E2E 테스트 — FHC-068

import pytest
import logging
import allure
from pages.settings.settings_useage_page import SettingsUseagePage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Settings"),
    allure.feature("이용 내역"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def settings_useage(login_module):
    """
    설정 > 이용 내역 페이지 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → SettingsUseagePage 반환
      2. 설정 페이지 이동
    """
    driver, wait = login_module
    page = SettingsUseagePage(driver, wait)
    page.navigate_to_settings()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("이용 내역 탭 출력")
@allure.title("[FHC-068] '이용 내역' 탭 출력 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_068_navigate_to_history_tab(settings_useage):
    """
    [FHC-068] '이용 내역' 탭 출력 테스트

    전제: 로그인 완료 상태 (관리자 계정), 설정 페이지 이동 완료
    단계:
      1. 이용 내역 탭 클릭
      2. '토큰 지급 내역' 활성화 확인
    기대: '이용 내역' 탭 클릭 시 토큰 발행 이력이 출력되며
          진행중인 토큰의 경우 '진행중' 표시 활성화 됨
    """
    logger.info("[FHC-068] 이용 내역 탭 이동 시작")
    settings_useage.navigate_to_history_tab()
    logger.info("[FHC-068] 이용 내역 탭 이동 완료")
