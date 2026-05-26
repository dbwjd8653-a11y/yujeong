# tests/conftest.py
# 통합 conftest — 팀 전체 공통 fixture

import logging
import os
import re
from datetime import datetime
from pathlib import Path

import requests

import pytest

from config.selenium_imports import WebDriverWait

from config.settings import DEFAULT_WAIT, DOWNLOAD_DIR
from config.browser_factory import make_firefox_driver, make_simple_firefox_driver
from config.login_helpers import do_login, close_token_banner
from utils.jira_helper import create_jira_bug_ticket, attach_image_to_jira

logger = logging.getLogger(__name__)


# ── 로깅 설정 ──────────────────────────────────────────────────────
def pytest_configure(config):
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)-5s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def pytest_sessionstart(session):
    import shutil
    history_src = Path("allure-report/history")
    history_dst = Path("allure-results/history")
    if history_src.exists():
        if history_dst.exists():
            shutil.rmtree(history_dst)
        shutil.copytree(str(history_src), str(history_dst))


def pytest_sessionfinish(session, exitstatus):
    import subprocess
    subprocess.run(
        ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"],
        capture_output=True, timeout=60, shell=True
    )
    if session.config.getoption("--open", default=False) or session.config.getoption("--discord", default=False):
        subprocess.Popen(["allure", "serve", "allure-results"], shell=True)


# ── 테스트 실패 자동 로깅 + Jira 이슈 생성 및 스크린샷 첨부 Hook ──
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # ── 로그 처리 ─────────────────────────────
    if report.when == "call":
        _logger = logging.getLogger(item.module.__name__)

        if report.failed:
            # ① 로그 기록
            msg = str(report.longrepr)
            match = re.search(r'AssertionError:\s*(.+)', msg)
            fail_msg = match.group(1).strip() if match else msg.splitlines()[-1].strip()
            _logger.error(f"❌ {item.name} | {fail_msg}")

        elif report.passed:
            _logger.info(f"✅ {item.name}")

        elif report.skipped:
            reason = getattr(report, 'wasxfail', None) or str(report.longrepr)
            _logger.warning(f"⚠️  {item.name} | {reason}")
    
    # ── Jira 처리 ────────────────────────────
    if report.when == "call" and report.failed:
        jira_enabled = item.config.getoption("--jira")

        if not jira_enabled:
            return
        
        # xfail 제외
        if hasattr(report, "wasxfail"):
            return

        # ② driver 탐색
        driver = (
            item.funcargs.get("driver")
            or item.funcargs.get("driver_module")
            or item.funcargs.get("tools_driver")
            or item.funcargs.get("tools_driver_module")
        )

        current_url = "URL 확인 실패"
        browser_name = "unknown"

        if driver:
            try:
                current_url = driver.current_url
            except Exception:
                pass
            try:
                browser_name = driver.capabilities.get("browserName")
            except Exception:
                pass

        # ③ Jira 이슈 생성
        test_file = item.location[0]
        error_message = str(call.excinfo.value)
        summary = f"[자동화 테스트 실패] {item.name}"
        description = f"""
                    자동화 테스트 실패

                    [Test Case]
                    {item.name}

                    [Test File]
                    {test_file}

                    [Browser]
                    {browser_name}

                    [URL]
                    {current_url}

                    [Error]
                    {error_message}
                    """

        issue_key = create_jira_bug_ticket(summary=summary, description=description)

        # ④ 스크린샷 첨부
        if issue_key and driver:
            try:
                screenshot = driver.get_screenshot_as_png()
                attach_image_to_jira(issue_key, screenshot)
            except Exception as e:
                print(f"스크린샷 첨부 실패: {e}")


# ── 테스트 실행 순서 정렬 (FHC 번호 오름차순) ─────────────────────
def pytest_collection_modifyitems(items):
    """FHC_NNN 번호 기준으로 전체 테스트를 오름차순 정렬"""
    def _fhc_key(item):
        m = re.search(r'FHC_(\d+)', item.nodeid)
        if m:
            return int(m.group(1))
        if 'recreate_account_after_withdraw' in item.nodeid:
            return 86.5
        return 9999
    items.sort(key=_fhc_key)


# ── CLI 옵션 ───────────────────────────────────────────────────────
def pytest_addoption(parser):
    parser.addoption(
        "--discord",
        action="store_true",
        default=False,
        help="테스트 완료 후 Discord로 결과 전송",
    )
    parser.addoption(
        "--open",
        action="store_true",
        default=False,
        help="테스트 완료 후 HTML 리포트를 브라우저로 열기",
    )
    parser.addoption(
        "--jira",
        action="store_true",
        default=False,
        help="실패 테스트를 Jira 등록"
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
    return driver_module, _wait


# ── tools 전용 fixtures (다운로드 디렉터리 설정 포함) ─────────────

@pytest.fixture(scope="module")
def tools_driver_module():
    """tools 테스트 전용 모듈 공유 브라우저 (다운로드 설정 포함)"""
    _driver = make_firefox_driver(DOWNLOAD_DIR)
    logger.info("브라우저: FIREFOX 실행 완료")
    yield _driver
    _driver.quit()


@pytest.fixture
def tools_driver():
    """tools 테스트 전용 독립 브라우저 (다운로드 설정 포함)"""
    _driver = make_firefox_driver(DOWNLOAD_DIR)
    logger.info("브라우저: FIREFOX 실행 완료")
    yield _driver
    _driver.quit()


# ── pytest 종료 시 Discord 결과 전송 ──────────────────────────────
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1506913724663992330/fFs7F0fWTaAADPwpaRXfTE0MkPPlLVuYKVERtR8qwdBfpJhSBwRyCbv8aYHj-5CfrJSV"

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if not config.getoption("--discord", default=False):
        return

    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error  = len(terminalreporter.stats.get('error', []))
    total  = passed + failed + error
    date   = datetime.now().strftime("%Y-%m-%d %H:%M")

    args = [a for a in config.args if not a.startswith("-")]
    if args:
        test_name = ", ".join(os.path.basename(a.rstrip("/\\")) for a in args) + " 테스트 결과"
    else:
        test_name = "전체 테스트 결과"

    config._discord_message = f"""🚀 {test_name}
테스트 일자: {date}
✅ 성공: {passed}건
❌ 실패: {failed}건
총: {total}건"""


def pytest_unconfigure(config):
    if not config.getoption("--discord", default=False):
        return

    message = getattr(config, '_discord_message', '')
    screenshot_bytes = None

    try:
        import subprocess, threading, http.server, socket, time
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options as FirefoxOptions

        with socket.socket() as s:
            s.bind(('', 0))
            port = s.getsockname()[1]

        class _Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory="allure-report", **kwargs)
            def log_message(self, *args):
                pass

        server = http.server.HTTPServer(('localhost', port), _Handler)
        t = threading.Thread(target=server.serve_forever)
        t.daemon = True
        t.start()

        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(options=opts)
        try:
            driver.get(f"http://localhost:{port}/index.html")
            driver.set_window_size(1400, 900)
            time.sleep(4)
            screenshot_bytes = driver.get_screenshot_as_png()
        finally:
            driver.quit()
            server.shutdown()

    except Exception as e:
        logger.warning(f"Allure 리포트 스크린샷 실패: {e}")

    try:
        if screenshot_bytes:
            requests.post(
                DISCORD_WEBHOOK_URL,
                data={"content": message},
                files={"file": ("report.png", screenshot_bytes, "image/png")},
                timeout=30
            )
        else:
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, timeout=10)
    except Exception as e:
        logger.warning(f"Discord 전송 실패: {e}")
