import time

from config.selenium_imports import By, EC, WebDriverWait

from pages.settings.settings_general_page import SettingsPage


class SettingsMemberPage(SettingsPage):

    _MEMBER_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/users"][role="tab"]')
    _NO_LIMIT_CHECKBOX = (By.CSS_SELECTOR, 'input[name="accountTokenQuotaList.0.quota.noLimit"][type="checkbox"]')
    _TOKEN_INPUT = (By.CSS_SELECTOR, 'input[name="accountTokenQuotaList.0.quota.quantity"]')
    _GLOBAL_TOKEN_INPUT = (By.CSS_SELECTOR, 'input[name="quota.quantity"]')
    _TOKEN_LIMIT_TOGGLE = (By.CSS_SELECTOR, 'span.MuiSwitch-sizeMedium input[type="checkbox"]')
    _SAVE_BTN = (By.XPATH, '//button[normalize-space()="저장"]')
    _TOAST = (By.ID, 'notistack-snackbar')

    def navigate_to_member_tab(self):
        self.wait.until(EC.element_to_be_clickable(self._MEMBER_TAB)).click()
        self.wait.until(EC.url_contains("/ai-helpy-chat/admin/users"))
        time.sleep(3)

    def click_no_limit_checkbox(self):
        checkbox = self.wait.until(EC.presence_of_element_located(self._NO_LIMIT_CHECKBOX))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
        if self.driver.execute_script("return arguments[0].checked", checkbox):
            self.driver.execute_script("arguments[0].click();", checkbox)
        self.driver.execute_script("arguments[0].click();", checkbox)

    def is_no_limit_checked(self):
        checkbox = self.driver.find_element(*self._NO_LIMIT_CHECKBOX)
        return self.driver.execute_script("return arguments[0].checked", checkbox)

    def is_token_input_disabled(self):
        return not self.driver.find_element(*self._TOKEN_INPUT).is_enabled()

    def set_global_token(self, value):
        input_el = self.wait.until(EC.presence_of_element_located(self._GLOBAL_TOKEN_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_el)
        input_el.clear()
        input_el.send_keys(value)

    def get_toggle(self):
        toggle = self.wait.until(EC.presence_of_element_located(self._TOKEN_LIMIT_TOGGLE))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
        return toggle

    def is_toggle_checked(self, toggle):
        return self.driver.execute_script("return arguments[0].checked", toggle)

    def set_token_limit_toggle(self, activate: bool):
        toggle = self.get_toggle()
        if self.is_toggle_checked(toggle) != activate:
            self.driver.execute_script("arguments[0].click();", toggle)
            time.sleep(1)

    def save_and_verify_toast(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self._TOAST)
            )
        except Exception:
            pass
        save_btn = self.wait.until(EC.element_to_be_clickable(self._SAVE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        self.driver.execute_script("arguments[0].click();", save_btn)
        toast = self.wait.until(EC.visibility_of_element_located(self._TOAST))
        assert "저장되었습니다" in toast.text, f"저장 알림창 메시지 불일치: '{toast.text}'"
