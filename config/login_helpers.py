# config/helpers.py
# 공통 유틸리티 함수 (로그인, 배너 닫기 등)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config.settings import LOGIN_URL, TEST_USER, SHORT_WAIT, DEFAULT_WAIT


def do_login(driver, wait, user: dict = None):
    """로그인 페이지(한글)에서 지정 계정으로 로그인"""
    user = user or TEST_USER
    driver.get(LOGIN_URL)
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
    wait.until(EC.url_contains("ai-helpy-chat"))


def close_token_banner(driver, wait):
    """토큰 안내 배너가 표시된 경우 닫기 (없으면 무시)"""
    try:
        close_btn = WebDriverWait(driver, SHORT_WAIT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@data-testid='xmark-largeIcon']/ancestor::button[1]")
            )
        )
        close_btn.click()
    except Exception:
        pass
