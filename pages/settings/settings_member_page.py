from config.selenium_imports import By, EC, WebDriverWait

from pages.settings.settings_general_page import SettingsPage


class SettingsMemberPage(SettingsPage):

    _MEMBER_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/users"][role="tab"]')
    _TOKEN_LIMIT_TOGGLE = (By.CSS_SELECTOR, 'span.MuiSwitch-sizeMedium input[type="checkbox"]')
    _SAVE_BTN = (By.XPATH, '//button[@type="submit"][normalize-space()="저장"]')
    _TOAST = (By.ID, 'notistack-snackbar')

    def navigate_to_member_tab(self):
        self.js_click(self.wait.until(EC.element_to_be_clickable(self._MEMBER_TAB)))
        self.wait.until(EC.url_contains("/ai-helpy-chat/admin/users"))

    def get_toggle(self):
        toggle = self.wait.until(EC.presence_of_element_located(self._TOKEN_LIMIT_TOGGLE))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
        return toggle

    def is_toggle_checked(self, toggle):
        return self.driver.execute_script("return arguments[0].checked", toggle)

    def set_token_limit_toggle(self, activate: bool):
        toggle = self.get_toggle()
        if self.is_toggle_checked(toggle) != activate:
            self.js_click(toggle)
            WebDriverWait(self.driver, 5).until(
                lambda d: self.is_toggle_checked(d.find_element(*self._TOKEN_LIMIT_TOGGLE)) == activate
            )

    def _wait_visible_save_btn(self):
        """'저장' 제출 버튼이 섹션별 form마다 여러 개 존재할 수 있어,
        DOM 첫 매치(숨겨진 버튼)를 잡으면 element_to_be_clickable이 타임아웃난다.
        화면에 보이고 활성화된 버튼만 골라 반환한다."""
        def _find(driver):
            for btn in driver.find_elements(*self._SAVE_BTN):
                if btn.is_displayed() and btn.is_enabled():
                    return btn
            return False
        return self.wait.until(_find)

    def save_and_verify_toast(self):
        try:
            self.wait_until_invisible(self._TOAST, 5)
        except Exception:
            pass
        save_btn = self._wait_visible_save_btn()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        self.js_click(save_btn)
        toast = self.wait_for_visible(self._TOAST)
        assert "저장되었습니다" in toast.text, f"저장 알림창 메시지 불일치: '{toast.text}'"
