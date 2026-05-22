import time

from config.selenium_imports import By, EC

from pages.settings.settings_general_page import SettingsPage


class SettingsUseagePage(SettingsPage):

    _HISTORY_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/history"][role="tab"]')

    def navigate_to_history_tab(self):
        self.wait.until(EC.element_to_be_clickable(self._HISTORY_TAB)).click()
        self.wait.until(EC.url_contains("/ai-helpy-chat/admin/history"))
        time.sleep(3)
