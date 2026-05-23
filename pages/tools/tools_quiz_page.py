"""
퀴즈 생성 도구 페이지 동작 및 검증 클래스
BaseToolPage를 상속받아 퀴즈 생성 전용 동작을 구현합니다.
"""

from config.selenium_imports import By, EC

from pages.tools.base_tool_page import BaseToolPage


class QuizPage(BaseToolPage):

    # ── Locators ───────────────────────────────────────────────────
    MENU_ITEM      = (By.XPATH, "//p[text()='퀴즈 생성']")                                               # 퀴즈 생성 메뉴 항목
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
        target = self.wait.until(EC.element_to_be_clickable(self.MENU_ITEM))
        self.js_click(target)

    def select_option(self, dropdown_id, target_text):
        """
        드롭다운 특정 항목 선택

        단계:
          1. dropdown_id로 드롭다운 버튼 클릭
          2. 목록 전체 표시 대기
          3. target_text 일치 항목 클릭
          4. 목록 닫힘 대기
        """
        dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, dropdown_id)))
        dropdown.click()
        options = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul[role='listbox'] li"))
        )
        for option in options:
            if option.text == target_text:
                self.js_click(option)
                break
        self.wait_until_invisible((By.CSS_SELECTOR, "ul[role='listbox']"))

    def is_tool_page_displayed(self):
        """퀴즈 생성 페이지 타이틀 표시 여부 검증"""
        title_element = self.wait_for_visible(self.TITLE_ELEMENT)
        assert title_element.is_displayed(), "퀴즈 생성 타이틀이 화면에 보이지 않습니다."
        assert title_element.text == self.TITLE_TEXT, f"타이틀이 일치하지 않습니다. (현재: {title_element.text})"
