"""
퀴즈 생성 도구 페이지 동작 및 검증 클래스
BasePage를 상속받아 퀴즈 생성 전용 동작을 구현합니다.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage, DEFAULT_WAIT
import pytest

SHORT_WAIT = 5  # 생성 중단 버튼 확인용 짧은 대기


class Tool5Page(BasePage):

    # ── Locators ───────────────────────────────────────────────────
    LNB_MENU_BTN    = (By.XPATH, "//button[.//*[@data-testid='barsIcon']]")  # 햄버거 메뉴
    LNB_TOOLS_BTN   = (By.XPATH, "//span[text()='도구']")                    # 도구 메뉴
    MENU_ITEM       = (By.XPATH, "//p[text()='퀴즈 생성']")                  # 퀴즈 생성 메뉴 항목
    TITLE_ELEMENT   = (By.XPATH, "//span[text()='퀴즈 생성']")               # 페이지 타이틀
    OPTION_TYPE_DD  = "mui-component-select-quiz_configs.0.option_type"       # 문제 유형 드롭다운 ID
    DIFFICULTY_DD   = "mui-component-select-quiz_configs.0.difficulty"        # 난이도 드롭다운 ID
    CONTENT_INPUT   = (By.NAME, "content")                                    # 주제 입력 필드
    GENERATE_BTN    = (By.CSS_SELECTOR, "button[form='tool-factory-create_quiz_from_context']")  # 자동 생성 버튼
    STOP_BTN        = (By.XPATH, "//button[.//*[@data-testid='stopIcon']]")   # 생성 중단 버튼
    SPINNER         = (By.CSS_SELECTOR, "span[role='progressbar']")           # 로딩 스피너
    CHECK_ICON      = (By.CSS_SELECTOR, "[data-testid='circle-checkIcon']")   # 생성 완료 체크 아이콘
    TOKEN_BANNER    = (By.XPATH, "//p[contains(text(),'잔여 토큰이 부족하여')]") # 토큰 부족 배너

    # ── 테스트 입력값 상수 ─────────────────────────────────────────
    OPTION_TYPE_VALUE = "객관식 (단일 선택)"
    DIFFICULTY_VALUE  = "하"
    CONTENT_VALUE     = "퀴즈"
    TITLE_TEXT        = "퀴즈 생성"

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
        menu = self.wait.until(EC.presence_of_element_located(self.LNB_MENU_BTN))
        self.js_click(menu)
        tools_bt = self.wait.until(EC.presence_of_element_located(self.LNB_TOOLS_BTN))
        self.js_click(tools_bt)

    def tools_menu(self):
        """
        [퀴즈 생성 도구 선택]

        [Test Steps]
        1. 도구 목록에서 '퀴즈 생성' 항목을 클릭한다.
        """
        target = self.wait.until(EC.presence_of_element_located(self.MENU_ITEM))
        self.js_click(target)

    def setup_tool(self):
        """
        [퀴즈 생성 도구 초기 세팅]

        [Test Steps]
        1. '퀴즈 생성' 도구를 선택한다.
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
                EC.presence_of_element_located(self.GENERATE_BTN)
            )
        except TimeoutException:
            pass

    def select_option(self, dropdown_id, target_text):
        """
        [드롭다운 특정 항목 선택]

        [Test Steps]
        1. dropdown_id로 드롭다운 버튼을 찾아 클릭한다.
        2. 목록이 모두 보일 때까지 대기한다.
        3. target_text와 일치하는 항목을 찾아 클릭한다.
        4. 목록이 닫힐 때까지 대기한다.

        [Expected Result]
        target_text와 일치하는 항목이 선택된다.
        """
        dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, dropdown_id)))
        dropdown.click()
        options = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul[role='listbox'] li"))
        )
        for option in options:
            if option.text == target_text:
                print(f"선택된 항목: {option.text}")
                self.js_click(option)
                break
        self.wait_until_invisible((By.CSS_SELECTOR, "ul[role='listbox']"))

    def is_tool_page_displayed(self):
        """
        [퀴즈 생성 페이지 타이틀 검증]

        [Expected Result]
        - 타이틀 요소가 화면에 보여야 한다.
        - 타이틀 텍스트가 '퀴즈 생성'과 일치해야 한다.
        """
        title_element = self.wait_for_visible(self.TITLE_ELEMENT)
        assert title_element.is_displayed(), "퀴즈 생성 타이틀이 화면에 보이지 않습니다."
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
