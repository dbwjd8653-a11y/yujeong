"""
심층 조사 도구 페이지 동작 및 검증 클래스
BaseToolPage를 상속받아 심층 조사 전용 동작을 구현합니다.
"""

from config.selenium_imports import By, EC

from pages.tools.base_tool_page import BaseToolPage


class DeepPage(BaseToolPage):

    # ── Locators ───────────────────────────────────────────────────
    MENU_ITEM       = (By.XPATH, "//p[text()='심층 조사']")                                              # 심층 조사 메뉴 항목
    TITLE_ELEMENT   = (By.XPATH, "//span[text()='심층 조사']")                                           # 페이지 타이틀
    TOPIC_INPUT     = (By.NAME, "topic")                                                                   # 주제 입력 필드
    MESSAGE_INPUT   = (By.NAME, "instructions")                                                            # 지시사항 입력 필드
    GENERATE_BTN    = (By.CSS_SELECTOR, "button[form='tool-factory-do_deep_research']")                   # 자동 생성 버튼
    ERROR_ALERT     = (By.CSS_SELECTOR, "[data-testid='circle-exclamationIcon']")                         # 오류 알림 아이콘
    ERROR_ALERT_MSG = (By.XPATH, "//div[contains(text(),'답변 생성에 문제가 발생했습니다')]")                 # 오류 메시지 텍스트

    # ── 테스트 입력값 상수 ─────────────────────────────────────────
    TOPIC_TEXT      = "날씨"
    MESSAGE_TEXT    = "대한민국 서울의 2026년 5월의 날씨"
    TITLE_TEXT      = "심층 조사"
    TOPIC_500_CHARS = "가" * 500
    TOPIC_501_CHARS = "가" * 501
    TOPIC_BLANK     = " "

    def __init__(self, login):
        driver, wait = login
        super().__init__(driver, wait)

    def tools_menu(self):
        target = self.wait.until(EC.element_to_be_clickable(self.MENU_ITEM))
        self.js_click(target)

    def is_tool_page_displayed(self):
        """심층 조사 페이지 타이틀 표시 여부 검증"""
        title_element = self.wait_for_visible(self.TITLE_ELEMENT)
        assert title_element.is_displayed(), "심층 조사 타이틀이 화면에 보이지 않습니다."
        assert title_element.text == self.TITLE_TEXT, f"타이틀이 일치하지 않습니다. (현재: {title_element.text})"

    def is_error_alert_displayed(self):
        """
        오류 알림 표시 여부 확인

        결과:
          - 오류 아이콘 + 오류 메시지 텍스트 모두 표시 시 True 반환
        """
        icon = self.wait_for_visible(self.ERROR_ALERT)
        msg  = self.wait_for_visible(self.ERROR_ALERT_MSG)
        return icon.is_displayed() and msg.is_displayed()
