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
        By.XPATH,
        "//button[@type='submit'][@form='tool-factory-syllabus_generation']"
        "[not(ancestor::div[@role='dialog'])]",
    )
    REGEN_CONFIRM_BTN = (
        By.XPATH,
        "//div[@role='dialog']//button[@type='submit'][@form='tool-factory-syllabus_generation']",
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
        filename = os.path.basename(file_path)
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(text(), '{filename}')]")
        ))


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

    def regen_with_random_values(self):
        import random
        self.select_school_level(random.choice(["초등학교", "중학교", "고등학교"]))
        self.select_grade(random.choice(["1학년", "2학년", "3학년"]))
        self.select_subject(random.choice(["국어", "영어", "수학", "사회", "과학"]))
        self.select_period(random.choice(["1", "2", "3", "4"]))
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
        try:
            confirm = self.wait.until(EC.element_to_be_clickable(self.REGEN_CONFIRM_BTN))
            self.js_click(confirm)
        except Exception:
            pass

    def wait_for_generation(self, timeout: int = 60) -> bool:
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
        except Exception:
            return False

    def wait_for_regeneration(self, timeout: int = 60) -> bool:
        from selenium.webdriver.support.ui import WebDriverWait
        wait = WebDriverWait(self.driver, timeout)
        try:
            try:
                old = self.driver.find_element(*self.SUCCESS_MESSAGE)
                if old.is_displayed():
                    wait.until(EC.invisibility_of_element_located(self.SUCCESS_MESSAGE))
            except Exception:
                pass
            wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except Exception:
            return False
