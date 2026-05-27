"""
퀴즈 생성 도구 페이지 동작 및 검증 클래스
BaseToolPage를 상속받아 퀴즈 생성 전용 동작을 구현합니다.
"""

from config.selenium_imports import By, EC

from pages.tools.base_tool_page import BaseToolPage


class QuizPage(BaseToolPage):

    TOOL_NAME = "퀴즈 생성"

    # ── Locators ───────────────────────────────────────────────────
    TITLE_ELEMENT  = (By.XPATH, "//span[text()='퀴즈 생성']")                                            # 페이지 타이틀
    OPTION_TYPE_DD = "mui-component-select-quiz_configs.0.option_type"                                    # 문제 유형 드롭다운 ID
    DIFFICULTY_DD  = "mui-component-select-quiz_configs.0.difficulty"                                     # 난이도 드롭다운 ID
    CONTENT_INPUT  = (By.NAME, "content")                                                                  # 주제 입력 필드
    GENERATE_BTN   = (By.CSS_SELECTOR, "button[form='tool-factory-create_quiz_from_context']")            # 자동 생성 버튼

    # ── 테스트 입력값 상수 ─────────────────────────────────────────
    OPTION_TYPE_VALUE = "객관식 (단일 선택)"
    DIFFICULTY_VALUE  = "하"
    CONTENT_VALUE     = "퀴즈"
    TITLE_TEXT        = "퀴즈 생성"

    def __init__(self, login):
        driver, wait = login
        super().__init__(driver, wait)

    def tools_menu(self):
        self.click_tool_menu(self.TOOL_NAME)

    def select_option(self, dropdown_id, target_text):
        """드롭다운 특정 항목 선택"""
        self.wait.until(EC.element_to_be_clickable((By.ID, dropdown_id))).click()
        options = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul[role='listbox'] li"))
        )
        for option in options:
            if option.text == target_text:
                self.js_click(option)
                break
        self.wait_dropdown_closed()

    def is_tool_page_displayed(self):
        """퀴즈 생성 페이지 타이틀 표시 여부 검증"""
        title_element = self.wait_for_visible(self.TITLE_ELEMENT)
        assert title_element.is_displayed(), "퀴즈 생성 타이틀이 화면에 보이지 않습니다."
        assert title_element.text == self.TITLE_TEXT, f"타이틀이 일치하지 않습니다. (현재: {title_element.text})"
