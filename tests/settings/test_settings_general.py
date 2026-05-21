# tests/settings/test_settings_general.py
# 설정 > 일반 탭 E2E 테스트 — FHC-067

import pytest
import logging
from pages.settings.settings_general_page import SettingsPage

logger = logging.getLogger(__name__)


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def settings_general(login_module):
    """
    설정 > 일반 페이지 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → SettingsPage 반환
    """
    driver, wait = login_module
    return SettingsPage(driver, wait)


# ── 테스트 케이스 ──────────────────────────────────────────────────

def test_FHC_067_navigate_to_settings(settings_general):
    """
    [FHC-067] 설정창 기본 값 테스트

    전제: 로그인 완료 상태 (관리자 계정)
    단계:
      1. 오른쪽 상단 톱니바퀴 '설정' 클릭
      2. '일반' 탭 활성화 확인
    기대: '설정' 클릭 시 '일반' 탭이 활성화 되어 화면에 출력됨
    """
    logger.info("[FHC-067] 설정 페이지 이동 시작")
    settings_general.navigate_to_settings()
    logger.info("[FHC-067] 설정 페이지 이동 완료")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
