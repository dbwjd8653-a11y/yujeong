# tests/settings/test_settings_subscription.py
# 설정 > 구독 관리 탭 E2E 테스트 — FHC-071

import pytest
import logging
from pages.settings.settings_subscription_page import SettingsSubscriptionPage

logger = logging.getLogger(__name__)


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

def test_FHC_071_navigate_to_subscription_tab(settings_subscription):
    """
    [FHC-071] '구독 관리' 탭 출력 테스트

    전제: 로그인 완료 상태 (관리자 계정), 설정 페이지 이동 완료
    단계:
      1. 오른쪽 상단 톱니바퀴 '설정' 클릭
      2. '구독 관리' 탭 클릭
    기대: 구독한 내역과 구독에 대한 '플랜 만료', '청구내역 관리',
          '플랜 해지 취소'와 같은 내용들이 보임
    """
    logger.info("[FHC-071] 구독 관리 탭 이동 시작")
    settings_subscription.navigate_to_subscription_tab()
    logger.info("[FHC-071] 구독 관리 탭 이동 완료")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
