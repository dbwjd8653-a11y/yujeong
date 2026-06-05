# 마이페이지 > 계정 관리 — 기본 정보 E2E 테스트 — FHC-080, FHC-083, FHC-088, FHC-089
# ※ FHC-081, 082 (인증), FHC-084~087 (계정보안/본인확인/소셜연결) 은 비자동화 항목

import pytest
import allure

from pages.mypage.mypage_account_page import MyPage05
from config.settings import MYPAGE_USER, MYPAGE_NEW_PASSWORD

pytestmark = [
    allure.epic("MyPage"),
    allure.feature("계정 관리"),
]

MAIN_EMAIL    = MYPAGE_USER["id"]
MAIN_PASSWORD = MYPAGE_USER["pw"]
NEW_PASSWORD  = MYPAGE_NEW_PASSWORD
NEW_NAME      = "포커스 테스트"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def mypage(tools_driver_module):
    """
    MyPage05 fixture (모듈 공유)

    전제: tools_driver_module fixture로 로그인 완료 상태
    단계:
      1. tools_driver_module에서 driver 수신 → MyPage05 반환
    """
    page = MyPage05(tools_driver_module)
    page.login()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("이름 변경")
@allure.title("[FHC-080] 이름 변경")
@allure.severity(allure.severity_level.NORMAL)
def test_change_name(mypage):
    """
    [FHC-080] 이름 변경

    전제: 로그인 상태
    단계:
      1. '계정 관리' 영역 클릭
      2. '이름' 옆 수정 버튼 클릭
      3. 새 이름 입력 후 저장
    기대: '저장되었습니다' 메시지 출력 후 이름 변경 적용됨
    """
    with allure.step("[FHC-080] 계정 관리 페이지 이동 후 이름 수정"):
        mypage.navigate_to_account()
        mypage.click_name_edit()
        mypage.enter_name(NEW_NAME)
        mypage.save_name()
    with allure.step("[FHC-080] 저장 성공 확인"):
        assert mypage.is_save_success_toast_displayed(), \
            "이름 변경 후 '저장되었습니다' 메시지가 표시되지 않았습니다"


@allure.story("비밀번호 변경")
@allure.title("[FHC-083] 비밀번호 변경")
@allure.severity(allure.severity_level.NORMAL)
def test_change_password(mypage):
    """
    [FHC-083] 비밀번호 변경

    전제: 로그인 상태
    단계:
      1. '계정 관리' 영역 클릭
      2. '비밀번호' 옆 수정 버튼 클릭
      3. 새 비밀번호 입력 후 저장
      4. 검증 후 원래 비밀번호로 복구
    기대: '저장되었습니다' 메시지 출력 후 비밀번호 변경 적용됨
    """
    with allure.step("[FHC-081] 계정 관리 페이지 이동 후 비밀번호 변경"):
        mypage.navigate_to_account()
        mypage.click_password_edit()
        mypage.change_password(MAIN_PASSWORD, NEW_PASSWORD)
    with allure.step("[FHC-081] 저장 성공 확인 후 원래 비밀번호 복구"):
        assert mypage.is_save_success_toast_displayed(), \
            "비밀번호 변경 후 '저장되었습니다' 메시지가 표시되지 않았습니다"
        mypage.navigate_to_account()
        mypage.click_password_edit()
        mypage.change_password(NEW_PASSWORD, MAIN_PASSWORD)


@allure.story("프로모션 알림 설정 변경")
@allure.title("[FHC-088] 프로모션 알림 설정 변경")
@allure.severity(allure.severity_level.NORMAL)
def test_toggle_promotion(mypage):
    """
    [FHC-088] 프로모션 알림 설정 변경

    전제: 로그인 상태
    단계:
      1. '프로모션 알림' 영역 이동
      2. '프로모션 알림 받기' 클릭
    기대: 프로모션 알림 토글 시 'Saved successfully' 메시지 출력 및 상태 변경됨
    """
    with allure.step("[FHC-082] 계정 관리 페이지 이동 후 프로모션 알림 토글"):
        mypage.navigate_to_account()
        before = mypage.get_promotion_state()
        mypage.toggle_promotion()
    with allure.step("[FHC-082] 저장 성공 및 상태 변경 확인"):
        assert mypage.is_saved_successfully_displayed(), \
            "프로모션 알림 토글 후 'Saved successfully' 메시지가 표시되지 않았습니다"
        after = mypage.get_promotion_state()
        assert before != after, \
            f"프로모션 알림 상태가 변경되지 않았습니다 (전: {before}, 후: {after})"


@allure.story("선호 언어 설정 변경")
@allure.title("[FHC-089] 선호 언어 설정 변경")
@allure.severity(allure.severity_level.NORMAL)
def test_change_language(mypage):
    """
    [FHC-089] 선호 언어 설정 변경

    전제: 로그인 상태
    단계:
      1. '선호 언어' 영역 이동
      2. 한국어(ko-KR) 선택
    기대: 언어 변경 및 'Saved successfully' 메시지 출력
    """
    with allure.step("[FHC-083] 계정 관리 페이지 이동 후 언어 변경 (ko-KR)"):
        mypage.navigate_to_account()
        mypage.change_language("ko-KR")
    with allure.step("[FHC-083] 저장 성공 확인"):
        assert mypage.is_saved_successfully_displayed(), \
            "언어 변경 후 'Saved successfully' 메시지가 표시되지 않았습니다"
