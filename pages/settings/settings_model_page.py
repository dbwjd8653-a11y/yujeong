from config.selenium_imports import By, EC, WebDriverWait

from pages.settings.settings_general_page import SettingsPage


class SettingsModelPage(SettingsPage):

    _MODELS_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/models"][role="tab"]')
    _TOAST_ALERT = (By.ID, 'notistack-snackbar')

    def navigate_to_models_tab(self):
        self._wait_toast_gone()
        tab = self.wait.until(EC.element_to_be_clickable(self._MODELS_TAB))
        self.js_click(tab)
        self.wait.until(EC.url_contains("/ai-helpy-chat/admin/models"))
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.MuiListItem-root')))

    def _wait_toast_gone(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self._TOAST_ALERT)
            )
        except Exception:
            return
        try:
            self.wait_until_invisible(self._TOAST_ALERT, 5)
        except Exception:
            pass

    _TOGGLE = (By.CSS_SELECTOR, 'input.MuiSwitch-input[type="checkbox"]')

    def activate_disabled_model(self):
        self._wait_toast_gone()
        self.wait.until(EC.presence_of_element_located(self._TOGGLE))
        toggles = self.driver.find_elements(*self._TOGGLE)
        for toggle in toggles:
            if not self.driver.execute_script("return arguments[0].checked", toggle):
                try:
                    list_item = toggle.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
                    model_name = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary').text
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
                    self.js_click(toggle)
                    return model_name
                except Exception:
                    continue
        return None

    def deactivate_active_model(self):
        self._wait_toast_gone()
        self.wait.until(EC.presence_of_element_located(self._TOGGLE))
        toggles = self.driver.find_elements(*self._TOGGLE)
        for toggle in reversed(toggles):
            if self.driver.execute_script("return arguments[0].checked", toggle):
                try:
                    list_item = toggle.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
                    model_name = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary').text
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
                    self.js_click(toggle)
                    return model_name
                except Exception:
                    continue
        return None

    def get_toast_message(self):
        return self.wait_for_visible(self._TOAST_ALERT).text
