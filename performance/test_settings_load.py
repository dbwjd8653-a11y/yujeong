# tests/performance/test_settings_load.py
# 설정 > 탭 부하 테스트 — FHC-094

import pytest
import logging
import allure
from pages.performance.settings_load_page import SettingsLoadPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Performance"),
    allure.feature("탭 부하 테스트"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def settings_load(login_module):
    """
    설정 탭 부하 테스트 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → SettingsLoadPage 반환
      2. 설정 페이지 이동
    """
    driver, wait = login_module
    page = SettingsLoadPage(driver, wait)
    page.navigate_to_settings()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("설정 탭 부하 테스트")
@allure.title("[FHC-094] 설정 탭 부하 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_094_tab_load(settings_load):
    """
    [FHC-094] 설정 탭 부하 테스트

    전제: 헬피챗 접속, 로그인 완료 (관리자 계정), 오른쪽 상단 톱니바퀴 '설정' 클릭 > '설정' 클릭
    단계:
      1. 헬피챗 사이트 접속
      2. 로그인
      3. 오른쪽 상단 톱니바퀴 '설정' 클릭
      4. 일반, 이용내역, 모델 설정, 구독 관리, 구성원 관리 탭 순차적으로 누르기 (3번 반복)
      5. 페이지 이동 정상동작 확인
    기대: 각 탭(일반, 이용내역, 모델 설정, 구독 관리, 구성원 관리) 클릭 시 해당 탭
          페이지로 정상 이동되며, 탭 전환 시 페이지 깨짐/로딩 오류 없이 콘텐츠가 정상 표시됨
    관련 TC: FHC-082, FHC-083, FHC-065
    """
    logger.info("[FHC-094] 설정 탭 부하 테스트 시작")
    settings_load.click_all_tabs_three_times()
    logger.info("[FHC-094] 설정 탭 부하 테스트 완료")
