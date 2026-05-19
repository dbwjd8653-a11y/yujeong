"""
모든 Page Object가 상속받는 최상위 부모 클래스.
공통 동작(js_click, click, enter_text, get_text, wait 관련)과 명시적 대기를 래핑합니다.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ── 대기 시간 상수 ─────────────────────────────────────────────────
DEFAULT_WAIT = 10  # 기본 대기


class BasePage:
    """모든 페이지 객체의 부모 클래스"""

    def __init__(self, driver, wait=None):
        self.driver = driver
        self.wait = wait if wait else WebDriverWait(driver, DEFAULT_WAIT)

    def js_click(self, element):
        """Firefox 대응 JavaScript 클릭"""
        self.driver.execute_script("arguments[0].click();", element)

    def click(self, locator):
        """요소가 클릭 가능해질 때까지 대기 후 클릭"""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, text):
        """요소가 보일 때까지 대기 후 텍스트 입력"""
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)
        print(f"입력된 텍스트: {text}")

    def get_text(self, locator):
        """요소가 보일 때까지 대기 후 텍스트 반환"""
        return self.wait_for_visible(locator).text

    def wait_for_visible(self, locator):
        """요소가 화면에 보일 때까지 대기 후 반환"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_invisible(self, locator, timeout=DEFAULT_WAIT):
        """요소가 화면에서 사라질 때까지 대기
        주의: __init__의 self.wait과 별개인 일회용 타이머입니다.
        """
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_for_url_contains(self, text):
        """URL에 특정 텍스트가 포함될 때까지 대기"""
        self.wait.until(EC.url_contains(text))
