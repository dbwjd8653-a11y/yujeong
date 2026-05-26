# pages/mypage/mypage_account_page.py
# 마이페이지 > 계정 관리 — 기본 정보 전용 Page 클래스
# FHC-073(이름 변경) / FHC-074(비밀번호 변경) / FHC-075(프로모션 알림) / FHC-076(선호 언어)

import time

from config.selenium_imports import By, EC

from pages.mypage.mypage_page import MyPage


class MyPage05(MyPage):

    # ========== Locators — FHC-073: 이름 변경 ==========
    NAME_INPUT = (By.CSS_SELECTOR, "input[name='fullname']")
    SAVE_SUCCESS_TOAST = (By.XPATH,
        "//*[contains(text(),'저장되었습니다') or contains(text(),'Saved successfully')"
        " or contains(text(),'saved')]"
    )
    # 이름/비밀번호 인라인 편집 완료 버튼
    COMPLETE_BUTTON = (By.XPATH,
        "//button[@type='submit' and contains(@class,'MuiLoadingButton-root')]"
    )

    # ========== Locators — FHC-074: 비밀번호 변경 ==========
    CURRENT_PW_INPUT = (By.CSS_SELECTOR, "input[autocomplete='current-password']")
    NEW_PW_INPUT     = (By.CSS_SELECTOR, "input[name='newPassword']")
    CONFIRM_PW_INPUT = (By.CSS_SELECTOR, "input[name='confirmPassword']")

    # ========== Locators — FHC-075: 프로모션 알림 ==========
    PROMOTION_TOGGLE = (By.XPATH,
        "//input[@type='checkbox' and ("
        "@name='marketing' or @name='promotion' or @name='promotionAlarm'"
        ")]"
        " | //*[contains(text(),'프로모션 알림 받기')]/ancestor::label//input[@type='checkbox']"
        " | //*[contains(text(),'프로모션 알림 받기')]/following-sibling::*//input[@type='checkbox']"
    )

    # ========== FHC-073: 이름 변경 ==========

    def click_name_edit(self):
        """이름 옆 편집 아이콘 클릭 (JS — SVG 네임스페이스 문제 우회)"""
        result = self.driver.execute_script("""
            var s = document.querySelectorAll('svg[data-testid="EditOutlinedIcon"]');
            if (s.length > 0 && s[0].closest('button')) {
                s[0].closest('button').click(); return 'ok';
            }
            var b = document.querySelectorAll('button.MuiIconButton-root');
            if (b.length > 0) { b[0].click(); return 'fallback'; }
            return 'not-found';
        """)
        if result == 'not-found':
            raise Exception("이름 편집 버튼을 찾을 수 없습니다")
        self.logger.info(f"이름 편집 버튼 클릭 완료 ({result})")

    def enter_name(self, name: str):
        name_input = self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))
        name_input.clear()
        name_input.send_keys(name)
        self.logger.info(f"이름 입력 완료: {name}")

    def save_name(self):
        self.js_click(
            self.wait.until(EC.element_to_be_clickable(self.COMPLETE_BUTTON))
        )
        self.logger.info("이름 저장(완료) 버튼 클릭 완료")

    def is_save_success_toast_displayed(self) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(self.SAVE_SUCCESS_TOAST))
            return True
        except Exception:
            return False

    # ========== FHC-074: 비밀번호 변경 ==========

    def click_password_edit(self):
        """비밀번호 옆 편집 아이콘 클릭 (JS — SVG 네임스페이스 문제 우회)"""
        result = self.driver.execute_script("""
            var s = document.querySelectorAll('svg[data-testid="EditOutlinedIcon"]');
            if (s.length >= 4 && s[3].closest('button')) {
                s[3].closest('button').click(); return 'ok';
            }
            var b = document.querySelectorAll('button.MuiIconButton-root');
            if (b.length >= 4) { b[3].click(); return 'fallback'; }
            return 'not-found';
        """)
        if result == 'not-found':
            raise Exception("비밀번호 편집 버튼을 찾을 수 없습니다")
        self.logger.info(f"비밀번호 편집 버튼 클릭 완료 ({result})")

    def change_password(self, current_pw: str, new_pw: str):
        """비밀번호 변경 (current_pw → new_pw, 동일 비밀번호 불가)"""
        curr = self.wait.until(EC.visibility_of_element_located(self.CURRENT_PW_INPUT))
        curr.clear()
        curr.send_keys(current_pw)

        new = self.wait.until(EC.visibility_of_element_located(self.NEW_PW_INPUT))
        new.clear()
        new.send_keys(new_pw)

        confirm = self.wait.until(EC.visibility_of_element_located(self.CONFIRM_PW_INPUT))
        confirm.clear()
        confirm.send_keys(new_pw)

        self.js_click(
            self.wait.until(EC.element_to_be_clickable(self.COMPLETE_BUTTON))
        )
        self.logger.info(f"비밀번호 변경 완료: {current_pw} → {new_pw}")
        time.sleep(1)

    # ========== FHC-075: 프로모션 알림 토글 ==========

    def get_promotion_state(self) -> bool:
        checkbox = self.wait.until(
            EC.presence_of_element_located(self.PROMOTION_TOGGLE)
        )
        state = checkbox.is_selected()
        self.logger.info(f"프로모션 알림 현재 상태: {'ON' if state else 'OFF'}")
        return state

    def toggle_promotion(self):
        checkbox = self.wait.until(
            EC.presence_of_element_located(self.PROMOTION_TOGGLE)
        )
        self.driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(0.5)
        self.logger.info("프로모션 알림 토글 클릭 완료")
