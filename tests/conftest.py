# tests/conftest.py
# 통합 conftest — 팀 전체 공통 fixture

import logging
import os
import re
from datetime import datetime

import pytest

from config.selenium_imports import By, EC, WebDriverWait,TimeoutException

from config.settings import DEFAULT_WAIT, DOWNLOAD_DIR, LOGIN_URL, TEST_USER, SHORT_WAIT
from config.browser_factory import make_firefox_driver, make_simple_firefox_driver
from utils.jira_helper import create_jira_bug_ticket, attach_image_to_jira

# ── Logger 설정 ───────────────────────────────────────────────────

logger = logging.getLogger(__name__)


# ── 로그인 헬퍼 함수 ───────────────────────────────────────────────

def do_login(driver, wait, user: dict = None):
    """로그인 페이지에서 지정 계정으로 로그인"""
    user = user or TEST_USER
    driver.get(LOGIN_URL)
    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, "loginId"))
    )
    email_input.clear()
    email_input.send_keys(user["id"])

    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(user["pw"])

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='로그인']"))
    ).click()
    wait.until(EC.url_contains("ai-helpy-chat"))


def close_token_banner(driver, wait):
    """토큰 안내 배너가 표시된 경우 닫기 (없으면 무시)"""
    try:
        close_btn = WebDriverWait(driver, SHORT_WAIT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@data-testid='xmark-largeIcon']/ancestor::button[1]")
            )
        )
        close_btn.click()
    except Exception:
        pass


# ── 로깅 설정 ──────────────────────────────────────────────────────
def pytest_configure(config):
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


# ── 테스트 실패 자동 로깅 ──────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        _logger = logging.getLogger(item.module.__name__)
        # AssertionError 메시지만 추출
        msg = str(report.longrepr)
        match = re.search(r'AssertionError:\s*(.+)', msg)
        fail_msg = match.group(1).strip() if match else msg.splitlines()[-1].strip()
        _logger.error(f"[FAIL] {item.name} | {fail_msg}")


# ── 테스트 실행 순서 정렬 (FHC 번호 오름차순) ─────────────────────
def pytest_collection_modifyitems(items):
    """FHC_NNN 번호 기준으로 전체 테스트를 오름차순 정렬"""
    def _fhc_key(item):
        m = re.search(r'FHC_(\d+)', item.nodeid)
        if m:
            return int(m.group(1))
        if 'recreate_account_after_withdraw' in item.nodeid:
            return 86.5  # FHC-086(탈퇴) 직후, FHC-087 이전에 실행
        return 9999
    items.sort(key=_fhc_key)


# ── CLI 옵션 ───────────────────────────────────────────────────────
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="firefox",
        choices=["firefox", "chrome"],
        help="테스트에 사용할 브라우저 (기본값: firefox)",
    )


# ── 브라우저 fixtures (테스트마다 독립 실행) ───────────────────────

@pytest.fixture
def driver():
    """테스트마다 새 Firefox 브라우저 실행"""
    _driver = make_simple_firefox_driver()
    yield _driver
    _driver.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, DEFAULT_WAIT)


@pytest.fixture
def login(driver, wait):
    """로그인 완료 상태 반환 — (driver, wait) 튜플"""
    do_login(driver, wait)
    return driver, wait


# ── 브라우저 fixtures (모듈 전체 공유) ────────────────────────────

@pytest.fixture(scope="module")
def driver_module():
    """모듈 전체 공유 Firefox 브라우저"""
    _driver = make_simple_firefox_driver()
    yield _driver
    _driver.quit()


@pytest.fixture(scope="module")
def wait_module(driver_module):
    return WebDriverWait(driver_module, DEFAULT_WAIT)


@pytest.fixture(scope="module")
def login_module(driver_module):
    """모듈 전체 공유 로그인 상태 — (driver, wait) 튜플"""
    _wait = WebDriverWait(driver_module, DEFAULT_WAIT)
    do_login(driver_module, _wait)
    close_token_banner(driver_module, _wait)
    return driver_module, _wait


# ── tools 전용 fixtures (다운로드 디렉터리 설정 포함) ─────────────

@pytest.fixture(scope="module")
def tools_driver_module(request):
    """tools 테스트 전용 모듈 공유 브라우저 (다운로드 설정 포함)"""
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        from config.browser_factory import make_chrome_driver
        _driver = make_chrome_driver(DOWNLOAD_DIR)
    else:
        _driver = make_firefox_driver(DOWNLOAD_DIR)
    logger.info(f"브라우저: {browser.upper()} 실행 완료")
    yield _driver
    _driver.quit()


@pytest.fixture
def tools_driver(request):
    """tools 테스트 전용 독립 브라우저 (다운로드 설정 포함)"""
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        from config.browser_factory import make_chrome_driver
        _driver = make_chrome_driver(DOWNLOAD_DIR)
    else:
        _driver = make_firefox_driver(DOWNLOAD_DIR)
    logger.info(f"브라우저: {browser.upper()} 실행 완료")
    yield _driver
    _driver.quit()

# ── 테스트 실패 시 Jira 이슈 생성 및 스크린샷 첨부 Hook ───────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    # print("HOOK 실행됨")

    if report.when == "call" and report.failed:

        # print("실패 감지됨")

        signup = item.funcargs.get("signup")

        if signup:

            # print("signup fixture 확인")

            driver = signup.driver

            screenshot = driver.get_screenshot_as_png()

            summary = f"[UI 자동화 실패] {item.name}"

            description = f"""
                        자동화 테스트 실패

                        [Test Case]
                        {item.name}

                        [Error]
                        {call.excinfo.value}
                        """

            print("Jira 생성 시작")

            issue_key = create_jira_bug_ticket(
                summary=summary,
                description=description
            )

            print(f"issue_key: {issue_key}")

            if issue_key:

                # print("스크린샷 첨부 시작")

                attach_image_to_jira(
                    issue_key,
                    screenshot
                )