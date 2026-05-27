import glob
import os
import random
import time

from config.selenium_imports import By, EC
from pages.tools.base_tool_page import BaseToolPage


class PPTPage(BaseToolPage):

    TOOL_NAME = "PPT 생성"

    # 생성 완료 후 LinearProgress가 indeterminate → determinate로 교체되어 DOM 잔류
    SPINNER = (By.CSS_SELECTOR, "span.MuiLinearProgress-indeterminate[role='progressbar']")

    # ========== Locators ==========

    TOPIC_INPUT           = (By.CSS_SELECTOR, "input[name='topic']")
    INSTRUCTIONS_TEXTAREA = (By.CSS_SELECTOR, "textarea[name='instructions']")
    SLIDES_COUNT_INPUT    = (By.CSS_SELECTOR, "input[name='slides_count']")
    SECTION_COUNT_INPUT   = (By.CSS_SELECTOR, "input[name='section_count']")

    GENERATE_BTN = (
        By.XPATH,
        "//button[@type='submit'][@form='tool-factory-create_pptx']"
        "[not(ancestor::div[@role='dialog'])]",
    )
    REGEN_CONFIRM_BTN = (
        By.XPATH,
        "//div[@role='dialog']//button[@type='submit'][@form='tool-factory-create_pptx']",
    )
    REGEN_CANCEL_BTN = (
        By.XPATH,
        "//div[@role='dialog']//button[@type='button' and normalize-space()='취소']",
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

    _ALL_FIELDS = [
        "TOPIC_INPUT",
        "INSTRUCTIONS_TEXTAREA",
        "SLIDES_COUNT_INPUT",
        "SECTION_COUNT_INPUT",
    ]

    # ========== 입력 필드 사전 체크 / 초기화 ==========

    def has_any_field_value(self):
        for locator in [getattr(self, f) for f in self._ALL_FIELDS]:
            try:
                if self.driver.find_element(*locator).get_attribute("value"):
                    return True
            except Exception:
                pass
        return False

    def clear_all_fields(self):
        for locator in [getattr(self, f) for f in self._ALL_FIELDS]:
            try:
                el = self.wait.until(EC.element_to_be_clickable(locator))
                el.click()
                el.clear()
            except Exception:
                pass

    # ========== 필수 입력 ==========

    def enter_topic(self, topic):
        inp = self.wait.until(EC.element_to_be_clickable(self.TOPIC_INPUT))
        inp.click()
        inp.clear()
        inp.send_keys(topic)

    # ========== 선택 입력 ==========

    def enter_instructions(self, instructions):
        if not instructions:
            return
        ta = self.wait.until(EC.element_to_be_clickable(self.INSTRUCTIONS_TEXTAREA))
        ta.click()
        ta.clear()
        ta.send_keys(instructions)

    def enter_slides_count(self, count=None):
        count = count or str(random.randint(3, 10))
        inp = self.wait.until(EC.element_to_be_clickable(self.SLIDES_COUNT_INPUT))
        inp.click()
        inp.clear()
        inp.send_keys(count)

    def enter_section_count(self, count=None):
        count = count or str(random.randint(1, 5))
        inp = self.wait.until(EC.element_to_be_clickable(self.SECTION_COUNT_INPUT))
        inp.click()
        inp.clear()
        inp.send_keys(count)

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

    # ========== 다운로드 ==========

    def download_result(self, download_dir: str, browser: str = "firefox"):
        existing = set(glob.glob(os.path.join(download_dir, "*.pptx")))
        btn = self.wait.until(EC.element_to_be_clickable(self.DOWNLOAD_BTN))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn
        )
        self.js_click(btn)
        self.logger.info("생성 결과 다운받기 버튼 클릭 완료")

        self.logger.info("파일 다운로드 대기 중...")
        temp_ext = "*.part" if browser.lower() == "firefox" else "*.crdownload"
        deadline = time.time() + 30
        while time.time() < deadline:
            time.sleep(1)
            current = set(glob.glob(os.path.join(download_dir, "*.pptx")))
            new_files = current - existing
            temp_files = glob.glob(os.path.join(download_dir, temp_ext))
            if new_files and not temp_files:
                self.logger.info(f"다운로드 완료: {list(new_files)[0]}")
                return True
        self.logger.warning("다운로드 타임아웃 (30초 초과)")
        return False

    # ========== 생성 버튼 활성화 확인 / 클릭 / 결과 대기 ==========

    def is_generate_btn_enabled(self) -> bool:
        try:
            btn = self.wait.until(EC.presence_of_element_located(self.GENERATE_BTN))
            return btn.is_enabled()
        except Exception:
            return False

    def click_generate_and_cancel(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.GENERATE_BTN))
            self.js_click(btn)
            cancel = self.wait.until(EC.element_to_be_clickable(self.REGEN_CANCEL_BTN))
            self.js_click(cancel)
            return True
        except Exception:
            return False


