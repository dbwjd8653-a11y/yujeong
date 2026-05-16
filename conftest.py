# conftest.py
# 모든 테스트에서 공유하는 pytest fixture 정의

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


BASE_URL      = "https://qaproject.elice.io/ai-helpy-chat"
DOWNLOAD_DIR  = r"C:\Users\Admin\Downloads"


# ──────────────────────────────────────────────
#  CLI 옵션: --browser firefox(기본) / chrome
# ──────────────────────────────────────────────

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="firefox",
        choices=["firefox", "chrome"],
        help="테스트에 사용할 브라우저 (기본값: firefox)",
    )


# ──────────────────────────────────────────────
#  내부 드라이버 팩토리
# ──────────────────────────────────────────────

def _make_tools_driver(browser: str):
    """브라우저 이름에 맞는 WebDriver 생성 (xlsx 자동 다운로드 설정 포함)"""
    if browser == "chrome":
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager

        opts = ChromeOptions()
        opts.add_experimental_option("prefs", {
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
        })
        _driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=opts,
        )
    else:  # firefox (기본)
        opts = FirefoxOptions()
        opts.set_preference("browser.download.folderList", 2)
        opts.set_preference("browser.download.dir", DOWNLOAD_DIR)
        opts.set_preference("browser.download.useDownloadDir", True)
        opts.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        _driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=opts,
        )

    _driver.implicitly_wait(10)
    print(f"브라우저: {browser.upper()} 실행 완료")
    return _driver


# ──────────────────────────────────────────────
#  회원가입 테스트용 driver (다운로드 설정 불필요)
# ──────────────────────────────────────────────

@pytest.fixture
def driver():
    """기본 Firefox 드라이버 — 회원가입 테스트 등에 사용"""
    _driver = webdriver.Firefox()
    _driver.implicitly_wait(10)

    yield _driver

    _driver.quit()


@pytest.fixture
def wait(driver):
    """기본 WebDriverWait (timeout=10s)"""
    return WebDriverWait(driver, 10)


@pytest.fixture
def login(driver, wait):
    """회원가입 페이지용 로그인 완료 fixture"""
    driver.get(BASE_URL)

    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, "loginId"))
    )
    email_input.clear()
    email_input.send_keys("qa5team3-01@elicer.com")

    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("qwer1234!")

    driver.find_element(By.XPATH, "//button[text()='Login']").click()

    return driver, wait


# ──────────────────────────────────────────────
#  도구(Tools) 테스트용 driver
# ──────────────────────────────────────────────

@pytest.fixture
def tools_driver(request):
    """도구 테스트용 드라이버 (function 스코프)
    --browser 옵션으로 firefox/chrome 선택 가능 (기본: firefox)
    test_agents.py 등 단일 TC 테스트에서 사용
    """
    browser = request.config.getoption("--browser")
    _driver = _make_tools_driver(browser)

    yield _driver

    _driver.quit()


@pytest.fixture(scope="module")
def tools_driver_module(request):
    """도구 테스트용 드라이버 (module 스코프)
    --browser 옵션으로 firefox/chrome 선택 가능 (기본: firefox)
    test_tools_01.py / test_tools_02.py 처럼 순차 TC가 브라우저 상태를
    이어가며 실행해야 할 때 사용 — 모듈 내 모든 TC가 같은 브라우저 공유
    """
    browser = request.config.getoption("--browser")
    _driver = _make_tools_driver(browser)

    yield _driver

    _driver.quit()


# ──────────────────────────────────────────────
# 사용 예시
# def test_something(driver):              ← 회원가입 테스트
# def test_something(tools_driver):        ← 에이전트 등 독립 TC 테스트
# def test_something(tools_driver_module): ← 도구 순차 TC 테스트
