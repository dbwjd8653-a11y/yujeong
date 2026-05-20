# tests/test_mypage_09.py
# 마이페이지 > 고객 센터 E2E 테스트 — FHC-093

import pytest

from pages.mypage.mypage_support_page import MyPage09


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def mypage(tools_driver_module):
    """
    MyPage09 fixture (모듈 공유)

    전제: tools_driver_module fixture로 로그인 완료 상태
    단계:
      1. tools_driver_module에서 driver 수신 → MyPage09 반환
    """
    page = MyPage09(tools_driver_module)
    page.login()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

def test_FHC_093_customer_service_ai(mypage):
    """
    [FHC-093] 고객 센터 AI 작동

    전제: 로그인 상태
    단계:
      1. 마이페이지 → '고객 센터' 영역 클릭
      2. 'Start a chat' 영역 클릭
    기대: 설정된 AI 답변이 표시된다
    """
    mypage.navigate_to_support()
    mypage.click_start_chat()
    assert mypage.is_chat_ai_displayed(), \
        "'Start a chat' 클릭 후 AI 답변이 표시되지 않았습니다"
