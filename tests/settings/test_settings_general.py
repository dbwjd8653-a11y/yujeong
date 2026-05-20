"""[test_settings_01] 일반"""

import pytest
from pages.settings.settings_general_page import SettingsPage


@pytest.fixture(scope="module")
def settings01(login_module):
    driver, wait = login_module
    return SettingsPage(driver, wait)


def test_FHC_067_navigate_to_settings(settings01):
    """[FHC-067] 설정 페이지 이동 테스트"""
    settings01.navigate_to_settings()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
