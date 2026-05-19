# tests/conftest.py
# tests/ 폴더 전용 pytest fixture 정의

import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

_CACHED_GECKO = r"C:\Users\Admin\.wdm\drivers\geckodriver\win64\v0.36.0\geckodriver.exe"


def _gecko_driver_path() -> str:
    if os.path.exists(_CACHED_GECKO):
        return _CACHED_GECKO
    return GeckoDriverManager().install()


BASE_URL     = "https://qaproject.elice.io/ai-helpy-chat"
LOGIN_URL    = (
    "https://accounts.elice.io/accounts/signin/me"
    "?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat"
    "&lang=ko-KR&org=qaproject"
)
DOWNLOAD_DIR = r"C:\Users\Admin\Downloads"


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="firefox",
        choices=["firefox", "chrome"],
        help="테스트에 사용할 브라우저 (기본값: firefox)",
    )


def _make_tools_driver(browser: str):
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
    else:
        opts = FirefoxOptions()
        opts.set_preference("browser.download.folderList", 2)
        opts.set_preference("browser.download.dir", DOWNLOAD_DIR)
        opts.set_preference("browser.download.useDownloadDir", True)
        opts.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        _driver = webdriver.Firefox(
            service=FirefoxService(_gecko_driver_path()),
            options=opts,
        )

    _driver.implicitly_wait(10)
    print(f"브라우저: {browser.upper()} 실행 완료")
    return _driver


@pytest.fixture(scope="module")
def tools_driver_module(request):
    browser = request.config.getoption("--browser")
    _driver = _make_tools_driver(browser)
    yield _driver
    _driver.quit()


@pytest.fixture
def tools_driver(request):
    browser = request.config.getoption("--browser")
    _driver = _make_tools_driver(browser)
    yield _driver
    _driver.quit()
