# tests/test_mypage_07.py
# 마이페이지 > 내 기관 E2E 테스트 — FHC-087 ~ FHC-089

import pytest
import allure

from pages.mypage.mypage_organization_page import MyPage07

pytestmark = [
    allure.epic("MyPage"),
    allure.feature("내 기관"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def mypage(tools_driver_module):
    """
    MyPage07 fixture (모듈 공유)

    전제: tools_driver_module fixture로 로그인 완료 상태
    단계:
      1. tools_driver_module에서 driver 수신 → MyPage07 반환
    """
    page = MyPage07(tools_driver_module)
    page.login()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("내 기관 UI 및 정보 표시")
@allure.title("[FHC-087] 내 기관 클릭 시 UI 및 정보 표시")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_087_org_info_displayed(mypage):
    """
    [FHC-087] 내 기관 클릭 시 UI 및 정보 표시

    전제: 로그인 상태
    단계:
      1. 마이페이지 > 계정 관리 → '내 기관' 영역 클릭
    기대: 내 기관 페이지 UI 및 정보가 표시된다
    """
    mypage.navigate_to_org()
    assert mypage.is_on_org_page(), \
        "내 기관 페이지로 이동하지 못했습니다"
    assert mypage.is_org_info_displayed(), \
        "내 기관 페이지에 UI 및 정보가 표시되지 않았습니다"


@allure.story("qa프로젝트 페이지 하이퍼링크 작동")
@allure.title("[FHC-088] qa프로젝트 페이지 하이퍼링크 작동")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_088_qaproject_link(mypage):
    """
    [FHC-088] qa프로젝트 페이지 하이퍼링크 작동

    전제: 로그인 상태
    단계:
      1. 마이페이지 > 계정 관리 → '내 기관' 영역 클릭
      2. 'qa 프로젝트' 영역 이동
      3. 'qaproject.elice.io 가기' 텍스트 클릭
    기대: AI 헬피 챗 메인 페이지가 새 탭으로 생성된다
    """
    mypage.navigate_to_org()
    original_handle  = mypage.driver.current_window_handle
    original_handles = mypage.driver.window_handles[:]
    mypage.click_qaproject_link()
    assert mypage.is_new_tab_opened(original_handles), \
        "qaproject 링크 클릭 후 새 탭이 열리지 않았습니다"
    mypage.close_new_tabs_and_return(original_handle)


@allure.story("헬프 센터 하이퍼링크 작동")
@allure.title("[FHC-089] 헬프 센터 하이퍼링크 작동")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_089_help_center_link(mypage):
    """
    [FHC-089] 헬프 센터 하이퍼링크 작동

    전제: 로그인 상태
    단계:
      1. 마이페이지 > 계정 관리 → '내 기관' 영역 클릭
      2. '헬프 센터' 영역 클릭
    기대: 헬프 센터 페이지가 새 탭으로 생성된다
    """
    mypage.navigate_to_org()
    original_handle  = mypage.driver.current_window_handle
    original_handles = mypage.driver.window_handles[:]
    mypage.click_help_center_link()
    assert mypage.is_new_tab_opened(original_handles), \
        "헬프 센터 링크 클릭 후 새 탭이 열리지 않았습니다"
    mypage.close_new_tabs_and_return(original_handle)
