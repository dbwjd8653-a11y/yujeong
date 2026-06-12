# tests/conftest.py
# 통합 conftest — 팀 전체 공통 fixture

import inspect
import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path

import pytest
import allure

from config.selenium_imports import WebDriverWait

from config.settings import DEFAULT_WAIT, DOWNLOAD_DIR
from config.browser_factory import (
    make_edge_driver, make_simple_edge_driver,
    make_chrome_driver, make_simple_chrome_driver,
)
from config.login_helpers import do_login
from config.jira_config import JIRA_URL
from utils.jira_helper import create_jira_bug_ticket, attach_image_to_jira

logger = logging.getLogger(__name__)


# ── 로깅 설정 ──────────────────────────────────────────────────────
def pytest_configure(config):
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-5s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 파일: 에러만 기록 (실패 분석/보관용)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)

    # 콘솔: INFO 그대로 (실행 중 실시간 진행 확인용)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],
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
    import platform
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], capture_output=True)
        subprocess.run(["taskkill", "/F", "/IM", "msedgedriver.exe"], capture_output=True)
    else:
        subprocess.run(["pkill", "-f", "msedge"], capture_output=True)
        subprocess.run(["pkill", "-f", "msedgedriver"], capture_output=True)


# ── 생성된 Jira 티켓을 파일로 누적 기록 (Discord 버그 알림 연동용) ──
def _record_jira_ticket(config, test_name, issue_key, browser):
    """생성된 Jira 티켓을 allure-results 하위 파일에 누적 기록한다.

    notify 잡(scripts/ci_notify.py)이 이 파일을 읽어 Discord 알림에 버그 목록을 포함한다.
    매트릭스(edge/chrome) 아티팩트가 merge-multiple로 병합될 때 파일명이 겹치지 않도록
    --browser 값을 파일명에 넣어 브라우저별로 분리한다.
    """
    browser = config.getoption("--browser") or browser or "unknown"
    results_dir = Path("allure-results")
    results_dir.mkdir(parents=True, exist_ok=True)
    path = results_dir / f"jira_tickets_{browser}.json"

    tickets = []
    if path.exists():
        try:
            tickets = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            tickets = []

    tickets.append({
        "test": test_name,
        "key": issue_key,
        "url": f"{JIRA_URL}/browse/{issue_key}",
        "browser": browser,
    })

    try:
        path.write_text(
            json.dumps(tickets, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        logger.warning(f"Jira 티켓 기록 실패: {e}")


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
            if call.excinfo is not None:
                exc_type = call.excinfo.typename
                raw = str(call.excinfo.value).strip()
                # 첫 줄만 사용하고 셀레늄 예외의 "Message:" 접두어 제거
                first_line = raw.splitlines()[0].strip() if raw else ""
                detail = re.sub(r'^Message:\s*', '', first_line).strip()
                if exc_type == "AssertionError":
                    fail_msg = detail or exc_type
                else:
                    fail_msg = f"{exc_type}: {detail}" if detail else exc_type
            else:
                fail_msg = str(report.longrepr).splitlines()[-1].strip()
            _logger.error(f"{item.name} | {fail_msg}")

        elif report.passed:
            _logger.info(f"{item.name}")

        elif report.skipped:
            reason = getattr(report, 'wasxfail', None) or str(report.longrepr)
            _logger.warning(f"{item.name} | {reason}")
    
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
        # 테스트 docstring(전제/단계/기대)을 재현 정보로 사용
        doc = inspect.getdoc(item.function) or "(docstring 없음)"
        summary = f"[자동화 테스트 실패] {item.name}"
        description = (
            "자동화 테스트 실패\n\n"
            f"[Test Case]\n{item.name}\n\n"
            f"[설명 / 재현 단계]\n{doc}\n\n"
            f"[Test File]\n{test_file}\n\n"
            f"[Browser]\n{browser_name}\n\n"
            f"[URL]\n{current_url}\n\n"
            f"[Error]\n{error_message}\n"
        )

        issue_key = create_jira_bug_ticket(summary=summary, description=description)

        # ④ 스크린샷 첨부
        if issue_key and driver:
            try:
                screenshot = driver.get_screenshot_as_png()
                attach_image_to_jira(issue_key, screenshot)
            except Exception as e:
                logger.warning(f"스크린샷 첨부 실패: {e}")

        # ⑤ Discord 버그 알림 연동용 티켓 기록
        # notify 잡(scripts/ci_notify.py)이 이 파일을 읽어 Discord 알림에 버그 목록을 포함한다.
        if issue_key:
            _record_jira_ticket(item.config, item.name, issue_key, browser_name)


# ── mypage 테스트는 chrome 레그에서만 실행 ──
# mypage 파괴적 테스트(비번 변경/탈퇴)가 단일 공유 계정을 쓰므로, edge·chrome
# 병렬 실행 시 계정 레이스로 로그인이 깨진다 → edge에선 스킵. (상세: README)
def _skip_mypage_on_non_chrome(config, items):
    browser = config.getoption("--browser")
    if browser == "chrome":
        return
    skip_marker = pytest.mark.skip(
        reason=f"mypage 테스트는 단일 공유 계정 레이스 방지를 위해 chrome에서만 실행 (현재: {browser})"
    )
    for item in items:
        if "/mypage/" in item.nodeid.replace("\\", "/"):
            item.add_marker(skip_marker)


# ── 테스트 실행 순서 정렬 (FHC 번호 오름차순) ─────────────────────
def pytest_collection_modifyitems(config, items):
    """mypage 스킵(비-chrome) 처리 후 FHC_NNN 번호 기준으로 오름차순 정렬"""
    _skip_mypage_on_non_chrome(config, items)

    def _fhc_key(item):
        m = re.search(r'FHC[_-](\d+)', item.nodeid)
        if m:
            return int(m.group(1))
        doc = getattr(item.function, '__doc__', '') or ''
        m = re.search(r'FHC[_-](\d+)', doc)
        if m:
            return int(m.group(1))
        return 9999
    items.sort(key=_fhc_key)


# ── CLI 옵션 ───────────────────────────────────────────────────────
def pytest_addoption(parser):
    parser.addoption(
        "--jira",
        action="store_true",
        default=False,
        help="실패 테스트를 Jira 등록"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="edge",
        choices=["edge", "chrome"],
        help="테스트 브라우저 선택 (edge | chrome)",
    )


# ── 모든 테스트에 실행 브라우저를 Allure 파라미터로 기록 ───────────
@pytest.fixture(autouse=True)
def _tag_browser_param(request):
    """멀티 브라우저 실행 시 Allure 리포트에서 edge/chrome 결과를 구분하기 위함."""
    allure.dynamic.parameter("browser", request.config.getoption("--browser"))


# ── 브라우저 fixtures (테스트마다 독립 실행) ───────────────────────

def _make_simple_driver(browser: str):
    return make_simple_chrome_driver() if browser == "chrome" else make_simple_edge_driver()


def _make_driver(browser: str, download_dir: str = DOWNLOAD_DIR):
    return make_chrome_driver(download_dir) if browser == "chrome" else make_edge_driver(download_dir)


@pytest.fixture
def driver(request):
    """테스트마다 새 브라우저 실행 (--browser 옵션으로 선택)"""
    _driver = _make_simple_driver(request.config.getoption("--browser"))
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
def driver_module(request):
    """모듈 전체 공유 브라우저 (--browser 옵션으로 선택)"""
    _driver = _make_simple_driver(request.config.getoption("--browser"))
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
def tools_driver_module(request):
    """tools 테스트 전용 모듈 공유 브라우저 (다운로드 설정 포함)"""
    browser = request.config.getoption("--browser")
    _driver = _make_driver(browser, DOWNLOAD_DIR)
    logger.info(f"브라우저: {browser.upper()} 실행 완료")
    yield _driver
    _driver.quit()


@pytest.fixture
def tools_driver(request):
    """tools 테스트 전용 독립 브라우저 (다운로드 설정 포함)"""
    browser = request.config.getoption("--browser")
    _driver = _make_driver(browser, DOWNLOAD_DIR)
    logger.info(f"브라우저: {browser.upper()} 실행 완료")
    yield _driver
    _driver.quit()


