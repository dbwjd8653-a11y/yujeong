# 에이전트 탐색 기능 E2E 테스트 — FHC-065 ~ FHC-067

import pytest
import allure

from pages.agents.agents_page import AgentsPage
from pages.agents.agents_detail_page import AgentDetailPage
from pages.tools.base_tool_page import BaseToolPage

pytestmark = [
    allure.epic("Agent"),
    allure.feature("에이전트 탐색"),
]


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
@allure.title("[FHC-065] 에이전트 탐색 탭 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_agents_tab_click(agents_page):
    """
    [FHC-065] 에이전트 탐색 탭 확인

    전제: 로그인 한 상태
    단계:
      1. LNB > '에이전트 탐색' 탭 클릭
    기대: 맞춤형 AI 에이전트 목록이 표시된다
    """
    with allure.step("[FHC-065] 에이전트 탐색 탭 클릭"):
        agents_page.navigate_to_base()
        agents_page.click_agents_tab_from_lnb()
    with allure.step("[FHC-065] 에이전트 목록 표시 확인"):
        assert agents_page.is_agent_list_displayed(), \
            "에이전트 탐색 탭 클릭 후 에이전트 목록이 표시되지 않았습니다"


@allure.story("에이전트 기능 동작 확인")
@allure.title("[FHC-066] 에이전트 기능 동작 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_agent_features_displayed(agents_page, agent_detail_page):
    """
    [FHC-066] 에이전트 기능 동작 확인

    전제: 로그인 한 상태, '에이전트 탐색' 페이지
    단계:
      1. 에이전트 클릭 (랜덤)
    기대: 선택한 에이전트의 주요 기능이 표시된다
    """
    with allure.step("[FHC-066] 에이전트 탐색 페이지에서 에이전트 클릭 (랜덤)"):
        agents_page.open()
        agent_name = agents_page.click_random_agent()
    with allure.step("[FHC-066] 에이전트 주요 기능 표시 확인"):
        assert agent_detail_page.is_main_features_displayed(), \
            f"에이전트 '{agent_name}' 클릭 후 주요 기능이 표시되지 않았습니다"


@allure.story("에이전트 대화창 확인")
@allure.title("[FHC-067] 에이전트 대화창 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_agent_chat_via_button(agents_page, agent_detail_page):
    """
    [FHC-067] 에이전트 대화창 확인

    전제: 로그인 한 상태, '에이전트 마켓플레이스' 페이지
    단계:
      1. '네이티브 영어 번역 코치' 에이전트 클릭
      2. 퀵 리플라이 프롬프트 버튼 중 하나 클릭
    기대: 적절한 AI 답변이 생성된다
    """
    AGENT_NAME = "네이티브 영어 번역 코치"
    with allure.step(f"[FHC-067] '{AGENT_NAME}' 진입 후 퀵 리플라이 버튼 클릭"):
        agents_page.open()
        agents_page.click_agent_by_name(AGENT_NAME)
        agent_detail_page.click_quick_reply(index=0)
    with allure.step("[FHC-067] AI 답변 생성 확인"):
        assert agent_detail_page.wait_for_ai_response(), \
            "퀵 리플라이 클릭 후 AI 답변이 생성되지 않았습니다"
