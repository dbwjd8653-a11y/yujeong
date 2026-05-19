# conftest.py
# 모든 테스트 파일에서 공통으로 사용하는 fixture와 설정을 관리합니다.

import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# ── 공통 URL 상수 ──────────────────────────────────────────────────
# 로그인 페이지 한글 고정: lang=ko-KR 파라미터로 한글 버전 강제 접속
LOGIN_URL    = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=ko-KR&org=qaproject"
BASE_URL     = "https://qaproject.elice.io/ai-helpy-chat"
BASE_UI_URL  = "https://qaproject.elice.io"
BASE_API_URL = "https://dev-v2-community-api.dev.elicer.io"

# ── 대기 시간 상수 ─────────────────────────────────────────────────
SHORT_WAIT   = 5   # 짧은 대기 (팝업, 버튼 등 빠른 응답 요소)
DEFAULT_WAIT = 10  # 기본 대기
LONG_WAIT    = 20  # 긴 대기 (페이지 이동, 모달 등)

# ── 테스트 계정 정보 ───────────────────────────────────────────────
# 환경변수가 설정되어 있으면 환경변수 값을 사용, 없으면 기본값 사용
TEST_USER = {
    "id": os.getenv("TEST_USER_ID", "qa5team3-01@elicer.com"),
    "pw": os.getenv("TEST_USER_PW", "qwer1234!")
}


# ── 로그인 공통 함수 (fixture 아님) ───────────────────────────────
def do_login(driver, wait):
    """
    [공통 로그인 함수]

    [Pre-condition]
    - 브라우저가 실행된 상태

    [Test Steps]
    1. 한글 버전 로그인 페이지(lang=ko-KR)로 접속한다.
    2. 이메일 입력 필드에 TEST_USER ID를 입력한다.
    3. 비밀번호 입력 필드에 TEST_USER PW를 입력한다.
    4. 로그인 버튼을 클릭한다.
    5. URL에 'ai-helpy-chat'이 포함될 때까지 대기한다.

    [Note]
    LOGIN_URL에 lang=ko-KR 파라미터를 포함하여 한글 버전으로 강제 접속합니다.
    """
    driver.get(LOGIN_URL)
    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, "loginId"))
    )
    email_input.clear()
    email_input.send_keys(TEST_USER["id"])

    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(TEST_USER["pw"])

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='로그인']"))
    ).click()
    wait.until(EC.url_contains("ai-helpy-chat"))


# ── 토큰 안내 배너 닫기 공통 함수 (fixture 아님) ──────────────────
def close_token_banner(driver, wait):
    """
    [토큰 안내 배너 닫기 함수]

    [목적]
    토큰이 추가되거나 소진될 때 나타나는 안내 배너 팝업을 닫아
    이후 테스트 동작에 방해가 되지 않도록 합니다.

    [주의]
    배너가 없는 경우 TimeoutException을 무시하고 계속 진행합니다.
    """
    try:
        close_btn = WebDriverWait(driver, SHORT_WAIT).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='xmark-largeIcon']")
            )
        )
        driver.execute_script("arguments[0].click();", close_btn)
    except TimeoutException:
        pass


# ── 브라우저 열고 닫기 fixture (테스트마다 독립 실행) ─────────────
@pytest.fixture
def driver():
    """
    [브라우저 fixture - 테스트마다 독립 실행]

    [Pre-condition]
    - 없음 (매 테스트마다 새 브라우저를 실행합니다)

    [Test Steps]
    1. Firefox 브라우저를 실행한다.
    2. 테스트 종료 후 브라우저를 닫는다.

    [Note]
    - implicitly_wait 미사용 - 명시적 대기(WebDriverWait)만 사용합니다.
    - 매 테스트마다 새 브라우저를 실행하므로 쿠키가 없는 초기 상태입니다.
    """
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, DEFAULT_WAIT)


# ── 로그인 fixture (test_login 전용) ──────────────────────────────
@pytest.fixture
def login(driver, wait):
    """
    [로그인 fixture - 테스트마다 독립 실행]

    [Pre-condition]
    - 브라우저가 실행된 상태

    [Test Steps]
    1. do_login() 함수로 한글 버전 로그인 페이지에서 로그인을 수행한다.
    2. (driver, wait) 튜플을 반환한다.
    """
    do_login(driver, wait)
    return driver, wait


# ── 브라우저 1개로 모듈 전체 공유 fixture (시나리오 순서대로 실행) ─
@pytest.fixture(scope="module")
def driver_module():
    """
    [브라우저 fixture - 모듈 전체 공유]

    [Pre-condition]
    - 없음 (모듈 시작 시 브라우저를 한 번만 실행합니다)

    [Test Steps]
    1. Firefox 브라우저를 실행한다.
    2. 모듈 내 모든 테스트가 종료되면 브라우저를 닫는다.

    [Note]
    - implicitly_wait 미사용 - 명시적 대기(WebDriverWait)만 사용합니다.
    - 모듈 시작 시 새 브라우저를 실행하므로 쿠키가 없는 초기 상태입니다.
    """
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


# ── 로그인 fixture (tool/logout 테스트 전용 - 모듈 공유) ──────────
@pytest.fixture(scope="module")
def login_module(driver_module):
    """
    [로그인 fixture - 모듈 전체 공유]

    [Pre-condition]
    - driver_module 브라우저가 실행된 상태

    [Test Steps]
    1. do_login() 함수로 한글 버전 로그인 페이지에서 로그인을 수행한다.
    2. 토큰 안내 배너가 있으면 닫는다.
    3. (driver_module, wait) 튜플을 반환한다.

    [Note]
    scope="module" 이므로 모듈 내 최초 1회만 실행됩니다.
    """
    wait = WebDriverWait(driver_module, DEFAULT_WAIT)
    do_login(driver_module, wait)
    close_token_banner(driver_module, wait)
    return driver_module, wait
