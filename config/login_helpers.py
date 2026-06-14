# config/helpers.py
# 공통 유틸리티 함수 (로그인, 배너 닫기 등)

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config.settings import LOGIN_URL, TEST_USER, SHORT_WAIT, BASE_UI_URL

logger = logging.getLogger(__name__)


def safe_get(driver, url, attempts=2):
    """페이지를 연다. 첫 시도가 멈춰서(TimeoutException) 실패하면 한 번 더 시도한다.

    브라우저가 막 켜진 직후 첫 페이지 로딩이 가끔 멈추는(edge 콜드 스타트) 문제 완화용.
    모든 시도가 실패하면 마지막 에러를 그대로 올려 원인을 잃지 않는다.
    """
    last_error = None
    for i in range(attempts):
        try:
            driver.get(url)
            return
        except TimeoutException as e:
            last_error = e
            logger.warning(f"페이지 열기 실패 ({i + 1}/{attempts}) — 다시 시도: {url}")
    raise last_error


def do_login(driver, wait, user: dict = None):
    """로그인 페이지(한글)에서 지정 계정으로 로그인"""
    user = user or TEST_USER

    # ── 계정 정보 가드 ──────────────────────────────────────────────
    # id/pw 가 None이면 send_keys(None)에서 'NoneType is not iterable'로
    # 죽어 원인 파악이 어려움 → 환경변수(.env / CI secret) 누락을 명확히 알림
    if not user.get("id") or not user.get("pw"):
        raise ValueError(
            "로그인 계정 정보가 비어 있습니다. 환경변수(.env / CI secret)를 확인하세요. "
            f"id={'설정됨' if user.get('id') else '없음'}, "
            f"pw={'설정됨' if user.get('pw') else '없음'}"
        )

    safe_get(driver, LOGIN_URL)
    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, "loginId"))
    )
    email_input.clear()
    email_input.send_keys(user["id"])

    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(user["pw"])

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='로그인']"))
    ).click()
    wait.until(lambda d: d.current_url.startswith(BASE_UI_URL))
    # LNB 링크가 렌더링될 때까지 대기 — 세션 쿠키가 완전히 설정된 후에만 나타남
    # (URL만 보고 반환하면 세션 확립 전에 다음 navigate가 실행돼 레이스로 실패함)
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href,'ai-helpy-chat')]")
        )
    )
    close_token_banner(driver, wait)


_BANNER_BTN = (By.XPATH, "//*[@data-testid='xmark-largeIcon']/ancestor::button[1]")


def close_token_banner(driver, wait):
    """토큰 안내 배너가 표시된 경우 닫기 (없으면 무시)"""
    try:
        close_btn = WebDriverWait(driver, SHORT_WAIT).until(
            EC.element_to_be_clickable(_BANNER_BTN)
        )
        close_btn.click()
        WebDriverWait(driver, SHORT_WAIT).until(
            EC.invisibility_of_element_located(_BANNER_BTN)
        )
    except Exception:
        pass
