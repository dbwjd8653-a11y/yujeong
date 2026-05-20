"""[tc_01] 설정 > 탭 클릭 부하 테스트"""

import pytest
from pages.performance.settings_load_page import Tc01Page


@pytest.fixture(scope="module")
def tc01(login_module):
    driver, wait = login_module
    page = Tc01Page(driver, wait)
    page.navigate_to_settings()
    return page


def test_tab_load(tc01):
    """[tc_01] 탭 순서대로 3번 반복 클릭 부하 테스트"""
    tc01.click_all_tabs_three_times()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
