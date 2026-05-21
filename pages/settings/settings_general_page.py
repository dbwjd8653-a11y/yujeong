import time

from config.selenium_imports import By, EC

from config.login_helpers import close_token_banner


class SettingsPage:

    _GEAR_BTN = (By.CSS_SELECTOR, 'button:has(svg[data-testid="gearIcon"])')
    _SETTINGS_MENU_ITEM = (By.CSS_SELECTOR, 'a[role="menuitem"]:has(svg[data-testid="gearIcon"])')
    _ADMIN_URL = "/ai-helpy-chat/admin"

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def navigate_to_settings(self):
        self.driver.find_element(*self._GEAR_BTN).click()
        time.sleep(1)

        self.wait.until(EC.element_to_be_clickable(self._SETTINGS_MENU_ITEM)).click()
        time.sleep(1)

        self.wait.until(EC.url_contains(self._ADMIN_URL))
        assert self._ADMIN_URL in self.driver.current_url, \
            f"설정 페이지 이동 실패: {self.driver.current_url}"
        print("설정 페이지 이동 성공:", self.driver.current_url)
        time.sleep(2)

        close_token_banner(self.driver, self.wait)
