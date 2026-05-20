# tests/conftest.py
# 통합 conftest — 팀 전체 공통 fixture

import logging
import os
import re
from datetime import datetime

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from config.config import DEFAULT_WAIT, DOWNLOAD_DIR
from config.driver_factory import make_firefox_driver, make_simple_firefox_driver
from config.helpers import do_login, close_token_banner

logger = logging.getLogger(__name__)


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
        from common.driver_factory import make_chrome_driver
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
        from common.driver_factory import make_chrome_driver
        _driver = make_chrome_driver(DOWNLOAD_DIR)
    else:
        _driver = make_firefox_driver(DOWNLOAD_DIR)
    logger.info(f"브라우저: {browser.upper()} 실행 완료")
    yield _driver
    _driver.quit()
