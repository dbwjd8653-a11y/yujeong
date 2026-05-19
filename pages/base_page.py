# pages/base_page.py
# 모든 Page 클래스가 공통으로 상속받는 베이스 클래스
# js_click, js_input, wait 유틸리티 메서드를 한 곳에서 관리

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ========== JS 유틸리티 ==========

    def js_click(self, element):
        """일반 클릭이 막힐 때 JavaScript로 클릭"""
        self.driver.execute_script("arguments[0].click();", element)

    def js_input(self, element, text):
        """React controlled input/textarea에 JS로 값 입력
        (React가 value를 직접 제어하므로 send_keys만으로는 상태가 갱신되지 않음)"""
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

    # ========== 대기 유틸리티 ==========

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
        """MUI Select 드롭다운(listbox)이 닫힐 때까지 대기 — 옵션 선택 직후 호출"""
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
        time.sleep(0.3)  # MUI 다이얼로그 닫힘 애니메이션(~225ms) 여유
