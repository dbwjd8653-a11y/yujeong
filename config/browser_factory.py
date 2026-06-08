# config/browser_factory.py
# 브라우저 드라이버 생성 팩토리 — Selenium Manager 사용 (별도 드라이버 설치 불필요)

import os

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config.settings import DOWNLOAD_DIR

WINDOW_WIDTH  = 1920
WINDOW_HEIGHT = 1080

def _base_opts() -> EdgeOptions:
    opts = EdgeOptions()
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
    return webdriver.Edge(options=opts)


def make_simple_edge_driver() -> webdriver.Edge:
    """다운로드 설정 없는 기본 Edge 드라이버 생성"""
    return webdriver.Edge(options=_base_opts())


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
