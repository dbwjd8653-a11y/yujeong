"""[test_settings_02] 이용 내역"""

import pytest
from pages.settings_02_page import Settings02Page


@pytest.fixture(scope="module")
def settings02(login_module):
    driver, wait = login_module
    page = Settings02Page(driver, wait)
    page.navigate_to_settings()
    return page


def test_FHC_068_navigate_to_history_tab(settings02):
    """[FHC-068] 이용 내역 탭 이동 테스트"""
    settings02.navigate_to_history_tab()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
