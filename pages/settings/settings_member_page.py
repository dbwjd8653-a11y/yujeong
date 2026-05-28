import time

from config.selenium_imports import By, EC

from pages.settings.settings_general_page import SettingsPage


class SettingsMemberPage(SettingsPage):

    _MEMBER_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/users"][role="tab"]')
    _TOKEN_LIMIT_TOGGLE = (By.CSS_SELECTOR, 'span.MuiSwitch-sizeMedium input[type="checkbox"]')
    _SAVE_BTN = (By.XPATH, '//button[normalize-space()="저장"]')
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
            time.sleep(1)

    def save_and_verify_toast(self):
        try:
            self.wait_until_invisible(self._TOAST, 5)
        except Exception:
            pass
        save_btn = self.wait.until(EC.element_to_be_clickable(self._SAVE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        self.js_click(save_btn)
        toast = self.wait_for_visible(self._TOAST)
        assert "저장되었습니다" in toast.text, f"저장 알림창 메시지 불일치: '{toast.text}'"
