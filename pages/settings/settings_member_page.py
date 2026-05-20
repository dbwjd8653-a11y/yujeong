import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.settings_page import SettingsPage


class Settings05Page(SettingsPage):

    _MEMBER_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/users"][role="tab"]')
    _NO_LIMIT_CHECKBOX = (By.CSS_SELECTOR, 'input[name="accountTokenQuotaList.0.quota.noLimit"][type="checkbox"]')
    _TOKEN_INPUT = (By.CSS_SELECTOR, 'input[name="accountTokenQuotaList.0.quota.quantity"]')
    _GLOBAL_TOKEN_INPUT = (By.CSS_SELECTOR, 'input[name="quota.quantity"]')
    _TOKEN_LIMIT_TOGGLE = (By.CSS_SELECTOR, 'span.MuiSwitch-sizeMedium input[type="checkbox"]')
    _SAVE_BTN = (By.XPATH, '//button[text()="저장"]')
    _TOAST = (By.ID, "notistack-snackbar")

    def navigate_to_member_tab(self):
        self.wait.until(EC.element_to_be_clickable(self._MEMBER_TAB)).click()
        assert self.wait.until(EC.url_contains("/ai-helpy-chat/admin/users")), "구성원 관리 탭 이동 실패"
        time.sleep(3)

    def click_no_limit_checkbox(self):
        checkbox = self.wait.until(EC.presence_of_element_located(self._NO_LIMIT_CHECKBOX))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
        time.sleep(0.5)
        if self.driver.execute_script("return arguments[0].checked", checkbox):
            self.driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(1)
        self.driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(2)

    def is_no_limit_checked(self):
        checkbox = self.driver.find_element(*self._NO_LIMIT_CHECKBOX)
        return self.driver.execute_script("return arguments[0].checked", checkbox)

    def is_token_input_disabled(self):
        return not self.driver.find_element(*self._TOKEN_INPUT).is_enabled()

    def set_global_token(self, value):
        input_el = self.wait.until(EC.presence_of_element_located(self._GLOBAL_TOKEN_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_el)
        time.sleep(0.5)
        input_el.clear()
        input_el.send_keys(value)
        time.sleep(1)

    def get_toggle(self):
        toggle = self.wait.until(EC.presence_of_element_located(self._TOKEN_LIMIT_TOGGLE))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
        time.sleep(0.5)
        return toggle

    def is_toggle_checked(self, toggle):
        return self.driver.execute_script("return arguments[0].checked", toggle)

    def ensure_toggle_enabled(self, toggle):
        if not self.is_toggle_checked(toggle):
            self.driver.execute_script("arguments[0].click();", toggle)
            time.sleep(1)

    def click_toggle(self, toggle):
        self.driver.execute_script("arguments[0].click();", toggle)
        time.sleep(1)

    def save_and_verify_toast(self):
        save_btn = self.wait.until(EC.element_to_be_clickable(self._SAVE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        time.sleep(0.5)
        save_btn.click()
        time.sleep(1)
        assert self.wait.until(EC.text_to_be_present_in_element(
            self._TOAST, "토큰 한도가 저장되었습니다"
        )), "토큰 한도 저장 알림 팝업 미확인"
        time.sleep(2)
