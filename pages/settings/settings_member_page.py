from config.selenium_imports import By, EC, TimeoutException

from pages.settings.settings_general_page import SettingsPage


class SettingsMemberPage(SettingsPage):

    _MEMBER_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/users"][role="tab"]')
    _TOKEN_LIMIT_TOGGLE = (By.CSS_SELECTOR, 'span.MuiSwitch-sizeMedium input[type="checkbox"]')
    _SAVE_BTN = (By.XPATH, '//button[@type="submit"][normalize-space()="저장"]')
    _TOAST = (By.ID, 'notistack-snackbar')
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
        def _find(driver):
            for btn in driver.find_elements(*self._SAVE_BTN):
                if btn.is_displayed() and btn.is_enabled():
                    return btn
            return False
        return self._wait(timeout).until(_find)

    def _toast_shown(self, timeout=5) -> bool:
        def _find(driver):
            for t in driver.find_elements(*self._TOAST):
                if t.is_displayed() and "저장되었습니다" in t.text:
                    return True
            return False
        try:
            return self._wait(timeout).until(_find)
        except TimeoutException:
            return False

    def _save(self):
        try:
            self.wait_until_invisible(self._TOAST, 5)
        except Exception:
            pass
        save_btn = self._wait_visible_save_btn(self._SAVE_WAIT)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
        self.js_click(save_btn)
        if not self._toast_shown():
            self.logger.warning("저장 토스트를 감지하지 못했습니다 (headless에서 흔함) — 토글 상태로 검증")

    def _ensure_saved_state(self, activate: bool):
        toggle = self.get_toggle()
        if self.is_toggle_checked(toggle) == activate:
            return
        self.set_token_limit_toggle(activate)
        self._save()

    def toggle_token_limit_and_save(self, activate: bool):
        self._ensure_saved_state(not activate)
        self.set_token_limit_toggle(activate)
        self._save()
