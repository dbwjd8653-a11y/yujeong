# tests/settings/test_settings_model.py
# 설정 > 모델 설정 탭 E2E 테스트 — FHC-069 ~ FHC-070

import pytest
import logging
import allure
from pages.settings.settings_model_page import SettingsModelPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Settings"),
    allure.feature("모델 설정"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def settings_model(login_module):
    """
    설정 > 모델 설정 페이지 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → SettingsModelPage 반환
      2. 설정 페이지 이동
      3. 모델 설정 탭 이동
    """
    driver, wait = login_module
    page = SettingsModelPage(driver, wait)
    page.navigate_to_settings()
    page.navigate_to_models_tab()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("비활성화 모델 활성화")
@allure.title("[FHC-069] 비활성화 모델 활성화 후 에이전트 모델 리스트 업데이트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_069_activate_model(settings_model):
    """
    [FHC-069] 비활성화 모델 활성화 후 에이전트 모델 리스트 업데이트

    전제: 로그인 완료 상태 (관리자 계정), 모델 설정 탭 이동 완료
    단계:
      1. '모델 설정' 클릭
      2. 비활성화 되어 있는 모델 하나를 활성화 시킴
      3. '모델이 활성화되었습니다.' 알림창 활성화
      4. '새 대화' 클릭
      5. 'Helpy Pro Agent' 클릭
      6. 활성화 시킨 모델이 리스트에서 추가되었는지 확인
    기대: 비활성화 → 활성화 한 모델을 'Helpy Pro Agent' 클릭 시 모델 추가됨을 확인
    """
    logger.info("[FHC-069] 비활성화 모델 활성화 시작")
    settings_model.activated_model = settings_model.activate_disabled_model()
    assert settings_model.activated_model is not None, "비활성화 모델이 없음"
    settings_model.navigate_to_new_chat()
    settings_model.open_agent_dropdown()
    titles = settings_model.get_dropdown_model_titles()
    assert settings_model.activated_model in titles, f"모델 추가 실패: '{settings_model.activated_model}'"
    settings_model.close_dropdown()
    logger.info("[FHC-069] 비활성화 모델 활성화 완료")


@allure.story("활성화 모델 비활성화")
@allure.title("[FHC-070] 활성화 모델 비활성화 후 에이전트 모델 리스트 업데이트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_070_deactivate_model(settings_model):
    """
    [FHC-070] 활성화 모델 비활성화 후 에이전트 모델 리스트 업데이트

    전제: test_FHC_069 이어서 모델 활성화 완료 상태
    단계:
      1. '모델 설정' 클릭
      2. 활성화 되어 있는 모델 하나를 비활성화 시킴
      3. '모델이 비활성화되었습니다.' 알림창 활성화
      4. '새 대화' 클릭
      5. 'Helpy Pro Agent' 클릭
      6. 활성화 시킨 모델이 리스트에서 삭제되었는지 확인
    기대: 활성화 → 비활성화 한 모델을 'Helpy Pro Agent' 클릭 시 모델 삭제됨을 확인
    """
    logger.info("[FHC-070] 활성화 모델 비활성화 시작")
    settings_model.navigate_to_settings()
    settings_model.navigate_to_models_tab()
    settings_model.deactivate_model(settings_model.activated_model)
    settings_model.navigate_to_new_chat()
    settings_model.open_agent_dropdown()
    titles = settings_model.get_dropdown_model_titles()
    assert settings_model.activated_model not in titles, f"모델 비활성화 실패: '{settings_model.activated_model}'"
    settings_model.close_dropdown()
    logger.info("[FHC-070] 활성화 모델 비활성화 완료")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
