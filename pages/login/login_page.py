"""
로그인 페이지 동작 및 검증 클래스
BasePage를 상속받아 공통 동작을 재사용합니다.

[Note]
한글 버전 로그인 페이지(lang=ko-KR) 기준으로 구현되었습니다.
"""

from config.selenium_imports import By, EC, TimeoutException

from pages.base_page import BasePage


class LoginPage(BasePage):

    # ── Locators ───────────────────────────────────────────────────
    EMAIL_INPUT        = (By.NAME, "loginId")                                                         # 이메일 입력칸
    PWD_INPUT          = (By.NAME, "password")                                                        # 비밀번호 입력칸
    LOGIN_BUTTON       = (By.XPATH, "//button[text()='로그인']")                                      # 로그인 버튼
    FORGOT_PWD_LINK    = (By.XPATH, "//a[contains(text(),'비밀번호를 잊어버리셨나요?')]")               # 비밀번호 찾기 링크
    FIND_VIA_PHONE_BTN = (By.XPATH, "//button[@value='phone']")                                       # 휴대폰 번호로 찾기 버튼
    PHONE_INPUT        = (By.CSS_SELECTOR, "input[name='to']")                                        # 휴대폰 번호 입력칸
    VIEW_PWD_BTN       = (By.CSS_SELECTOR, "[aria-label='비밀번호 보기']")                            # 비밀번호 표시/숨기기 버튼

    # ── 약관 동의 Locators ─────────────────────────────────────────
    AGREE_ALL_CHECKBOX    = (By.CSS_SELECTOR, "input[type='checkbox']")                               # 약관 동의 체크박스
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[form='signup-form']")                           # 약관 동의 제출 버튼

    # ── 언어 설정 Locators ────────────────────────────────────────
    LANGUAGE_SELECT = (By.CSS_SELECTOR, "select[aria-label='Change Languages']")  # 언어 선택 드롭다운

    # ── Error Message Locators ─────────────────────────────────────
    EMAIL_FORMAT_ERR = (By.XPATH, "//p[contains(text(),'잘못된 이메일 형식입니다.')]")                  # 이메일 유효성 오류 메시지
    PWD_FORMAT_ERR   = (By.XPATH, "//p[contains(text(),'비밀번호는 8자리 이상 입력해주세요.')]")         # 비밀번호 유효성 오류 메시지
    PHONE_FORMAT_ERR = (By.XPATH, "//p[contains(text(),'잘못된 번호 형식입니다.')]")                    # 전화번호 유효성 오류 메시지
    LOCKOUT_MSG      = (By.XPATH, "//p[contains(text(),'로그인을 여러 번 잘못 시도하셨습니다.')]")       # 계정 잠금 메시지
    LOGIN_ERROR_MSG  = (By.XPATH, "//p[contains(text(),'이메일 또는 비밀번호가 일치하지 않습니다.')]")   # 로그인 실패 오류 메시지

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def agree_and_submit(self):
        """
        [최초 로그인 약관 동의 및 제출]

        [Test Steps]
        1. 약관 동의 체크박스를 JavaScript로 클릭한다.
        2. 제출 버튼을 클릭한다.
        """
        agree_checkbox = self.wait.until(EC.presence_of_element_located(self.AGREE_ALL_CHECKBOX))
        self.js_click(agree_checkbox)
        self.click(self.CREATE_ACCOUNT_BUTTON)

    def enter_email(self, email):
        """이메일 입력 필드에 텍스트를 입력한다."""
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_password(self, pwd):
        """비밀번호 입력 필드에 텍스트를 입력한다."""
        self.enter_text(self.PWD_INPUT, pwd)

    def go_to_forgot_password(self):
        """'비밀번호를 잊어버리셨나요?' 링크를 클릭하여 비밀번호 찾기 페이지로 이동한다."""
        self.click(self.FORGOT_PWD_LINK)

    def enter_phone(self, phone):
        """
        [전화번호 입력]

        [Test Steps]
        1. '휴대폰 번호로 찾기' 버튼을 클릭한다.
        2. 휴대폰 번호 입력 필드에 텍스트를 입력한다.
        """
        self.click(self.FIND_VIA_PHONE_BTN)
        self.wait_for_visible(self.PHONE_INPUT).send_keys(phone)

    def attempt_login(self, email, password):
        """
        [로그인 시도]

        [Test Steps]
        1. 이메일을 입력한다.
        2. 비밀번호를 입력한다.
        3. 로그인 버튼을 클릭한다.
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click(self.LOGIN_BUTTON)

    def is_email_error_displayed(self):
        """'잘못된 이메일 형식입니다.' 오류 메시지가 표시되는지 확인한다."""
        return self.wait_for_visible(self.EMAIL_FORMAT_ERR).is_displayed()

    def is_pwd_error_displayed(self):
        """'비밀번호는 8자리 이상 입력해주세요.' 오류 메시지가 표시되는지 확인한다."""
        return self.wait_for_visible(self.PWD_FORMAT_ERR).is_displayed()

    def is_phone_error_displayed(self):
        """'잘못된 번호 형식입니다.' 오류 메시지가 표시되는지 확인한다."""
        return self.wait_for_visible(self.PHONE_FORMAT_ERR).is_displayed()

    def is_lockout_msg_displayed(self):
        """'로그인을 여러 번 잘못 시도하셨습니다.' 잠금 메시지가 표시되는지 확인한다."""
        return self.wait_for_visible(self.LOCKOUT_MSG).is_displayed()

    def is_login_error_displayed(self):
        """'이메일 또는 비밀번호가 일치하지 않습니다.' 오류 메시지가 표시되는지 확인한다."""
        return self.wait_for_visible(self.LOGIN_ERROR_MSG).is_displayed()

    def is_login_success(self):
        """
        [로그인 성공 검증]
        URL에 'ai-helpy-chat'이 포함되면 로그인 성공으로 간주한다.
        """
        try:
            self.wait_for_url_contains("ai-helpy-chat")
            return True
        except TimeoutException:
            return False

    def is_pwd_masked(self):
        """비밀번호 입력 필드의 type이 'password'인지 확인한다. (마스킹 상태)"""
        return self.wait_for_visible(self.PWD_INPUT).get_attribute("type") == "password"

    def toggle_pwd_mask(self):
        """비밀번호 표시/숨기기 버튼을 클릭한다."""
        self.click(self.VIEW_PWD_BTN)

    def is_pwd_unmasked(self):
        """비밀번호 입력 필드의 type이 'text'인지 확인한다. (마스킹 해제 상태)"""
        return self.wait_for_visible(self.PWD_INPUT).get_attribute("type") == "text"

    def select_language(self, lang_value):
        """
        [언어 설정 변경]

        [Test Steps]
        1. 언어 선택 드롭다운을 찾는다.
        2. 원하는 언어 값(value)으로 선택한다.

        [Note]
        lang_value: 'ko-KR' (한국어), 'en-US' (영어) 등
        """
        from selenium.webdriver.support.ui import Select
        select = Select(self.wait_for_visible(self.LANGUAGE_SELECT))
        select.select_by_value(lang_value)

    def get_current_language(self):
        """현재 선택된 언어 value를 반환한다."""
        from selenium.webdriver.support.ui import Select
        select = Select(self.wait_for_visible(self.LANGUAGE_SELECT))
        return select.first_selected_option.get_attribute("value")
