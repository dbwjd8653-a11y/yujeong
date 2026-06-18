from config.selenium_imports import By, EC, TimeoutException

from pages.settings.settings_general_page import SettingsPage


class SettingsMemberPage(SettingsPage):

    _MEMBER_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/users"][role="tab"]')
    _TOKEN_LIMIT_TOGGLE = (By.CSS_SELECTOR, 'span.MuiSwitch-sizeMedium input[type="checkbox"]')
    _SAVE_BTN = (By.XPATH, '//button[@type="submit"][normalize-space()="저장"]')
    _TOAST = (By.ID, 'notistack-snackbar')

    # 저장 버튼/토스트 대기는 기본(10초)보다 넉넉히 — CI(headless·느린 환경)에서
    # 저장 후 토스트가 10초를 넘겨 뜨며 TimeoutException으로 flaky
    _SAVE_WAIT = 20

    def navigate_to_member_tab(self):
        self.js_click(self.wait.until(EC.element_to_be_clickable(self._MEMBER_TAB)))
        self.wait.until(EC.url_contains("/ai-helpy-chat/admin/users"))

    def get_toggle(self):
        toggle = self.wait.until(EC.presence_of_element_located(self._TOKEN_LIMIT_TOGGLE))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
        return toggle

    def is_toggle_checked(self, toggle):
        return self.driver.execute_script("return arguments[0].checked", toggle)

    def set_token_limit_toggle(self, activate: bool):
        """토큰 한도 토글을 원하는 상태로 설정.

        MUI 스위치의 숨은 input에 JS click이 headless Edge에서 간헐적으로 React에
        전달되지 않아 상태가 안 바뀔 때가 있다 → 반영될 때까지 최대 3회 재클릭한다.
        """
        for _ in range(3):
            toggle = self.get_toggle()
            if self.is_toggle_checked(toggle) == activate:
                return
            self.js_click(toggle)
            try:
                self.wait.until(
                    lambda d: self.is_toggle_checked(d.find_element(*self._TOKEN_LIMIT_TOGGLE)) == activate
                )
                return
            except TimeoutException:
                continue
        raise TimeoutException(
            f"토큰 한도 토글을 {'ON' if activate else 'OFF'}로 변경하지 못했습니다 (3회 재시도)"
        )

    def _wait_visible_save_btn(self, timeout=None):
        """'저장' 제출 버튼이 섹션별 form마다 여러 개 존재할 수 있어,
        DOM 첫 매치(숨겨진 버튼)를 잡으면 element_to_be_clickable이 타임아웃난다.
        화면에 보이고 활성화된 버튼만 골라 반환한다."""
        def _find(driver):
            for btn in driver.find_elements(*self._SAVE_BTN):
                if btn.is_displayed() and btn.is_enabled():
                    return btn
            return False
        return self._wait(timeout).until(_find)

    def save_and_verify_toast(self):
        try:
            self.wait_until_invisible(self._TOAST, 5)
        except Exception:
            pass
        save_btn = self._wait_visible_save_btn(self._SAVE_WAIT)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        self.js_click(save_btn)
        toast = self._wait(self._SAVE_WAIT).until(EC.visibility_of_element_located(self._TOAST))
        assert "저장되었습니다" in toast.text, f"저장 알림창 메시지 불일치: '{toast.text}'"

    def _ensure_saved_state(self, activate: bool):
        """토글의 '저장된(서버 반영) 값'을 activate로 맞춘다.
        이미 그 값이면 아무것도 하지 않고, 다르면 토글 후 저장한다.
        (토글을 누른 뒤엔 항상 저장하므로 DOM 값 == 저장된 값 불변식이 유지된다.)"""
        toggle = self.get_toggle()
        if self.is_toggle_checked(toggle) == activate:
            return
        self.set_token_limit_toggle(activate)
        self.save_and_verify_toast()

    def toggle_token_limit_and_save(self, activate: bool):
        """토큰 한도 토글을 activate 상태로 바꾸고 저장 → 토스트를 검증한다.

        저장 버튼은 '저장된 값과 다를 때만' 활성화되므로, 목표의 반대 상태를
        먼저 저장해 baseline을 고정한 뒤 본 토글을 수행한다. 이 보정을 생략하면
        직전 실행이 남긴 저장 상태에 따라 순변경이 0이 되어 저장 버튼이 비활성화되고
        TimeoutException으로 flaky하게 실패한다."""
        self._ensure_saved_state(not activate)
        self.set_token_limit_toggle(activate)
        self.save_and_verify_toast()
