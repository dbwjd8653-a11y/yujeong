# scripts/recreate_test_account.py
# test_dummy@naver.com 계정 재생성 (탈퇴 후 복구용 1회성 스크립트)

import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.browser_factory import make_simple_firefox_driver

EMAIL    = "test_dummy@naver.com"
PASSWORD = "test@1234"
NAME     = "포커스 테스트"

SIGNUP_FORM_URL = (
    "https://accounts.elice.io/accounts/signup/form"
    "?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat"
    "&lang=ko-KR&org=qaproject"
)


def recreate_account():
    driver = make_simple_firefox_driver()
    wait   = WebDriverWait(driver, 15)

    try:
        print(f"[1] 회원가입 폼 직접 이동 (org=qaproject)")
        driver.get(SIGNUP_FORM_URL)
        wait.until(EC.url_contains("signup/form"))

        print("[2] 폼 입력")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='loginId']"))).send_keys(EMAIL)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='new-password']"))).send_keys(PASSWORD)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='fullname']"))).send_keys(NAME)

        print("[3] 전체 동의 클릭")
        checkbox = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[normalize-space(text())='전체 동의']/ancestor::label"
                       " | //label[.//span[normalize-space(text())='전체 동의']]")
        ))
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(0.3)

        print("[4] 회원가입 제출")
        submit = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit' and @form='signup-form']"
                       " | //button[@type='submit' and contains(@class,'MuiLoadingButton-root')]")
        ))
        submit.click()

        print("[5] 성공 대기 (qaproject.elice.io 이동)")
        WebDriverWait(driver, 30).until(EC.url_contains("qaproject.elice.io"))
        print(f"[OK] 계정 재생성 완료: {EMAIL} / {PASSWORD}")

    except Exception as e:
        print(f"[FAIL] 실패: {e}")
        print(f"현재 URL: {driver.current_url}")
    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    recreate_account()
