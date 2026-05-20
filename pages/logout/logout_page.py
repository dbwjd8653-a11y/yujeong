"""
로그아웃 페이지 동작 및 검증 클래스
BasePage를 상속받아 공통 동작을 재사용합니다.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class LogoutPage(BasePage):

    # ── Locators ───────────────────────────────────────────────────
    PROFILE_BTN        = (By.XPATH, "//button[.//*[@data-testid='PersonIcon']]")             # 프로필 아이콘
    LOGOUT_BTN         = (By.CSS_SELECTOR, "[data-testid='arrow-right-from-bracketIcon']")   # 로그아웃 목록칸
    MASKED_EMAIL       = (By.CSS_SELECTOR, "p.css-54qhqc")                                   # 로그아웃 창의 마스킹된 이메일 정보
    PWD_INPUT          = (By.NAME, "password")                                                # 비밀번호 입력칸
    LOGIN_BTN          = (By.CSS_SELECTOR, "button[type='submit']")                           # 로그인 버튼
    SWITCH_ACCOUNT_BTN = (By.PARTIAL_LINK_TEXT, "Sign in with a different account")           # 다른 아이디로 로그인하기
    LOGIN_ERROR_MSG    = (By.CSS_SELECTOR, "p.Mui-error")                                     # 잘못된 로그인 정보 오류 메시지

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def click_profile(self):
        """프로필 아이콘 버튼을 클릭하여 계정 메뉴를 연다."""
        self.click(self.PROFILE_BTN)

    def click_logout(self):
        """계정 메뉴에서 로그아웃 버튼을 클릭한다."""
        self.click(self.LOGOUT_BTN)

    def is_masked_email_valid(self, original_email):
        """
        [마스킹된 이메일 검증]

        [목적] 로그아웃 후 표시되는 마스킹된 이메일이
               원래 계정의 앞 2자리와 @이후 도메인과 일치하는지 검증한다.

        [Test Steps]
        1. 마스킹된 이메일 텍스트를 가져온다.
        2. 원본 이메일의 앞 2자리와 @이후 도메인을 추출한다.
        3. 마스킹된 이메일이 앞 2자리로 시작하고 도메인으로 끝나는지 확인한다.

        [Expected Result]
        마스킹된 이메일이 원본 계정과 일치하면 True를 반환한다.
        """
        masked = self.wait_for_visible(self.MASKED_EMAIL).text
        prefix = original_email[:2]           # 앞 2자리
        domain = original_email.split("@")[1] # @이후
        print(f"마스킹된 이메일: {masked}")
        return masked.startswith(prefix) and masked.endswith(domain)

    def enter_password(self, pwd):
        """비밀번호 입력 필드에 텍스트를 입력한다."""
        self.enter_text(self.PWD_INPUT, pwd)

    def click_login_btn(self):
        """로그인 버튼을 클릭한다."""
        self.click(self.LOGIN_BTN)

    def is_login_error_displayed(self):
        """
        [로그인 오류 메시지 검증]

        [Expected Result]
        'Email or password does not match' 오류 메시지가 표시되면 True를 반환한다.
        """
        return self.wait_for_visible(self.LOGIN_ERROR_MSG).is_displayed()

    def click_switch_account(self):
        """'Sign in with a different account' 링크를 클릭한다."""
        self.click(self.SWITCH_ACCOUNT_BTN)

    def is_login_success(self):
        """
        [로그인 성공 검증]

        [Expected Result]
        URL에 'ai-helpy-chat'이 포함되면 로그인 성공으로 간주하여 True를 반환한다.
        """
        try:
            self.wait_for_url_contains("ai-helpy-chat")
            return True
        except TimeoutException:
            return False

    def is_login_page(self):
        """
        [로그인 페이지 확인]

        [Expected Result]
        URL에 'accounts.elice.io'가 포함되면 로그인 페이지로 간주하여 True를 반환한다.
        """
        try:
            self.wait_for_url_contains("accounts.elice.io")
            return True
        except TimeoutException:
            return False
