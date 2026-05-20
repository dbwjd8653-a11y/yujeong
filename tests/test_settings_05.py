"""[test_settings_05] 구성원 관리"""



import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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

    # 2. 드롭다운에서 설정 클릭
    settings_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[role="menuitem"]:has(svg[data-testid="gearIcon"])')
    ))
    settings_btn.click()
    time.sleep(1)

    # 3. 설정 페이지 이동 확인
    wait.until(EC.url_contains("/ai-helpy-chat/admin"))
    assert "/ai-helpy-chat/admin" in driver.current_url, f"설정 페이지 이동 실패: {driver.current_url}"
    print("설정 페이지 이동 성공:", driver.current_url)

    time.sleep(2)

    # 4. 구성원 관리 탭 클릭
    member_tab = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/users"][role="tab"]')
    ))
    member_tab.click()
    print("구성원 관리 탭 클릭 성공")
    time.sleep(3)

    # 5. 첫 번째 구성원 '제한 없음' 체크박스 클릭
    no_limit_checkbox = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'input[name="accountTokenQuotaList.0.quota.noLimit"][type="checkbox"]')
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", no_limit_checkbox)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", no_limit_checkbox)
    print("제한 없음 체크박스 클릭 성공")

    time.sleep(2)

    # 6. 체크박스 활성화 확인
    is_checked = driver.execute_script("return arguments[0].checked;", no_limit_checkbox)
    assert is_checked, "제한 없음 체크박스 활성화 실패"
    print("제한 없음 체크 완료!")
    time.sleep(2)

    # 7. 토큰 입력 필드가 비활성화(disabled) 됐는지 확인
    token_input = driver.find_element(
        By.CSS_SELECTOR, 'input[name="accountTokenQuotaList.0.quota.quantity"]'
    )
    assert not token_input.is_enabled(), "토큰 입력 필드 비활성화 실패"
    print("토큰 입력 필드 비활성화 확인 완료!")
    time.sleep(2)

    # 8. 제한 없음 체크박스 다시 클릭 (체크 해제)
    no_limit_checkbox2 = driver.find_element(
        By.CSS_SELECTOR, 'input[name="accountTokenQuotaList.0.quota.noLimit"][type="checkbox"]'
    )
    driver.execute_script("arguments[0].click();", no_limit_checkbox2)
    print("제한 없음 체크박스 해제 클릭 성공")
    time.sleep(2)

    # 9. 체크박스 해제 확인
    is_unchecked = driver.execute_script("return arguments[0].checked;", no_limit_checkbox2)
    assert not is_unchecked, "제한 없음 체크박스 해제 실패"
    print("제한 없음 체크 해제 완료!")
    time.sleep(2)

    # 10. 토큰 입력 필드가 다시 활성화됐는지 확인
    token_input2 = driver.find_element(
        By.CSS_SELECTOR, 'input[name="accountTokenQuotaList.0.quota.quantity"]'
    )
    assert token_input2.is_enabled(), "토큰 입력 필드 활성화 실패"
    print("토큰 입력 필드 활성화 확인 완료!")
    time.sleep(2)



if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
