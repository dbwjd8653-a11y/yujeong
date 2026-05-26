# config/browser_factory.py
# 브라우저 드라이버 생성 팩토리 — Selenium Manager 사용 (별도 드라이버 설치 불필요)

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.settings import DEFAULT_WAIT, DOWNLOAD_DIR


def _base_opts() -> FirefoxOptions:
    return FirefoxOptions()


def make_firefox_driver(download_dir: str = DOWNLOAD_DIR) -> webdriver.Firefox:
    """파일 다운로드 설정이 포함된 Firefox 드라이버 생성"""
    opts = _base_opts()
    opts.set_preference("browser.download.folderList", 2)
    opts.set_preference("browser.download.dir", download_dir)
    opts.set_preference("browser.download.useDownloadDir", True)
    opts.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
    driver = webdriver.Firefox(options=opts)
    driver.implicitly_wait(DEFAULT_WAIT)
    return driver


def make_simple_firefox_driver() -> webdriver.Firefox:
    """다운로드 설정 없는 기본 Firefox 드라이버 생성"""
    driver = webdriver.Firefox(options=_base_opts())
    driver.implicitly_wait(DEFAULT_WAIT)
    return driver
