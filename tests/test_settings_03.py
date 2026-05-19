"""[test_settings_03] 모델설정"""

import pytest
import time
from pages.settings_03_page import Settings03Page


# =====================
# 테스트: 모델 활성화/비활성화
# =====================
def test_settings(login):
    driver, wait = login
    time.sleep(5)

    page = Settings03Page(driver, wait)

    # 1. 설정 페이지 이동
    page.navigate_to_settings()

    # 2. 모델 설정 탭 클릭
    page.navigate_to_models_tab()

    # 3. 비활성화된 모델 하나 활성화
    activated_model = page.activate_disabled_model()
    assert activated_model, "비활성화된 모델을 찾지 못함"
    time.sleep(2)

    # 4. 새 대화 탭으로 이동 후 드롭다운에서 모델 확인
    page.navigate_to_new_chat()
    page.open_agent_dropdown()
    assert activated_model in page.get_dropdown_model_titles(), \
        f"모델 추가 실패: '{activated_model}'이 목록에 없음"
    time.sleep(2)

    # 5. 드롭다운 닫고 설정 페이지로 재이동
    page.close_dropdown()
    page.navigate_to_settings()

    # 6. 모델 설정 탭으로 이동 후 활성화한 모델 비활성화
    page.navigate_to_models_tab()
    page.deactivate_model(activated_model)
    time.sleep(2)

    # 7. 새 대화 탭으로 이동 후 드롭다운에서 모델 사라졌는지 확인
    page.navigate_to_new_chat()
    page.open_agent_dropdown()
    assert activated_model not in page.get_dropdown_model_titles(), \
        f"모델 비활성화 실패: '{activated_model}'이 아직 목록에 있음"
    time.sleep(2)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
