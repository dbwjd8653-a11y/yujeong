# pages/signup/signup_page.py

from config.selenium_imports import By, EC

from pages.base_page import BasePage
from config.settings import SIGNUP_URL


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

    # def get_create_account_button(self):
    #     return self.wait.until(EC.element_to_be_clickable(self.CREATE_ACCOUNT_BUTTON))

    def get_email_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.EMAIL_ERROR_MESSAGE))

    def get_name_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.NAME_ERROR_MESSAGE))

    # ── 액션 ──────────────────────────────────────────────────────────

    def click_create_account_with_email(self):
        self.wait.until(EC.element_to_be_clickable(self.CREATE_EMAIL_BUTTON)).click()
        
    def input_text(self, locator, text):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)
    
    def enter_email(self, email):
        self.input_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        self.input_text(self.PASSWORD_INPUT, password)

    def enter_name(self, name):
        self.input_text(self.NAME_INPUT, name)  

    def click_agree_checkbox(self):
        self.js_click(self.get_agree_checkbox())

    def click_age_checkbox(self):
        self.js_click(self.get_age_checkbox())

    def click_required_checkbox(self):
        for cb in self.get_required_checkboxes():
            self.js_click(cb)

    def click_create_account_button(self):
        self.js_click(
            self.wait.until(
                EC.element_to_be_clickable(self.CREATE_ACCOUNT_BUTTON)
            )
        )

    # email, pw, 이름 입력하기
    def fill_signup_form(self, email, password, name):
        self.enter_email(email)
        self.enter_password(password)
        self.enter_name(name)

    # 약관 동의하기
    def agree_terms(self, agreement_type="all"):
        if agreement_type == "all":
            self.click_agree_checkbox()

        elif agreement_type == "required":
            self.click_age_checkbox()
            self.click_required_checkbox()
        else:
            raise ValueError(
                f"지원하지 않는 agreement_type: {agreement_type}"
            )


    # ── 검증 ──────────────────────────────────────────────────────────

    def is_signup_success(self) -> bool:
        try:
            self.wait.until(EC.url_contains("isFirstLogin=true"))
            return True
        except Exception:
            return False
