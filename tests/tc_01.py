"""[tc_01] 설정 > 탭 클릭 부하 테스트"""



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

    # 8~12. 탭 순서대로 3번 반복 클릭 (부하 테스트)
    for i in range(3):
        print(f"\n=== {i + 1}번째 반복 시작 ===")

        # 일반 탭
        general_tab = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/general"][role="tab"]')
        ))
        general_tab.click()
        print("일반 탭 클릭 성공")
        time.sleep(0.5)

        # 이용 내역 탭
        history_tab = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/history"][role="tab"]')
        ))
        history_tab.click()
        print("이용 내역 탭 클릭 성공")
        time.sleep(0.5)

        # 모델 설정 탭
        models_tab = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/models"][role="tab"]')
        ))
        models_tab.click()
        print("모델 설정 탭 클릭 성공")
        time.sleep(0.5)

        # 구독 관리 탭
        subscription_tab = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/subscription"][role="tab"]')
        ))
        subscription_tab.click()
        print("구독 관리 탭 클릭 성공")
        time.sleep(0.5)

        # 구성원 관리 탭
        member_tab = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/admin/users"][role="tab"]')
        ))
        member_tab.click()
        print("구성원 관리 탭 클릭 성공")
        time.sleep(0.5)

        print(f"=== {i + 1}번째 반복 완료 ===")

    print("\n부하 테스트 완료!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
