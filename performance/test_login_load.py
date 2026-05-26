# tests/performance/test_login_load.py
# 로그인/로그아웃 반복 부하 테스트 — FHC-096

import time
import logging
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import DEFAULT_WAIT, LONG_WAIT
from config.browser_factory import make_simple_firefox_driver
from config.login_helpers import do_login, close_token_banner
from pages.logout.logout_page import LogoutPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Performance"),
    allure.feature("로그인 부하 테스트"),
]

REPEAT = 5
INTERVAL = 2


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def login_load():
    driver = make_simple_firefox_driver()
    wait = WebDriverWait(driver, DEFAULT_WAIT)
    yield driver, wait
    driver.quit()


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("로그인 로그아웃 반복 부하 테스트")
@allure.title("[FHC-096] 로그인/로그아웃 반복 부하 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_096_login_logout_load(login_load):
    """
    [FHC-096] 로그인/로그아웃 반복 부하 테스트

    전제: 헬피챗 접속, 비로그인 상태
    단계:
      1. 헬피챗 사이트 접속
      2. 로그인
      3. 로그아웃
      4. 2~3 반복 (5회)
      5. 각 로그인 성공 여부 및 시간 확인
    기대: 5회 반복 중 로그인 실패 없음, 매 회 정상 메인 페이지 진입
    관련 TC: FHC-006, FHC-014, FHC-015, FHC-016, FHC-017
    """
    logger.info("[FHC-096] 로그인/로그아웃 반복 부하 테스트 시작")
    driver, wait = login_load
    fail_count = 0

    for i in range(1, REPEAT + 1):
        start = time.time()
        do_login(driver, wait)
        close_token_banner(driver, wait)
        elapsed_login = round(time.time() - start, 2)

        if "ai-helpy-chat" in driver.current_url:
            logger.info(f"[{i}/{REPEAT}] 로그인 성공 ({elapsed_login}s)")
        else:
            fail_count += 1
            logger.error(f"[{i}/{REPEAT}] 로그인 실패 ({elapsed_login}s)")
            continue

        logout_page = LogoutPage(driver, WebDriverWait(driver, LONG_WAIT))
        logout_page.click_profile()
        logout_page.click_logout()
        wait.until(EC.url_contains("accounts.elice.io"))  # 로그아웃 완료 대기
        logger.info(f"[{i}/{REPEAT}] 로그아웃 완료")
        time.sleep(INTERVAL)

    assert fail_count == 0, f"5회 중 {fail_count}회 로그인 실패"
    logger.info("[FHC-096] 로그인/로그아웃 반복 부하 테스트 완료")
