# pages/mypage/mypage_06_page.py
# 마이페이지 > 계정 탈퇴 + 재가입 전용 Page 클래스
# FHC-077(탈퇴 영역) / FHC-078(탈퇴 확인) / FHC-079(탈퇴) / FHC-080(재가입)

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.mypage.mypage_page import MyPage


class MyPage06(MyPage):

    # ========== Locators — FHC-077~079: 계정 탈퇴 (한/영 모두) ==========
    WITHDRAW_AREA = (By.XPATH,
        "//*[contains(text(),'계정 탈퇴') or contains(text(),'탈퇴')"
        " or contains(text(),'Leave') or contains(text(),'Delete Account')"
        " or contains(text(),'Close Account') or contains(text(),'Withdraw')]"
        "[not(@role='menuitem')]"
    )
    WITHDRAW_BUTTON = (By.XPATH,
        "//button[contains(@class,'MuiButton') and ("
        " contains(normalize-space(),'탈퇴하기')"
        " or contains(normalize-space(),'탈퇴')"
        " or normalize-space()='Leave'"
        " or contains(normalize-space(),'Delete Account')"
        " or contains(normalize-space(),'Withdraw')"
        " or contains(normalize-space(),'Close Account')"
        ")]"
    )
    WITHDRAW_CONFIRM_INPUT = (By.CSS_SELECTOR,
        "input[name='email'], input[placeholder*='Delete'], input[placeholder*='delete']"
    )
    WITHDRAW_CONFIRM_MSG = (By.XPATH,
        "//*[contains(text(),'Delete') and (contains(text(),'이메일') or contains(text(),'email'))]"
        " | //*[contains(text(),'탈퇴하려면') or contains(text(),'withdraw')]"
    )
    WITHDRAW_FINAL_BUTTON = (By.CSS_SELECTOR,
        "button[type='submit'].MuiLoadingButton-root"
    )

    # ========== Locators — FHC-080: 회원가입 ==========
    SIGNUP_LINK         = (By.CSS_SELECTOR, "a[href*='/accounts/signup']")
    EMAIL_SIGNUP_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'이메일로 가입하기')"
        " or contains(normalize-space(),'Create account with email')]"
    )
    SIGNUP_EMAIL_INPUT    = (By.CSS_SELECTOR, "input[name='loginId']")
    SIGNUP_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[autocomplete='new-password']")
    SIGNUP_NAME_INPUT     = (By.CSS_SELECTOR, "input[name='fullname']")
    AGREE_ALL_CHECKBOX    = (By.CSS_SELECTOR, "input.PrivateSwitchBase-input[type='checkbox']")
    SIGNUP_SUBMIT         = (By.XPATH,
        "//button[@type='submit' and @form='signup-form']"
        " | //button[@type='submit' and contains(@class,'MuiLoadingButton-root')]"
    )

    # ========== FHC-077: 탈퇴 영역 스크롤 ==========

    def scroll_to_withdraw_area(self):
        """JS로 탈퇴 관련 버튼/섹션 찾아 스크롤"""
        self.driver.execute_script("""
            var kws = ['탈퇴', 'Leave', 'Delete Account', 'Delete account',
                       'Withdraw', 'Deactivate', 'Close Account'];
            var els = Array.from(document.querySelectorAll('button, h2, h3, h4, span, p'));
            var target = els.find(function(el) {
                var txt = (el.innerText || '').trim();
                return kws.some(function(k){ return txt === k || txt.includes(k); });
            });
            if (target) { target.scrollIntoView({behavior:'auto', block:'center'}); }
            else { window.scrollTo(0, document.body.scrollHeight); }
        """)
        time.sleep(0.5)
        print("탈퇴 영역으로 스크롤 완료")

    def is_withdraw_area_displayed(self) -> bool:
        """JS로 탈퇴 버튼 존재 여부 확인"""
        try:
            result = self.driver.execute_script("""
                var kws = ['탈퇴', 'Leave', 'Delete Account', 'Delete account',
                           'Withdraw', 'Deactivate', 'Close Account'];
                var btns = Array.from(document.querySelectorAll('button'));
                return btns.some(function(btn) {
                    var txt = (btn.innerText || '').trim();
                    return kws.some(function(k){ return txt === k || txt.includes(k); });
                });
            """)
            return bool(result)
        except Exception:
            return False

    # ========== FHC-078: 탈퇴 확인 ==========

    def click_withdraw_button(self):
        """JS로 탈퇴 버튼 찾아 클릭 (한/영 모두)"""
        result = self.driver.execute_script("""
            var kws = ['탈퇴하기', '탈퇴', 'Leave', 'Delete Account', 'Delete account',
                       'Withdraw', 'Deactivate', 'Close Account'];
            var btns = Array.from(document.querySelectorAll('button'));
            var found = btns.find(function(btn) {
                var txt = (btn.innerText || '').trim();
                return kws.some(function(k){ return txt === k || txt.includes(k); });
            });
            if (found) { found.click(); return 'clicked: ' + found.innerText.trim(); }
            return 'not-found';
        """)
        if result == 'not-found':
            raise Exception("탈퇴 버튼을 찾을 수 없습니다")
        time.sleep(0.5)
        print(f"탈퇴하기 버튼 클릭 완료 ({result})")

    def is_withdraw_confirm_message_displayed(self) -> bool:
        try:
            self.wait.until(
                lambda d: any(
                    kw in d.find_element(By.TAG_NAME, "body").text
                    for kw in ["Delete", "탈퇴하려면", "정확히 입력"]
                )
            )
            return True
        except Exception:
            return False

    # ========== FHC-079: 탈퇴 실행 ==========

    def enter_withdraw_confirm_text(self, email: str):
        """'Delete [전체 이메일]' 형식으로 입력"""
        input_el = self.wait.until(
            EC.visibility_of_element_located(self.WITHDRAW_CONFIRM_INPUT)
        )
        confirm_text = f"Delete {email}"
        input_el.clear()
        input_el.send_keys(confirm_text)
        print(f"탈퇴 확인 문구 입력 완료: {confirm_text}")

    def submit_withdraw(self):
        self.js_click(
            self.wait.until(EC.element_to_be_clickable(self.WITHDRAW_FINAL_BUTTON))
        )
        print("최종 탈퇴 제출 완료")

    def is_withdrawal_complete(self) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: (
                    "login" in d.current_url.lower()
                    or "signin" in d.current_url.lower()
                    or "withdraw" in d.current_url.lower()
                    or any(
                        kw in d.find_element(By.TAG_NAME, "body").text
                        for kw in ["탈퇴", "로그인", "Login"]
                    )
                )
            )
            return True
        except Exception:
            return False

    # ========== FHC-080: 재가입 ==========

    def signup(self, email: str, password: str, name: str):
        """로그인 페이지 → Create account → 이메일로 가입하기 → 폼 입력 → 제출"""
        self.js_click(
            self.wait.until(EC.element_to_be_clickable(self.SIGNUP_LINK))
        )
        print("Create account 링크 클릭 완료")

        self.js_click(
            self.wait.until(EC.element_to_be_clickable(self.EMAIL_SIGNUP_BUTTON))
        )
        print("이메일로 가입하기 클릭 완료")

        email_input = self.wait.until(EC.visibility_of_element_located(self.SIGNUP_EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)

        pw_input = self.wait.until(EC.visibility_of_element_located(self.SIGNUP_PASSWORD_INPUT))
        pw_input.clear()
        pw_input.send_keys(password)

        name_input = self.wait.until(EC.visibility_of_element_located(self.SIGNUP_NAME_INPUT))
        name_input.clear()
        name_input.send_keys(name)

        agree_checkbox = self.wait.until(
            EC.presence_of_element_located(self.AGREE_ALL_CHECKBOX)
        )
        self.driver.execute_script("arguments[0].click();", agree_checkbox)
        time.sleep(0.3)
        print("전체 동의 클릭 완료")

        self.js_click(
            self.wait.until(EC.element_to_be_clickable(self.SIGNUP_SUBMIT))
        )
        print(f"회원가입 제출 완료: {email}")
        time.sleep(2)

    def is_signup_success(self) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: (
                    "ai-helpy-chat" in d.current_url
                    or "qaproject.elice.io" in d.current_url
                )
            )
            return True
        except Exception:
            return False
