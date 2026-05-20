"""[test_settings_01] 일반"""


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



if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
