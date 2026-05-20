# pages/mypage/mypage_page.py
# 마이페이지 공통 Base 클래스
# 로그인 / 페이지 이동 / 언어 변경 등 모든 mypage_XX_page.py가 공유하는 기능

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class MyPage(BasePage):

    # ========== URLs ==========
    CHAT_URL         = "https://qaproject.elice.io/ai-helpy-chat"
    ACCOUNT_URL      = "https://accounts.elice.io/members/account"
    ORG_URL          = "https://accounts.elice.io/members/organization"
    LANGUAGE_URL     = "https://accounts.elice.io/members/language"
    SUPPORT_URL      = "https://accounts.elice.io/members/support"
    SIGNUP_FORM_URL  = (
        "https://accounts.elice.io/accounts/signup/form"
        "?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat"
        "&lang=ko-KR&org=qaproject"
    )

    # ========== 계정 정보 ==========
    MAIN_EMAIL    = "test_dummy@naver.com"
    MAIN_PASSWORD = "test@1234"

    # ========== Locators — 로그인 ==========
    EMAIL_INPUT    = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BUTTON  = (By.CSS_SELECTOR, "button[type='submit']")

    # ========== Locators — qaproject 헤더 ==========
    PROFILE_BUTTON    = (By.CSS_SELECTOR, "button.MuiAvatar-root")
    ACCOUNT_MENU_ITEM = (By.XPATH,
        "//*[@role='menuitem' and ("
        "contains(text(),'계정') or contains(text(),'마이페이지') or contains(text(),'설정')"
        " or contains(text(),'Account') or contains(text(),'My Page') or contains(text(),'Settings')"
        ")]"
    )

    # ========== Locators — 언어 선택 드롭다운 ==========
    LANGUAGE_SELECT = (By.CSS_SELECTOR,
        "div#mui-component-select-locale, div[aria-haspopup='listbox']"
    )

    # ========== 초기화 ==========

    def __init__(self, driver):
        super().__init__(driver)

    # ========== 로그인 ==========

    def login(self, email: str = None, password: str = None):
        """qaproject SSO 로그인 (기본: MAIN_EMAIL/MAIN_PASSWORD)"""
        from config.settings import LOGIN_URL
        email    = email    or self.MAIN_EMAIL
        password = password or self.MAIN_PASSWORD

        self.driver.get(LOGIN_URL)
        self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        submit = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit.click()
        self.wait.until(EC.staleness_of(submit))
        WebDriverWait(self.driver, 30).until(EC.url_contains("qaproject.elice.io"))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href,'ai-helpy-chat')]")
            )
        )
        self.logger.info(f"로그인 성공: {email}")

    # ========== 페이지 이동 ==========

    def navigate_to_account(self):
        self.driver.get(self.ACCOUNT_URL)
        WebDriverWait(self.driver, 30).until(EC.url_contains("members/account"))
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.MuiIconButton-root"))
        )
        self.logger.info("계정 관리 페이지 이동 완료")

    def navigate_to_org(self):
        self.driver.get(self.ORG_URL)
        self.wait.until(EC.url_contains("members/organization"))
        self.logger.info("내 기관 페이지 이동 완료")

    def navigate_to_language(self):
        self.driver.get(self.LANGUAGE_URL)
        self.wait.until(EC.url_contains("members"))
        self.logger.info("언어 설정 페이지 이동 완료")

    def navigate_to_support(self):
        """고객 센터: 계정 페이지 이동 후 JS로 ChannelTalk 위젯 열기 (언어 무관)"""
        self.driver.get(self.ACCOUNT_URL)
        self.wait.until(EC.url_contains("members"))
        time.sleep(2)
        result = self.driver.execute_script("""
            if (window.ChannelIO) {
                window.ChannelIO('showMessenger');
                return 'channelIO-api';
            }
            var kws = ['Contact us', '문의하기', '고객 센터', '고객센터',
                       '1:1 문의', 'Contact', '채팅'];
            var els = Array.from(document.querySelectorAll('a, button'));
            var found = els.find(function(el) {
                var txt = (el.innerText || el.textContent || '').trim();
                return kws.some(function(k){ return txt.includes(k); });
            });
            if (found) { found.click(); return 'link: ' + (found.innerText||'').trim(); }
            var launcher = document.getElementById('ch-plugin-launcher')
                || document.querySelector('[class*="ch-launcher"]')
                || document.querySelector('[class*="ch-plugin"]');
            if (launcher) { launcher.click(); return 'launcher'; }
            return 'not-found';
        """)
        self.logger.info(f"고객 센터 열기 결과: {result}")
        time.sleep(3)
        self.logger.info("고객 센터 페이지 이동 완료")

    # ========== 공통 유틸 ==========

    def change_language(self, lang_code: str):
        self.wait.until(EC.element_to_be_clickable(self.LANGUAGE_SELECT)).click()
        option = (By.CSS_SELECTOR, f"li[data-value='{lang_code}']")
        self.wait.until(EC.element_to_be_clickable(option)).click()
        time.sleep(0.3)
        self.logger.info(f"언어 변경 완료: {lang_code}")

    def is_saved_successfully_displayed(self) -> bool:
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: any(
                    kw in d.find_element(By.TAG_NAME, "body").text
                    for kw in ["Saved successfully", "저장되었습니다", "저장"]
                )
            )
            return True
        except Exception:
            return False

    def is_on_org_page(self) -> bool:
        try:
            self.wait.until(EC.url_contains("members/organization"))
            return True
        except Exception:
            return False

    def is_new_tab_opened(self, original_handles: list) -> bool:
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: len(d.window_handles) > len(original_handles)
            )
            return True
        except Exception:
            return False

    def close_new_tabs_and_return(self, original_handle: str):
        for h in list(self.driver.window_handles):
            if h != original_handle:
                self.driver.switch_to.window(h)
                self.driver.close()
        self.driver.switch_to.window(original_handle)
        self.logger.info("새 탭 닫고 원래 탭으로 복귀 완료")
