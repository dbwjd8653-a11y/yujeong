import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class SettingsPage:

    _GEAR_BTN = (By.CSS_SELECTOR, 'button:has(svg[data-testid="gearIcon"])')
    _SETTINGS_MENU_ITEM = (By.CSS_SELECTOR, 'a[role="menuitem"]:has(svg[data-testid="gearIcon"])')
    _POPUP_CLOSE_BTN = (By.CSS_SELECTOR, 'button:has(svg[data-icon="xmark-large"])')
    _ADMIN_URL = "/ai-helpy-chat/admin"

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def close_popup_if_present(self):
        try:
            short_wait = WebDriverWait(self.driver, 3)
            popup_text = short_wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[contains(text(),"개인 토큰 한도가 설정되었습니다.")]')
                )
            )
            assert "개인 토큰 한도가 설정되었습니다." in popup_text.text, "팝업 텍스트 불일치"
            close_btn = short_wait.until(
                EC.element_to_be_clickable(self._POPUP_CLOSE_BTN)
            )
            close_btn.click()
            time.sleep(0.5)
            print("팝업 닫기 완료")
        except TimeoutException:
            pass

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

        self.close_popup_if_present()
