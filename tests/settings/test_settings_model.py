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

@allure.story("비활성화 모델 활성화 토글 작동")
@allure.title("[FHC-069] 비활성화 모델 활성화 토글 작동 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_069_activate_model(settings_model):
    """
    [FHC-069] 비활성화 모델 활성화 토글 작동 확인

    전제: 헬피챗 접속, 로그인 완료 (관리자 계정), 오른쪽 상단 톱니바퀴 '설정' 클릭 > '설정' 클릭
    단계:
      1. '모델 설정' 클릭
      2. 비활성화 되어 있는 모델 하나를 활성화 시킴
    기대: '모델이 활성화되었습니다.' 알림창 활성화 됨
    """
    logger.info("[FHC-069] 비활성화 모델 활성화 시작")
    model_name = settings_model.activate_disabled_model()
    assert model_name is not None, "비활성화 모델이 없음"
    toast = settings_model.get_toast_message()
    assert toast == "모델이 활성화되었습니다.", f"알림창 메시지 불일치: '{toast}'"
    logger.info("[FHC-069] 비활성화 모델 활성화 완료")


@allure.story("활성화 모델 비활성화 토글 작동")
@allure.title("[FHC-070] 활성화 모델 비활성화 토글 작동 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_070_deactivate_model(settings_model):
    """
    [FHC-070] 활성화 모델 비활성화 토글 작동 테스트

    전제: FHC-069 완료 후 모델 설정 탭 유지 상태 (활성화된 모델 존재)
    단계:
      1. 활성화 되어 있는 모델 하나를 비활성화 시킴
    기대: '모델이 비활성화되었습니다.' 알림창 활성화 됨
    """
    logger.info("[FHC-070] 활성화 모델 비활성화 시작")
    model_name = settings_model.deactivate_active_model()
    assert model_name is not None, "활성화된 모델이 없음"
    toast = settings_model.get_toast_message()
    assert toast == "모델이 비활성화되었습니다.", f"알림창 메시지 불일치: '{toast}'"
    logger.info("[FHC-070] 활성화 모델 비활성화 완료")
