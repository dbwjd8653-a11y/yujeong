"""[test_settings_04] 구독 관리"""

import pytest
from pages.settings_04_page import Settings04Page


@pytest.fixture(scope="module")
def settings04(login_module):
    driver, wait = login_module
    page = Settings04Page(driver, wait)
    page.navigate_to_settings()
    return page


def test_FHC_071_navigate_to_subscription_tab(settings04):
    """[FHC-071] 구독 관리 탭 이동 테스트"""
    settings04.navigate_to_subscription_tab()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
