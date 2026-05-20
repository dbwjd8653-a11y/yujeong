"""[test_settings_03] 모델설정"""



import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# =====================
# 테스트: 로그인 후 설정 페이지 이동
# =====================
def test_settings(login):
    driver, wait = login
    time.sleep(5)

    # 1. 로그인 성공 확인 (기어 아이콘이 보이면 로그인 성공)
    gear_btn = driver.find_element(
        By.CSS_SELECTOR,
        'button:has(svg[data-testid="gearIcon"])'
    )

    gear_btn.click()
    time.sleep(1)

    # 6. 드롭다운에서 설정 클릭
    settings_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[role="menuitem"]:has(svg[data-testid="gearIcon"])')
    ))
    settings_btn.click()
    time.sleep(1)

    # 7. 설정 페이지 이동 확인
    wait.until(EC.url_contains("/ai-helpy-chat/admin"))
    assert "/ai-helpy-chat/admin" in driver.current_url, f"설정 페이지 이동 실패: {driver.current_url}"
    print("설정 페이지 이동 성공:", driver.current_url)
    time.sleep(2)

    # 8. 모델 설정 탭 클릭
    models_tab = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/models"][role="tab"]')
    ))
    models_tab.click()
    print("모델 설정 탭 클릭 성공")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.MuiListItem-root')))
    time.sleep(1)

    # 9. 비활성화된 토글 하나 활성화
    activated_model = None

    # 체크박스에서 시작 → 부모 li에서 모델 이름 가져오기 (사이드바 항목 제외)
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
                print(f"활성화한 모델: {activated_model}")
                break
            except Exception:
                continue
    time.sleep(2)

    # 10. 새 대화 탭 클릭
    new_chat_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat"]')
    ))
    new_chat_btn.click()
    print("새 대화 탭 클릭 성공")
    time.sleep(2)

    # 11. Agent 드롭다운 클릭
    agent_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div.css-18ssuj3')
    ))
    agent_btn.click()
    print("Agent 드롭다운 클릭 성공")
    time.sleep(2)

    # 12. 드롭다운 목록에 활성화한 모델명이 있는지 확인
    model_titles = driver.find_elements(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
    title_texts = [t.text for t in model_titles]
    assert activated_model in title_texts, \
        f"모델 추가 실패: '{activated_model}'이 목록에 없음 {title_texts}"
    print("모델 추가 완료!")
    time.sleep(2)

    # 드롭다운 닫기
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    time.sleep(1)

    # 13. 설정 버튼 클릭
    gear_btn = driver.find_element(
        By.CSS_SELECTOR,
        'button:has(svg[data-testid="gearIcon"])'
    )

    gear_btn.click()
    time.sleep(1)

    # 14. 드롭다운에서 설정 클릭
    settings_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[role="menuitem"]:has(svg[data-testid="gearIcon"])')
    ))
    settings_btn.click()
    time.sleep(1)

    # 15. 설정 페이지 이동 확인
    wait.until(EC.url_contains("/ai-helpy-chat/admin"))
    assert "/ai-helpy-chat/admin" in driver.current_url, f"설정 페이지 이동 실패: {driver.current_url}"
    print("설정 페이지 이동 성공:", driver.current_url)
    time.sleep(2)

    # 16. 모델 설정 탭으로 이동
    models_tab = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/models"][role="tab"]')
    ))
    models_tab.click()
    print("모델 설정 탭 이동 성공")
    time.sleep(2)

    # 17. step 9에서 활성화한 모델을 이름으로 찾아서 비활성화
    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
    for checkbox in checkboxes:
        try:
            list_item = checkbox.find_element(By.XPATH, './ancestor::li[contains(@class,"MuiListItem")]')
            name_el = list_item.find_element(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
            if name_el.text == activated_model:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", checkbox)
                print(f"'{activated_model}' 비활성화 완료")
                break
        except Exception:
            continue
    time.sleep(2)

    # 18. 새 대화 탭으로 이동
    new_chat_btn2 = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat"]')
    ))
    new_chat_btn2.click()
    print("새 대화 탭 클릭 성공")
    time.sleep(2)

    # 19. Agent 드롭다운 열기
    agent_btn2 = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div.css-18ssuj3')
    ))
    agent_btn2.click()
    print("Agent 드롭다운 클릭 성공")
    time.sleep(2)

    # 20. 드롭다운 목록에서 모델명이 사라졌는지 확인
    model_titles = driver.find_elements(By.CSS_SELECTOR, 'span.MuiListItemText-primary')
    title_texts = [t.text for t in model_titles]

    assert activated_model not in title_texts, \
        f"모델 비활성화 실패: '{activated_model}'이 아직 목록에 있음"
    print("모델 삭제 완료!")
    time.sleep(2)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

