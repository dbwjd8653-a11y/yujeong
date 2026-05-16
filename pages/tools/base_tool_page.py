# pages/tools/base_tool_page.py
# AI Helpy Chat 도구 페이지들이 공통으로 상속받는 클래스
# 두 테스트(세부 특기사항 / 행동특성 및 종합의견)에서 중복되는 흐름을 한 곳에 정의

import glob
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class BaseToolPage(BasePage):

    BASE_URL   = "https://qaproject.elice.io/ai-helpy-chat"
    TOOLS_URL  = "https://qaproject.elice.io/ai-helpy-chat/tools"
    LOGIN_EMAIL    = "qa5team3-02@elicer.com"
    LOGIN_PASSWORD = "Mdk@02169630"

    # ========== Locators ==========

    EMAIL_INPUT    = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BUTTON  = (By.CSS_SELECTOR, "button[type='submit']")

    RESET_BUTTON   = (By.XPATH, "//button[contains(text(),'입력 내역 초기화')]")
    CONFIRM_RESET  = (By.XPATH, "//*[@role='dialog']//button[contains(text(),'초기화 하기')]")

    CLASS_INFO_TAB = (By.XPATH, "//button[@role='tab' and contains(text(),'수업 정보 입력')]")

    SCHOOL_COMBOBOX = (
        By.XPATH,
        "//label[contains(text(),'학교급')]/following-sibling::div//div[@role='combobox']",
    )

    NEXT_BUTTON    = (By.XPATH, "//button[not(@disabled) and text()='다음으로']")
    MODIFY_BUTTON  = (By.XPATH, "//*[@role='dialog']//button[contains(text(),'수정하기')]")

    STUDENT_TAB    = (By.XPATH, "//*[contains(text(),'학생 정보 입력 및 생성')]")

    STUDENT_NAME_PLACEHOLDER = (
        By.XPATH,
        "//p[@role='button' and text()='이름을 입력해주세요.']",
    )
    ADD_STUDENT_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'MuiButton-outlined') and contains(text(),'학생 추가')]",
    )
    FOOTER_NAME_PLACEHOLDER = (
        By.XPATH,
        "//tr[contains(@class,'MuiTableRow-footer')]//p[@role='button' and text()='이름을 입력해주세요.']",
    )
    FOOTER_NAME_INPUT = (
        By.XPATH,
        "//tr[contains(@class,'MuiTableRow-footer')]//textarea[not(@aria-hidden='true') and @placeholder='이름을 입력해주세요.']",
    )

    KEYWORD_BUTTON = (
        By.XPATH,
        "//tr[contains(@class,'MuiTableRow-footer')]//button[contains(@class,'css-mowt55')]",
    )
    KEYWORD_SAVE   = (By.XPATH, "//*[@role='dialog']//button[text()='저장']")

    SEARCH_INPUT   = (By.XPATH, "//input[@placeholder='학생 이름 검색']")
    RESULT_BUTTON  = (By.XPATH, "//button[contains(text(),'생성 결과 받기')]")

    # '생성 결과 받기' 클릭 후 확인 모달의 '다운받기' 버튼
    DOWNLOAD_CONFIRM_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'MuiDialogActions-root')]//button[normalize-space(text())='다운받기']",
    )

    # LNB '도구' 탭 링크
    LNB_TOOLS_LINK = (
        By.XPATH,
        "//a[contains(@href,'ai-helpy-chat/tools') and not(contains(@href,'ai-helpy-chat/tools/'))]",
    )

    # 학생 데이터 행 (헤더·푸터 제외)
    STUDENT_DATA_ROWS = (
        By.XPATH,
        "//tr[contains(@class,'MuiTableRow-root')"
        " and not(contains(@class,'MuiTableRow-head'))"
        " and not(contains(@class,'MuiTableRow-footer'))]",
    )

    # ========== 초기화 ==========

    def __init__(self, driver):
        super().__init__(driver)

    # ========== 로그인 ==========

    def login(self):
        self.driver.get(self.BASE_URL)
        self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(self.LOGIN_EMAIL)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(self.LOGIN_PASSWORD)
        submit = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit.click()
        self.wait.until(EC.staleness_of(submit))  # 로그인 후 DOM 변경 확인
        print("로그인 성공")

    # ========== LNB 탭 이동 ==========

    def click_lnb_tools_tab(self):
        """LNB의 '도구' 탭 클릭으로 도구 목록 페이지 이동"""
        link = self.wait.until(EC.element_to_be_clickable(self.LNB_TOOLS_LINK))
        self.js_click(link)
        self.wait.until(EC.url_contains("ai-helpy-chat/tools"))
        print("LNB '도구' 탭 클릭 완료")

    # ========== 도구 선택 ==========

    def navigate_to_tools(self):
        self.driver.get(self.TOOLS_URL)
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href,'ai-helpy-chat/tools/')]")
            )
        )

    def click_tool_menu(self, tool_name: str):
        """도구 목록에서 tool_name 텍스트를 가진 메뉴 클릭"""
        tool_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[.//p[text()='{tool_name}']]")
            )
        )
        self.js_click(tool_btn)
        self.wait.until(EC.url_contains("ai-helpy-chat/tools/"))
        print(f"'{tool_name}' 클릭 완료")

    # ========== 입력 내역 초기화 ==========

    def reset_inputs(self):
        reset_btn = self.wait.until(EC.presence_of_element_located(self.RESET_BUTTON))
        if reset_btn.is_enabled():
            self.js_click(reset_btn)
            print("입력 내역 초기화 버튼 클릭 완료")
            confirm_btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_RESET))
            self.js_click(confirm_btn)
            print("초기화 하기 버튼 클릭 완료")
            self.wait_dialog_gone()
            print("초기화 모달 닫힘 확인")
        else:
            print("입력 내역 초기화 버튼 비활성화 → 초기화 건너뜀")

    # ========== 수업 정보 입력 탭 ==========

    def click_class_info_tab(self):
        tab_btn = self.wait.until(EC.element_to_be_clickable(self.CLASS_INFO_TAB))
        self.js_click(tab_btn)
        print("수업 정보 입력 탭 클릭 완료")
        self.wait.until(EC.presence_of_element_located(self.SCHOOL_COMBOBOX))

    def select_school_level(self, school_level: str):
        self.wait.until(EC.element_to_be_clickable(self.SCHOOL_COMBOBOX)).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//li[@role='option' and normalize-space(text())='{school_level}']")
            )
        ).click()
        self.wait_backdrop_gone()
        print(f"학교급 '{school_level}' 선택 완료")

    def click_next(self):
        next_btn = self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON))
        self.js_click(next_btn)
        print("다음으로 버튼 클릭 완료")

    def handle_modify_modal(self):
        """'수정하기' 모달이 뜰 경우에만 처리 (없으면 조용히 넘어감)"""
        try:
            modify_btn = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable(self.MODIFY_BUTTON)
            )
            self.js_click(modify_btn)
            self.wait_dialog_gone()
            print("수정하기 모달 처리 완료")
        except Exception:
            print("수정 확인 모달 없음 → 바로 진행")

    # ========== 학생 정보 입력 ==========

    def ensure_student_row_exists(self):
        """이름 입력 행이 없으면 '+ 학생 추가' 버튼 클릭"""
        self.wait.until(EC.presence_of_element_located(self.ADD_STUDENT_BUTTON))
        if not self.driver.find_elements(*self.STUDENT_NAME_PLACEHOLDER):
            self.js_click(
                self.wait.until(EC.element_to_be_clickable(self.ADD_STUDENT_BUTTON))
            )
            self.wait.until(EC.visibility_of_element_located(self.STUDENT_NAME_PLACEHOLDER))
            print("+ 학생 추가 버튼 클릭 완료")
        else:
            print("이름 입력 필드 이미 존재")

    def enter_student_name(self, name: str):
        self.js_click(
            self.wait.until(EC.presence_of_element_located(self.FOOTER_NAME_PLACEHOLDER))
        )
        print("이름 필드 클릭 완료")
        name_input = self.wait.until(EC.visibility_of_element_located(self.FOOTER_NAME_INPUT))
        name_input.clear()
        name_input.send_keys(name)
        print(f"학생 이름 '{name}' 입력 완료")
        time.sleep(0.3)  # React 키 입력 상태 반영 최소 대기

    def open_keyword_modal(self):
        self.js_click(
            self.wait.until(EC.presence_of_element_located(self.KEYWORD_BUTTON))
        )
        print("키워드 모달 열기 완료")

    def save_keyword_modal(self):
        self.js_click(
            self.wait.until(EC.presence_of_element_located(self.KEYWORD_SAVE))
        )
        self.wait_dialog_gone()
        print("키워드 저장 완료")

    def enter_request_text(self, request_text: str):
        """요청사항이 있을 경우에만 입력 및 저장"""
        if not request_text:
            print("요청사항 없음 → 입력 건너뜀")
            return

        request_placeholder_xpath = (
            "(//tr[not(contains(@class,'MuiTableRow-head'))])[last()]"
            "//p[@role='button' and text()='요청사항을 입력해주세요.']"
        )
        request_input_xpath = (
            "(//tr[not(contains(@class,'MuiTableRow-head'))])[last()]"
            "//textarea[not(@aria-hidden='true') and @placeholder='요청사항을 입력해주세요.']"
        )
        save_xpath = (
            "(//tr[not(contains(@class,'MuiTableRow-head'))])[last()]"
            "//button[text()='저장']"
        )

        self.js_click(
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, request_placeholder_xpath))
            )
        )
        request_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, request_input_xpath))
        )
        self.js_input(request_input, request_text)
        print(f"추가 요청사항 입력 완료: {request_text}")

        try:
            save_btns = self.driver.find_elements(By.XPATH, save_xpath)
            if save_btns and save_btns[0].is_enabled():
                self.js_click(save_btns[0])
                print("요청사항 저장 버튼 클릭 완료")
            else:
                print("요청사항 저장 버튼 비활성화 → 건너뜀")
        except Exception:
            print("요청사항 저장 버튼 확인 중 오류 → 건너뜀")

    # ========== 상태 확인 (assertion helpers) ==========

    def is_tools_list_displayed(self) -> bool:
        """도구 목록 페이지에 도구 카드가 표시되는지 확인"""
        try:
            cards = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[contains(@href,'ai-helpy-chat/tools/')]")
                )
            )
            print(f"도구 목록 표시 확인 ({len(cards)}개)")
            return len(cards) > 0
        except Exception:
            return False

    def is_on_tool_page(self) -> bool:
        """현재 URL이 특정 도구 상세 페이지인지 확인"""
        try:
            self.wait.until(EC.url_contains("ai-helpy-chat/tools/"))
            return True
        except Exception:
            return False

    def is_class_info_tab_visible(self) -> bool:
        """수업 정보 입력 탭이 화면에 표시되는지 확인"""
        try:
            self.wait.until(EC.presence_of_element_located(self.CLASS_INFO_TAB))
            return True
        except Exception:
            return False

    def is_school_level_combobox_visible(self) -> bool:
        """학교급 콤보박스가 화면에 표시되는지 확인"""
        try:
            self.wait.until(EC.presence_of_element_located(self.SCHOOL_COMBOBOX))
            return True
        except Exception:
            return False

    def is_next_button_enabled(self) -> bool:
        """'다음으로' 버튼이 활성화 상태인지 확인"""
        try:
            btn = self.wait.until(EC.presence_of_element_located(self.NEXT_BUTTON))
            return btn.is_enabled()
        except Exception:
            return False

    def is_student_tab_visible(self) -> bool:
        """학생 정보 입력 탭이 화면에 표시되는지 확인"""
        try:
            self.wait.until(EC.presence_of_element_located(self.STUDENT_TAB))
            return True
        except Exception:
            return False

    def is_student_name_entered(self, name: str) -> bool:
        """입력한 학생 이름이 footer 행에 반영되었는지 확인"""
        try:
            input_el = self.driver.find_element(*self.FOOTER_NAME_INPUT)
            value = input_el.get_attribute("value") or ""
            return name in value
        except Exception:
            return False

    def is_result_button_visible(self) -> bool:
        """'생성 결과 받기' 버튼이 화면에 표시되는지 확인"""
        try:
            self.wait.until(EC.presence_of_element_located(self.RESULT_BUTTON))
            return True
        except Exception:
            return False

    def is_class_info_reflected(self, school_level: str, grade: str, subject: str, unit: str) -> bool:
        """학생 정보 페이지 상단에 수업 정보가 모두 반영됐는지 확인"""
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            return all(v in body_text for v in [school_level, grade, subject, unit])
        except Exception:
            return False

    def wait_for_result_button_enabled(self, timeout: int = 60) -> bool:
        """'생성 결과 받기' 버튼이 활성화될 때까지 대기 (AI 생성 완료 확인)
        TC 기준 '1분 이내 생성' 검증용"""
        deadline = time.time() + timeout
        self.wait.until(EC.presence_of_element_located(self.RESULT_BUTTON))
        while time.time() < deadline:
            time.sleep(2)
            try:
                if self.driver.find_element(*self.RESULT_BUTTON).is_enabled():
                    print("AI 생성 완료 — 생성 결과 받기 버튼 활성화 확인")
                    return True
            except Exception:
                pass
            print(".", end="", flush=True)
        print(f"\nAI 생성 타임아웃 ({timeout}초 초과)")
        return False

    def get_student_row_count(self) -> int:
        """현재 학생 데이터 행 수 반환"""
        rows = self.driver.find_elements(*self.STUDENT_DATA_ROWS)
        print(f"현재 학생 행 수: {len(rows)}")
        return len(rows)

    # ========== 생성 트리거 및 결과 다운로드 ==========

    def trigger_generation(self):
        """'+ 학생 추가' 버튼 재클릭으로 AI 생성 트리거"""
        self.js_click(
            self.wait.until(EC.element_to_be_clickable(self.ADD_STUDENT_BUTTON))
        )
        print("학생 추가 버튼 클릭 완료 (생성 트리거)")

    def search_student(self, name: str):
        search_input = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        search_input.send_keys(name)
        print(f"학생 이름 검색 입력 완료: {name}")

    def download_result(self, download_dir: str, browser: str = "firefox"):
        """생성 결과 받기 버튼 클릭 후 xlsx 다운로드 완료 대기"""
        print(f"생성 결과 받기 버튼 활성화 대기 중 (최대 120초)...")
        self.wait.until(EC.presence_of_element_located(self.RESULT_BUTTON))
        deadline_btn = time.time() + 120
        result_btn = None
        while time.time() < deadline_btn:
            time.sleep(1)
            btn = self.driver.find_element(*self.RESULT_BUTTON)
            if btn.is_enabled():
                result_btn = btn
                print("생성 결과 받기 버튼 활성화 확인")
                break
            print(".", end="", flush=True)
        else:
            print("\n생성 결과 받기 버튼 활성화 타임아웃 (120초 초과)")
            return False

        existing_xlsx = set(glob.glob(os.path.join(download_dir, "*.xlsx")))
        self.js_click(result_btn)
        print("생성 결과 받기 버튼 클릭 완료")

        # 확인 모달 → '다운받기' 버튼 클릭
        try:
            confirm_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.DOWNLOAD_CONFIRM_BUTTON)
            )
            self.js_click(confirm_btn)
            print("'다운받기' 확인 버튼 클릭 완료")
        except Exception:
            print("확인 모달 없음 → 바로 다운로드 진행")

        # 다운로드 완료 대기 (최대 90초)
        print("파일 다운로드 대기 중...")
        temp_ext = "*.part" if browser.lower() == "firefox" else "*.crdownload"
        deadline = time.time() + 90
        while time.time() < deadline:
            time.sleep(1)
            current_xlsx = set(glob.glob(os.path.join(download_dir, "*.xlsx")))
            new_files = current_xlsx - existing_xlsx
            temp_files = glob.glob(os.path.join(download_dir, temp_ext))
            if new_files and not temp_files:
                print(f"다운로드 완료: {list(new_files)[0]}")
                return True
        print("다운로드 타임아웃 (90초 초과)")
        return False
