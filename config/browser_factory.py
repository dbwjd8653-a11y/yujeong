# config/browser_factory.py
# 브라우저 드라이버 생성 팩토리

import os
import shutil
from functools import lru_cache
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from config.settings import DEFAULT_WAIT, DOWNLOAD_DIR


@lru_cache(maxsize=1)
def _firefox_path() -> str | None:
    path = shutil.which("firefox")
    if path:
        return path
    if os.name == "nt":  # Windows
        candidates = [
            os.path.join(os.environ.get("PROGRAMFILES", r"C:\Program Files"), "Mozilla Firefox", "firefox.exe"),
            os.path.join(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"), "Mozilla Firefox", "firefox.exe"),
        ]
    elif os.path.isdir("/Applications"):  # macOS
        candidates = ["/Applications/Firefox.app/Contents/MacOS/firefox"]
    else:  # Linux
        candidates = ["/usr/bin/firefox", "/usr/local/bin/firefox"]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    return None


@lru_cache(maxsize=1)
def _gecko_path() -> str:
    return GeckoDriverManager().install()


def _base_opts() -> FirefoxOptions:
    opts = FirefoxOptions()
    path = _firefox_path()
    if path:
        opts.binary_location = path
    return opts


def make_firefox_driver(download_dir: str = DOWNLOAD_DIR) -> webdriver.Firefox:
    """파일 다운로드 설정이 포함된 Firefox 드라이버 생성"""
    opts = _base_opts()
    opts.set_preference("browser.download.folderList", 2)
    opts.set_preference("browser.download.dir", download_dir)
    opts.set_preference("browser.download.useDownloadDir", True)
    opts.set_preference("browser.download.alwaysOpenPanel", False)
    opts.set_preference("browser.helperApps.alwaysAsk.force", False)
    opts.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
        "application/vnd.openxmlformats-officedocument.presentationml.presentation,"
        "application/octet-stream,"
        "application/zip,"
        "binary/octet-stream,"
        "application/x-download",
    )
    driver = webdriver.Firefox(service=FirefoxService(_gecko_path()), options=opts)
    driver.implicitly_wait(DEFAULT_WAIT)
    return driver


def make_simple_firefox_driver() -> webdriver.Firefox:
    """다운로드 설정 없는 기본 Firefox 드라이버 생성"""
    driver = webdriver.Firefox(service=FirefoxService(_gecko_path()), options=_base_opts())
    driver.implicitly_wait(DEFAULT_WAIT)
    return driver
