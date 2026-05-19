# conftest.py
# 보통 conftest 안에는 공통 fixture를 작성한다.

import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL     = "https://qaproject.elice.io/ai-helpy-chat"
BASE_UI_URL  = "https://qaproject.elice.io"
BASE_API_URL = "https://dev-v2-community-api.dev.elicer.io"

TEST_USER = {
    "id": os.getenv("TEST_USER_ID", "qa5team3-01@elicer.com"),  # 환경변수 없으면 기본값
    "pw": os.getenv("TEST_USER_PW", "qwer1234!")
}


# ── 로그인 공통 함수 (fixture 아님) ───────────────────────────────
# 동작순서: 로그인 페이지 접속 → 이메일/비밀번호 입력 → 로그인 버튼 클릭 → 완료 대기
def _do_login(driver, wait):
    driver.get(BASE_URL)
    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, "loginId"))
    )
    email_input.clear()
    email_input.send_keys(TEST_USER["id"])

    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(TEST_USER["pw"])

    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    wait.until(EC.url_contains("ai-helpy-chat"))


# ── 브라우저 열고 닫기 fixture (테스트마다 독립 실행) ─────────────
@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)

@pytest.fixture
def login(driver, wait):
    _do_login(driver, wait)
    return driver, wait


# ── 브라우저 1개로 모듈 전체 공유 fixture (시나리오 순서대로 실행) ─
@pytest.fixture(scope="module")
def driver_module():
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def wait_module(driver_module):
    return WebDriverWait(driver_module, 10)

@pytest.fixture(scope="module")
def login_module(driver_module, wait_module):
    _do_login(driver_module, wait_module)
    return driver_module, wait_module