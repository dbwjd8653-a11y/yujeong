from config.selenium_imports import By, EC, WebDriverWait

from selenium.webdriver.common.keys import Keys

from pages.settings.settings_general_page import SettingsPage


class SettingsModelPage(SettingsPage):

    _MODELS_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/models"][role="tab"]')
    _NEW_CHAT_BTN = (By.CSS_SELECTOR, 'a:has(svg[data-testid="pen-to-squareIcon"])')
    _AGENT_DROPDOWN = (By.CSS_SELECTOR, 'button:has(svg[data-testid="chevron-downIcon"])')
    _MODEL_TITLE = (By.CSS_SELECTOR, 'span.MuiListItemText-primary')
    _TOAST_ALERT = (By.ID, 'notistack-snackbar')

    def navigate_to_models_tab(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self._TOAST_ALERT)
            )
        except Exception:
            pass
        tab = self.wait.until(EC.element_to_be_clickable(self._MODELS_TAB))
        self.driver.execute_script("arguments[0].click();", tab)
        self.wait.until(EC.url_contains("/ai-helpy-chat/admin/models"))
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.MuiListItem-root')))

    def activate_disabled_model(self):
        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                try:
                    list_item = checkbox.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
                    name_el = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
                    model_name = name_el.text
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    self.driver.execute_script("arguments[0].click();", checkbox)
                    return model_name
                except Exception:
                    continue
        return None

    def deactivate_active_model(self):
        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        for checkbox in reversed(checkboxes):
            if checkbox.is_selected():
                try:
                    list_item = checkbox.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
                    name_el = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
                    model_name = name_el.text
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    self.driver.execute_script("arguments[0].click();", checkbox)
                    return model_name
                except Exception:
                    continue
        return None

    def navigate_to_new_chat(self):
        self.wait.until(EC.element_to_be_clickable(self._NEW_CHAT_BTN)).click()
        self.wait.until(lambda d: "admin" not in d.current_url)

    def open_agent_dropdown(self):
        before = len(self.driver.find_elements(*self._MODEL_TITLE))
        self.wait.until(EC.element_to_be_clickable(self._AGENT_DROPDOWN)).click()
        # 드롭다운 항목이 추가로 렌더링될 때까지 대기
        self.wait.until(lambda d: len(d.find_elements(*self._MODEL_TITLE)) > before)

    def get_dropdown_model_titles(self):
        elements = self.driver.find_elements(*self._MODEL_TITLE)
        return [el.text for el in elements]

    def close_dropdown(self):
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

    def get_toast_message(self):
        el = self.wait.until(EC.visibility_of_element_located(self._TOAST_ALERT))
        return el.text
