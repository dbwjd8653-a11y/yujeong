# config/browser_factory.py
# 브라우저 드라이버 생성 팩토리 — Selenium Manager 사용 (별도 드라이버 설치 불필요)

import os

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config.settings import DOWNLOAD_DIR

WINDOW_WIDTH  = 1920
WINDOW_HEIGHT = 1080


def _enable_headless_downloads(driver, download_dir: str) -> None:
    """headless Chromium/Edge는 prefs의 download.default_directory를 무시하므로
    CDP로 다운로드 동작을 명시적으로 허용한다 (CI 환경 다운로드 핵심 설정)."""
    os.makedirs(download_dir, exist_ok=True)
    try:
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": download_dir,
        })
    except Exception:
        pass


def _base_opts() -> EdgeOptions:
    opts = EdgeOptions()
    opts.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
    if os.environ.get("CI"):
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
    return opts


def _chrome_base_opts() -> ChromeOptions:
    """Edge `_base_opts()`와 동일하게 — CI에서는 headless로 실행한다.
    (CI는 디스플레이가 없어 headless 없이는 Chrome이 즉시 종료됨)"""
    opts = ChromeOptions()
    opts.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
    if os.environ.get("CI"):
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
    return opts

# ── Edge (Chromium 기반) ──────────────────────────────────────────

def make_edge_driver(download_dir: str = DOWNLOAD_DIR) -> webdriver.Edge:
    """파일 다운로드 설정이 포함된 Edge 드라이버 생성"""
    opts = _base_opts()
    opts.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    })
    driver = webdriver.Edge(options=opts)
    _enable_headless_downloads(driver, download_dir)
    return driver


def make_simple_edge_driver() -> webdriver.Edge:
    """다운로드 설정 없는 기본 Edge 드라이버 생성"""
    return webdriver.Edge(options=_base_opts())


# ── Chrome ────────────────────────────────────────────────────────

def make_chrome_driver(download_dir: str = DOWNLOAD_DIR) -> webdriver.Chrome:
    """파일 다운로드 설정이 포함된 Chrome 드라이버 생성"""
    opts = _chrome_base_opts()
    opts.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    })
    driver = webdriver.Chrome(options=opts)
    _enable_headless_downloads(driver, download_dir)
    return driver


def make_simple_chrome_driver() -> webdriver.Chrome:
    """다운로드 설정 없는 기본 Chrome 드라이버 생성"""
    return webdriver.Chrome(options=_chrome_base_opts())
