# tests/test_mypage_08.py
# 마이페이지 > 언어 설정 E2E 테스트 — FHC-090 ~ FHC-092

import time
import pytest
import allure

from pages.mypage.mypage_language_page import MyPage08

pytestmark = [
    allure.epic("MyPage"),
    allure.feature("언어 설정"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def mypage(tools_driver_module):
    """
    MyPage08 fixture (모듈 공유)

    전제: tools_driver_module fixture로 로그인 완료 상태
    단계:
      1. tools_driver_module에서 driver 수신 → MyPage08 반환
    """
    page = MyPage08(tools_driver_module)
    page.login()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("언어 변경 국가 설정")
@allure.title("[FHC-090] 언어 변경 국가 설정")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_090_language_setting(mypage):
    """
    [FHC-090] 언어 변경 국가 설정

    전제: 로그인 상태
    단계:
      1. 마이페이지 → '언어 설정' 영역 클릭
      2. 변경할 언어 선택 (ko-KR → en-US)
    기대: 선택한 언어로 변경된다 ('Saved successfully' 메시지 출력)
        ※ 현재 언어와 무관하게 저장이 일어나도록 ko-KR 먼저 변경 후 en-US로 변경
    """
    mypage.navigate_to_language()
    assert mypage.is_language_setting_displayed(), \
        "언어 설정 드롭다운이 표시되지 않았습니다"
    mypage.change_language("ko-KR")
    time.sleep(1)
    mypage.change_language("en-US")
    assert mypage.is_saved_successfully_displayed(), \
        "언어 변경 후 'Saved successfully' 메시지가 표시되지 않았습니다"
    mypage.change_language("ko-KR")


@allure.story("언어 변경 후 로그아웃 로그인 페이지 언어")
@allure.title("[FHC-091] 언어 변경 후 로그아웃 로그인 페이지 언어")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_091_logout_shows_language_login_page(mypage):
    """
    [FHC-091] 언어 변경 후 로그아웃 시 로그인 페이지 언어 확인

    전제: 로그인 상태
    단계:
      1. 마이페이지 > 언어 설정 → 한국어 선택
      2. [로그아웃] 버튼 클릭
    기대: 로그아웃 후 설정한 언어(한국어)의 로그인 페이지로 이동한다
        ※ 로그인 페이지가 영어로 표시되면 Fail
    """
    mypage.navigate_to_language()
    mypage.change_language("ko-KR")
    mypage.logout_via_profile_menu()
    is_english = mypage.is_login_page_in_english()
    mypage.login()
    assert not is_english, \
        "로그아웃 후 로그인 페이지가 영어로 표시됩니다 (설정한 언어로 표시되어야 합니다)"


@allure.story("언어 변경 후 재로그인 언어 유지")
@allure.title("[FHC-092] 언어 변경 후 재로그인 언어 유지")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_092_language_maintained_after_relogin(mypage):
    """
    [FHC-092] 언어 변경 후 재로그인 시 언어 유지

    전제: 로그인 상태
    단계:
      1. 마이페이지 > 언어 설정 → 한국어 선택
      2. 로그아웃
      3. 재로그인
    기대: 재로그인 후 설정한 언어(한국어)가 유지된다
    """
    mypage.navigate_to_language()
    mypage.change_language("ko-KR")
    mypage.logout_via_profile_menu()
    mypage.login()
    assert mypage.is_language_maintained("ko-KR"), \
        "재로그인 후 언어 설정이 한국어(ko-KR)로 유지되지 않았습니다"
