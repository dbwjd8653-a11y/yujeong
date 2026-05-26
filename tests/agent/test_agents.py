# tests/test_agents_01.py
# 에이전트 탐색 기능 E2E 테스트 — FHC-064 ~ FHC-066

import pytest
import allure

from pages.agents.agents_page import AgentsPage
from pages.agents.agents_detail_page import AgentDetailPage
from pages.tools.base_tool_page import BaseToolPage

pytestmark = [
    allure.epic("Agent"),
    allure.feature("에이전트 탐색"),
]

TEST_MESSAGE = "안녕하세요, 간단히 소개해 주세요."


# ── fixtures ───────────────────────────────────────────────────────

@pytest.fixture
def logged_in_driver(tools_driver):
    """
    로그인 완료 상태 드라이버 반환

    전제: tools_driver fixture 브라우저 실행 상태
    단계:
      1. BaseToolPage.login() 실행
    """
    base = BaseToolPage(tools_driver)
    base.login()
    return tools_driver


@pytest.fixture
def agents_page(logged_in_driver):
    """로그인 후 에이전트 탐색 페이지 Page 객체"""
    return AgentsPage(logged_in_driver)


@pytest.fixture
def agent_detail_page(logged_in_driver):
    """로그인 후 에이전트 상세 페이지 Page 객체"""
    return AgentDetailPage(logged_in_driver)


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("에이전트 탐색 탭 확인")
@allure.title("[FHC-064] 에이전트 탐색 탭 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_064_agents_tab_click(agents_page):
    """
    [FHC-064] 에이전트 탐색 탭 확인

    전제: 로그인 한 상태
    단계:
      1. LNB > '에이전트 탐색' 탭 클릭
    기대: 맞춤형 AI 에이전트 목록이 표시된다
    """
    with allure.step("r: 로그인 완료 상태"):
        agents_page.navigate_to_base()
    with allure.step("g: 에이전트 탐색 탭 클릭 → 에이전트 목록 표시 확인"):
        agents_page.click_agents_tab_from_lnb()
        assert agents_page.is_agent_list_displayed(), \
            "에이전트 탐색 탭 클릭 후 에이전트 목록이 표시되지 않았습니다"


@allure.story("에이전트 기능 동작 확인")
@allure.title("[FHC-065] 에이전트 기능 동작 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_065_agent_features_displayed(agents_page, agent_detail_page):
    """
    [FHC-065] 에이전트 기능 동작 확인

    전제: 로그인 한 상태, '에이전트 탐색' 페이지
    단계:
      1. 에이전트 클릭 (랜덤)
    기대: 선택한 에이전트의 주요 기능이 표시된다
    """
    with allure.step("r: 에이전트 탐색 페이지 이동"):
        agents_page.open()
    with allure.step("g: 에이전트 클릭 (랜덤) → 주요 기능 표시 확인"):
        agent_name = agents_page.click_random_agent()
        assert agent_detail_page.is_main_features_displayed(), \
            f"에이전트 '{agent_name}' 클릭 후 주요 기능이 표시되지 않았습니다"


@allure.story("에이전트 대화창 버튼 방식 확인")
@allure.title("[FHC-066] 에이전트 대화창 버튼 방식 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_066_agent_chat_via_button(agents_page, agent_detail_page):
    """
    [FHC-066] 에이전트 대화창 확인 — 메뉴 버튼 클릭 방식

    전제: 로그인 한 상태, '에이전트 탐색' 페이지 > 에이전트 클릭
    단계:
      1. 퀵 리플라이 메뉴 버튼 선택
    기대:
      1. 적절한 AI 답변이 생성된다
      2. LNB 메뉴에 대화 내용이 표시된다
    """
    with allure.step("r: 에이전트 상세 페이지 이동"):
        agents_page.open()
        agents_page.click_first_agent()
    with allure.step("g: 퀵 리플라이 버튼 클릭 → AI 답변 생성 및 LNB 대화 표시 확인"):
        agent_detail_page.click_quick_reply(index=0)
        assert agent_detail_page.wait_for_ai_response(), \
            "AI 답변이 생성되지 않았습니다 (버튼 클릭 방식)"
        assert agent_detail_page.is_lnb_chatroom_visible(), \
            "LNB 메뉴에 대화 내용이 표시되지 않았습니다"

    # TODO: FHC-066 번호 중복 — 팀원과 번호 분리(FHC-067) 또는 통합 상의 후 처리
    # def test_FHC_066_agent_chat_via_text_input(agents_page, agent_detail_page):
    #     """
    #     [FHC-066] 에이전트 대화창 확인 — 텍스트 직접 입력 방식
    #
    #     전제: 로그인 한 상태, '에이전트 탐색' 페이지 > 에이전트 클릭
    #     단계:
    #       1. 채팅창에 텍스트 직접 입력 후 전송
    #     기대:
    #       1. 적절한 AI 답변이 생성된다
    #       2. LNB 메뉴에 대화 내용이 표시된다
    #     """
    #     agents_page.open()
    #     agents_page.click_first_agent()
    #     agent_detail_page.send_text_message(TEST_MESSAGE)
    #     assert agent_detail_page.wait_for_ai_response(), \
    #         "AI 답변이 생성되지 않았습니다 (직접 입력 방식)"
    #     assert agent_detail_page.is_lnb_chatroom_visible(), \
    #         "LNB 메뉴에 대화 내용이 표시되지 않았습니다"
