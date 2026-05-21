import glob
import os
import random
import time

from config.selenium_imports import By, EC


from pages.tools.base_tool_page import BaseToolPage


class PPTPage(BaseToolPage):

    TOOL_NAME = "PPT 생성"

    # ========== Locators ==========

    TOPIC_INPUT           = (By.CSS_SELECTOR, "input[name='topic']")
    INSTRUCTIONS_TEXTAREA = (By.CSS_SELECTOR, "textarea[name='instructions']")
    SLIDES_COUNT_INPUT    = (By.CSS_SELECTOR, "input[name='slides_count']")
    SECTION_COUNT_INPUT   = (By.CSS_SELECTOR, "input[name='section_count']")

    GENERATE_BTN = (
        By.CSS_SELECTOR,
        "button[type='submit'][form='tool-factory-create_pptx']",
    )

    DEEP_RESEARCH_INPUT  = (By.CSS_SELECTOR, "input[name='simple_mode']")
    DEEP_RESEARCH_TOGGLE = (
        By.XPATH,
        "//input[@name='simple_mode']/ancestor::span[contains(@class,'MuiSwitch-root')]",
    )
    SUCCESS_MESSAGE = (
        By.XPATH,
        "//div[@role='tabpanel'][@data-panel='output']"
        "//p[contains(., '입력하신 내용 기반으로 PPT를 생성했습니다')]",
    )
    DOWNLOAD_BTN = (
        By.XPATH,
        "//a[contains(., '생성 결과 다운받기')]",
    )

    # ========== 입력 필드 사전 체크 / 초기화 ==========

    def has_any_field_value(self):
        for locator in [
            self.TOPIC_INPUT,
            self.INSTRUCTIONS_TEXTAREA,
            self.SLIDES_COUNT_INPUT,
            self.SECTION_COUNT_INPUT,
        ]:
            try:
                if self.driver.find_element(*locator).get_attribute("value"):
                    return True
            except Exception:
                pass
        return False

    def clear_all_fields(self):
        for locator in [
            self.TOPIC_INPUT,
            self.INSTRUCTIONS_TEXTAREA,
            self.SLIDES_COUNT_INPUT,
            self.SECTION_COUNT_INPUT,
        ]:
            try:
                el = self.wait.until(EC.element_to_be_clickable(locator))
                el.click()
                time.sleep(0.3)
                el.clear()
            except Exception:
                pass
        time.sleep(0.5)

    # ========== 필수 입력 ==========

    def enter_topic(self, topic):
        inp = self.wait.until(EC.element_to_be_clickable(self.TOPIC_INPUT))
        inp.click()
        time.sleep(0.5)
        inp.clear()
        inp.send_keys(topic)
        time.sleep(0.5)
        assert inp.get_attribute("value") == topic, \
            f"주제 '{topic}' 입력 실패"

    # ========== 선택 입력 ==========

    def enter_instructions(self, instructions):
        if not instructions:
            return
        ta = self.wait.until(EC.element_to_be_clickable(self.INSTRUCTIONS_TEXTAREA))
        ta.click()
        time.sleep(0.5)
        ta.clear()
        ta.send_keys(instructions)
        time.sleep(0.5)
        assert ta.get_attribute("value") == instructions, \
            f"지시사항 '{instructions}' 입력 실패"

    def enter_slides_count(self, count=None):
        count = count or str(random.randint(3, 10))
        inp = self.wait.until(EC.element_to_be_clickable(self.SLIDES_COUNT_INPUT))
        inp.click()
        time.sleep(0.5)
        inp.clear()
        inp.send_keys(count)
        time.sleep(0.5)
        assert inp.get_attribute("value") == count, \
            f"슬라이드 수 '{count}' 입력 실패"

    def enter_section_count(self, count=None):
        count = count or str(random.randint(1, 5))
        inp = self.wait.until(EC.element_to_be_clickable(self.SECTION_COUNT_INPUT))
        inp.click()
        time.sleep(0.5)
        inp.clear()
        inp.send_keys(count)
        time.sleep(0.5)
        assert inp.get_attribute("value") == count, \
            f"섹션 수 '{count}' 입력 실패"

    # ========== 심층조사 모드 토글 ==========

    def is_deep_research_on(self):
        inp = self.driver.find_element(*self.DEEP_RESEARCH_INPUT)
        return self.driver.execute_script("return arguments[0].checked;", inp)

    def click_deep_research_toggle(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.DEEP_RESEARCH_TOGGLE))
        self.js_click(toggle)

    # ========== 생성 버튼 스크롤 ==========

    def scroll_to_generate_btn(self):
        btn = self.wait.until(EC.presence_of_element_located(self.GENERATE_BTN))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn
        )
        time.sleep(0.5)

    # ========== 다운로드 ==========

    def click_download(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.DOWNLOAD_BTN))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn
        )
        time.sleep(0.5)
        self.js_click(btn)
        time.sleep(1)

    def is_pptx_downloaded(self, download_dir, timeout=30):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if glob.glob(os.path.join(download_dir, "*.pptx")):
                return True
            time.sleep(1)
        return False

    # ========== 생성 버튼 활성화 확인 / 클릭 / 결과 대기 ==========

    def is_generate_btn_enabled(self) -> bool:
        try:
            btn = self.wait.until(EC.presence_of_element_located(self.GENERATE_BTN))
            return btn.is_enabled()
        except Exception:
            return False

    def click_generate(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.GENERATE_BTN))
        self.js_click(btn)

    def wait_for_generation(self, timeout: int = 120) -> bool:
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
        except Exception:
            return False
