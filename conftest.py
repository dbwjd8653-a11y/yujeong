# conftest.py
# 보통 conftest 안에는 공통 fixture를 작성한다.

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://qaproject.elice.io/ai-helpy-chat"


# 공통 브라우저 fixture
@pytest.fixture
def driver():

    driver = webdriver.Firefox()
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


# 공통 wait fixture
@pytest.fixture
def wait(driver):

    return WebDriverWait(driver, 10)


# 로그인 완료 상태 fixture
@pytest.fixture
def login(driver, wait):

    driver.get(BASE_URL)

    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, "loginId"))
    )

    email_input.clear()
    email_input.send_keys("qa5team3-01@elicer.com")

    password_input = driver.find_element(By.NAME, "password")

    password_input.clear()
    password_input.send_keys("qwer1234!")

    driver.find_element(
        By.XPATH,
        "//button[text()='Login']"
    ).click()

    return driver, wait

# 이렇게 작성해두면, 모든 test 파일에서 아래 형식과 같이 사용 가능
# def test_something(driver):  