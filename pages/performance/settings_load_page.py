import time

from config.selenium_imports import By, EC

from pages.settings.settings_general_page import SettingsPage


class SettingsLoadPage(SettingsPage):

    _GENERAL_TAB      = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/general"][role="tab"]')
    _HISTORY_TAB      = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/history"][role="tab"]')
    _MODELS_TAB       = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/models"][role="tab"]')
    _SUBSCRIPTION_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/subscription"][role="tab"]')
    _MEMBER_TAB       = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/users"][role="tab"]')

    def click_all_tabs_three_times(self):
        for _ in range(3):
            self.wait.until(EC.element_to_be_clickable(self._GENERAL_TAB)).click()
            assert self.wait.until(EC.url_contains("/ai-helpy-chat/admin/general")), "일반 탭 이동 실패"
            time.sleep(0.5)

            self.wait.until(EC.element_to_be_clickable(self._HISTORY_TAB)).click()
            assert self.wait.until(EC.url_contains("/ai-helpy-chat/admin/history")), "이용 내역 탭 이동 실패"
            time.sleep(0.5)

            self.wait.until(EC.element_to_be_clickable(self._MODELS_TAB)).click()
            assert self.wait.until(EC.url_contains("/ai-helpy-chat/admin/models")), "모델 설정 탭 이동 실패"
            time.sleep(0.5)

            self.wait.until(EC.element_to_be_clickable(self._SUBSCRIPTION_TAB)).click()
            assert self.wait.until(EC.url_contains("/ai-helpy-chat/admin/subscription")), "구독 관리 탭 이동 실패"
            time.sleep(0.5)

            self.wait.until(EC.element_to_be_clickable(self._MEMBER_TAB)).click()
            assert self.wait.until(EC.url_contains("/ai-helpy-chat/admin/users")), "구성원 관리 탭 이동 실패"
            time.sleep(0.5)
