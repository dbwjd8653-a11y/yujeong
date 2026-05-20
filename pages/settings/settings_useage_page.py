import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.settings.settings_general_page import SettingsPage


class Settings02Page(SettingsPage):

    _HISTORY_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/history"][role="tab"]')

    def navigate_to_history_tab(self):
        self.wait.until(EC.element_to_be_clickable(self._HISTORY_TAB)).click()
        assert self.wait.until(EC.url_contains("/ai-helpy-chat/admin/history")), "이용 내역 탭 이동 실패"
        time.sleep(3)
