"""[test_settings_01] 일반"""


import pytest
import time
from settings_page import SettingsPage


# =====================
# 테스트: 로그인 후 설정 페이지 이동
# =====================
def test_settings(login):
    driver, wait = login
    time.sleep(5)

    # 1. 설정 페이지 이동 (기어 클릭 → 드롭다운 설정 클릭 → URL 확인)
    SettingsPage(driver, wait).navigate_to_settings()



if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
