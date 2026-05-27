# tests/settings/test_settings_subscription.py
# 설정 > 구독 관리 탭 E2E 테스트 — FHC-072

import pytest
import logging
import allure
from pages.settings.settings_subscription_page import SettingsSubscriptionPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Settings"),
    allure.feature("구독 관리"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def settings_subscription(login_module):
    """
    설정 > 구독 관리 페이지 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → SettingsSubscriptionPage 반환
      2. 설정 페이지 이동
    """
    driver, wait = login_module
    page = SettingsSubscriptionPage(driver, wait)
    page.navigate_to_settings()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("구독 관리 탭 출력")
@allure.title("[FHC-072] '구독 관리' 탭 출력 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_navigate_to_subscription_tab(settings_subscription):
    """
    [FHC-072] '구독 관리' 탭 출력 테스트

    전제: 헬피챗 접속, 로그인 완료 (관리자 계정), 오른쪽 상단 톱니바퀴 '설정' 클릭 > '설정' 클릭
    단계:
      1. '구독 관리' 탭 클릭
    기대: 구독 내역 및 플랜 만료, 청구내역 관리, 플랜 해지 취소 항목 표시
    """
    logger.info("[FHC-072] 구독 관리 탭 이동 시작")
    settings_subscription.navigate_to_subscription_tab()
    logger.info("[FHC-072] 구독 관리 탭 이동 완료")
