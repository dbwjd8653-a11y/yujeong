# pages/tools/tools_specialty_page.py
# '세부 특기사항' 도구 전용 Page 클래스
# BaseToolPage에 없는 학년/과목/단원 입력 + 학습 태도 키워드 선택 로직을 담당


from selenium.webdriver.common.keys import Keys

from config.selenium_imports import By, EC, WebDriverWait

from pages.tools.base_tool_page import BaseToolPage


class SpecialtyPage(BaseToolPage):

    TOOL_NAME = "세부 특기사항"

    # ========== Locators ==========

    GRADE_COMBOBOX = (
        By.XPATH,
        "//input[@name='grade']/preceding-sibling::div[@role='combobox']",
    )
    SUBJECT_INPUT = (By.CSS_SELECTOR, "input[placeholder*='과목'], input[placeholder*='Subject']")
    UNIT_INPUT    = (By.CSS_SELECTOR, "input[name='unit']")

    # 키워드 모달 — 학습 태도 아코디언
    STUDY_ATTITUDE_ACCORDION = (
        By.XPATH,
        "//*[@role='dialog']//div[contains(@class,'MuiAccordionSummary-root')"
        " and (contains(normalize-space(.), '학습 태도') or contains(normalize-space(.), 'Learning Attitude'))]",
    )
    # 수업 집중도 높음 칩
    CONCENTRATION_CHIP = (
        By.XPATH,
        "//*[@role='dialog']//div[contains(@class,'MuiChip-root')"
        " and contains(@class,'MuiChip-outlined')]"
        "[.//span[contains(@class,'MuiChip-label') and "
        "(text()='수업 집중도 높음' or contains(text(),'Concentration') or contains(text(),'Focus'))]]",
    )

    # ========== 수업 정보 입력 — 학년/과목/단원 ==========

    def select_grade(self, grade: str):
        self.wait.until(EC.element_to_be_clickable(self.GRADE_COMBOBOX)).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//li[@role='option' and @data-value='{grade}']")
            )
        ).click()
        self.wait_backdrop_gone()
        self.logger.info(f"학년 '{grade}' 선택 완료")

    def enter_subject(self, subject: str):
        subject_input = self.wait.until(EC.element_to_be_clickable(self.SUBJECT_INPUT))
        subject_input.click()
        subject_input.send_keys(Keys.CONTROL + "a")
        subject_input.send_keys(Keys.DELETE)
        subject_input.send_keys(subject)
        try:
            WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//li[@role='option' and normalize-space(text())='{subject}']")
                )
            ).click()
            self.logger.info(f"과목 '{subject}' 목록에서 선택 완료")
        except Exception:
            subject_input.send_keys(Keys.ESCAPE)
            self.logger.info(f"과목 '{subject}' 직접 입력 완료")

    def enter_unit(self, unit: str):
        unit_input = self.wait.until(EC.element_to_be_clickable(self.UNIT_INPUT))
        unit_input.click()
        unit_input.send_keys(Keys.CONTROL + "a")
        unit_input.send_keys(Keys.DELETE)
        unit_input.send_keys(unit)
        self.logger.info(f"단원 '{unit}' 입력 완료")

    # ========== 키워드 선택 — 학습 태도 ==========

    def select_study_attitude_keyword(self):
        """학습 태도 아코디언 → 수업 집중도 높음 칩 선택"""
        self.js_click(
            self.wait.until(EC.presence_of_element_located(self.STUDY_ATTITUDE_ACCORDION))
        )
        self.logger.info("학습 태도 아코디언 펼치기 완료")

        self.js_click(
            self.wait.until(EC.presence_of_element_located(self.CONCENTRATION_CHIP))
        )
        self.logger.info("수업 집중도 높음 선택 완료")
