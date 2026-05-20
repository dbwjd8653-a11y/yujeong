"""[test_settings_03] 모델 설정"""

import pytest
from pages.settings.settings_model_page import Settings03Page


@pytest.fixture(scope="module")
def settings03(login_module):
    driver, wait = login_module
    page = Settings03Page(driver, wait)
    page.navigate_to_settings()
    page.navigate_to_models_tab()
    return page


def test_FHC_069_activate_model(settings03):
    """[FHC-069] 비활성화 모델 활성화 테스트"""
    settings03.activated_model = settings03.activate_disabled_model()
    assert settings03.activated_model is not None, "비활성화 모델이 없음"
    settings03.navigate_to_new_chat()
    settings03.open_agent_dropdown()
    titles = settings03.get_dropdown_model_titles()
    assert settings03.activated_model in titles, f"모델 추가 실패: '{settings03.activated_model}'"
    settings03.close_dropdown()


def test_FHC_070_deactivate_model(settings03):
    """[FHC-070] 활성화 모델 비활성화 테스트"""
    settings03.navigate_to_settings()
    settings03.navigate_to_models_tab()
    settings03.deactivate_model(settings03.activated_model)
    settings03.navigate_to_new_chat()
    settings03.open_agent_dropdown()
    titles = settings03.get_dropdown_model_titles()
    assert settings03.activated_model not in titles, f"모델 비활성화 실패: '{settings03.activated_model}'"
    settings03.close_dropdown()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
