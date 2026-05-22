import time

from config.selenium_imports import By, EC

from selenium.webdriver.common.keys import Keys

from pages.settings.settings_general_page import SettingsPage


class SettingsModelPage(SettingsPage):

    _MODELS_TAB = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/models"][role="tab"]')
    _NEW_CHAT_BTN = (By.CSS_SELECTOR, 'a:has(svg[data-testid="pen-to-squareIcon"])')
    _AGENT_DROPDOWN = (By.CSS_SELECTOR, 'button:has(svg[data-testid="chevron-downIcon"])')
    _MODEL_TITLE = (By.CSS_SELECTOR, 'span.MuiListItemText-primary')

    def navigate_to_models_tab(self):
        self.wait.until(EC.element_to_be_clickable(self._MODELS_TAB)).click()
        assert self.wait.until(EC.url_contains("/ai-helpy-chat/admin/models")), "모델 설정 탭 이동 실패"
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.MuiListItem-root')))
        time.sleep(1)

    def activate_disabled_model(self):
        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                try:
                    list_item = checkbox.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
                    name_el = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
                    model_name = name_el.text
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", checkbox)
                    return model_name
                except Exception:
                    continue
        return None

    def deactivate_model(self, model_name):
        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        for checkbox in checkboxes:
            try:
                list_item = checkbox.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
                name_el = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
                if name_el.text == model_name:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", checkbox)
                    return
            except Exception:
                continue

    def navigate_to_new_chat(self):
        self.wait.until(EC.element_to_be_clickable(self._NEW_CHAT_BTN)).click()
        assert self.wait.until(lambda d: "admin" not in d.current_url), "새 대화 탭 이동 실패"
        time.sleep(2)

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
        time.sleep(1)
