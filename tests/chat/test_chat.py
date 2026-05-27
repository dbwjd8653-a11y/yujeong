# tests/test_chat_01.py
# 메인 채팅 / 검색 / 대화 목록 E2E 테스트 — FHC-022 ~ FHC-027

import pytest
import allure

from pages.chat.chat_page import ChatPage

TEST_MESSAGE   = "오늘 마실 차를 추천해 주세요"
SEARCH_KEYWORD = "오늘"

pytestmark = [
    allure.epic("Chat"),
    allure.feature("채팅"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def chat(login_module):
    """
    ChatPage fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 driver 수신 → ChatPage 반환
    """
    driver, wait = login_module
    page = ChatPage(driver)
    page.open()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("새 대화 탭 확인")
@allure.title("[FHC-022] '새 대화' 탭 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_new_chat_tab_click(chat):
    """
    [FHC-022] '새 대화' 탭 확인

    전제: 로그인 한 상태
    단계:
      1. LNB > '새 대화' 탭 클릭
    기대: AI 대화창이 열린다 (Default: Helpy Pro Agent)
    """
    chat.click_new_chat_from_lnb()
    assert chat.is_chat_window_open(), \
        "새 대화 탭 클릭 후 채팅 입력 필드가 표시되지 않았습니다"
    assert chat.is_default_agent_helpy_pro(), \
        "새 대화창의 기본 에이전트가 Helpy Pro Agent가 아닙니다"


@allure.story("AI 대화 기능 테스트")
@allure.title("[FHC-023] AI 대화 기능 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_ai_chat_response(chat):
    """
    [FHC-023] AI 대화 기능 테스트

    전제: AI 대화창 표시 상태
    단계:
      1. 메시지 입력 후 전송
    기대: 적절한 AI 답변이 생성된다
    """
    chat.send_message(TEST_MESSAGE)
    assert chat.wait_for_ai_response(), \
        "메시지 전송 후 AI 답변이 생성되지 않았습니다"


@allure.story("검색 탭 확인")
@allure.title("[FHC-024] '검색' 탭 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_search_tab_click(chat):
    """
    [FHC-024] '검색' 탭 확인

    전제: 로그인 한 상태
    단계:
      1. LNB > '검색' 탭 클릭
    기대: 검색 창이 열린다
    """
    chat.click_search_from_lnb()
    assert chat.is_search_modal_open(), \
        "검색 탭 클릭 후 검색 창이 열리지 않았습니다"


@allure.story("검색 기능 테스트")
@allure.title("[FHC-025] 검색 기능 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_search_keyword_results(chat):
    """
    [FHC-025] 검색 기능 테스트

    전제: 검색 창 표시 상태
    단계:
      1. 검색 단어 입력
    기대: 검색 결과가 표시된다
    """
    chat.enter_search_keyword(SEARCH_KEYWORD)
    assert chat.is_search_results_displayed(), \
        f"'{SEARCH_KEYWORD}' 검색 후 결과가 표시되지 않았습니다"


@allure.story("검색 기존 대화 선택")
@allure.title("[FHC-026] '검색' 기능 — 기존 대화 선택")
@allure.severity(allure.severity_level.NORMAL)
def test_search_select_existing_chat(chat):
    """
    [FHC-026] '검색' 기능 — 기존 대화 선택

    전제: 검색 창 표시 상태 + 기존 대화가 있는 경우
    단계:
      1. 기존 대화 클릭 (랜덤)
    기대: 선택한 대화의 상세 화면으로 전환된다
    """
    chat.click_random_search_result()
    assert chat.is_chat_detail_displayed(), \
        "검색 결과 클릭 후 대화 상세 화면으로 전환되지 않았습니다"


@allure.story("대화 목록 확인")
@allure.title("[FHC-027] '대화 목록' 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_lnb_chat_list_click(chat):
    """
    [FHC-027] '대화 목록' 확인

    전제: 로그인 한 상태 + 기존 대화가 있는 경우
    단계:
      1. LNB > 기존 대화 목록 확인
      2. 목록 항목 클릭 (랜덤)
    기대: 선택한 대화의 상세 화면으로 전환된다
    """
    assert chat.is_lnb_chat_list_visible(), \
        "LNB에 기존 대화 목록이 표시되지 않습니다"
    chat.click_random_lnb_chat()
    assert chat.is_chat_detail_displayed(), \
        "LNB 대화 목록 클릭 후 대화 상세 화면으로 전환되지 않았습니다"
