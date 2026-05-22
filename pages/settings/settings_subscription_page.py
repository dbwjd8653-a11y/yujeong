import time

from config.selenium_imports import By, EC

from pages.settings.settings_general_page import SettingsPage


class SettingsSubscriptionPage(SettingsPage):

    _SUBSCRIPTION_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/subscription"][role="tab"]')

    def navigate_to_subscription_tab(self):
        self.wait.until(EC.element_to_be_clickable(self._SUBSCRIPTION_TAB)).click()
        self.wait.until(EC.url_contains("/ai-helpy-chat/admin/subscription"))
        time.sleep(3)
