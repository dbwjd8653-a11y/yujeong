# tests/performance/test_ai_tool_load.py
# AI 도구(행동특성 및 종합의견) 연속 생성 요청 부하 테스트 — FHC-097

import time
import logging
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_WAIT, DOWNLOAD_DIR
from config.browser_factory import make_firefox_driver
from config.login_helpers import do_login, close_token_banner
from pages.tools.tools_behavior_page import BehaviorPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Performance"),
    allure.feature("AI 도구 부하 테스트"),
]

REPEAT      = 3
SCHOOL_LEVEL = "중학교"
STUDENT_NAME = "테스트학생"
REQUEST_TEXT = ""


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def ai_tool_load():
    driver = make_firefox_driver(DOWNLOAD_DIR)
    wait = WebDriverWait(driver, DEFAULT_WAIT)
    do_login(driver, wait)
    close_token_banner(driver, wait)
    yield driver, wait
    driver.quit()


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("AI 도구 연속 생성 요청 부하 테스트")
@allure.title("[FHC-097] AI 도구(행동특성) 연속 생성 요청 부하 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_097_ai_tool_load(ai_tool_load):
    """
    [FHC-097] AI 도구(행동특성) 연속 생성 요청 부하 테스트

    전제: 헬피챗 접속, 로그인 완료 (관리자 계정)
    단계:
      1. 헬피챗 사이트 접속
      2. 로그인
      3. AI 도구(행동특성 및 종합의견) 진입
      4. 생성 요청 3회 연속 실행
      5. 각 생성 완료 여부 및 시간 확인
    기대: 3회 연속 생성 요청 모두 완료, 결과 파일 정상 다운로드
    관련 TC: FHC-037, FHC-038, FHC-042, FHC-043, FHC-044
    """
    logger.info("[FHC-097] AI 도구 연속 생성 부하 테스트 시작")
    driver, wait = ai_tool_load
    fail_count = 0

    page = BehaviorPage(driver, wait)

    for i in range(1, REPEAT + 1):
        logger.info(f"[{i}/{REPEAT}] 생성 요청 시작")
        start = time.time()

        page.navigate_to_tools()
        page.click_tool_menu(page.TOOL_NAME)
        page.reset_inputs()
        page.click_class_info_tab()
        page.select_school_level(SCHOOL_LEVEL)
        page.click_next()
        page.handle_modify_modal()
        page.ensure_student_row_exists()
        page.enter_student_name(STUDENT_NAME)
        page.open_keyword_modal()
        page.select_character_keyword()
        page.save_keyword_modal()
        page.enter_request_text(REQUEST_TEXT)
        page.trigger_generation()
        page.search_student(STUDENT_NAME)
        result = page.download_result(DOWNLOAD_DIR)
        elapsed = round(time.time() - start, 2)

        if result:
            logger.info(f"[{i}/{REPEAT}] 생성 및 다운로드 완료 ({elapsed}s)")
        else:
            fail_count += 1
            logger.error(f"[{i}/{REPEAT}] 생성 실패 또는 다운로드 실패 ({elapsed}s)")

    assert fail_count == 0, f"3회 중 {fail_count}회 생성 실패"
    logger.info("[FHC-097] AI 도구 연속 생성 부하 테스트 완료")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
