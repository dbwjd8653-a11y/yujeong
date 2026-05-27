from config.selenium_imports import By, EC

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
            self.wait_until_invisible(self._TOAST_ALERT, 5)
        except Exception:
            pass

    def activate_disabled_model(self):
        self._wait_toast_gone()
        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                try:
                    list_item = checkbox.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
                    name_el = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
                    model_name = name_el.text
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    self.js_click(checkbox)
                    return model_name
                except Exception:
                    continue
        return None

    def deactivate_active_model(self):
        self._wait_toast_gone()
        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        for checkbox in reversed(checkboxes):
            if checkbox.is_selected():
                try:
                    list_item = checkbox.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
                    name_el = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
                    model_name = name_el.text
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    self.js_click(checkbox)
                    return model_name
                except Exception:
                    continue
        return None

    def get_toast_message(self):
        return self.wait_for_visible(self._TOAST_ALERT).text
