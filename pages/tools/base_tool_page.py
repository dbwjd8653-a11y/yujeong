# pages/tools/base_tool_page.py
# AI Helpy Chat 도구 페이지들이 공통으로 상속받는 클래스
# 수업지도안 / PPT 생성 공통 흐름 담당

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BaseToolPage:

    BASE_URL       = "https://qaproject.elice.io/ai-helpy-chat"
    TOOLS_URL      = "https://qaproject.elice.io/ai-helpy-chat/tools"
    LOGIN_EMAIL    = "qa5team3-03@elicer.com"
    LOGIN_PASSWORD = "asd123!!"

    # ========== Locators ==========

    EMAIL_INPUT    = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BUTTON  = (By.CSS_SELECTOR, "button[type='submit']")

    # 다시 생성 확인 팝업 (수업지도안 / PPT 공통)
    REGEN_CONFIRM_BTN = (By.XPATH, "//*[@role='dialog']//button[contains(., '다시 생성')]")

    # 개인 토큰 한도 팝업 닫기 버튼 (X 버튼)
    TOKEN_POPUP_CLOSE = (By.CSS_SELECTOR, "[data-testid='xmark-largeIcon']")

    # ========== 초기화 ==========

    def __init__(self, driver):
        self.driver = driver
        # 요소를 찾을 때 최대 10초 기다린다
        self.wait = WebDriverWait(driver, 10)

    # ========== 로그인 ==========

    def login(self):
        # 로그인 페이지 열기
        self.driver.get(self.BASE_URL)

        # 이메일, 비밀번호 입력
        self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(self.LOGIN_EMAIL)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(self.LOGIN_PASSWORD)

        # 로그인 버튼 클릭 후 버튼이 사라질 때까지 대기 (로그인 완료 기준)
        submit = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit.click()
        self.wait.until(EC.staleness_of(submit))
        print("로그인 성공")

    # ========== 공통 브라우저 동작 ==========

    def js_click(self, element):
        # 일반 click()이 안 될 때 JavaScript로 강제 클릭
        self.driver.execute_script("arguments[0].click();", element)

    def wait_backdrop_gone(self):
        # 콤보박스 선택 후 나타나는 반투명 배경이 사라질 때까지 기다린다
        try:
            self.wait.until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBackdrop-root"))
            )
        except Exception:
            pass

    # ========== 팝업 처리 ==========

    def dismiss_token_popup(self):
        # 개인 토큰 한도 팝업이 뜨면 X 버튼을 눌러 닫는다
        # 팝업이 없으면 그냥 넘어간다
        try:
            # X 버튼이 나타날 때까지 최대 3초 기다린 뒤 클릭
            close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.TOKEN_POPUP_CLOSE)
            )
            close_btn.click()

            # 팝업이 완전히 사라질 때까지 대기
            self.wait_dialog_gone()
            print("토큰 한도 팝업 닫기 완료")
        except Exception:
            pass

    def wait_dialog_gone(self):
        # 팝업(role='dialog')이 화면에서 사라질 때까지 최대 5초 기다린다
        try:
            WebDriverWait(self.driver, 5).until_not(
                EC.presence_of_element_located((By.XPATH, "//*[@role='dialog']"))
            )
        except Exception:
            pass

    # ========== 도구 선택 ==========

    def navigate_to_tools(self):
        # 도구 목록 페이지로 바로 이동
        self.driver.get(self.TOOLS_URL)
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href,'ai-helpy-chat/tools/')]")
            )
        )

    def click_tool_menu(self, tool_name):
        # tool_name 에 해당하는 도구 버튼을 찾아 클릭
        tool_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[.//p[text()='{tool_name}']]")
            )
        )
        self.js_click(tool_btn)

        # 도구 상세 페이지로 이동될 때까지 대기
        self.wait.until(EC.url_contains("ai-helpy-chat/tools/"))
        print(f"'{tool_name}' 클릭 완료")

        # 도구 진입 시 나타나는 토큰 한도 팝업 닫기
        self.dismiss_token_popup()

    # ========== 생성 버튼 공통 동작 (수업지도안 / PPT 공통) ==========

    def is_generate_btn_enabled(self):
        # 생성 버튼이 활성화 상태인지 확인 (True / False 반환)
        try:
            btn = self.wait.until(EC.presence_of_element_located(self.GENERATE_BTN))
            return btn.is_enabled()
        except Exception:
            return False

    def click_generate(self):
        # 생성 버튼으로 스크롤 이동 후 클릭
        btn = self.wait.until(EC.presence_of_element_located(self.GENERATE_BTN))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn
        )
        time.sleep(0.5)

        btn = self.wait.until(EC.element_to_be_clickable(self.GENERATE_BTN))
        self.js_click(btn)
        time.sleep(1)

        # 이전 결과가 있으면 "다시 생성" 확인 팝업이 뜬다 → 확인 버튼 클릭
        try:
            confirm = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.REGEN_CONFIRM_BTN)
            )
            self.js_click(confirm)
            self.wait_dialog_gone()
        except Exception:
            pass

    def wait_for_generation(self, timeout=60):
        # AI 생성이 완료되면 SUCCESS_MESSAGE 가 나타난다
        # timeout 초 안에 나타나면 True, 시간 초과면 False 반환
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                msg = self.driver.find_element(*self.SUCCESS_MESSAGE)
                if msg.is_displayed() and msg.text.strip():
                    return True
            except Exception:
                pass
            time.sleep(2)
        return False

    # ========== 상태 확인 ==========

    def is_on_tool_page(self):
        # 현재 URL이 도구 상세 페이지인지 확인 (True / False 반환)
        try:
            self.wait.until(EC.url_contains("ai-helpy-chat/tools/"))
            return True
        except Exception:
            return False
