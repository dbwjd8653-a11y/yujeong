# pages/mypage/mypage_profile_page.py

from pathlib import Path

from config.selenium_imports import By, EC

from pages.base_page import BasePage


class MyPage(BasePage):

    # ── Locators ──────────────────────────────────────────────────────

    PROFILE_BUTTON             = (By.CSS_SELECTOR, "button.MuiAvatar-root")
    ACCOUNT_MANAGEMENT_MENU    = (By.XPATH, "//span[contains(text(), '계정 관리')]")
    ACCOUNT_MANAGEMENT_TITLE   = (By.XPATH, "//*[contains(text(), '계정 관리')]")
    PAYMENT_HISTORY_MENU       = (By.XPATH, "//*[contains(text(), '결제 내역')]")
    LANGUAGE_SETTING_MENU      = (By.XPATH, "//*[contains(text(), '언어 설정')]")
    CUSTOMER_CENTER_MENU       = (By.XPATH, "//*[contains(text(), '고객 센터')]")
    LOGOUT_MENU                = (By.XPATH, "//*[contains(text(), '로그아웃')]")
    FILE_INPUT                 = (By.CSS_SELECTOR, "input[type='file']")
    SAVE_SUCCESS_MESSAGE       = (By.XPATH, "//*[contains(text(), '저장되었습니다') or contains(text(), 'Saved successfully')]")
    NAME_LABEL                 = (By.XPATH, "//*[contains(text(), '이름')]")
    EMAIL_LABEL                = (By.XPATH, "//*[contains(text(), '이메일')]")
    REMOVE_PROFILE_IMAGE_MENU  = (By.XPATH, "//li[@role='menuitem'][.//*[contains(text(), '프로필 이미지 제거')]]")
    PROFILE_IMAGE_EDIT_BUTTON  = (By.XPATH, "//span[contains(@class, 'MuiBadge-badge')][.//*[contains(@data-testid, 'pen-to-squareIcon')]]")

    # ── 요소 조회 (테스트에서 직접 사용) ─────────────────────────────

    def get_profile_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.PROFILE_BUTTON))

    def get_account_management_menu(self):
        return self.wait.until(EC.element_to_be_clickable(self.ACCOUNT_MANAGEMENT_MENU))

    def get_payment_history_menu(self):
        return self.wait.until(EC.visibility_of_element_located(self.PAYMENT_HISTORY_MENU))

    def get_language_setting_menu(self):
        return self.wait.until(EC.visibility_of_element_located(self.LANGUAGE_SETTING_MENU))

    def get_customer_center_menu(self):
        return self.wait.until(EC.visibility_of_element_located(self.CUSTOMER_CENTER_MENU))

    def get_logout_menu(self):
        return self.wait.until(EC.visibility_of_element_located(self.LOGOUT_MENU))

    def get_file_input(self):
        return self.wait.until(EC.presence_of_element_located(self.FILE_INPUT))

    def get_save_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.SAVE_SUCCESS_MESSAGE))

    def get_name_label(self):
        return self.wait.until(EC.visibility_of_element_located(self.NAME_LABEL))

    def get_email_label(self):
        return self.wait.until(EC.visibility_of_element_located(self.EMAIL_LABEL))

    def get_remove_profile_image_menu(self):
        return self.wait.until(EC.element_to_be_clickable(self.REMOVE_PROFILE_IMAGE_MENU))

    def get_profile_image_edit_button(self):
        return self.wait.until(EC.presence_of_element_located(self.PROFILE_IMAGE_EDIT_BUTTON))

    # ── 액션 ──────────────────────────────────────────────────────────

    def click_profile_button(self):
        self.js_click(self.get_profile_button())
        self.logger.info("프로필 버튼 클릭 완료")

    def click_account_management(self):
        self.js_click(self.get_account_management_menu())
        self.logger.info("계정 관리 메뉴 클릭 완료")

    def move_to_account_management(self):
        current_window = self.driver.current_window_handle
        self.click_profile_button()
        self.click_account_management()
        self.wait.until(lambda d: len(d.window_handles) > 1)
        for window in self.driver.window_handles:
            if window != current_window:
                self.driver.switch_to.window(window)
                break
        self.logger.info("계정 관리 페이지 새 탭 이동 완료")

    def click_profile_image_edit_button(self):
        button = self.get_profile_image_edit_button()
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.js_click(button)
        self.logger.info("프로필 이미지 수정 버튼 클릭 완료")

    def upload_profile_image(self, image_path):
        absolute_path = str(Path(image_path).resolve())
        self.get_file_input().send_keys(absolute_path)
        self.logger.info(f"프로필 이미지 업로드 완료: {absolute_path}")

    def click_remove_profile_image_menu(self):
        self.js_click(self.get_remove_profile_image_menu())
        self.logger.info("프로필 이미지 제거 완료")
