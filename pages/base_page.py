# pages/base_page.py
# 모든 Page 클래스가 공통으로 상속받는 베이스 클래스

import logging
import time

from config.selenium_imports import By, EC, WebDriverWait

class BasePage:

    def __init__(self, driver, wait_or_timeout=10):
        self.driver = driver
        if isinstance(wait_or_timeout, WebDriverWait):
            self.wait = wait_or_timeout
        else:
            self.wait = WebDriverWait(driver, wait_or_timeout)
        self.logger = logging.getLogger(self.__class__.__name__)

    # ========== 클릭 유틸리티 ==========

    def js_click(self, element):
        """JavaScript로 클릭 (일반 클릭이 막힐 때 사용)"""
        self.driver.execute_script("arguments[0].click();", element)

    def click(self, locator):
        """요소가 클릭 가능해질 때까지 대기 후 클릭"""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    # ========== 입력 유틸리티 ==========

    def enter_text(self, locator, text):
        """요소가 보일 때까지 대기 후 텍스트 입력"""
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)

    def js_input(self, element, text):
        """React controlled input/textarea에 JS로 값 입력"""
        self.driver.execute_script(
            """
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value').set;
            nativeInputValueSetter.call(arguments[0], arguments[1]);
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            text,
        )

    # ========== 조회 유틸리티 ==========

    def get_text(self, locator):
        """요소가 보일 때까지 대기 후 텍스트 반환"""
        return self.wait_for_visible(locator).text

    # ========== 대기 유틸리티 ==========

    def wait_for_visible(self, locator):
        """요소가 화면에 보일 때까지 대기 후 반환"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_invisible(self, locator, timeout=10):
        """요소가 화면에서 사라질 때까지 대기"""
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_for_url_contains(self, text):
        """URL에 특정 텍스트가 포함될 때까지 대기"""
        self.wait.until(EC.url_contains(text))

    def wait_backdrop_gone(self, timeout=5):
        """MUI Backdrop(딤 레이어)이 사라질 때까지 대기"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(
                    (By.CLASS_NAME, "MuiBackdrop-root")
                )
            )
        except Exception:
            pass

    def wait_dropdown_closed(self, timeout=5):
        """MUI Select 드롭다운(listbox)이 닫힐 때까지 대기"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//ul[@role='listbox']")
                )
            )
        except Exception:
            pass

    def wait_dialog_gone(self, timeout=10):
        """MUI Dialog가 완전히 닫힐 때까지 대기"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "h2.MuiDialogTitle-root")
                )
            )
        except Exception:
            pass
        time.sleep(0.3)
