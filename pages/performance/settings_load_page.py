from config.selenium_imports import By, EC

from pages.settings.settings_general_page import SettingsPage


class SettingsLoadPage(SettingsPage):

    _GENERAL_TAB      = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/general"][role="tab"]')
    _HISTORY_TAB      = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/history"][role="tab"]')
    _MODELS_TAB       = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/models"][role="tab"]')
    _SUBSCRIPTION_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/subscription"][role="tab"]')
    _MEMBER_TAB       = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/users"][role="tab"]')

    def _js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def click_all_tabs_three_times(self):
        for _ in range(3):
            self._js_click(self.wait.until(EC.element_to_be_clickable(self._GENERAL_TAB)))
            self.wait.until(EC.url_contains("/ai-helpy-chat/admin/general"))

            self._js_click(self.wait.until(EC.element_to_be_clickable(self._HISTORY_TAB)))
            self.wait.until(EC.url_contains("/ai-helpy-chat/admin/history"))

            self._js_click(self.wait.until(EC.element_to_be_clickable(self._MODELS_TAB)))
            self.wait.until(EC.url_contains("/ai-helpy-chat/admin/models"))

            self._js_click(self.wait.until(EC.element_to_be_clickable(self._SUBSCRIPTION_TAB)))
            self.wait.until(EC.url_contains("/ai-helpy-chat/admin/subscription"))

            self._js_click(self.wait.until(EC.element_to_be_clickable(self._MEMBER_TAB)))
            self.wait.until(EC.url_contains("/ai-helpy-chat/admin/users"))
