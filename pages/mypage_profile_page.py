from pathlib import Path
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 실행 로그 출력용 logger
logger = logging.getLogger(__name__)


class MyPage:

    # =========================
    # Locator
    # Selenium이 화면 요소를 찾기 위한 경로 정보
    # =========================

    PROFILE_BUTTON = (
        By.CSS_SELECTOR,
        "button.MuiAvatar-root"
    )

    ACCOUNT_MANAGEMENT_MENU = (
        By.XPATH,
        "//span[contains(text(), '계정 관리')]"
    )

    ACCOUNT_MANAGEMENT_TITLE = (
        By.XPATH,
        "//*[contains(text(), '계정 관리')]"
    )

    PAYMENT_HISTORY_MENU = (
        By.XPATH,
        "//*[contains(text(), '결제 내역')]"
    )

    LANGUAGE_SETTING_MENU = (
        By.XPATH,
        "//*[contains(text(), '언어 설정')]"
    )

    CUSTOMER_CENTER_MENU = (
        By.XPATH,
        "//*[contains(text(), '고객 센터')]"
    )

    LOGOUT_MENU = (
        By.XPATH,
        "//*[contains(text(), '로그아웃')]"
    )

    FILE_INPUT = (
        By.CSS_SELECTOR,
        "input[type='file']"
    )

    SAVE_SUCCESS_MESSAGE = (
        By.XPATH,
        "//*[contains(text(), '저장되었습니다') or contains(text(), 'Saved successfully')]"
    )

    NAME_LABEL = (
        By.XPATH,
        "//*[contains(text(), '이름')]"
    )

    EMAIL_LABEL = (
        By.XPATH,
        "//*[contains(text(), '이메일')]"
    )

    REMOVE_PROFILE_IMAGE_MENU = (
        By.XPATH,
        "//li[@role='menuitem']"
        "[.//*[contains(text(), '프로필 이미지 제거')]]"
    )

    PROFILE_IMAGE_EDIT_BUTTON = (
        By.XPATH,
        "//span[contains(@class, 'MuiBadge-badge')]"
        "[.//*[contains(@data-testid, 'pen-to-squareIcon')]]"
    )

    # =========================
    # 초기화
    # =========================

    def __init__(self, driver):

        logger.info("🛠️ MyPage 객체 초기화")

        self.driver = driver

        # 최대 10초 동안 요소가 나타날 때까지 대기
        self.wait = WebDriverWait(driver, 10)

    # =========================
    # 요소 조회
    # 화면 요소가 나타날 때까지 기다렸다가 반환
    # =========================

    def get_profile_button(self):

        logger.info("👤 프로필 버튼 조회 시도")

        try:
            button = self.wait.until(
                EC.element_to_be_clickable(
                    self.PROFILE_BUTTON
                )
            )

            logger.info("✅ 프로필 버튼 조회 완료")

            return button

        except Exception:
            logger.exception(
                "❌ 프로필 버튼 조회 실패"
            )
            raise

    def get_account_management_menu(self):

        logger.info("⚙️ 계정 관리 메뉴 조회 시도")

        try:
            menu = self.wait.until(
                EC.element_to_be_clickable(
                    self.ACCOUNT_MANAGEMENT_MENU
                )
            )

            logger.info("✅ 계정 관리 메뉴 조회 완료")

            return menu

        except Exception:
            logger.exception(
                "❌ 계정 관리 메뉴 조회 실패"
            )
            raise

    def get_payment_history_menu(self):

        logger.info("💳 결제 내역 메뉴 조회 시도")

        try:
            menu = self.wait.until(
                EC.visibility_of_element_located(
                    self.PAYMENT_HISTORY_MENU
                )
            )

            logger.info("✅ 결제 내역 메뉴 조회 완료")

            return menu

        except Exception:
            logger.exception(
                "❌ 결제 내역 메뉴 조회 실패"
            )
            raise

    def get_language_setting_menu(self):

        logger.info("🌐 언어 설정 메뉴 조회 시도")

        try:
            menu = self.wait.until(
                EC.visibility_of_element_located(
                    self.LANGUAGE_SETTING_MENU
                )
            )

            logger.info("✅ 언어 설정 메뉴 조회 완료")

            return menu

        except Exception:
            logger.exception(
                "❌ 언어 설정 메뉴 조회 실패"
            )
            raise

    def get_customer_center_menu(self):

        logger.info("📞 고객 센터 메뉴 조회 시도")

        try:
            menu = self.wait.until(
                EC.visibility_of_element_located(
                    self.CUSTOMER_CENTER_MENU
                )
            )

            logger.info("✅ 고객 센터 메뉴 조회 완료")

            return menu

        except Exception:
            logger.exception(
                "❌ 고객 센터 메뉴 조회 실패"
            )
            raise

    def get_logout_menu(self):

        logger.info("🚪 로그아웃 메뉴 조회 시도")

        try:
            menu = self.wait.until(
                EC.visibility_of_element_located(
                    self.LOGOUT_MENU
                )
            )

            logger.info("✅ 로그아웃 메뉴 조회 완료")

            return menu

        except Exception:
            logger.exception(
                "❌ 로그아웃 메뉴 조회 실패"
            )
            raise

    def get_file_input(self):

        logger.info("📁 파일 업로드 input 조회 시도")

        try:
            file_input = self.wait.until(
                EC.presence_of_element_located(
                    self.FILE_INPUT
                )
            )

            logger.info("✅ 파일 업로드 input 조회 완료")

            return file_input

        except Exception:
            logger.exception(
                "❌ 파일 업로드 input 조회 실패"
            )
            raise

    def get_save_success_message(self):

        logger.info("✅ 저장 완료 메시지 조회 시도")

        try:
            message = self.wait.until(
                EC.visibility_of_element_located(
                    self.SAVE_SUCCESS_MESSAGE
                )
            )

            logger.info("✅ 저장 완료 메시지 조회 완료")

            return message

        except Exception:
            logger.exception(
                "❌ 저장 완료 메시지 조회 실패"
            )
            raise

    def get_name_label(self):

        logger.info("👤 이름 항목 조회 시도")

        try:
            label = self.wait.until(
                EC.visibility_of_element_located(
                    self.NAME_LABEL
                )
            )

            logger.info("✅ 이름 항목 조회 완료")

            return label

        except Exception:
            logger.exception(
                "❌ 이름 항목 조회 실패"
            )
            raise

    def get_email_label(self):

        logger.info("📧 이메일 항목 조회 시도")

        try:
            label = self.wait.until(
                EC.visibility_of_element_located(
                    self.EMAIL_LABEL
                )
            )

            logger.info("✅ 이메일 항목 조회 완료")

            return label

        except Exception:
            logger.exception(
                "❌ 이메일 항목 조회 실패"
            )
            raise

    def get_remove_profile_image_menu(self):

        logger.info("🗑️ 프로필 이미지 제거 메뉴 조회 시도")

        try:
            menu = self.wait.until(
                EC.element_to_be_clickable(
                    self.REMOVE_PROFILE_IMAGE_MENU
                )
            )

            logger.info("✅ 프로필 이미지 제거 메뉴 조회 완료")

            return menu

        except Exception:
            logger.exception(
                "❌ 프로필 이미지 제거 메뉴 조회 실패"
            )
            raise

    def get_profile_image_edit_button(self):

        logger.info("✏️ 프로필 이미지 수정 버튼 조회 시도")

        try:
            button = self.wait.until(
                EC.presence_of_element_located(
                    self.PROFILE_IMAGE_EDIT_BUTTON
                )
            )

            logger.info("✅ 프로필 이미지 수정 버튼 조회 완료")

            return button

        except Exception:
            logger.exception(
                "❌ 프로필 이미지 수정 버튼 조회 실패"
            )
            raise

    # =========================
    # 액션
    # =========================

    def click_profile_button(self):

        logger.info("👆 프로필 버튼 클릭 시도")

        try:
            button = self.get_profile_button()

            self.driver.execute_script(
                "arguments[0].click();",
                button
            )

            logger.info("✅ 프로필 버튼 클릭 완료")

        except Exception:
            logger.exception(
                "❌ 프로필 버튼 클릭 실패"
            )
            raise

    def click_account_management(self):

        logger.info("⚙️ 계정 관리 메뉴 클릭 시도")

        try:
            menu = self.get_account_management_menu()

            self.driver.execute_script(
                "arguments[0].click();",
                menu
            )

            logger.info("✅ 계정 관리 메뉴 클릭 완료")

        except Exception:
            logger.exception(
                "❌ 계정 관리 메뉴 클릭 실패"
            )
            raise

    def move_to_account_management(self):

        logger.info("🚀 계정 관리 페이지 이동 시작")

        try:
            current_window = (
                self.driver.current_window_handle
            )

            self.click_profile_button()

            self.click_account_management()

            logger.info("⏳ 새 탭 열림 대기 중")

            self.wait.until(
                lambda d: len(d.window_handles) > 1
            )

            for window in self.driver.window_handles:

                if window != current_window:

                    self.driver.switch_to.window(window)

                    logger.info(
                        "✅ 계정 관리 페이지 새 탭 이동 완료"
                    )

                    break

        except Exception:
            logger.exception(
                "❌ 계정 관리 페이지 이동 실패"
            )
            raise

    def click_profile_image_edit_button(self):

        logger.info(
            "✏️ 프로필 이미지 수정 버튼 클릭 시도"
        )

        try:
            button = self.get_profile_image_edit_button()

            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);",
                button
            )

            self.driver.execute_script(
                "arguments[0].click();",
                button
            )

            logger.info(
                "✅ 프로필 이미지 수정 버튼 클릭 완료"
            )

        except Exception:
            logger.exception(
                "❌ 프로필 이미지 수정 버튼 클릭 실패"
            )
            raise

    def upload_profile_image(self, image_path):

        logger.info(
            f"📤 프로필 이미지 업로드 시도: {image_path}"
        )

        try:
            absolute_path = str(
                Path(image_path).resolve()
            )

            file_input = self.get_file_input()

            file_input.send_keys(
                absolute_path
            )

            logger.info(
                "✅ 프로필 이미지 업로드 완료"
            )

        except Exception:
            logger.exception(
                "❌ 프로필 이미지 업로드 실패"
            )
            raise

    def click_remove_profile_image_menu(self):

        logger.info(
            "🗑️ 프로필 이미지 제거 클릭 시도"
        )

        try:
            menu = self.get_remove_profile_image_menu()

            self.driver.execute_script(
                "arguments[0].click();",
                menu
            )

            logger.info(
                "✅ 프로필 이미지 제거 완료"
            )

        except Exception:
            logger.exception(
                "❌ 프로필 이미지 제거 실패"
            )
            raise