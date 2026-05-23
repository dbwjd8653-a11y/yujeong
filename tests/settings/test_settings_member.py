# tests/settings/test_settings_member.py
# 설정 > 구성원 관리 탭 E2E 테스트 — FHC-072 ~ FHC-074

import pytest
import logging
import time
import allure
from pages.settings.settings_member_page import SettingsMemberPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Settings"),
    allure.feature("구성원 관리"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def settings_member(login_module):
    """
    설정 > 구성원 관리 페이지 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → SettingsMemberPage 반환
      2. 설정 페이지 이동
      3. 구성원 관리 탭 이동
    """
    driver, wait = login_module
    page = SettingsMemberPage(driver, wait)
    page.navigate_to_settings()
    page.navigate_to_member_tab()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("토큰 한도 토글 비활성화")
@allure.title("[FHC-072] 토큰 한도 토글 비활성화 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_072_token_limit_disable(settings_member):
    """
    [FHC-072] 토큰 한도 토글 비활성화 테스트

    전제: 로그인 완료 상태 (관리자 계정), 구성원 관리 탭 이동 완료
    단계:
      1. '구성원 관리' 탭 클릭
      2. '구성원 토큰 관리'에서 '토큰 한도' 토글 비활성화
      3. 왼쪽 하단에 '저장' 버튼 클릭
      4. '토큰 한도가 저장되었습니다.' 알림창 활성화
    기대: '토큰 한도가 저장되었습니다.' 알림창 활성화됨
    """
    logger.info("[FHC-072] 토큰 한도 토글 비활성화 시작")
    toggle = settings_member.get_toggle()
    settings_member.ensure_toggle_enabled(toggle)
    settings_member.click_toggle(toggle)
    assert not settings_member.is_toggle_checked(toggle), "토큰 한도 토글 비활성화 실패"
    settings_member.save_and_verify_toast()
    logger.info("[FHC-072] 토큰 한도 토글 비활성화 완료")


@allure.story("토큰 한도 토글 활성화")
@allure.title("[FHC-073] 토큰 한도 토글 활성화 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_073_token_limit_enable(settings_member):
    """
    [FHC-073] 토큰 한도 토글 활성화 테스트

    전제: test_FHC_072 이어서 토큰 한도 토글 비활성화 상태
    단계:
      1. '구성원 관리' 탭 클릭
      2. '구성원 토큰 관리'에서 '토큰 한도' 토글 활성화
      3. 왼쪽 하단에 '저장' 버튼 클릭
      4. '토큰 한도가 저장되었습니다.' 알림창 활성화
    기대: '토큰 한도가 저장되었습니다.' 알림창 활성화됨
    """
    logger.info("[FHC-073] 토큰 한도 토글 활성화 시작")
    toggle = settings_member.get_toggle()
    settings_member.click_toggle(toggle)
    assert settings_member.is_toggle_checked(toggle), "토큰 한도 토글 활성화 실패"
    settings_member.set_global_token("10")
    settings_member.save_and_verify_toast()
    logger.info("[FHC-073] 토큰 한도 토글 활성화 완료")


@allure.story("무제한 토큰 멤버 선택")
@allure.title("[FHC-074] 무제한 토큰 멤버 선택 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_074_member_no_limit(settings_member):
    """
    [FHC-074] 무제한 토큰 멤버 선택 테스트

    전제: test_FHC_073 이어서 토큰 한도 토글 활성화 상태
    단계:
      1. '구성원 관리' 탭 클릭
      2. '구성원 토큰 관리'에서 첫 번째 예외구성원에 '제한없음' 앞 네모박스 클릭
      3. 왼쪽 하단에 '저장' 버튼 클릭
      4. '토큰 한도가 저장되었습니다.' 알림창 활성화
    기대: 네모 박스가 보라색 'v' 표시로 활성화 되며 해당 위원의 '토큰 한도'는
          비활성화되며 '저장' 버튼 클릭 시 '토큰 한도가 저장되었습니다.' 알림창 활성화 됨
    """
    logger.info("[FHC-074] 무제한 토큰 멤버 선택 시작")
    settings_member.click_no_limit_checkbox()
    assert settings_member.is_no_limit_checked(), "제한 없음 체크박스 활성화 실패"
    time.sleep(2)
    assert settings_member.is_token_input_disabled(), "토큰 입력 필드 비활성화 실패"
    time.sleep(2)
    settings_member.save_and_verify_toast()
    logger.info("[FHC-074] 무제한 토큰 멤버 선택 완료")


if __name__ == "__main__":
    from tests.settings.settings_main import run
    run(__file__)
