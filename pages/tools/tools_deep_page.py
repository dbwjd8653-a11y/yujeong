"""
심층 조사 도구 페이지 동작 및 검증 클래스
BasePage를 상속받아 심층 조사 전용 동작을 구현합니다.
"""

from config.selenium_imports import By, EC, WebDriverWait,TimeoutException

from pages.base_page import BasePage
from config.settings import DEFAULT_WAIT, SHORT_WAIT
import pytest


class DeepPage(BasePage):

    # ── Locators ───────────────────────────────────────────────────
    LNB_MENU_BTN    = (By.XPATH, "//button[.//*[@data-testid='barsIcon']]")              # 햄버거 메뉴
    LNB_TOOLS_BTN   = (By.XPATH, "//span[text()='도구']")                                # 도구 메뉴
    MENU_ITEM       = (By.XPATH, "//p[text()='심층 조사']")                              # 심층 조사 메뉴 항목
    TITLE_ELEMENT   = (By.XPATH, "//span[text()='심층 조사']")                           # 페이지 타이틀
    TOPIC_INPUT     = (By.NAME, "topic")                                                  # 주제 입력 필드
    MESSAGE_INPUT   = (By.NAME, "instructions")                                           # 지시사항 입력 필드
    GENERATE_BTN    = (By.CSS_SELECTOR, "button[form='tool-factory-do_deep_research']")  # 자동 생성 버튼
    STOP_BTN        = (By.XPATH, "//button[.//*[@data-testid='stopIcon']]")              # 생성 중단 버튼
    SPINNER         = (By.CSS_SELECTOR, "span[role='progressbar']")                      # 로딩 스피너
    CHECK_ICON      = (By.CSS_SELECTOR, "[data-testid='circle-checkIcon']")              # 생성 완료 체크 아이콘
    TOKEN_BANNER    = (By.XPATH, "//p[contains(text(),'잔여 토큰이 부족하여')]")           # 토큰 부족 배너
    ERROR_ALERT     = (By.CSS_SELECTOR, "[data-testid='circle-exclamationIcon']")        # 오류 알림 아이콘
    ERROR_ALERT_MSG = (By.XPATH, "//div[contains(text(),'답변 생성에 문제가 발생했습니다')]")  # 오류 메시지 텍스트

    # ── 테스트 입력값 상수 ─────────────────────────────────────────
    TOPIC_TEXT        = "날씨"
    MESSAGE_TEXT      = "대한민국 서울의 2026년 5월의 날씨"
    TITLE_TEXT        = "심층 조사"
    TOPIC_500_CHARS   = "가" * 500   # 경계값: 500자 (버튼 활성화)
    TOPIC_501_CHARS   = "가" * 501   # 경계값: 501자 (버튼 비활성화)
    TOPIC_BLANK       = " "          # 공백 입력

    def __init__(self, login):
        driver, wait = login
        super().__init__(driver, wait)

    def tools_LNB(self):
        """
        [LNB 도구 메뉴 진입]

        [Test Steps]
        1. 햄버거 메뉴(barsIcon) 버튼을 클릭한다.
        2. '도구' 텍스트를 클릭하여 도구 목록 페이지로 이동한다.
        """
        menu = self.wait.until(EC.element_to_be_clickable(self.LNB_MENU_BTN))
        self.js_click(menu)
        tools_bt = self.wait.until(EC.element_to_be_clickable(self.LNB_TOOLS_BTN))
        self.js_click(tools_bt)

    def tools_menu(self):
        """
        [심층 조사 도구 선택]

        [Test Steps]
        1. 도구 목록에서 '심층 조사' 항목을 클릭한다.
        """
        target = self.wait.until(EC.element_to_be_clickable(self.MENU_ITEM))
        self.js_click(target)

    def setup_tool(self):
        """
        [심층 조사 도구 초기 세팅]

        [Test Steps]
        1. '심층 조사' 도구를 선택한다.
        2. AI 생성이 진행 중이면 정지시킨다.

        [Expected Result]
        테스트를 시작하기에 앞서 깨끗한 초기 상태를 보장한다.
        """
        self.tools_menu()
        self.stop_if_generating()

    def stop_if_generating(self):
        """
        [AI 생성 중단]

        [Test Steps]
        1. stopIcon 버튼이 존재하면 클릭하여 생성을 중단한다.
        2. 생성 버튼이 다시 나타날 때까지 대기한다.

        [Note]
        생성 중이 아닌 경우 TimeoutException을 무시하고 계속 진행합니다.
        """
        try:
            stop_btn = WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.presence_of_element_located(self.STOP_BTN)
            )
            self.js_click(stop_btn)
            WebDriverWait(self.driver, DEFAULT_WAIT).until(
            EC.element_to_be_clickable(self.TOPIC_INPUT)
        )
        except TimeoutException:
            pass

    def is_tool_page_displayed(self):
        """
        [심층 조사 페이지 타이틀 검증]

        [Expected Result]
        - 타이틀 요소가 화면에 보여야 한다.
        - 타이틀 텍스트가 '심층 조사'와 일치해야 한다.
        """
        title_element = self.wait_for_visible(self.TITLE_ELEMENT)
        assert title_element.is_displayed(), "심층 조사 타이틀이 화면에 보이지 않습니다."
        assert title_element.text == self.TITLE_TEXT, f"타이틀이 일치하지 않습니다. (현재: {title_element.text})"

    def is_token_exhausted(self):
        """
        [토큰 소진 여부 확인]

        [Expected Result]
        잔여 토큰이 부족하여 기능 이용이 제한되었을 때 나타나는 배너가 보이면 True를 반환한다.

        [Note]
        배너는 토큰이 추가되거나 소진될 때 모두 나타날 수 있습니다.
        배너 존재 자체가 토큰 소진을 의미하지는 않습니다.
        """
        try:
            banner = self.driver.find_element(*self.TOKEN_BANNER)
            return banner.is_displayed()
        except Exception:
            return False

    def get_generate_btn(self):
        """생성 버튼 요소를 반환한다. (클릭하지 않음 - 활성화 여부 확인용)"""
        return self.wait.until(EC.presence_of_element_located(self.GENERATE_BTN))

    def assert_generate_btn_enabled(self):
        """
        [생성 버튼 활성화 검증]

        [Expected Result]
        - 토큰이 소진된 경우: 버튼이 비활성화 상태임을 확인하고 xfail 처리한다.
        - 토큰이 정상인 경우: 버튼이 활성화 상태임을 확인한다.
        """
        btn = self.get_generate_btn()
        if self.is_token_exhausted():
            assert not btn.is_enabled(), "토큰 소진 상태인데 버튼이 활성화되어 있습니다"
            pytest.xfail("토큰 한도 소진 - 버튼 비활성화 확인 완료")
        else:
            assert btn.is_enabled(), "모두 입력했는데 버튼이 비활성화 상태입니다"

    def assert_generate_btn_disabled(self):
        """
        [생성 버튼 비활성화 검증]

        [Expected Result]
        생성 버튼이 비활성화 상태임을 확인한다.
        """
        btn = self.get_generate_btn()
        assert not btn.is_enabled(), "버튼이 활성화 상태입니다 (비활성화 예상)"

    def click_generate(self):
        """
        [생성 버튼 클릭]

        [Test Steps]
        1. 생성 버튼을 확인한다.
        2. 비활성화 상태이면 활성화될 때까지 대기한다.
        3. 버튼 텍스트를 확인한다.
        4. 버튼을 클릭한다.
        5. '다시 생성' 버튼인 경우 확인 팝업에서 '다시 생성'을 클릭한다.
        """
        btn = self.get_generate_btn()
        if not btn.is_enabled():
            btn = self.wait.until(EC.element_to_be_clickable(self.GENERATE_BTN))
        btn_text = btn.text
        self.js_click(btn)
        if btn_text == '다시 생성':
            popup_btn = WebDriverWait(self.driver, DEFAULT_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='dialog']//button[text()='다시 생성']"))
            )
            self.js_click(popup_btn)

    def is_generating(self):
        """
        [AI 생성 시작 확인]

        [Expected Result]
        로딩 스피너(progressbar)가 화면에 보이면 True를 반환한다.
        """
        try:
            spinner = self.wait_for_visible(self.SPINNER)
            return spinner.is_displayed()
        except TimeoutException:
            return False

    def is_generated(self, timeout=DEFAULT_WAIT):
        """
        [AI 생성 완료 확인]

        [Test Steps]
        1. 로딩 스피너(progressbar)가 사라질 때까지 대기한다.
        2. 완료 체크 아이콘(circle-checkIcon)이 나타날 때까지 대기한다.

        [Expected Result]
        스피너가 먼저 사라지고 체크 아이콘이 나타나야 True를 반환한다.
        이미 존재하던 체크 아이콘을 완료로 착각하는 것을 방지합니다.
        """
        self.wait_until_invisible(self.SPINNER, timeout)
        result = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.CHECK_ICON)
        )
        return result.is_displayed()

    def is_error_alert_displayed(self):
        """
        [오류 알림 확인]

        [Expected Result]
        - 오류 아이콘(circle-exclamationIcon)이 화면에 보여야 한다.
        - '답변 생성에 문제가 발생했습니다' 텍스트가 화면에 보여야 한다.
        """
        icon = self.wait_for_visible(self.ERROR_ALERT)
        msg  = self.wait_for_visible(self.ERROR_ALERT_MSG)
        return icon.is_displayed() and msg.is_displayed()
