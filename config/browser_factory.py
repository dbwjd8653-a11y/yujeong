# config/browser_factory.py
# 브라우저 드라이버 생성 팩토리

import logging
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from config.settings import DEFAULT_WAIT, DOWNLOAD_DIR

_CACHED_GECKO = r"C:\Users\Admin\.wdm\drivers\geckodriver\win64\v0.36.0\geckodriver.exe"


def _gecko_path() -> str:
    if os.path.exists(_CACHED_GECKO):
        return _CACHED_GECKO
    return GeckoDriverManager().install()


def make_firefox_driver(download_dir: str = DOWNLOAD_DIR) -> webdriver.Firefox:
    """파일 다운로드 설정이 포함된 Firefox 드라이버 생성"""
    opts = FirefoxOptions()
    opts.set_preference("browser.download.folderList", 2)
    opts.set_preference("browser.download.dir", download_dir)
    opts.set_preference("browser.download.useDownloadDir", True)
    opts.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
    driver = webdriver.Firefox(
        service=FirefoxService(_gecko_path()),
        options=opts,
    )
    driver.implicitly_wait(DEFAULT_WAIT)
    return driver


def make_simple_firefox_driver() -> webdriver.Firefox:
    """다운로드 설정 없는 기본 Firefox 드라이버 생성"""
    try:
        driver = webdriver.Firefox(service=FirefoxService(_gecko_path()))
        driver.implicitly_wait(DEFAULT_WAIT)
        return driver
    except Exception:
        logging.exception("❌ Firefox Driver 생성 실패")
        raise
