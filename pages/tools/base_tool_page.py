# pages/tools/base_tool_page.py
# AI Helpy Chat 도구 페이지들이 공통으로 상속받는 클래스
# 두 테스트(세부 특기사항 / 행동특성 및 종합의견)에서 중복되는 흐름을 한 곳에 정의

import glob
import os
import time

from selenium.webdriver.common.action_chains import ActionChains
from config.selenium_imports import By, EC, WebDriverWait, TimeoutException

from pages.base_page import BasePage
from config.settings import BASE_URL, LOGIN_URL, TEST_USER, DEFAULT_WAIT, SHORT_WAIT
from config.login_helpers import close_token_banner


class BaseToolPage(BasePage):

    BASE_URL       = BASE_URL
    TOOLS_URL      = "https://qaproject.elice.io/ai-helpy-chat/tools"
    LOGIN_URL      = LOGIN_URL
    LOGIN_EMAIL    = TEST_USER["id"]
    LOGIN_PASSWORD = TEST_USER["pw"]

    # ========== Locators ==========

    EMAIL_INPUT    = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BUTTON  = (By.CSS_SELECTOR, "button[type='submit']")

    RESET_BUTTON   = (By.XPATH, "//button[contains(text(),'입력 내역 초기화') or contains(text(),'Reset')]")
    CONFIRM_RESET  = (By.XPATH, "//*[@role='dialog']//button[contains(text(),'초기화 하기') or contains(text(),'Reset')]")

    CLASS_INFO_TAB = (By.XPATH, "//button[@role='tab' and (contains(text(),'수업 정보 입력') or contains(text(),'Class Info'))]")

    SCHOOL_COMBOBOX = (
        By.XPATH,
        "//input[@name='school_level']/preceding-sibling::div[@role='combobox']",
    )

    NEXT_BUTTON    = (By.CSS_SELECTOR, "button[form='student_evaluation'], button[form='student_record_generation']")
    MODIFY_BUTTON  = (By.XPATH, "//*[@role='dialog']//button[contains(text(),'수정하기') or contains(text(),'Modify') or contains(text(),'Edit')]")

    STUDENT_TAB    = (By.XPATH, "//*[contains(text(),'학생 정보 입력 및 생성') or contains(text(),'Student Info')]")

    STUDENT_NAME_PLACEHOLDER = (
        By.XPATH,
        "//p[@role='button' and (text()='이름을 입력해주세요.' or text()='Enter name' or text()='Please enter a name')]",
    )
    ADD_STUDENT_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'MuiButton-outlined') and (contains(text(),'학생 추가') or contains(text(),'Add Student'))]",
    )
    FOOTER_NAME_PLACEHOLDER = (
        By.XPATH,
        "//tr[contains(@class,'MuiTableRow-footer')]//p[@role='button' and "
        "(text()='이름을 입력해주세요.' or text()='Enter name' or text()='Please enter a name')]",
    )
    FOOTER_NAME_INPUT = (
        By.XPATH,
        "//tr[contains(@class,'MuiTableRow-footer')]//textarea[not(@aria-hidden='true')]",
    )

    KEYWORD_BUTTON = (
        By.XPATH,
        "//tr[contains(@class,'MuiTableRow-footer')]//button[contains(@class,'css-mowt55')]",
    )
    KEYWORD_SAVE   = (By.XPATH, "//*[@role='dialog']//button[text()='저장' or text()='Save']")

    SEARCH_INPUT   = (By.XPATH, "//input[contains(@placeholder,'학생 이름 검색') or contains(@placeholder,'Search student') or contains(@placeholder,'검색')]")
    RESULT_BUTTON  = (By.XPATH, "//button[contains(text(),'생성 결과 받기') or contains(text(),'Get Result') or contains(text(),'Download Result')]")

    # '생성 결과 받기' 클릭 후 확인 모달의 '다운받기' 버튼
    DOWNLOAD_CONFIRM_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'MuiDialogActions-root')]//button"
        "[contains(normalize-space(text()),'다운') or contains(normalize-space(text()),'Download')"
        " or contains(normalize-space(text()),'받기') or contains(normalize-space(text()),'확인')]",
    )

    # LNB 햄버거 메뉴 / 도구 탭
    LNB_MENU_BTN   = (By.XPATH, "//button[.//*[@data-testid='barsIcon']]")
    LNB_TOOLS_BTN  = (By.XPATH, "//span[text()='도구']")

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
    
    STOP_BTN       = (By.XPATH, "//button[.//*[@data-testid='stopIcon']]")  # 생성 중단 버튼
    SPINNER        = (By.CSS_SELECTOR, "span[role='progressbar']")          # 로딩 스피너
    CHECK_ICON     = (By.CSS_SELECTOR, "[data-testid='circle-checkIcon']")  # 생성 완료 체크 아이콘
    GENERATE_BTN   = None  # 서브클래스에서 반드시 정의

    # ========== 초기화 ==========

    def __init__(self, driver, wait_or_timeout=10):
        super().__init__(driver, wait_or_timeout)

    # ========== 로그인 ==========

    def login(self):
        self.driver.get(self.LOGIN_URL)
        self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(self.LOGIN_EMAIL)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(self.LOGIN_PASSWORD)
        submit = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit.click()
        self.wait.until(EC.staleness_of(submit))
        # 리다이렉트가 qaproject로 완전히 완료될 때까지 추가 대기
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("qaproject.elice.io")
        )
        # LNB 링크가 렌더링될 때까지 대기 — 세션 쿠키 완전히 설정된 후에만 나타남
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href,'ai-helpy-chat')]")
            )
        )
        self.logger.info("로그인 성공")
        close_token_banner(self.driver, self.wait)  # BaseToolPage 자체 login() 전용

    # ========== LNB 탭 이동 ==========

    def click_lnb_tools_tab(self):
        """LNB의 '도구' 탭 클릭으로 도구 목록 페이지 이동"""
        link = self.wait.until(EC.element_to_be_clickable(self.LNB_TOOLS_LINK))
        self.js_click(link)
        self.wait.until(EC.url_contains("ai-helpy-chat/tools"))
        self.logger.info("LNB '도구' 탭 클릭 완료")

    # ========== 도구 선택 ==========

    def navigate_to_tools(self):
        self.go(self.TOOLS_URL)
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
        self.logger.info(f"'{tool_name}' 클릭 완료")
        close_token_banner(self.driver, self.wait)

    # ========== 입력 내역 초기화 ==========

    def reset_inputs(self):
        reset_btn = self.wait.until(EC.presence_of_element_located(self.RESET_BUTTON))
        if reset_btn.is_enabled():
            self.js_click(reset_btn)
            self.logger.info("입력 내역 초기화 버튼 클릭 완료")
            confirm_btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_RESET))
            self.js_click(confirm_btn)
            self.logger.info("초기화 하기 버튼 클릭 완료")
            self.wait_dialog_gone()
            self.logger.info("초기화 모달 닫힘 확인")
        else:
            self.logger.info("입력 내역 초기화 버튼 비활성화 → 초기화 건너뜀")

    # ========== 수업 정보 입력 탭 ==========

    def click_class_info_tab(self):
        tab_btn = self.wait.until(EC.element_to_be_clickable(self.CLASS_INFO_TAB))
        self.js_click(tab_btn)
        self.logger.info("수업 정보 입력 탭 클릭 완료")
        self.wait.until(EC.presence_of_element_located(self.SCHOOL_COMBOBOX))

    def select_school_level(self, school_level: str):
        self.wait.until(EC.element_to_be_clickable(self.SCHOOL_COMBOBOX)).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//li[@role='option' and @data-value='{school_level}']")
            )
        ).click()
        self.wait_backdrop_gone()
        self.logger.info(f"학교급 '{school_level}' 선택 완료")

    def click_next(self):
        next_btn = self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON))
        self.js_click(next_btn)
        self.logger.info("다음으로 버튼 클릭 완료")

    def handle_modify_modal(self):
        """'수정하기' 모달이 뜰 경우에만 처리 (없으면 조용히 넘어감)"""
        try:
            modify_btn = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable(self.MODIFY_BUTTON)
            )
            self.js_click(modify_btn)
            self.wait_dialog_gone()
            self.logger.info("수정하기 모달 처리 완료")
        except Exception:
            self.logger.info("수정 확인 모달 없음 → 바로 진행")

    # ========== 학생 정보 입력 ==========

    def ensure_student_row_exists(self):
        """이름 입력 행이 없으면 '+ 학생 추가' 버튼 클릭"""
        self.wait.until(EC.presence_of_element_located(self.ADD_STUDENT_BUTTON))
        if not self.driver.find_elements(*self.STUDENT_NAME_PLACEHOLDER):
            self.js_click(
                self.wait.until(EC.element_to_be_clickable(self.ADD_STUDENT_BUTTON))
            )
            self.wait.until(EC.visibility_of_element_located(self.STUDENT_NAME_PLACEHOLDER))
            self.logger.info("+ 학생 추가 버튼 클릭 완료")
        else:
            self.logger.info("이름 입력 필드 이미 존재")

    def enter_student_name(self, name: str):
        self.js_click(
            self.wait.until(EC.presence_of_element_located(self.FOOTER_NAME_PLACEHOLDER))
        )
        self.logger.info("이름 필드 클릭 완료")
        name_input = self.wait.until(EC.visibility_of_element_located(self.FOOTER_NAME_INPUT))
        name_input.clear()
        name_input.send_keys(name)
        self.logger.info(f"학생 이름 '{name}' 입력 완료")
        time.sleep(0.3)  # React 키 입력 상태 반영 최소 대기

    def open_keyword_modal(self):
        self.js_click(
            self.wait.until(EC.presence_of_element_located(self.KEYWORD_BUTTON))
        )
        self.logger.info("키워드 모달 열기 완료")

    def save_keyword_modal(self):
        self.js_click(
            self.wait.until(EC.presence_of_element_located(self.KEYWORD_SAVE))
        )
        self.wait_dialog_gone()
        self.logger.info("키워드 저장 완료")

    def enter_request_text(self, request_text: str):
        """요청사항이 있을 경우에만 입력 및 저장"""
        if not request_text:
            self.logger.info("요청사항 없음 → 입력 건너뜀")
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
        self.logger.info(f"추가 요청사항 입력 완료: {request_text}")

        try:
            save_btns = self.driver.find_elements(By.XPATH, save_xpath)
            if save_btns and save_btns[0].is_enabled():
                self.js_click(save_btns[0])
                self.logger.info("요청사항 저장 버튼 클릭 완료")
            else:
                self.logger.info("요청사항 저장 버튼 비활성화 → 건너뜀")
        except Exception:
            self.logger.info("요청사항 저장 버튼 확인 중 오류 → 건너뜀")

    # ========== 상태 확인 (assertion helpers) ==========

    def is_tools_list_displayed(self) -> bool:
        """도구 목록 페이지에 도구 카드가 표시되는지 확인"""
        try:
            cards = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[contains(@href,'ai-helpy-chat/tools/')]")
                )
            )
            self.logger.info(f"도구 목록 표시 확인 ({len(cards)}개)")
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

    def wait_for_result_button_enabled(self, timeout: int = 10) -> bool:
        """'생성 결과 받기' 버튼이 활성화될 때까지 대기 (AI 생성 완료 확인)
        TC 기준 '1분 이내 생성' 검증용"""
        deadline = time.time() + timeout
        self.wait.until(EC.presence_of_element_located(self.RESULT_BUTTON))
        self.logger.info(f"AI 생성 결과 버튼 활성화 대기 중 (최대 {timeout}초)...")
        while time.time() < deadline:
            time.sleep(2)
            try:
                if self.driver.find_element(*self.RESULT_BUTTON).is_enabled():
                    self.logger.info("AI 생성 완료 — 생성 결과 받기 버튼 활성화 확인")
                    return True
            except Exception:
                pass
        self.logger.warning(f"AI 생성 타임아웃 ({timeout}초 초과)")
        return False

    def get_student_row_count(self) -> int:
        """현재 학생 데이터 행 수 반환"""
        rows = self.driver.find_elements(*self.STUDENT_DATA_ROWS)
        self.logger.info(f"현재 학생 행 수: {len(rows)}")
        return len(rows)

    # ========== 생성 트리거 및 결과 다운로드 ==========

    def trigger_generation(self):
        """'+ 학생 추가' 버튼 재클릭으로 AI 생성 트리거"""
        self.js_click(
            self.wait.until(EC.element_to_be_clickable(self.ADD_STUDENT_BUTTON))
        )
        self.logger.info("학생 추가 버튼 클릭 완료 (생성 트리거)")

    def search_student(self, name: str):
        search_input = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(name)
        self.logger.info(f"학생 이름 검색 입력 완료: {name}")

    def download_result(self, download_dir: str, browser: str = "firefox"):
        """생성 결과 받기 버튼 클릭 후 xlsx 다운로드 완료 대기"""
        self.logger.info("생성 결과 받기 버튼 활성화 대기 중 (최대 120초)...")
        try:
            result_btn = WebDriverWait(self.driver, 120).until(
                EC.element_to_be_clickable(self.RESULT_BUTTON)
            )
        except Exception:
            self.logger.warning("생성 결과 받기 버튼 활성화 타임아웃 (120초 초과)")
            return False

        # 클릭 전 xlsx 파일별 수정 시간 스냅샷 (신규 파일 + 덮어쓰기 모두 감지)
        before_mtime = {}
        for f in glob.glob(os.path.join(download_dir, "*.xlsx")):
            try:
                before_mtime[f] = os.path.getmtime(f)
            except OSError:
                pass

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", result_btn)
        ActionChains(self.driver).move_to_element(result_btn).click().perform()
        self.logger.info("생성 결과 받기 버튼 클릭 완료")
        click_time = time.time()

        # 확인 모달 → '다운받기' 버튼 클릭 (모달 없을 경우 3초 후 바로 다운로드 진행)
        try:
            confirm_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.DOWNLOAD_CONFIRM_BUTTON)
            )
            ActionChains(self.driver).move_to_element(confirm_btn).click().perform()
            self.logger.info("'다운받기' 확인 버튼 클릭 완료")
        except Exception:
            self.logger.info("확인 모달 없음 → 바로 다운로드 진행")

        # 다운로드 완료 대기 (최대 90초)
        # 신규 파일 OR 기존 파일 덮어쓰기(mtime 변경) 모두 감지
        self.logger.info("파일 다운로드 대기 중...")
        deadline = time.time() + 90
        while time.time() < deadline:
            time.sleep(1)
            for f in glob.glob(os.path.join(download_dir, "*.xlsx")):
                if os.path.exists(f + ".part"):
                    continue
                try:
                    mtime = os.path.getmtime(f)
                except OSError:
                    continue
                if f not in before_mtime or mtime > click_time:
                    self.logger.info(f"다운로드 완료: {f}")
                    return True
        self.logger.warning("다운로드 타임아웃 (90초 초과)")
        return False

    # ========== AI 생성 공통 메서드 (DeepPage / QuizPage 등 생성형 도구 공용) ==========

    def tools_LNB(self):
        """LNB 햄버거 메뉴 → 도구 탭 클릭"""
        menu = self.wait.until(EC.element_to_be_clickable(self.LNB_MENU_BTN))
        self.js_click(menu)
        tools_bt = self.wait.until(EC.element_to_be_clickable(self.LNB_TOOLS_BTN))
        self.js_click(tools_bt)

    def setup_tool(self):
        """도구 메뉴 진입 후 생성 중이면 중단 (서브클래스의 tools_menu() 사용)"""
        self.tools_menu()
        self.stop_if_generating()

    def stop_if_generating(self):
        """
        AI 생성 중단

        단계:
          1. stopIcon 버튼 존재 시 클릭 → 생성 중단
          2. GENERATE_BTN 클릭 가능까지 대기 (disabled 해제 확인)

        Note:
          생성 중이 아닌 경우 TimeoutException 무시
        """
        try:
            stop_btn = WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.presence_of_element_located(self.STOP_BTN)
            )
            self.js_click(stop_btn)
            if self.GENERATE_BTN is not None:
                WebDriverWait(self.driver, DEFAULT_WAIT).until(
                    EC.element_to_be_clickable(self.GENERATE_BTN)
                )
        except TimeoutException:
            pass

    def get_generate_btn(self):
        """생성 버튼 요소 반환 (활성화 여부 확인용)"""
        if self.GENERATE_BTN is None:
            raise NotImplementedError(f"{self.__class__.__name__}에 GENERATE_BTN이 정의되지 않았습니다")
        return self.wait.until(EC.presence_of_element_located(self.GENERATE_BTN))

    def assert_generate_btn_enabled(self):
        """생성 버튼 활성화 검증"""
        btn = self.get_generate_btn()
        assert btn.is_enabled(), "모두 입력했는데 버튼이 비활성화 상태입니다"

    def assert_generate_btn_disabled(self):
        """생성 버튼 비활성화 검증"""
        btn = self.get_generate_btn()
        assert not btn.is_enabled(), "버튼이 활성화 상태입니다 (비활성화 예상)"

    def click_generate(self):
        """
        생성 버튼 클릭

        단계:
          1. 생성 버튼 확인
          2. 비활성화 상태이면 활성화까지 대기
          3. 버튼 텍스트 확인
          4. 버튼 클릭
          5. '다시 생성' 버튼인 경우 확인 팝업에서 '다시 생성' 클릭
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
        """로딩 스피너 표시 여부 → AI 생성 시작 확인"""
        try:
            spinner = self.wait_for_visible(self.SPINNER)
            return spinner.is_displayed()
        except TimeoutException:
            return False

    def is_generated(self, timeout=DEFAULT_WAIT):
        """
        AI 생성 완료 확인 (최초 생성 및 재생성 모두 대응)

        단계:
          1. 기존 체크 아이콘이 있으면 사라질 때까지 대기 (재생성 케이스)
          2. 로딩 스피너 사라짐 대기
          3. 완료 체크 아이콘 표시 대기
        """
        try:
            WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.visibility_of_element_located(self.CHECK_ICON)
            )
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.CHECK_ICON)
            )
        except TimeoutException:
            pass
        self.wait_until_invisible(self.SPINNER, timeout)
        result = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.CHECK_ICON)
        )
        return result.is_displayed()
