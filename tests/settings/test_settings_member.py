"""[test_settings_05] 구성원 관리"""

import pytest
import time
from pages.settings.settings_member_page import Settings05Page


@pytest.fixture(scope="module")
def settings05(login_module):
    driver, wait = login_module
    page = Settings05Page(driver, wait)
    page.navigate_to_settings()
    page.navigate_to_member_tab()
    return page


# ========== FHC-072: 토큰 한도 토글 비활성화 ==========

def test_FHC_072_token_limit_disable(settings05):
    """[FHC-072] 토큰 한도 토글 비활성화 테스트"""
    toggle = settings05.get_toggle()
    settings05.ensure_toggle_enabled(toggle)
    settings05.click_toggle(toggle)
    assert not settings05.is_toggle_checked(toggle), "토큰 한도 토글 비활성화 실패"
    settings05.save_and_verify_toast()


# ========== FHC-073: 토큰 한도 토글 활성화 ==========

def test_FHC_073_token_limit_enable(settings05):
    """[FHC-073] 토큰 한도 토글 활성화 테스트"""
    toggle = settings05.get_toggle()
    settings05.click_toggle(toggle)
    assert settings05.is_toggle_checked(toggle), "토큰 한도 토글 활성화 실패"
    settings05.save_and_verify_toast()


# ========== FHC-074: 무제한 토큰 멤버 선택 ==========

def test_FHC_074_member_no_limit(settings05):
    """[FHC-074] 무제한 토큰 멤버 선택 테스트"""
    settings05.click_no_limit_checkbox()
    assert settings05.is_no_limit_checked(), "제한 없음 체크박스 활성화 실패"
    time.sleep(2)
    assert settings05.is_token_input_disabled(), "토큰 입력 필드 비활성화 실패"
    time.sleep(2)
    settings05.save_and_verify_toast()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
