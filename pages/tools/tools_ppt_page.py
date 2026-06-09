import os
import random
from urllib.parse import urlparse

import requests

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

    def tools_menu(self):
        self.click_tool_menu(self.TOOL_NAME)

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
                self.js_input(el, "")
            except Exception:
                pass

    # ========== 필수 입력 ==========

    def enter_topic(self, topic):
        inp = self.wait.until(EC.element_to_be_clickable(self.TOPIC_INPUT))
        self.js_input(inp, topic)

    # ========== 선택 입력 ==========

    def enter_instructions(self, instructions):
        if not instructions:
            return
        ta = self.wait.until(EC.element_to_be_clickable(self.INSTRUCTIONS_TEXTAREA))
        self.js_input(ta, instructions)

    def enter_slides_count(self, count=None):
        count = count or str(random.randint(3, 10))
        inp = self.wait.until(EC.element_to_be_clickable(self.SLIDES_COUNT_INPUT))
        self.js_input(inp, count)

    def enter_section_count(self, count=None):
        count = count or str(random.randint(1, 5))
        inp = self.wait.until(EC.element_to_be_clickable(self.SECTION_COUNT_INPUT))
        self.js_input(inp, count)

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

    def download_result(self, download_dir: str, browser: str = "edge"):
        """'생성 결과 다운받기' 링크(href)를 직접 받아 저장한다.

        href는 Azure Blob Storage의 SAS 서명 포함 직접 파일 URL이라 쿠키 없이
        접근 가능하다. 클릭 방식은 Edge 내장 Office 뷰어가 .pptx를 새 탭에서
        열어버려(다운로드 대신) 실패하므로, href를 HTTP GET으로 직접 받는다.
        """
        btn = self.wait.until(EC.element_to_be_clickable(self.DOWNLOAD_BTN))
        href = btn.get_attribute("href")
        if not href:
            self.logger.warning("다운로드 링크(href)를 찾을 수 없습니다")
            return False
        self.logger.info("생성 결과 다운로드 URL 획득")

        os.makedirs(download_dir, exist_ok=True)
        filename = os.path.basename(urlparse(href).path) or "result.pptx"
        dest = os.path.join(download_dir, filename)

        try:
            resp = requests.get(href, timeout=60)
            resp.raise_for_status()
        except Exception as e:
            self.logger.warning(f"파일 다운로드 요청 실패: {e}")
            return False

        if not resp.content:
            self.logger.warning("다운로드 응답이 비어 있습니다")
            return False

        # pptx는 zip 컨테이너 — PK 시그니처로 산출물 무결성 검증 (HTML 에러 페이지 등 false pass 방지)
        if resp.content[:4] != b"PK\x03\x04":
            self.logger.warning("받은 파일이 유효한 pptx(zip)가 아닙니다")
            return False

        with open(dest, "wb") as f:
            f.write(resp.content)
        self.logger.info(f"다운로드 완료: {dest} ({len(resp.content)} bytes)")
        return True

    # ========== 생성 버튼 활성화 확인 / 클릭 / 결과 대기 ==========

    def is_generate_btn_enabled(self) -> bool:
        try:
            btn = self.wait.until(EC.presence_of_element_located(self.GENERATE_BTN))
            return btn.is_enabled()
        except Exception:
            return False



