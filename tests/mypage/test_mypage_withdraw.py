# tests/test_mypage_06.py
# 마이페이지 > 계정 관리 — 계정 탈퇴 E2E 테스트 — FHC-084 ~ FHC-086
# ※ FHC-086 계정 탈퇴 후 test_recreate_account_after_withdraw에서 동일 계정으로 재가입하여 복구

import pytest

from pages.mypage.mypage_withdraw_page import MyPage06

MAIN_EMAIL    = "test_dummy@naver.com"
MAIN_PASSWORD = "test@1234"
MAIN_NAME     = "포커스 테스트"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def mypage(tools_driver_module):
    """
    MyPage06 fixture (모듈 공유)

    전제: tools_driver_module fixture로 로그인 완료 상태
    단계:
      1. tools_driver_module에서 driver 수신 → MyPage06 반환
    """
    page = MyPage06(tools_driver_module)
    page.login()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

def test_FHC_084_withdraw_area_displayed(mypage):
    """
    [FHC-084] '계정 탈퇴' 영역 확인

    전제: 로그인 상태
    단계:
      1. 마이페이지 > 계정 관리 → 하단 '계정 탈퇴' 영역 이동
    기대: 탈퇴 안내 메시지와 [탈퇴하기] 버튼이 표시된다
    """
    mypage.navigate_to_account()
    mypage.scroll_to_withdraw_area()
    assert mypage.is_withdraw_area_displayed(), \
        "계정 탈퇴 영역 또는 [탈퇴하기] 버튼이 표시되지 않았습니다"


def test_FHC_085_withdraw_confirm_message(mypage):
    """
    [FHC-085] 계정 탈퇴 2차 확인 문구

    전제: 로그인 상태
    단계:
      1. 마이페이지 > 계정 관리 > 계정 탈퇴 영역 → [탈퇴하기] 버튼 클릭
    기대: 계정 탈퇴 메시지 표시
          > 계정을 탈퇴하려면 'Delete [이메일 아이디]'를 정확히 입력하세요
    """
    mypage.navigate_to_account()
    mypage.scroll_to_withdraw_area()
    mypage.click_withdraw_button()
    assert mypage.is_withdraw_confirm_message_displayed(), \
        "탈퇴하기 클릭 후 2차 확인 문구('Delete [이메일]' 입력 안내)가 표시되지 않았습니다"
    mypage.driver.back()


def test_FHC_086_withdraw_account(mypage):
    """
    [FHC-086] 계정 탈퇴

    전제: 로그인 상태
    단계:
      1. 마이페이지 > 계정 관리 > 계정 탈퇴 영역
      2. [탈퇴하기] 버튼 클릭
      3. 계정 탈퇴 2차 문구 입력
      4. [탈퇴하기] 버튼 클릭
    기대: 로그인 랜딩 페이지로 이동한다
    ※ test_recreate_account_after_withdraw에서 동일 계정으로 재가입하여 복구
    """
    mypage.navigate_to_account()
    mypage.scroll_to_withdraw_area()
    mypage.click_withdraw_button()
    mypage.enter_withdraw_confirm_text(MAIN_EMAIL)
    mypage.submit_withdraw()
    assert mypage.is_withdrawal_complete(), \
        "계정 탈퇴 후 로그인 랜딩 페이지로 이동하지 못했습니다"


def test_recreate_account_after_withdraw(mypage):
    """
    [인프라] 계정 생성 (탈퇴 후 재가입)

    전제: FHC-086 계정 탈퇴 후 → 로그인 페이지 상태
    단계:
      1. 회원가입 클릭
      2. 이메일로 가입하기
      3. 이메일/비밀번호/이름 기입
      4. 전체 동의 버튼 클릭
      5. 회원가입 버튼 클릭
    기대: 회원가입 후 헬피 챗 메인 페이지로 접속된다
    """
    mypage.driver.get(mypage.CHAT_URL)
    mypage.signup(MAIN_EMAIL, MAIN_PASSWORD, MAIN_NAME)
    assert mypage.is_signup_success(), \
        f"탈퇴 후 재가입 시 helpy-chat 메인 페이지로 이동하지 못했습니다 (이메일: {MAIN_EMAIL})"
