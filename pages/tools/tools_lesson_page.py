import os

from config.selenium_imports import By, EC


from pages.tools.base_tool_page import BaseToolPage


class LessonPlanPage(BaseToolPage):

    TOOL_NAME = "수업지도안"

    # ========== Locators ==========

    SCHOOL_COMBOBOX = (
        By.XPATH,
        "//label[contains(text(),'학교급')]/following-sibling::div//div[@role='combobox']",
    )
    SCHOOL_LEVEL_INPUT = (By.CSS_SELECTOR, "input[name='school_level']")

    GRADE_COMBOBOX = (
        By.XPATH,
        "//input[@name='school_year']/preceding-sibling::div[@role='combobox']",
    )
    GRADE_INPUT = (By.CSS_SELECTOR, "input[name='school_year']")

    SUBJECT_COMBOBOX = (
        By.XPATH,
        "//input[@name='subject']/preceding-sibling::div[@role='combobox']",
    )
    SUBJECT_INPUT_HIDDEN = (By.CSS_SELECTOR, "input[name='subject']")

    PERIOD_COMBOBOX = (
        By.XPATH,
        "//input[@name='lesson_number']/preceding-sibling::div[@role='combobox']",
    )
    PERIOD_INPUT = (By.CSS_SELECTOR, "input[name='lesson_number']")

    TOPIC_INPUT = (By.CSS_SELECTOR, "input[name='topic']")

    METHOD_BASIC   = (By.CSS_SELECTOR, "input[type='radio'][value='basic']")
    METHOD_PRECISE = (
        By.XPATH,
        "//input[@type='radio'][ancestor::label[.//*[contains(text(),'정교한 생성')]]]",
    )

    DROPZONE         = (By.CSS_SELECTOR, "div[data-scope='file-upload'][data-part='dropzone']")
    FILE_INPUT       = (By.CSS_SELECTOR, "input[accept='.pdf,.ppt,.jpg']")

    COMMENT_TEXTAREA = (By.CSS_SELECTOR, "textarea[name='comment']")

    GENERATE_BTN = (
        By.CSS_SELECTOR,
        "button[type='submit'][form='tool-factory-syllabus_generation']",
    )
    SUCCESS_MESSAGE = (
        By.XPATH,
        "//div[@role='tabpanel'][@data-panel='output']"
        "//p[contains(., '입력하신 내용 기반으로 수업 지도안을 생성했습니다')]",
    )

    # ========== 학교급 선택 ==========

    def select_school_level(self, school_level):
        combo = self.wait.until(EC.presence_of_element_located(self.SCHOOL_COMBOBOX))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", combo
        )
        self.wait.until(EC.element_to_be_clickable(self.SCHOOL_COMBOBOX)).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//li[@role='option' and contains(normalize-space(), '{school_level}')]")
            )
        ).click()
        self.wait_backdrop_gone()
        print(f"학교급 '{school_level}' 선택 완료")

    # ========== 필수 입력 ==========

    def select_grade(self, grade):
        combo = self.wait.until(EC.element_to_be_clickable(self.GRADE_COMBOBOX))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combo)
        combo.click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//li[@role='option' and contains(normalize-space(), '{grade}')]")
            )
        ).click()
        self.wait_backdrop_gone()

    def select_subject(self, subject):
        combo = self.wait.until(EC.element_to_be_clickable(self.SUBJECT_COMBOBOX))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combo)
        combo.click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//li[@role='option' and contains(normalize-space(), '{subject}')]")
            )
        ).click()
        self.wait_backdrop_gone()
        self.enter_topic(subject)

    def enter_topic(self, topic):
        inp = self.wait.until(EC.element_to_be_clickable(self.TOPIC_INPUT))
        inp.clear()
        inp.send_keys(topic)

    def select_period(self, period):
        combo = self.wait.until(EC.element_to_be_clickable(self.PERIOD_COMBOBOX))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combo)
        combo.click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//li[@role='option' and contains(normalize-space(), '{period}')]")
            )
        ).click()
        self.wait_backdrop_gone()

    def select_generation_method(self, method="basic"):
        locator = self.METHOD_BASIC if method == "basic" else self.METHOD_PRECISE
        radio = self.wait.until(EC.presence_of_element_located(locator))
        self.js_click(radio)

    # ========== 선택 입력 ==========

    def scroll_to_upload_area(self):
        dropzone = self.wait.until(EC.presence_of_element_located(self.DROPZONE))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", dropzone
        )

    def is_upload_area_visible(self):
        try:
            return self.driver.find_element(*self.DROPZONE).is_displayed()
        except Exception:
            return False

    @staticmethod
    def get_current_path():
        print("current path is ", os.getcwd())
        return os.getcwd()

    def upload_reference(self, file_path):
        file_input = self.wait.until(EC.presence_of_element_located(self.FILE_INPUT))
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.get_current_path(), file_path)
        file_input.send_keys(file_path)

    def enter_comment(self, comment):
        if not comment:
            return
        ta = self.wait.until(EC.presence_of_element_located(self.COMMENT_TEXTAREA))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ta
        )
        ta = self.wait.until(EC.element_to_be_clickable(self.COMMENT_TEXTAREA))
        ta.clear()
        ta.send_keys(comment)

    # ========== 이전 결과 감지 및 재입력 ==========

    def has_previous_result(self):
        try:
            msg = self.driver.find_element(*self.SUCCESS_MESSAGE)
            return msg.is_displayed()
        except Exception:
            return False

    @staticmethod
    def _pick_different(options, current):
        for opt in options:
            if opt != current:
                return opt
        return options[0]

    def regen_with_different_values(self):
        cur_school  = self.driver.find_element(*self.SCHOOL_LEVEL_INPUT).get_attribute("value")
        cur_grade   = self.driver.find_element(*self.GRADE_INPUT).get_attribute("value")
        cur_subject = self.driver.find_element(*self.SUBJECT_INPUT_HIDDEN).get_attribute("value")
        cur_period  = self.driver.find_element(*self.PERIOD_INPUT).get_attribute("value")

        new_school  = self._pick_different(["초등학교", "중학교", "고등학교"], cur_school)
        new_grade   = self._pick_different(["1학년", "2학년", "3학년"], cur_grade)
        new_subject = self._pick_different(["국어", "영어", "수학", "사회", "과학"], cur_subject)
        new_period  = self._pick_different(["1", "2", "3", "4"], cur_period)

        self.select_school_level(new_school)
        self.select_grade(new_grade)
        self.select_subject(new_subject)
        self.select_period(new_period)
        self.select_generation_method("basic")

    # ========== 생성 버튼 및 결과 대기 ==========

    def is_generate_btn_enabled(self) -> bool:
        try:
            btn = self.wait.until(EC.presence_of_element_located(self.GENERATE_BTN))
            return btn.is_enabled()
        except Exception:
            return False

    def click_generate(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.GENERATE_BTN))
        self.js_click(btn)

    def wait_for_generation(self, timeout: int = 60) -> bool:
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
        except Exception:
            return False
