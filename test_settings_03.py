"""[test_settings_03] 모델설정"""



import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from settings_page import SettingsPage


# =====================
# 테스트: 로그인 후 설정 페이지 이동
# =====================
def test_settings(login):
    driver, wait = login
    time.sleep(5)

    # 1. 설정 페이지 이동 (기어 클릭 → 드롭다운 설정 클릭 → URL 확인)
    page = SettingsPage(driver, wait)
    page.navigate_to_settings()

    # 2. 모델 설정 탭 클릭
    models_tab = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/models"][role="tab"]')
    ))
    models_tab.click()
    assert wait.until(EC.url_contains("/ai-helpy-chat/admin/models")), "모델 설정 탭 이동 실패"
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.MuiListItem-root')))
    time.sleep(1)

    # 3. 비활성화된 토글 하나 활성화
    activated_model = None

    # 4. 체크박스에서 시작 → 부모 li에서 모델 이름 가져오기 (사이드바 항목 제외)
    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            try:
                list_item = checkbox.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
                name_el = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
                activated_model = name_el.text
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", checkbox)
                break
            except Exception:
                continue
    assert activated_model, "비활성화된 모델을 찾지 못함"
    time.sleep(2)

    # 5. 새 대화 탭 클릭
    new_chat_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat"]')
    ))
    new_chat_btn.click()
    assert wait.until(lambda d: "admin" not in d.current_url), "새 대화 탭 이동 실패"
    time.sleep(2)

    # 6. Agent 드롭다운 클릭
    agent_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div.css-18ssuj3')
    ))
    agent_btn.click()
    time.sleep(2)

    # 7. 드롭다운 목록에 활성화한 모델명이 있는지 확인
    model_titles = driver.find_elements(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
    title_texts = [t.text for t in model_titles]
    assert activated_model in title_texts, \
        f"모델 추가 실패: '{activated_model}'이 목록에 없음 {title_texts}"
    time.sleep(2)

    # 8. 드롭다운 닫기
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    time.sleep(1)

    # 9. 설정 페이지 재이동
    page.navigate_to_settings()

    # 10. 모델 설정 탭으로 이동
    models_tab = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/models"][role="tab"]')
    ))
    models_tab.click()
    assert wait.until(EC.url_contains("/ai-helpy-chat/admin/models")), "모델 설정 탭 이동 실패"
    time.sleep(2)

    # 11. step 4에서 활성화한 모델을 이름으로 찾아서 비활성화
    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
    for checkbox in checkboxes:
        try:
            list_item = checkbox.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
            name_el = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
            if name_el.text == activated_model:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", checkbox)
                break
        except Exception:
            continue
    time.sleep(2)

    # 12. 새 대화 탭으로 이동
    new_chat_btn2 = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat"]')
    ))
    new_chat_btn2.click()
    assert wait.until(lambda d: "admin" not in d.current_url), "새 대화 탭 이동 실패"
    time.sleep(2)

    # 13. Agent 드롭다운 열기
    agent_btn2 = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div.css-18ssuj3')
    ))
    agent_btn2.click()
    time.sleep(2)

    # 14. 드롭다운 목록에서 모델명이 사라졌는지 확인
    model_titles = driver.find_elements(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
    title_texts = [t.text for t in model_titles]
    assert activated_model not in title_texts, \
        f"모델 비활성화 실패: '{activated_model}'이 아직 목록에 있음"
    time.sleep(2)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
