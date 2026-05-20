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
from config.settings import SIGNUP_URL

EMAIL    = "test_dummy@naver.com"
PASSWORD = "test@1234"
NAME     = "포커스 테스트"


def recreate_account():
    driver = make_simple_firefox_driver()
    wait   = WebDriverWait(driver, 15)

    try:
        print(f"[1] 회원가입 페이지 이동: {SIGNUP_URL}")
        driver.get(SIGNUP_URL)

        print("[2] 이메일로 가입하기 클릭")
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(normalize-space(),'이메일로 가입하기')"
                       " or contains(normalize-space(),'Create account with email')]")
        ))
        btn.click()

        print("[3] 폼 입력")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='loginId']"))).send_keys(EMAIL)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='new-password']"))).send_keys(PASSWORD)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='fullname']"))).send_keys(NAME)

        print("[4] 전체 동의 클릭")
        checkbox = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input.PrivateSwitchBase-input[type='checkbox']")
        ))
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(0.3)

        print("[5] 회원가입 제출")
        submit = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit' and @form='signup-form']"
                       " | //button[@type='submit' and contains(@class,'MuiLoadingButton-root')]")
        ))
        submit.click()

        print("[6] 성공 대기 (qaproject.elice.io 이동)")
        WebDriverWait(driver, 30).until(EC.url_contains("qaproject.elice.io"))
        print(f"✅ 계정 재생성 완료: {EMAIL} / {PASSWORD}")

    except Exception as e:
        print(f"❌ 실패: {e}")
        print(f"현재 URL: {driver.current_url}")
    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    recreate_account()
