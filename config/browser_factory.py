# config/browser_factory.py
# 브라우저 드라이버 생성 팩토리 — Selenium Manager 사용 (별도 드라이버 설치 불필요)

import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config.settings import DOWNLOAD_DIR

WINDOW_WIDTH  = 1920
WINDOW_HEIGHT = 1080

def _base_opts() -> FirefoxOptions:
    opts = FirefoxOptions()
    if os.environ.get("CI"):
        opts.add_argument("--headless")
    return opts

# ── Firefox ───────────────────────────────────────────────────────

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
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    return driver


def make_simple_firefox_driver() -> webdriver.Firefox:
    """다운로드 설정 없는 기본 Firefox 드라이버 생성"""
    driver = webdriver.Firefox(options=_base_opts())
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    return driver


# ── Chrome ────────────────────────────────────────────────────────

def make_chrome_driver(download_dir: str = DOWNLOAD_DIR) -> webdriver.Chrome:
    """파일 다운로드 설정이 포함된 Chrome 드라이버 생성"""
    opts = ChromeOptions()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
    opts.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    })
    return webdriver.Chrome(options=opts)


def make_simple_chrome_driver() -> webdriver.Chrome:
    """다운로드 설정 없는 기본 Chrome 드라이버 생성"""
    opts = ChromeOptions()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
    return webdriver.Chrome(options=opts)
