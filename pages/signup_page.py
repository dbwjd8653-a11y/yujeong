# pages/signup_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from common.config import SIGNUP_URL


class SignupPage(BasePage):

    SIGNUP_URL = SIGNUP_URL

    # ── Locators ──────────────────────────────────────────────────────

    EMAIL_INPUT           = (By.CSS_SELECTOR, "input[placeholder='이메일']")
    PASSWORD_INPUT        = (By.CSS_SELECTOR, "input[placeholder='비밀번호']")
    NAME_INPUT            = (By.CSS_SELECTOR, "input[placeholder='이름']")
    CREATE_EMAIL_BUTTON   = (By.XPATH, "//button[contains(., 'Create account with email') or contains(., '이메일로 가입하기')]")
    AGREE_ALL_CHECKBOX    = (By.XPATH, "//span[text()='전체 동의']/ancestor::label")
    AGE_CHECKBOX          = (By.XPATH, "//span[contains(text(), '만 14세 이상입니다.')]/ancestor::label")
    REQ_CHECKBOXES        = (By.XPATH, "//span[contains(text(), '[필수]')]/ancestor::label")
    CREATE_ACCOUNT_BUTTON = (By.XPATH, "//button[contains(text(), '회원가입')]")
    EMAIL_ERROR_MESSAGE   = (By.XPATH, "//p[contains(text(), '이메일 주소가 올바르지 않습니다.')]")
    NAME_ERROR_MESSAGE    = (By.XPATH, "//span[contains(text(), '예기치 못한 문제가 발생하였습니다.')]")

    # ── 페이지 이동 ───────────────────────────────────────────────────

    def open(self):
        self.driver.get(self.SIGNUP_URL)
        self.wait.until(EC.url_contains("signup"))
        self.logger.info("회원가입 페이지 접속 완료")

    # ── 요소 조회 (테스트에서 직접 사용) ─────────────────────────────

    def get_email_input(self):
        return self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))

    def get_password_input(self):
        return self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))

    def get_name_input(self):
        return self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))

    def get_agree_checkbox(self):
        return self.wait.until(EC.element_to_be_clickable(self.AGREE_ALL_CHECKBOX))

    def get_age_checkbox(self):
        return self.wait.until(EC.element_to_be_clickable(self.AGE_CHECKBOX))

    def get_required_checkboxes(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.REQ_CHECKBOXES))

    def get_create_account_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.CREATE_ACCOUNT_BUTTON))

    def get_email_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.EMAIL_ERROR_MESSAGE))

    def get_name_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.NAME_ERROR_MESSAGE))

    # ── 액션 ──────────────────────────────────────────────────────────

    def click_create_account_with_email(self):
        self.wait.until(EC.element_to_be_clickable(self.CREATE_EMAIL_BUTTON)).click()
        self.logger.info("이메일로 가입하기 버튼 클릭 완료")

    def enter_email(self, email):
        self.get_email_input().send_keys(email)
        self.logger.info(f"이메일 입력 완료: {email}")

    def enter_password(self, password):
        self.get_password_input().send_keys(password)
        self.logger.info("비밀번호 입력 완료")

    def enter_name(self, name):
        self.get_name_input().send_keys(name)
        self.logger.info(f"이름 입력 완료: {name}")

    def click_agree_checkbox(self):
        self.js_click(self.get_agree_checkbox())
        self.logger.info("전체 동의 체크 완료")

    def click_age_checkbox(self):
        self.js_click(self.get_age_checkbox())
        self.logger.info("만 14세 이상 체크 완료")

    def click_required_checkbox(self):
        for cb in self.get_required_checkboxes():
            self.js_click(cb)
        self.logger.info("필수 약관 체크 완료")

    def click_create_account_button(self):
        self.js_click(self.get_create_account_button())
        self.logger.info("회원가입 버튼 클릭 완료")

    # ── 검증 ──────────────────────────────────────────────────────────

    def is_signup_success(self) -> bool:
        try:
            self.wait.until(EC.url_contains("isFirstLogin=true"))
            return True
        except Exception:
            return False
